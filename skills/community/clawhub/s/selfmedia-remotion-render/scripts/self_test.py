from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_render_request import RequestError, load_request

ROOT = Path(__file__).resolve().parents[1]


class RenderRequestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / "project"
        (self.workspace / "src").mkdir(parents=True)
        (self.workspace / "out").mkdir()
        (self.workspace / "package.json").write_text(json.dumps({"dependencies": {"remotion": "4.x"}}))
        (self.workspace / "src/index.tsx").write_text("entry")
        (self.workspace / "src/Root.tsx").write_text("component")
        self.request_path = self.root / "request.json"
        self.request = {
            "workspace": "project", "entry_point": "src/index.tsx", "composition_id": "Sample",
            "output_path": "out/sample.mp4", "width": 1080, "height": 1920, "fps": 30,
            "codec": "h264", "input_files": ["src/Root.tsx"],
        }

    def save_and_validate(self, request: dict) -> None:
        self.request_path.write_text(json.dumps(request), encoding="utf-8")
        load_request(self.request_path)

    def test_valid_user_supplied_workspace_and_inputs_pass(self) -> None:
        self.save_and_validate(self.request)

    def test_existing_output_is_never_overwritten(self) -> None:
        (self.workspace / "out/sample.mp4").write_bytes(b"existing")
        with self.assertRaisesRegex(RequestError, "prevent overwrite"):
            self.save_and_validate(self.request)

    def test_input_path_traversal_is_rejected(self) -> None:
        request = copy.deepcopy(self.request)
        request["input_files"] = ["../outside.tsx"]
        with self.assertRaisesRegex(RequestError, "relative path inside the workspace"):
            self.save_and_validate(request)

    def test_missing_remotion_dependency_is_rejected(self) -> None:
        (self.workspace / "package.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(RequestError, "declare the remotion dependency"):
            self.save_and_validate(self.request)

    def test_missing_input_is_reported(self) -> None:
        request = copy.deepcopy(self.request)
        request["input_files"] = ["src/missing.tsx"]
        with self.assertRaisesRegex(RequestError, "input file does not exist"):
            self.save_and_validate(request)

    def test_windows_separator_is_rejected_for_portable_relative_paths(self) -> None:
        request = copy.deepcopy(self.request)
        request["input_files"] = [r"src\..\outside.tsx"]
        with self.assertRaisesRegex(RequestError, "relative path inside the workspace"):
            self.save_and_validate(request)


if __name__ == "__main__":
    unittest.main()
