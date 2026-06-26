"""Shared utilities for Twitter Skill scripts."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def get_scripts_dir() -> Path:
    """Get the directory containing these scripts."""
    return Path(__file__).parent.resolve()


def find_python() -> str:
    """Find the best Python executable."""
    # Prefer the same python that is running this script
    return sys.executable


def run_twitter_cli(args: list[str], json_output: bool = False) -> dict[str, Any]:
    """Run twitter-cli with given arguments and return parsed result.

    Args:
        args: Command arguments passed to twitter-cli (e.g. ["post", "hello", "--json"])
        json_output: Whether to append --json flag automatically

    Returns:
        A dict with "ok" and either "data" or "error" keys.
    """
    python = find_python()
    cmd = [python, "-m", "twitter_cli"] + args
    if json_output:
        # Avoid duplicate --json
        if "--json" not in args and "--yaml" not in args:
            cmd.append("--json")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "error": {
                "code": "TIMEOUT",
                "message": "Twitter 请求超时，请稍后重试",
            },
        }
    except FileNotFoundError:
        return {
            "ok": False,
            "error": {
                "code": "NOT_INSTALLED",
                "message": "未检测到 twitter-cli，请先安装：pip install twitter-cli",
            },
        }
    except Exception as e:
        return {
            "ok": False,
            "error": {
                "code": "UNKNOWN",
                "message": f"执行错误: {str(e)}",
            },
        }

    # Parse JSON from stdout if available
    if result.stdout and result.stdout.strip():
        try:
            output = json.loads(result.stdout.strip())
            return output
        except json.JSONDecodeError:
            pass

    # If non-zero exit, try to extract error from stderr
    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else ""
        # Try to extract structured error from stderr
        for line in (stderr.split("\n") if stderr else []):
            if line.strip().startswith("{"):
                try:
                    parsed = json.loads(line.strip())
                    if isinstance(parsed, dict) and "ok" in parsed:
                        return parsed
                except json.JSONDecodeError:
                    pass

        # Fallback error message
        if "authentication" in stderr.lower() or "auth" in stderr.lower():
            return {
                "ok": False,
                "error": {
                    "code": "NOT_LOGGED_IN",
                    "message": "未登录 Twitter，请先在浏览器中登录 Twitter（支持 Arc/Chrome/Edge/Firefox/Brave）",
                },
            }
        if "rate limit" in stderr.lower():
            return {
                "ok": False,
                "error": {
                    "code": "RATE_LIMITED",
                    "message": "发送过于频繁，请稍后再试",
                },
            }

        return {
            "ok": False,
            "error": {
                "code": "CLI_ERROR",
                "message": stderr[:500] if stderr else f"Twitter CLI 返回错误码 {result.returncode}",
            },
        }

    # Zero exit with no output - unexpected
    return {
        "ok": False,
        "error": {
            "code": "UNKNOWN",
            "message": "Twitter CLI 未返回任何输出",
        },
    }


def print_result(result: dict[str, Any]) -> None:
    """Print result as JSON for AI parsing."""
    print(json.dumps(result, ensure_ascii=False))
