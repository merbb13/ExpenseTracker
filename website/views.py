from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from .expense import db
from .models import Expense, Income

views = Blueprint('views', __name__)
today = datetime.now().date()


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        typeofexpense = request.form.get('typeOfExpense')
        amount = request.form.get('amount')
        category = request.form.get('category')
        desc = request.form.get('description')

        if not typeofexpense:
            flash("Please select the type of expense!", category='error')
        elif not amount:
            flash("Please enter the amount!", category='error')
        elif not category:
            flash("Please select the category!", category='error')
        elif not desc:
            flash("Please enter the description!", category='error')
        else:
            if typeofexpense == 'expense':
                new_expense = Expense(
                    name=desc, category=category, amount=amount, user_id=current_user.id, date=datetime.utcnow())
                db.session.add(new_expense)
                db.session.commit()
                flash("Expense added!", category='success')
            elif typeofexpense == 'income':
                new_income = Income(
                    name=desc, category=category, amount=amount, user_id=current_user.id, date=datetime.utcnow())
                db.session.add(new_income)
                db.session.commit()
                flash("Income added!", category='success')

    return render_template("home.html", user=current_user)


@views.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    expenses = Expense.query.filter_by(
        user_id=current_user.id).order_by(Expense.date.desc()).all()
    incomes = Income.query.filter_by(
        user_id=current_user.id).filter(func.date(Income.date)).order_by(Income.date.desc()).all()
    total_expense = db.session.query(func.sum(Expense.amount)).filter_by(
        user_id=current_user.id).scalar()
    total_income = db.session.query(func.sum(Income.amount)).filter_by(
        user_id=current_user.id).scalar()
    expense_dates = db.session.query(func.date(Expense.date).label(
        'date')).filter_by(user_id=current_user.id).distinct().all()
    income_dates = db.session.query(func.date(Income.date).label(
        'date')).filter_by(user_id=current_user.id).distinct().all()
    expenses_by_date = db.session.query(
        func.date(Expense.date).label('date'),  # Extract date (without time)
    ).filter_by(user_id=current_user.id) \
        .group_by(func.date(Expense.date)) \
        .order_by(func.date(Expense.date).desc()) \
        .all()
    return render_template("profile.html", user=current_user, expenses=expenses, incomes=incomes, total_expense=total_expense, total_income=total_income, expense_dates=expense_dates, income_dates=income_dates)


@views.route("/delete-expense/<int:id>", methods=['POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)

    # Optional: Ensure only the owner can delete their expense
    if expense.user_id != current_user.id:
        flash("You don't have permission to delete this expense.", category='error')
        return redirect(url_for('views.profile'))

    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted!', category='success')
    return redirect(url_for('views.profile'))


@views.route("/delete-income/<int:id>", methods=['POST'])
@login_required
def delete_income(id):
    income = Income.query.get_or_404(id)

    # Optional: Ensure only the owner can delete their expense
    if income.user_id != current_user.id:
        flash("You don't have permission to delete this expense.", category='error')
        return redirect(url_for('views.profile'))

    db.session.delete(income)
    db.session.commit()
    flash('Income deleted!', category='success')
    return redirect(url_for('views.profile'))


@views.route("/update-expense/<int:id>", methods=['GET', 'POST'])
@login_required
def update_expense(id):
    expense = Expense.query.get_or_404(id)

    # Optional: Ensure only the owner can update their expense
    if expense.user_id != current_user.id:
        flash("You don't have permission to update this expense.", category='error')
        return redirect(url_for('views.profile'))

    if request.method == 'POST':
        expense.name = request.form.get('name')
        expense.category = request.form.get('category')
        expense.amount = request.form.get('amount')
        db.session.commit()
        flash('Expense updated!', category='success')
        return redirect(url_for('views.profile'))

    return render_template('update_expense.html', expense=expense)


@views.route("/update-income/<int:id>", methods=['GET', 'POST'])
@login_required
def update_income(id):
    income = Income.query.get_or_404(id)

    # Optional: Ensure only the owner can update their income
    if income.user_id != current_user.id:
        flash("You don't have permission to update this income.", category='error')
        return redirect(url_for('views.profile'))

    if request.method == 'POST':
        income.name = request.form.get('name')
        income.category = request.form.get('category')
        income.amount = request.form.get('amount')
        db.session.commit()
        flash('Income updated!', category='success')
        return redirect(url_for('views.profile'))

    return render_template('update_income.html', income=income)
