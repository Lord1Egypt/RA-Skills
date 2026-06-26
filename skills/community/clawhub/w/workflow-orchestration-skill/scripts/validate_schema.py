#!/usr/bin/env python3
"""Validate Plan IR against output_schema.json."""

import argparse
import json
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent.parent / "assets" / "output_schema.json"


def validate_schema(plan_path: str, schema_path: str = None) -> dict:
    """Validate plan JSON against schema."""
    schema_file = schema_path or SCHEMA_PATH
    
    try:
        import jsonschema
    except ImportError:
        print("WARN: jsonschema not installed, doing basic validation")
        return _basic_validate(plan_path)

    with open(plan_path) as f:
        plan = json.load(f)
    
    with open(schema_file) as f:
        schema = json.load(f)

    errors = []
    try:
        jsonschema.validate(plan, schema)
    except jsonschema.ValidationError as e:
        errors.append(str(e.message))

    return {
        "schema_valid": len(errors) == 0,
        "errors": errors
    }


def _basic_validate(plan_path: str) -> dict:
    """Fallback: basic structural validation without jsonschema."""
    with open(plan_path) as f:
        plan = json.load(f)

    errors = []
    required_top = ["plan_id", "plan_ir", "validation_report"]
    for key in required_top:
        if key not in plan:
            errors.append(f"Missing required field: {key}")

    plan_ir = plan.get("plan_ir", {})
    for key in ["nodes", "edges", "entry_nodes", "exit_nodes"]:
        if key not in plan_ir:
            errors.append(f"Missing plan_ir field: {key}")

    for node in plan_ir.get("nodes", []):
        for key in ["node_id", "target_skill", "purpose", "scoped_state_keys"]:
            if key not in node:
                errors.append(f"Node {node.get('node_id', '?')}: missing {key}")

    for edge in plan_ir.get("edges", []):
        for key in ["from_node", "to_node"]:
            if key not in edge:
                errors.append(f"Edge: missing {key}")

    return {
        "schema_valid": len(errors) == 0,
        "errors": errors
    }


def main():
    parser = argparse.ArgumentParser(description="Validate Plan IR schema")
    parser.add_argument("--plan", required=True, help="Plan JSON file")
    parser.add_argument("--schema", help="Schema JSON file (default: assets/output_schema.json)")
    args = parser.parse_args()

    result = validate_schema(args.plan, args.schema)
    
    if result["schema_valid"]:
        print("✅ Schema validation passed")
    else:
        print(f"❌ Schema validation failed ({len(result['errors'])} errors)")
        for err in result["errors"]:
            print(f"  - {err}")

    with open(args.plan) as f:
        plan = json.load(f)
    
    if "validation_report" not in plan:
        plan["validation_report"] = {}
    plan["validation_report"]["schema_valid"] = result["schema_valid"]
    plan["validation_report"]["errors"] = result["errors"]
    
    with open(args.plan, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    sys.exit(0 if result["schema_valid"] else 1)


if __name__ == "__main__":
    main()
