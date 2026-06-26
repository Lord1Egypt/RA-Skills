import datetime as dt
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from heartbeat_bridge import ACK_TEXT, build_heartbeat_response  # noqa: E402
from proactive_scheduler import LOCAL_TZ  # noqa: E402


class HeartbeatBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "roles").mkdir(parents=True, exist_ok=True)
        (self.root / "state").mkdir(parents=True, exist_ok=True)
        (self.root / "references" / "presets").mkdir(parents=True, exist_ok=True)

        preset_src = Path(__file__).resolve().parents[1] / "references" / "presets" / "luoshui-v1.yaml"
        shutil.copy2(preset_src, self.root / "references" / "presets" / "luoshui-v1.yaml")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_returns_ack_when_proactive_is_disabled(self) -> None:
        session = {
            "initialized": True,
            "proactive": {
                "enabled": False,
                "frequency": "mid",
                "quiet_hours": None,
                "pause_until": None,
                "last_sent_at": None,
            },
            "context": {"freshness_hours": 72},
            "role": {"active": None, "draft": None, "pending_activation": None},
            "last_user_input_at": None,
            "updated_at": None,
            "schema_version": 1,
        }
        session_path = self.root / "state" / "session.yaml"
        session_path.write_text(yaml.safe_dump(session, sort_keys=False, allow_unicode=True), encoding="utf-8")

        payload = build_heartbeat_response(
            self.root,
            dt.datetime(2026, 4, 11, 10, 0, tzinfo=LOCAL_TZ),
        )

        self.assertFalse(payload["eligible"])
        self.assertEqual(payload["response_text"], ACK_TEXT)
        self.assertFalse(payload["marked_sent"])

    def test_marks_sent_when_eligible(self) -> None:
        session = {
            "initialized": True,
            "proactive": {
                "enabled": True,
                "frequency": "mid",
                "quiet_hours": None,
                "pause_until": None,
                "last_sent_at": None,
            },
            "context": {"freshness_hours": 72},
            "role": {"active": None, "draft": None, "pending_activation": None},
            "last_user_input_at": None,
            "updated_at": None,
            "schema_version": 1,
        }
        session_path = self.root / "state" / "session.yaml"
        session_path.write_text(yaml.safe_dump(session, sort_keys=False, allow_unicode=True), encoding="utf-8")

        now = dt.datetime(2026, 4, 11, 10, 0, tzinfo=LOCAL_TZ)
        payload = build_heartbeat_response(self.root, now, mark_delivered=True)
        persisted = yaml.safe_load(session_path.read_text(encoding="utf-8"))

        self.assertTrue(payload["eligible"])
        self.assertNotEqual(payload["response_text"], ACK_TEXT)
        self.assertTrue(payload["marked_sent"])
        self.assertEqual(
            persisted["proactive"]["last_sent_at"],
            now.isoformat(timespec="seconds"),
        )


if __name__ == "__main__":
    unittest.main()
