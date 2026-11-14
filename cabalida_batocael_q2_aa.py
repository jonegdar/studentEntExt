# -------- DOCUMENTATION --------

# PSHS-ZRC Student Entrance and Exit Recording System
# Problem Fixed: Organizes student registration and campus entry/exit records.
# Target users: School guards and authorized school staff.
# Features: Register, view, search, update, remove, record entry/exit, view parent messages, and display a daily summary.
# IDs: A generated QR payload is the student ID; student number is separate (16-YYYY-NNN).
# Python concepts: Classes, objects, lists, functions, loops, conditions, string methods, input validation, and formatted output.
 
# -------- EXPLANATION --------
# This system helps school guards and authorized staff register students and
# record campus entry and exit. 

# class Student stores a student's details, while
# class AttendanceRecord stores each event and its simulated guardian message.
# class CampusSystem owns the student and attendance lists and performs student lookups. 

# The original menu and functions still control registration, viewing,
# searching, updating, removal, event recording, message viewing, and the daily summary. 
# During a scan, a QR code identifies a registered student; the user
# chooses entry or exit, and the program timestamps the event. The event object
# is added to the attendance list. The system displays a friendly message, but
# does not send a real text or email. Input checks help reject blank values,
# invalid freshman-entry years, and invalid menu choices. All data is
# temporary and is lost when the program closes.
# Each student has a generated QR payload as their student ID and a separate
# student number: 16-YYYY-NNN, where YYYY is their freshman-entry year.

# ADDITIONAL: This program serves as a "prototype" for a planned future project for this sytem, with implementation IRL.

# Developers: 
# John Edgar A. Cabalida, 11 - Polaris
# Shan Fernan Emiel F. Batocael, 11 - Sirius

from datetime import datetime

# Object models and manager used by the menu functions.
class Student:
    def __init__(self, student_id, student_number, full_name, grade_section, birthday,
                 contact_number, guardian_name, guardian_contact):
        # student_id is the string payload represented by the student QR code.
        self.student_id = student_id
        self.student_number = student_number
        self.full_name = full_name
        self.grade_section = grade_section
        self.birthday = birthday
        self.contact_number = contact_number
        self.guardian_name = guardian_name
        self.guardian_contact = guardian_contact

    def __getitem__(self, field):
        return getattr(self, field)

    def __setitem__(self, field, value):
        if not hasattr(self, field):
            raise KeyError(field)
        setattr(self, field, value)


class AttendanceRecord:
    def __init__(self, record_id, student_id, student_number, student_name, grade_section,
                 guardian_name, guardian_contact, event_type, event_date,
                 event_time, notification):
        self.record_id = record_id
        self.student_id = student_id
        self.student_number = student_number
        self.student_name = student_name
        self.grade_section = grade_section
        self.guardian_name = guardian_name
        self.guardian_contact = guardian_contact
        self.event_type = event_type
        self.event_date = event_date
        self.event_time = event_time
        self.notification = notification

    def __getitem__(self, field):
        return getattr(self, field)


class CampusSystem:
    def __init__(self):
        self.student_records = []
        self.attendance_records = []

    def create_next_student_number(self, freshman_year):
        highest_sequence = 0
        for student in self.student_records:
            parts = student.student_number.split("-")
            if len(parts) == 3 and parts[1] == freshman_year:
                highest_sequence = max(highest_sequence, int(parts[2]))
        if highest_sequence >= 999:
            raise ValueError("The student-number sequence for this year is full.")
        return f"16-{freshman_year}-{highest_sequence + 1:03d}"

    def find_student_by_id(self, student_id):
        for student in self.student_records:
            if student.student_id.lower() == student_id.lower():
                return student
        return None

    def find_student_by_qr_code(self, qr_code):
        # The QR code payload is the student's ID itself.
        return self.find_student_by_id(qr_code)


# Keep the original collection names so the existing functions remain intact.
campus_system = CampusSystem()
student_records = campus_system.student_records
attendance_records = campus_system.attendance_records

# Displays the program introduction.
def display_program_header():
    print("=" * 58)
    print("PSHS-ZRC STUDENT ENTRANCE AND EXIT RECORDING SYSTEM")
    print("=" * 58)
    print("Registers students and records campus entry and exit events.")
    print("Intended users: School guards and authorized school staff")
    print("=" * 58)

