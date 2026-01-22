import sqlite3
from datetime import date

conn = sqlite3.connect("timesheet.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS timesheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    work_date TEXT,
    hours REAL,
    FOREIGN KEY(employee_id) REFERENCES employees(id)
)
""")

def add_employee(name):
    cursor.execute("INSERT INTO employees (name) VALUES (?)", (name,))
    conn.commit()

def log_hours(emp_id, hours):
    cursor.execute(
        "INSERT INTO timesheets (employee_id, work_date, hours) VALUES (?, ?, ?)",
        (emp_id, date.today().isoformat(), hours)
    )
    conn.commit()

def view_timesheets():
    for row in cursor.execute("""
        SELECT e.name, t.work_date, t.hours
        FROM timesheets t JOIN employees e ON t.employee_id = e.id
    """):
        print(row)

print("Fredrick Gaming Tech – Timesheet System")
print("1. Add Employee")
print("2. Log Hours")
print("3. View Timesheets")

choice = input("Choose option: ")

if choice == "1":
    name = input("Employee name: ")
    add_employee(name)
    print("Employee added.")
elif choice == "2":
    emp_id = int(input("Employee ID: "))
    hours = float(input("Hours worked: "))
    log_hours(emp_id, hours)
    print("Hours logged.")
elif choice == "3":
    view_timesheets()

conn.close()