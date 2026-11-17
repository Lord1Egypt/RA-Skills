#!/usr/bin/env python3
"""Fail-fast environment checks for TaoHtml capability profiles.

The parent process uses only the Python standard library. Imports that may load
native code and the Chromium smoke test run in child processes so a crash,
timeout, or missing browser is reported without taking down the calling Agent.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable


SCHEMA_VERSION = "1.0"
MINIMUM_PYTHON = (3, 10)
DEFAULT_TIMEOUT_SECONDS = 20.0
MODULE_TIMEOUT_SECONDS = 10.0
PROFILES = ("core", "pdf", "static-reference", "profile-reuse", "browser")

PROFILE_MODULES: dict[str, tuple[tuple[str, str, str], ...]] = {
    "core": (),
    "pdf": (
        ("module_pymupdf", "fitz", "PyMuPDF"),
    ),
    "static-reference": (
        ("module_pillow", "PIL", "Pillow"),
        ("module_pyyaml", "yaml", "PyYAML"),
        ("module_playwright", "playwright.sync_api", "Playwright"),
    ),
    "profile-reuse": (
        ("module_pillow", "PIL", "Pillow"),
        ("module_theme_loader", "theme_runtime", "TaoHtml project-theme loader"),
    ),
    "browser": (
        ("module_playwright", "playwright.sync_api", "Playwright"),
    ),
}

BROWSER_PROBE = r"""
import json
import sys
import tempfile
from pathlib import Path

profile = sys.argv[1]
executable_path = sys.argv[2] or None
phase = "import"
browser = None
try:
    from playwright.sync_api import sync_playwright
    phase = "launch"
    launch_options = {"headless": True}
    if profile == "static-reference":
        launch_options["args"] = ["--disable-gpu"]
    if executable_path:
        launch_options["executable_path"] = executable_path
    with tempfile.TemporaryDirectory(prefix="taohtml-browser-probe-") as temp_dir:
        screenshot = Path(temp_dir) / "smoke.png"
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**launch_options)
            phase = "page"
            page = browser.new_page(viewport={"width": 640, "height": 360})
            page.set_content(
                "<!doctype html><meta charset='utf-8'>"
                "<style>html,body{margin:0;width:100%;height:100%;background:#111;color:#fff}"
                "main{font:32px sans-serif;padding:48px}</style><main>TaoHtml preflight</main>",
                wait_until="load",
            )
            phase = "screenshot"
            page.screenshot(path=str(screenshot), full_page=False)
            browser.close()
            browser = None
        payload = screenshot.read_bytes()
        if len(payload) < 100 or not payload.startswith(b"\x89PNG\r\n\x1a\n"):
            raise RuntimeError("minimal screenshot is not a valid PNG")
    print(json.dumps({"status": "pass", "category": "ok", "detail": "Chromium launched and produced a minimal PNG screenshot."}))
except BaseException as exc:
    if browser is not None:
        try:
            browser.close()
        except BaseException:
            pass
    detail = f"{type(exc).__name__}: {exc}"
    lowered = detail.lower()
    if phase == "import":
        category = "playwright_import_failed"
    elif "executable doesn't exist" in lowered or "playwright install" in lowered:
        category = "chromium_missing"
    elif phase == "screenshot":
        category = "chromium_screenshot_failed"
    else:
        category = "chromium_launch_failed"
    print(json.dumps({"status": "fail", "category": category, "detail": detail[:1600]}))
    raise SystemExit(1)
