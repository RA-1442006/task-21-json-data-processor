# Task 21: JSON Data Processor

A Python data processing project that reads structured employee information from a JSON file, validates records, handles messy or incomplete data gracefully, and performs searching, filtering, and summary operations.

This project was built as part of an internship assignment focused on learning core JSON handling and structured data manipulation in Python using only the standard library (`json`, `os`, `sys`).

---

## What It Does

1. **Loads and parses JSON data safely**: Reads `data/employees.json` using Python's built-in `json.load()` and catches `FileNotFoundError` or malformed JSON syntax errors with human-friendly messages.
2. **Validates records**: Checks every record for mandatory keys, valid numeric data types, and non-empty nested lists. Records that fail validation are skipped, while logging the reason and employee info.
3. **Searches data**:
   - By employee name (case-insensitive, partial matching)
   - By unique employee ID
   - By technical skill (case-insensitive check inside lists)
4. **Filters data**:
   - By department
   - By salary range (min and max limits)
   - By city (checks both root city and nested address city)
   - By project status (ongoing vs. completed)
5. **Summarizes insights**:
   - Total active headcount
   - Company average salary
   - Highest and lowest paid employees
   - Department employee counts and percentage distributions
   - Most common skill across the company and skill frequency counts
   - Total completed vs. ongoing project counts
6. **Exports results**:
   - Saves filtered datasets and summary statistics to `output/filtered_results.json` using `json.dump()` with an indentation of 4 spaces.
   - Generates and writes an aligned text report to `output/summary_report.txt`.

---

## Folder Structure

```text
task-21-json-data-processor/
  ├── data/
  │   └── employees.json            # Input dataset with 15 employee records (including messy ones)
  ├── output/
  │   ├── filtered_results.json     # Filtered and summarized results exported via json.dump()
  │   ├── sample_output.txt         # Real output saved from a successful execution
  │   └── summary_report.txt        # Clean human-readable summary report
  ├── processor.py                  # Pure data logic: loading, validation, search, filter, summary (no print statements)
  ├── report.py                     # Output formatting and console/file printing only
  ├── main.py                       # Application entry point with automated demo flow and optional interactive menu
  ├── README.md                     # Project documentation and learning notes
  └── .gitignore                    # Git ignore file (keeps output directory tracked)
```

---

## How to Run

No external third-party dependencies are required. Any standard Python 3 installation will work.

### 1. Run the Full Demo Flow (Default)

Running `main.py` directly executes the full pipeline: loading the data, validating records, generating the summary, running sample searches/filters, and writing out the report and JSON output:

```bash
python main.py
```

### 2. Run the Interactive Menu

If you want to interactively query employees, search by skills, or filter departments from the command line:

```bash
python main.py --menu
```

---

## How Missing Keys and Invalid Values Are Handled

Real-world datasets are rarely completely clean. To test our validation logic, `data/employees.json` deliberately contains 3 messy records among its 15 total entries:
- **Record ID 105 (Ethan Hunt)**: Missing the required `"salary"` key entirely.
- **Record ID 111 (Kevin Bacon)**: Has an empty skills list (`"skills": []`).
- **Record ID 114 (Nina Patel)**: Contains a string instead of a number for salary (`"salary": "abc"`).

In `processor.py`, the `validate_employee(emp)` function performs several validation checks on each record:
1. **Dictionary Check**: Ensures the item is a valid dictionary.
2. **Missing Key Validation**: Iterates through all mandatory keys (`id`, `name`, `age`, `department`, `salary`, `city`, `skills`, `address`, `projects`). If any key is missing, the record is rejected with an explanation like `Missing required key: 'salary'`.
3. **Type and Value Checks**:
   - `salary`: Verifies that salary is a numeric type (`int` or `float`, not boolean) and strictly greater than zero. Strings like `"abc"` are caught and rejected.
   - `age`: Verifies that age is a positive integer.
   - `skills`: Verifies that skills is a `list` and has at least one item (`len(skills) > 0`). Empty lists are caught and rejected.
   - `address`: Ensures address is a dictionary containing `city`, `state`, and `pincode`.
   - `projects`: Ensures projects is a list.

