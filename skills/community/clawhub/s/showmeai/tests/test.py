#!/usr/bin/env python3
"""ShowMeAI Skill offline contract and runtime tests."""

from __future__ import annotations

import io
import json
import os
import re
import stat
import sys
import tempfile
import threading
import urllib.error
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from showmeai import (  # noqa: E402
    _require_category_ready,
    build_parser,
    command_config_set,
    command_image,
    command_onboarding,
    command_paths,
    command_setup,
    main,
)
from showmeai_core.catalog import (  # noqa: E402
    grouped_models,
    infer_creative_category,
    load_catalog,
    recommended_image_model,
    validate_params,
)
from showmeai_core.config import (  # noqa: E402
    DEFAULT_CONFIG,
    complete_onboarding_category,
    load_config,
    onboarding_status,
    save_api_key,
    save_config,
)
from showmeai_core.errors import HttpError, SkillError, error_result  # noqa: E402
from showmeai_core.http import ApiClient  # noqa: E402
from showmeai_core.outputs import OutputManager  # noqa: E402
from showmeai_core.tasks import TaskJournal, TaskRecord, TaskRunner, normalize_response  # noqa: E402
from video_gen import legacy_args as video_legacy_args  # noqa: E402


passed = 0
failed = 0


def ok(message: str) -> None:
    global passed
    passed += 1
    print(f"  ✅ {message}")


def fail(message: str) -> None:
    global failed
    failed += 1
    print(f"  ❌ {message}")


def check(condition: bool, message: str) -> None:
    ok(message) if condition else fail(message)


def section(title: str) -> None:
    print(f"\n{'=' * 60}\n  {title}\n{'=' * 60}")


def expect_error(code: str, callback, message: str) -> None:
    try:
        callback()
    except SkillError as error:
        check(error.code == code, message)
    else:
        fail(message)


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0

    def now(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.value += seconds


class FakeTaskClient:
    def __init__(self, responses: list[object]) -> None:
        self.responses = list(responses)

    def request_json(self, _method: str, _url: str, timeout: int = 90) -> dict:
        del timeout
        value = self.responses.pop(0)
        if isinstance(value, Exception):
            raise value
        return value

    def request(self, _method: str, _url: str, timeout: int = 300):
        del timeout
        return b"media", {"Content-Type": "video/mp4"}


class FakeResponse:
    headers = {"Content-Type": "application/json"}

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self) -> bytes:
        return b'{"ok":true}'


section("T1 · file completeness")
required = [
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "DESIGN.md",
    "CHANGELOG.md",
    "LICENSE",
    "data/model-catalog.json",
    "scripts/showmeai.py",
    "scripts/showmeai_core/config.py",
    "scripts/showmeai_core/tasks.py",
]
for relative in required:
    check((ROOT / relative).is_file(), f"{relative} exists")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
check("├──" in readme and "└──" in readme, "README contains an annotated file tree")


section("T2 · frontmatter and output contract")
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
frontmatter_match = re.match(r"^---\n(.*?)\n---", skill, re.DOTALL)
check(frontmatter_match is not None, "SKILL.md has YAML frontmatter")
frontmatter = frontmatter_match.group(1) if frontmatter_match else ""
for field in ("name:", "description:", "version:", "triggers:", "token_budget:"):
    check(re.search(rf"(?m)^{re.escape(field)}", frontmatter) is not None, f"frontmatter includes {field[:-1]}")
check("## Output file conventions" in skill, "SKILL.md declares output-file conventions")


section("T3 · route consistency")
references = sorted((ROOT / "references").glob("*.md"))
for reference in references:
    relative = f"references/{reference.name}"
    check(relative in skill, f"{relative} is routed by SKILL.md")
    intro = "\n".join(reference.read_text(encoding="utf-8").splitlines()[:5])
    check("SKILL.md" in intro and "remain" in intro.lower(), f"{relative} points routing back to SKILL.md")


section("T4 · path and platform neutrality")
runtime_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "scripts").rglob("*.py"))
for brand_path in ("~/.openclaw", "~/.codex", "~/.hermes", "~/.workbuddy"):
    check(brand_path not in runtime_text.lower(), f"runtime does not depend on {brand_path}")
check("SHOWMEAI_CONFIG_DIR" in runtime_text and "XDG_CONFIG_HOME" in runtime_text, "runtime supports portable and OS-native paths")


