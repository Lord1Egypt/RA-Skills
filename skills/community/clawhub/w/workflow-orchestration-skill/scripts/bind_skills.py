#!/usr/bin/env python3
"""Validate that all target_skills in the plan exist in the skills manifest."""

import argparse
import json
import sys
from pathlib import Path


def bind_skills(plan_path: str, manifest_path: str) -> dict:
    """Validate skill bindings."""
    with open(plan_path) as f:
        plan = json.load(f)
    
    with open(manifest_path) as f:
        raw = json.load(f)
    # Handle both flat array and nested formats
    manifest = raw if isinstance(raw, list) else raw.get("available_skills_manifest", raw.get("skills_manifest", []))

    plan_ir = plan.get("plan_ir", {})
    nodes = plan_ir.get("nodes", [])
    
    # Build allowed skills set
    allowed_skills = set()
    skill_details = {}
    for s in manifest:
        name = s.get("skill_name")
        if name:
            allowed_skills.add(name)
            skill_details[name] = s

    errors = []
    used_skills = set()

    for node in nodes:
        target = node.get("target_skill", "")
        used_skills.add(target)
        if target not in allowed_skills:
            errors.append(f"Node {node['node_id']}: skill '{target}' not in allowed skills manifest")

    return {
        "skills_bound": len(errors) == 0,
        "used_skills": sorted(used_skills),
        "allowed_skills": sorted(allowed_skills),
        "errors": errors
    }


def main():
    parser = argparse.ArgumentParser(description="Validate skill bindings")
    parser.add_argument("--plan", required=True, help="Plan JSON file")
    parser.add_argument("--manifest", required=True, help="Skills manifest JSON file")
    args = parser.parse_args()

    result = bind_skills(args.plan, args.manifest)

    if result["skills_bound"]:
        print(f"✅ Skills bound: {result['used_skills']}")
    else:
        print(f"❌ Skills binding failed ({len(result['errors'])} errors)")
        for err in result["errors"]:
            print(f"  - {err}")

    with open(args.plan) as f:
        plan = json.load(f)
    
    if "validation_report" not in plan:
        plan["validation_report"] = {}
    plan["validation_report"]["skills_bound"] = result["skills_bound"]
    plan["validation_report"].setdefault("errors", []).extend(result["errors"])
    
    with open(args.plan, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    sys.exit(0 if result["skills_bound"] else 1)


if __name__ == "__main__":
    main()
