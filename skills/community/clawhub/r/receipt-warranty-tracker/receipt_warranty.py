#!/usr/bin/env python3
"""receipt-warranty-tracker: OpenClaw personal-admin skill.

Stores receipts you photograph, keeps item/price/warranty-end, and reminds
you before coverage lapses. No personal data leaves local disk.

Security posture (mirrors jerithchain skill):
  - no network, no subprocess, no eval/exec
  - ledger writes are atomic (tmp file + rename)
  - timestamps from the host clock only
"""

import argparse
import json
import os
import sys
import tempfile
import time
from datetime import date

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.environ.get("RECEIPT_WARRANTY_STATE_DIR",
                           os.path.expanduser("~/.openclaw/receipt-warranty-tracker"))
LEDGER_PATH = os.path.join(STATE_DIR, "ledger.json")
LOCK_PATH = os.path.join(STATE_DIR, "lock")

LEDGER_VERSION = 1
# how many days ahead we start reminding (configurable via config.json)
DEFAULT_REMIND_AHEAD_DAYS = 3


def _fail(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def _state_dir():
    os.makedirs(STATE_DIR, exist_ok=True)
    return STATE_DIR


def load_config():
    cfg = {"remind_ahead_days": DEFAULT_REMIND_AHEAD_DAYS}
    try:
        with open(os.path.join(STATE_DIR, "config.json")) as f:
            cfg.update(json.load(f))
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, OSError) as e:
        _fail(f"config unreadable at {STATE_DIR}/config.json: {e}")
    if not isinstance(cfg.get("remind_ahead_days"), int) or cfg["remind_ahead_days"] < 0:
        _fail("config: remind_ahead_days must be a non-negative integer")
    return cfg


def load_ledger():
    try:
        with open(LEDGER_PATH) as f:
            ledger = json.load(f)
    except FileNotFoundError:
        return {"version": LEDGER_VERSION, "entries": {}}
    except (json.JSONDecodeError, OSError) as e:
        _fail(f"ledger unreadable at {LEDGER_PATH}: {e}")
    if ledger.get("version") != LEDGER_VERSION or not isinstance(ledger.get("entries"), dict):
        _fail(f"ledger format unrecognized at {LEDGER_PATH}")
    return ledger