# Gets text and rejects blank input.
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Please enter a value. This cannot be blank.")

# Gets a contact number containing at least seven digits.
def get_valid_contact(prompt):
    while True:
        contact_number = input(prompt).strip()
        if contact_number.isdigit() and len(contact_number) >= 7:
            return contact_number
        print("Please type a contact number with at least 7 digits.")

# Gets Y or N for a yes-or-no question.
def get_yes_or_no(prompt):
    while True:
        answer = input(prompt).strip().upper()
        if answer in {"Y", "N"}:
            return answer
        print("Please type Y for Yes or N for No.")

# Checks that the freshman-entry year has exactly four digits.
def is_valid_freshman_year(year):
    return len(year) == 4 and year.isdigit()

# Gets the freshman-entry year used in the separate student number.
def get_freshman_year():
    while True:
        year = input("Year the student entered as a freshman (YYYY): ").strip()
        if is_valid_freshman_year(year):
            return year
        print("Enter a four-digit year, such as 2026.")

# Creates a prototype QR payload; this string is the student's ID.
def create_qr_code_value(student_number):
    return f"PSHS-ZRC-STUDENT-{student_number}"

# Shows a clear heading for the selected screen.
def display_section_header(title):
    print("\n\n" + "-" * 58)
    print(f"                 {title.upper()}")
    print("-" * 58)

# Creates the next student number for the freshman-entry year.
def create_next_student_number(freshman_year):
    return campus_system.create_next_student_number(freshman_year)

# Finds one student by student ID.
def find_student_by_id(student_id):
    return campus_system.find_student_by_id(student_id)

# Finds one student by QR code.
def find_student_by_qr_code(qr_code):
    return campus_system.find_student_by_qr_code(qr_code)

# Adds a new student to the student list.
def register_student():
    display_section_header("Student Registration")
    print("Enter the student details below.")

    full_name = get_non_empty_input("Full name: ")
    grade_section = get_non_empty_input("Grade and section: ")
    birthday = get_non_empty_input("Birthday (YYYY-MM-DD): ")
    contact_number = get_valid_contact("Student contact number: ")
    freshman_year = get_freshman_year()
    student_number = create_next_student_number(freshman_year)
    qr_code = create_qr_code_value(student_number)
    guardian_name = get_non_empty_input("Parent/guardian full name: ")
    guardian_contact = get_valid_contact("Parent/guardian contact number: ")

    new_student = Student(
        student_id=qr_code,
        student_number=student_number,
        full_name=full_name,
        grade_section=grade_section,
        birthday=birthday,
        contact_number=contact_number,
        guardian_name=guardian_name,
        guardian_contact=guardian_contact,
    )

    student_records.append(new_student)

    print("\nStudent registered successfully.")
    print(f"Student ID / QR payload: {new_student['student_id']}")
    print(f"Student number: {new_student['student_number']}")

# Displays one student record.
def display_student(student):
    print("." * 44)
    print(f"Student ID / QR payload: {student['student_id']}")
    print(f"Student number: {student['student_number']}")
    print(f"Full name: {student['full_name']}")
    print(f"Grade/section: {student['grade_section']}")
    print(f"Birthday: {student['birthday']}")
    print(f"Student contact: {student['contact_number']}")
    print(f"Parent/guardian: {student['guardian_name']}")
    print(f"Guardian contact: {student['guardian_contact']}")

# Displays all registered students.
def display_all_students():
    display_section_header("View All Students")

    if not student_records:
        print("There are no registered students yet.")
        return

    for student in student_records:
        display_student(student)
    print("." * 44)
    print(f"Total students: {len(student_records)}")

# Searches students using a keyword.
def search_student():
    display_section_header("Search Student")
    print("Search by student ID/QR payload, student number, name, or grade/section.")
    keyword = get_non_empty_input("Search keyword: ").lower()
    matches = []

    for student in student_records:
        searchable_text = (
            student["student_id"] + " "
            + student["student_number"] + " "
            + student["full_name"] + " "
            + student["grade_section"]
        ).lower()

        if keyword in searchable_text:
            matches.append(student)

    if not matches:
        print("No matching student was found.")
        return

    print(f"Found {len(matches)} matching student(s).")
    for student in matches:
        display_student(student)

