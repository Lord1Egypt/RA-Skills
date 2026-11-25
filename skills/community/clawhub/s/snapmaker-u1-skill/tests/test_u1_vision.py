"""Compile Apple's native CLI and check failures before Vision inference."""

from __future__ import annotations

import json
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "u1_vision.swift"


@unittest.skipUnless(platform.system() == "Darwin" and shutil.which("xcrun"), "requires macOS and the Swift toolchain")
class NativeVisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build_directory = tempfile.TemporaryDirectory(prefix="u1-vision-build-")
        cls.addClassCleanup(cls.build_directory.cleanup)
        cls.binary = Path(cls.build_directory.name) / "u1_vision"
        subprocess.run(["xcrun", "swiftc", "-O", "-parse-as-library", str(SOURCE), "-o", str(cls.binary), "-module-cache-path", "/private/tmp/u1-swift-cache"], check=True, capture_output=True, text=True, timeout=180)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="u1-vision-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.invalid = self.root / "invalid.jpg"
        self.invalid.write_bytes(b"not an image")
        self.output = self.root / "cutout.png"

    def execute(self, *arguments):
        result = subprocess.run([str(self.binary), *map(str, arguments)], text=True, capture_output=True, timeout=20, check=False)
        return result, json.loads(result.stdout)

    def test_help_is_json_and_identifies_real_engine(self):
        result, report = self.execute("--help")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["engine"], "Apple Vision")
        self.assertIn("--input", report["usage"])
        self.assertEqual(report["existing_files"], "refused")
        self.assertEqual(report["default_mode"], "foreground")
        self.assertEqual(report["modes"], ["foreground", "person"])

    def test_missing_unknown_and_repeated_arguments_are_json_errors(self):
        for arguments in [[], ["--input"], ["--wat"], ["--input", "a", "--input", "b", "--output", "c.png"], ["--input", "a", "--output", "c.png", "--mode", "cat"], ["--input", "a", "--output", "c.png", "--mode"]]:
            with self.subTest(arguments=arguments):
                result, report = self.execute(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report["status"], "error")
                self.assertEqual(report["code"], "invalid_arguments")

    def test_missing_file_and_invalid_image_do_not_write_output(self):
        result, report = self.execute("--input", self.root / "missing.jpg", "--output", self.output)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["code"], "missing_input")
        result, report = self.execute("--input", self.invalid, "--output", self.output)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["code"], "invalid_image")
        self.assertFalse(self.output.exists())
        self.assertEqual(self.invalid.read_bytes(), b"not an image")

    def test_person_mode_checks_input_without_starting_segmentation(self):
        result, report = self.execute("--input", self.invalid, "--output", self.output, "--mode", "person")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["code"], "invalid_image")
        self.assertFalse(self.output.exists())

    def test_original_and_report_path_collisions_are_refused(self):
        for arguments in [
            ["--input", self.invalid, "--output", self.invalid],
            ["--input", self.invalid, "--output", self.output, "--report", self.invalid],
            ["--input", self.invalid, "--output", self.output, "--report", self.output],
        ]:
            with self.subTest(arguments=arguments):
                result, report = self.execute(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report["code"], "path_collision")
        self.assertEqual(self.invalid.read_bytes(), b"not an image")

    def test_existing_outputs_and_reports_are_never_replaced(self):
        self.output.write_bytes(b"keep this output")
        result, report = self.execute("--input", self.invalid, "--output", self.output)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["code"], "output_exists")
        self.assertEqual(self.output.read_bytes(), b"keep this output")
        existing_report = self.root / "existing.json"
        existing_report.write_text('{"keep": true}')
        result, report = self.execute("--input", self.invalid, "--output", self.root / "new.png", "--report", existing_report)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["code"], "output_exists")
        self.assertEqual(json.loads(existing_report.read_text()), {"keep": True})

    def test_non_png_output_and_symlink_to_original_are_refused(self):
        result, report = self.execute("--input", self.invalid, "--output", self.root / "loses-alpha.jpg")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["code"], "invalid_arguments")
        link = self.root / "original-link.png"
        link.symlink_to(self.invalid)
        result, report = self.execute("--input", self.invalid, "--output", link)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["code"], "path_collision")


if __name__ == "__main__":
    unittest.main()
