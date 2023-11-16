import sqlite3
import calendar
from datetime import datetime, date

# Create a database connection
conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()

# Create expenses table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        date DATE NOT NULL
    )
''')
conn.commit()

def add_expense(description, amount, date_str):
    date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
    cursor.execute('INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)',
                   (description, amount, date_object))
    conn.commit()

def get_monthly_report(year, month):
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])

    cursor.execute('''
        SELECT description, amount, date
        FROM expenses
        WHERE date BETWEEN ? AND ?
    ''', (start_date, end_date))

    expenses = cursor.fetchall()
    return expenses

def print_report(year, month, expenses):
    month_name = calendar.month_name[month]
    total_expenses = sum(expense[1] for expense in expenses)

    print(f"----- {month_name} {year} Expense Report -----")
    for expense in expenses:
        print(f"{expense[2]} - {expense[0]}: ${expense[1]:.2f}")

    print(f"Total Expenses: ${total_expenses:.2f}")

def main():
    while True:
        print("\n1. Add Expense\n2. View Monthly Report\n3. Exit")
        choice = input("Select an option (1/2/3): ")

        if choice == '1':
            description = input("Enter expense description: ")
            amount = float(input("Enter expense amount: "))
            date_str = input("Enter expense date (YYYY-MM-DD): ")
            add_expense(description, amount, date_str)
            print("Expense added successfully!")

        elif choice == '2':
            year = int(input("Enter year: "))
            month = int(input("Enter month (1-12): "))
            expenses = get_monthly_report(year, month)
            print_report(year, month, expenses)

        elif choice == '3':
            print("Exiting Expense Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
