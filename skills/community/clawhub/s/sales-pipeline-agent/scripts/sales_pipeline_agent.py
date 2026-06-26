#!/usr/bin/env python3
"""Sales Pipeline Agent — manages leads and deals through the full sales lifecycle."""

import json
import sys
import uuid
from datetime import datetime, date, timedelta
from pathlib import Path

DB_PATH = Path.home() / ".openclaw" / "workspace" / "sales-pipeline-agent" / "pipeline.json"

STAGES = ["prospecting", "qualified", "proposal", "negotiation", "closed_won", "closed_lost", "on_hold"]
STAGE_WEIGHTS = {"prospecting": 0.05, "qualified": 0.20, "proposal": 0.40, "negotiation": 0.70, "closed_won": 1.0, "closed_lost": 0.0, "on_hold": 0.10}


def load_db() -> dict:
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        return {"deals": {}}
    with open(DB_PATH) as f:
        return json.load(f)


def save_db(db: dict) -> None:
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2, default=str)


def add_deal(name: str, company: str, contact_name: str, contact_email: str = "",
             stage: str = "prospecting", value: float = 0, close_date: str = "", source: str = "", notes: str = "") -> dict:
    """Add a new deal."""
    db = load_db()
    deal_id = uuid.uuid4().hex[:8]

    deal = {
        "id": deal_id,
        "name": name,
        "company": company,
        "contact_name": contact_name,
        "contact_email": contact_email,
        "stage": stage,
        "probability": STAGE_WEIGHTS.get(stage, 0.05),
        "value": value,
        "weighted_value": value * STAGE_WEIGHTS.get(stage, 0.05),
        "close_date": close_date,
        "source": source,
        "notes": notes,
        "created_at": date.today().isoformat(),
        "updated_at": date.today().isoformat(),
        "activities": [],
    }

    db["deals"][deal_id] = deal
    save_db(db)
    return deal


def list_deals(stage: str = "", min_value: float = 0) -> list[dict]:
    """List deals with optional filters."""
    db = load_db()
    deals = list(db["deals"].values())

    if stage:
        deals = [d for d in deals if d.get("stage") == stage]
    if min_value > 0:
        deals = [d for d in deals if d.get("value", 0) >= min_value]

    return sorted(deals, key=lambda d: d.get("value", 0), reverse=True)


def get_deal(deal_id: str) -> dict:
    """Get a specific deal."""
    db = load_db()
    if deal_id not in db["deals"]:
        return {"error": f"Deal {deal_id} not found"}

    d = db["deals"][deal_id]
    if d.get("close_date"):
        try:
            close = date.fromisoformat(d["close_date"])
            d["days_to_close"] = (close - date.today()).days
        except:
            pass
    return d


def update_deal(deal_id: str, **updates) -> dict:
    """Update a deal."""
    db = load_db()
    if deal_id not in db["deals"]:
        return {"error": f"Deal {deal_id} not found"}

    d = db["deals"][deal_id]
    d.update(updates)
    d["updated_at"] = date.today().isoformat()

    if "stage" in updates:
        d["probability"] = STAGE_WEIGHTS.get(updates["stage"], 0.05)
        d["weighted_value"] = d.get("value", 0) * d["probability"]

    save_db(db)
    return d


def delete_deal(deal_id: str) -> dict:
    """Delete a deal."""
    db = load_db()
    if deal_id not in db["deals"]:
        return {"error": f"Deal {deal_id} not found"}

    db["deals"].pop(deal_id)
    save_db(db)
    return {"deleted": deal_id}


def pipeline_summary() -> dict:
    """Get pipeline overview."""
    db = load_db()
    deals = list(db["deals"].values())
    today = date.today()

    by_stage = {}
    for stage in STAGES:
        stage_deals = [d for d in deals if d.get("stage") == stage]
        by_stage[stage] = {
            "count": len(stage_deals),
            "value": sum(d.get("value", 0) for d in stage_deals),
            "weighted": sum(d.get("weighted_value", 0) for d in stage_deals),
        }

    return {
        "total_deals": len(deals),
        "total_value": sum(d.get("value", 0) for d in deals),
        "weighted_forecast": sum(d.get("weighted_value", 0) for d in deals),
        "by_stage": by_stage,
    }


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "add":
        if len(args) < 3:
            print("Usage: add <name> <company> <contact> [email] [stage] [value] [close_date]")
            return
        result = add_deal(
            name=args[0],
            company=args[1],
            contact_name=args[2],
            contact_email=args[3] if len(args) > 3 and "@" in args[3] else "",
            stage=args[4] if len(args) > 4 and args[4] in STAGES else "prospecting",
            value=float(args[5]) if len(args) > 5 else 0,
            close_date=args[6] if len(args) > 6 else ""
        )
        print(json.dumps(result, indent=2, default=str))

    elif command == "list":
        stage = args[0] if args and args[0] in STAGES else ""
        deals = list_deals(stage)
        print(json.dumps(deals, indent=2, default=str))

    elif command == "get":
        if not args:
            print("Usage: get <deal_id>")
            return
        result = get_deal(args[0])
        print(json.dumps(result, indent=2, default=str))

    elif command == "update":
        if len(args) < 2:
            print("Usage: update <deal_id> <key=value> [key=value]...")
            return
        deal_id = args[0]
        updates = {}
        for arg in args[1:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                try:
                    updates[k] = float(v) if k == "value" else v
                except:
                    updates[k] = v
        result = update_deal(deal_id, **updates)
        print(json.dumps(result, indent=2, default=str))

    elif command == "delete":
        if not args:
            print("Usage: delete <deal_id>")
            return
        result = delete_deal(args[0])
        print(json.dumps(result, indent=2, default=str))

    elif command == "summary":
        summary = pipeline_summary()
        print(json.dumps(summary, indent=2, default=str))

    elif command == "status":
        summary = pipeline_summary()
        print("Sales Pipeline Status:")
        print(f"  Total Deals: {summary['total_deals']}")
        print(f"  Total Value: ${summary['total_value']:,.2f}")
        print(f"  Weighted Forecast: ${summary['weighted_forecast']:,.2f}")
        print("\nBy Stage:")
        for stage, data in summary["by_stage"].items():
            if data["count"] > 0:
                print(f"  {stage}: {data['count']} deal(s) - ${data['value']:,.2f} (weighted: ${data['weighted']:,.2f})")

    else:
        print(f"Unknown command: {command}")
        print_help()


def print_help():
    print("""Sales Pipeline Agent

Commands:
  add <name> <company> <contact> [email] [stage] [value] [close_date]
  list [stage]
  get <id>
  update <id> <key=value> [key=value]...
  delete <id>
  summary
  status

Stages: prospecting, qualified, proposal, negotiation, closed_won, closed_lost, on_hold

Example:
  sales_pipeline_agent.py add "Acme Deal" "Acme Corp" "John Doe" john@acme.com proposal 50000 2026-06-30
  sales_pipeline_agent.py list
  sales_pipeline_agent.py status
  sales_pipeline_agent.py update <id> stage=negotiation
""")


if __name__ == "__main__":
    main()
