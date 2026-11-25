"""Native Object Capture argument/data guards; never launch reconstruction."""

from __future__ import annotations

import base64
import json
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "u1_capture.swift"
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=")


@unittest.skipUnless(platform.system() == "Darwin" and shutil.which("xcrun"), "requires macOS and Swift")
class NativeCaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = tempfile.TemporaryDirectory(prefix="u1-capture-build-")
        cls.addClassCleanup(cls.build.cleanup)
        cls.binary = Path(cls.build.name) / "u1_capture"
        subprocess.run(["xcrun", "swiftc", "-O", "-parse-as-library", str(SOURCE), "-o", str(cls.binary), "-module-cache-path", "/private/tmp/u1-swift-cache"], check=True, capture_output=True, text=True, timeout=180)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="u1-capture-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.photos = self.root / "photos"
        self.photos.mkdir()
        self.output = self.root / "new-capture"

    def execute(self, *arguments):
        result = subprocess.run([str(self.binary), *map(str, arguments)], check=False, capture_output=True, text=True, timeout=20)
        return result, json.loads(result.stdout)

    def generate(self, *extra):
        return self.execute("generate", "--input-dir", self.photos, "--output-dir", self.output, *extra)

    def test_help_identifies_native_local_route(self):
        result, report = self.execute("--help")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["engine"], "RealityKit PhotogrammetrySession")
        self.assertEqual(report["default_detail"], "medium")
        self.assertEqual(report["existing_outputs"], "refused")
        self.assertFalse(report["ready_to_print"])

    def test_invalid_and_repeated_arguments_are_errors(self):
        for args in [[], ["generate"], ["generate", "--wat", "x"], ["generate", "--input-dir", "a", "--input-dir", "b", "--output-dir", "c"], ["generate", "--input-dir", "a", "--output-dir", "b", "--detail", "raw"]]:
            with self.subTest(args=args):
                result, report = self.execute(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report["code"], "invalid_arguments")

    def test_empty_and_single_photo_folders_do_not_start_ml(self):
        for count in (0, 1):
            if count:
                (self.photos / "one.png").write_bytes(PNG)
            result, report = self.generate()
            self.assertEqual(result.returncode, 2)
            self.assertEqual(report["code"], "insufficient_images")
            self.assertFalse(self.output.exists())

    def test_missing_input_and_existing_output_are_refused(self):
        result, report = self.execute("generate", "--input-dir", self.root / "missing", "--output-dir", self.output)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["code"], "missing_input_directory")
        self.output.mkdir()
        sentinel = self.output / "keep.txt"
        sentinel.write_text("preserve")
        result, report = self.generate()
        self.assertEqual(report["code"], "output_exists")
        self.assertEqual(sentinel.read_text(), "preserve")

    def test_input_alias_nested_output_and_dangling_output_link_are_refused(self):
        for output in [self.photos, self.photos / "child", self.root]:
            with self.subTest(output=output):
                result, report = self.execute("generate", "--input-dir", self.photos, "--output-dir", output)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report["code"], "path_collision")
        self.output.symlink_to(self.root / "missing-target", target_is_directory=True)
        result, report = self.generate()
        self.assertEqual(report["code"], "output_exists")
        self.assertTrue(self.output.is_symlink())
        self.assertFalse((self.root / "missing-target").exists())

    def test_duplicates_and_corrupt_photos_do_not_start_ml(self):
        (self.photos / "one.png").write_bytes(PNG)
        (self.photos / "two.png").write_bytes(PNG)
        result, report = self.generate()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["code"], "insufficient_distinct_images")
        self.assertFalse(self.output.exists())
        (self.photos / "two.png").write_bytes(b"not an image")
        result, report = self.generate()
        self.assertEqual(report["code"], "invalid_image")
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