section("T5 · model catalog and parameter integrity")
catalog = load_catalog()
model_ids = [model["id"] for model in catalog["models"]]
check(len(model_ids) == len(set(model_ids)), "catalog model IDs are unique")
recommended = [model for model in catalog["models"] if model.get("category") == "image" and model.get("recommended") == 1]
check(len(recommended) == 1 and recommended[0]["id"] == "gemini-3.1-flash-image", "Gemini 3.1 Flash Image is the single initial preference")
check(DEFAULT_CONFIG["defaults"]["image"]["model"] == "gemini-3.1-flash-image", "runtime default matches catalog preference")
check(recommended_image_model(["gpt-image-2", "nano-banana-2"]) == "nano-banana-2", "preference works through the Nano Banana 2 alias")
groups = grouped_models(["gpt-image-2", "whisper-1"], include_catalog_tasks=False)
check([item["selected_id"] for item in groups["image"]] == ["gpt-image-2"], "live models are filtered into creative categories")
new_groups = grouped_models(["future-image-v9", "future-chat-v9"], include_catalog_tasks=False)
check([item["selected_id"] for item in new_groups["image"]] == ["future-image-v9"], "new creative IDs remain visible without leaking language models")
check(infer_creative_category("next-seedance-model") == "video", "new video IDs are categorized conservatively")
expect_error("PARAM_INVALID", lambda: validate_params("gpt-image-2", {"n": 11}), "image count upper bound is enforced")
expect_error("PARAM_INVALID", lambda: validate_params("Hunyuan3D-2", {"octree_resolution": 401}), "3D resolution upper bound is enforced")


section("T6 · configuration, output, and CLI boundaries")
with tempfile.TemporaryDirectory() as temp:
    old_config_dir = os.environ.get("SHOWMEAI_CONFIG_DIR")
    old_state_dir = os.environ.get("SHOWMEAI_STATE_DIR")
    os.environ["SHOWMEAI_CONFIG_DIR"] = str(Path(temp) / "config")
    os.environ["SHOWMEAI_STATE_DIR"] = str(Path(temp) / "state")
    try:
        key_path = save_api_key("test-key-123456")
        config_path = save_config(DEFAULT_CONFIG)
        check(load_config()["defaults"]["image"]["model"] == "gemini-3.1-flash-image", "configuration round-trips atomically")
        check(stat.S_IMODE(key_path.stat().st_mode) == 0o600, "credential file uses owner-only permissions")
        check("test-key" not in config_path.read_text(encoding="utf-8"), "secret is not written to config.json")
        output_config = load_config()
        output_config["output"]["directory"] = str(Path(temp) / "output")
        manager = OutputManager(output_config, "image")
        first = manager.write_bytes(b"one", "sample", "png", "same.png")
        second = manager.write_bytes(b"two", "sample", "png", "same.png")
        check(first != second and second.name == "same-2.png", "existing media files are never overwritten")
        signed = manager.write_base64("/9j/AA==", "signed", "png")
        check(signed.suffix == ".jpg", "base64 output extension follows the actual media signature")
        signed_named = manager.write_base64("/9j/AA==", "signed", "png", "requested.png")
        check(signed_named.name == "requested.jpg", "an explicit filename cannot force a false media extension")
        expect_error(
            "OUTPUT_FILENAME_INVALID",
            lambda: manager.write_bytes(b"blocked", "sample", "png", "../escape.png"),
            "output filenames cannot escape the configured directory",
        )
    finally:
        if old_config_dir is None:
            os.environ.pop("SHOWMEAI_CONFIG_DIR", None)
        else:
            os.environ["SHOWMEAI_CONFIG_DIR"] = old_config_dir
        if old_state_dir is None:
            os.environ.pop("SHOWMEAI_STATE_DIR", None)
        else:
            os.environ["SHOWMEAI_STATE_DIR"] = old_state_dir

parser = build_parser()
check(parser.parse_args(["image", "--prompt", "test"]).command == "image", "unified CLI routes image commands")
check(video_legacy_args(["--prompt", "x", "--no-audio"]) == ["video", "--prompt", "x", "--no-audio"], "legacy video wrapper preserves no-audio intent")
with tempfile.TemporaryDirectory() as temp:
    with patch.dict(os.environ, {"SHOWMEAI_CONFIG_DIR": str(Path(temp) / "config")}, clear=False):
        check(main(["config", "show", "--json"]) == 0, "--json is accepted after a subcommand")

