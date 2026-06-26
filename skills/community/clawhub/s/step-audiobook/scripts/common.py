#!/usr/bin/env python3

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path
from typing import Any

import yaml


DEFAULT_WORKSPACE_DIR = (Path(__file__).resolve().parent / "../../..").resolve()
DEFAULT_LIBRARY_PATH = (Path(__file__).resolve().parent / "../../.." / "audiobook-library" / "voice-library.yaml").resolve()


def load_yaml_if_exists(file_path: str | Path, fallback: Any = None) -> Any:
    path = Path(file_path)
    if not path.exists():
        return fallback

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data


def load_yaml(file_path: str | Path) -> Any:
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def save_yaml(file_path: str | Path, value: Any) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(value, handle, allow_unicode=True, sort_keys=False)


def load_json_if_exists(file_path: str | Path, fallback: Any = None) -> Any:
    path = Path(file_path)
    if not path.exists():
        return fallback

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_json(file_path: str | Path) -> Any:
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(file_path: str | Path, value: Any) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def resolve_path(root_dir: str | Path, target: str | Path) -> Path:
    candidate = Path(target)
    if candidate.is_absolute():
        return candidate
    return Path(root_dir).resolve() / candidate


def resolve_artifact_dir(anchor: str | Path, dir_name: str = ".audiobook") -> Path:
    path = Path(anchor).resolve()
    base_dir = path if path.is_dir() else path.parent
    if base_dir.name == dir_name:
        return base_dir
    return base_dir / dir_name


def is_relative_to(path: str | Path, root: str | Path) -> bool:
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except ValueError:
        return False


def strip_story_suffixes(name: str) -> str:
    value = str(name or "")
    for suffix in (".tts-requests", ".casting-plan", ".structured-script"):
        if value.endswith(suffix):
            return value[: -len(suffix)]
    return value


def slugify_story_name(name: str) -> str:
    normalized = re.sub(r"[^0-9A-Za-z\u4e00-\u9fa5-]+", "-", str(name or "").strip().lower())
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized or "audiobook"


def get_story_base_name(path: str | Path) -> str:
    return strip_story_suffixes(Path(path).resolve().stem)


def get_story_slug(path: str | Path) -> str:
    return slugify_story_name(get_story_base_name(path))


def get_story_run_dir(path: str | Path, skill_name: str = "audiobook") -> Path:
    return DEFAULT_WORKSPACE_DIR / "runs" / skill_name / get_story_slug(path)


def resolve_story_workspace_dir(anchor: str | Path, skill_name: str = "audiobook") -> Path:
    path = Path(anchor).resolve()
    base_dir = path if path.is_dir() else path.parent
    runs_root = DEFAULT_WORKSPACE_DIR / "runs" / skill_name

    if base_dir.name == ".audiobook" and is_relative_to(base_dir.parent, runs_root):
        return base_dir.parent

    if is_relative_to(base_dir, runs_root):
        return base_dir

    return get_story_run_dir(path, skill_name=skill_name)


def ensure_dir(dir_path: str | Path) -> None:
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def sha256_file(file_path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(file_path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_env_text(text: str) -> dict[str, str]:
    env: dict[str, str] = {}
    for raw_line in str(text or "").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        env[key.strip()] = value
    return env


def find_upward(start_dir: str | Path, file_name: str) -> Path | None:
    current = Path(start_dir).resolve()
    while True:
        candidate = current / file_name
        if candidate.exists():
            return candidate
        if current.parent == current:
            return None
        current = current.parent


def resolve_step_api_key(search_dirs: list[str | Path]) -> dict[str, str | None]:
    return resolve_api_key(search_dirs, "STEP_API_KEY")


def describe_api_key_source(env_key: str, source_kind: str) -> str:
    normalized_kind = str(source_kind or "").strip().lower()
    if normalized_kind == "process_env":
        return f"process.env.{env_key}"
    if normalized_kind == "dotenv":
        # Keep the provenance signal, but never expose the real .env path.
        return f"dotenv:.env:{env_key}"
    return normalized_kind or "unknown"


def resolve_api_key(search_dirs: list[str | Path], env_key: str) -> dict[str, str | None]:
    import os

    if os.environ.get(env_key):
        return {
            "value": os.environ[env_key],
            "source": describe_api_key_source(env_key, "process_env"),
        }

    visited: set[Path] = set()
    for directory in search_dirs:
        env_path = find_upward(directory, ".env")
        if not env_path or env_path in visited:
            continue
        visited.add(env_path)
        env = parse_env_text(env_path.read_text(encoding="utf-8"))
        if env.get(env_key):
            return {
                "value": env[env_key],
                "source": describe_api_key_source(env_key, "dotenv"),
            }

    return {"value": "", "source": None}


def trim_string(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def normalize_string_array(value: Any) -> list[str]:
    if isinstance(value, list):
        result: list[str] = []
        seen: set[str] = set()
        for item in value:
            text = str(item).strip()
            if text and text not in seen:
                seen.add(text)
                result.append(text)
        return result

    if isinstance(value, str):
        normalized = value
        for separator in ("、", "，", ",", "；", ";", "/", "|"):
            normalized = normalized.replace(separator, "\n")
        result = []
        seen = set()
        for part in normalized.splitlines():
            text = part.strip()
            if text and text not in seen:
                seen.add(text)
                result.append(text)
        return result

    return []


def format_value(value: Any) -> str:
    text = str(value or "").strip()
    return text or "（空）"


def format_list(items: list[str]) -> str:
    return " / ".join(items) if items else "（空）"
