"""Read and search fictional employee records without a model or MCP server."""

import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent / "data" / "employees.json"


def _load_employees() -> list[dict]:
    """Load records relative to this module, independent of the working directory."""
    with DATA_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def search_employees(query: str) -> dict:
    """Search fictional employees by name, department, or title.

    Match a case-insensitive substring and return up to five summaries.
    Use an employee ID from these results to retrieve skills with get_employee.
    """
    query = query.strip().casefold()
    if not 1 <= len(query) <= 100:
        raise ValueError("query must contain 1 to 100 characters")

    matches = [
        {key: employee[key] for key in ("id", "name", "department", "title")}
        for employee in _load_employees()
        if query in " ".join(
            employee[key] for key in ("name", "department", "title")
        ).casefold()
    ]
    return {
        "source": "fictional-demo",
        "count": len(matches[:5]),
        "has_more": len(matches) > 5,
        "employees": matches[:5],
    }


def get_employee(employee_id: str) -> dict:
    """Return a full fictional employee record for an exact ID, or found=False."""
    employee_id = employee_id.strip().upper()
    if not 1 <= len(employee_id) <= 20:
        raise ValueError("employee_id must contain 1 to 20 characters")

    employee = next(
        (person for person in _load_employees() if person["id"] == employee_id),
        None,
    )
    return {
        "source": "fictional-demo",
        "found": employee is not None,
        "employee": employee,
    }