with tempfile.TemporaryDirectory() as temp:
    old_config_dir = os.environ.get("SHOWMEAI_CONFIG_DIR")
    os.environ["SHOWMEAI_CONFIG_DIR"] = str(Path(temp) / "config")
    setup_stdin = io.StringIO("agent-key-123456\n")
    with patch("showmeai.sys.stdin", setup_stdin), patch(
        "showmeai.ApiClient.models",
        return_value={"data": [{"id": "gpt-image-2"}, {"id": "nano-banana-2"}, {"id": "future-chat-v9"}]},
    ):
        setup_result = command_setup(
            type(
                "SetupArgs",
                (),
                {"base_url": "", "key_stdin": True, "replace_key": False, "non_interactive": True},
            )()
        )
    check(setup_result["ok"] and setup_result["data"]["default_image_model"] == "nano-banana-2", "Agent-assisted setup validates stdin Key and applies image preference")
    check(setup_result["data"]["models"]["image"][0]["id"] == "nano-banana-2", "Agent setup lists the recommended image model first")
    check(setup_result["data"]["onboarding_status"] == "needs_defaults", "Key-only Agent setup cannot silently skip default-model confirmation")
    expect_error(
        "ONBOARDING_REQUIRED",
        lambda: _require_category_ready(load_config(), "image"),
        "new image generation is blocked before the user confirms a default model",
    )
    check((Path(temp) / "config" / "credentials").read_text(encoding="utf-8").strip() == "agent-key-123456", "Agent-assisted setup persists the Key once")
    with patch(
        "showmeai.ApiClient.models",
        return_value={"data": [{"id": "gpt-image-2"}, {"id": "nano-banana-2"}]},
    ):
        onboarding_result = command_onboarding(
            type(
                "OnboardingArgs",
                (),
                {
                    "onboarding_command": "apply",
                    "category": "image",
                    "model": "nano-banana-2",
                    "params_json": '{"n":2,"image_size":"2K","aspect_ratio":"4:3"}',
                },
            )()
        )
    check(onboarding_result["data"]["status"] == "complete", "Agent onboarding explicitly saves the chosen image model")
    check(load_config()["defaults"]["image"]["params"]["n"] == 2, "onboarding saves model-supported default quantity")
    check(onboarding_status(load_config(), "image") == "complete", "image onboarding completion persists across requests")
    expect_error(
        "UNSUPPORTED_MODEL_PARAMETER",
        lambda: validate_params("gemini-3.1-flash-image", {"quality": "high"}, reject_unknown=True),
        "onboarding rejects parameters unsupported by the selected model",
    )
    with patch(
        "showmeai.ApiClient.models",
        return_value={"data": [{"id": "nano-banana-2"}]},
    ):
        expect_error(
            "MODEL_NOT_AVAILABLE_IN_GROUP",
            lambda: command_onboarding(
                type(
                    "OnboardingArgs",
                    (),
                    {"onboarding_command": "apply", "category": "image", "model": "gpt-image-2", "params_json": "{}"},
                )()
            ),
            "onboarding rejects a model unavailable to the current token group",
        )
    command_config_set(
        type("ConfigArgs", (), {"path": "defaults.image.model", "value": "gpt-image-2"})()
    )
    check(onboarding_status(load_config(), "image") == "needs_defaults", "low-level default edits require onboarding confirmation again")
    if old_config_dir is None:
        os.environ.pop("SHOWMEAI_CONFIG_DIR", None)
    else:
        os.environ["SHOWMEAI_CONFIG_DIR"] = old_config_dir

paths_result = command_paths(type("PathsArgs", (), {})())
path_values = " ".join(str(value).lower() for value in paths_result["data"].values())
check("openclaw" not in path_values and "workbuddy" not in path_values, "resolved ShowMeAI paths never target an Agent host config")

with tempfile.TemporaryDirectory() as temp:
    old_config_dir = os.environ.get("SHOWMEAI_CONFIG_DIR")
    os.environ["SHOWMEAI_CONFIG_DIR"] = str(Path(temp) / "config")
    image_config = json.loads(json.dumps(DEFAULT_CONFIG))
    image_config["output"]["directory"] = str(Path(temp) / "output")
    complete_onboarding_category(image_config, "image", "test-catalog")
    save_config(image_config)
    image_args = type(
        "ImageArgs",
        (),
        {
            "model": "gpt-image-2",
            "prompt": "two variants",
            "count": 3,
            "concurrency": 2,
            "size": "1536x1152",
            "image_size": None,
            "aspect_ratio": None,
            "quality": "low",
            "output_format": "png",
            "background": None,
            "output_compression": None,
            "input": [],
            "mask": "",
            "out_dir": "",
            "filename": "",
        },
    )()
    image_barrier = threading.Barrier(2)
    image_lock = threading.Lock()
    image_calls = 0
    active_image_calls = 0
    max_active_image_calls = 0

    def fake_image_request(*_args):
        global image_calls, active_image_calls, max_active_image_calls
        with image_lock:
            image_calls += 1
            call_number = image_calls
            if call_number > 1:
                active_image_calls += 1
                max_active_image_calls = max(max_active_image_calls, active_image_calls)
        if call_number > 1:
            image_barrier.wait(timeout=2)
            with image_lock:
                active_image_calls -= 1
        token_count = 100 + (call_number - 1) * 10
        encoded = ("b25l", "dHdv", "dGhyZWU=")[call_number - 1]
        return {"data": [{"b64_json": encoded}], "usage": {"output_tokens": token_count}}

    with patch("showmeai._client", return_value=object()), patch(
        "showmeai._image_request", side_effect=fake_image_request
    ) as image_request:
        image_result = command_image(image_args)
    check(len(image_result["data"]["files"]) == 3, "missing multi-image results are completed with single-image requests")
    check(image_result["data"]["request_count"] == 3, "multi-image completion reports the number of API requests")
    check(image_result["data"]["usage"]["output_tokens"] == 330, "multi-request image usage is aggregated")
    check(image_request.call_args_list[1].args[3]["n"] == 1, "completion requests explicitly request one image")
    check(max_active_image_calls == 2, "multiple completion requests run concurrently")
    if old_config_dir is None:
        os.environ.pop("SHOWMEAI_CONFIG_DIR", None)
    else:
        os.environ["SHOWMEAI_CONFIG_DIR"] = old_config_dir