Whenever an invalid record is detected, it is appended to a `skipped` list containing the employee's ID, name, and the specific failure reason. The processing pipeline continues without crashing, ensuring clean downstream statistics.

---

## Questions on JSON and Python

### 1. What is JSON?
JSON stands for **JavaScript Object Notation**. It is a lightweight, human-readable, and text-based standard format used for storing and exchanging data across different systems, APIs, and programming languages. It represents data using key-value pairs (objects) and ordered sequences (arrays).

### 2. What is the difference between JSON and a Python dictionary?
- **Format vs. Data Structure**: JSON is a **text format** (a string according to a specific syntax specification), whereas a Python dictionary is an **in-memory data structure** (an object in Python).
- **Syntax Differences**:
  - In JSON, keys **must** be enclosed in double quotes (`"key": "value"`). Python dictionaries allow single quotes, double quotes, or any hashable object (like integers or tuples) as keys.
  - JSON boolean values are lowercase (`true`, `false`) and null values are `null`. In Python, they are capitalized (`True`, `False`) and `None`.
- **Interoperability**: JSON can be read by almost any language (JavaScript, Go, Java, Python), whereas a Python dictionary exists only within a Python runtime.

### 3. How do you read JSON from a file in Python?
You import the built-in `json` module, open the file in read mode with proper encoding, and pass the file object to `json.load()`:

```python
import json

with open("data/employees.json", "r", encoding="utf-8") as f:
    employee_data = json.load(f)
```

`json.load()` reads the file stream and deserializes the JSON text into native Python objects (dictionaries, lists, strings, numbers, booleans).

---

## What I Learned

During this task, I learned several practical skills in Python:
- **Separation of Concerns**: Splitting pure data logic (`processor.py`) from report presentation (`report.py`) and application orchestration (`main.py`) kept the code clean and testable.
- **Defensive Programming**: Writing small validation functions prevents runtime errors like `KeyError` or `TypeError` when computing averages or iterating over nested fields.
- **Handling Nested Data Structures**: Working with dictionaries containing nested dictionaries (`address`) and lists of dictionaries (`projects`) taught me how to navigate complex data with list comprehensions and `.get()`.
- **File I/O with Standard Modules**: Using `json.load()` and `json.dump(data, f, indent=4)` without relying on any external packages.

---

## Sample Output

Below is the real console output produced by running `python main.py` on `data/employees.json`:

