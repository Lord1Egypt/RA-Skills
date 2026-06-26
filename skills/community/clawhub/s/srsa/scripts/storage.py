import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


class Storage:
    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

    @staticmethod
    def _utc_now() -> datetime:
        return datetime.now(timezone.utc)

    @classmethod
    def _utc_now_iso(cls) -> str:
        return cls._utc_now().isoformat()

    @classmethod
    def _utc_day_bounds(
        cls, reference: datetime | None = None
    ) -> tuple[datetime, datetime]:
        now = reference.astimezone(timezone.utc) if reference else cls._utc_now()
        start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        end = start + timedelta(days=1)
        return start, end

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    card_json TEXT NOT NULL,
                    due_ts REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    deleted_at TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_cards_due_ts
                ON cards (due_ts);

                CREATE INDEX IF NOT EXISTS idx_cards_deleted_due
                ON cards (deleted_at, due_ts);

                CREATE TABLE IF NOT EXISTS review_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_id INTEGER NOT NULL,
                    rating TEXT NOT NULL,
                    review_datetime TEXT NOT NULL,
                    review_log_json TEXT NOT NULL,
                    retrievability_before REAL NOT NULL,
                    retrievability_after REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (card_id) REFERENCES cards(id)
                );

                CREATE INDEX IF NOT EXISTS idx_review_logs_card_id
                ON review_logs (card_id);

                CREATE INDEX IF NOT EXISTS idx_review_logs_review_datetime
                ON review_logs (review_datetime);

                CREATE TABLE IF NOT EXISTS review_state (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    current_card_id INTEGER,
                    answer_shown INTEGER NOT NULL CHECK (answer_shown IN (0, 1)),
                    rated INTEGER NOT NULL CHECK (rated IN (0, 1)),
                    updated_at TEXT NOT NULL
                );
                """
            )

            existing = connection.execute(
                "SELECT id FROM review_state WHERE id = 1"
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO review_state (id, current_card_id, answer_shown, rated, updated_at)
                    VALUES (1, NULL, 0, 1, ?)
                    """,
                    (self._utc_now_iso(),),
                )

    def create_card(
        self, question: str, answer: str, card_json: str, due_ts: float
    ) -> int:
        now_iso = self._utc_now_iso()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO cards (question, answer, card_json, due_ts, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (question, answer, card_json, due_ts, now_iso, now_iso),
            )
            inserted_id = cursor.lastrowid
            if inserted_id is None:
                raise RuntimeError("Failed to create card: missing lastrowid")
            return int(inserted_id)

    def get_card(
        self, card_id: int, include_deleted: bool = False
    ) -> dict[str, Any] | None:
        query = "SELECT * FROM cards WHERE id = ?"
        args: tuple[Any, ...] = (card_id,)
        if not include_deleted:
            query += " AND deleted_at IS NULL"

        with self._connect() as connection:
            row = connection.execute(query, args).fetchone()
            return dict(row) if row else None

    def override_card(
        self,
        card_id: int,
        question: str,
        answer: str,
        card_json: str,
        due_ts: float,
    ) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE cards
                SET question = ?, answer = ?, card_json = ?, due_ts = ?, updated_at = ?
                WHERE id = ? AND deleted_at IS NULL
                """,
                (question, answer, card_json, due_ts, self._utc_now_iso(), card_id),
            )
            return cursor.rowcount > 0

    def soft_delete_card(self, card_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE cards
                SET deleted_at = ?, updated_at = ?
                WHERE id = ? AND deleted_at IS NULL
                """,
                (self._utc_now_iso(), self._utc_now_iso(), card_id),
            )
            return cursor.rowcount > 0

    def get_next_due_card(self, now_ts: float | None = None) -> dict[str, Any] | None:
        effective_now = now_ts if now_ts is not None else self._utc_now().timestamp()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM cards
                WHERE deleted_at IS NULL AND due_ts <= ?
                ORDER BY due_ts ASC, id ASC
                LIMIT 1
                """,
                (effective_now,),
            ).fetchone()
            return dict(row) if row else None

    def update_card_schedule(self, card_id: int, card_json: str, due_ts: float) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE cards
                SET card_json = ?, due_ts = ?, updated_at = ?
                WHERE id = ? AND deleted_at IS NULL
                """,
                (card_json, due_ts, self._utc_now_iso(), card_id),
            )

    def append_review_log(
        self,
        card_id: int,
        rating: str,
        review_datetime: str,
        review_log_json: str,
        retrievability_before: float,
        retrievability_after: float,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO review_logs (
                    card_id,
                    rating,
                    review_datetime,
                    review_log_json,
                    retrievability_before,
                    retrievability_after,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    card_id,
                    rating,
                    review_datetime,
                    review_log_json,
                    retrievability_before,
                    retrievability_after,
                    self._utc_now_iso(),
                ),
            )

    def get_review_state(self) -> dict[str, Any]:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT current_card_id, answer_shown, rated
                FROM review_state
                WHERE id = 1
                """
            ).fetchone()

        if row is None:
            return {"current_card_id": None, "answer_shown": False, "rated": True}

        return {
            "current_card_id": row["current_card_id"],
            "answer_shown": bool(row["answer_shown"]),
            "rated": bool(row["rated"]),
        }

    def set_review_state(
        self, current_card_id: int | None, answer_shown: bool, rated: bool
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE review_state
                SET current_card_id = ?, answer_shown = ?, rated = ?, updated_at = ?
                WHERE id = 1
                """,
                (
                    current_card_id,
                    int(answer_shown),
                    int(rated),
                    self._utc_now_iso(),
                ),
            )

    def count_active_cards(self) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM cards WHERE deleted_at IS NULL"
            ).fetchone()
            return int(row["total"])

    def count_due_cards_now(self, now_ts: float | None = None) -> int:
        effective_now = now_ts if now_ts is not None else self._utc_now().timestamp()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM cards
                WHERE deleted_at IS NULL AND due_ts <= ?
                """,
                (effective_now,),
            ).fetchone()
            return int(row["total"])

    def count_reviewed_today(self, reference: datetime | None = None) -> int:
        start, end = self._utc_day_bounds(reference)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM review_logs
                WHERE review_datetime >= ? AND review_datetime < ?
                """,
                (start.isoformat(), end.isoformat()),
            ).fetchone()
            return int(row["total"])

    def count_due_cards_in_day(self, day_start: datetime) -> int:
        day_end = day_start + timedelta(days=1)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM cards
                WHERE deleted_at IS NULL
                  AND due_ts >= ?
                  AND due_ts < ?
                """,
                (day_start.timestamp(), day_end.timestamp()),
            ).fetchone()
            return int(row["total"])

    def due_counts_next_days(
        self, days: int = 7, reference: datetime | None = None
    ) -> list[tuple[str, int]]:
        start, _ = self._utc_day_bounds(reference)
        results: list[tuple[str, int]] = []

        for offset in range(days):
            day_start = start + timedelta(days=offset)
            count = self.count_due_cards_in_day(day_start)
            results.append((day_start.date().isoformat(), count))

        return results

    def list_active_card_payloads(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, card_json FROM cards WHERE deleted_at IS NULL"
            ).fetchall()
            return [dict(row) for row in rows]

    def get_card_history_stats(self, card_id: int) -> tuple[int, int]:
        with self._connect() as connection:
            total_row = connection.execute(
                "SELECT COUNT(*) AS total FROM review_logs WHERE card_id = ?",
                (card_id,),
            ).fetchone()
            correct_row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM review_logs
                WHERE card_id = ? AND rating != 'again'
                """,
                (card_id,),
            ).fetchone()

        total = int(total_row["total"]) if total_row else 0
        correct = int(correct_row["total"]) if correct_row else 0
        return total, correct
