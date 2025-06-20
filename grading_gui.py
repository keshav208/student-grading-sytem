import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class Student:
    subjects = ["Physics", "Chemistry", "Maths", "Biology", "English"]

    def __init__(self, name, roll, marks):
        self.name = name
        self.roll = roll
        self.marks = marks
        self.percentage = sum(marks) / len(marks)
        self.grade = self.get_grade()
        self.status = "PASS" if all(m >= 33 for m in marks) else "FAIL"
        self.rank = None
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_grade(self):
        if self.percentage >= 90: return "A+"
        elif self.percentage >= 80: return "A"
        elif self.percentage >= 70: return "B"
        elif self.percentage >= 60: return "C"
        elif self.percentage >= 50: return "D"
        else: return "F"

students = []

root = tk.Tk()
root.title("Student Grading System")
root.geometry("900x700")
root.config(bg="#edf2fb")

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 11, 'bold'), background="#0d3b66", foreground="white")
style.configure("Treeview", font=('Arial', 10), rowheight=30)

# Title
tk.Label(root, text="Student Grading System", font=("Helvetica", 22, "bold"), bg="#1f4068", fg="white", pady=12).pack(fill="x")

# Form
form = tk.LabelFrame(root, text="Enter Student Details", font=("Arial", 12, "bold"), bg="#edf2fb", fg="#1f4068", padx=10, pady=10, relief="groove")
form.pack(pady=10, padx=20, fill="x")

tk.Label(form, text="Student Name:", bg="#edf2fb").grid(row=0, column=0, sticky="e")
tk.Label(form, text="Roll Number:", bg="#edf2fb").grid(row=1, column=0, sticky="e")

name_entry = tk.Entry(form, width=30)
roll_entry = tk.Entry(form, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)
roll_entry.grid(row=1, column=1, padx=10, pady=5)

entries = {}
for i, sub in enumerate(Student.subjects):
    tk.Label(form, text=f"{sub} Marks:", bg="#edf2fb").grid(row=i, column=2, sticky="e")
    entry = tk.Entry(form, width=10)
    entry.grid(row=i, column=3, padx=5, pady=5)
    entries[sub] = entry

# Buttons
button_frame = tk.LabelFrame(root, text="Actions", font=("Arial", 12, "bold"), bg="#edf2fb", fg="#1f4068", padx=10, pady=10, relief="groove")
button_frame.pack(pady=10, padx=20, fill="x")

def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    for sub in Student.subjects:
        entries[sub].delete(0, tk.END)

def add_student():
    try:
        name = name_entry.get().strip()
        roll = roll_entry.get().strip()
        marks = [float(entries[sub].get()) for sub in Student.subjects]
        if not name or not roll:
            raise ValueError("Name or Roll Number is empty")

        student = Student(name, roll, marks)
        students.append(student)
        messagebox.showinfo("Success", f"{name} added successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def generate_reports():
    if not students:
        messagebox.showwarning("Warning", "No students added yet.")
        return
    students.sort(key=lambda s: s.percentage, reverse=True)
    for i, s in enumerate(students):
        s.rank = i + 1

    update_table()

def update_table():
    for row in report_table.get_children():
        report_table.delete(row)
    for s in students:
        report_table.insert('', 'end', values=(
            s.rank, s.name, s.roll, *s.marks, f"{s.percentage:.2f}%", s.grade, s.status, s.timestamp
        ))

tk.Button(button_frame, text="Add Student", command=add_student,
 bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Generate Report", command=generate_reports,
 bg="#007bff", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Clear Fields", command=clear_fields,
 bg="#ffc107", fg="black", font=("Arial", 10, "bold"), width=15).grid(row=0, column=2, padx=10)

# Table

report_frame = tk.LabelFrame(root, text="Final Report Card", font=("Arial", 12, "bold"), bg="#edf2fb", fg="#1f4068", padx=10, pady=10, relief="groove")
report_frame.pack(pady=10, padx=20, fill="both", expand=True)

columns = ("Rank", "Name", "Roll", "Physics", "Chemistry", "Maths", "Biology", "English", "Percentage", "Grade", "Status", "Timestamp")
report_table = ttk.Treeview(report_frame, columns=columns, show="headings")
for col in columns:
    report_table.heading(col, text=col)
    report_table.column(col, width=80, anchor="center")
report_table.pack(fill="both", expand=True)

root.mainloop()
