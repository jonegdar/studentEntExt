# -------- DOCUMENTATION --------
# PSHS-ZRC Student Entrance and Exit Recording System
# Problem Fixed: Organizes student registration and campus entry/exit records.
# Goal: Help guards, teachers, and dorm managers record and review student presence.
# Target users: School guards and authorized school staff.
# Features: Register, find, update, and remove students; record entry/exit events;
# browse filtered student histories; view daily and overall event histories; and
# view simulated guardian messages. Search results and histories are paginated.
# Sorting and searching features:
# - Find students by grade/section and name using Linear Search + Insertion Sort.
# - Find full or partial student numbers using Linear Search + Selection Sort.
# - View overall attendance chronologically using Merge Sort.
# - View one student's date-filtered events chronologically using Merge Sort.
# - View today's events by time using Insertion Sort.
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
# built-in sorting functions. Event history includes only records from the current
# run. Data is temporary, and guardian notifications are displayed for the
# prototype but are not sent by SMS or email.

# Developers:
# John Edgar A. Cabalida, 11 - Polaris
# Shan Fernan Emiel F. Batocael, 11 - Sirius

from datetime import datetime, timedelta


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

CLASS_OPTIONS = (
    (7, "Diamond"), (7, "Emerald"), (7, "Ruby"),
    (8, "Jasmin"), (8, "Sampaguita"), (8, "Waling-waling"),
    (9, "Lithium"), (9, "Potassium"), (9, "Sodium"),
    (10, "Gluon"), (10, "Graviton"), (10, "Muon"),
    (11, "Polaris"), (11, "Rigel"), (11, "Sirius"),
    (12, "Byte"), (12, "Quantum"), (12, "Qubit"),
)


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


def get_class_assignment(current=None):
    """Choose one of the school's fixed grade-and-section combinations."""
    print("Choose the student's grade and section:")
    for number, (grade_level, section) in enumerate(CLASS_OPTIONS, start=1):
        print(f"[{number}] G{grade_level} - {section}")
    if current is not None:
        print(f"[Enter] Keep current class (G{current[0]} - {current[1]})")

    while True:
        choice = input("Class option (1-18): ").strip()
        if not choice and current is not None:
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(CLASS_OPTIONS):
            return CLASS_OPTIONS[int(choice) - 1]
        print("Choose a listed class option" +
              (" or press Enter to keep the current class." if current is not None else "."))


def class_has_capacity(grade_level, section, exclude_student=None):
    """Enforce the stated 30-per-section and three-sections-per-grade limits."""
    if not any(grade_level == option_grade and
               section.strip().casefold() == option_section.casefold()
               for option_grade, option_section in CLASS_OPTIONS):
        return False, "Choose one of the school's preset grade-and-section options."
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
    grade_level, section = get_class_assignment()
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
    """Browse recorded events and open the simulated guardian message for one."""
    if not attendance_records:
        display_section_header("Simulated Guardian Messages")
        print("There are no recorded guardian messages yet.")
        return

    newest_first = list(reversed(merge_sort(attendance_records, timestamp_key)))
    page = 0
    total_pages = (len(newest_first) + PAGE_SIZE - 1) // PAGE_SIZE
    while True:
        start = page * PAGE_SIZE
        page_records = newest_first[start:start + PAGE_SIZE]
        display_section_header(f"Simulated Guardian Messages | Page {page + 1} of {total_pages}")
        for position, record in enumerate(page_records, start=1):
            print(f"[{position}] {record.student_name} | {record.id_no} | "
                  f"{describe_movement(record.event_type)} | "
                  f"{record.timestamp.strftime('%Y-%m-%d %I:%M:%S %p')}")
        choices = {str(i) for i in range(1, len(page_records) + 1)} | {"B"}
        if page > 0:
            choices.add("P")
        if page + 1 < total_pages:
            choices.add("N")
        navigation_labels = []
        if page > 0:
            navigation_labels.append("[P] Previous page")
        if page + 1 < total_pages:
            navigation_labels.append("[N] Next page")
        navigation_labels.append("[B] Back to main menu")
        print("  ".join(navigation_labels))
        choice = get_menu_choice("Choose an event or navigation option: ", choices)
        if choice == "B":
            return
        if choice == "P":
            page -= 1
            continue
        if choice == "N":
            page += 1
            continue

        record = page_records[int(choice) - 1]
        display_parent_message(record)
        after_message = get_menu_choice(
            "[B] Back to guardian messages  [M] Main menu: ", {"B", "M"}
        )
        if after_message == "M":
            return RETURN_TO_MAIN


