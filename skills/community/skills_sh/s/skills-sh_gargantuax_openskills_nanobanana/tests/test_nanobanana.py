import json
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "nanobanana.py"
SPEC = importlib.util.spec_from_file_location("nanobanana_script", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
NANOBANANA = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(NANOBANANA)


class NanoBananaCliTest(unittest.TestCase):
    def run_cli(
        self,
        *args: str,
        env: dict[str, str] | None = None,
        cwd: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmpdir:
            workdir = cwd or tmpdir
            return subprocess.run(
                [sys.executable, str(SCRIPT_PATH), *args],
                cwd=workdir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env or {},
                check=False,
            )

    def test_generate_dry_run_resolves_default_alias(self) -> None:
        result = self.run_cli(
            "generate",
            "--prompt",
            "Generate a poster",
            "--output",
            "poster.png",
            "--dry-run",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["model"], "gemini-2.5-flash-image")
        self.assertTrue(payload["url"].endswith("/models/gemini-2.5-flash-image:generateContent"))

    def test_generate_dry_run_accepts_nanobanana_2_with_2k(self) -> None:
        result = self.run_cli(
            "generate",
            "--prompt",
            "Generate a poster",
            "--model",
            "nanobanana-2",
            "--size",
            "2K",
            "--output",
            "poster.png",
            "--dry-run",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        image_config = payload["request"]["generationConfig"]["imageConfig"]
        self.assertEqual(payload["model"], "gemini-3.1-flash-image-preview")
        self.assertEqual(image_config["imageSize"], "2K")

    def test_generate_rejects_size_for_nanobanana(self) -> None:
        result = self.run_cli(
            "generate",
            "--prompt",
            "Generate a poster",
            "--model",
            "nanobanana",
            "--size",
            "2K",
            "--output",
            "poster.png",
            "--dry-run",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not support image_size", result.stderr)

    def test_generate_ignores_inherited_size_for_nanobanana(self) -> None:
        env = {
            "GEMINI_API_KEY": "test-key",
            "GEMINI_BASE_URL": "https://example.com/v1beta",
            "GEMINI_IMAGE_SIZE": "2K",
        }
        result = self.run_cli(
            "generate",
            "--prompt",
            "Generate a poster",
            "--model",
            "nanobanana",
            "--output",
            "poster.png",
            "--dry-run",
            env=env,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        generation_config = payload["request"]["generationConfig"]
        self.assertNotIn("imageConfig", generation_config)

    def test_generate_rejects_512_for_nanobanana_pro(self) -> None:
        result = self.run_cli(
            "generate",
            "--prompt",
            "Generate a poster",
            "--model",
            "nanobanana-pro",
            "--size",
            "512",
            "--output",
            "poster.png",
            "--dry-run",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Supported values: 1K, 2K, 4K", result.stderr)

    def test_generate_rejects_base_url_ending_with_models(self) -> None:
        result = self.run_cli(
            "generate",
            "--prompt",
            "Generate a poster",
            "--base-url",
            "https://example.com/v1beta/models",
            "--output",
            "poster.png",
            "--dry-run",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not /models", result.stderr)

    def test_batch_dry_run_uses_configured_count(self) -> None:
        result = self.run_cli(
            "batch",
            "--prompt",
            "Generate a poster",
            "--count",
            "3",
            "--dir",
            "out",
            "--prefix",
            "poster",
            "--dry-run",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["count"], 3)
        self.assertEqual(len(payload["requests"]), 3)

    def test_generate_dry_run_finds_dotenv_in_parent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            nested = root / "nested" / "child"
            nested.mkdir(parents=True)
            (root / ".env").write_text(
                "\n".join(
                    [
                        "GEMINI_BASE_URL=http://parent-env-gemini.example/v1beta",
                        "GEMINI_MODEL=nanobanana-2",
                        "GEMINI_ASPECT_RATIO=3:4",
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_cli(
                "generate",
                "--prompt",
                "Generate a poster",
                "--output",
                "poster.png",
                "--dry-run",
                cwd=str(nested),
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["url"], "http://parent-env-gemini.example/v1beta/models/gemini-3.1-flash-image-preview:generateContent")
        image_config = payload["request"]["generationConfig"]["imageConfig"]
        self.assertEqual(image_config["aspectRatio"], "3:4")


class NanoBananaModuleTest(unittest.TestCase):
    def test_execute_single_batch_request_uses_passed_output_dir(self) -> None:
        settings = {
            "model": "gemini-3.1-flash-image-preview",
            "base_url": "https://example.com/v1beta",
            "api_key": "test-key",
            "auth_mode": "x-goog-api-key",
            "aspect_ratio": None,
            "image_size": None,
            "use_search": False,
            "timeout": 30,
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(NANOBANANA, "send_request", return_value={"candidates": []}):
                with mock.patch.object(
                    NANOBANANA,
                    "summarize_result",
                    return_value={"images": [], "texts": [], "command": "batch"},
                ) as summarize_result:
                    result = NANOBANANA.execute_single_batch_request(
                        prompt="test",
                        input_images=[],
                        settings=settings,
                        output_template="out-{index}",
                        default_output_dir=tmpdir,
                        index=2,
                    )

        self.assertEqual(result["index"], 2)
        self.assertEqual(summarize_result.call_args.kwargs["default_output_dir"], tmpdir)


if __name__ == "__main__":
    unittest.main()