"""

Probe = Callable[..., dict[str, str]]


def _check(
    check_id: str,
    status: str,
    summary: str,
    *,
    category: str = "ok",
    detail: str = "",
    remediation: str = "",
) -> dict[str, object]:
    return {
        "id": check_id,
        "required": True,
        "status": status,
        "category": category,
        "summary": summary,
        "detail": detail,
        "remediation": remediation,
    }


def _python_check() -> dict[str, object]:
    actual = sys.version_info[:3]
    minimum = ".".join(str(item) for item in MINIMUM_PYTHON)
    if actual[:2] < MINIMUM_PYTHON:
        return _check(
            "python_version",
            "fail",
            f"Python {minimum}+ is required.",
            category="python_unsupported",
            detail=f"Found {'.'.join(str(item) for item in actual)} at {sys.executable}",
            remediation=f"Use an environment with Python {minimum} or newer.",
        )
    return _check(
        "python_version",
        "pass",
        f"Python {'.'.join(str(item) for item in actual)} is supported.",
        detail=sys.executable,
    )


def _filesystem_check(workspace: Path) -> dict[str, object]:
    try:
        resolved = workspace.expanduser().resolve(strict=True)
        if not resolved.is_dir():
            raise NotADirectoryError(resolved)
        with tempfile.TemporaryDirectory(prefix=".taohtml-preflight-", dir=resolved) as temp_dir:
            probe = Path(temp_dir) / "probe.txt"
            probe.write_text("taohtml", encoding="utf-8")
            if probe.read_text(encoding="utf-8") != "taohtml":
                raise OSError("filesystem read-back did not match")
    except OSError as exc:
        return _check(
            "workspace_filesystem",
            "fail",
            "The workspace is not usable for TaoHtml output.",
            category="filesystem_unavailable",
            detail=f"{type(exc).__name__}: {exc}",
            remediation="Choose a readable and writable workspace, then rerun the preflight.",
        )
    return _check(
        "workspace_filesystem",
        "pass",
        "The workspace supports temporary read/write operations.",
        detail=str(resolved),
    )


def _trim_process_detail(completed: subprocess.CompletedProcess[str]) -> str:
    text = (completed.stderr or completed.stdout or "").strip()
    if not text:
        text = f"child process exited with code {completed.returncode}"
    return text[-1600:]


def _probe_module(module: str, timeout: float) -> dict[str, str]:
    code = (
        "import importlib,sys; "
        "sys.path.insert(0, sys.argv[2]); "
        "importlib.import_module(sys.argv[1]); "
        "print(sys.argv[1] + ' import ok')"
    )
    try:
        completed = subprocess.run(
            [sys.executable, "-c", code, module, str(Path(__file__).resolve().parent)],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "fail",
            "category": "module_import_timeout",
            "detail": f"Import timed out after {timeout:g} seconds.",
        }
    if completed.returncode == 0:
        return {"status": "pass", "category": "ok", "detail": completed.stdout.strip()}
    detail = _trim_process_detail(completed)
    lowered = detail.lower()
    category = (
        "module_missing"
        if "modulenotfounderror" in lowered or "no module named" in lowered
        else "module_import_failed"
    )
    if completed.returncode < 0 or completed.returncode >= 128:
        category = "module_import_crashed"
    return {"status": "fail", "category": category, "detail": detail}


def _probe_browser(
    profile: str, executable_path: Path | None, timeout: float
) -> dict[str, str]:
    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                BROWSER_PROBE,
                profile,
                str(executable_path) if executable_path else "",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "fail",
            "category": "chromium_launch_timeout",
            "detail": f"Chromium smoke test timed out after {timeout:g} seconds.",
        }

    payload: dict[str, str] | None = None
    for line in reversed(completed.stdout.splitlines()):
        try:
            candidate = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict) and isinstance(candidate.get("status"), str):
            payload = {str(key): str(value) for key, value in candidate.items()}
            break
    if completed.returncode == 0 and payload and payload.get("status") == "pass":
        return payload
    if payload:
        return payload
    category = "browser_probe_crashed"
    detail = _trim_process_detail(completed)
    return {"status": "fail", "category": category, "detail": detail}


def _customer_message(profile: str, checks: list[dict[str, object]]) -> tuple[str, list[str]]:
    failures = [item for item in checks if item["status"] == "fail"]
    if not failures:
        return (
            f"环境预检通过（{profile}）：当前环境具备这条能力路径所需的最小条件。",
            [],
        )

    labels = "、".join(str(item["summary"]) for item in failures)
    if profile == "static-reference":
        return (
            "环境预检未通过（static-reference）：尚未读取或处理客户参考图；"
            f"企业模板保真与参考风格重构都不能继续。失败项：{labels}",
            [
                "修复依赖或更换可用环境后，重新运行 static-reference 预检并重试客户参考路线。",
                "明确放弃客户参考路线，改用 TaoHtml 八套内置视觉系统。",
            ],
        )
    if profile == "pdf":
        return (
            "环境预检未通过（pdf）：尚未读取或提取 PDF；请先修复或更换环境。"
            f"失败项：{labels}",
            ["安装 Skill 声明的 PDF 依赖或更换环境，预检通过后再读取材料。"],
        )
    if profile == "profile-reuse":
        return (
            "环境预检未通过（profile-reuse）：尚未绑定或加载企业模板档案；"
            f"请先修复最小复用依赖。失败项：{labels}",
            [
                "修复 Pillow 或 TaoHtml project-theme loader，或更换环境；"
                "重新运行 profile-reuse 预检后再绑定档案。"
            ],
        )
    if profile == "browser":
        return (
            "环境预检未通过（browser）：不能执行浏览器 QA，也不能把该项标记为通过。"
            f"失败项：{labels}",
            ["修复 Playwright/Chromium 或更换环境，预检通过后再运行浏览器 QA。"],
        )
    return (
        f"环境预检未通过（core）：当前工作区不能安全启动 TaoHtml。失败项：{labels}",
        ["修复 Python 或工作区读写条件，或更换环境后重试。"],
    )


def run_preflight(
    profile: str,
    workspace: Path,
    *,
    executable_path: Path | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    module_probe: Probe = _probe_module,
    browser_probe: Probe = _probe_browser,
) -> dict[str, object]:
    if profile not in PROFILES:
        raise ValueError(f"unknown profile: {profile}")
    started = time.monotonic()
    checks = [_python_check(), _filesystem_check(workspace)]

    module_results: dict[str, dict[str, str]] = {}
    module_timeout = min(timeout, MODULE_TIMEOUT_SECONDS)
    for check_id, module, distribution in PROFILE_MODULES[profile]:
        if not all(item["status"] == "pass" for item in checks[:2]):
            probe = {
                "status": "blocked",
                "category": "prerequisite_failed",
                "detail": "Core Python or filesystem check failed.",
            }
            module_results[module] = probe
            checks.append(
                _check(
                    check_id,
                    "blocked",
                    f"{distribution} import was not run because a core check failed.",
                    category="prerequisite_failed",
                    detail=probe["detail"],
                )
            )
            continue
        probe = module_probe(module, module_timeout)
        module_results[module] = probe
        if probe["status"] == "pass":
            checks.append(
                _check(
                    check_id,
                    "pass",
                    f"{distribution} imports successfully.",
                    detail=probe.get("detail", ""),
                )
            )
        else:
            checks.append(
                _check(
                    check_id,
                    "fail",
                    f"{distribution} is unavailable.",
                    category=probe.get("category", "module_import_failed"),
                    detail=probe.get("detail", ""),
                    remediation=(
                        "Install the exact skill requirements in this Python environment, "
                        "or use a different environment."
                    ),
                )
            )

    if profile in {"static-reference", "browser"}:
        playwright = module_results.get("playwright.sync_api")
        prerequisites_ok = all(item["status"] == "pass" for item in checks)
        if prerequisites_ok and playwright and playwright["status"] == "pass":
            probe = browser_probe(profile, executable_path, timeout)
            if probe["status"] == "pass":
                checks.append(
                    _check(
                        "chromium_launch_screenshot",
                        "pass",
                        "Chromium launches and captures a minimal screenshot.",
                        detail=probe.get("detail", ""),
                    )
                )
            else:
                checks.append(
                    _check(
                        "chromium_launch_screenshot",
                        "fail",
                        "Chromium launch or screenshot failed.",
                        category=probe.get("category", "chromium_launch_failed"),
                        detail=probe.get("detail", ""),
                        remediation=(
                            "Install Chromium for this Playwright environment or switch to a "
                            "known-good environment, then rerun the same profile."
                        ),
                    )
                )
        else:
            checks.append(
                _check(
                    "chromium_launch_screenshot",
                    "blocked",
                    "Chromium smoke test was not run because a prerequisite failed.",
                    category="prerequisite_failed",
                )
            )

    ok = all(item["status"] == "pass" for item in checks)
    conclusion, options = _customer_message(profile, checks)
    return {
        "schema_version": SCHEMA_VERSION,
        "profile": profile,
        "status": "pass" if ok else "fail",
        "ok": ok,
        "duration_ms": round((time.monotonic() - started) * 1000),
        "python_executable": sys.executable,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "os_name": os.name,
            "sys_platform": sys.platform,
        },
        "checks": checks,
        "customer_conclusion": conclusion,
        "customer_options": options,
    }


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Run a fail-fast TaoHtml environment capability preflight."
    )
    parser.add_argument("--profile", choices=PROFILES, required=True)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace whose basic read/write behavior must be verified.",
    )
    parser.add_argument(
        "--chromium-executable",
        type=Path,
        help="Optional explicit Chromium executable for managed environments.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=(
            f"Browser-probe timeout. Default: {DEFAULT_TIMEOUT_SECONDS:g}; "
            f"module imports cap at {MODULE_TIMEOUT_SECONDS:g}."
        ),
    )
    args = parser.parse_args()
    if args.timeout_seconds <= 0 or args.timeout_seconds > 120:
        parser.error("--timeout-seconds must be greater than 0 and no more than 120")

    result = run_preflight(
        args.profile,
        args.workspace,
        executable_path=args.chromium_executable,
        timeout=args.timeout_seconds,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(result["customer_conclusion"], file=sys.stderr)
    for index, option in enumerate(result["customer_options"], start=1):
        print(f"{index}. {option}", file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
