import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from companion_runtime import CompanionRuntime, SESSION_SCHEMA_VERSION  # noqa: E402


class SessionSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "roles").mkdir(parents=True, exist_ok=True)
        (self.root / "state").mkdir(parents=True, exist_ok=True)
        (self.root / "references" / "presets").mkdir(parents=True, exist_ok=True)

        preset_src = Path(__file__).resolve().parents[1] / "references" / "presets" / "luoshui-v1.yaml"
        shutil.copy2(preset_src, self.root / "references" / "presets" / "luoshui-v1.yaml")

        legacy_session = {
            "initialized": True,
            "proactive": {
                "enabled": False,
                "frequency": "mid",
                "quiet_hours": None,
                "pause_until": "2026-04-03T10:00:00",
                "last_sent_at": "2026-04-03T09:00:00",
            },
            "context": {"freshness_hours": 72},
            "role": {"active": None, "draft": None},
            "last_user_input_at": "2026-04-03T09:30:00",
            "updated_at": "2026-04-03T09:30:00",
        }
        (self.root / "state" / "session.yaml").write_text(
            yaml.safe_dump(legacy_session, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_session_migration_adds_schema_and_pending_activation(self) -> None:
        runtime = CompanionRuntime(self.root)
        self.assertEqual(runtime.session["schema_version"], SESSION_SCHEMA_VERSION)
        self.assertIn("pending_activation", runtime.session["role"])

        pause_until = runtime.session["proactive"]["pause_until"]
        self.assertIsInstance(pause_until, str)
        self.assertIn("+", pause_until)

        persisted = yaml.safe_load((self.root / "state" / "session.yaml").read_text(encoding="utf-8"))
        self.assertEqual(persisted["schema_version"], SESSION_SCHEMA_VERSION)
        self.assertIn("pending_activation", persisted["role"])


if __name__ == "__main__":
    unittest.main()
