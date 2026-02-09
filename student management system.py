import json
import os
from datetime import datetime

DATA_FILE = "students_data.json"


class Student:
    def __init__(self, roll_no, name, age, course, marks):
        self.roll_no = roll_no
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks

    def calculate_grade(self):
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        elif self.marks >= 40:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "marks": self.marks,
            "grade": self.calculate_grade()
        }


class StudentManager:
    def __init__(self):
        self.students = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                for s in data:
                    student = Student(
                        s["roll_no"],
                        s["name"],
                        s["age"],
                        s["course"],
                        s["marks"]
                    )
                    self.students.append(student)

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump([s.to_dict() for s in self.students], file, indent=4)

    def add_student(self):
        try:
            roll_no = input("Enter Roll Number: ")
            if self.find_student(roll_no):
                print("❌ Student with this roll number already exists.")
                return

            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            course = input("Enter Course: ")
            marks = float(input("Enter Marks: "))

            student = Student(roll_no, name, age, course, marks)
            self.students.append(student)
            self.save_data()
            print("✅ Student added successfully!")

        except ValueError:
            print("❌ Invalid input. Please try again.")

    def view_all_students(self):
        if not self.students:
            print("⚠️ No students found.")
            return

        print("\n------ STUDENT LIST ------")
        for s in self.students:
            print(
                f"Roll: {s.roll_no} | Name: {s.name} | "
                f"Course: {s.course} | Marks: {s.marks} | "
                f"Grade: {s.calculate_grade()}"
            )

    def find_student(self, roll_no):
        for s in self.students:
            if s.roll_no == roll_no:
                return s
        return None

    def search_student(self):
        roll_no = input("Enter Roll Number to search: ")
        student = self.find_student(roll_no)

        if student:
            print("\n🎯 Student Found:")
            print(json.dumps(student.to_dict(), indent=4))
        else:
            print("❌ Student not found.")

    def update_student(self):
        roll_no = input("Enter Roll Number to update: ")
        student = self.find_student(roll_no)

        if not student:
            print("❌ Student not found.")
            return

        try:
            student.name = input(f"New Name ({student.name}): ") or student.name
            student.age = int(input(f"New Age ({student.age}): ") or student.age)
            student.course = input(f"New Course ({student.course}): ") or student.course
            student.marks = float(input(f"New Marks ({student.marks}): ") or student.marks)

            self.save_data()
            print("✅ Student updated successfully!")

        except ValueError:
            print("❌ Invalid input.")

    def delete_student(self):
        roll_no = input("Enter Roll Number to delete: ")
        student = self.find_student(roll_no)

        if student:
            self.students.remove(student)
            self.save_data()
            print("🗑️ Student deleted successfully.")
        else:
            print("❌ Student not found.")

    def generate_report(self):
        if not self.students:
            print("⚠️ No data to generate report.")
            return

        avg_marks = sum(s.marks for s in self.students) / len(self.students)
        highest = max(self.students, key=lambda s: s.marks)
        lowest = min(self.students, key=lambda s: s.marks)

        print("\n📈 STUDENT REPORT")
        print(f"Total Students: {len(self.students)}")
        print(f"Average Marks: {avg_marks:.2f}")
        print(f"Topper: {highest.name} ({highest.marks})")
        print(f"Lowest: {lowest.name} ({lowest.marks})")

    def sort_students(self):
        print("1. Sort by Marks")
        print("2. Sort by Name")
        choice = input("Choose option: ")

        if choice == "1":
            self.students.sort(key=lambda s: s.marks, reverse=True)
            print("✅ Sorted by marks.")
        elif choice == "2":
            self.students.sort(key=lambda s: s.name.lower())
            print("✅ Sorted by name.")
        else:
            print("❌ Invalid choice.")

    def menu(self):
        while True:
            print("\n====== STUDENT MANAGEMENT SYSTEM ======")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Generate Report")
            print("7. Sort Students")
            print("8. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_all_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                self.generate_report()
            elif choice == "7":
                self.sort_students()
            elif choice == "8":
                print("👋 Exiting... Goodbye!")
                break
            else:
                print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    print("🕒 Started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    manager = StudentManager()
    manager.menu()
