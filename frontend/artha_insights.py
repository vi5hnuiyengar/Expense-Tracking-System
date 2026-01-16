"""
Artha Insights - Financial wisdom inspired by Sanskrit tradition.

'Artha' (अर्थ) is one of the four Puruṣārthas - the aims of human life in Hindu philosophy.
It represents prosperity, wealth, and economic security pursued ethically.

This module computes a "Lakshmi Score" (financial health metric) and pairs spending
insights with relevant Sanskrit wisdom from texts like Arthaśāstra and Cāṇakya Nīti.
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import random

API_URL = "http://localhost:8000"

# ─────────────────────────────────────────────────────────────────────────────
# SANSKRIT WISDOM DATABASE
# Curated shlokas on wealth, savings, and prudent living
# ─────────────────────────────────────────────────────────────────────────────

ARTHA_WISDOM = [
    {
        "sanskrit": "अर्थस्य मूलं राज्यं",
        "transliteration": "arthasya mūlaṃ rājyaṃ",
        "translation": "The foundation of wealth is governance (self-discipline).",
        "source": "Kauṭilya's Arthaśāstra 1.7",
        "context": "savings_high"
    },
    {
        "sanskrit": "उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः",
        "transliteration": "udyamena hi sidhyanti kāryāṇi na manorathaiḥ",
        "translation": "Tasks are accomplished through effort, not by wishful thinking.",
        "source": "Cāṇakya Nīti 16.4",
        "context": "general"
    },
    {
        "sanskrit": "अनागतविधाता च प्रत्युत्पन्नमतिस्तथा",
        "transliteration": "anāgatavidhātā ca pratyutpannamatistathā",
        "translation": "One who plans for the future and thinks quickly in the present [succeeds].",
        "source": "Pañcatantra 1.41",
        "context": "savings_high"
    },
    {
        "sanskrit": "अल्पानामपि वस्तूनां संहतिः कार्यसाधिका",
        "transliteration": "alpānāmapi vastūnāṃ saṃhatiḥ kāryasādhikā",
        "translation": "Even small things, when accumulated, accomplish great tasks.",
        "source": "Cāṇakya Nīti 15.14",
        "context": "small_savings"
    },
    {
        "sanskrit": "अर्थनाशं मनस्तापं गृहे दुश्चरितानि च। वञ्चनं चापमानं च मतिमान्न प्रकाशयेत्॥",
        "transliteration": "arthanāśaṃ manastāpaṃ gṛhe duścaritāni ca | vañcanaṃ cāpamānaṃ ca matimānna prakāśayet ||",
        "translation": "A wise person does not reveal: loss of wealth, mental anguish, household troubles, deception, or dishonor.",
        "source": "Cāṇakya Nīti 7.2",
        "context": "overspending"
    },
    {
        "sanskrit": "अर्थातुराणां न सुहृन्न बन्धुः",
        "transliteration": "arthāturāṇāṃ na suhṛnna bandhuḥ",
        "translation": "Those desperate for money have neither friends nor family.",
        "source": "Vidura Nīti (Mahābhārata)",
        "context": "overspending"
    },
    {
        "sanskrit": "सर्वे गुणाः काञ्चनमाश्रयन्ति",
        "transliteration": "sarve guṇāḥ kāñcanamāśrayanti",
        "translation": "All virtues depend on gold (financial security).",
        "source": "Cāṇakya Nīti 5.3",
        "context": "general"
    },
    {
        "sanskrit": "धनेन किं यो न ददाति नाश्नुते",
        "transliteration": "dhanena kiṃ yo na dadāti nāśnute",
        "translation": "What use is wealth if one neither gives nor enjoys it?",
        "source": "Subhāṣita",
        "context": "balanced"
    },
    {
        "sanskrit": "आयादधिकं व्ययं कुर्वन् अधमो जायते नरः",
        "transliteration": "āyādadhikaṃ vyayaṃ kurvan adhamo jāyate naraḥ",
        "translation": "One who spends more than their income becomes degraded.",
        "source": "Vidura Nīti",
        "context": "overspending"
    },
    {
        "sanskrit": "धनानि जीवितं चैव परार्थे प्राज्ञ उत्सृजेत्",
        "transliteration": "dhanāni jīvitaṃ caiva parārthe prājña utsṛjet",
        "translation": "The wise person sacrifices wealth and even life for a higher purpose.",
        "source": "Vidura Nīti",
        "context": "charitable"
    },
]


def get_wisdom_for_context(context: str) -> dict:
    """Return a shloka appropriate for the user's financial context."""
    relevant = [w for w in ARTHA_WISDOM if w["context"] == context]
    if not relevant:
        relevant = [w for w in ARTHA_WISDOM if w["context"] == "general"]
    return random.choice(relevant)


