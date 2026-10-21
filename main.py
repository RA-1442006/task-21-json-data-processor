import sys
import os
import processor
import report

def run_demo():
    # Resolve directory paths relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "data", "employees.json")
    json_output_file = os.path.join(base_dir, "output", "filtered_results.json")
    report_output_file = os.path.join(base_dir, "output", "summary_report.txt")

    # 1. Load the json file
    result = processor.load_json_file(input_file)
    if result["error"]:
        print(f"Error loading file: {result['error']}")
        return

    raw_data = result["data"]

    # 2. Validate records and skip invalid ones
    processed = processor.process_employee_data(raw_data)
    valid_employees = processed["valid_employees"]
    skipped = processed["skipped"]

    # 3. Generate summary statistics
    summary = processor.generate_summary(valid_employees, skipped)

    # 4. Run sample searches and filters to exercise all processor functions
    name_matches = processor.search_by_name(valid_employees, "alice")
    id_match = processor.search_by_id(valid_employees, 102)
    skill_matches = processor.search_by_skill(valid_employees, "Python")

    dept_matches = processor.filter_by_department(valid_employees, "Engineering")
    salary_matches = processor.filter_by_salary_range(valid_employees, min_salary=60000, max_salary=90000)
    city_matches = processor.filter_by_city(valid_employees, "Pune")
    ongoing_matches = processor.filter_by_project_status(valid_employees, "ongoing")

    sample_results = {
        "name_search": {"query": "alice", "matches": name_matches},
        "id_search": {"target_id": 102, "result": id_match},
        "skill_search": {"skill": "Python", "matches": skill_matches},
        "department_filter": {"department": "Engineering", "matches": dept_matches},
        "salary_filter": {"min": 60000, "max": 90000, "matches": salary_matches},
        "city_filter": {"city": "Pune", "matches": city_matches},
        "project_status_filter": {"status": "ongoing", "matches": ongoing_matches}
    }

    # 5. Save combined filtered & summarized results to output/filtered_results.json
    export_payload = {
        "summary": summary,
        "skipped_records": skipped,
        "sample_searches": {
            "search_name_alice": name_matches,
            "search_id_102": id_match,
            "search_skill_python": skill_matches
        },
        "sample_filters": {
            "department_engineering": dept_matches,
            "salary_range_60000_to_90000": salary_matches,
            "city_pune": city_matches,
            "project_status_ongoing": ongoing_matches
        }
    }
    processor.save_to_json(export_payload, json_output_file)

    # 6. Generate, print, and save the readable text report
    report.print_and_save_report(summary, skipped, sample_results, report_output_file)

    print(f"\n[OK] Results saved to JSON : {json_output_file}")
    print(f"[OK] Summary report saved  : {report_output_file}")


def interactive_menu():
    # Simple interactive console menu
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "data", "employees.json")

    result = processor.load_json_file(input_file)
    if result["error"]:
        print(f"Error loading file: {result['error']}")
        return

    processed = processor.process_employee_data(result["data"])
    valid_employees = processed["valid_employees"]
    skipped = processed["skipped"]

    while True:
        print("\n--- JSON DATA PROCESSOR MENU ---")
        print("1. View Company Summary Report")
        print("2. Search by Employee Name")
        print("3. Search by Employee ID")
        print("4. Search by Skill")
        print("5. Filter by Department")
        print("6. Filter by Salary Range")
        print("7. Filter by City")
        print("8. Filter by Project Status")
        print("9. Run Full Demo & Save Files")
        print("0. Exit")

        choice = input("Enter choice (0-9): ").strip()
        if choice == "0":
            print("Exiting. Bye!")
            break
        elif choice == "1":
            summary = processor.generate_summary(valid_employees, skipped)
            report.print_and_save_report(summary, skipped)
        elif choice == "2":
            q = input("Enter name to search: ")
            matches = processor.search_by_name(valid_employees, q)
            print(f"Found {len(matches)} match(es):")
            for m in matches:
                print(f"  - {m['name']} | Dept: {m['department']} | Salary: ${m['salary']:,}")
        elif choice == "3":
            val = input("Enter employee ID: ")
            try:
                emp_id = int(val)
                emp = processor.search_by_id(valid_employees, emp_id)
                if emp:
                    print(f"Found: {emp['name']} | Dept: {emp['department']} | City: {emp['city']} | Salary: ${emp['salary']:,}")
                else:
                    print("Employee not found.")
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
        elif choice == "4":
            skill = input("Enter skill (e.g. Python): ")
            matches = processor.search_by_skill(valid_employees, skill)
            print(f"Found {len(matches)} match(es) with skill '{skill}':")
            for m in matches:
                print(f"  - {m['name']} ({m['department']})")
        elif choice == "5":
            dept = input("Enter department (e.g. Engineering): ")
            matches = processor.filter_by_department(valid_employees, dept)
            print(f"Found {len(matches)} employee(s) in {dept}:")
            for m in matches:
                print(f"  - {m['name']} | ${m['salary']:,}")
        elif choice == "6":
            try:
                min_s = float(input("Enter minimum salary: "))
                max_s = float(input("Enter maximum salary: "))
                matches = processor.filter_by_salary_range(valid_employees, min_s, max_s)
                print(f"Found {len(matches)} employee(s):")
                for m in matches:
                    print(f"  - {m['name']} | ${m['salary']:,}")
            except ValueError:
                print("Invalid number.")
        elif choice == "7":
            city = input("Enter city name: ")
            matches = processor.filter_by_city(valid_employees, city)
            print(f"Found {len(matches)} employee(s) in {city}:")
            for m in matches:
                print(f"  - {m['name']} ({m['department']})")
        elif choice == "8":
            status = input("Enter status (ongoing/completed): ")
            matches = processor.filter_by_project_status(valid_employees, status)
            print(f"Found {len(matches)} employee(s) with '{status}' projects:")
            for m in matches:
                print(f"  - {m['name']}")
        elif choice == "9":
            run_demo()
        else:
            print("Invalid choice. Please select from 0 to 9.")

def main():
    # If the user passes --menu or -m, launch interactive mode
    if len(sys.argv) > 1 and sys.argv[1] in ["--menu", "-m"]:
        interactive_menu()
    else:
        run_demo()

if __name__ == "__main__":
    main()
