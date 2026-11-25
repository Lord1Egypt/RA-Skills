#!/usr/bin/env python3
"""Deterministic task workflow advisor using only the Python standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from copy import deepcopy
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


STATE_FILE = "workflow_learning.json"
EXTERNAL_ACTIONS = ("send", "purchase", "buy", "book", "post", "submit", "order")
DEMO_REQUEST = {
    "task": {
        "type": "compare_food_quotes",
        "quotes": [
            {"vendor": "Fictional Cafe A", "subtotal": "20.00", "fees": {"delivery": "4.00", "service": "1.50"}},
            {"vendor": "Fictional Cafe B", "subtotal": "22.00", "fees": {"delivery": "1.00", "service": "0.25"}},
        ],
    },
    "available_device": "fictional Windows laptop",
    "privacy_requirement": "local processing only",
    "user_preferences": {"currency": "USD", "format": "lowest total first"},
    "data_classification": "synthetic",
}
STRICT_DEMO_REQUEST = {
    "task": {
        "type": "compare_food_quotes",
        "budget": {"operator": "under", "amount": "25.00"},
        "party_size": 2,
        "allergies": ["peanut"],
        "quotes": [
            {
                "vendor": "Synthetic Cafe A",
                "subtotal": "24.00",
                "fees": {"delivery": "3.80"},
                "tip": "1.00",
                "charges_confirmed": True,
                "serves": 2,
            },
            {
                "vendor": "Synthetic Cafe B",
                "subtotal": "22.00",
                "fees": {"service": "2.00"},
                "tip": "2.00",
                "charges_confirmed": True,
                "serves": 2,
            },
        ],
    },
    "available_device": "synthetic Windows laptop",
    "privacy_requirement": "local processing only",
    "user_preferences": {"currency": "USD", "format": "qualification decision first"},
    "data_classification": "synthetic",
}


def _compact(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _task_type(task: Any) -> str:
    if isinstance(task, dict) and isinstance(task.get("type"), str):
        return task["type"].strip().lower().replace("-", "_").replace(" ", "_")
    text = _compact(task).lower() if not isinstance(task, str) else task.lower()
    if "dictat" in text and "email" in text:
        return "dictated_notes_to_email_draft"
    if "quote" in text or "food" in text:
        return "compare_food_quotes"
    if "deadline" in text or "organize" in text:
        return "organize_tasks_by_deadline"
    return "general_task"


def _missing_core(request: dict[str, Any]) -> list[str]:
    missing = []
    for key in ("task", "available_device", "privacy_requirement", "user_preferences"):
        if key not in request or request[key] in (None, "", [], {}):
            missing.append(key)
    return missing


def _signature(request: dict[str, Any]) -> dict[str, str]:
    preferences_hash = hashlib.sha256(_compact(request.get("user_preferences")).encode()).hexdigest()[:12]
    return {
        "task_type": _task_type(request.get("task")),
        "available_device": str(request.get("available_device", "")).strip().lower(),
        "privacy_requirement": str(request.get("privacy_requirement", "")).strip().lower(),
        "preferences_hash": preferences_hash,
    }


def _load_state(state_dir: Path) -> dict[str, Any]:
    path = state_dir / STATE_FILE
    if not path.exists():
        return {"version": 1, "successful_workflows": []}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"version": 1, "successful_workflows": []}
    if not isinstance(value, dict) or not isinstance(value.get("successful_workflows"), list):
        return {"version": 1, "successful_workflows": []}
    return value


def _save_state(state_dir: Path, state: dict[str, Any]) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    target = state_dir / STATE_FILE
    temporary = target.with_suffix(".tmp")
    temporary.write_text(_compact(state) + "\n", encoding="utf-8")
    os.replace(temporary, target)


def _find_reuse(request: dict[str, Any], state: dict[str, Any]) -> dict[str, Any] | None:
    signature = _signature(request)
    for entry in reversed(state["successful_workflows"]):
        saved = entry.get("signature", {})
        if all(saved.get(key) == signature[key] for key in ("task_type", "available_device", "privacy_requirement")):
            return entry
    return None


def _base_result(request: dict[str, Any], workflow: str, rationale: str) -> dict[str, Any]:
    classification = request.get("data_classification", "unspecified")
    return {
        "status": "ready",
        "data_classification": classification,
        "recommended_workflow": workflow,
        "steps": [],
        "required_tools": [],
        "suitability_rationale": rationale,
        "missing_information": [],
        "approval_required_actions": [],
        "workflow_learning": {"reused": False, "source": None},
    }


def _email_workflow(request: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    result = _base_result(
        request,
        "Convert supplied dictated notes into a reviewable local email draft, then stop before sending.",
        "Drafting locally minimizes external disclosure and leaves the irreversible communication decision with the user.",
    )
    missing = [key for key in ("dictated_notes", "recipient") if not task.get(key)]
    tone = task.get("tone")
    preferences = request.get("user_preferences")
    if not tone and isinstance(preferences, dict):
        tone = preferences.get("tone")
    if not tone:
        missing.append("task.tone or user_preferences.tone")
    result["missing_information"] = missing
    result["required_tools"] = ["Python 3 standard library", "local text editor"]
    result["steps"] = [
        {"order": 1, "action": "Review the supplied dictated notes and recipient", "approval_required": False},
        {"order": 2, "action": "Create a subject and email draft using only supplied facts", "approval_required": False},
        {"order": 3, "action": "Have the user review and edit the draft", "approval_required": False},
        {"order": 4, "action": "Send the email only after explicit human approval", "approval_required": True},
    ]
    result["approval_required_actions"] = [
        {"action": "Send the email", "reason": "Sending is an external communication", "status": "not_executed"}
    ]
    if not missing:
        notes = re.sub(r"\s+", " ", str(task["dictated_notes"])).strip()
        result["draft"] = {
            "to": task["recipient"],
            "subject": task.get("subject") or "Draft based on supplied notes",
            "tone": tone,
            "body": notes,
            "send_status": "not_sent",
        }
    return result


def _organize_workflow(request: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    result = _base_result(
        request,
        "Validate the five supplied fictional tasks and sort them by deadline, preserving ties in input order.",
        "A deterministic local sort is fast, reproducible, and does not expose task contents to an external integration.",
    )
    tasks = task.get("tasks")
    if not isinstance(tasks, list):
        result["missing_information"].append("task.tasks (list of five tasks)")
        tasks = []
    elif len(tasks) != 5:
        result["missing_information"].append(f"task.tasks must contain exactly five items (received {len(tasks)})")
    parsed = []
    for index, item in enumerate(tasks):
        if not isinstance(item, dict) or not item.get("title") or not item.get("deadline"):
            result["missing_information"].append(f"task.tasks[{index}].title and deadline")
            continue
        try:
            deadline = datetime.fromisoformat(str(item["deadline"]).replace("Z", "+00:00"))
        except ValueError:
            result["missing_information"].append(f"task.tasks[{index}].deadline as ISO 8601")
            continue
        parsed.append((deadline, index, item))
    result["required_tools"] = ["Python 3 standard library"]
    result["steps"] = [
        {"order": 1, "action": "Validate all five supplied titles and ISO 8601 deadlines", "approval_required": False},
        {"order": 2, "action": "Sort valid tasks from earliest to latest deadline", "approval_required": False},
        {"order": 3, "action": "Present the ordered list for user review", "approval_required": False},
    ]
    if not result["missing_information"]:
        result["organized_tasks"] = [item for _, _, item in sorted(parsed, key=lambda row: (row[0], row[1]))]
    return result


def _money(value: Any) -> Decimal:
    if isinstance(value, bool):
        raise InvalidOperation
    amount = Decimal(str(value))
    if not amount.is_finite() or amount < 0:
        raise InvalidOperation
    return amount


def _budget_requirement(task: dict[str, Any], preferences: Any) -> tuple[str, Decimal] | None:
    value = task.get("budget")
    if value is None and isinstance(preferences, dict):
        value = preferences.get("budget")
    if value is None:
        return None
    if isinstance(value, dict):
        operator = str(value.get("operator", value.get("condition", ""))).strip().lower().replace(" ", "_")
        amount = value.get("amount")
    elif isinstance(value, str):
        match = re.fullmatch(r"\s*(under|below|less\s+than|at\s+most|max(?:imum)?)\s*\$?\s*([0-9]+(?:\.[0-9]+)?)\s*", value, re.I)
        if not match:
            raise ValueError("budget must be like 'under 25' or an object with operator and amount")
        operator, amount = match.group(1).lower().replace(" ", "_"), match.group(2)
    else:
        raise ValueError("budget must be a string or object")
    aliases = {"below": "under", "less_than": "under", "max": "at_most", "maximum": "at_most"}
    operator = aliases.get(operator, operator)
    if operator not in ("under", "at_most"):
        raise ValueError("budget operator must be 'under' or 'at_most'")
    if amount is None:
        raise ValueError("budget amount is required")
    return operator, _money(amount)


def _positive_int(value: Any, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a positive integer")
    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field} must be a positive integer") from error
    if number <= 0 or str(number) != str(value).strip():
        raise ValueError(f"{field} must be a positive integer")
    return number


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _quote_workflow(request: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    result = _base_result(
        request,
        "Calculate complete supplied totals, evaluate every explicit budget, party-size, and allergy requirement, then rank only with unresolved facts visible.",
        "Decimal arithmetic and explicit qualification checks avoid treating unknown charges, portions, or allergy safety as suitable.",
    )
    preferences = request.get("user_preferences")
    try:
        budget = _budget_requirement(task, preferences)
    except (InvalidOperation, ValueError) as error:
        budget = None
        result["missing_information"].append(f"task.budget: {error}")
    party_value = task.get("party_size")
    if party_value is None and isinstance(preferences, dict):
        party_value = preferences.get("party_size")
    party_size = None
    if party_value is not None:
        try:
            party_size = _positive_int(party_value, "party_size")
        except ValueError as error:
            result["missing_information"].append(str(error))
    allergy_value = task.get("allergies")
    if allergy_value is None and isinstance(preferences, dict):
        allergy_value = preferences.get("allergies")
    if allergy_value is None:
        allergies: list[str] = []
    elif isinstance(allergy_value, list) and all(isinstance(item, str) and item.strip() for item in allergy_value):
        allergies = [item.strip().lower() for item in allergy_value]
    else:
        allergies = []
        result["missing_information"].append("task.allergies or user_preferences.allergies as a list of names")
    quotes = task.get("quotes")
    if not isinstance(quotes, list) or not quotes:
        result["missing_information"].append("task.quotes (non-empty list)")
        quotes = []
    comparisons = []
    clarification_questions: list[str] = []
    for index, quote in enumerate(quotes):
        if not isinstance(quote, dict) or not quote.get("vendor"):
            result["missing_information"].append(f"task.quotes[{index}].vendor")
            continue
        vendor = str(quote["vendor"])
        if "subtotal" not in quote:
            result["missing_information"].append(f"task.quotes[{index}].subtotal")
            continue
        unresolved: list[str] = []
        disqualifying: list[str] = []
        unknown_charges = quote.get("unknown_charges", [])
        if not isinstance(unknown_charges, list):
            result["missing_information"].append(f"task.quotes[{index}].unknown_charges as a list")
            unknown_charges = ["invalid unknown_charges value"]
        unknown_charges = [str(item) for item in unknown_charges]
        fees_value = quote.get("fees")
        if not isinstance(fees_value, dict):
            unresolved.append("fees are missing or not itemized")
            result["missing_information"].append(f"task.quotes[{index}].fees as an object, including an empty object when confirmed none")
            fees_value = None
        if quote.get("charges_confirmed") is not True:
            unresolved.append("all fees, taxes, and required tips are not confirmed")
            clarification_questions.append(f"Can {vendor} confirm that all fees, taxes, and required tips are included?")
        if unknown_charges:
            unresolved.append("unknown charges: " + ", ".join(unknown_charges))
            clarification_questions.append(f"Can {vendor} confirm the amounts for these unknown charges: {', '.join(unknown_charges)}?")
        try:
            subtotal = _money(quote["subtotal"])
            fees = {name: _money(value) for name, value in fees_value.items()} if fees_value is not None else {}
            tip = _money(quote["tip"]) if "tip" in quote else Decimal("0")
        except (InvalidOperation, ValueError):
            result["missing_information"].append(f"task.quotes[{index}] non-negative numeric subtotal, fees, and tip")
            continue
        total = subtotal + sum(fees.values(), Decimal("0")) + tip if fees_value is not None else None
        if budget is not None and total is not None:
            operator, limit = budget
            within_budget = total < limit if operator == "under" else total <= limit
            if not within_budget:
                symbol = "<" if operator == "under" else "<="
                disqualifying.append(f"total {total:.2f} does not satisfy required budget {symbol} {limit:.2f}")
        serves = quote.get("serves")
        if party_size is not None:
            if serves is None:
                unresolved.append("explicit serves count is missing")
                clarification_questions.append(f"How many people does {vendor}'s quoted option explicitly serve?")
            else:
                try:
                    serves = _positive_int(serves, f"task.quotes[{index}].serves")
                except ValueError as error:
                    result["missing_information"].append(str(error))
                    unresolved.append("explicit serves count is invalid")
                else:
                    if serves < party_size:
                        disqualifying.append(f"serves {serves}, fewer than requested party size {party_size}")
                        clarification_questions.append(f"Can {vendor} provide enough portions to serve {party_size} people within the other requirements?")
        allergen_info = quote.get("allergen_information")
        cross_info = quote.get("cross_contamination_information")
        for allergy in allergies:
            allergen_status = allergen_info.get(allergy) if isinstance(allergen_info, dict) else None
            cross_status = cross_info.get(allergy) if isinstance(cross_info, dict) else None
            if allergen_status is None:
                unresolved.append(f"{allergy} allergen information is missing")
                clarification_questions.append(f"Can {vendor} provide explicit {allergy} allergen information for this option?")
            elif str(allergen_status).strip().lower() in ("contains", "may contain", "may_contain", "unsafe"):
                disqualifying.append(f"{allergy} allergen status is {allergen_status}")
            elif str(allergen_status).strip().lower() not in ("free", "allergen_free", "does_not_contain"):
                unresolved.append(f"{allergy} allergen status is unclear: {allergen_status}")
            if cross_status is None:
                unresolved.append(f"{allergy} cross-contamination information is missing")
                clarification_questions.append(f"Can {vendor} provide explicit {allergy} cross-contamination information?")
            elif str(cross_status).strip().lower() not in ("none", "none_reported", "controlled", "no_risk_reported"):
                disqualifying.append(f"{allergy} cross-contamination status is {cross_status}")
        unresolved = _unique(unresolved)
        disqualifying = _unique(disqualifying)
        comparisons.append({
            "vendor": vendor,
            "subtotal": f"{subtotal:.2f}",
            "fees": {name: f"{value:.2f}" for name, value in fees.items()},
            "tip": f"{tip:.2f}",
            "total": f"{total:.2f}" if total is not None else None,
            "charges_confirmed": quote.get("charges_confirmed") is True,
            "unknown_charges": unknown_charges,
            "serves": serves,
            "qualifies": not unresolved and not disqualifying,
            "disqualifying_reasons": disqualifying,
            "unresolved_requirements": unresolved,
        })
    result["required_tools"] = ["Python 3 standard library"]
    result["steps"] = [
        {"order": 1, "action": "Validate supplied subtotals, every fee, tip, and charge confirmation", "approval_required": False},
        {"order": 2, "action": "Apply the budget operator exactly and check explicit portions for the requested party", "approval_required": False},
        {"order": 3, "action": "Keep missing allergen and cross-contamination facts unresolved, then rank qualifying quotes", "approval_required": False},
        {"order": 4, "action": "Place an order only after explicit human approval", "approval_required": True},
    ]
    result["approval_required_actions"] = [
        {"action": "Place a food order or make a purchase", "reason": "Purchases are external and financially consequential", "status": "not_executed"}
    ]
    result["quote_comparison"] = sorted(
        comparisons,
        key=lambda quote: (quote["total"] is None, Decimal(quote["total"]) if quote["total"] is not None else Decimal("Infinity"), quote["vendor"]),
    )
    qualifying = [quote for quote in result["quote_comparison"] if quote["qualifies"]]
    has_requirements = budget is not None or party_size is not None or bool(allergies)
    if has_requirements:
        if qualifying:
            result["decision"] = "qualifying option available"
            result["recommended_option"] = qualifying[0]["vendor"]
        else:
            result["decision"] = "no qualifying option"
            if budget is not None:
                operator, limit = budget
                wording = "below" if operator == "under" else "at or below"
                clarification_questions.append(f"Can any vendor provide a fully confirmed total {wording} {limit:.2f}?")
            result["clarification_questions"] = _unique(clarification_questions)
    elif clarification_questions:
        result["clarification_questions"] = _unique(clarification_questions)
    result["missing_information"] = _unique(result["missing_information"])
    return result


def _general_workflow(request: dict[str, Any], task: Any) -> dict[str, Any]:
    result = _base_result(
        request,
        "Clarify the outcome, perform reversible local preparation, review the result, and stop before external execution.",
        "This conservative workflow works across devices while respecting the stated privacy requirement and approval boundaries.",
    )
    result["required_tools"] = ["available device", "local text editor"]
    result["steps"] = [
        {"order": 1, "action": "Confirm the desired outcome and supplied constraints", "approval_required": False},
        {"order": 2, "action": "Prepare the work locally using reversible steps", "approval_required": False},
        {"order": 3, "action": "Review the prepared result", "approval_required": False},
    ]
    text = _compact(task).lower()
    actions = sorted({verb for verb in EXTERNAL_ACTIONS if re.search(rf"\b{verb}\w*\b", text)})
    for action in actions:
        result["approval_required_actions"].append({
            "action": action,
            "reason": "External execution requires explicit human approval",
            "status": "not_executed",
        })
    return result


def recommend(request: dict[str, Any], state_dir: Path) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("input must be a JSON object")
    core_missing = _missing_core(request)
    if core_missing:
        result = _base_result(
            request,
            "Collect the missing required inputs before selecting a workflow.",
            "A reliable recommendation requires the task, device, privacy requirement, and preferences; guessing would be unsafe.",
        )
        result["status"] = "needs_information"
        result["missing_information"] = core_missing
        result["steps"] = [{"order": 1, "action": "Supply the listed missing information", "approval_required": False}]
        return result

    task = request["task"]
    kind = _task_type(task)
    task_dict = task if isinstance(task, dict) else {"description": task}
    if kind == "dictated_notes_to_email_draft":
        result = _email_workflow(request, task_dict)
    elif kind == "organize_tasks_by_deadline":
        result = _organize_workflow(request, task_dict)
    elif kind == "compare_food_quotes":
        result = _quote_workflow(request, task_dict)
    else:
        result = _general_workflow(request, task)

    if result["missing_information"]:
        result["status"] = "needs_information"

    reused = _find_reuse(request, _load_state(state_dir))
    if reused:
        result["workflow_learning"] = {
            "reused": True,
            "source": "successful local workflow for a similar task",
            "feedback_note": reused.get("feedback_note", ""),
        }
        result["recommended_workflow"] = reused["recommended_workflow"]
    return result


def record_feedback(payload: dict[str, Any], state_dir: Path) -> dict[str, Any]:
    if not isinstance(payload, dict) or not isinstance(payload.get("request"), dict):
        raise ValueError("feedback input must contain a request object")
    if payload.get("successful") is not True:
        return {"saved": False, "reason": "Only explicitly successful workflows are reused"}
    workflow = payload.get("recommended_workflow")
    if not isinstance(workflow, str) or not workflow.strip():
        raise ValueError("feedback input must contain recommended_workflow")
    state = _load_state(state_dir)
    signature = _signature(payload["request"])
    entry = {
        "signature": signature,
        "recommended_workflow": workflow.strip(),
        "feedback_note": str(payload.get("feedback_note", ""))[:200],
    }
    state["successful_workflows"] = [
        old for old in state["successful_workflows"] if old.get("signature") != signature
    ][-49:] + [entry]
    _save_state(state_dir, state)
    return {"saved": True, "workflow_learning": True, "stored_fields": sorted(entry.keys())}


def _read_json(path: str) -> dict[str, Any]:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("recommend", "feedback"):
        child = subparsers.add_parser(command)
        child.add_argument("--input", required=True, help="JSON file path, or - for stdin")
        child.add_argument("--state-dir", required=True, help="Local directory for compact workflow-learning state")
    subparsers.add_parser("demo", help="Run the built-in synthetic food-quote scenario without live integrations")
    subparsers.add_parser("demo-strict", help="Run strict budget, party-size, and allergy checks on new synthetic quotes")
    args = parser.parse_args(argv)
    try:
        if args.command in ("demo", "demo-strict"):
            demo_request = DEMO_REQUEST if args.command == "demo" else STRICT_DEMO_REQUEST
            output = recommend(deepcopy(demo_request), Path(os.devnull) / "workflow-learning-disabled")
        else:
            payload = _read_json(args.input)
            state_dir = Path(args.state_dir)
            output = recommend(payload, state_dir) if args.command == "recommend" else record_feedback(payload, state_dir)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
