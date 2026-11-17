#!/usr/bin/env python3
"""journal_trade.py — append-only trade journal (trades.json).

Every decision is journaled, including "wait". Entries follow the SPEC section 6
schema (ts, symbol, mode, decision, signal, signal_reason, confidence,
adjusted_confidence, regime, confluence, order, exec_result, status, market,
features_1h, outcome, realised_pnl, close_reason, closed_at, lesson_tags).

Module:  from journal_trade import journal_entry, load_journal, update_entry
CLI:     python3 journal_trade.py trades.json --last 5
         cat entry.json | python3 journal_trade.py trades.json --append
"""

import argparse
import json
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import filelock  # noqa: E402

JOURNAL_FIELDS = [
    "ts", "symbol", "mode", "decision", "signal", "signal_reason", "confidence",
    "adjusted_confidence", "regime", "confluence", "order", "exec_result",
    "status", "market", "features_1h", "outcome", "realised_pnl",
    "close_reason", "closed_at", "lesson_tags",
    "model", "llm_reasoning", "exit_plan",
]


def utcnow():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def load_journal(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("journal %s must contain a JSON array" % path)
    return data


def save_journal(path, entries):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(path)) or ".",
                               prefix=".trades-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(entries, f, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def normalize_entry(entry):
    out = {k: entry.get(k) for k in JOURNAL_FIELDS if k in entry or k in _DEFAULTS}
    for k, v in _DEFAULTS.items():
        if out.get(k) is None and v is not None:
            out[k] = v() if callable(v) else v
    return out


_DEFAULTS = {
    "ts": utcnow,
    "lesson_tags": list,
    "status": "journaled",
    "decision": "wait",
    "outcome": None,
    "realised_pnl": None,
    "close_reason": None,
    "closed_at": None,
}


def journal_entry(path, entry):
    """Append one normalized entry. Returns the stored entry."""
    with filelock.held(path):  # load->append->save must be one critical section
        entries = load_journal(path)
        stored = normalize_entry(entry)
        entries.append(stored)
        save_journal(path, entries)
        return stored


def update_entry(path, predicate, updates):
    """Update the newest entry matching predicate(entry). Returns it or None."""
    with filelock.held(path):
        entries = load_journal(path)
        for entry in reversed(entries):
            if predicate(entry):
                entry.update(updates)
                save_journal(path, entries)
                return entry
        return None


def find_open_entry(entries, symbol):
    """Newest executed entry for a symbol that is not closed yet."""
    for entry in reversed(entries):
        if (entry.get("symbol") == symbol and entry.get("decision") == "executed"
                and entry.get("status") in ("open", "executed")):
            return entry
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description="Trade journal tool")
    parser.add_argument("journal", help="path to trades.json")
    parser.add_argument("--last", type=int, default=None, help="print the last N entries")
    parser.add_argument("--append", action="store_true", help="append entry JSON from stdin")
    parser.add_argument("--symbol", default=None, help="filter by symbol")
    args = parser.parse_args(argv)

    if args.append:
        entry = json.load(sys.stdin)
        stored = journal_entry(args.journal, entry)
        print(json.dumps(stored, indent=2))
        return 0

    entries = load_journal(args.journal)
    if args.symbol:
        entries = [e for e in entries if e.get("symbol") == args.symbol.upper()]
    if args.last is not None:
        entries = entries[-args.last:]
    print(json.dumps(entries, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
