import mysql.connector
from contextlib import contextmanager
from backend.loggin_setup import setup_logger


logger = setup_logger("db_helper")

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="YOURUSER",
        password="YOURPASSWORD",
        database="expense_manager",

    )

    # if connection.is_connected():
    #     print("Connection successful")
    # else:
    #     print("Failed to connect to a database")

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        for expense in expenses:
            print(expense)


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expenses called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                       (expense_date, amount, category, notes)
                       )


def delete_expense_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date}, end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total
               FROM expense_manager.expenses WHERE expense_date BETWEEN %s and %s
               GROUP BY category; ''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_monthly_expense_summary():
    """
    Return all expenses aggregated by month in ascending order,
    with a human-readable month label (e.g. 'August 2024').

    Output sample:
        [{'year_month': '2024-08',
          'month_label': 'August 2024',
          'total': 123.45}, …]
    """
    logger.info("fetch_monthly_expense_summary called (full history)")

    query = """
        SELECT  DATE_FORMAT(expense_date, '%M') AS month_name ,   -- 'August'
        SUM(amount)                     AS total
FROM    expense_manager.expenses
GROUP BY MONTH(expense_date),                       -- 8, 9, …
         DATE_FORMAT(expense_date, '%M')            -- 'August', 'September'
ORDER BY MONTH(expense_date);                       -- Jan → Dec order
    """

    with get_db_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

# if __name__ == "__main__":
#     monthly_summary = fetch_monthly_expense_summary()
#     print(monthly_summary)
#     data = {
#         "Month Name": (monthly_summary.keys()),
#         "Total": [monthly_summary["month_name"]["total"] for _ in monthly_summary],
#     }
#     print(data)
#     # fetch_all_records()
# #     expenses = fetch_expenses_for_date("2024-09-30")
# #     print(expenses)
# # #     # insert_expense("2024-08-25", 40, "Food", "Ate Tasty Samosa Chat")
# # #     # delete_expense_for_date("2024-08-25")
# #     summary = fetch_expense_summary("2024-08-01", "2024-08-05")
# #
# #     for record in summary:
# #        print(record)


# expenses = fetch_expenses_for_date('2024-08-15')
# print(len(expenses))

