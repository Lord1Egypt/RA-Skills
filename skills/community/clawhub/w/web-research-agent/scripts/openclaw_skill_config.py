"""Helpers for reading persisted OpenClaw skill config."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
import urllib.error
import urllib.request


SKILL_KEY = "openmarlin"
SKILL_KEY_ALIASES = [SKILL_KEY]
PRIMARY_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
DEFAULT_SERVER_URL = "https://api.openmarlin.ai"


def _candidate_config_paths() -> list[Path]:
    return [
        PRIMARY_CONFIG_PATH,
        Path("/data/.clawdbot/openclaw.json"),
    ]


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        raw = path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _skill_entry(config: dict[str, Any]) -> dict[str, Any] | None:
    skills = config.get("skills")
    if not isinstance(skills, dict):
        return None
    entries = skills.get("entries")
    if not isinstance(entries, dict):
        return None
    for key in SKILL_KEY_ALIASES:
        entry = entries.get(key)
        if isinstance(entry, dict):
            return entry
    return None


def load_openclaw_skill_entry() -> tuple[dict[str, Any] | None, str | None]:
    for path in _candidate_config_paths():
        parsed = _load_json(path)
        if not parsed:
            continue
        entry = _skill_entry(parsed)
        if entry is not None:
            return entry, str(path)
    return None, None


def get_skill_env(var_name: str) -> tuple[str | None, str | None]:
    env_value = os.environ.get(var_name, "").strip()
    if env_value:
        return env_value, "process-env"

    entry, config_path = load_openclaw_skill_entry()
    if not entry:
        if var_name == "OPENMARLIN_SERVER_URL":
            return DEFAULT_SERVER_URL, "built-in-default"
        return None, None

    env_block = entry.get("env")
    if not isinstance(env_block, dict):
        if var_name == "OPENMARLIN_SERVER_URL":
            return DEFAULT_SERVER_URL, "built-in-default"
        return None, config_path

    value = env_block.get(var_name)
    if isinstance(value, str) and value.strip():
        return value.strip(), f"openclaw-config:{config_path}"

    if var_name == "OPENMARLIN_SERVER_URL":
        return DEFAULT_SERVER_URL, "built-in-default"

    return None, config_path


def preferred_openclaw_config_path() -> str:
    return str(PRIMARY_CONFIG_PATH)


def build_server_url_setup_message(*, resolved_value: str | None = None, reason: str | None = None) -> str:
    lines: list[str] = []
    if reason:
        lines.append(reason)
    headline = (
        "OpenMarlin is configured, but the current server URL could not be reached."
        if resolved_value
        else "OpenMarlin is not configured yet."
    )
    lines.extend(
        [
            headline,
            "",
            f'OPENMARLIN_SERVER_URL defaults to "{DEFAULT_SERVER_URL}".',
            "Use the bare API origin. Do not include /v1 because the helper scripts add endpoint paths themselves.",
            "",
            "One-off shell setup:",
            f'  export OPENMARLIN_SERVER_URL="{DEFAULT_SERVER_URL}"',
            "",
            f"Persisted OpenClaw config: {preferred_openclaw_config_path()}",
            f'  skills.entries["{SKILL_KEY}"].env.OPENMARLIN_SERVER_URL = "{DEFAULT_SERVER_URL}"',
            "",
            f"If available in your OpenClaw build, prefer `openclaw skills update-config {SKILL_KEY}` or the skill settings UI.",
        ]
    )
    if resolved_value:
        lines.extend(
            [
                "",
                f"Current resolved server URL: {resolved_value}",
                "If that value is wrong, update it and retry the same command.",
            ]
        )
    return "\n".join(lines)


def require_server_url(raw: str) -> str:
    server_url = raw.strip().rstrip("/")
    if not server_url:
        raise SystemExit(build_server_url_setup_message())
    parsed = urllib.parse.urlparse(server_url)
    if parsed.scheme in {"http", "https"} and parsed.netloc.lower() == "openmarlin.ai":
        raise SystemExit(
            build_server_url_setup_message(
                resolved_value=server_url,
                reason=(
                    "OPENMARLIN_SERVER_URL points at the OpenMarlin website frontend. "
                    f"Use the API origin instead: {DEFAULT_SERVER_URL}"
                ),
            )
        )
    return server_url


def build_server_connection_error(server_url: str, reason: str) -> str:
    return build_server_url_setup_message(
        resolved_value=server_url,
        reason=f"Request could not reach the OpenMarlin server: {reason}",
    )


def probe_server_openapi(server_url: str) -> tuple[bool, str]:
    url = f"{server_url.rstrip('/')}/openapi.json"
    request = urllib.request.Request(url, method="GET", headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request) as response:
            return True, f"reachable via GET {url} (HTTP {response.status})"
    except urllib.error.HTTPError as error:
        return False, f"GET {url} returned HTTP {error.code}"
    except urllib.error.URLError as error:
        return False, f"GET {url} failed: {error.reason}"
