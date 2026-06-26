from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import user_state


class UserStateTest(unittest.TestCase):
    def test_activity_state_is_saved_as_one_current_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_file = Path(temp_dir) / "state.json"
            previous_state_file = os.environ.get("XINYI_DRINK_STATE_FILE")
            os.environ["XINYI_DRINK_STATE_FILE"] = str(state_file)
            try:
                user_state.mark_activity_joined("15712459595")

                payload = json.loads(state_file.read_text(encoding="utf-8"))
                self.assertEqual(payload["mobile"], "15712459595")
                self.assertTrue(payload["activityJoined"])
                self.assertEqual(state_file.stat().st_mode & 0o777, 0o600)
                self.assertEqual(user_state.load_mobile(), "15712459595")
                self.assertTrue(user_state.load_activity_joined("15712459595"))
                self.assertIsNone(user_state.load_activity_joined("18888888888"))

                user_state.mark_activity_not_joined("18888888888")

                payload = json.loads(state_file.read_text(encoding="utf-8"))
                self.assertEqual(payload["mobile"], "18888888888")
                self.assertFalse(payload["activityJoined"])
                self.assertFalse(user_state.load_activity_joined("18888888888"))

                user_state.clear_mobile()

                payload = json.loads(state_file.read_text(encoding="utf-8"))
                self.assertIsNone(payload["mobile"])
                self.assertIsNone(payload["activityJoined"])
                self.assertIsNone(user_state.load_mobile())
            finally:
                if previous_state_file is None:
                    os.environ.pop("XINYI_DRINK_STATE_FILE", None)
                else:
                    os.environ["XINYI_DRINK_STATE_FILE"] = previous_state_file


if __name__ == "__main__":
    unittest.main()
