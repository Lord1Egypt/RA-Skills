#!/usr/bin/env python3
"""
Role Template Manager
- Load preset role templates
- List all available templates
- Get template details by ID
"""

import json
import os

def get_templates_path():
    """Get role templates file path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "../data/role_templates.json")

def load_templates():
    """Load all role templates"""
    templates_path = get_templates_path()
    with open(templates_path, "r", encoding="utf-8") as f:
        return json.load(f)["templates"]

def list_templates():
    """List all available role templates"""
    templates = load_templates()
    result = []
    for template in templates:
        result.append({
            "id": template["id"],
            "name": template["name"],
            "description": template["description"]
        })
    return result

def get_template(template_id):
    """Get template details by ID"""
    templates = load_templates()
    for template in templates:
        if template["id"] == template_id:
            return template
    return None

if __name__ == "__main__":
    # Test code
    print("All role templates:")
    for template in list_templates():
        print(f"- {template['name']}: {template['description']}")