# Updates selected fields in a student record.
def update_student():
    display_section_header("Update Student")
    student_id = get_non_empty_input("Student ID / QR payload to update: ")
    student = find_student_by_id(student_id)

    if student is None:
        print("Student not found. Check the ID and try again.")
        return

    print("Press Enter to keep the current value.")
    display_student(student)

    new_name = input(f"New full name [{student['full_name']}]: ").strip()
    new_grade_section = input(
        f"New grade and section [{student['grade_section']}]: "
    ).strip()
    new_birthday = input(f"New birthday [{student['birthday']}]: ").strip()
    new_contact = input(
        f"New student contact [{student['contact_number']}]: "
    ).strip()
    new_guardian_name = input(
        f"New parent/guardian name [{student['guardian_name']}]: "
    ).strip()
    new_guardian_contact = input(
        f"New guardian contact [{student['guardian_contact']}]: "
    ).strip()

    if new_name:
        student["full_name"] = new_name
    if new_grade_section:
        student["grade_section"] = new_grade_section
    if new_birthday:
        student["birthday"] = new_birthday
    if new_contact:
        if new_contact.isdigit() and len(new_contact) >= 7:
            student["contact_number"] = new_contact
        else:
            print("Invalid student contact. The old value was kept.")
    if new_guardian_name:
        student["guardian_name"] = new_guardian_name
    if new_guardian_contact:
        if new_guardian_contact.isdigit() and len(new_guardian_contact) >= 7:
            student["guardian_contact"] = new_guardian_contact
        else:
            print("Invalid guardian contact. The old value was kept.")

    print("Student record updated successfully.")

# Removes a student after confirmation.
def remove_student():
    display_section_header("Remove Student")
    student_id = get_non_empty_input("Student ID / QR payload to remove: ")
    student = find_student_by_id(student_id)

    if student is None:
        print("Student not found. Check the ID and try again.")
        return

    display_student(student)
    confirmation = get_yes_or_no("Remove this record? Type Y for Yes, N for No: ")

    if confirmation == "Y":
        student_records.remove(student)
        print("Student removed successfully.")
    else:
        print("Removal cancelled. The record was kept.")

# Builds a friendly parent or guardian message.
def build_notification(student, event_type, event_date, event_time):
    return (
        f"Hello po, Ma'am/Sir {student['guardian_name']}!\n\n"
        f"This is a school guard-house notification.\n"
        f"Student name: {student['full_name']}\n"
        f"Student number: {student['student_number']}\n"
        f"Grade/section: {student['grade_section']}\n"
        f"Event: Student {event_type.lower()}\n"
        f"Date: {event_date}\n"
        f"Time: {event_time}\n\n"
        f"Your child's campus record has been updated. Thank you po!"
    )

# Displays the detailed parent or guardian message.
def display_parent_message(record):
    display_section_header("Message Sent to Parent/Guardian")
    print(f"Recipient: Parent/guardian of {record['student_name']}")
    print(f"Guardian contact: {record['guardian_contact']}")
    print(f"Related record ID: {record['record_id']}")
    print("." * 58)
    print(record["notification"])
    print("." * 58)
    print("Prototype notice: This message is displayed only.")
    print("It is not sent through SMS, email, or another service yet.")

# Records a student entry or exit and prepares a message.
def record_entry_or_exit():
    display_section_header("Record Student Entry or Exit")
    print("Type the registered QR code, then choose Entry or Exit.")
    qr_code = get_non_empty_input("Student ID / QR payload: ").upper()
    student = find_student_by_qr_code(qr_code)

    if student is None:
        print("QR code not found. Check the code or register the student first.")
        return

    while True:
        event_choice = input("Type E for Entry or X for Exit: ").strip().upper()
        if event_choice in {"E", "X"}:
            break
        print("Please type E for Entry or X for Exit.")

    event_type = "ENTRY" if event_choice == "E" else "EXIT"
    current_time = datetime.now()
    event_date = current_time.strftime("%Y-%m-%d")
    event_time = current_time.strftime("%I:%M %p")
    notification = build_notification(
        student, event_type, event_date, event_time
    )

    new_record = AttendanceRecord(
        record_id=len(attendance_records) + 1,
        student_id=student["student_id"],
        student_number=student["student_number"],
        student_name=student["full_name"],
        grade_section=student["grade_section"],
        guardian_name=student["guardian_name"],
        guardian_contact=student["guardian_contact"],
        event_type=event_type,
        event_date=event_date,
        event_time=event_time,
        notification=notification,
    )

    attendance_records.append(new_record)

    print("\nRecord saved successfully.")
    print(f"Student: {new_record['student_name']}")
    print(f"Student number: {new_record['student_number']}")
    print(f"Grade/section: {new_record['grade_section']}")
    print(f"Event: {new_record['event_type']}")
    print(f"Date and time: {event_date} {event_time}")

    view_now = get_yes_or_no(
        "View the message sent to the parent now? Type Y for Yes, N for No: "
    )
    if view_now == "Y":
        display_parent_message(new_record)