section("T7 · success, rate-limit, failure, and durable polling")
check(normalize_response("music", {"data": {"status": "SUCCESS", "data": [{"audio_url": "https://example.com/a.mp3"}]}})[0] == "success", "music terminal success is normalized")
check(normalize_response("pic", {"data": {"state": -1, "state_detail": "bad"}})[0] == "failed", "image-tool terminal failure is normalized")

with tempfile.TemporaryDirectory() as temp:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    config["output"]["directory"] = str(Path(temp) / "output")
    config["polling"]["heartbeat_seconds"] = 999
    clock = FakeClock()
    journal = TaskJournal(Path(temp) / "tasks")
    client = FakeTaskClient([
        {"status": "processing", "progress": 20},
        {"status": "succeeded", "content": {"video_url": "https://example.com/result.mp4"}},
    ])
    record = TaskRecord("success-task", "video", "https://example.com/task", "video", "demo")
    result = TaskRunner(client, config, journal=journal, sleep_fn=clock.sleep, clock=clock.now).wait(record)
    check(result["status"] == "success" and Path(result["files"][0]).is_file(), "polling waits through processing and downloads terminal output")
    check(json.loads(journal.path("success-task").read_text(encoding="utf-8"))["files"], "terminal files are persisted to the task journal")

with tempfile.TemporaryDirectory() as temp:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    config["output"]["directory"] = str(Path(temp) / "output")
    clock = FakeClock()
    retry = SkillError("NETWORK_ERROR", "temporary", retryable=True)
    client = FakeTaskClient([retry, {"status": "completed", "output": {"file_url": "https://example.com/model.glb"}}])
    record = TaskRecord("retry-task", "3d", "https://example.com/task", "3d", "model")
    result = TaskRunner(client, config, journal=TaskJournal(Path(temp) / "tasks"), sleep_fn=clock.sleep, clock=clock.now).wait(record)
    check(result["status"] == "success", "retryable polling errors do not discard an active task")

with tempfile.TemporaryDirectory() as temp:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    clock = FakeClock()
    client = FakeTaskClient([{"status": "failed", "error": "rejected"}])
    record = TaskRecord("failed-task", "video", "https://example.com/task", "video", "demo")
    expect_error(
        "TASK_FAILED",
        lambda: TaskRunner(client, config, journal=TaskJournal(Path(temp)), sleep_fn=clock.sleep, clock=clock.now).wait(record),
        "terminal task failure stops with a structured error",
    )

rate_limit = urllib.error.HTTPError(
    "https://example.com",
    429,
    "rate limited",
    {"Retry-After": "0"},
    io.BytesIO(b'{"error":"rate"}'),
)
sleeps: list[float] = []
with patch("urllib.request.urlopen", side_effect=[rate_limit, FakeResponse()]):
    raw, _headers = ApiClient("https://example.com/v1", "secret", retries=1, sleep_fn=sleeps.append).request("GET", "https://example.com")
check(raw == b'{"ok":true}' and len(sleeps) == 1, "HTTP 429 follows Retry-After and retries successfully")

secret_error = urllib.error.HTTPError(
    "https://example.com",
    401,
    "unauthorized",
    {},
    io.BytesIO(b'{"error":"secret-key-123 is invalid"}'),
)
with patch("urllib.request.urlopen", side_effect=secret_error):
    try:
        ApiClient("https://example.com/v1", "secret-key-123", retries=0).request("GET", "https://example.com")
    except HttpError as error:
        check("secret-key-123" not in error.body and "REDACTED" in error.body, "HTTP error bodies redact a reflected API Key")
    else:
        fail("HTTP error bodies redact a reflected API Key")

unexpected = error_result(RuntimeError("private/path/and/value"))
check("private/path" not in unexpected["error"]["message"], "unexpected errors do not expose raw internal details")


section("SUMMARY")
total = passed + failed
print(f"  Score: {passed}/{total} ({passed / total * 100:.0f}%)")
sys.exit(0 if failed == 0 else 1)
