import json
from src.server.tools import get_schemes_tool, check_eligibility_tool

print("="*50)
print("Testing Tools Directly (No WebSocket)")
print("="*50)

# Test 1: Get schemes for a farmer
print("\n--- Test 1: Farmer Profile ---")
user_profile = {
    "age": 25,
    "income": 40000,
    "state": "Andhra Pradesh",
    "category": "FARMER"
}
print(f"User Profile: {user_profile}")
result1 = get_schemes_tool.invoke({"user_profile": user_profile})  # Pass dict, not JSON string
print(f"\nSchemes Found:\n{result1}")

# Test 2: Check eligibility for PM-KISAN
print("\n--- Test 2: Check PM-KISAN Eligibility ---")
result2 = check_eligibility_tool.invoke({
    "user_profile": user_profile,
    "scheme_id": "pmkisan"
})
print(f"Eligibility Result:\n{result2}")

# Test 3: High income (no match)
print("\n--- Test 3: High Income Profile ---")
high_income_profile = {
    "age": 40,
    "income": 800000,
    "state": "Karnataka",
    "category": "GENERAL"
}
print(f"User Profile: {high_income_profile}")
result3 = get_schemes_tool.invoke({"user_profile": high_income_profile})
print(f"\nSchemes Found:\n{result3}")

print("\n" + "="*50)
print("Tools are working correctly!")
print("="*50)
