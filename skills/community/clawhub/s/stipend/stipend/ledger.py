"""Ledger, P&L and runway — the part that makes an agent self-aware about money.

Every other agent wallet tracks transactions. None of them answer the question
that actually matters to the person paying the bills:

    "Is this agent worth running?"

That needs earnings and costs in the same place, categorised, over time. It is
deliberately small and boring — an append-only JSONL file and some arithmetic —
because the value is in asking the question at all, not in the machinery.

Also home to the **known-destinations** record, which powers a security control
that falls out of having a ledger: the first payment to an address you have
never paid before requires confirmation, whatever the amount. Caps alone don't
stop a drain by many small payments; an attacker's address is always new.

That trust expires. An address you have not paid in months is confirmed again
before it is used, so the trusted list does not grow forever.
"""

import json
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from .config import CONFIG_DIR, ensure_dirs, load_config

LEDGER_FILE = CONFIG_DIR / "ledger.jsonl"
DESTINATIONS_FILE = CONFIG_DIR / "known-destinations.json"

# Anything not matched keeps its own name — better a long tail than a wrong bucket.
CATEGORIES = ("inference", "api", "data", "storage", "service", "earnings", "other")


# ---------------------------------------------------------------------------
# Recording
# ---------------------------------------------------------------------------

def _append(entry):
    ensure_dirs()
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    try:
        os.chmod(LEDGER_FILE, 0o600)
    except (OSError, NotImplementedError):
        pass


def record_spend(amount_usdc, to_address, category="other", note=None, tx=None):
    """Money out."""
    _append({
        "at": datetime.now(timezone.utc).isoformat(),
        "direction": "out",
        "amount_usdc": round(float(amount_usdc), 6),
        "counterparty": to_address,
        "category": category if category in CATEGORIES else "other",
        "note": note,
        "tx": tx,
    })
    remember_destination(to_address)


def record_cost(amount_usd, category="inference", note=None, tokens=None):
    """A cost that never touched the chain — tokens, an API bill, a server.

    Most of what an agent really spends is inference, and none of it is on
    Base. Without this the P&L reads "spent $0.00" to somebody who spent forty
    dollars on tokens yesterday, which makes the one number they paid to see
    wrong by omission rather than by arithmetic.

    Recorded in the same column as everything else. USDC is a dollar
    stablecoin, so a dollar of inference and a dollar of USDC belong together
    in a total that is meant to answer "what did this agent cost me".

    counterparty and tx stay null, and the entry is marked so nothing
    downstream tries to look it up on a chain it was never on. It also does not
    remember a destination: there is nobody here to pay again.
    """
    _append({
        "at": datetime.now(timezone.utc).isoformat(),
        "direction": "out",
        "amount_usdc": round(float(amount_usd), 6),
        "counterparty": None,
        "category": category if category in CATEGORIES else "other",
        "note": note,
        "tx": None,
        "offchain": True,
        # Kept even when a rate converted it to dollars: the token count is the
        # fact, the dollar figure is an interpretation of it. If the rate later
        # turns out to be wrong, the tokens are still right.
        "tokens": int(tokens) if tokens else None,
    })


def record_earning(amount_usdc, from_address=None, category="earnings", note=None, tx=None):
    """Money in. Without this there is no P&L, only a spending report."""
    _append({
        "at": datetime.now(timezone.utc).isoformat(),
        "direction": "in",
        "amount_usdc": round(float(amount_usdc), 6),
        "counterparty": from_address,
        "category": category,
        "note": note,
        "tx": tx,
    })


