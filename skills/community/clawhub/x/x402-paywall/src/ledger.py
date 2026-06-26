"""
Agent Economy — Standalone Ledger for tracking x402 payments.
Can be used independently of the Paywall class.
"""

import csv
import json
import os
import sqlite3
import time
from typing import Dict, List, Optional


class Ledger:
    """Track x402 payments, usage, and revenue."""

    def __init__(self, db_path: str = "agent_economy.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tx_hash TEXT UNIQUE NOT NULL,
                    payer TEXT NOT NULL,
                    skill TEXT NOT NULL,
                    amount REAL NOT NULL,
                    token TEXT DEFAULT 'USDC',
                    network TEXT DEFAULT 'base',
                    verified INTEGER DEFAULT 1,
                    created_at REAL NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_payments_payer ON payments(payer)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_payments_skill ON payments(skill)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_payments_created ON payments(created_at)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payer TEXT NOT NULL,
                    skill TEXT NOT NULL,
                    amount REAL NOT NULL,
                    starts_at REAL NOT NULL,
                    expires_at REAL NOT NULL,
                    active INTEGER DEFAULT 1
                )
            """)

    def record(self, payer: str, skill: str, amount: float,
               tx_hash: str, network: str = "base", token: str = "USDC",
               verified: bool = True):
        """Record a payment."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO payments "
                "(tx_hash, payer, skill, amount, token, network, verified, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (tx_hash, payer.lower(), skill, amount, token, network,
                 1 if verified else 0, time.time())
            )

    def get_revenue(self, period: str = "30d") -> Dict:
        """Get total revenue for a time period."""
        days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
        cutoff = time.time() - (days * 86400)

        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0), COUNT(*), COUNT(DISTINCT payer) "
                "FROM payments WHERE created_at > ? AND verified = 1",
                (cutoff,)
            ).fetchone()

        return {
            "period": period,
            "total_usd": round(row[0], 2),
            "calls": row[1],
            "unique_payers": row[2],
        }

    def get_skill_breakdown(self) -> Dict[str, Dict]:
        """Revenue breakdown per skill."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT skill, COUNT(*), COALESCE(SUM(amount), 0), COUNT(DISTINCT payer) "
                "FROM payments WHERE verified = 1 GROUP BY skill ORDER BY SUM(amount) DESC"
            ).fetchall()

        return {
            row[0]: {
                "calls": row[1],
                "revenue_usd": round(row[2], 2),
                "unique_payers": row[3],
            }
            for row in rows
        }

    def get_payer_history(self, payer: str, limit: int = 50) -> List[Dict]:
        """Payment history for a specific payer."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM payments WHERE payer = ? ORDER BY created_at DESC LIMIT ?",
                (payer.lower(), limit)
            ).fetchall()

        return [dict(r) for r in rows]

    def is_subscribed(self, payer: str, skill: str = "") -> bool:
        """Check if payer has an active subscription."""
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT 1 FROM subscriptions WHERE payer = ? AND active = 1 AND expires_at > ?"
            params = [payer.lower(), now]
            if skill:
                query += " AND skill = ?"
                params.append(skill)
            return conn.execute(query, params).fetchone() is not None

    def add_subscription(self, payer: str, skill: str, amount: float,
                         duration_days: int = 30, tx_hash: str = ""):
        """Record a new subscription."""
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            # Deactivate any existing subscription for this payer/skill
            conn.execute(
                "UPDATE subscriptions SET active = 0 WHERE payer = ? AND skill = ?",
                (payer.lower(), skill)
            )
            conn.execute(
                "INSERT INTO subscriptions (payer, skill, amount, starts_at, expires_at, active) "
                "VALUES (?, ?, ?, ?, ?, 1)",
                (payer.lower(), skill, amount, now, now + (duration_days * 86400))
            )
            # Also record as a payment
            if tx_hash:
                self.record(payer, skill, amount, tx_hash)

    def export_csv(self, output_path: str, period: str = "30d"):
        """Export payments to CSV."""
        days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
        cutoff = time.time() - (days * 86400)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM payments WHERE created_at > ? ORDER BY created_at DESC",
                (cutoff,)
            ).fetchall()

        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "tx_hash", "payer", "skill", "amount", "token", "network", "verified", "timestamp"])
            for r in rows:
                writer.writerow([
                    r["id"], r["tx_hash"], r["payer"], r["skill"],
                    r["amount"], r["token"], r["network"], r["verified"],
                    time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(r["created_at"]))
                ])

    def get_daily_revenue(self, days: int = 30) -> List[Dict]:
        """Daily revenue for charting."""
        cutoff = time.time() - (days * 86400)
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT date(created_at, 'unixepoch') as day, "
                "COUNT(*) as calls, COALESCE(SUM(amount), 0) as revenue "
                "FROM payments WHERE created_at > ? AND verified = 1 "
                "GROUP BY day ORDER BY day",
                (cutoff,)
            ).fetchall()

        return [{"date": r[0], "calls": r[1], "revenue": round(r[2], 2)} for r in rows]


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Agent Economy Ledger CLI")
    parser.add_argument("--db", default="agent_economy.db", help="Database path")
    sub = parser.add_subparsers(dest="command")

    rev = sub.add_parser("revenue", help="Show revenue summary")
    rev.add_argument("--period", default="30d")

    skills = sub.add_parser("skills", help="Show per-skill breakdown")

    history = sub.add_parser("history", help="Show payer history")
    history.add_argument("payer")
    history.add_argument("--limit", type=int, default=20)

    export = sub.add_parser("export", help="Export to CSV")
    export.add_argument("--output", default="payments.csv")
    export.add_argument("--period", default="30d")

    daily = sub.add_parser("daily", help="Daily revenue")
    daily.add_argument("--days", type=int, default=30)

    args = parser.parse_args()
    ledger = Ledger(db_path=args.db)

    if args.command == "revenue":
        print(json.dumps(ledger.get_revenue(args.period), indent=2))
    elif args.command == "skills":
        print(json.dumps(ledger.get_skill_breakdown(), indent=2))
    elif args.command == "history":
        print(json.dumps(ledger.get_payer_history(args.payer, args.limit), indent=2))
    elif args.command == "export":
        ledger.export_csv(args.output, args.period)
        print(f"Exported to {args.output}")
    elif args.command == "daily":
        print(json.dumps(ledger.get_daily_revenue(args.days), indent=2))
    else:
        parser.print_help()
