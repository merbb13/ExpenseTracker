function showTable(tableId) {
    var expensesTable = document.getElementById('expenses-table');
    var incomesTable = document.getElementById('incomes-table');

    if (tableId === 'expenses') {
        expensesTable.style.display = 'table';
        incomesTable.style.display = 'none';
    } else if (tableId === 'incomes') {
        incomesTable.style.display = 'table';
        expensesTable.style.display = 'none';
    }
}