def display_daily_summary():
    """Print today's entry/exit counts and return today's events in time order."""
    today = datetime.now().date()
    todays_records = [record for record in attendance_records
                      if record.timestamp.date() == today]
    entries = sum(1 for record in todays_records if record.event_type == "ENTRY")
    exits = sum(1 for record in todays_records if record.event_type == "EXIT")
    display_section_header("Today's Daily Summary")
    print(f"Date: {today.isoformat()}")
    print(f"Total events: {entries + exits}")
    print(f"Entries: {entries}")
    print(f"Exits: {exits}")
    return insertion_sort(todays_records, timestamp_key)


def display_main_menu():
    print("\n" + "=" * 72)
    print("MAIN MENU")
    print("=" * 72)
    print("[1] Register student")
    print("[2] Find student")
    print("[3] Update student details")
    print("[4] Remove student")
    print("[5] Record student entry/exit")
    print("[6] View events history")
    print("[7] View simulated guardian's message")
    print("[8] Exit")
    return get_menu_choice("Choose an option (1-8): ", {str(i) for i in range(1, 9)})

RETURN_TO_MAIN = object()
PAGE_SIZE = 10


def get_menu_choice(prompt, valid_choices):
    valid = {choice.upper() for choice in valid_choices}
    while True:
        choice = input(prompt).strip().upper()
        if choice in valid:
            return choice
        print("That choice is not on this menu. Please try again.")


def prompt_calendar_date(prompt, date_format, format_hint):
    """Read a valid date, with B to cancel and M to return to the main menu."""
    while True:
        raw_value = input(f"{prompt} ({format_hint}; B=Back, M=Main menu): ").strip()
        command = raw_value.upper()
        if command == "B":
            return None
        if command == "M":
            return RETURN_TO_MAIN
        try:
            return datetime.strptime(raw_value, date_format).date()
        except ValueError:
            print(f"Enter a valid date using {format_hint}.")


def find_students_by_class(grade_level, section):
    """Use a linear scan to find students in one grade and section."""
    matches = []
    target_section = section.casefold()
    for student in student_records:
        if (student.grade_level == grade_level
                and student.section.casefold() == target_section):
            matches.append(student)
    return insertion_sort(matches, student_class_key)


def find_students_by_name(keyword):
    """Use Linear Search for a case-insensitive partial name match."""
    target = keyword.casefold()
    matches = []
    for student in student_records:
        if target in student.full_name.casefold():
            matches.append(student)
    return insertion_sort(matches, student_class_key)


def find_students_by_number(keyword):
    """Use Linear Search for a full or partial student-number match."""
    target = keyword.casefold()
    matches = []
    for student in student_records:
        if target in student.id_no.casefold():
            matches.append(student)
    return selection_sort(matches, student_number_key)


def run_find_student_menu():
    """Offer the three student-finding paths requested for the main menu."""
    while True:
        display_section_header("Find Student")
        print("[1] Find by grade and section")
        print("[2] Find by name")
        print("[3] Find by student ID number")
        print("[B] Back to main menu")
        choice = get_menu_choice("Choose an option: ", {"1", "2", "3", "B"})
        if choice == "B":
            return

        if choice == "1":
            grade_level, section = get_class_assignment()
            matches = find_students_by_class(grade_level, section)
            title = f"G{grade_level} - {section}"
        elif choice == "2":
            keyword = get_non_empty_input("Enter all or part of the student's name: ")
            matches = find_students_by_name(keyword)
            title = f"Name matches for {keyword!r}"
        else:
            keyword = get_non_empty_input("Enter the full or partial student ID number: ")
            matches = find_students_by_number(keyword)
            title = f"Student number matches for {keyword!r}"

        navigation = browse_student_results(matches, title)
        if navigation is RETURN_TO_MAIN:
            return


