#!/usr/bin/env python3
"""Storage backends and shared models for seats-aero-monitor."""

from __future__ import annotations

import datetime as dt
import json
import os
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class WatcherConfig:
    id: str
    enabled: bool
    origin: str
    destination: str
    program: str | None
    airlines: list[str]
    cabins: list[str]
    seats_required: int
    window_days: int
    fixed_start_date: str | None
    fixed_end_date: str | None
    alert_new_only: bool
    enhanced_alert_on_seat_increase: bool
    notify_channel: str
    notify_target: str | None
    fetch_retries: int
    fetch_retry_delay_seconds: int


@dataclass
class AvailabilityRecord:
    watcher_id: str
    key: str
    date: str
    route: str
    cabin: str
    flight_no: str
    program: str
    seats: int
    miles: str | None
    taxes: str | None
    source_seen_at: str
    payload_hash: str
    raw: dict[str, Any]


@dataclass
class AlertEvent:
    watcher_id: str
    key: str
    alert_type: str
    record: AvailabilityRecord
    previous_seats: int | None


class Store(ABC):
    @abstractmethod
    def list_watchers(self, include_disabled: bool = False) -> list[WatcherConfig]: ...

    @abstractmethod
    def upsert_watchers(self, watchers: list[WatcherConfig], replace: bool = False) -> dict[str, int]: ...

    @abstractmethod
    def load_watcher_states(self, watcher_id: str) -> dict[str, dict[str, Any]]: ...

    @abstractmethod
    def upsert_available(self, record: AvailabilityRecord, observed_at: str, alerted: bool) -> None: ...

    @abstractmethod
    def mark_unseen_as_none(self, watcher_id: str, seen_keys: set[str], observed_at: str) -> int: ...

    @abstractmethod
    def close(self) -> None: ...


def _pick(dct: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in dct and dct[key] not in (None, ""):
            return dct[key]
    return None


def _to_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(str(value)))
        except (TypeError, ValueError):
            return None


