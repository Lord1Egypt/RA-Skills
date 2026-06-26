#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "generated",
    "generated-milestone",
    "htmlcov",
}

EXCLUDED_FILES = {
    ".DS_Store",
}

SECRET_PATTERNS = {
    "telegram_bot_token": re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),
    "notion_token": re.compile(r"\bntn_[A-Za-z0-9]{20,}\b"),
    "tavily_token": re.compile(r"\btvly-[A-Za-z0-9_-]{20,}\b"),
    "generic_sk_token": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if path.name in EXCLUDED_FILES:
        return True
    return any(part in EXCLUDED_DIRS for part in rel.parts)


def scan_file(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    findings = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                findings.append(
                    {
                        "type": name,
                        "path": str(path),
                        "line": line_number,
                    }
                )
    return findings


def scan(root: Path) -> list[dict]:
    findings = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or should_skip(path, root):
            continue
        findings.extend(scan_file(path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan the repository for committed secrets.")
    parser.add_argument("--root", default=str(repo_root()))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    findings = scan(root)
    payload = {"status": "ok" if not findings else "failed", "findings": findings}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if findings:
            for item in findings:
                print(f"{item['type']} {item['path']}:{item['line']}")
        else:
            print("no secrets found")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())

