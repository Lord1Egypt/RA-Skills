#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNTIME_HOME = Path.home() / ".uwillberich"
LEGACY_RUNTIME_HOME = Path.home() / ".a-share-decision-desk"
DEFAULT_ENV_PATH = DEFAULT_RUNTIME_HOME / "runtime.env"
LEGACY_ENV_PATH = LEGACY_RUNTIME_HOME / "runtime.env"
DEFAULT_EXAMPLE_ENV = ROOT / "assets" / "runtime.env.example"
DEFAULT_DATA_DIR = DEFAULT_RUNTIME_HOME / "data"
RUNTIME_ENV_VARS = ("UWILLBERICH_RUNTIME_ENV", "A_SHARE_RUNTIME_ENV")
DATA_DIR_ENV_VARS = ("UWILLBERICH_DATA_DIR", "A_SHARE_DECISION_DATA_DIR")
OPTIONAL_KEYS = ("EM_API_KEY",)
EM_INTEGRATIONS = ("MX_FinSearch", "MX_StockPick", "MX_MacroData", "MX_FinData")
EASTMONEY_APPLY_URL = "https://ai.eastmoney.com/mxClaw"
EASTMONEY_HOME_URL = "https://ai.eastmoney.com/nlink/"


def parse_env_text(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values


def read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return parse_env_text(path.read_text(encoding="utf-8"))


def resolve_env_paths(env_path: str | None = None) -> list[Path]:
    paths: list[Path] = []
    if env_path:
        paths.append(Path(env_path).expanduser())
    for env_var in RUNTIME_ENV_VARS:
        custom = os.environ.get(env_var)
        if custom:
            paths.append(Path(custom).expanduser())
    paths.extend([DEFAULT_ENV_PATH, LEGACY_ENV_PATH, ROOT / ".env.local", ROOT / ".env"])

    deduped: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        resolved = str(path.expanduser())
        if resolved in seen:
            continue
        seen.add(resolved)
        deduped.append(Path(resolved))
    return deduped


def load_runtime_env(env_path: str | None = None, override: bool = False) -> dict[str, str]:
    loaded: dict[str, str] = {}
    for path in resolve_env_paths(env_path):
        values = read_env_file(path)
        for key, value in values.items():
            if override or key not in os.environ:
                os.environ[key] = value
                loaded[key] = value
    em_key = os.environ.get("EM_API_KEY", "").strip()
    mx_key = os.environ.get("MX_APIKEY", "").strip()
    if em_key and not mx_key:
        os.environ["MX_APIKEY"] = em_key
        loaded.setdefault("MX_APIKEY", em_key)
    elif mx_key and not em_key:
        os.environ["EM_API_KEY"] = mx_key
        loaded.setdefault("EM_API_KEY", mx_key)
    return loaded


def redact_value(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def build_capabilities() -> dict[str, object]:
    em_ready = bool(os.environ.get("EM_API_KEY") or os.environ.get("MX_APIKEY"))
    return {
        "public_mode": False,
        "em_required_mode": True,
        "em_key_configured": em_ready,
        "em_enhanced_mode": em_ready,
        "available_integrations": list(EM_INTEGRATIONS) if em_ready else [],
    }


def em_key_setup_instructions(script_hint: str | None = None) -> str:
    hint = script_hint or "python3 scripts/runtime_config.py set-em-key --stdin"
    return (
        "EM_API_KEY is required for uwillberich.\n"
        f"Apply here: {EASTMONEY_APPLY_URL}\n"
        "After opening the link, click download and you will see the key.\n"
        f"Official site: {EASTMONEY_HOME_URL}\n"
        "Store the key in ~/.uwillberich/runtime.env, or run:\n"
        f"printf '%s' 'your_em_api_key' | {hint}"
    )


def require_em_api_key(env_path: str | None = None, script_hint: str | None = None) -> str:
    load_runtime_env(env_path)
    key = (os.environ.get("EM_API_KEY") or os.environ.get("MX_APIKEY") or "").strip()
    if key:
        return key
    raise RuntimeError(em_key_setup_instructions(script_hint))


def get_output_root() -> Path:
    load_runtime_env()
    custom = ""
    for env_var in DATA_DIR_ENV_VARS:
        value = (os.environ.get(env_var) or "").strip()
        if value:
            custom = value
            break
    path = Path(custom).expanduser() if custom else DEFAULT_DATA_DIR
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_output_dir(subdir: str | None = None) -> Path:
    root = get_output_root()
    if not subdir:
        return root
    path = root / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_status(env_path: str | None = None) -> dict[str, object]:
    load_runtime_env(env_path)
    env_paths = resolve_env_paths(env_path)
    existing_path = next((str(path) for path in env_paths if path.exists()), "")
    configured_keys = [key for key in OPTIONAL_KEYS if os.environ.get(key)]
    if os.environ.get("MX_APIKEY") and "EM_API_KEY" not in configured_keys:
        configured_keys.append("EM_API_KEY")

    return {
        "runtime_env_path": existing_path or str(env_paths[0]),
        "env_file_exists": bool(existing_path),
        "configured_keys": configured_keys,
        "redacted_values": {key: redact_value(os.environ.get(key, "")) for key in configured_keys},
        "capabilities": build_capabilities(),
        "example_env_path": str(DEFAULT_EXAMPLE_ENV),
        "output_root": str(get_output_root()),
        "eastmoney_apply_url": EASTMONEY_APPLY_URL,
    }


def write_env_file(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}={value}" for key, value in sorted(values.items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)


def set_em_key(path: Path, value: str) -> None:
    values = read_env_file(path)
    values["EM_API_KEY"] = value.strip()
    write_env_file(path, values)
    os.environ["EM_API_KEY"] = value.strip()
    os.environ["MX_APIKEY"] = value.strip()


def unset_em_key(path: Path) -> None:
    values = read_env_file(path)
    values.pop("EM_API_KEY", None)
    write_env_file(path, values)
    os.environ.pop("EM_API_KEY", None)
    os.environ.pop("MX_APIKEY", None)


def print_status(env_path: str | None, as_json: bool) -> int:
    status = build_status(env_path)
    if as_json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 0

    print(f"runtime_env_path: {status['runtime_env_path']}")
    print(f"env_file_exists: {status['env_file_exists']}")
    print(f"configured_keys: {', '.join(status['configured_keys']) or 'none'}")
    print(f"em_required_mode: {status['capabilities']['em_required_mode']}")
    print(f"em_key_configured: {status['capabilities']['em_key_configured']}")
    integrations = status["capabilities"]["available_integrations"]
    print(f"available_integrations: {', '.join(integrations) or 'none until EM_API_KEY is configured'}")
    print(f"eastmoney_apply_url: {status['eastmoney_apply_url']}")
    print(f"output_root: {status['output_root']}")
    return 0


def run_set_em_key(args: argparse.Namespace) -> int:
    value = args.value
    if args.stdin:
        value = sys.stdin.read().strip()
    if not value:
        print("missing --value or --stdin", file=sys.stderr)
        return 1
    env_path = Path(args.env_path).expanduser()
    set_em_key(env_path, value)
    print(f"stored_em_api_key: {env_path}")
    print(f"em_enhanced_mode: {build_capabilities()['em_enhanced_mode']}")
    return 0


def run_unset_em_key(args: argparse.Namespace) -> int:
    env_path = Path(args.env_path).expanduser()
    unset_em_key(env_path)
    print(f"removed_em_api_key: {env_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage local runtime credentials for uwillberich.")
    parser.add_argument(
        "--env-path",
        default=str(DEFAULT_ENV_PATH),
        help="Runtime env file path. Defaults to ~/.uwillberich/runtime.env",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Show credential and capability status.")
    status_parser.add_argument("--json", action="store_true", help="Render status as JSON.")
    status_parser.set_defaults(func=lambda args: print_status(args.env_path, args.json))

    set_parser = subparsers.add_parser("set-em-key", help="Store EM_API_KEY in the local runtime env file.")
    set_parser.add_argument("--value", help="EM_API_KEY value.")
    set_parser.add_argument("--stdin", action="store_true", help="Read EM_API_KEY from stdin.")
    set_parser.set_defaults(func=run_set_em_key)

    unset_parser = subparsers.add_parser("unset-em-key", help="Remove EM_API_KEY from the local runtime env file.")
    unset_parser.set_defaults(func=run_unset_em_key)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
