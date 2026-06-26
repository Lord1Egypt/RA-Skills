#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "settings.json"


def _default_script(name: str) -> Path:
    candidates = {
        "capture": [
            SCRIPT_DIR / "最终完结版.py",
            SCRIPT_DIR / "淘宝skills" / "核心数据" / "最终完结版.py",
            Path.home() / "Desktop" / "最终完结版.py",
            Path.home() / "Desktop" / "淘宝skills" / "核心数据" / "最终完结版.py",
        ],
        "inspection": [
            SCRIPT_DIR / "shop_inspection_fresh_run_universal.py",
            SCRIPT_DIR / "shop_inspection_fresh_run.py",
            Path.home() / "Desktop" / "shop_inspection_fresh_run_universal.py",
            Path.home() / "Desktop" / "shop_inspection_fresh_run.py",
        ],
        "parse": [
            SCRIPT_DIR / "parse_taobao_report.py",
        ],
    }
    for candidate in candidates[name]:
        if candidate.exists():
            return candidate
    return candidates[name][0]


def _resolve_path(raw: str | Path | None, *, base_dir: Path) -> Path | None:
    if raw in (None, ""):
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    return path


def _load_user_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Config must be an object: {config_path}")
    return data


def default_runtime_config() -> dict[str, Any]:
    downloads_dir = SCRIPT_DIR / "downloads"
    output_dir = PROJECT_ROOT / "output"
    return {
        "capture_script": str(_default_script("capture")),
        "inspection_script": str(_default_script("inspection")),
        "parse_script": str(_default_script("parse")),
        "mapping_path": str(PROJECT_ROOT / "mapping.final.json"),
        "downloads_dir": str(downloads_dir),
        "output_dir": str(output_dir),
        "run_log_dir": str(downloads_dir / "run_logs"),
        "license_file": str(PROJECT_ROOT / "license" / "license.json"),
        "inspection_modules": "evaluation,frontend,backend,shipping",
        "storage_state_file": str(SCRIPT_DIR / "yingdao_storage_state.json"),
        "report_name_prefix": "生意参谋报表",
        "version": "1.0.6",
    }


def load_runtime_config(config_path: str | Path | None = None) -> dict[str, Any]:
    config_file = _resolve_path(config_path, base_dir=PROJECT_ROOT) or DEFAULT_CONFIG_PATH
    merged = default_runtime_config()
    merged.update(_load_user_config(config_file))

    path_keys = [
        "capture_script",
        "inspection_script",
        "parse_script",
        "mapping_path",
        "downloads_dir",
        "output_dir",
        "run_log_dir",
        "license_file",
        "storage_state_file",
    ]
    for key in path_keys:
        value = _resolve_path(merged.get(key), base_dir=config_file.parent)
        if value is not None:
            merged[key] = str(value)
    merged["config_path"] = str(config_file)
    return merged


def save_default_config(config_path: str | Path | None = None) -> Path:
    target = _resolve_path(config_path, base_dir=PROJECT_ROOT) or DEFAULT_CONFIG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(default_runtime_config(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return target
