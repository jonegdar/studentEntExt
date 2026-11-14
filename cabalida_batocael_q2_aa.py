# PSHS-ZRC Student Entrance and Exit Recording System
# Q2 Alternative Assessment program
# This terminal prototype records student registrations and campus entry/exit events.
# It uses Linear Search, Insertion Sort, Selection Sort, and Merge Sort implemented
# directly in this file. It does not use Python's built-in sorting functions.
# Student identifiers: id_qr is a prototype QR payload; id_no is 16-YYYY-NNN.
# All records are held in memory and disappear when the program closes.

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
    print(f"Student number (id_no): {student.id_no}")
    print(f"Student ID / QR payload (id_qr): {student.id_qr}")


def print_student(student):
    print("." * 68)
    print(f"Student number (id_no): {student.id_no}")
    print(f"Student ID / QR payload (id_qr): {student.id_qr}")
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
    display_student_list(ordered, "Students by grade, section, and name (Insertion Sort)")


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
    print("Search by id_qr, id_no, name, batch/grade, section, or residence.")
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
    display_student_list(ordered, "Students by id_no (Selection Sort)")


def build_notification(student, event_type, timestamp):
    return (
        f"Hello po, Ma'am/Sir {student.guardian_name}!\n\n"
        "This is a school guard-house notification.\n"
        f"Student: {student.full_name}\n"
        f"Student number (id_no): {student.id_no}\n"
        f"Residence: {student.residence_type} ({student.intern_subtype})\n"
        f"Event: Student {event_type.lower()}\n"
        f"Date and time: {timestamp.strftime('%Y-%m-%d %I:%M:%S %p')}\n\n"
        "The campus record has been updated. Thank you po!"
    )


def record_entry_or_exit():
    display_section_header("Record Student Entry or Exit")
    value = get_non_empty_input("Scan/type the student's id_qr payload: ")
    student = campus_system.find_student_by_id(value)
    if student is None:
        print("No matching student. Check the QR payload or use id_no instead.")
        return
    while True:
        choice = input("Type E for Entry or X for Exit: ").strip().upper()
        if choice in {"E", "X"}:
            break
        print("Enter E for Entry or X for Exit.")
    event_type = "ENTRY" if choice == "E" else "EXIT"
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
    print(f"{record.student_name} | {record.id_no} | {record.event_type}")
    print(timestamp.strftime("%Y-%m-%d %I:%M:%S %p"))
    if get_yes_or_no("Display the simulated guardian message now? (Y/N): ") == "Y":
        display_parent_message(record)


def print_attendance_record(record):
    print("." * 68)
    print(f"Record ID: {record.record_id}")
    print(f"Student: {record.student_name} | id_no: {record.id_no}")
    print(f"id_qr: {record.id_qr}")
    print(f"Batch/grade: {record.grade_level} | Section: {record.section}")
    print(f"Residence: {record.residence_type} | Type: {record.intern_subtype}")
    print(f"Event: {record.event_type}")
    print(f"Date/time: {record.timestamp.strftime('%Y-%m-%d %I:%M:%S %p')}")


def display_attendance_list(records, title, algorithm_name):
    display_section_header(f"{title} ({algorithm_name})")
    if not records:
        print("No attendance events to display.")
        return
    for record in records:
        print_attendance_record(record)
    print("." * 68)
    print(f"Total events: {len(records)}")


def view_all_events_chronologically():
    ordered = merge_sort(attendance_records, timestamp_key)
    display_attendance_list(ordered, "All Attendance Events by Date and Time", "Merge Sort")


def view_todays_events():
    today = datetime.now().date()
    todays_records = [record for record in attendance_records
                      if record.timestamp.date() == today]
    ordered = insertion_sort(todays_records, timestamp_key)
    display_attendance_list(ordered, "Today's Attendance Events", "Insertion Sort")


