#!/usr/bin/env python3
"""Subscription Auditor - track subscriptions, renewal dates, costs, and alerts.

Security posture (mirrors other openclaw skills):
  - no network, no subprocess, no eval/exec
  - ledger/config writes are atomic (tmp file + rename)
  - all arithmetic from user-stored entries; nothing auto-discovered

Cycles and their conversions (verified by tests):
  monthly   -> yearly = cost * 12
  yearly    -> yearly = cost
  quarterly -> yearly = cost * 4
  weekly    -> yearly = cost * 52
  daily     -> yearly = cost * 365
Monthly equivalent is yearly / 12 in every case.
"""

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta

DEFAULT_STATE_DIR = os.path.expanduser("~/.openclaw/subscription-auditor")
STATE_DIR = os.environ.get("SUBSCRIPTION_AUDITOR_STATE_DIR", DEFAULT_STATE_DIR)
LEDGER_PATH = os.path.join(STATE_DIR, "ledger.json")
CONFIG_PATH = os.path.join(STATE_DIR, "config.json")

LEDGER_VERSION = 1
CYCLES = ("monthly", "yearly", "quarterly", "weekly", "daily")
CYCLE_PER_YEAR = {"monthly": 12, "yearly": 1, "quarterly": 4, "weekly": 52, "daily": 365}