def sync_earnings(cfg=None, lookback_blocks=200000):
    """Record money that arrived while nobody was watching.

    Until this existed, being paid was something an agent had to notice and
    write down itself. It was never running at the moment the money landed, so
    the honest state of the ledger was "whatever anyone remembered".

    Deduplicated on (tx, log_index), not on the transaction alone: one
    transaction can carry two transfers to the same address, and dropping the
    second is a silent undercount of what you earned.

    Returns the entries it added, newest last.
    """
    import json as _json
    from . import chain, keystore
    from .config import EARNINGS_CURSOR_FILE, ensure_dirs

    address = keystore.address()
    ensure_dirs()
    try:
        cursor = _json.loads(EARNINGS_CURSOR_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        cursor = {}

    head = chain.block_number(cfg)
    start = int(cursor.get("block") or max(0, head - lookback_blocks))

    seen = {(e.get("tx"), e.get("log_index")) for e in entries()
            if e.get("direction") == "in"}

    added = []
    for t in chain.incoming_transfers(address, start, cfg):
        if (t["tx"], t["log_index"]) in seen:
            continue
        _append({
            "at": datetime.now(timezone.utc).isoformat(),
            "direction": "in",
            "amount_usdc": round(float(t["amount_usdc"]), 6),
            "counterparty": t["from"],
            "category": "earnings",
            "note": "observed on chain",
            "tx": t["tx"],
            "log_index": t["log_index"],
            "block": t["block"],
            # Nobody signed anything to say what this was for. Marked so a
            # human reading the ledger later is not misled into thinking the
            # attribution is stronger than it is.
            "attributed": False,
        })
        added.append(t)

    # Only advance the cursor past blocks we have actually read. Recording it
    # before the writes would lose anything that failed halfway.
    EARNINGS_CURSOR_FILE.write_text(
        _json.dumps({"block": head + 1, "address": address}, indent=2),
        encoding="utf-8")
    return added


def entries(days=None):
    if not LEDGER_FILE.exists():
        return []
    cutoff = None
    if days:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    with open(LEDGER_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
                if cutoff and datetime.fromisoformat(e["at"]) < cutoff:
                    continue
                out.append(e)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue    # one bad line must not hide the rest
    return out


# ---------------------------------------------------------------------------
# Known destinations — security, not analytics
# ---------------------------------------------------------------------------

def known_destinations():
    if not DESTINATIONS_FILE.exists():
        return {}
    try:
        return json.loads(DESTINATIONS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        # Fail closed: if we can't tell what's known, treat everything as new.
        return {}


def is_new_destination(address):
    """Never paid before. Says nothing about how long ago that was."""
    return address.lower() not in {k.lower() for k in known_destinations()}


def destination_status(address, cfg=None):
    """Is this address new, long-dormant, or in regular use?

    Trust here was permanent: an address confirmed once was trusted for the
    rest of the install's life. hermessol pointed out what that means — a
    merchant compromised six months after you last paid them is still on your
    trusted list, and the control that was supposed to catch a strange payment
    has already been spent on a payment you made in another era.

    So trust decays with disuse. An address you have not paid in
    `destination_trust_days` needs confirming again, exactly like a new one.

    Be clear about what this does and does not buy. It does NOT detect a
    compromise: an address you pay every week stays trusted, and nothing in a
    ledger could tell you otherwise. What it stops is trust accumulating —
    a list that only ever grows, where every address you have ever paid is a
    permanently open door. Dormant entries close by themselves.

    Returns "new", "lapsed" or "known", with the dates behind the verdict so a
    refusal can say when it was last paid rather than merely that it was.
    """
    entry = known_destinations().get(address.lower())
    if not entry:
        return {"status": "new", "last_paid": None, "days_since": None,
                "trust_days": _trust_days(cfg)}

    trust_days = _trust_days(cfg)
    last = entry.get("last_paid") or entry.get("first_paid")
    days = None
    if last:
        try:
            days = (datetime.now(timezone.utc)
                    - datetime.fromisoformat(last)).days
        except ValueError:
            days = None

    # A record with no readable date is treated as known, not as lapsed. The
    # date is bookkeeping we wrote ourselves; failing closed on our own bad
    # data would refuse payments to addresses the human really did confirm.
    lapsed = bool(trust_days and days is not None and days >= trust_days)
    return {"status": "lapsed" if lapsed else "known",
            "last_paid": last, "days_since": days, "trust_days": trust_days,
            "count": entry.get("count"), "label": entry.get("label")}


def _trust_days(cfg=None):
    """How long trust survives disuse. 0 means it never lapses.

    An unreadable value falls back to the default rather than to 0, because 0
    switches a security control off. A typo in a config file should not
    silently disable it.
    """
    from .config import DEFAULT_CONFIG
    cfg = cfg if cfg is not None else load_config()
    raw = cfg.get("destination_trust_days", DEFAULT_CONFIG["destination_trust_days"])
    try:
        return max(0, int(float(raw)))
    except (TypeError, ValueError):
        return int(DEFAULT_CONFIG["destination_trust_days"])


def remember_destination(address, label=None):
    ensure_dirs()
    known = known_destinations()
    key = address.lower()
    entry = known.get(key, {"first_paid": datetime.now(timezone.utc).isoformat(), "count": 0})
    entry["count"] = entry.get("count", 0) + 1
    entry["last_paid"] = datetime.now(timezone.utc).isoformat()
    if label:
        entry["label"] = label
    known[key] = entry
    DESTINATIONS_FILE.write_text(json.dumps(known, indent=2), encoding="utf-8")
    try:
        os.chmod(DESTINATIONS_FILE, 0o600)
    except (OSError, NotImplementedError):
        pass


# ---------------------------------------------------------------------------
# P&L
# ---------------------------------------------------------------------------

def lifetime():
    """Everything, since the first entry. No window.

    The windowed figures answer "how is it going"; this answers "has it ever
    been worth it", which is the question somebody asks before deciding to stop
    paying for an agent. Nothing else in here could answer it.
    """
    rows = entries(days=None)
    earned = sum(e["amount_usdc"] for e in rows if e["direction"] == "in")
    spent = sum(e["amount_usdc"] for e in rows if e["direction"] == "out")
    return {
        "earned_usdc": round(earned, 6),
        "spent_usdc": round(spent, 6),
        "net_usdc": round(earned - spent, 6),
        "transactions": len(rows),
        "since": rows[0]["at"][:10] if rows else None,
    }


def profit_and_loss(days=30):
    rows = entries(days=days)
    earned = sum(e["amount_usdc"] for e in rows if e["direction"] == "in")
    spent = sum(e["amount_usdc"] for e in rows if e["direction"] == "out")

    by_category = defaultdict(float)
    for e in rows:
        if e["direction"] == "out":
            by_category[e.get("category", "other")] += e["amount_usdc"]

    biggest = sorted(by_category.items(), key=lambda kv: kv[1], reverse=True)

    net = round(earned - spent, 6)
    return {
        "window_days": days,
        "earned_usdc": round(earned, 6),
        "spent_usdc": round(spent, 6),
        "net_usdc": net,
        "profitable": net >= 0,
        "spend_by_category": {k: round(v, 6) for k, v in biggest},
        "largest_cost": biggest[0][0] if biggest else None,
        "transactions": len(rows),
        # Only meaningful once there is income to compare against.
        "cost_recovery_percent": (round(earned / spent * 100, 1) if spent else None),
    }


def daily_burn(days=30):
    """Average USDC out per day. The denominator for runway."""
    rows = [e for e in entries(days=days) if e["direction"] == "out"]
    if not rows:
        return 0.0
    observed = min(days, max(1, _days_spanned(rows)))
    return round(sum(e["amount_usdc"] for e in rows) / observed, 6)


def _days_spanned(rows):
    try:
        stamps = [datetime.fromisoformat(e["at"]) for e in rows]
        return max(1, (max(stamps) - min(stamps)).days + 1)
    except Exception:
        return 1


def runway(balance_usdc, days=30):
    """How long the money lasts at the current rate.

    Reported so an agent can warn its human BEFORE it stops working, which is
    the difference between a useful assistant and one that silently died.
    """
    burn = daily_burn(days)
    if burn <= 0:
        return {"days_remaining": None, "daily_burn_usdc": 0.0,
                "status": "no spending recorded yet", "balance_usdc": balance_usdc}

    remaining = balance_usdc / burn
    if remaining < 3:
        status, action = "critical", "Ask your human to top up now — you stop working within days."
    elif remaining < 7:
        status, action = "low", "Tell your human this week."
    elif remaining < 30:
        status, action = "ok", "Fine for now. Mention it at the next check-in."
    else:
        status, action = "healthy", "No action needed."

    return {
        "balance_usdc": round(balance_usdc, 6),
        "daily_burn_usdc": burn,
        "days_remaining": round(remaining, 1),
        "empty_on": (datetime.now(timezone.utc) + timedelta(days=remaining)).strftime("%Y-%m-%d"),
        "status": status,
        "action": action,
    }


def report(balance_usdc, days=30):
    """The whole picture, in the shape an agent can relay to its human."""
    pnl = profit_and_loss(days)
    run = runway(balance_usdc, days)

    if pnl["transactions"] == 0:
        summary = "No activity yet."
    elif pnl["earned_usdc"] == 0:
        summary = (f"Spent ${pnl['spent_usdc']:.2f} over {days} days and earned nothing. "
                   f"Biggest cost: {pnl['largest_cost']}.")
    elif pnl["profitable"]:
        summary = (f"Earned ${pnl['earned_usdc']:.2f}, spent ${pnl['spent_usdc']:.2f} — "
                   f"${pnl['net_usdc']:.2f} ahead over {days} days.")
    else:
        summary = (f"Earned ${pnl['earned_usdc']:.2f} against ${pnl['spent_usdc']:.2f} of costs — "
                   f"${abs(pnl['net_usdc']):.2f} short. Covering "
                   f"{pnl['cost_recovery_percent']}% of what it costs to run.")

    if run["days_remaining"] is not None and run["status"] in ("critical", "low"):
        summary += f" {run['days_remaining']} days of funds left."

    return {"summary": summary, "profit_and_loss": pnl, "runway": run}


# ---------------------------------------------------------------------------
# Goals — turning accounting into an objective
# ---------------------------------------------------------------------------
#
# A ledger tells an agent what happened. A goal tells it what to aim at, which
# is the difference between a report and a reason to act. Three kinds:
#
#   target      earn a specific amount by a date
#   breakeven   earn enough to cover what you cost to run — the honest one,
#               and the only goal that makes an agent self-sustaining
#   runway      keep at least N days of funds in hand
#
# The kit tracks the gap and the rate needed. It does not promise the money will
# appear — that depends entirely on whether anyone buys what the agent offers.

GOAL_FILE = CONFIG_DIR / "goal.json"
GOAL_TYPES = ("target", "breakeven", "runway")


def set_goal(kind, amount=None, by_date=None, note=None):
    """Set the objective. Human or agent may call this."""
    if kind not in GOAL_TYPES:
        raise ValueError(f"Unknown goal type {kind!r}. Use one of: {', '.join(GOAL_TYPES)}")
    if kind in ("target", "runway") and (amount is None or float(amount) <= 0):
        raise ValueError(f"A {kind} goal needs a positive amount.")

    ensure_dirs()
    goal = {
        "kind": kind,
        "amount": float(amount) if amount is not None else None,
        "by_date": by_date,
        "note": note,
        "set_at": datetime.now(timezone.utc).isoformat(),
    }
    GOAL_FILE.write_text(json.dumps(goal, indent=2), encoding="utf-8")
    return goal


def get_goal():
    if not GOAL_FILE.exists():
        return None
    try:
        return json.loads(GOAL_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def clear_goal():
    if GOAL_FILE.exists():
        GOAL_FILE.unlink()
    return True


def goal_progress(balance_usdc=None, days=30):
    """Where the agent stands against its objective, and what rate closes the gap."""
    goal = get_goal()
    if not goal:
        return {"goal": None, "message": "No goal set. Try: stipend goal set breakeven"}

    rows = entries(days=days)
    earned = sum(e["amount_usdc"] for e in rows if e["direction"] == "in")
    spent = sum(e["amount_usdc"] for e in rows if e["direction"] == "out")
    kind = goal["kind"]

    days_left = None
    if goal.get("by_date"):
        try:
            deadline = datetime.fromisoformat(goal["by_date"]).replace(tzinfo=timezone.utc)
            days_left = max(0, (deadline - datetime.now(timezone.utc)).days)
        except ValueError:
            pass

    if kind == "target":
        achieved, needed = earned, goal["amount"]
    elif kind == "breakeven":
        achieved, needed = earned, spent
    else:  # runway
        # Follow the window that was asked for. This was pinned at 7 while the
        # rest of the report moved, so a 30-day view showed a runway derived
        # from a week of spending — two different periods in one sentence.
        burn = daily_burn(days=days)
        achieved = (balance_usdc / burn) if burn > 0 and balance_usdc is not None else 0.0
        needed = goal["amount"]

    remaining = max(0.0, needed - achieved)
    percent = round(achieved / needed * 100, 1) if needed > 0 else 100.0
    per_day = round(remaining / days_left, 4) if days_left else None

    if remaining <= 0:
        message = {
            "target": f"Goal reached — earned ${achieved:.2f} of ${needed:.2f}.",
            "breakeven": f"Breaking even: earned ${achieved:.2f} against ${needed:.2f} of costs.",
            "runway": f"Runway goal met — {achieved:.1f} days in hand.",
        }[kind]
    elif kind == "breakeven":
        message = (f"Covering {percent}% of costs. ${remaining:.2f} short over {days} days — "
                   f"earned ${achieved:.2f} against ${needed:.2f} spent.")
    elif kind == "runway":
        message = f"{achieved:.1f} days of funds against a {needed:.0f}-day goal."
    else:
        message = f"${achieved:.2f} of ${needed:.2f} ({percent}%). ${remaining:.2f} to go."
        if per_day:
            message += f" That's ${per_day:.2f}/day for {days_left} days."

    return {
        "goal": goal,
        "achieved_usdc": round(achieved, 6),
        "needed_usdc": round(needed, 6),
        "remaining_usdc": round(remaining, 6),
        "percent": percent,
        "reached": remaining <= 0,
        "days_left": days_left,
        "required_per_day_usdc": per_day,
        "message": message,
    }