```text
Sample output of main.py
========================================================================
                     EMPLOYEE DATA PROCESSING REPORT
========================================================================

1. DATASET INGESTION & VALIDATION
------------------------------------------------------------------------
Total Records Read    : 15
Valid Records         : 12
Skipped Records       : 3

Skipped Records Details:
  - ID: 105   | Name: Ethan Hunt         | Reason: Missing required key: 'salary'
  - ID: 111   | Name: Kevin Bacon        | Reason: Skills list cannot be empty
  - ID: 114   | Name: Nina Patel         | Reason: Salary must be a number, got 'abc'

2. SALARY & COMPENSATION SUMMARY
------------------------------------------------------------------------
Active Employees       : 12
Average Salary         : $68,500.00
Highest Paid Employee  : Ian Malcolm (Engineering) - $96,000.00 (ID: 109)
Lowest Paid Employee   : Charlie Brown (Marketing) - $48,000.00 (ID: 103)

3. DEPARTMENT BREAKDOWN
------------------------------------------------------------------------
Department               Count      Percentage
------------------------------------------------------------------------
Engineering              4          33.3%
Marketing                2          16.7%
Sales                    2          16.7%
HR                       2          16.7%
Design                   2          16.7%
------------------------------------------------------------------------

4. SKILLS OVERVIEW
------------------------------------------------------------------------
Most Common Skill      : Python (4 employees)

Skill Counts:
  - Python                : 4
  - Figma                 : 2
  - Negotiation           : 2
  - Payroll               : 2
  - SEO                   : 2
  - SQL                   : 2
  - AWS                   : 1
  - B2B Sales             : 1
  - CRM                   : 1
  - Client Management     : 1
  - Compliance            : 1
  - Content Strategy      : 1
  - Copywriting           : 1
  - Design Systems        : 1
  - Docker                : 1
  - Email Marketing       : 1
  - Employee Relations    : 1
  - Google Analytics      : 1
  - HTML/CSS              : 1
  - Java                  : 1
  - Kubernetes            : 1
  - Lead Generation       : 1
  - Machine Learning      : 1
  - Microservices         : 1
  - Prototyping           : 1
  - Recruitment           : 1
  - Spring Boot           : 1
  - UI/UX                 : 1

5. PROJECTS OVERVIEW
------------------------------------------------------------------------
Completed Projects     : 9
Ongoing Projects       : 8
Total Projects Tracked : 17

6. SAMPLE SEARCHES & FILTERS DEMONSTRATION
------------------------------------------------------------------------
[A] Search by Name: 'alice' (Found: 1)
    - Alice Johnson (ID: 101) | Dept: Engineering | Salary: $75,000.00

[B] Search by ID: 102
    - Found: Bob Smith | Dept: Engineering | City: Pune | Salary: $82,000.00

[C] Search by Skill: 'Python' (Found: 4)
    - Alice Johnson (Engineering) | City: Bangalore | Salary: $75,000.00
    - Diana Prince (Engineering) | City: Hyderabad | Salary: $92,000.00
    - Ian Malcolm (Engineering) | City: Bangalore | Salary: $96,000.00
    - Oscar Martinez (HR) | City: Pune | Salary: $62,000.00

[D] Filter by Department: 'Engineering' (Found: 4)
    - Alice Johnson | Salary: $75,000.00 | City: Bangalore
    - Bob Smith | Salary: $82,000.00 | City: Pune
    - Diana Prince | Salary: $92,000.00 | City: Hyderabad
    - Ian Malcolm | Salary: $96,000.00 | City: Bangalore

[E] Filter by Salary Range: $60,000.00 - $90,000.00 (Found: 6)
    - Alice Johnson      | Dept: Engineering  | Salary: $75,000.00
    - Bob Smith          | Dept: Engineering  | Salary: $82,000.00
    - George Clark       | Dept: HR           | Salary: $68,000.00
    - Laura Croft        | Dept: Design       | Salary: $64,000.00
    - Michael Scott      | Dept: Sales        | Salary: $72,000.00
    - Oscar Martinez     | Dept: HR           | Salary: $62,000.00

[F] Filter by City: 'Pune' (Found: 3)
    - Bob Smith | Dept: Engineering | State: Maharashtra
    - Hannah Abbott | Dept: Design | State: Maharashtra
    - Oscar Martinez | Dept: HR | State: Maharashtra

[G] Filter by Project Status: 'ongoing' (Found: 8)
    - Alice Johnson      | Projects: Cloud Migration
    - Charlie Brown      | Projects: Q1 Campaign
    - Diana Prince       | Projects: Monitoring Dashboard
    - George Clark       | Projects: Hiring Drive 2026
    - Hannah Abbott      | Projects: Mobile App UI
    - Ian Malcolm        | Projects: Recommendation Engine
    - Laura Croft        | Projects: Design System 2.0
    - Michael Scott      | Projects: Regional Sales Expansion

========================================================================
                          END OF REPORT
========================================================================

[OK] Results saved to JSON : C:\Users\realc\.gemini\antigravity\scratch\task-21-json-data-processor\output\filtered_results.json
[OK] Summary report saved  : C:\Users\realc\.gemini\antigravity\scratch\task-21-json-data-processor\output\summary_report.txt
```
