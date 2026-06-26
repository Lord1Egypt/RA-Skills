"""
Trade Logger — 交易记录核心脚本

Record, edit, delete, and list trade journal entries.

Usage:
    python trade_logger.py add <json_string>              # Add a new trade
    python trade_logger.py add --from-file <json_file>    # Add from JSON file
    python trade_logger.py list [date]                    # List trades for a date (default: today)
    python trade_logger.py list --range <start> <end>     # List trades in date range
    python trade_logger.py delete <date> <index>          # Delete trade at index
    python trade_logger.py update <date> <index> <field=value> # Update a trade
    python trade_logger.py search <keyword>               # Search trades by keyword/symbol
"""

import json
import sys
import os
from datetime import date, datetime
from typing import Optional

# ── Config ──

JOURNALS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "journals"
)


def _journal_path(target_date: str = None) -> str:
    """Get path for a date's journal file."""
    if target_date is None:
        target_date = date.today().isoformat()
    return os.path.join(JOURNALS_DIR, target_date + ".json")


def _ensure_journals_dir():
    os.makedirs(JOURNALS_DIR, exist_ok=True)


def _load_trades(target_date: str = None) -> list:
    """Load trades for a given date."""
    path = _journal_path(target_date)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("trades", [])


def _save_trades(trades: list, target_date: str = None):
    """Save trades for a given date."""
    _ensure_journals_dir()
    path = _journal_path(target_date)
    data = {
        "date": target_date or date.today().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "trade_count": len(trades),
        "trades": trades
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _calculate_pnl(trade: dict) -> float:
    """Calculate P&L for a single trade."""
    if trade.get("open", False) or trade.get("exit_price") is None:
        return None

    if trade["type"] == "futures":
        direction = 1 if trade["direction"] == "long" else -1
        pnl = (trade["exit_price"] - trade["entry_price"]) * trade["quantity"] * trade["multiplier"] * direction
    elif trade["type"] == "stock":
        direction = 1 if trade["direction"] == "long" else -1
        pnl = (trade["exit_price"] - trade["entry_price"]) * trade["quantity"] * direction
    else:
        return 0

    # Subtract fees and stamp duty
    fees = trade.get("fees", 0)
    stamp_duty = trade.get("stamp_duty", 0)
    pnl -= fees + stamp_duty

    return round(pnl, 2)


def add_trade(trade_data: dict) -> dict:
    """Add a new trade entry and calculate P&L."""
    target_date = trade_data.get("date", date.today().isoformat())

    # Auto-calculate P&L
    if not trade_data.get("open", False) and trade_data.get("exit_price") is not None:
        trade_data["pnl"] = _calculate_pnl(trade_data)

    trades = _load_trades(target_date)
    trades.append(trade_data)
    _save_trades(trades, target_date)

    return {
        "status": "ok",
        "date": target_date,
        "index": len(trades) - 1,
        "trade": trade_data,
        "pnl": trade_data.get("pnl")
    }


def list_trades(target_date: str = None, start_date: str = None, end_date: str = None) -> list:
    """List trades for a date or range."""
    if start_date and end_date:
        all_trades = []
        from datetime import timedelta
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        current = start
        while current <= end:
            ds = current.isoformat()
            trades = _load_trades(ds)
            for t in trades:
                t["_file_date"] = ds
                all_trades.append(t)
            current += timedelta(days=1)
        return all_trades

    tgt = target_date or date.today().isoformat()
    trades = _load_trades(tgt)
    for t in trades:
        t["_file_date"] = tgt
    return trades


def delete_trade(target_date: str, index: int) -> dict:
    """Delete a trade at index for a given date."""
    trades = _load_trades(target_date)
    if index < 0 or index >= len(trades):
        return {"status": "error", "message": f"Index {index} out of range (0-{len(trades)-1})"}
    removed = trades.pop(index)
    _save_trades(trades, target_date)
    return {"status": "ok", "removed": removed}


def update_trade(target_date: str, index: int, field: str, value: str) -> dict:
    """Update a field in a trade entry."""
    trades = _load_trades(target_date)
    if index < 0 or index >= len(trades):
        return {"status": "error", "message": f"Index {index} out of range (0-{len(trades)-1})"}

    # Typecast common fields
    if field in ("entry_price", "exit_price", "fees", "stamp_duty", "multiplier"):
        value = float(value)
    elif field in ("quantity",):
        value = int(value)

    trades[index][field] = value

    # Recalculate P&L if relevant fields changed
    if field in ("entry_price", "exit_price", "quantity", "multiplier", "fees", "direction", "stamp_duty"):
        trades[index]["pnl"] = _calculate_pnl(trades[index])

    _save_trades(trades, target_date)
    return {"status": "ok", "index": index, "updated": {field: value}, "trade": trades[index]}


def search_trades(keyword: str) -> list:
    """Search across all journal files for trades matching keyword/symbol."""
    results = []
    if not os.path.exists(JOURNALS_DIR):
        return results

    kw_lower = keyword.lower()
    for fname in os.listdir(JOURNALS_DIR):
        if not fname.endswith(".json"):
            continue
        fdate = fname.replace(".json", "")
        # Validate date format
        try:
            date.fromisoformat(fdate)
        except ValueError:
            continue

        trades = _load_trades(fdate)
        for i, t in enumerate(trades):
            text = json.dumps(t, ensure_ascii=False).lower()
            if kw_lower in text:
                t["_file_date"] = fdate
                t["_index"] = i
                results.append(t)

    return results


# ── Main ──

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if "--from-file" in sys.argv:
            idx = sys.argv.index("--from-file") + 1
            with open(sys.argv[idx], "r", encoding="utf-8") as f:
                data = json.load(f)
        elif len(sys.argv) >= 3:
            data = json.loads(sys.argv[2])
        else:
            print("Error: Provide trade data as JSON string or --from-file <path>")
            sys.exit(1)
        result = add_trade(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "list":
        if "--range" in sys.argv:
            idx = sys.argv.index("--range") + 1
            start = sys.argv[idx]
            end = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else start
            trades = list_trades(start_date=start, end_date=end)
        else:
            tgt = sys.argv[2] if len(sys.argv) >= 3 else None
            trades = list_trades(target_date=tgt)
        print(json.dumps(trades, ensure_ascii=False, indent=2))

    elif command == "delete" and len(sys.argv) >= 4:
        result = delete_trade(sys.argv[2], int(sys.argv[3]))
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "update" and len(sys.argv) >= 5:
        tgt, idx, kv = sys.argv[2], int(sys.argv[3]), sys.argv[4]
        if "=" not in kv:
            print("Error: Field update must be in format field=value")
            sys.exit(1)
        field, value = kv.split("=", 1)
        result = update_trade(tgt, idx, field, value)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "search" and len(sys.argv) >= 3:
        results = search_trades(sys.argv[2])
        print(json.dumps(results, ensure_ascii=False, indent=2))

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
