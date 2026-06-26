#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime, timezone


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(path.read_text())


def dump_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def calc_equity(account: dict) -> float:
    cash = float(account.get("cash", 0))
    positions = account.get("positions", [])
    market_value = 0.0
    for pos in positions:
        qty = float(pos.get("qty", 0))
        price = pos.get("currentPrice")
        if price is None:
            continue
        market_value += qty * float(price)
    return cash + market_value


def main():
    if len(sys.argv) < 2:
        print("Usage: update_account.py <account.json>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    account = load_json(path)

    equity = calc_equity(account)
    initial_cash = float(account.get("initialCash", equity or 0))
    account["equity"] = round(equity, 2)
    account["totalReturnPct"] = round(((equity - initial_cash) / initial_cash) * 100, 4) if initial_cash else 0
    account["updatedAt"] = datetime.now(timezone.utc).isoformat()

    dump_json(path, account)
    print(json.dumps({
        "equity": account["equity"],
        "totalReturnPct": account["totalReturnPct"],
        "updatedAt": account["updatedAt"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