def _normalize_fixed_date(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    try:
        parsed = dt.date.fromisoformat(text)
    except ValueError as exc:
        raise RuntimeError(f"Invalid fixed date `{text}` (expected YYYY-MM-DD).") from exc
    return parsed.isoformat()


def _iso_now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _default_state_db() -> str:
    """Return default db path from env or local data directory."""
    env_path = os.environ.get("SEATS_AERO_DB", "").strip()
    if env_path:
        return env_path
    skill_root = Path(__file__).resolve().parent.parent
    return str(skill_root / "data" / "monitor.db")


def _clean_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        if text.startswith("["):
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        return [item.strip() for item in text.split(",") if item.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _watcher_to_dict(watcher: WatcherConfig) -> dict[str, Any]:
    return asdict(
        WatcherConfig(
            id=str(watcher.id).strip(),
            enabled=bool(watcher.enabled),
            origin=str(watcher.origin).upper(),
            destination=str(watcher.destination).upper(),
            program=str(watcher.program).strip() or None if watcher.program is not None else None,
            airlines=[code.upper() for code in _clean_list(watcher.airlines)],
            cabins=[cab.lower() for cab in _clean_list(watcher.cabins) or ["business"]],
            seats_required=max(1, int(watcher.seats_required)),
            window_days=max(1, int(watcher.window_days)),
            fixed_start_date=_normalize_fixed_date(watcher.fixed_start_date),
            fixed_end_date=_normalize_fixed_date(watcher.fixed_end_date),
            alert_new_only=bool(watcher.alert_new_only),
            enhanced_alert_on_seat_increase=bool(watcher.enhanced_alert_on_seat_increase),
            notify_channel=str(watcher.notify_channel or "telegram"),
            notify_target=str(watcher.notify_target).strip() or None if watcher.notify_target is not None else None,
            fetch_retries=max(0, int(watcher.fetch_retries)),
            fetch_retry_delay_seconds=max(0, int(watcher.fetch_retry_delay_seconds)),
        )
    )


def _watcher_from_dict(data: dict[str, Any]) -> WatcherConfig:
    normalized = {
        "id": str(_pick(data, "id") or "").strip(),
        "enabled": bool(data.get("enabled", True)),
        "origin": str(_pick(data, "origin") or "").upper(),
        "destination": str(_pick(data, "destination") or "").upper(),
        "program": str(_pick(data, "program") or "").strip() or None,
        "airlines": [code.upper() for code in _clean_list(_pick(data, "airlines", "airlines_json"))],
        "cabins": [
            cab.lower()
            for cab in (_clean_list(_pick(data, "cabins", "cabins_json")) or ["business"])
        ],
        "seats_required": max(1, _to_int(_pick(data, "seats_required")) or 1),
        "window_days": max(1, _to_int(_pick(data, "window_days")) or 365),
        "fixed_start_date": _normalize_fixed_date(_pick(data, "fixed_start_date")),
        "fixed_end_date": _normalize_fixed_date(_pick(data, "fixed_end_date")),
        "alert_new_only": bool(data.get("alert_new_only", True)),
        "enhanced_alert_on_seat_increase": bool(data.get("enhanced_alert_on_seat_increase", False)),
        "notify_channel": str(_pick(data, "notify_channel") or "telegram"),
        "notify_target": str(_pick(data, "notify_target") or "").strip() or None,
        "fetch_retries": max(0, _to_int(_pick(data, "fetch_retries")) or 0),
        "fetch_retry_delay_seconds": max(0, _to_int(_pick(data, "fetch_retry_delay_seconds")) or 2),
    }
    return WatcherConfig(**normalized)


class SqliteStore(Store):
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        try:
            self._init_db()
        except sqlite3.OperationalError as exc:
            text = str(exc).lower()
            if "access permission denied" not in text and "unable to open database file" not in text:
                raise
            self.conn.close()
            sqlite_uri = f"file:{self.db_path.resolve().as_posix()}?mode=rwc&nolock=1"
            self.conn = sqlite3.connect(sqlite_uri, uri=True)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA journal_mode=OFF")
            self.conn.execute("PRAGMA synchronous=OFF")
            self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS watchers (
              id TEXT PRIMARY KEY,
              enabled INTEGER NOT NULL DEFAULT 1,
              origin TEXT NOT NULL,
              destination TEXT NOT NULL,
              program TEXT,
              airlines_json TEXT NOT NULL DEFAULT '[]',
              cabins_json TEXT NOT NULL DEFAULT '["business"]',
              seats_required INTEGER NOT NULL DEFAULT 1,
              window_days INTEGER NOT NULL DEFAULT 365,
              fixed_start_date TEXT,
              fixed_end_date TEXT,
              alert_new_only INTEGER NOT NULL DEFAULT 1,
              enhanced_alert_on_seat_increase INTEGER NOT NULL DEFAULT 0,
              notify_channel TEXT NOT NULL DEFAULT 'telegram',
              notify_target TEXT,
              fetch_retries INTEGER NOT NULL DEFAULT 0,
              fetch_retry_delay_seconds INTEGER NOT NULL DEFAULT 2,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )
        self._ensure_column(cur, "watchers", "fixed_start_date", "TEXT")
        self._ensure_column(cur, "watchers", "fixed_end_date", "TEXT")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS watcher_state (
              key TEXT PRIMARY KEY,
              watcher_id TEXT NOT NULL,
              availability_state TEXT NOT NULL,
              first_seen_at TEXT NOT NULL,
              last_seen_at TEXT NOT NULL,
              last_alert_at TEXT,
              last_payload_hash TEXT NOT NULL,
              seats INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_watchers_enabled ON watchers(enabled)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_watcher_state_watcher ON watcher_state(watcher_id)")
        self.conn.commit()

    @staticmethod
    def _ensure_column(cur: sqlite3.Cursor, table: str, column: str, definition: str) -> None:
        rows = cur.execute(f"PRAGMA table_info({table})").fetchall()
        names = {str(row[1]) for row in rows}
        if column not in names:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    @staticmethod
    def _row_to_watcher(row: sqlite3.Row) -> WatcherConfig:
        return _watcher_from_dict(dict(row))

    def list_watchers(self, include_disabled: bool = False) -> list[WatcherConfig]:
        cur = self.conn.cursor()
        if include_disabled:
            cur.execute("SELECT * FROM watchers ORDER BY id")
        else:
            cur.execute("SELECT * FROM watchers WHERE enabled=1 ORDER BY id")
        rows = cur.fetchall()
        return [self._row_to_watcher(row) for row in rows]

    def upsert_watchers(self, watchers: list[WatcherConfig], replace: bool = False) -> dict[str, int]:
        cur = self.conn.cursor()
        now = _iso_now()
        inserted = 0
        updated = 0

        if replace:
            cur.execute("DELETE FROM watchers")

        for watcher in watchers:
            existing = cur.execute("SELECT 1 FROM watchers WHERE id=?", (watcher.id,)).fetchone()
            if existing is None:
                inserted += 1
            else:
                updated += 1
            normalized = _watcher_to_dict(watcher)
            cur.execute(
                """
                INSERT INTO watchers (
                  id, enabled, origin, destination, program, airlines_json, cabins_json,
                  seats_required, window_days, fixed_start_date, fixed_end_date,
                  alert_new_only, enhanced_alert_on_seat_increase,
                  notify_channel, notify_target, fetch_retries, fetch_retry_delay_seconds,
                  created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                  enabled=excluded.enabled,
                  origin=excluded.origin,
                  destination=excluded.destination,
                  program=excluded.program,
                  airlines_json=excluded.airlines_json,
                  cabins_json=excluded.cabins_json,
                  seats_required=excluded.seats_required,
                  window_days=excluded.window_days,
                  fixed_start_date=excluded.fixed_start_date,
                  fixed_end_date=excluded.fixed_end_date,
                  alert_new_only=excluded.alert_new_only,
                  enhanced_alert_on_seat_increase=excluded.enhanced_alert_on_seat_increase,
                  notify_channel=excluded.notify_channel,
                  notify_target=excluded.notify_target,
                  fetch_retries=excluded.fetch_retries,
                  fetch_retry_delay_seconds=excluded.fetch_retry_delay_seconds,
                  updated_at=excluded.updated_at
                """,
                (
                    normalized["id"],
                    1 if normalized["enabled"] else 0,
                    normalized["origin"],
                    normalized["destination"],
                    normalized["program"],
                    json.dumps(normalized["airlines"], ensure_ascii=False),
                    json.dumps(normalized["cabins"], ensure_ascii=False),
                    normalized["seats_required"],
                    normalized["window_days"],
                    normalized["fixed_start_date"],
                    normalized["fixed_end_date"],
                    1 if normalized["alert_new_only"] else 0,
                    1 if normalized["enhanced_alert_on_seat_increase"] else 0,
                    normalized["notify_channel"],
                    normalized["notify_target"],
                    normalized["fetch_retries"],
                    normalized["fetch_retry_delay_seconds"],
                    now,
                    now,
                ),
            )

        self.conn.commit()
        return {
            "input": len(watchers),
            "inserted": inserted,
            "updated": updated,
            "replaced": 1 if replace else 0,
        }

    def load_watcher_states(self, watcher_id: str) -> dict[str, dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM watcher_state WHERE watcher_id = ?", (watcher_id,))
        rows = cur.fetchall()
        return {str(row["key"]): dict(row) for row in rows}

    def upsert_available(self, record: AvailabilityRecord, observed_at: str, alerted: bool) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO watcher_state (
              key, watcher_id, availability_state, first_seen_at, last_seen_at,
              last_alert_at, last_payload_hash, seats
            )
            VALUES (?, ?, 'available', ?, ?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
              availability_state='available',
              last_seen_at=excluded.last_seen_at,
              last_alert_at=CASE
                WHEN excluded.last_alert_at IS NOT NULL THEN excluded.last_alert_at
                ELSE watcher_state.last_alert_at
              END,
              last_payload_hash=excluded.last_payload_hash,
              seats=excluded.seats
            """,
            (
                record.key,
                record.watcher_id,
                observed_at,
                observed_at,
                observed_at if alerted else None,
                record.payload_hash,
                record.seats,
            ),
        )
        self.conn.commit()

    def mark_unseen_as_none(self, watcher_id: str, seen_keys: set[str], observed_at: str) -> int:
        cur = self.conn.cursor()
        placeholders = ",".join("?" for _ in seen_keys)
        if seen_keys:
            sql = (
                "UPDATE watcher_state "
                "SET availability_state='none', last_seen_at=?, seats=0 "
                f"WHERE watcher_id=? AND key NOT IN ({placeholders}) AND availability_state!='none'"
            )
            params = [observed_at, watcher_id, *sorted(seen_keys)]
        else:
            sql = (
                "UPDATE watcher_state "
                "SET availability_state='none', last_seen_at=?, seats=0 "
                "WHERE watcher_id=? AND availability_state!='none'"
            )
            params = [observed_at, watcher_id]
        cur.execute(sql, params)
        changed = cur.rowcount
        self.conn.commit()
        return changed

    def close(self) -> None:
        self.conn.close()


class JsonStore(Store):
    def __init__(self, json_path: Path):
        self.json_path = json_path
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _empty_data(self) -> dict[str, Any]:
        return {
            "version": 1,
            "updated_at": _iso_now(),
            "watchers": {},
            "watcher_state": {},
        }

    def _load(self) -> dict[str, Any]:
        if not self.json_path.exists():
            return self._empty_data()

        try:
            raw = json.loads(self.json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON state file: {self.json_path}") from exc
        if not isinstance(raw, dict):
            raise RuntimeError(f"JSON state file root must be an object: {self.json_path}")

        data = self._empty_data()
        data["version"] = int(_to_int(raw.get("version")) or 1)
        data["updated_at"] = str(raw.get("updated_at") or _iso_now())

        raw_watchers = raw.get("watchers", {})
        if isinstance(raw_watchers, dict):
            for watcher_id, payload in raw_watchers.items():
                if not isinstance(payload, dict):
                    continue
                watcher_data = dict(payload)
                watcher_data.setdefault("id", str(watcher_id))
                normalized = _watcher_to_dict(_watcher_from_dict(watcher_data))
                data["watchers"][normalized["id"]] = normalized

        raw_states = raw.get("watcher_state", {})
        if isinstance(raw_states, dict):
            for compound_key, payload in raw_states.items():
                if not isinstance(payload, dict):
                    continue
                state = self._normalize_state(compound_key=str(compound_key), payload=payload)
                data["watcher_state"][str(compound_key)] = state

        return data

    def _normalize_state(self, compound_key: str, payload: dict[str, Any]) -> dict[str, Any]:
        watcher_id = str(payload.get("watcher_id") or compound_key.split("|", 1)[0]).strip()
        now = _iso_now()
        return {
            "watcher_id": watcher_id,
            "availability_state": "available"
            if str(payload.get("availability_state") or "none").lower() == "available"
            else "none",
            "first_seen_at": str(payload.get("first_seen_at") or now),
            "last_seen_at": str(payload.get("last_seen_at") or now),
            "last_alert_at": str(payload.get("last_alert_at")) if payload.get("last_alert_at") is not None else None,
            "last_payload_hash": str(payload.get("last_payload_hash") or ""),
            "seats": max(0, _to_int(payload.get("seats")) or 0),
        }

    def _save(self) -> None:
        self.data["updated_at"] = _iso_now()
        temp_path = self.json_path.with_name(f"{self.json_path.name}.tmp")
        temp_path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temp_path.replace(self.json_path)

    def list_watchers(self, include_disabled: bool = False) -> list[WatcherConfig]:
        watchers = []
        for watcher_id in sorted(self.data["watchers"]):
            watcher = _watcher_from_dict(dict(self.data["watchers"][watcher_id]))
            if include_disabled or watcher.enabled:
                watchers.append(watcher)
        return watchers

    def upsert_watchers(self, watchers: list[WatcherConfig], replace: bool = False) -> dict[str, int]:
        if replace:
            self.data["watchers"] = {}

        inserted = 0
        updated = 0
        for watcher in watchers:
            if watcher.id in self.data["watchers"]:
                updated += 1
            else:
                inserted += 1
            normalized = _watcher_to_dict(watcher)
            self.data["watchers"][normalized["id"]] = normalized

        self._save()
        return {
            "input": len(watchers),
            "inserted": inserted,
            "updated": updated,
            "replaced": 1 if replace else 0,
        }

    def load_watcher_states(self, watcher_id: str) -> dict[str, dict[str, Any]]:
        states: dict[str, dict[str, Any]] = {}
        for compound_key, payload in self.data["watcher_state"].items():
            if str(payload.get("watcher_id")) != watcher_id:
                continue
            states[str(compound_key)] = dict(payload)
        return states

    def upsert_available(self, record: AvailabilityRecord, observed_at: str, alerted: bool) -> None:
        existing = dict(self.data["watcher_state"].get(record.key, {}))
        self.data["watcher_state"][record.key] = {
            "watcher_id": record.watcher_id,
            "availability_state": "available",
            "first_seen_at": str(existing.get("first_seen_at") or observed_at),
            "last_seen_at": observed_at,
            "last_alert_at": observed_at if alerted else existing.get("last_alert_at"),
            "last_payload_hash": record.payload_hash,
            "seats": record.seats,
        }
        self._save()

    def mark_unseen_as_none(self, watcher_id: str, seen_keys: set[str], observed_at: str) -> int:
        changed = 0
        for compound_key, payload in self.data["watcher_state"].items():
            if str(payload.get("watcher_id")) != watcher_id:
                continue
            if compound_key in seen_keys:
                continue
            if str(payload.get("availability_state")) == "none":
                continue
            payload["availability_state"] = "none"
            payload["last_seen_at"] = observed_at
            payload["seats"] = 0
            changed += 1
        self._save()
        return changed

    def close(self) -> None:
        return None
