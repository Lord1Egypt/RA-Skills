#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def set_s2_api_key(env_path: Path, api_key: str) -> None:
    if env_path.is_file():
        lines = env_path.read_text(encoding="utf-8").splitlines()
    else:
        lines = []

    updated_lines = []
    replaced = False
    for line in lines:
        if line.strip().startswith("S2_API_KEY="):
            updated_lines.append(f"S2_API_KEY={api_key}")
            replaced = True
        else:
            updated_lines.append(line)

    if not replaced:
        updated_lines.append(f"S2_API_KEY={api_key}")

    env_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Set or overwrite S2_API_KEY in .env")
    parser.add_argument("--api-key", required=True, help="Semantic Scholar API key")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    env_path = Path(__file__).resolve().parent / ".env"
    set_s2_api_key(env_path, args.api_key)
    print(f"S2_API_KEY 已写入 {env_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