def browse_student_results(students, title):
    """Display a paginated result list and open a selected student's details."""
    if not students:
        display_section_header(title)
        print("No matching students were found.")
        choice = get_menu_choice("[B] Back to search options  [M] Main menu: ", {"B", "M"})
        return RETURN_TO_MAIN if choice == "M" else None

    page = 0
    total_pages = (len(students) + PAGE_SIZE - 1) // PAGE_SIZE
    while True:
        start = page * PAGE_SIZE
        page_students = students[start:start + PAGE_SIZE]
        display_section_header(f"{title} | Page {page + 1} of {total_pages}")
        for position, student in enumerate(page_students, start=1):
            print(f"[{position}] {student.id_no} | {student.full_name} | "
                  f"Grade {student.grade_level}, {student.section}")
        choices = {str(i) for i in range(1, len(page_students) + 1)} | {"B", "M"}
        if page > 0:
            choices.add("P")
        if page + 1 < total_pages:
            choices.add("N")
        navigation_labels = []
        if page > 0:
            navigation_labels.append("[P] Previous page")
        if page + 1 < total_pages:
            navigation_labels.append("[N] Next page")
        navigation_labels.extend(("[B] Back to search options", "[M] Main menu"))
        print("  ".join(navigation_labels))
        choice = get_menu_choice("Choose a result number or navigation option: ", choices)
        if choice == "B":
            return None
        if choice == "M":
            return RETURN_TO_MAIN
        if choice == "P":
            page -= 1
            continue
        if choice == "N":
            page += 1
            continue
        navigation = view_student_details(page_students[int(choice) - 1])
        if navigation is RETURN_TO_MAIN:
            return RETURN_TO_MAIN


def view_student_details(student):
    """Show a selected student's details and provide access to filtered history."""
    while True:
        display_section_header("Student Details")
        print_student(student)
        print("[1] View this student's event history")
        print("[B] Back to search results  [M] Main menu")
        choice = get_menu_choice("Choose an option: ", {"1", "B", "M"})
        if choice == "B":
            return None
        if choice == "M":
            return RETURN_TO_MAIN
        navigation = run_student_history_menu(student)
        if navigation is RETURN_TO_MAIN:
            return RETURN_TO_MAIN


def filter_student_history(student, period, selected_date):
    """Filter one student's events for a selected day, seven-day week, or month."""
    if period == "day":
        start_date = selected_date
        end_date = selected_date
        title = f"{student.full_name}: events on {selected_date.isoformat()}"
    elif period == "week":
        start_date = selected_date
        end_date = selected_date + timedelta(days=6)
        title = (f"{student.full_name}: events from {start_date.isoformat()} "
                 f"through {end_date.isoformat()}")
    else:
        start_date = selected_date
        title = f"{student.full_name}: events for {selected_date.strftime('%B %Y')}"

    matches = []
    for record in attendance_records:
        if record.id_qr != student.id_qr:
            continue
        event_date = record.timestamp.date()
        if period == "month":
            if event_date.year == selected_date.year and event_date.month == selected_date.month:
                matches.append(record)
        elif start_date <= event_date <= end_date:
            matches.append(record)
    return browse_attendance_records(merge_sort(matches, timestamp_key), title,
                                     "Back to history filters")


def run_student_history_menu(student):
    """Choose a specific day, seven-day week, or calendar month for a student's history."""
    while True:
        display_section_header(f"Event History: {student.full_name}")
        print("[1] Choose a specific day")
        print("[2] Choose a week (7 days starting on the selected date)")
        print("[3] Choose a calendar month")
        print("[B] Back to student details  [M] Main menu")
        choice = get_menu_choice("Choose a time period: ", {"1", "2", "3", "B", "M"})
        if choice == "B":
            return None
        if choice == "M":
            return RETURN_TO_MAIN

        if choice == "1":
            selected_date = prompt_calendar_date("Date", "%Y-%m-%d", "YYYY-MM-DD")
            period = "day"
        elif choice == "2":
            selected_date = prompt_calendar_date("First day of the 7-day period", "%Y-%m-%d", "YYYY-MM-DD")
            period = "week"
        else:
            selected_date = prompt_calendar_date("Month", "%Y-%m", "YYYY-MM")
            period = "month"

        if selected_date is RETURN_TO_MAIN:
            return RETURN_TO_MAIN
        if selected_date is None:
            continue
        navigation = filter_student_history(student, period, selected_date)
        if navigation is RETURN_TO_MAIN:
            return RETURN_TO_MAIN


