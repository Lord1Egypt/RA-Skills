"""SQLite store for tracking Zim service fees collected per booking.

Append-only ledger — one row per booking. Used for revenue reporting via
the admin API (GET /v1/admin/fees/summary).

Schema:
    booking_id     TEXT PK  — Zim request/booking ID
    tenant_id      TEXT     — Tenant the booking belongs to
    subtotal_usd   REAL     — Booking value before Zim fee
    fee_amount_usd REAL     — Zim service fee charged
    fee_type       TEXT     — flat / percentage / flat_plus_percentage
    created_at     TEXT     — ISO-8601 UTC timestamp
"""

from __future__ import annotations

import logging
import sqlite3
from datetime import UTC, datetime
from typing import Optional

logger = logging.getLogger(__name__)


class FeeStore:
    """Persistent SQLite store for fee records."""

    def __init__(self, db_path: str = "/tmp/zim_fees.db") -> None:
        self._db = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self._db) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS fees (
                    booking_id     TEXT PRIMARY KEY,
                    tenant_id      TEXT NOT NULL,
                    subtotal_usd   REAL NOT NULL,
                    fee_amount_usd REAL NOT NULL,
                    fee_type       TEXT NOT NULL,
                    created_at     TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_fees_tenant ON fees(tenant_id)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_fees_created ON fees(created_at)"
            )
            conn.commit()

    def record_fee(
        self,
        booking_id: str,
        tenant_id: str,
        subtotal_usd: float,
        fee_amount_usd: float,
        fee_type: str,
    ) -> None:
        """Record a service fee collected for a booking.

        Uses INSERT OR REPLACE so re-executing a booking is idempotent.
        """
        created_at = datetime.now(UTC).isoformat()
        with sqlite3.connect(self._db) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO fees
                    (booking_id, tenant_id, subtotal_usd, fee_amount_usd, fee_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (booking_id, tenant_id, subtotal_usd, fee_amount_usd, fee_type, created_at),
            )
            conn.commit()
        logger.info(
            "Recorded fee for booking %s: $%.2f service fee on $%.2f subtotal",
            booking_id, fee_amount_usd, subtotal_usd,
        )

    def get_summary(
        self,
        tenant_id: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> dict:
        """Return aggregate fee revenue statistics.

        Args:
            tenant_id: Filter to a single tenant (optional).
            since:     ISO-8601 lower bound on created_at (optional).
            until:     ISO-8601 upper bound on created_at (optional).

        Returns:
            Dict with booking_count, total_fees_usd, total_subtotal_usd,
            avg_fee_usd, and per-fee-type breakdown.
        """
        where_clauses: list[str] = []
        params: list = []

        if tenant_id:
            where_clauses.append("tenant_id = ?")
            params.append(tenant_id)
        if since:
            where_clauses.append("created_at >= ?")
            params.append(since)
        if until:
            where_clauses.append("created_at <= ?")
            params.append(until)

        where = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        with sqlite3.connect(self._db) as conn:
            row = conn.execute(
                f"""
                SELECT
                    COUNT(*)                          AS booking_count,
                    COALESCE(SUM(fee_amount_usd), 0)  AS total_fees_usd,
                    COALESCE(SUM(subtotal_usd), 0)    AS total_subtotal_usd,
                    COALESCE(AVG(fee_amount_usd), 0)  AS avg_fee_usd
                FROM fees {where}
                """,
                params,
            ).fetchone()

            breakdown_rows = conn.execute(
                f"""
                SELECT fee_type, COUNT(*) AS count, COALESCE(SUM(fee_amount_usd), 0) AS fees
                FROM fees {where}
                GROUP BY fee_type
                """,
                params,
            ).fetchall()

        return {
            "booking_count": row[0],
            "total_fees_usd": round(row[1], 2),
            "total_subtotal_usd": round(row[2], 2),
            "avg_fee_usd": round(row[3], 2),
            "by_fee_type": [
                {"fee_type": r[0], "count": r[1], "total_fees_usd": round(r[2], 2)}
                for r in breakdown_rows
            ],
        }

    def list_fees(
        self,
        tenant_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        """List individual fee records, newest first."""
        where_clauses: list[str] = []
        params: list = []

        if tenant_id:
            where_clauses.append("tenant_id = ?")
            params.append(tenant_id)

        where = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        params.extend([limit, offset])

        with sqlite3.connect(self._db) as conn:
            rows = conn.execute(
                f"""
                SELECT booking_id, tenant_id, subtotal_usd, fee_amount_usd, fee_type, created_at
                FROM fees {where}
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
                """,
                params,
            ).fetchall()

        return [
            {
                "booking_id": r[0],
                "tenant_id": r[1],
                "subtotal_usd": r[2],
                "fee_amount_usd": r[3],
                "fee_type": r[4],
                "created_at": r[5],
            }
            for r in rows
        ]
