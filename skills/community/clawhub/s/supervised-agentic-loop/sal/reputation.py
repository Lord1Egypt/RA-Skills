"""Reputation scoring — EMA-based agent reputation with SQLite persistence.

Standalone reimplementation inspired by governed-agents reputation system.
"""

import os
import sqlite3
import time
from pathlib import Path
from typing import Optional


# Scoring constants
SCORE_FIRST_PASS = 1.0       # Success on first try (keep)
SCORE_RETRY_PASS = 0.7       # Success after retries
SCORE_HONEST_BLOCK = 0.5     # Agent reported blocker honestly
SCORE_NO_CHANGE = 0.0        # No improvement (discard)
SCORE_CRASH = 0.0            # Honest crash (not hallucination)
SCORE_HALLUCINATION = -1.0   # Claimed success but gates failed

ALPHA = 0.1  # EMA learning rate
DEFAULT_REPUTATION = 0.7  # Starting reputation for new agents


def _resolve_db_path(db_path: Optional[str] = None) -> Path:
    """Resolve DB path with fallback."""
    if db_path:
        return Path(db_path)
    env = os.environ.get("SAL_DB_PATH")
    if env:
        return Path(env)
    return Path(".state") / "reputation.db"


class ReputationDB:
    """SQLite-backed EMA reputation scoring.

    Tracks agent performance across iterations. Agents with low
    reputation get suspended (auto-brake).
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        resolved = _resolve_db_path(db_path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = resolved
        self.conn = sqlite3.connect(str(resolved))
        self._init_tables()

    def _init_tables(self) -> None:
        """Create tables if they don't exist."""
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                reputation REAL DEFAULT 0.7,
                total_iterations INTEGER DEFAULT 0,
                keeps INTEGER DEFAULT 0,
                discards INTEGER DEFAULT 0,
                crashes INTEGER DEFAULT 0,
                suspended INTEGER DEFAULT 0,
                suspension_reason TEXT,
                created_at REAL,
                updated_at REAL
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS iteration_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT,
                iteration INTEGER,
                score REAL,
                status TEXT,
                reputation_before REAL,
                reputation_after REAL,
                hypothesis TEXT,
                details TEXT,
                timestamp REAL
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT,
                action TEXT,
                reason TEXT,
                reputation_before REAL,
                reputation_after REAL,
                timestamp REAL
            )
        """)
        self.conn.commit()

    def get_score(self, agent_id: str) -> float:
        """Get current reputation score."""
        row = self.conn.execute(
            "SELECT reputation FROM agents WHERE agent_id = ?", (agent_id,)
        ).fetchone()
        return row[0] if row else DEFAULT_REPUTATION

    def update(
        self,
        agent_id: str,
        iteration: int,
        score: float,
        status: str = "unknown",
        hypothesis: str = "",
        details: str = "",
    ) -> dict:
        """Update reputation via EMA.

        R_new = (1 - α) × R_old + α × score

        Returns:
            Dict with reputation_before, reputation_after, delta.
        """
        now = time.time()
        old_rep = self.get_score(agent_id)

        # EMA update
        new_rep = (1 - ALPHA) * old_rep + ALPHA * score
        new_rep = max(-1.0, min(1.0, new_rep))

        # Upsert agent
        row = self.conn.execute(
            "SELECT agent_id FROM agents WHERE agent_id = ?", (agent_id,)
        ).fetchone()

        if row:
            # Update counters based on status
            counter_col = {
                "keep": "keeps", "discard": "discards",
                "crash": "crashes", "error": "crashes",
            }.get(status, "discards")

            self.conn.execute(
                f"UPDATE agents SET reputation=?, total_iterations=total_iterations+1, "
                f"{counter_col}={counter_col}+1, updated_at=? WHERE agent_id=?",
                (new_rep, now, agent_id),
            )
        else:
            self.conn.execute("""
                INSERT INTO agents (agent_id, reputation, total_iterations,
                keeps, discards, crashes, created_at, updated_at)
                VALUES (?, ?, 1, ?, ?, ?, ?, ?)
            """, (
                agent_id, new_rep,
                1 if status == "keep" else 0,
                1 if status == "discard" else 0,
                1 if status in ("crash", "error") else 0,
                now, now,
            ))

        # Log iteration
        self.conn.execute("""
            INSERT INTO iteration_log (agent_id, iteration, score, status,
            reputation_before, reputation_after, hypothesis, details, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (agent_id, iteration, score, status, old_rep, new_rep,
              hypothesis, details, now))

        self.conn.commit()

        return {
            "agent_id": agent_id,
            "reputation_before": round(old_rep, 4),
            "reputation_after": round(new_rep, 4),
            "delta": round(new_rep - old_rep, 4),
            "score": score,
        }

    def get_level(self, agent_id: str) -> dict:
        """Determine supervision level from reputation.

        Levels:
            > 0.8  → autonomous
            > 0.6  → standard
            > 0.4  → supervised
            > 0.2  → strict
            ≤ 0.2  → suspended
        """
        rep = self.get_score(agent_id)
        if rep > 0.8:
            level = "autonomous"
        elif rep > 0.6:
            level = "standard"
        elif rep > 0.4:
            level = "supervised"
        elif rep > 0.2:
            level = "strict"
        else:
            level = "suspended"

        return {"level": level, "reputation": round(rep, 4)}

    def suspend(self, agent_id: str, reason: str) -> None:
        """Suspend an agent with audit trail."""
        now = time.time()
        rep = self.get_score(agent_id)
        self.conn.execute(
            "UPDATE agents SET suspended=1, suspension_reason=?, updated_at=? "
            "WHERE agent_id=?",
            (reason, now, agent_id),
        )
        self.conn.execute("""
            INSERT INTO audit_log (agent_id, action, reason,
            reputation_before, reputation_after, timestamp)
            VALUES (?, 'suspend', ?, ?, ?, ?)
        """, (agent_id, reason, rep, rep, now))
        self.conn.commit()

    def unsuspend(self, agent_id: str, reason: str) -> dict:
        """Unsuspend an agent — human-only, with audit trail.

        Resets reputation to 0.5 (neutral prior).
        """
        now = time.time()
        old_rep = self.get_score(agent_id)
        new_rep = 0.5

        self.conn.execute(
            "UPDATE agents SET suspended=0, suspension_reason=NULL, "
            "reputation=?, updated_at=? WHERE agent_id=?",
            (new_rep, now, agent_id),
        )
        self.conn.execute("""
            INSERT INTO audit_log (agent_id, action, reason,
            reputation_before, reputation_after, timestamp)
            VALUES (?, 'unsuspend', ?, ?, ?, ?)
        """, (agent_id, reason, old_rep, new_rep, now))
        self.conn.commit()

        return {
            "agent_id": agent_id,
            "reputation_before": round(old_rep, 4),
            "reputation_after": new_rep,
            "action": "unsuspend",
            "reason": reason,
        }

    def get_history(self, agent_id: str, limit: int = 20) -> list[dict]:
        """Get recent iteration history."""
        rows = self.conn.execute(
            "SELECT iteration, score, status, reputation_before, reputation_after, "
            "hypothesis, timestamp FROM iteration_log "
            "WHERE agent_id=? ORDER BY timestamp DESC LIMIT ?",
            (agent_id, limit),
        ).fetchall()
        cols = ["iteration", "score", "status", "reputation_before",
                "reputation_after", "hypothesis", "timestamp"]
        return [dict(zip(cols, row)) for row in rows]

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()