def browse_attendance_records(records, title, back_label="Back"):
    """Display already-sorted event records in pages with consistent navigation."""
    if not records:
        display_section_header(title)
        print("No attendance events match this view.")
        choice = get_menu_choice(f"[B] {back_label}  [M] Main menu: ", {"B", "M"})
        return RETURN_TO_MAIN if choice == "M" else None

    page = 0
    total_pages = (len(records) + PAGE_SIZE - 1) // PAGE_SIZE
    while True:
        start = page * PAGE_SIZE
        page_records = records[start:start + PAGE_SIZE]
        display_section_header(f"{title} | Page {page + 1} of {total_pages}")
        for record in page_records:
            print_attendance_record(record)
        choices = {"B", "M"}
        if page > 0:
            choices.add("P")
        if page + 1 < total_pages:
            choices.add("N")
        navigation_labels = []
        if page > 0:
            navigation_labels.append("[P] Previous page")
        if page + 1 < total_pages:
            navigation_labels.append("[N] Next page")
        navigation_labels.extend((f"[B] {back_label}", "[M] Main menu"))
        print("  ".join(navigation_labels))
        choice = get_menu_choice("Choose a navigation option: ", choices)
        if choice == "B":
            return None
        if choice == "M":
            return RETURN_TO_MAIN
        if choice == "P":
            page -= 1
        elif choice == "N":
            page += 1


def run_event_history_menu():
    """Provide daily summary and overall chronological event history."""
    while True:
        display_section_header("View Events History")
        print("[1] Today's daily summary and events")
        print("[2] Overall event history")
        print("[B] Back to main menu")
        choice = get_menu_choice("Choose an option: ", {"1", "2", "B"})
        if choice == "B":
            return
        if choice == "1":
            today_records = display_daily_summary()
            navigation = browse_attendance_records(
                today_records, "Today's Entry and Exit Events", "Back to event history options"
            )
        else:
            ordered = merge_sort(attendance_records, timestamp_key)
            navigation = browse_attendance_records(
                ordered, "Overall Event History", "Back to event history options"
            )
        if navigation is RETURN_TO_MAIN:
            return

def update_student():
    display_section_header("Update Student")
    student = get_student_by_lookup("Student number or QR ID to update: ")
    if student is None:
        return
    print("Press Enter to keep each current value.")
    print_student(student)
    name = input(f"New name [{student.full_name}]: ").strip()
    new_class = get_class_assignment((student.grade_level, student.section))
    birthday = input(f"New birthday [{student.birthday}]: ").strip()
    contact = input(f"New student contact [{student.contact_number}]: ").strip()
    guardian = input(f"New guardian name [{student.guardian_name}]: ").strip()
    guardian_contact = input(
        f"New guardian contact [{student.guardian_contact}]: "
    ).strip()
    if name:
        student.full_name = name
    if new_class is not None:
        allowed, reason = class_has_capacity(
            new_class[0], new_class[1], exclude_student=student
        )
        if allowed:
            student.grade_level, student.section = new_class
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
    """Run the single-file terminal application until the user exits."""
    display_program_header()
    actions = {
        "1": register_student,
        "2": run_find_student_menu,
        "3": update_student,
        "4": remove_student,
        "5": record_entry_or_exit,
        "6": run_event_history_menu,
        "7": view_parent_message,
    }
    while True:
        choice = display_main_menu()
        if choice == "8":
            print("\nThank you for using the campus recording system.")
            return
        actions[choice]()

if __name__ == "__main__":
    run_program()