def view_student_history():
    display_section_header("Student Attendance History")
    student = get_student_by_lookup("Enter id_no or id_qr: ")
    if student is None:
        return
    history = [record for record in attendance_records if record.id_qr == student.id_qr]
    ordered = merge_sort(history, timestamp_key)
    print(f"History for {student.full_name} ({student.id_no})")
    print("Residence type is descriptive only; no travel rules are enforced.")
    display_attendance_list(ordered, "Student Events in Date/Time Order", "Merge Sort")


def display_parent_message(record):
    display_section_header("Simulated Parent/Guardian Message")
    print(f"Recipient: Parent/guardian of {record.student_name}")
    print(f"Guardian contact: {record.guardian_contact}")
    print(f"Related record ID: {record.record_id}")
    print("." * 68)
    print(record.notification)
    print("." * 68)
    print("This prototype displays the message only. It does not send SMS or email.")


def view_parent_message():
    if not attendance_records:
        print("There are no recorded messages yet.")
        return
    for record in attendance_records:
        print(f"[{record.record_id}] {record.student_name} - {record.event_type} - "
              f"{record.timestamp.strftime('%Y-%m-%d %I:%M:%S %p')}")
    record_id = get_non_empty_input("Recording ID to view: ")
    if not record_id.isdigit():
        print("Enter a numeric recording ID.")
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


def view_current_presence_estimate():
    """Infer a session-only status from each student's latest recorded event."""
    latest_by_id_qr = {}
    for record in attendance_records:
        previous = latest_by_id_qr.get(record.id_qr)
        if previous is None or record.timestamp > previous.timestamp:
            latest_by_id_qr[record.id_qr] = record
    students_with_events = [
        student for student in student_records if student.id_qr in latest_by_id_qr
    ]
    ordered = insertion_sort(students_with_events, student_class_key)
    display_section_header("Estimated Current Campus Presence")
    print("Estimate from the latest event recorded in this running session only.")
    print("It is not a live or persistent attendance register.")
    if not ordered:
        print("No student has a recorded event in this session.")
        return
    for student in ordered:
        latest = latest_by_id_qr[student.id_qr]
        status = "PRESUMED ON CAMPUS" if latest.event_type == "ENTRY" else "PRESUMED OFF CAMPUS"
        print(f"{student.id_no} | {student.full_name} | {student.grade_level}-{student.section}")
        print(f"{status} based on latest {latest.event_type} at "
              f"{latest.timestamp.strftime('%Y-%m-%d %I:%M:%S %p')}")


def display_menu():
    print("\n" + "=" * 72)
    print("MAIN MENU")
    print("=" * 72)
    print("[1] Register student")
    print("[2] View students by grade, section, and name (Insertion Sort)")
    print("[3] Find student; search results ordered by class (Linear + Insertion)")
    print("[4] Update student details")
    print("[5] Remove student")
    print("[6] Record student entry/exit")
    print("[7] View all events by date/time (Merge Sort)")
    print("[8] View today's events by time (Insertion Sort)")
    print("[9] View a student's chronological event history (Merge Sort)")
    print("[10] View students by id_no (Selection Sort)")
    print("[11] Estimate current presence from latest recorded event")
    print("[12] View simulated guardian message")
    print("[13] Daily summary")
    print("[14] Exit")
    while True:
        choice = input("Menu choice (1-14): ").strip()
        if choice in {str(number) for number in range(1, 15)}:
            return choice
        print("Enter a number from 1 through 14.")


def update_student():
    display_section_header("Update Student")
    student = get_student_by_lookup("Student id_no or id_qr to update: ")
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
    student = get_student_by_lookup("Student id_no or id_qr to remove: ")
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
    actions = {
        "1": register_student,
        "2": view_students_by_class,
        "3": search_students,
        "4": update_student,
        "5": remove_student,
        "6": record_entry_or_exit,
        "7": view_all_events_chronologically,
        "8": view_todays_events,
        "9": view_student_history,
        "10": view_students_by_id_no,
        "11": view_current_presence_estimate,
        "12": view_parent_message,
        "13": display_daily_summary,
    }
    while True:
        choice = display_menu()
        if choice == "14":
            print("\nThank you for using the campus recording system.")
            break
        actions[choice]()


if __name__ == "__main__":
    run_program()
