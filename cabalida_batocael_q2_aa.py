# -------- DOCUMENTATION --------
# PSHS-ZRC Student Entrance and Exit Recording System
# Problem Fixed: Organizes student registration and campus entry/exit records.
# Goal: Help guards, teachers, and dorm managers record and review student presence.
# Target users: School guards and authorized school staff.
# Features: Register, view, search, update, and remove students; record entry and
# exit events; view simulated guardian messages and daily entry/exit summaries.
# Sorting and searching features:
# - View students by grade, section, and name using Insertion Sort.
# - Find students using Linear Search, then order matches by class with Insertion Sort.
# - View students by id_no using Selection Sort.
# - View all attendance events by timestamp using Merge Sort.
# - View one student's events chronologically using Merge Sort.
# - View today's events by time using Insertion Sort.
# - View each student's latest recorded campus status from this session.
# Student details include intern/extern residence type and intern subtype; these
# are descriptive and do not restrict or validate a student's movements.
# IDs: id_qr is the student's prototype QR payload; id_no is 16-YYYY-NNN.
# Capacity: Up to 540 students, 30 students per section, and 3 sections per grade.
# Python concepts: Classes, objects, lists, functions, loops, conditions, input
# validation, Linear Search, Insertion Sort, Selection Sort, and Merge Sort.

# -------- EXPLANATION --------
# The program is a terminal-based prototype for recording student registrations
# and each campus entry or exit as a separate timestamped attendance event.
# id_qr is the text payload representing the student's QR-based ID; id_no is a
# separate student number with the freshman-entry year and a three-digit sequence.
# The user types the QR payload in place of scanning a physical QR card. Residence
# information describes the student but does not impose a schedule, since interns
# and externs may make multiple trips or leave at different times.
# The sorting functions are implemented in this file rather than using Python's
# built-in sorting functions. The status view reflects only events entered during
# the current run. Data is temporary, and guardian notifications
# are displayed for the prototype but are not sent by SMS or email.

# Developers:
# John Edgar A. Cabalida, 11 - Polaris
# Shan Fernan Emiel F. Batocael, 11 - Sirius

from datetime import datetime


class Student:
    """Stores a student's identity, school details, residence, and contacts."""

    def __init__(self, id_qr, id_no, full_name, grade_level, section, birthday,
                 contact_number, residence_type, intern_subtype, guardian_name,
                 guardian_contact):
        self.id_qr = id_qr
        self.id_no = id_no
        self.full_name = full_name
        self.grade_level = grade_level
        self.section = section
        self.birthday = birthday
        self.contact_number = contact_number
        self.residence_type = residence_type
        self.intern_subtype = intern_subtype
        self.guardian_name = guardian_name
        self.guardian_contact = guardian_contact


class AttendanceRecord:
    """Stores one timestamped entry or exit event and its simulated message."""

    def __init__(self, record_id, id_qr, id_no, student_name, grade_level,
                 section, residence_type, intern_subtype, guardian_name,
                 guardian_contact, event_type, timestamp, notification):
        self.record_id = record_id
        self.id_qr = id_qr
        self.id_no = id_no
        self.student_name = student_name
        self.grade_level = grade_level
        self.section = section
        self.residence_type = residence_type
        self.intern_subtype = intern_subtype
        self.guardian_name = guardian_name
        self.guardian_contact = guardian_contact
        self.event_type = event_type
        self.timestamp = timestamp
        self.notification = notification


class CampusSystem:
    """Owns the in-memory student and attendance collections."""

    def __init__(self):
        self.student_records = []
        self.attendance_records = []
        self.next_sequence_by_year = {}

    def create_next_id_no(self, freshman_year):
        sequence = self.next_sequence_by_year.get(freshman_year, 1)
        if sequence > 999:
            raise ValueError("The 001-999 student-number sequence is full for that year.")
        self.next_sequence_by_year[freshman_year] = sequence + 1
        return f"16-{freshman_year}-{sequence:03d}"

    def find_student_by_id(self, value):
        """Linear search by either id_no or id_qr."""
        target = value.strip().casefold()
        for student in self.student_records:
            if student.id_no.casefold() == target or student.id_qr.casefold() == target:
                return student
        return None


