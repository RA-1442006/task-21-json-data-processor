import json
import os

# Fields every employee record must have
REQUIRED_KEYS = ["id", "name", "age", "department", "salary", "city", "skills", "address", "projects"]

def load_json_file(filepath):
    # Check if file exists first
    if not os.path.exists(filepath):
        return {"error": f"File not found: '{filepath}'", "data": None}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {"error": None, "data": data}
    except json.JSONDecodeError as err:
        return {"error": f"Invalid JSON format on line {err.lineno}: {err.msg}", "data": None}
    except Exception as err:
        return {"error": f"Could not read file: {str(err)}", "data": None}

def validate_employee(emp):
    # Make sure the employee record is a dictionary
    if not isinstance(emp, dict):
        return False, "Record is not a dictionary"

    # Check for missing keys
    for key in REQUIRED_KEYS:
        if key not in emp:
            return False, f"Missing required key: '{key}'"

    # Salary must be a positive number
    if isinstance(emp["salary"], bool) or not isinstance(emp["salary"], (int, float)):
        return False, f"Salary must be a number, got '{emp['salary']}'"
    if emp["salary"] <= 0:
        return False, "Salary must be greater than zero"

    # Age must be a positive integer
    if isinstance(emp["age"], bool) or not isinstance(emp["age"], int) or emp["age"] <= 0:
        return False, f"Age must be a positive integer, got '{emp['age']}'"

    # Skills should be a list and cannot be empty
    if not isinstance(emp["skills"], list):
        return False, "Skills must be a list"
    if len(emp["skills"]) == 0:
        return False, "Skills list cannot be empty"

    # Address must be a dictionary with city, state, and pincode
    if not isinstance(emp["address"], dict):
        return False, "Address must be a dictionary"
    for addr_key in ["city", "state", "pincode"]:
        if addr_key not in emp["address"]:
            return False, f"Address is missing '{addr_key}'"

    # Projects should be a list
    if not isinstance(emp["projects"], list):
        return False, "Projects must be a list"

    return True, ""

def process_employee_data(raw_data):
    # Validate records and keep track of skipped ones
    valid_employees = []
    skipped = []

    if not isinstance(raw_data, list):
        return {
            "valid_employees": [],
            "skipped": [{"id": None, "name": "N/A", "reason": "Expected JSON to contain a list of employees"}],
            "total_count": 0,
            "valid_count": 0,
            "skipped_count": 1
        }

    for emp in raw_data:
        is_valid, reason = validate_employee(emp)
        if is_valid:
            valid_employees.append(emp)
        else:
            emp_id = emp.get("id") if isinstance(emp, dict) else None
            emp_name = emp.get("name") if isinstance(emp, dict) else "Unknown"
            skipped.append({
                "id": emp_id,
                "name": emp_name,
                "reason": reason
            })

    return {
        "valid_employees": valid_employees,
        "skipped": skipped,
        "total_count": len(raw_data),
        "valid_count": len(valid_employees),
        "skipped_count": len(skipped)
    }

# --- SEARCH FUNCTIONS ---

def search_by_name(employees, name_query):
    # Partial and case-insensitive search on name
    query = name_query.strip().lower()
    matches = []
    for emp in employees:
        if query in emp.get("name", "").lower():
            matches.append(emp)
    return matches

def search_by_id(employees, emp_id):
    # Search for an employee by exact ID
    for emp in employees:
        if emp.get("id") == emp_id:
            return emp
    return None

def search_by_skill(employees, skill_name):
    # Case-insensitive skill search
    target = skill_name.strip().lower()
    matches = []
    for emp in employees:
        skills = [s.lower() for s in emp.get("skills", [])]
        if target in skills:
            matches.append(emp)
    return matches

# --- FILTER FUNCTIONS ---

def filter_by_department(employees, department):
    # Case-insensitive filter by department
    dept = department.strip().lower()
    return [emp for emp in employees if emp.get("department", "").lower() == dept]

def filter_by_salary_range(employees, min_salary=None, max_salary=None):
    # Filter employees within salary bounds
    results = []
    for emp in employees:
        sal = emp.get("salary", 0)
        if min_salary is not None and sal < min_salary:
            continue
        if max_salary is not None and sal > max_salary:
            continue
        results.append(emp)
    return results

def filter_by_city(employees, city):
    # Check both top-level city and nested address city
    target_city = city.strip().lower()
    results = []
    for emp in employees:
        emp_city = emp.get("city", "").lower()
        addr_city = emp.get("address", {}).get("city", "").lower()
        if target_city == emp_city or target_city == addr_city:
            results.append(emp)
    return results

def filter_by_project_status(employees, status):
    # Keep employees who have at least one project with this status
    target_status = status.strip().lower()
    results = []
    for emp in employees:
        for proj in emp.get("projects", []):
            if proj.get("status", "").lower() == target_status:
                results.append(emp)
                break
    return results

# --- SUMMARY FUNCTIONS ---

def generate_summary(employees, skipped=None):
    # Build overall summary metrics
    if not employees:
        return {
            "total_employees": 0,
            "average_salary": 0.0,
            "highest_paid": None,
            "lowest_paid": None,
            "department_counts": {},
            "most_common_skill": {"skill": None, "count": 0},
            "skill_counts": {},
            "project_status_counts": {"ongoing": 0, "completed": 0},
            "skipped_count": len(skipped) if skipped else 0
        }

    total_employees = len(employees)
    total_salary = sum(emp["salary"] for emp in employees)
    avg_salary = round(total_salary / total_employees, 2)

    # Find highest and lowest earners
    highest = max(employees, key=lambda x: x["salary"])
    lowest = min(employees, key=lambda x: x["salary"])

    # Count employees per department
    dept_counts = {}
    for emp in employees:
        dept = emp.get("department", "Unknown")
        dept_counts[dept] = dept_counts.get(dept, 0) + 1

    # Count skill occurrences
    skill_counts = {}
    for emp in employees:
        for skill in emp.get("skills", []):
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    # Figure out the most common skill
    top_skill = None
    top_skill_count = 0
    for skill, count in skill_counts.items():
        if count > top_skill_count:
            top_skill = skill
            top_skill_count = count

    # Count project statuses
    ongoing_count = 0
    completed_count = 0
    for emp in employees:
        for proj in emp.get("projects", []):
            st = proj.get("status", "").lower()
            if st == "ongoing":
                ongoing_count += 1
            elif st == "completed":
                completed_count += 1

    return {
        "total_employees": total_employees,
        "average_salary": avg_salary,
        "highest_paid": {
            "id": highest["id"],
            "name": highest["name"],
            "department": highest["department"],
            "salary": highest["salary"]
        },
        "lowest_paid": {
            "id": lowest["id"],
            "name": lowest["name"],
            "department": lowest["department"],
            "salary": lowest["salary"]
        },
        "department_counts": dept_counts,
        "most_common_skill": {
            "skill": top_skill,
            "count": top_skill_count
        },
        "skill_counts": skill_counts,
        "project_status_counts": {
            "ongoing": ongoing_count,
            "completed": completed_count
        },
        "skipped_count": len(skipped) if skipped else 0
    }

def save_to_json(data, output_path):
    # Save processed dictionary or list to JSON with clean indent
    folder = os.path.dirname(output_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return output_path