# Displays one entrance or exit record.
def display_attendance_record(record):
    print("." * 44)
    print(f"Record ID: {record['record_id']}")
    print(f"Student: {record['student_name']}")
    print(f"Student number: {record['student_number']}")
    print(f"Grade/section: {record['grade_section']}")
    print(f"Event: {record['event_type']}")
    print(f"Date and time: {record['event_date']} {record['event_time']}")

# Displays today's attendance records.
def display_todays_records():
    display_section_header("View Today's Records")
    today = datetime.now().strftime("%Y-%m-%d")
    todays_records = []

    for record in attendance_records:
        if record["event_date"] == today:
            todays_records.append(record)

    if not todays_records:
        print("There are no records for today yet.")
        return

    for record in todays_records:
        display_attendance_record(record)
    print("." * 44)
    print(f"Total records today: {len(todays_records)}")

# Finds and displays a selected parent or guardian message.
def view_parent_message():
    display_section_header("View Message Sent to Parent/Guardian")

    if not attendance_records:
        print("There are no recorded messages yet.")
        return

    print("Available recording IDs:")
    for record in attendance_records:
        print(
            f"[{record['record_id']}] {record['student_name']} - "
            f"{record['event_type']} - {record['event_date']} {record['event_time']}"
        )

    record_id = get_non_empty_input("Recording ID to view: ")

    if not record_id.isdigit():
        print("Please type a recording ID number, such as 1.")
        return

    selected_record = None
    for record in attendance_records:
        if record["record_id"] == int(record_id):
            selected_record = record
            break

    if selected_record is None:
        print("Recording not found. Check the ID and try again.")
        return

    display_parent_message(selected_record)

# Counts today's entries and exits.
def display_daily_summary():
    display_section_header("Daily Summary")
    today = datetime.now().strftime("%Y-%m-%d")
    entry_count = 0
    exit_count = 0

    for record in attendance_records:
        if record["event_date"] == today:
            if record["event_type"] == "ENTRY":
                entry_count += 1
            elif record["event_type"] == "EXIT":
                exit_count += 1

    print(f"Date: {today}")
    print(f"Total records: {entry_count + exit_count}")
    print(f"Total entries: {entry_count}")
    print(f"Total exits: {exit_count}")

# Displays and validates the main menu.
def display_menu():
    print("\n\n" + "=" * 58)
    print("                 MAIN MENU")
    print("=" * 58)
    print("Choose one number. Type 10 to exit the program.")
    print("[1] Register Student")
    print("[2] View All Students")
    print("[3] Search Student")
    print("[4] Update Student")
    print("[5] Remove Student")
    print("[6] Record Student Entry or Exit")
    print("[7] View Today's Records")
    print("[8] View Message Sent to Parent/Guardian")
    print("[9] Daily Summary")
    print("[10] Exit")
    print("=" * 58)

    while True:
        menu_choice = input("Menu choice (1-10): ").strip()
        if menu_choice in {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}:
            return menu_choice
        print("Invalid choice. Please type a number from 1 to 10.")

# Runs the menu until the user exits.
def run_program():
    display_program_header()

    while True:
        menu_choice = display_menu()

        if menu_choice == "1":
            register_student()
        elif menu_choice == "2":
            display_all_students()
        elif menu_choice == "3":
            search_student()
        elif menu_choice == "4":
            update_student()
        elif menu_choice == "5":
            remove_student()
        elif menu_choice == "6":
            record_entry_or_exit()
        elif menu_choice == "7":
            display_todays_records()
        elif menu_choice == "8":
            view_parent_message()
        elif menu_choice == "9":
            display_daily_summary()
        elif menu_choice == "10":
            print("\nThank you for using the PSHS-ZRC Student Entrance and Exit Recording System.")
            break

# Starts the program.
if __name__ == "__main__":
    run_program()
