from datetime import date

from tenacity import retry_if_exception

from backend import db_helper
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import math
app = FastAPI()


class Expense(BaseModel):
    # expense_date: date
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

@app.get("/expenses/{expense_date}", response_model = List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    db_helper.delete_expense_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message": "Expense updated successfully"}


@app.post("/analytics")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")

    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total']/total)*100 if total !=0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage,
        }

    return breakdown


@app.get("/analytics/monthly")
def get_monthly_analytics():
    data = db_helper.fetch_monthly_expense_summary()
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve monthly analytics.")
    return data

class SavingsRequest(BaseModel):
    target: float          # $ you want to put aside
    start_date: date
    end_date: date
    period: str            # "week" or "month"

class SavingsAdvice(BaseModel):
    category: str
    save_per_period: float
    period: str
    num_periods: int

@app.post("/savings_plan", response_model=SavingsAdvice)
def savings_plan(req: SavingsRequest):
    """
    Suggest trimming the largest *discretionary* category to reach a target.
    Mandatory categories (rent, mortgage, utilities, insurance, taxes) are skipped.
    """
    mandatory = {"rent", "mortgage", "utilities", "insurance", "taxes"}

    # 1. totals per category for the requested window
    summary = db_helper.fetch_expense_summary(req.start_date, req.end_date)
    if not summary:
        raise HTTPException(status_code=404, detail="No expenses in that range.")

    # 2. pick the biggest discretionary sink
    discretionary = [row for row in summary
                     if row["category"].lower() not in mandatory and row["total"] > 0]
    if not discretionary:
        raise HTTPException(
            status_code=400,
            detail="No discretionary spending found to cut. Nice job!"
        )

    top = max(discretionary, key=lambda r: r["total"])

    # 3. how many weeks or months in the window?
    days = (req.end_date - req.start_date).days or 1
    if req.period == "week":
        periods = math.ceil(days / 7)
    else:  # month
        periods = ((req.end_date.year - req.start_date.year) * 12 +
                   req.end_date.month - req.start_date.month + 1)

    # 4. dollars to set aside each period
    save_each = round(req.target / periods, 2)

    return SavingsAdvice(
        category=top["category"],
        save_per_period=save_each,
        period=req.period,
        num_periods=periods,
    )