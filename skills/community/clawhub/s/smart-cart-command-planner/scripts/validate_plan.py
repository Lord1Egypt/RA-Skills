#!/usr/bin/env python3
"""Validate a smart-cart motion plan against the bundled schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ACTION_LIMITS = {
    "sense": ("clearance_required_cm", 20, 200),
    "move_forward": ("distance_cm", 1, 300),
    "move_backward": ("distance_cm", 1, 100),
    "strafe_left": ("distance_cm", 1, 150),
    "strafe_right": ("distance_cm", 1, 150),
    "turn_left": ("angle_deg", 1, 180),
    "turn_right": ("angle_deg", 1, 180),
    "wait": ("duration_s", 0.1, 10),
    "stop": None,
}
MOTION_ACTIONS = {
    "move_forward",
    "move_backward",
    "strafe_left",
    "strafe_right",
    "turn_left",
    "turn_right",
}


def validate(plan: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["Top level must be a JSON object."]

    status = plan.get("status")
    if status not in {"ready", "needs_confirmation", "emergency_stop"}:
        errors.append("status must be ready, needs_confirmation, or emergency_stop.")

    request = plan.get("request")
    if not isinstance(request, dict) or not request.get("original") or not request.get("normalized_goal"):
        errors.append("request must include non-empty original and normalized_goal fields.")

    if not isinstance(plan.get("assumptions"), list):
        errors.append("assumptions must be a list.")

    steps = plan.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append("steps must be a non-empty list.")
        return errors

    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            errors.append(f"step {index} must be an object.")
            continue
        if step.get("seq") != index:
            errors.append(f"step {index} must have seq={index}.")
        action = step.get("action")
        if action not in ACTION_LIMITS:
            errors.append(f"step {index} has unsupported action: {action!r}.")
            continue
        if not isinstance(step.get("reason"), str) or not step["reason"].strip():
            errors.append(f"step {index} must include a reason.")
        limit = ACTION_LIMITS[action]
        if limit:
            field, minimum, maximum = limit
            value = step.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"step {index} requires numeric {field}.")
            elif not minimum <= value <= maximum:
                errors.append(f"step {index} {field} must be between {minimum} and {maximum}.")
        if action in MOTION_ACTIONS and step.get("speed") not in {"slow", "medium"}:
            errors.append(f"step {index} speed must be slow or medium.")

    if steps[-1].get("action") != "stop":
        errors.append("The final step must be stop.")

    if status == "emergency_stop" and (len(steps) != 1 or steps[0].get("action") != "stop"):
        errors.append("An emergency_stop plan must contain exactly one stop step.")

    safety = plan.get("safety")
    if not isinstance(safety, dict):
        errors.append("safety must be an object.")
    else:
        if safety.get("final_stop") is not True:
            errors.append("safety.final_stop must be true.")
        if status != "emergency_stop" and safety.get("obstacle_check") is not True:
            errors.append("safety.obstacle_check must be true for ordinary plans.")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_plan.py PLAN.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}")
        return 1
    errors = validate(plan)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: smart-cart command plan passed all checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

