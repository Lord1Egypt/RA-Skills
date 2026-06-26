#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - setup.py diagnoses this before normal use.
    yaml = None


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_DIR = Path(os.path.expanduser("~/.config/social-favorites-to-obsidian"))
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.yaml"


def expand_path(value: str | Path) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(str(value)))).resolve()


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed. Run: python scripts/setup.py --install-python-deps")
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeError(f"{path} must contain a YAML mapping")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed. Run: python scripts/setup.py --install-python-deps")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    template = load_yaml(SKILL_ROOT / "assets" / "config.example.yaml")
    path = expand_path(config_path or DEFAULT_CONFIG_PATH)
    config = deep_merge(template, load_yaml(path))
    config["_config_path"] = str(path)
    return config


def ensure_runtime_dirs(config: dict[str, Any]) -> None:
    data_dir = expand_path(config["data_dir"])
    for platform in ("xhs", "zhihu"):
        for name in ("raw", "notes", "images", "logs"):
            (data_dir / platform / name).mkdir(parents=True, exist_ok=True)
    expand_path(config["config_dir"]).mkdir(parents=True, exist_ok=True)


def load_env_file(path: str | Path) -> int:
    env_path = expand_path(path)
    if not env_path.exists():
        return 0
    loaded = 0
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value
            loaded += 1
    return loaded


def skill_dir(config: dict[str, Any], skill_key: str) -> Path:
    root = expand_path(config.get("hctec", {}).get("skills_root", "~/.openclaw/workspace/skills"))
    name = config.get("hctec", {}).get(skill_key, "")
    return root / name


def python_bin(config: dict[str, Any], skill_key: str | None = None) -> str:
    configured = str(config.get("hctec", {}).get("python") or "").strip()
    if configured:
        return configured
    if skill_key:
        d = skill_dir(config, skill_key)
        venv_py = d / ".venv" / "bin" / "python"
        if venv_py.exists():
            return str(venv_py)
    return sys.executable


def run_json(cmd: list[str], timeout: int = 600) -> dict[str, Any]:
    proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy(), timeout=timeout)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(err or f"command failed: {' '.join(cmd)}")
    raw = (proc.stdout or "").strip()
    if not raw:
        raise RuntimeError(f"empty output: {' '.join(cmd)}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON from {' '.join(cmd)}: {exc}\n{raw[:500]}") from exc


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


INVALID_CHARS = re.compile(r'[\\/:*?"<>|#\[\]]+')


def sanitize_filename(name: str, fallback: str) -> str:
    text = (name or "").strip() or fallback
    text = INVALID_CHARS.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip().rstrip(".")
    return (text[:120] or fallback).strip()


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def script_path(config: dict[str, Any], skill_key: str, relative: str) -> Path:
    path = skill_dir(config, skill_key) / "scripts" / relative
    if not path.exists():
        raise RuntimeError(f"missing dependency script: {path}")
    return path