def fail(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def ensure_state():
    os.makedirs(STATE_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        save_config({"remind_ahead_days": 7, "currency": "USD"})
    if not os.path.exists(LEDGER_PATH):
        save_ledger({"version": LEDGER_VERSION, "entries": {}})


def load_config():
    try:
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
    except FileNotFoundError:
        cfg = {"remind_ahead_days": 7, "currency": "USD"}
    except (json.JSONDecodeError, OSError) as e:
        fail(f"config unreadable: {e}")
    cfg.setdefault("remind_ahead_days", 7)
    cfg.setdefault("currency", "USD")
    if not isinstance(cfg["remind_ahead_days"], int) or cfg["remind_ahead_days"] < 1:
        fail("config: remind_ahead_days must be a positive integer")
    if not isinstance(cfg["currency"], str) or not cfg["currency"]:
        fail("config: currency must be a non-empty string")
    return cfg


def save_config(cfg):
    tmp = CONFIG_PATH + ".tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(cfg, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, CONFIG_PATH)
    except OSError as e:
        fail(f"could not write config: {e}")


def load_ledger():
    try:
        with open(LEDGER_PATH) as f:
            raw = f.read()
    except FileNotFoundError:
        return {"version": LEDGER_VERSION, "entries": {}}
    except OSError as e:
        fail(f"ledger unreadable: {e}")
    if not raw.strip():
        # zero-byte ledger is a common crash artifact; treat like missing
        return {"version": LEDGER_VERSION, "entries": {}}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"ledger unreadable: {e}")
    if data.get("version") != LEDGER_VERSION:
        fail("ledger format unrecognized (version != 1)")
    if not isinstance(data.get("entries"), dict):
        data["entries"] = {}
    return data


def save_ledger(ledger):
    tmp = LEDGER_PATH + ".tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(ledger, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, LEDGER_PATH)
    except OSError as e:
        fail(f"could not write ledger: {e}")


def parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        fail(f"invalid date: {s} (expected YYYY-MM-DD)")


def entry_id(name):
    eid = name.strip().lower().replace(" ", "_")
    if not eid:
        fail("name must not be empty")
    return eid


def yearly_and_monthly(cost, cycle):
    per_year = cost * CYCLE_PER_YEAR[cycle]
    return per_year, per_year / 12.0


def cmd_add(args):
    ensure_state()
    cfg = load_config()
    ledger = load_ledger()
    name = args.name.strip()
    if not name:
        fail("name must not be empty")
    if args.cost is None or args.cost < 0:
        fail("--cost must be >= 0")
    cycle = args.cycle or "monthly"
    if cycle not in CYCLES:
        fail(f"cycle must be one of {', '.join(CYCLES)}")
    if args.next_renewal:
        nr = parse_date(args.next_renewal)
    else:
        nr = datetime.now().date() + timedelta(days=30)
    eid = entry_id(name)
    entry = {
        "name": name,
        "cost": args.cost,
        "cycle": cycle,
        "next_renewal": nr.isoformat(),
        "auto_renew": bool(args.auto_renew),
        "notes": args.notes or "",
        "currency": cfg["currency"],
        "added_at": datetime.now().isoformat(),
    }
    ledger["entries"][eid] = entry
    save_ledger(ledger)
    per_year, per_month = yearly_and_monthly(args.cost, cycle)
    if args.json:
        print(json.dumps({"id": eid, "entry": entry,
                          "per_year": round(per_year, 2), "per_month": round(per_month, 2)}))
    else:
        print(f"added {eid} ({entry['cost']} {entry['currency']}/{cycle}, "
              f"~{per_month:.2f}/mo, ~{per_year:.2f}/yr, renews {entry['next_renewal']})")


def cmd_list(args):
    ensure_state()
    ledger = load_ledger()
    entries = ledger["entries"]
    if args.json:
        print(json.dumps(entries, indent=2))
        return
    if not entries:
        print("(no subscriptions)")
        return
    for k, v in sorted(entries.items()):
        print(f"{k}: {v['name']} ({v['cost']} {v['currency']}/{v['cycle']}, "
              f"next={v['next_renewal']}, auto={'yes' if v['auto_renew'] else 'no'})")


def cmd_status(args):
    ensure_state()
    cfg = load_config()
    ledger = load_ledger()
    entries = ledger["entries"]
    total_monthly = 0.0
    total_yearly = 0.0
    now = datetime.now().date()
    upcoming = []
    for k, v in entries.items():
        cost = float(v.get("cost", 0))
        cycle = v.get("cycle", "monthly")
        if cycle not in CYCLE_PER_YEAR:
            fail(f"ledger entry {k}: unknown cycle {cycle}")
        per_year, per_month = yearly_and_monthly(cost, cycle)
        total_yearly += per_year
        total_monthly += per_month
        nr = parse_date(v["next_renewal"])
        days_left = (nr - now).days
        upcoming.append({"id": k, "name": v["name"], "renewal": v["next_renewal"],
                         "days_left": days_left, "cost": cost,
                         "currency": v.get("currency", cfg["currency"]),
                         "auto_renew": v.get("auto_renew", True)})
    res = {
        "count": len(entries),
        "total_monthly": round(total_monthly, 2),
        "total_yearly": round(total_yearly, 2),
        "upcoming": sorted(upcoming, key=lambda x: (x["days_left"], x["id"])),
        "currency": cfg["currency"],
    }
    if args.json:
        print(json.dumps(res, indent=2))
        return
    print(f"subs: {res['count']}, ~{res['total_monthly']} {res['currency']}/mo, "
          f"~{res['total_yearly']} {res['currency']}/yr")
    for u in res["upcoming"]:
        if u["days_left"] < 0:
            flag = f"PAST-DUE {-u['days_left']}d"
        elif u["days_left"] <= cfg["remind_ahead_days"]:
            flag = f"renews in {u['days_left']}d"
        else:
            continue
        print(f"  ⚠ {u['name']}: {flag} ({u['renewal']}, "
              f"{u['cost']} {u['currency']}, "
              f"auto={'yes' if u['auto_renew'] else 'no'})")


def cmd_remind(args):
    ensure_state()
    cfg = load_config()
    ledger = load_ledger()
    days = args.days if args.days is not None else cfg["remind_ahead_days"]
    now = datetime.now().date()
    items = []
    for k, v in ledger["entries"].items():
        nr = parse_date(v["next_renewal"])
        dl = (nr - now).days
        if dl <= days:
            items.append({"id": k, "name": v["name"], "renewal": v["next_renewal"],
                          "days_left": dl, "cost": v["cost"],
                          "currency": v.get("currency", cfg["currency"]),
                          "auto_renew": v.get("auto_renew", True)})
    items.sort(key=lambda x: (x["days_left"], x["id"]))
    if args.json:
        print(json.dumps(items, indent=2))
        return
    if not items:
        print(f"nothing renews within {days} days")
        return
    for it in items:
        if it["days_left"] < 0:
            print(f"⚠ {it['name']} PAST-DUE {-it['days_left']}d ago "
                  f"({it['renewal']}, {it['cost']} {it['currency']}, "
                  f"auto={'yes' if it['auto_renew'] else 'no'})")
        else:
            print(f"{it['name']} renews {it['renewal']} ({it['days_left']}d) "
                  f"- {it['cost']} {it['currency']} "
                  f"auto={'yes' if it['auto_renew'] else 'no'}")


def cmd_rm(args):
    ensure_state()
    ledger = load_ledger()
    sid = args.id
    if sid not in ledger["entries"]:
        fail(f"subscription not found: {sid}")
    del ledger["entries"][sid]
    save_ledger(ledger)
    if args.json:
        print(json.dumps({"removed": sid}))
    else:
        print(f"removed {sid}")


def cmd_config(args):
    ensure_state()
    cfg = load_config()
    changed = False
    if args.remind_ahead_days is not None:
        if args.remind_ahead_days < 1:
            fail("remind_ahead_days must be positive")
        cfg["remind_ahead_days"] = args.remind_ahead_days
        changed = True
    if args.currency is not None:
        if not args.currency.strip():
            fail("currency must be a non-empty string")
        cfg["currency"] = args.currency.strip()
        changed = True
    if changed:
        save_config(cfg)
        state = "set"
    else:
        state = "current"
    if args.json:
        print(json.dumps(cfg, indent=2))
    else:
        print(f"{state}: remind_ahead_days={cfg['remind_ahead_days']}, "
              f"currency={cfg['currency']}")


def build_parser():
    p = argparse.ArgumentParser(prog="subscription-auditor",
                                description="Track subscriptions and renewals. "
                                            "All data local; costs cycle-arithmetic only.")
    p.add_argument("--json", action="store_true", help="structured output")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add subscription (same name = replace)")
    a.add_argument("name")
    a.add_argument("--cost", type=float, required=True)
    a.add_argument("--cycle", choices=list(CYCLES))
    a.add_argument("--next-renewal", dest="next_renewal", help="YYYY-MM-DD (default: today+30)")
    a.add_argument("--auto-renew", dest="auto_renew", action="store_true", default=True)
    a.add_argument("--no-auto-renew", dest="auto_renew", action="store_false")
    a.add_argument("--notes")
    a.set_defaults(fn=cmd_add)

    sub.add_parser("list", help="list subscriptions").set_defaults(fn=cmd_list)
    sub.add_parser("status", help="totals + upcoming renewals").set_defaults(fn=cmd_status)

    r = sub.add_parser("remind", help="subscriptions renewing within N days")
    r.add_argument("--days", type=int)
    r.set_defaults(fn=cmd_remind)

    rm = sub.add_parser("rm", help="remove subscription")
    rm.add_argument("id")
    rm.set_defaults(fn=cmd_rm)

    c = sub.add_parser("config", help="get/set config")
    c.add_argument("--remind-ahead-days", type=int)
    c.add_argument("--currency")
    c.set_defaults(fn=cmd_config)
    return p


def main():
    args = build_parser().parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
