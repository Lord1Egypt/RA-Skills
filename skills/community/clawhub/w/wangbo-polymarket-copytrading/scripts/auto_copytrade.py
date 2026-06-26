#!/usr/bin/env python3
import argparse
import json
import subprocess
import time
from datetime import datetime

BASE = "https://data-api.polymarket.com/v1/leaderboard"
PERIODS = ["DAY", "WEEK", "MONTH", "ALL"]


def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()


def fetch_board(category: str, period: str, limit: int = 100):
    url = f"{BASE}?category={category}&timePeriod={period}&orderBy=PNL&limit={limit}&offset=0"
    out = run(["curl", "-sS", "-L", "--retry", "3", "--retry-delay", "1", "--max-time", "20", url])
    rows = json.loads(out)
    idx = {}
    for i, r in enumerate(rows, start=1):
        w = (r.get("proxyWallet") or "").lower()
        if not w:
            continue
        idx[w] = {
            "rank": i,
            "pnl": float(r.get("pnl", 0) or 0),
            "vol": float(r.get("vol", 0) or 0),
            "userName": r.get("userName") or "",
        }
    return idx


def phase(day, week, month):
    if day <= 10 and week <= 10 and month <= 20:
        return "巅峰"
    if week <= 15 and month <= 30:
        return "强势"
    if month <= 20 and day > 30:
        return "观察"
    return "普通"


def phase_ok(current, min_phase):
    order = {"普通": 0, "观察": 1, "强势": 2, "巅峰": 3}
    return order.get(current, 0) >= order.get(min_phase, 2)


def get_trader_phase(wallet: str, category: str):
    w = wallet.lower()
    boards = {p: fetch_board(category, p) for p in PERIODS}
    d = boards["DAY"].get(w, {}).get("rank", 999)
    wk = boards["WEEK"].get(w, {}).get("rank", 999)
    m = boards["MONTH"].get(w, {}).get("rank", 999)
    a = boards["ALL"].get(w, {}).get("rank", 999)
    return {
        "day": d,
        "week": wk,
        "month": m,
        "all": a,
        "phase": phase(d, wk, m),
    }


def get_market_snapshot(slug: str):
    out = run(["polymarket", "markets", "get", slug, "--output", "json"])
    m = json.loads(out)
    outcomes = json.loads(m.get("outcomes", "[]"))
    prices = [float(x) for x in json.loads(m.get("outcomePrices", "[]"))]
    token_ids = json.loads(m.get("clobTokenIds", "[]"))
    return {
        "slug": slug,
        "question": m.get("question", ""),
        "acceptingOrders": bool(m.get("acceptingOrders", False)),
        "closed": bool(m.get("closed", True)),
        "outcomes": outcomes,
        "prices": prices,
        "token_ids": token_ids,
    }


def find_outcome_index(outcomes, target_name):
    target = target_name.strip().lower()
    for i, name in enumerate(outcomes):
        if str(name).strip().lower() == target:
            return i
    raise ValueError(f"Outcome '{target_name}' not found in {outcomes}")


def place_order(token_id: str, amount: float, signature_type: str, execute: bool):
    cmd = [
        "polymarket",
        "clob",
        "market-order",
        "--signature-type",
        signature_type,
        "--token",
        token_id,
        "--amount",
        str(amount),
        "--side",
        "buy",
        "--output",
        "json",
    ]
    if not execute:
        return {"dryRun": True, "cmd": " ".join(cmd)}
    out = run(cmd)
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out}


def process_once(cfg, execute=False):
    print(f"\n[{datetime.now().isoformat(timespec='seconds')}] scan start")
    sig = cfg.get("signatureType", "eoa")
    max_concurrent = int(cfg.get("maxConcurrent", 2))
    placed = 0

    for r in cfg.get("rules", []):
        if placed >= max_concurrent:
            print("- hit maxConcurrent, stop this cycle")
            break

        trader = r["trader"]
        wallet = r["wallet"]
        category = r.get("category", "OVERALL")
        min_phase = r.get("minPhase", "强势")

        tphase = get_trader_phase(wallet, category)
        ok_phase = phase_ok(tphase["phase"], min_phase)
        print(f"- trader {trader} phase={tphase['phase']} (D/W/M={tphase['day']}/{tphase['week']}/{tphase['month']}) need>={min_phase}")
        if not ok_phase:
            print("  skip: trader phase below threshold")
            continue

        try:
            market = get_market_snapshot(r["marketSlug"])
        except Exception as e:
            print(f"  skip: market fetch failed for {r['marketSlug']}: {e}")
            continue

        if market["closed"] or (not market["acceptingOrders"]):
            print(f"  skip: market unavailable closed={market['closed']} accepting={market['acceptingOrders']}")
            continue

        idx = find_outcome_index(market["outcomes"], r["outcome"])
        price = market["prices"][idx]
        token_id = market["token_ids"][idx]
        max_entry = float(r["maxEntryPrice"])
        amount = float(r["amount"])

        print(f"  market={r['marketSlug']} outcome={r['outcome']} price={price:.3f} threshold<={max_entry:.3f}")
        if price > max_entry:
            print("  skip: price above threshold")
            continue

        res = place_order(token_id, amount, sig, execute)
        placed += 1
        print("  order:", json.dumps(res, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description="Auto monitor + threshold execution for copytrading")
    ap.add_argument("--config", required=True, help="Path to JSON config")
    ap.add_argument("--execute", action="store_true", help="Actually place orders (default dry-run)")
    ap.add_argument("--interval", type=int, default=0, help="Loop interval seconds, 0 means run once")
    args = ap.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if args.interval <= 0:
        process_once(cfg, execute=args.execute)
        return

    while True:
        try:
            process_once(cfg, execute=args.execute)
        except Exception as e:
            print("scan error:", e)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
