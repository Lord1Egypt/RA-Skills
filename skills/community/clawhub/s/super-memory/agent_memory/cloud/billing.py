"""Billing engine for the managed service."""
from __future__ import annotations

import json
import logging
import os
import sqlite3
import threading
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class BillingPlan(Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"


# Hardcoded defaults — used when pricing.json is not available
_DEFAULT_PLAN_PRICING: dict[str, dict[str, float]] = {
    "free": {"monthly_fee": 0.0, "per_remember": 0.0, "per_recall": 0.0, "per_gb": 0.0, "monthly_credits": 100.0},
    "starter": {"monthly_fee": 29.0, "per_remember": 0.0001, "per_recall": 0.0002, "per_gb": 0.5, "monthly_credits": 10000.0},
    "pro": {"monthly_fee": 99.0, "per_remember": 0.00005, "per_recall": 0.0001, "per_gb": 0.3, "monthly_credits": 100000.0},
    "enterprise": {"monthly_fee": 499.0, "per_remember": 0.00002, "per_recall": 0.00005, "per_gb": 0.1, "monthly_credits": 1000000.0},
}

PLAN_PRICING: dict[str, dict[str, float]] = dict(_DEFAULT_PLAN_PRICING)


class InsufficientCreditsError(Exception):
    """Raised when a tenant has insufficient credits for an operation."""
    pass


class TenantSuspendedError(Exception):
    """Raised when a tenant is suspended."""
    pass


@dataclass
class UsageRecord:
    tenant_id: str
    operation: str
    timestamp: float
    latency_ms: float
    is_error: bool


class BillingEngine:
    _BILLING_BATCH_SIZE = 100
    _BILLING_FLUSH_INTERVAL = 5.0

    def __init__(self, db_path: str = ":memory:"):
        self._db = sqlite3.connect(db_path, check_same_thread=False)
        self._plans: dict[str, BillingPlan] = {}
        self._billing_buffer = []
        self._last_billing_flush = time.time()
        self._billing_lock = threading.Lock()
        self._init_db()
        self._load_pricing()

    def _init_db(self):
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS billing_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id TEXT NOT NULL,
                operation TEXT NOT NULL,
                timestamp REAL NOT NULL,
                latency_ms REAL,
                is_error INTEGER DEFAULT 0,
                cost REAL DEFAULT 0
            )
        """)
        self._db.execute("""
            CREATE INDEX IF NOT EXISTS idx_billing_tenant_ts
            ON billing_records(tenant_id, timestamp)
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id TEXT NOT NULL,
                period_start REAL NOT NULL,
                period_end REAL NOT NULL,
                total_cost REAL NOT NULL,
                operations_json TEXT,
                created_at REAL NOT NULL
            )
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS tenant_credits (
                tenant_id TEXT PRIMARY KEY,
                credits REAL NOT NULL DEFAULT 0,
                updated_at REAL
            )
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS tenant_suspensions (
                tenant_id TEXT PRIMARY KEY,
                reason TEXT NOT NULL,
                suspended_at REAL NOT NULL,
                suspended_by TEXT
            )
        """)
        self._db.execute("""
            CREATE INDEX IF NOT EXISTS idx_suspensions_tenant
            ON tenant_suspensions(tenant_id)
        """)
        self._db.commit()

    # ── Pricing externalization ────────────────────────────

    def _load_pricing(self):
        """Load pricing from JSON file, falling back to defaults."""
        global PLAN_PRICING
        custom_path = os.environ.get("AGENT_MEMORY_PRICING_CONFIG", "")
        if custom_path:
            path = Path(custom_path)
        else:
            path = Path(__file__).parent / "pricing.json"

        if path.is_file():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict) and "plans" in data:
                    PLAN_PRICING.clear()
                    for plan_name, pricing in data["plans"].items():
                        PLAN_PRICING[plan_name] = pricing
                    logger.info("Loaded pricing from %s", path)
                else:
                    logger.warning("Invalid pricing.json format, using defaults")
                    PLAN_PRICING = dict(_DEFAULT_PLAN_PRICING)
            except Exception as e:
                logger.warning("Failed to load pricing from %s: %s — using defaults", path, e)
                PLAN_PRICING = dict(_DEFAULT_PLAN_PRICING)
        else:
            PLAN_PRICING = dict(_DEFAULT_PLAN_PRICING)

    def load_pricing(self, path: str):
        """Load pricing from a custom JSON file path."""
        global PLAN_PRICING
        p = Path(path)
        if p.is_file():
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "plans" in data:
                PLAN_PRICING.clear()
                for plan_name, pricing in data["plans"].items():
                    PLAN_PRICING[plan_name] = pricing
                logger.info("Loaded pricing from %s", path)
        else:
            raise FileNotFoundError(f"Pricing file not found: {path}")

    # ── Plan management ────────────────────────────────────

    def set_plan(self, tenant_id: str, plan: BillingPlan):
        self._plans[tenant_id] = plan
        # Initialize credits for the tenant based on plan
        pricing = PLAN_PRICING.get(plan.value, {})
        monthly_credits = pricing.get("monthly_credits", 0)
        self._ensure_credits_row(tenant_id, monthly_credits)

    def get_plan(self, tenant_id: str) -> BillingPlan:
        return self._plans.get(tenant_id, BillingPlan.FREE)

    # ── Credit balance ─────────────────────────────────────

    def _ensure_credits_row(self, tenant_id: str, initial_credits: float = 0):
        """Ensure a credits row exists for the tenant."""
        row = self._db.execute(
            "SELECT credits FROM tenant_credits WHERE tenant_id = ?",
            (tenant_id,),
        ).fetchone()
        if row is None:
            self._db.execute(
                "INSERT INTO tenant_credits (tenant_id, credits, updated_at) VALUES (?, ?, ?)",
                (tenant_id, initial_credits, time.time()),
            )
            self._db.commit()

    def check_balance(self, tenant_id: str) -> float:
        """Return remaining credits for a tenant."""
        row = self._db.execute(
            "SELECT credits FROM tenant_credits WHERE tenant_id = ?",
            (tenant_id,),
        ).fetchone()
        if row is None:
            return 0.0
        return float(row[0])

    def add_credits(self, tenant_id: str, amount: float):
        """Add credits to a tenant's balance."""
        self._ensure_credits_row(tenant_id)
        self._db.execute(
            "UPDATE tenant_credits SET credits = credits + ?, updated_at = ? WHERE tenant_id = ?",
            (amount, time.time(), tenant_id),
        )
        self._db.commit()

    def deduct_credits(self, tenant_id: str, amount: float, operation: str = "") -> float:
        """Deduct credits from a tenant's balance.

        Returns remaining balance after deduction.
        Raises InsufficientCreditsError if balance is insufficient.
        """
        balance = self.check_balance(tenant_id)
        if balance <= 0 or balance < amount:
            raise InsufficientCreditsError(
                f"Insufficient credits for tenant {tenant_id}: "
                f"balance={balance:.4f}, required={amount:.4f}, operation={operation}"
            )
        new_balance = balance - amount
        self._db.execute(
            "UPDATE tenant_credits SET credits = ?, updated_at = ? WHERE tenant_id = ?",
            (new_balance, time.time(), tenant_id),
        )
        self._db.commit()
        return new_balance

    # ── Service suspension ─────────────────────────────────

    def suspend_tenant(self, tenant_id: str, reason: str, suspended_by: str = ""):
        """Suspend a tenant's service."""
        now = time.time()
        self._db.execute(
            "INSERT OR REPLACE INTO tenant_suspensions (tenant_id, reason, suspended_at, suspended_by) "
            "VALUES (?, ?, ?, ?)",
            (tenant_id, reason, now, suspended_by),
        )
        self._db.commit()
        logger.warning("Tenant %s suspended: %s", tenant_id, reason)

    def is_suspended(self, tenant_id: str) -> bool:
        """Check if a tenant is currently suspended."""
        row = self._db.execute(
            "SELECT 1 FROM tenant_suspensions WHERE tenant_id = ?",
            (tenant_id,),
        ).fetchone()
        return row is not None

    def reactivate_tenant(self, tenant_id: str):
        """Reactivate a suspended tenant."""
        self._db.execute(
            "DELETE FROM tenant_suspensions WHERE tenant_id = ?",
            (tenant_id,),
        )
        self._db.commit()
        logger.info("Tenant %s reactivated", tenant_id)

    # ── Billing-quota linkage ──────────────────────────────

    def check_and_deduct(self, tenant_id: str, operation: str, tokens: int = 0) -> tuple[bool, str]:
        """Check suspension and credit balance, then deduct credits for an operation.

        Returns (allowed, reason).
        """
        # 1. Check suspension
        if self.is_suspended(tenant_id):
            return False, "账户已暂停，请联系管理员或充值恢复"

        # 2. Calculate cost
        plan = self.get_plan(tenant_id)
        pricing = PLAN_PRICING.get(plan.value, {})
        cost = 0.0
        if operation == "remember":
            cost = pricing.get("per_remember", 0)
        elif operation == "recall":
            cost = pricing.get("per_recall", 0)

        # 3. Check credit balance
        if cost > 0:
            balance = self.check_balance(tenant_id)
            if balance <= 0 or balance < cost:
                return False, f"Insufficient credits: balance={balance:.4f}, required={cost:.4f}"

        # 4. Deduct credits
        if cost > 0:
            try:
                self.deduct_credits(tenant_id, cost, operation)
            except InsufficientCreditsError as e:
                return False, str(e)

        return True, ""

    # ── Usage recording ────────────────────────────────────

    def record_usage(self, tenant_id: str, operation: str,
                     latency_ms: float, is_error: bool = False):
        """Record billing with buffered writes."""
        plan = self.get_plan(tenant_id)
        pricing = PLAN_PRICING.get(plan.value, {})

        cost = 0.0
        if not is_error:
            if operation == "remember":
                cost = pricing.get("per_remember", 0)
            elif operation == "recall":
                cost = pricing.get("per_recall", 0)

        with self._billing_lock:
            self._billing_buffer.append(
                (tenant_id, operation, time.time(), latency_ms, int(is_error), cost)
            )

            should_flush = (
                len(self._billing_buffer) >= self._BILLING_BATCH_SIZE or
                time.time() - self._last_billing_flush >= self._BILLING_FLUSH_INTERVAL
            )

        if should_flush:
            self._flush_billing()

    def _flush_billing(self):
        """Flush buffered billing records."""
        with self._billing_lock:
            if not self._billing_buffer:
                return
            records = self._billing_buffer[:]
            self._billing_buffer.clear()
            self._last_billing_flush = time.time()

        try:
            self._db.executemany(
                "INSERT INTO billing_records (tenant_id, operation, timestamp, latency_ms, is_error, cost) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                records
            )
            self._db.commit()
        except Exception as e:
            logger.warning("计费数据写入失败: %s", e)

    def calculate_monthly_cost(self, tenant_id: str, year: int, month: int) -> dict:
        import calendar
        start = time.mktime((__import__('datetime').datetime(year, month, 1)).timetuple())
        last_day = calendar.monthrange(year, month)[1]
        end = time.mktime((__import__('datetime').datetime(year, month, last_day, 23, 59, 59)).timetuple())

        cursor = self._db.execute(
            "SELECT operation, COUNT(*), SUM(cost) FROM billing_records "
            "WHERE tenant_id = ? AND timestamp BETWEEN ? AND ? AND is_error = 0 "
            "GROUP BY operation",
            (tenant_id, start, end)
        )

        operations = {}
        total_usage_cost = 0.0
        for row in cursor.fetchall():
            op, count, cost = row
            operations[op] = {"count": count, "cost": round(cost or 0, 4)}
            total_usage_cost += (cost or 0)

        plan = self.get_plan(tenant_id)
        pricing = PLAN_PRICING.get(plan.value, {})
        monthly_fee = pricing.get("monthly_fee", 0)
        total = monthly_fee + total_usage_cost

        return {
            "tenant_id": tenant_id,
            "plan": plan.value,
            "period": f"{year}-{month:02d}",
            "monthly_fee": monthly_fee,
            "usage_cost": round(total_usage_cost, 4),
            "total": round(total, 2),
            "operations": operations,
        }

    def generate_invoice(self, tenant_id: str, year: int, month: int) -> dict:
        cost_data = self.calculate_monthly_cost(tenant_id, year, month)

        import calendar
        import time as _time
        start = _time.mktime((__import__('datetime').datetime(year, month, 1)).timetuple())
        last_day = calendar.monthrange(year, month)[1]
        end = _time.mktime((__import__('datetime').datetime(year, month, last_day, 23, 59, 59)).timetuple())

        import json
        self._db.execute(
            "INSERT INTO invoices (tenant_id, period_start, period_end, total_cost, operations_json, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (tenant_id, start, end, cost_data["total"], json.dumps(cost_data["operations"]), _time.time())
        )
        self._db.commit()

        cost_data["invoice_id"] = self._db.execute("SELECT last_insert_rowid()").fetchone()[0]
        return cost_data

    def close(self):
        self._flush_billing()
        self._db.close()
