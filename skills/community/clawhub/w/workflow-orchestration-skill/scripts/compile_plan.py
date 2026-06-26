#!/usr/bin/env python3
"""Workflow plan compiler — generates Plan IR from business goal + skills manifest."""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path


def compile_plan(business_goal: str, skills_manifest: list, constraints: dict = None) -> dict:
    """
    Placeholder: In production, this would be called by the LLM with
    the planning logic. This script validates the input and returns
    a plan structure for the LLM to populate.
    """
    plan_id = f"plan_{hashlib.md5(business_goal.encode()).hexdigest()[:8]}_{datetime.now().strftime('%Y%m%d')}"
    
    result = {
        "plan_id": plan_id,
        "business_goal": business_goal,
        "available_skills": [s["skill_name"] for s in skills_manifest],
        "constraints": constraints or {"max_nodes": 20, "max_depth": 5, "max_parallelism": 4},
        "plan_ir": None,  # LLM fills this
        "compiled_at": datetime.now().isoformat()
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="Compile business goal to Plan IR")
    parser.add_argument("--goal", required=True, help="Business goal description")
    parser.add_argument("--manifest", required=True, help="Skills manifest JSON file")
    parser.add_argument("--output", default="plan.json", help="Output plan file")
    parser.add_argument("--max-nodes", type=int, default=20)
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--max-parallel", type=int, default=4)
    args = parser.parse_args()

    with open(args.manifest) as f:
        raw = json.load(f)
    # Handle both flat array and nested {available_skills_manifest: [...]}
    manifest = raw if isinstance(raw, list) else raw.get("available_skills_manifest", raw.get("skills_manifest", []))

    constraints = {
        "max_nodes": args.max_nodes,
        "max_depth": args.max_depth,
        "max_parallelism": args.max_parallel
    }

    plan = compile_plan(args.goal, manifest, constraints)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print(f"Plan template written to {args.output}")
    print(f"Plan ID: {plan['plan_id']}")
    print(f"Available skills: {plan['available_skills']}")
    print("NOTE: plan_ir is empty — LLM should populate it based on the business goal.")


if __name__ == "__main__":
    main()