campus_system = CampusSystem()
student_records = campus_system.student_records
attendance_records = campus_system.attendance_records


def display_program_header():
    print("=" * 72)
    print("PSHS-ZRC STUDENT ENTRANCE AND EXIT RECORDING SYSTEM")
    print("=" * 72)
    print("Register students and record campus entry and exit events.")
    print("Residence information is recorded for context, not used to restrict trips.")
    print("=" * 72)


def display_section_header(title):
    print("\n\n" + "-" * 72)
    print(f"{title.upper():^72}")
    print("-" * 72)


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value. This cannot be blank.")


def get_valid_contact(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and len(value) >= 7:
            return value
        print("Enter a contact number containing at least seven digits.")


def get_yes_or_no(prompt):
    while True:
        answer = input(prompt).strip().upper()
        if answer in {"Y", "N"}:
            return answer
        print("Enter Y for Yes or N for No.")


def get_freshman_year():
    while True:
        year = input("Year the student entered as a freshman (YYYY): ").strip()
        if len(year) == 4 and year.isdigit():
            return year
        print("Enter a four-digit year, such as 2026.")


def get_grade_level():
    while True:
        level = input("Batch/grade level (7-12): ").strip()
        if level in {"7", "8", "9", "10", "11", "12"}:
            return int(level)
        print("Enter a grade level from 7 through 12.")


def class_has_capacity(grade_level, section, exclude_student=None):
    """Enforce the stated 30-per-section and three-sections-per-grade limits."""
    active_students = [student for student in student_records
                       if student is not exclude_student]
    if exclude_student is None and len(active_students) >= 540:
        return False, "The campus capacity of 540 student records has been reached."
    normalized_section = section.strip().casefold()
    same_class = [student for student in active_students
                  if student.grade_level == grade_level
                  and student.section.casefold() == normalized_section]
    if len(same_class) >= 30:
        return False, "This section already has 30 registered students."
    sections_in_grade = {student.section.casefold() for student in active_students
                         if student.grade_level == grade_level}
    if normalized_section not in sections_in_grade and len(sections_in_grade) >= 3:
        return False, "This grade level already has three registered sections."
    return True, ""


def get_residence_details():
    while True:
        choice = input("Residence type: [1] Intern (dorm)  [2] Extern: ").strip()
        if choice == "1":
            while True:
                subtype = input(
                    "Intern type: [1] Weekender  [2] Goes home Friday, returns Sunday: "
                ).strip()
                if subtype == "1":
                    return "Intern", "Weekender"
                if subtype == "2":
                    return "Intern", "Friday-home intern"
                print("Choose 1 or 2.")
        if choice == "2":
            return "Extern", "Not applicable"
        print("Choose 1 for Intern or 2 for Extern.")


def create_id_qr(id_no):
    """Create the prototype text payload represented by the student's QR code."""
    return f"PSHS-ZRC:STUDENT:{id_no}"


def get_student_by_lookup(prompt):
    value = get_non_empty_input(prompt)
    student = campus_system.find_student_by_id(value)
    if student is None:
        print("Student not found. Check the ID number or QR payload.")
    return student


def register_student():
    display_section_header("Student Registration")
    if len(student_records) >= 540:
        print("The campus capacity of 540 student records has been reached.")
        return
    full_name = get_non_empty_input("Full name: ")
    grade_level = get_grade_level()
    section = get_non_empty_input("Section name: ")
    allowed, reason = class_has_capacity(grade_level, section)
    if not allowed:
        print(reason)
        return
    birthday = get_non_empty_input("Birthday (YYYY-MM-DD): ")
    contact_number = get_valid_contact("Student contact number: ")
    freshman_year = get_freshman_year()
    residence_type, intern_subtype = get_residence_details()
    guardian_name = get_non_empty_input("Parent/guardian full name: ")
    guardian_contact = get_valid_contact("Parent/guardian contact number: ")
    id_no = campus_system.create_next_id_no(freshman_year)
    id_qr = create_id_qr(id_no)

    student = Student(
        id_qr, id_no, full_name, grade_level, section, birthday,
        contact_number, residence_type, intern_subtype, guardian_name,
        guardian_contact
    )
    student_records.append(student)
    print("\nStudent registered successfully.")
    print(f"Student number: {student.id_no}")
    print(f"Student QR ID: {student.id_qr}")


def print_student(student):
    print("." * 68)
    print(f"Student number: {student.id_no}")
    print(f"Student QR ID: {student.id_qr}")
    print(f"Name: {student.full_name}")
    print(f"Batch/grade: {student.grade_level} | Section: {student.section}")
    print(f"Birthday: {student.birthday}")
    print(f"Student contact: {student.contact_number}")
    print(f"Residence: {student.residence_type} | Type: {student.intern_subtype}")
    print(f"Parent/guardian: {student.guardian_name}")
    print(f"Guardian contact: {student.guardian_contact}")


def insertion_sort(items, key_function):
    """Return a new list sorted with the class Insertion Sort algorithm."""
    result = list(items)
    for index in range(1, len(result)):
        current_item = result[index]
        current_key = key_function(current_item)
        position = index - 1
        while position >= 0 and key_function(result[position]) > current_key:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current_item
    return result


def selection_sort(items, key_function):
    """Return a new list sorted with the class Selection Sort algorithm."""
    result = list(items)
    for start in range(len(result) - 1):
        smallest = start
        for scan in range(start + 1, len(result)):
            if key_function(result[scan]) < key_function(result[smallest]):
                smallest = scan
        if smallest != start:
            result[start], result[smallest] = result[smallest], result[start]
    return result


def merge_sort(items, key_function):
    """Return a new list sorted with a stable recursive Merge Sort."""
    if len(items) <= 1:
        return list(items)
    middle = len(items) // 2
    left = merge_sort(items[:middle], key_function)
    right = merge_sort(items[middle:], key_function)
    merged = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if key_function(left[left_index]) <= key_function(right[right_index]):
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def student_class_key(student):
    return student.grade_level, student.section.casefold(), student.full_name.casefold()


def student_number_key(student):
    return student.id_no


def timestamp_key(record):
    return record.timestamp


def display_student_list(students, title):
    display_section_header(title)
    if not students:
        print("No students to display.")
        return
    for student in students:
        print_student(student)
    print("." * 68)
    print(f"Total students: {len(students)}")


def view_students_by_class():
    ordered = insertion_sort(student_records, student_class_key)
    display_student_list(ordered, "Student Directory: By Grade, Section, and Name")


def linear_search_students(keyword):
    """Find substring matches by scanning student records from first to last."""
    target = keyword.casefold()
    matches = []
    for student in student_records:
        searchable_text = " ".join((
            student.id_qr, student.id_no, student.full_name,
            str(student.grade_level), student.section, student.residence_type,
            student.intern_subtype, student.guardian_name
        )).casefold()
        if target in searchable_text:
            matches.append(student)
    return matches


def search_students():
    display_section_header("Student Record Finder")
    print("Search by student number, QR ID, name, grade, section, or residence.")
    keyword = get_non_empty_input("Search term: ")
    matches = linear_search_students(keyword)
    if not matches:
        print("No matching student was found.")
        return
    ordered_matches = insertion_sort(matches, student_class_key)
    print(f"Found {len(matches)} matching student(s). Results sorted by class.")
    for student in ordered_matches:
        print_student(student)


def view_students_by_id_no():
    ordered = selection_sort(student_records, student_number_key)
    display_student_list(ordered, "Student Directory: By Student Number")


def build_notification(student, event_type, timestamp):
    return (
        f"Hello po, Ma'am/Sir {student.guardian_name}!\n\n"
        "This is a school guard-house notification.\n"
        f"Student: {student.full_name}\n"
        f"Student number: {student.id_no}\n"
        f"Residence: {student.residence_type} ({student.intern_subtype})\n"
        f"Event: {describe_movement(event_type)}\n"
        f"Date and time: {timestamp.strftime('%Y-%m-%d %I:%M:%S %p')}\n\n"
        "The campus record has been updated. Thank you po!"
    )


def record_entry_or_exit():
    display_section_header("Record Student Entry or Exit")
    value = get_non_empty_input("Student number or QR ID: ")
    student = campus_system.find_student_by_id(value)
    if student is None:
        print("Student not found. Check the student number or QR ID.")
        return
    while True:
        choice = input(
            "Select movement: [1] Arriving on campus  [2] Leaving campus  [B] Cancel: "
        ).strip().upper()
        if choice in {"1", "2", "B"}:
            break
        print("Choose 1, 2, or B to cancel.")
    if choice == "B":
        print("No event was recorded.")
        return
    event_type = "ENTRY" if choice == "1" else "EXIT"
    timestamp = datetime.now()
    notification = build_notification(student, event_type, timestamp)
    record = AttendanceRecord(
        len(attendance_records) + 1, student.id_qr, student.id_no,
        student.full_name, student.grade_level, student.section,
        student.residence_type, student.intern_subtype, student.guardian_name,
        student.guardian_contact, event_type, timestamp, notification
    )
    attendance_records.append(record)
    print("\nEvent recorded.")
    print(f"{record.student_name} | {record.id_no} | {describe_movement(record.event_type)}")
    print(timestamp.strftime("%Y-%m-%d %I:%M:%S %p"))
    if get_yes_or_no("Display the simulated guardian message now? (Y/N): ") == "Y":
        display_parent_message(record)


def describe_movement(event_type):
    return "Arrived on campus" if event_type == "ENTRY" else "Left campus"


def print_attendance_record(record):
    print("." * 68)
    print(f"Record ID: {record.record_id}")
    print(f"Student: {record.student_name} | Student number: {record.id_no}")
    print(f"Student QR ID: {record.id_qr}")
    print(f"Batch/grade: {record.grade_level} | Section: {record.section}")
    print(f"Residence: {record.residence_type} | Type: {record.intern_subtype}")
    print(f"Movement: {describe_movement(record.event_type)}")
    print(f"Date/time: {record.timestamp.strftime('%Y-%m-%d %I:%M:%S %p')}")


def display_attendance_list(records, title):
    display_section_header(title)
    if not records:
        print("No attendance events to display.")
        return
    for record in records:
        print_attendance_record(record)
    print("." * 68)
    print(f"Total events: {len(records)}")


def view_all_events_chronologically():
    ordered = merge_sort(attendance_records, timestamp_key)
    display_attendance_list(ordered, "All Recorded Events, in Date and Time Order")


def view_todays_events():
    today = datetime.now().date()
    todays_records = [record for record in attendance_records
                      if record.timestamp.date() == today]
    ordered = insertion_sort(todays_records, timestamp_key)
    display_attendance_list(ordered, "Today's Entry and Exit Activity")


def view_student_history():
    display_section_header("Student Attendance History")
    student = get_student_by_lookup("Student number or QR ID: ")
    if student is None:
        return
    history = [record for record in attendance_records if record.id_qr == student.id_qr]
    ordered = merge_sort(history, timestamp_key)
    print(f"History for {student.full_name} ({student.id_no})")
    print("Residence type is descriptive only; no travel rules are enforced.")
    display_attendance_list(ordered, "Student Events, in Date and Time Order")


def display_parent_message(record):
    display_section_header("Simulated Parent/Guardian Message")
    print(f"Recipient: Parent/guardian of {record.student_name}")
    print(f"Guardian contact: {record.guardian_contact}")
    print(f"Event number: {record.record_id}")
    print("." * 68)
    print(record.notification)
    print("." * 68)
    print("This prototype displays the message only. It does not send SMS or email.")


def view_parent_message():
    if not attendance_records:
        print("There are no recorded messages yet.")
        return
    for record in attendance_records:
        print(f"[{record.record_id}] {record.student_name} - {describe_movement(record.event_type)} - "
              f"{record.timestamp.strftime('%Y-%m-%d %I:%M:%S %p')}")
    record_id = get_non_empty_input("Event number to open: ")
    if not record_id.isdigit():
        print("Enter one of the event numbers shown above.")
        return
    for record in attendance_records:
        if record.record_id == int(record_id):
            display_parent_message(record)
            return
    print("Recording not found.")


def display_daily_summary():
    today = datetime.now().date()
    entries = sum(1 for record in attendance_records
                  if record.timestamp.date() == today and record.event_type == "ENTRY")
    exits = sum(1 for record in attendance_records
                if record.timestamp.date() == today and record.event_type == "EXIT")
    display_section_header("Daily Summary")
    print(f"Date: {today}")
    print(f"Total events: {entries + exits}")
    print(f"Entries: {entries}")
    print(f"Exits: {exits}")


def view_latest_recorded_status():
    """Show what each student's latest recorded entry or exit indicates."""
    latest_by_id_qr = {}
    for record in attendance_records:
        previous = latest_by_id_qr.get(record.id_qr)
        if previous is None or record.timestamp > previous.timestamp:
            latest_by_id_qr[record.id_qr] = record

    ordered_students = insertion_sort(student_records, student_class_key)
    display_section_header("Latest Recorded Campus Status")
    print("Based on each student's latest event recorded since this program started.")
    print("Latest ENTRY means recorded as on campus. Latest EXIT means recorded as off campus.")
    print("No event this session means the status is unknown. This is not a live location check.")
    print("Event records are cleared when the program closes.")
    if not ordered_students:
        print("No students are registered.")
        return

    for student in ordered_students:
        latest = latest_by_id_qr.get(student.id_qr)
        print("." * 68)
        print(f"{student.id_no} | {student.full_name} | "
              f"Grade {student.grade_level}, {student.section}")
        if latest is None:
            print("Status: UNKNOWN. No entry or exit has been recorded this session.")
        else:
            status = "Recorded as on campus" if latest.event_type == "ENTRY" else "Recorded as off campus"
            print(f"Status: {status}")
            print(f"Latest event: {latest.event_type} at "
                  f"{latest.timestamp.strftime('%Y-%m-%d %I:%M:%S %p')}")


def get_menu_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("That choice is not on this menu. Please try again.")


def display_main_menu():
    print("\n" + "=" * 72)
    print("MAIN MENU")
    print("=" * 72)
    print("[1] Register a student")
    print("[2] Find a student")
    print("[3] Student records")
    print("[4] Record an entry or exit")
    print("[5] Attendance and reports")
    print("[6] Guardian messages")
    print("[7] Exit")
    return get_menu_choice("Choose an option (1-7): ", {str(i) for i in range(1, 8)})


def run_student_records_menu():
    actions = {"1": view_students_by_class, "2": view_students_by_id_no,
               "3": update_student, "4": remove_student}
    while True:
        display_section_header("Student Records")
        print("[1] Browse students by grade and section")
        print("[2] Browse students by student number")
        print("[3] Update a student record")
        print("[4] Remove a student record")
        print("[5] Back to main menu")
        choice = get_menu_choice("Choose an option (1-5): ", {"1", "2", "3", "4", "5"})
        if choice == "5":
            return
        actions[choice]()


def run_attendance_menu():
    actions = {"1": view_todays_events,
               "2": view_all_events_chronologically,
               "3": view_student_history,
               "4": display_daily_summary,
               "5": view_latest_recorded_status}
    while True:
        display_section_header("Attendance and Reports")
        print("[1] Today's entry and exit activity")
        print("[2] Browse all recorded events")
        print("[3] View one student's event history")
        print("[4] Today's entry/exit summary")
        print("[5] View latest recorded campus status")
        print("[6] Back to main menu")
        choice = get_menu_choice("Choose an option (1-6): ", {str(i) for i in range(1, 7)})
        if choice == "6":
            return
        actions[choice]()


def run_guardian_messages_menu():
    while True:
        display_section_header("Guardian Messages")
        print("[1] View a message for a recorded event")
        print("[2] Back to main menu")
        choice = get_menu_choice("Choose an option (1-2): ", {"1", "2"})
        if choice == "2":
            return
        view_parent_message()


def update_student():
    display_section_header("Update Student")
    student = get_student_by_lookup("Student number or QR ID to update: ")
    if student is None:
        return
    print("Press Enter to keep each current value.")
    print_student(student)
    name = input(f"New name [{student.full_name}]: ").strip()
    grade = input(f"New batch/grade 7-12 [{student.grade_level}]: ").strip()
    section = input(f"New section [{student.section}]: ").strip()
    birthday = input(f"New birthday [{student.birthday}]: ").strip()
    contact = input(f"New student contact [{student.contact_number}]: ").strip()
    guardian = input(f"New guardian name [{student.guardian_name}]: ").strip()
    guardian_contact = input(
        f"New guardian contact [{student.guardian_contact}]: "
    ).strip()
    if name:
        student.full_name = name
    proposed_grade = student.grade_level
    proposed_section = student.section
    valid_grade = not grade or grade in {"7", "8", "9", "10", "11", "12"}
    if grade and valid_grade:
        proposed_grade = int(grade)
    elif grade:
        print("Enter a grade from 7 through 12; previous value kept.")
    if section:
        proposed_section = section
    if (grade or section) and valid_grade:
        allowed, reason = class_has_capacity(
            proposed_grade, proposed_section, exclude_student=student
        )
        if allowed:
            student.grade_level = proposed_grade
            student.section = proposed_section
        else:
            print(f"Class change not applied: {reason}")
    if birthday:
        student.birthday = birthday
    if contact:
        if contact.isdigit() and len(contact) >= 7:
            student.contact_number = contact
        else:
            print("Invalid contact; previous value kept.")
    if guardian:
        student.guardian_name = guardian
    if guardian_contact:
        if guardian_contact.isdigit() and len(guardian_contact) >= 7:
            student.guardian_contact = guardian_contact
        else:
            print("Invalid guardian contact; previous value kept.")
    residence_choice = input("Change residence type? [Y/N]: ").strip().upper()
    if residence_choice == "Y":
        student.residence_type, student.intern_subtype = get_residence_details()
    print("Student record updated.")


def remove_student():
    display_section_header("Remove Student")
    student = get_student_by_lookup("Student number or QR ID to remove: ")
    if student is None:
        return
    print_student(student)
    if get_yes_or_no("Remove this student? (Y/N): ") == "Y":
        student_records.remove(student)
        print("Student removed. Existing attendance events remain in this session.")
    else:
        print("Removal cancelled.")


def run_program():
    display_program_header()
    actions = {"1": register_student, "2": search_students,
               "3": run_student_records_menu, "4": record_entry_or_exit,
               "5": run_attendance_menu, "6": run_guardian_messages_menu}
    while True:
        choice = display_main_menu()
        if choice == "7":
            print("\nThank you for using the campus recording system.")
            break
        actions[choice]()


if __name__ == "__main__":
    run_program()
