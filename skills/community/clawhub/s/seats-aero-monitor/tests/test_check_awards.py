#!/usr/bin/env python3
"""Tests for seats-aero-monitor."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_awards import (  # type: ignore  # noqa: E402
    _resolve_watchers,
    _watcher_date_window,
    load_watchers,
    normalize_records,
    process_watcher_records,
    select_watchers,
)
from store import JsonStore, SqliteStore, WatcherConfig  # type: ignore  # noqa: E402


def make_watcher(**kwargs):
    base = dict(
        id="ana_sfo_hnd",
        enabled=True,
        origin="SFO",
        destination="HND",
        program="aeroplan",
        airlines=["NH"],
        cabins=["business", "first"],
        seats_required=1,
        window_days=365,
        fixed_start_date=None,
        fixed_end_date=None,
        alert_new_only=True,
        enhanced_alert_on_seat_increase=False,
        notify_channel="telegram",
        notify_target="your-chat-id",
        fetch_retries=0,
        fetch_retry_delay_seconds=0,
    )
    base.update(kwargs)
    return WatcherConfig(**base)


class CheckAwardsTests(unittest.TestCase):
    def test_normalize_handles_missing_and_multisegment(self):
        watcher = make_watcher()
        raw_items = [
            {
                "availabilitySegments": [
                    {
                        "origin": "SFO",
                        "destination": "HND",
                        "flightNumber": "NH107",
                        "cabin": "business",
                        "seats": 2,
                    }
                ],
                "Date": "2026-06-01T00:00:00Z",
                "source": "aeroplan",
            },
            {"origin": "SFO", "destination": "HND"},
        ]
        out = normalize_records(raw_items, watcher, observed_at="2026-01-01T00:00:00+00:00")
        self.assertEqual(1, len(out))
        self.assertEqual("2026-06-01", out[0].date)
        self.assertEqual("SFO->HND", out[0].route)
        self.assertEqual("NH107", out[0].flight_no)

    def test_new_only_is_idempotent(self):
        watcher = make_watcher(alert_new_only=True)
        raw_items = [
            {
                "date": "2026-06-01",
                "origin": "SFO",
                "destination": "HND",
                "cabin": "business",
                "flightNumber": "NH7",
                "seats": 2,
                "source": "aeroplan",
            }
        ]
        with tempfile.TemporaryDirectory() as td:
            store = SqliteStore(Path(td) / "state.db")
            records = normalize_records(raw_items, watcher, observed_at="2026-01-01T00:00:00+00:00")
            alerts1, _ = process_watcher_records(
                watcher, records, store, observed_at="2026-01-01T00:00:00+00:00"
            )
            alerts2, _ = process_watcher_records(
                watcher, records, store, observed_at="2026-01-01T00:05:00+00:00"
            )
            self.assertEqual(1, len(alerts1))
            self.assertEqual(0, len(alerts2))

    def test_config_parse_and_disabled_watcher_skip(self):
        cfg = {
            "defaults": {"cabins": ["business"], "window_days": 180},
            "watchers": [
                {
                    "id": "disabled_one",
                    "enabled": False,
                    "origin": "SFO",
                    "destination": "HND",
                },
                {
                    "id": "enabled_one",
                    "enabled": True,
                    "origin": "SFO",
                    "destination": "HND",
                    "program": "united",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as td:
            cfg_path = Path(td) / "watchers.yaml"
            cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
            watchers = load_watchers(cfg_path)
            selected = select_watchers(watchers, watcher_id=None)
            self.assertEqual(1, len(selected))
            self.assertEqual("enabled_one", selected[0].id)

    def test_integration_lifecycle_fixture(self):
        watcher = make_watcher()
        steps = json.loads((ROOT / "tests" / "fixtures" / "lifecycle.json").read_text(encoding="utf-8"))
        total_alerts = 0
        with tempfile.TemporaryDirectory() as td:
            store = SqliteStore(Path(td) / "state.db")
            for idx, raw_items in enumerate(steps):
                now = f"2026-01-01T00:0{idx}:00+00:00"
                records = normalize_records(raw_items, watcher, observed_at=now)
                alerts, _ = process_watcher_records(watcher, records, store, observed_at=now)
                total_alerts += len(alerts)
        self.assertEqual(2, total_alerts)

    def test_watchers_import_and_auto_resolution_prefers_db(self):
        cfg = {
            "watchers": [
                {
                    "id": "cfg_one",
                    "enabled": True,
                    "origin": "SFO",
                    "destination": "HND",
                    "program": "aeroplan",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as td:
            config_path = Path(td) / "watchers.yaml"
            config_path.write_text(json.dumps(cfg), encoding="utf-8")
            store = SqliteStore(Path(td) / "state.db")

            imported = store.upsert_watchers(load_watchers(config_path), replace=True)
            self.assertEqual(1, imported["input"])
            self.assertEqual(1, imported["inserted"])

            cfg2 = {
                "watchers": [
                    {
                        "id": "cfg_two",
                        "enabled": True,
                        "origin": "SFO",
                        "destination": "NRT",
                    }
                ]
            }
            config_path.write_text(json.dumps(cfg2), encoding="utf-8")
            watchers, source = _resolve_watchers(
                store=store,
                watchers_source="auto",
                config_path=config_path,
                watcher_id=None,
            )
            self.assertEqual("db", source)
            self.assertEqual(1, len(watchers))
            self.assertEqual("cfg_one", watchers[0].id)

    def test_json_store_persists_watchers_and_state(self):
        watcher = make_watcher()
        raw_items = [
            {
                "date": "2026-06-01",
                "origin": "SFO",
                "destination": "HND",
                "cabin": "business",
                "flightNumber": "NH7",
                "seats": 2,
                "source": "aeroplan",
            }
        ]
        with tempfile.TemporaryDirectory() as td:
            state_path = Path(td) / "state.json"
            store = JsonStore(state_path)
            imported = store.upsert_watchers([watcher], replace=True)
            self.assertEqual(1, imported["inserted"])

            now = "2026-01-01T00:00:00+00:00"
            records = normalize_records(raw_items, watcher, observed_at=now)
            alerts1, _ = process_watcher_records(watcher, records, store, observed_at=now)
            self.assertEqual(1, len(alerts1))
            store.close()

            reopened = JsonStore(state_path)
            watchers = reopened.list_watchers()
            self.assertEqual(1, len(watchers))
            self.assertEqual(watcher.id, watchers[0].id)
            alerts2, _ = process_watcher_records(
                watcher,
                records,
                reopened,
                observed_at="2026-01-01T00:05:00+00:00",
            )
            self.assertEqual(0, len(alerts2))

            payload = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertIn("watchers", payload)
            self.assertIn("watcher_state", payload)

    def test_fixed_date_range_and_single_date(self):
        watcher_month = make_watcher(
            fixed_start_date="2026-08-01",
            fixed_end_date="2026-08-31",
            window_days=10,
        )
        start, end = _watcher_date_window(watcher_month)
        self.assertEqual("2026-08-01", start)
        self.assertEqual("2026-08-31", end)

        watcher_day = make_watcher(fixed_start_date="2026-08-15", fixed_end_date="2026-08-15")
        start2, end2 = _watcher_date_window(watcher_day)
        self.assertEqual("2026-08-15", start2)
        self.assertEqual("2026-08-15", end2)

        raw_items = [
            {
                "date": "2026-08-10",
                "origin": "SFO",
                "destination": "HND",
                "cabin": "business",
                "flightNumber": "NH7",
                "seats": 2,
                "source": "aeroplan",
            },
            {
                "date": "2026-09-01",
                "origin": "SFO",
                "destination": "HND",
                "cabin": "business",
                "flightNumber": "NH9",
                "seats": 2,
                "source": "aeroplan",
            },
        ]
        normalized = normalize_records(
            raw_items,
            watcher_month,
            observed_at="2026-01-01T00:00:00+00:00",
        )
        self.assertEqual(1, len(normalized))
        self.assertEqual("2026-08-10", normalized[0].date)


if __name__ == "__main__":
    unittest.main()
