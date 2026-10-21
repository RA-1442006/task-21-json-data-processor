import os

def format_currency(amount):
    # Quick helper to format money numbers nicely
    return f"${amount:,.2f}"

def build_report_text(summary, skipped=None, sample_results=None):
    # Build a clean text report line by line
    lines = []
    separator = "=" * 72
    thin_sep = "-" * 72

    lines.append(separator)
    lines.append("                     EMPLOYEE DATA PROCESSING REPORT")
    lines.append(separator)
    lines.append("")

    # 1. Ingestion and Validation
    lines.append("1. DATASET INGESTION & VALIDATION")
    lines.append(thin_sep)
    total_valid = summary.get("total_employees", 0)
    skipped_records = skipped if skipped else []
    total_read = total_valid + len(skipped_records)

    lines.append(f"Total Records Read    : {total_read}")
    lines.append(f"Valid Records         : {total_valid}")
    lines.append(f"Skipped Records       : {len(skipped_records)}")

    if skipped_records:
        lines.append("")
        lines.append("Skipped Records Details:")
        for item in skipped_records:
            emp_id = item.get("id") if item.get("id") is not None else "N/A"
            lines.append(f"  - ID: {str(emp_id):<5} | Name: {item.get('name', 'Unknown'):<18} | Reason: {item.get('reason')}")
    lines.append("")

    # 2. Salary Summary
    lines.append("2. SALARY & COMPENSATION SUMMARY")
    lines.append(thin_sep)
    lines.append(f"Active Employees       : {total_valid}")
    lines.append(f"Average Salary         : {format_currency(summary.get('average_salary', 0))}")

    high = summary.get("highest_paid")
    if high:
        lines.append(f"Highest Paid Employee  : {high['name']} ({high['department']}) - {format_currency(high['salary'])} (ID: {high['id']})")

    low = summary.get("lowest_paid")
    if low:
        lines.append(f"Lowest Paid Employee   : {low['name']} ({low['department']}) - {format_currency(low['salary'])} (ID: {low['id']})")
    lines.append("")

    # 3. Department Breakdown
    lines.append("3. DEPARTMENT BREAKDOWN")
    lines.append(thin_sep)
    lines.append(f"{'Department':<24} {'Count':<10} {'Percentage'}")
    lines.append(thin_sep)
    dept_counts = summary.get("department_counts", {})
    for dept, count in dept_counts.items():
        pct = (count / total_valid * 100) if total_valid > 0 else 0
        lines.append(f"{dept:<24} {count:<10} {pct:.1f}%")
    lines.append(thin_sep)
    lines.append("")

    # 4. Skills Breakdown
    lines.append("4. SKILLS OVERVIEW")
    lines.append(thin_sep)
    top_skill_info = summary.get("most_common_skill", {})
    lines.append(f"Most Common Skill      : {top_skill_info.get('skill')} ({top_skill_info.get('count')} employees)")
    lines.append("")
    lines.append("Skill Counts:")
    skill_counts = summary.get("skill_counts", {})
    # Sort skills by count descending, then alphabetically
    sorted_skills = sorted(skill_counts.items(), key=lambda x: (-x[1], x[0]))
    for skill, count in sorted_skills:
        lines.append(f"  - {skill:<22}: {count}")
    lines.append("")

    # 5. Projects Breakdown
    lines.append("5. PROJECTS OVERVIEW")
    lines.append(thin_sep)
    proj_counts = summary.get("project_status_counts", {})
    ongoing = proj_counts.get("ongoing", 0)
    completed = proj_counts.get("completed", 0)
    total_proj = ongoing + completed
    lines.append(f"Completed Projects     : {completed}")
    lines.append(f"Ongoing Projects       : {ongoing}")
    lines.append(f"Total Projects Tracked : {total_proj}")
    lines.append("")

    # 6. Sample Search and Filters
    if sample_results:
        lines.append("6. SAMPLE SEARCHES & FILTERS DEMONSTRATION")
        lines.append(thin_sep)

        # Name search
        if "name_search" in sample_results:
            ns = sample_results["name_search"]
            lines.append(f"[A] Search by Name: '{ns.get('query')}' (Found: {len(ns.get('matches', []))})")
            for emp in ns.get("matches", []):
                lines.append(f"    - {emp['name']} (ID: {emp['id']}) | Dept: {emp['department']} | Salary: {format_currency(emp['salary'])}")
            lines.append("")

        # ID search
        if "id_search" in sample_results:
            ids = sample_results["id_search"]
            target_id = ids.get("target_id")
            emp = ids.get("result")
            lines.append(f"[B] Search by ID: {target_id}")
            if emp:
                lines.append(f"    - Found: {emp['name']} | Dept: {emp['department']} | City: {emp['city']} | Salary: {format_currency(emp['salary'])}")
            else:
                lines.append("    - No employee found.")
            lines.append("")

        # Skill search
        if "skill_search" in sample_results:
            ss = sample_results["skill_search"]
            lines.append(f"[C] Search by Skill: '{ss.get('skill')}' (Found: {len(ss.get('matches', []))})")
            for emp in ss.get("matches", []):
                lines.append(f"    - {emp['name']} ({emp['department']}) | City: {emp['city']} | Salary: {format_currency(emp['salary'])}")
            lines.append("")

        # Department filter
        if "department_filter" in sample_results:
            df = sample_results["department_filter"]
            lines.append(f"[D] Filter by Department: '{df.get('department')}' (Found: {len(df.get('matches', []))})")
            for emp in df.get("matches", []):
                lines.append(f"    - {emp['name']} | Salary: {format_currency(emp['salary'])} | City: {emp['city']}")
            lines.append("")

        # Salary filter
        if "salary_filter" in sample_results:
            sf = sample_results["salary_filter"]
            lines.append(f"[E] Filter by Salary Range: {format_currency(sf.get('min'))} - {format_currency(sf.get('max'))} (Found: {len(sf.get('matches', []))})")
            for emp in sf.get("matches", []):
                lines.append(f"    - {emp['name']:<18} | Dept: {emp['department']:<12} | Salary: {format_currency(emp['salary'])}")
            lines.append("")

        # City filter
        if "city_filter" in sample_results:
            cf = sample_results["city_filter"]
            lines.append(f"[F] Filter by City: '{cf.get('city')}' (Found: {len(cf.get('matches', []))})")
            for emp in cf.get("matches", []):
                lines.append(f"    - {emp['name']} | Dept: {emp['department']} | State: {emp['address']['state']}")
            lines.append("")

        # Project status filter
        if "project_status_filter" in sample_results:
            psf = sample_results["project_status_filter"]
            lines.append(f"[G] Filter by Project Status: '{psf.get('status')}' (Found: {len(psf.get('matches', []))})")
            for emp in psf.get("matches", []):
                proj_names = [p['title'] for p in emp.get('projects', []) if p.get('status', '').lower() == psf.get('status').lower()]
                lines.append(f"    - {emp['name']:<18} | Projects: {', '.join(proj_names)}")
            lines.append("")

    lines.append(separator)
    lines.append("                          END OF REPORT")
    lines.append(separator)

    return "\n".join(lines)

def print_and_save_report(summary, skipped=None, sample_results=None, output_path="output/summary_report.txt"):
    # Generate the formatted text
    report_text = build_report_text(summary, skipped, sample_results)

    # Print to console
    print(report_text)

    # Save to file
    folder = os.path.dirname(output_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    return report_text