def compute_lakshmi_score(breakdown: dict) -> tuple[int, str, str]:
    """
    Compute the Lakshmi Score (0-100) based on spending patterns.

    Factors:
    - Mandatory vs. discretionary ratio
    - Diversification across categories
    - Presence of savings-friendly patterns

    Returns: (score, grade, insight)
    """
    if not breakdown:
        return 50, "Unrated", "No spending data available for analysis."

    mandatory = {"rent", "mortgage", "utilities", "insurance", "taxes", "groceries", "healthcare"}

    total = sum(cat_data["total"] for cat_data in breakdown.values())
    if total == 0:
        return 50, "Unrated", "No spending recorded."

    # Calculate mandatory vs discretionary
    mandatory_total = sum(
        cat_data["total"] for cat, cat_data in breakdown.items()
        if cat.lower() in mandatory
    )
    discretionary_total = total - mandatory_total

    mandatory_ratio = mandatory_total / total if total > 0 else 0
    discretionary_ratio = discretionary_total / total if total > 0 else 0

    # Base score starts at 50
    score = 50

    # Reward higher mandatory ratio (essentials focus) - up to +25
    score += int(mandatory_ratio * 25)

    # Reward diversification (not putting all eggs in one basket) - up to +15
    num_categories = len(breakdown)
    if num_categories >= 5:
        score += 15
    elif num_categories >= 3:
        score += 10
    else:
        score += 5

    # Penalize if one discretionary category dominates (>40% of total) - up to -15
    for cat, cat_data in breakdown.items():
        if cat.lower() not in mandatory:
            if cat_data["percentage"] > 40:
                score -= 15
                break
            elif cat_data["percentage"] > 30:
                score -= 8
                break

    # Bonus for having low discretionary spending (<30%) - up to +10
    if discretionary_ratio < 0.3:
        score += 10
    elif discretionary_ratio < 0.5:
        score += 5

    # Clamp score
    score = max(0, min(100, score))

    # Determine grade and context
    if score >= 85:
        grade = "Kuber"  # God of wealth
        context = "savings_high"
        insight = "Excellent financial discipline. Your spending reflects the wisdom of the ancients."
    elif score >= 70:
        grade = "Śreṣṭha"  # Excellent
        context = "balanced"
        insight = "Strong financial health. You balance necessities with mindful discretionary spending."
    elif score >= 55:
        grade = "Madhyama"  # Middle
        context = "general"
        insight = "Moderate financial health. Consider reviewing discretionary categories for optimization."
    elif score >= 40:
        grade = "Sādhāraṇa"  # Ordinary
        context = "small_savings"
        insight = "Room for improvement. Small, consistent changes can significantly impact your score."
    else:
        grade = "Cintanīya"  # Needs thought
        context = "overspending"
        insight = "Financial attention needed. Consider the wisdom: spend less than you earn."

    return score, grade, insight, context


