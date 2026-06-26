#!/usr/bin/env python3
"""
Pre-Flight Validation Hook (Improved Version)

Validates user input for required three elements: Vendor Full Name, Solution Model, Application Scenario.
If incomplete, returns a structured questionnaire for the user rather than rejecting outright.
"""

import sys
import json
import re

def analyze_input(user_input: str) -> dict:
    result = {
        "status": "incomplete",
        "missing": [],
        "questionnaire": [],
        "fallback_query": user_input
    }
    
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', user_input))
    words = user_input.split()
    
    # Detect vendor name (Chinese: 2-10 chars; English: 1-3 capitalized words)
    if has_chinese:
        if not re.search(r'[\u4e00-\u9fff]{2,10}(公司|集团|科技|有限|股份)?', user_input):
            result["missing"].append("Vendor Full Name")
            result["questionnaire"].append("Please provide the official full name of the vendor (e.g., Framatome, Tesla).")
    else:
        if len(words) < 2 or not any(w[0].isupper() for w in words):
            result["missing"].append("Vendor Full Name")
            result["questionnaire"].append("Please provide the official full name of the vendor (e.g., Framatome, Tesla).")
    
    # Detect product/solution model
    if not re.search(r'[A-Z0-9\-]{3,}|[\u4e00-\u9fff]+(system|chip|platform|solution|product)', user_input, re.IGNORECASE):
        result["missing"].append("Solution/Product Full Model")
        result["questionnaire"].append("Please provide the specific technical solution or product full model (e.g., 'Bolt Tensioning Robot System', 'FSD Chip').")
    
    # Detect application scenario
    scene_keywords = ['scenario', 'application', 'used for', 'domain', 'nuclear', 'autonomous', 'industrial', 'medical', 'consumer']
    if not any(kw in user_input.lower() for kw in scene_keywords):
        result["missing"].append("Application Scenario")
        result["questionnaire"].append("Please specify the main application scenario (e.g., 'Nuclear Refueling Outage', 'L4 Autonomous Driving').")
    
    if not result["missing"]:
        result["status"] = "passed"
        result["questionnaire"] = []
    else:
        result["prompt_for_user"] = "To conduct precise technical research, the following information is needed:\n" + "\n".join(f"- {q}" for q in result["questionnaire"])
    
    return result

def main():
    user_query = ''
    if len(sys.argv) > 1:
        user_query = ' '.join(sys.argv[1:])
    else:
        try:
            data = json.load(sys.stdin)
            user_query = data.get('query', '')
        except:
            pass
    
    if not user_query:
        print(json.dumps({"status": "error", "message": "No research query received"}))
        sys.exit(1)
    
    analysis = analyze_input(user_query)
    print(json.dumps(analysis, ensure_ascii=False))
    sys.exit(0 if analysis["status"] == "passed" else 1)

if __name__ == '__main__':
    main()
