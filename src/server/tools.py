from typing import List, Dict, Any
import json
import os
from langchain_core.tools import tool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMES_PATH = os.path.join(BASE_DIR, "schemes.json")


def _load_schemes() -> List[Dict[str, Any]]:
    with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _match_scheme(user_profile: Dict[str, Any], scheme: Dict[str, Any]) -> bool:
    age = user_profile.get("age")
    income = user_profile.get("income")
    state = user_profile.get("state")
    category = user_profile.get("category")

    # Age check
    if age is not None:
        if "min_age" in scheme and age < scheme["min_age"]:
            return False
        if "max_age" in scheme and age > scheme["max_age"]:
            return False

    # Income check
    if income is not None and "income_max" in scheme:
        if income > scheme["income_max"]:
            return False

    # State check
    if state is not None and scheme.get("state") not in ("ALL", state):
        return False

    # Category check (e.g., BPL, FARMER, WOMAN, STUDENT)
    if category is not None and scheme.get("category") not in (None, "ALL", category):
        return False

    return True


@tool
def get_schemes_tool(user_profile: Dict[str, Any]) -> str:
    """
    Given a user profile (age, income, state, category, occupation, etc.),
    return a short list of matching government welfare schemes.
    """
    schemes = _load_schemes()
    matched = [s for s in schemes if _match_scheme(user_profile, s)]

    if not matched:
        return "No schemes found for the given details. Ask the user to confirm or adjust their information."

    lines = []
    for s in matched[:5]:
        lines.append(
            f"- ID: {s.get('id')}, Name: {s.get('name')}, "
            f"Description: {s.get('description')}, Apply: {s.get('apply_url')}"
        )
    return "\n".join(lines)


@tool
def check_eligibility_tool(user_profile: Dict[str, Any], scheme_id: str) -> str:
    """
    Check if the user is eligible for a specific scheme_id based on schemes.json rules.
    Returns 'eligible' or 'not eligible' with a brief reason.
    """
    schemes = _load_schemes()
    scheme = next((s for s in schemes if s.get("id") == scheme_id), None)

    if scheme is None:
        return f"Scheme with id '{scheme_id}' not found."

    if _match_scheme(user_profile, scheme):
        return f"The user IS eligible for {scheme.get('name')} because their details satisfy the scheme rules."
    else:
        return f"The user is NOT eligible for {scheme.get('name')} based on the current age/income/state/category."


TOOLS = [get_schemes_tool, check_eligibility_tool]