def save_ledger(ledger):
    _state_dir()
    fd, tmp = tempfile.mkstemp(dir=STATE_DIR, prefix=".ledger-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(ledger, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, LEDGER_PATH)
    except OSError as e:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        _fail(f"could not write ledger: {e}")


def now_iso(ts):
    """Stamp a time value for display.

    Accepts either a Unix epoch (int/float) or an ISO date string; the
    warranty-until field passes ISO strings, so both forms are handled.
    """
    if isinstance(ts, str):
        ts = time.mktime(time.strptime(ts, "%Y-%m-%d"))
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


# ---------------------------------------------------------------- commands

def cmd_add(args):
    if not args.receipt or not args.receipt.strip():
        _fail("receipt text is required (the item description you photographed)")  # noqa: E501
    if not args.item or not args.item.strip():
        _fail("item is required")
    if args.price is not None and args.price < 0:
        _fail("--price must be >= 0")
    if args.warranty_days is not None and args.warranty_days < 0:
        _fail("--warranty-days must be >= 0")
    if args.warranty_until is not None:
        try:
            date.fromisoformat(args.warranty_until)
        except ValueError:
            _fail(f"--warranty-until '{args.warranty_until}' is not a valid date (YYYY-MM-DD)")

    now = time.time()
    entry = {
        "item": args.item.strip(),
        "receipt": args.receipt.strip(),
        "price": args.price if args.price is not None else 0,
        "currency": args.currency,
        "warranty_days": args.warranty_days if args.warranty_days is not None else 0,
        "warranty_until": args.warranty_until,
        "added_at": now,
        "reminded": False,
    }
    ledger = load_ledger()
    # replace an existing entry for the same item (idempotent add)
    ledger["entries"][args.item.strip()] = entry
    save_ledger(ledger)

    until = entry["warranty_until"]
    when = now_iso(until) if until else "no warranty window"
    _remind = None
    if args.days_before and until:
        _remind = time.mktime(time.strptime(until, "%Y-%m-%d")) - args.days_before * 86400
    out = {
        "item": entry["item"],
        "price": entry["price"],
        "warranty_days": entry["warranty_days"],
        "warranty_until": until,
        "reminds_at": _remind and now_iso(_remind) or None,
        "state": "ok",
    }
    print(json.dumps(out) if args.json else
          f"stored: {entry['item']} ({entry['price']}{entry['currency'] or ''} money, "
          f"warranty until {when})")


def cmd_estimate(args):
    """Estimate warranty end from warranty duration + date (no receipt text)."""
    if not args.date:
        _fail("use --date YYYY-MM-DD to anchor the estimate")
    try:
        from datetime import date, timedelta
        d = date.fromisoformat(args.date)
    except ValueError:
        _fail(f"--date '{args.date}' is not a valid date (use YYYY-MM-DD)")
    days = args.days
    if args.weeks is not None:
        days = args.weeks * 7
    if days is None or days <= 0:
        _fail("--days or --weeks must be provided and positive")
    end = d + timedelta(days=days)
    out = {
        "date": args.date,
        "days": days,
        "warranty_until": end.isoformat(),
        "days_remaining": (end - date.today()).days,
    }
    print(json.dumps(out) if args.json else
          f"firmware/model note: coverage ends {end.isoformat()} "
          f"({out['days_remaining']} days from {args.date})")


def cmd_status(args):
    ledger = load_ledger()
    now = time.time()
    rows = []
    rem = args.days_before or load_config()["remind_ahead_days"]
    for item, e in sorted(ledger["entries"].items(), key=lambda kv: kv[1]["added_at"]):
        until = e.get("warranty_until")
        if until:
            try:
                from datetime import date
                ue = date.fromisoformat(until)
                days_left = (ue - date.today()).days
            except ValueError:
                days_left = None
        else:
            days_left = None
        reminder_due = bool(until) and days_left is not None and days_left <= rem
        if days_left is not None and days_left < 0:
            state = "EXPIRED"
        elif reminder_due:
            state = "REMIND"
        elif until:
            state = "ok"
        else:
            state = "no-warranty"
        rows.append({
            "item": item, "price": e["price"],
            "warranty_until": until, "days_left": days_left,
            "state": state, "added_at": e["added_at"],
            "reminded": e["reminded"],
        })
    if args.json:
        print(json.dumps({"updated_at": now_iso(now), "entries": rows}))
    elif not rows:
        print("(ledger empty)")
    else:
        print(f"updated_at: {now_iso(now)}")
        for r in rows:
            print(f"{r['item']:<40} {r['price']:>10}{r['price'] and ' ' or ''} "
                  f"warranty {r['warranty_until'] or 'n/a':<12} "
                  f"(days left {r['days_left'] or 'n/a':>5}) {r['state']}")


def cmd_remind(args):
    ledger = load_ledger()
    now = time.time()
    due = []
    for item, e in ledger["entries"].items():
        until = e.get("warranty_until")
        if not until:
            continue
        try:
            from datetime import date
            days_left = (date.fromisoformat(until) - date.today()).days
        except ValueError:
            continue
        if days_left <= (args.days_before or load_config()["remind_ahead_days"]) and not e.get("reminded"):
            e["reminded"] = True
            due.append({"item": item, "warranty_until": until, "days_left": days_left})
    if due:
        save_ledger(ledger)
    if args.json:
        print(json.dumps({"reminded": due, "count": len(due)}))
    else:
        if due:
            print(f"reminder(s) for today ({date.today().isoformat()}):")
            for d in due:
                print(f"  {d['item']}: coverage ends {d['warranty_until']} ({d['days_left']} days left)")
        else:
            print("nothing to remind — all tracked coverage end in more than the "
                  f"{args.days_before or load_config()['remind_ahead_days']} days, "
                  "or already past")


def cmd_list(args):
    ledger = load_ledger()
    if args.json:
        print(json.dumps(sorted(ledger["entries"].items(), key=lambda kv: kv[1]["added_at"])))
    elif not ledger["entries"]:
        print("(ledger empty)")
    else:
        for item, e in sorted(ledger["entries"].items(), key=lambda kv: kv[1]["added_at"]):
            print(f"{item}\t{e['price']}{e.get('currency', '')}\t{e['warranty_days']}d\t{e.get('warranty_until', 'n/a')}")


def cmd_rm(args):
    ledger = load_ledger()
    if args.item not in ledger["entries"]:
        _fail(f"item not in ledger: {args.item}")
    del ledger["entries"][args.item]
    save_ledger(ledger)
    print(json.dumps({"removed": args.item}) if args.json else f"removed {args.item}")


# ---------------------------------------------------------------- argparse

def build_parser():
    p = argparse.ArgumentParser(prog="receipt_warranty", description=__doc__)
    p.add_argument("--json", action="store_true", help="structured output")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="store a receipt with item/price/warranty window")
    a.add_argument("--item", required=True)
    a.add_argument("--receipt", default="")
    a.add_argument("--price", type=float, default=None)
    a.add_argument("--currency", default="USD")
    a.add_argument("--warranty-days", type=int, default=None,
                   help="coverage length from purchase in days (or use --warranty-until)")
    a.add_argument("--warranty-until", default=None, help="explicit warranty end YYYY-MM-DD")
    a.add_argument("--days-before", type=int, default=3,
                   help="how many days ahead reminders should fire")
    a.set_defaults(fn=cmd_add)

    se = sub.add_parser("estimate", help="estimate warranty end from days + anchor date")
    se.add_argument("--date", required=True, help="anchor YYYY-MM-DD")
    se.add_argument("--days", type=int, default=None, help="duration in days")
    se.add_argument("--weeks", type=int, default=None, help="duration in whole weeks")
    se.set_defaults(fn=cmd_estimate)

    sub.add_parser("list", help="list stored entries (item, price, warranty days)").set_defaults(fn=cmd_list)

    s = sub.add_parser("status", help="per-entry expiry state + reminders overview")
    s.add_argument("--days-before", type=int, default=None)
    s.set_defaults(fn=cmd_status)

    r = sub.add_parser("remind", help="mark today's reminders, save reminded flags")
    r.add_argument("--days-before", type=int, default=None)
    r.set_defaults(fn=cmd_remind)

    rm = sub.add_parser("rm", help="delete an item")
    rm.add_argument("item")
    rm.set_defaults(fn=cmd_rm)

    cs = sub.add_parser("config", help="show/set config")
    cs.add_argument("--remind-ahead-days", type=int, default=None)
    cs.set_defaults(fn=cmd_show_config, set_fn=cmd_set_config)
    return p


def cmd_show_config(args):
    print(json.dumps(load_config()) if args.json else
          f"remind_ahead_days: {load_config()['remind_ahead_days']}")


def cmd_set_config(args):
    if args.remind_ahead_days is not None:
        if args.remind_ahead_days < 0:
            _fail("remind_ahead_days must be >= 0")
        _state_dir()
        cfg = load_config()
        cfg["remind_ahead_days"] = args.remind_ahead_days
        tmp = os.path.join(STATE_DIR, "config.json.tmp")
        with open(tmp, "w") as f:
            json.dump(cfg, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, os.path.join(STATE_DIR, "config.json"))
    print(json.dumps(load_config()) if args.json else
          f"remind_ahead_days: {load_config()['remind_ahead_days']}")


def main(argv=None):
    args = build_parser().parse_args(argv)
    if getattr(args, "set_fn", None) is not None:
        args.set_fn(args)
    else:
        args.fn(args)


if __name__ == "__main__":
    main()
