import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "gpt_image.py"


class GptImageCliTest(unittest.TestCase):
    def run_cli(self, *args: str, cwd: str | None = None) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmpdir:
            workdir = cwd or tmpdir
            return subprocess.run(
                [sys.executable, str(SCRIPT_PATH), *args],
                cwd=workdir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env={},
                check=False,
            )

    def test_responses_dry_run_uses_responses_model_and_object_tool_choice(self) -> None:
        result = self.run_cli(
            "responses",
            "--input-text",
            "Generate a poster",
            "--output",
            "poster.png",
            "--dry-run",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        request = payload["request"]

        self.assertEqual(request["model"], "gpt-5.4")
        self.assertEqual(request["tool_choice"], {"type": "image_generation"})
        self.assertEqual(request["tools"][0]["type"], "image_generation")
        self.assertEqual(request["tools"][0]["size"], "auto")
        self.assertEqual(request["tools"][0]["quality"], "high")
        self.assertEqual(request["tools"][0]["output_format"], "webp")

    def test_generations_rejects_response_format_for_gpt_image_models(self) -> None:
        result = self.run_cli(
            "generations",
            "--prompt",
            "test",
            "--output",
            "test.png",
            "--response-format",
            "b64_json",
            "--dry-run",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Omit response_format", result.stderr)

    def test_responses_rejects_gpt_image_model_as_top_level_model(self) -> None:
        result = self.run_cli(
            "responses",
            "--model",
            "gpt-image-2",
            "--input-text",
            "Generate a poster",
            "--output",
            "poster.png",
            "--dry-run",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("text-capable Responses model", result.stderr)

    def test_responses_rejects_input_fidelity_for_default_gpt_image_2_tool(self) -> None:
        result = self.run_cli(
            "responses",
            "--input-text",
            "Generate a poster",
            "--input-fidelity",
            "high",
            "--output",
            "poster.png",
            "--dry-run",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not configurable for gpt-image-2", result.stderr)

    def test_responses_accepts_supported_tool_model_with_input_fidelity(self) -> None:
        result = self.run_cli(
            "responses",
            "--input-text",
            "Generate a poster",
            "--tool-model",
            "gpt-image-1.5",
            "--input-fidelity",
            "high",
            "--output",
            "poster.png",
            "--dry-run",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        tool = payload["request"]["tools"][0]

        self.assertEqual(tool["model"], "gpt-image-1.5")
        self.assertEqual(tool["input_fidelity"], "high")

    def test_dry_run_finds_dotenv_in_parent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            nested = root / "a" / "b"
            nested.mkdir(parents=True)
            (root / ".env").write_text(
                "\n".join(
                    [
                        "OPENAI_BASE_URL=http://parent-env.example/v1",
                        "OPENAI_IMAGE_QUALITY=medium",
                    ]
                ),
                encoding="utf-8",
            )

            result = self.run_cli(
                "generations",
                "--prompt",
                "test",
                "--output",
                "test.png",
                "--dry-run",
                cwd=str(nested),
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        request = payload["request"]
        self.assertEqual(payload["url"], "http://parent-env.example/v1/images/generations")
        self.assertEqual(request["quality"], "medium")


if __name__ == "__main__":
    unittest.main()