def render_score_gauge(score: int, grade: str):
    """Render a visual gauge for the Lakshmi Score."""
    # Color based on score
    if score >= 85:
        color = "#FFD700"  # Gold
    elif score >= 70:
        color = "#90EE90"  # Light green
    elif score >= 55:
        color = "#87CEEB"  # Sky blue
    elif score >= 40:
        color = "#FFA500"  # Orange
    else:
        color = "#FF6B6B"  # Red

    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border-radius: 16px; margin-bottom: 1rem; border: 1px solid {color}40;">
        <div style="font-size: 0.9rem; color: #888; margin-bottom: 0.5rem; letter-spacing: 2px;">
            LAKSHMI SCORE
        </div>
        <div style="font-size: 4rem; font-weight: 700; color: {color}; line-height: 1;">
            {score}
        </div>
        <div style="font-size: 1.2rem; color: {color}; margin-top: 0.5rem; font-style: italic;">
            {grade}
        </div>
        <div style="margin-top: 1rem; height: 8px; background: #333; border-radius: 4px; overflow: hidden;">
            <div style="width: {score}%; height: 100%; background: {color};
                        transition: width 0.5s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_wisdom_card(wisdom: dict):
    """Render a Sanskrit wisdom card."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2d1b4e 0%, #1a1a2e 100%);
                padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                border-left: 4px solid #9b59b6;">
        <div style="font-size: 1.4rem; color: #f4d03f; margin-bottom: 0.75rem;
                    font-family: 'Noto Sans Devanagari', sans-serif;">
            {wisdom['sanskrit']}
        </div>
        <div style="font-size: 0.9rem; color: #bbb; font-style: italic; margin-bottom: 0.75rem;">
            {wisdom['transliteration']}
        </div>
        <div style="font-size: 1rem; color: #fff; margin-bottom: 0.75rem; line-height: 1.5;">
            "{wisdom['translation']}"
        </div>
        <div style="font-size: 0.8rem; color: #888; text-align: right;">
            — {wisdom['source']}
        </div>
    </div>
    """, unsafe_allow_html=True)


def artha_insights_tab():
    """Main tab for Artha Insights."""
    st.header("Artha Insights")
    st.markdown("""
    <div style="color: #888; margin-bottom: 1.5rem; font-size: 0.95rem;">
        <em>अर्थ (Artha)</em> — Prosperity and economic security, one of the four aims of life.
        <br/>Analyze your spending through the lens of ancient Indian wisdom.
    </div>
    """, unsafe_allow_html=True)

    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Analyze from",
            value=datetime.today().replace(day=1) - timedelta(days=30),
            key="artha_start"
        )
    with col2:
        end_date = st.date_input(
            "To",
            value=datetime.today(),
            key="artha_end"
        )

    if st.button("Generate Insights", type="primary"):
        # Fetch analytics data
        try:
            resp = requests.post(
                f"{API_URL}/analytics",
                json={"start_date": str(start_date), "end_date": str(end_date)},
                timeout=5
            )
        except requests.exceptions.RequestException as e:
            st.error(f"Cannot reach API: {e}")
            return

        if resp.status_code != 200:
            st.error("Could not fetch spending data. Add some expenses first!")
            return

        breakdown = resp.json()

        if not breakdown:
            st.warning("No expenses found in this date range.")
            return

        # Compute Lakshmi Score
        score, grade, insight, context = compute_lakshmi_score(breakdown)

        # Layout: Score on left, Wisdom on right
        col_score, col_wisdom = st.columns([1, 1])

        with col_score:
            render_score_gauge(score, grade)
            st.markdown(f"""
            <div style="text-align: center; color: #ccc; font-size: 0.95rem; padding: 0 1rem;">
                {insight}
            </div>
            """, unsafe_allow_html=True)

        with col_wisdom:
            st.markdown("#### Wisdom for You")
            wisdom = get_wisdom_for_context(context)
            render_wisdom_card(wisdom)

        # Spending breakdown
        st.markdown("---")
        st.markdown("#### Spending Breakdown")

        # Sort by total descending
        sorted_cats = sorted(breakdown.items(), key=lambda x: x[1]["total"], reverse=True)

        mandatory = {"rent", "mortgage", "utilities", "insurance", "taxes", "groceries", "healthcare"}

        for cat, data in sorted_cats:
            is_mandatory = cat.lower() in mandatory
            icon = "🏠" if is_mandatory else "💸"
            bar_color = "#4a9eff" if is_mandatory else "#ff6b6b"

            st.markdown(f"""
            <div style="margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span>{icon} {cat}</span>
                    <span style="color: #888;">${data['total']:.2f} ({data['percentage']:.1f}%)</span>
                </div>
                <div style="height: 6px; background: #333; border-radius: 3px; overflow: hidden;">
                    <div style="width: {data['percentage']}%; height: 100%; background: {bar_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Daily wisdom (bonus)
        st.markdown("---")
        st.markdown("#### Today's Wisdom")
        daily_wisdom = random.choice(ARTHA_WISDOM)
        render_wisdom_card(daily_wisdom)
