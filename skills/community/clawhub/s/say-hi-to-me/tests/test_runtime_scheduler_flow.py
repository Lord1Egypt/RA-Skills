import datetime as dt
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from companion_runtime import CompanionRuntime  # noqa: E402
from proactive_scheduler import LOCAL_TZ, evaluate  # noqa: E402


class RuntimeSchedulerFlowTests(unittest.TestCase):
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

    def test_save_requires_confirm_and_scheduler_rules(self) -> None:
        runtime = CompanionRuntime(self.root)
        runtime.handle("帮我初始化一下")
        runtime.handle("/hi 角色 模板 luoshui")

        save_result = runtime.handle("/hi 角色 保存 洛水")
        self.assertEqual(save_result["intent"], "role_save")
        self.assertIsNone(save_result["session"]["role"]["active"])
        pending = save_result["session"]["role"]["pending_activation"]
        self.assertIsInstance(pending, str)
        self.assertTrue(pending.endswith("洛水.yaml"))

        confirm_result = runtime.handle("/hi 角色 确认")
        self.assertEqual(confirm_result["intent"], "role_confirm_activation")
        self.assertTrue(confirm_result["session"]["role"]["active"].endswith("洛水.yaml"))

        runtime.handle("/hi 开")
        runtime.handle("/hi 免打扰 22:00-08:00")
        night = dt.datetime(2026, 4, 3, 22, 30, tzinfo=LOCAL_TZ)
        quiet = evaluate(self.root, night)
        self.assertEqual(quiet["reason"], "quiet_hours")

        session_path = self.root / "state" / "session.yaml"
        session = yaml.safe_load(session_path.read_text(encoding="utf-8"))
        session["proactive"]["quiet_hours"] = None
        session["proactive"]["pause_until"] = None
        session["proactive"]["frequency"] = "mid"
        session["proactive"]["last_sent_at"] = (night - dt.timedelta(hours=1)).isoformat(timespec="seconds")
        session_path.write_text(yaml.safe_dump(session, sort_keys=False, allow_unicode=True), encoding="utf-8")

        cooldown = evaluate(self.root, night)
        self.assertEqual(cooldown["reason"], "cooldown")


if __name__ == "__main__":
    unittest.main()
