import os
from expense import Expense


def main():
    print(f"💸 Running Expense Tracker!")
    expense_file_path = "D:\\Documents\\HTML Files\\python\\Expense Tracker\\expenses.csv"
    # expense = get_user_expense()
    # save_expense_to_file(expense, expense_file_path)
    summarize_expenses(expense_file_path)


def get_user_expense():
    print(f"💸 Get User Expense ")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    print(f"You've entered {expense_name}, {expense_amount}")

    expense_categories = ["🥙 Food", "🏠 House", "⛽ Work", "😝 Fun", "✨ Misc"]

    while True:
        print("Select a Category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        try:
            selected_index = int(
                input(f"Enter a Category Number {value_range}: ")) - 1
        except Exception:
            pass

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid Category. Please Try again")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"💸 Save Expense to File: {expense} to {expense_file_path}")
    abs_path = os.path.abspath(expense_file_path)
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name}, PHP{expense.amount}, {expense.category}\n")


def summarize_expenses(expense_file_path):
    print(f"💸 Summarize Expenses")
    expenses: list[Expense] = []

    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, amount_with_currency, expense_category = line.strip().split(",")
            expense_amount = float(amount_with_currency.replace(
                "PHP", "").strip())  # Fix here

            line_expense = Expense(
                name=expense_name, amount=expense_amount, category=expense_category
            )

            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print(amount_by_category)


if __name__ == "__main__":
    main()
