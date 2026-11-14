# PSHS-ZRC Student Entrance and Exit Recording System

## I. Background

The program models a campus gate process in which a guard records each student's entry or exit. The campus has six grade levels, Grades 7 through 12, with three sections of up to 30 students each, for a maximum of 540 student records. Students are classified as interns, who live in campus dormitories, or externs, who live off campus. Interns are recorded as either weekenders or Friday-home interns who usually return on Sunday. These residence details help staff understand the student's context; they do not determine whether a trip is allowed. The Q2 alternative assessment calls for at least one searching algorithm, one sorting algorithm, and project documentation (Philippine Science High School, Zamboanga Peninsula Region Campus, 2026).

Students can leave and return more than once, including during weekends. The program therefore records each event as an individual timestamped entry or exit rather than enforcing a fixed schedule. Organizing a roster by grade, section, and name helps teachers and campus staff find a student. Searching helps locate a record, while chronological event lists help guards, teachers, and dorm managers review recorded campus movements.

The project goal is to provide a terminal-based prototype that records the student roster and entry/exit events in one Python file. Its measurable targets are to support up to 540 students, enforce a maximum of 30 registered students per section and three section names per grade level, assign a distinct student number to each registration during a run, and display correct search and sort results for the registered data. The program keeps its data in memory, so registrations and attendance events are lost when the program closes. It is not a persistent or live attendance system.

## II. Application

### Program description and features

The program is a menu-driven Python application intended for guards and authorized school staff. It uses `Student`, `AttendanceRecord`, and `CampusSystem` classes. Registration collects a student's name, grade, section, birthday, contact details, residence type, intern subtype when applicable, and guardian contact details.

The two identifiers have distinct purposes:

- `id_qr` is the student's student ID expressed as a QR payload string. The prototype generates a value such as `PSHS-ZRC:STUDENT:16-2026-001`. It does not generate a QR image or scan a physical card; the payload can be typed into the terminal.
- `id_no` is the separate student number in the form `16-YYYY-NNN`. `YYYY` is the year the student entered as a freshman. `NNN` is a three-digit sequence assigned during the current program run.

A user records each movement separately by identifying the student and selecting Entry or Exit. The program stores the timestamp and prepares a simulated guardian message, but it does not send SMS or email. The program also provides roster views, student lookup, event history, a daily event list, and a daily entry/exit summary.

Residence type is descriptive. The software does not assume that an intern remains in the dorm, that an extern makes only one trip per day, or that a student's movement is invalid because it differs from a typical schedule. The optional current-presence view estimates status from each student's latest event recorded in the current run. It is not a live presence guarantee. An unrecorded movement or closing the program can make that estimate incomplete.

### Searching and sorting

The program implements the algorithms directly in the single Python file. It does not call Python's built-in `list.sort()` or `sorted()` for these program features. The course slides cover Bubble, Selection, Insertion, Merge, and Quick Sort; this program uses Insertion, Selection, and Merge Sort (Philippine Science High School, Zamboanga Peninsula Region Campus, n.d.). The selected features are:

| Feature | Algorithm | How it is used and why |
|---|---|---|
| Student directory ordered by grade, section, then name | Insertion Sort | Builds a class-oriented roster using a multi-field key. The roster is capped at 540, and Insertion Sort is simple to trace and works well on small or nearly ordered lists. Best-case time is O(n); average and worst-case time are O(n²). The feature returns a copy, so the list copy uses O(n) space; the insertion procedure itself uses O(1) additional space. |
| All attendance events in date/time order | Merge Sort | Recursively splits event records and merges them by timestamp. The event log may contain several movements per student, so its size can grow beyond the student count. Merge Sort has O(n log n) time in best, average, and worst cases and uses O(n) additional space for merged lists. |
| Student finder with results ordered by class | Linear Search followed by Insertion Sort | Linear Search checks each registered student's searchable fields for the requested substring. It is easy to use with a roster of up to 540 students and supports searches by `id_qr`, `id_no`, name, grade, section, and residence. Search time is O(n), plus the cost of checking each record's text. Matching results are then ordered by grade, section, and name with Insertion Sort. |
| Student directory ordered by `id_no` | Selection Sort | Each pass locates the smallest remaining student number and places it in the next position. The fixed `16-YYYY-NNN` structure gives a consistent key. Selection Sort is included to demonstrate a second method from the class slides; it takes O(n²) comparisons and O(1) auxiliary sorting space, apart from the O(n) returned copy. |
| One student's event history in date/time order | Linear Search and Merge Sort | Linear Search locates the requested student by either identifier. The program filters that student's recorded events and applies Merge Sort by timestamp. This presents repeated weekend departures and returns, as well as longer absences, in the order they were recorded. |
| Today's attendance events in time order | Insertion Sort | The program filters events to the current date and orders them by timestamp. Daily event lists are expected to be much smaller than the entire roster. Insertion Sort is easy to explain and performs well when the list is already nearly ordered. Its average and worst-case time is O(n²). |

The sort routines return new lists, leaving registration order and the underlying event history unchanged. Equal sort keys retain their order in the Insertion and Merge Sort routines. The daily summary counts today's ENTRY and EXIT records without treating multiple valid movements as errors.

### Validation performed

The program passed a Python syntax check and terminal menu smoke test covering registration, student search, event recording, chronological event views, student history, ID-number sorting, and the session-only presence estimate. Separate checks exercised each sorting method with empty, single-item, duplicate-value, and reverse-ordered inputs. Tests also checked that `id_qr` and `id_no` both find the same student, and that the capacity checks reject a 31st student in one section and a fourth section within one grade.

### Rationale and limits

The algorithms match the data and the assignment. A class-grouped student directory is directly useful to staff who need to locate students by grade or section. Linear Search is appropriate for the bounded roster and can find partial text without requiring the list to be sorted first. Insertion Sort is suitable for small rosters and daily lists, and its shifts are visible when tracing the method. Selection Sort demonstrates the repeated minimum-selection process using student numbers. Merge Sort is used for event histories because it maintains O(n log n) time as records accumulate and gives a clear split-and-merge process.

The current-presence display uses the most recent recorded event for each registered student in the running session. An ENTRY means the student is presumed on campus and an EXIT means presumed off campus. The estimate can be wrong if a gate event is missed, the student is removed, or the program is restarted. The program stores no data between runs, uses typed text in place of actual QR scanning, and does not transmit guardian notifications. Those limits should be addressed before relying on it for real attendance decisions.

## III. References

Philippine Science High School, Zamboanga Peninsula Region Campus. (2026). *CS 5: Data structures and algorithms alternative assessment, second quarter SY 2026–2027* [Assignment description].

Philippine Science High School, Zamboanga Peninsula Region Campus. (n.d.). *Sorting algorithms* [PowerPoint slides]. CS 5 course material.
