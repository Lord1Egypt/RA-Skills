#!/usr/bin/env python3
"""Fail-fast sensitive information scanner for this repository."""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BLOCK_PATTERNS = [
    ("OpenAI key", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("Telegram-style negative chat id", re.compile(r"(?<!\d)-\d{8,}")),
    ("Long numeric user/chat id", re.compile(r"\b\d{8,}\b")),
    ("Private local absolute path", re.compile(r"/root/|/home/[^/]+/|~/.openclaw/")),
    ("Private email hint", re.compile(r"[A-Za-z0-9._%+-]+@(qq\.com|gmail\.com|alibaba-inc\.com)")),
]

ALLOWLIST_SNIPPETS = [
    "target=\"<chat_id>\"",
    "replyTo=\"<message_id>\"",
    "Wenzhuang Zhu",
    "TetraClaw",
    "tetraclaw@local",
    "openclaw-assistant@local",
    "STICKER_MANAGER_DIR",
    "STICKER_MANAGER_INBOUND_DIR",
    "STICKER_MANAGER_LANG",
    "STICKER_MANAGER_VISION_MODELS",
    "~/.openclaw/workspace/stickers/library/",
    "~/.openclaw/media/inbound/",
    "Private local absolute path",
    "token = \"ghp_example_token_not_real\"",
    "token = \"ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcd\"",
    "token = \\\"ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcd\\\"",
    "line = '/root/EXAMPLE_PATH'",
    "/root/EXAMPLE_PATH/",
]

TEXT_EXTS = {".md", ".py", ".txt", ".yml", ".yaml", ".ini", ".toml", ".json", ".sample", ".gitignore", ""}
EXCLUDED_PREFIXES = [
    ".git/",
    ".pytest_cache/",
    "__pycache__/",
    "scripts/check_sensitive.py",
]


def staged_files() -> list[str]:
    out = subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT"], cwd=ROOT, text=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


def should_scan(path: str) -> bool:
    return not any(path.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def read_text(path: Path) -> str | None:
    if path.suffix.lower() not in TEXT_EXTS and path.name not in {"LICENSE", "README", "README.md", "README.zh-CN.md"}:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def is_allowed(line: str) -> bool:
    return any(snippet in line for snippet in ALLOWLIST_SNIPPETS)


def main() -> int:
    problems: list[str] = []
    for rel in staged_files():
        if not should_scan(rel):
            continue
        path = ROOT / rel
        text = read_text(path)
        if text is None:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if is_allowed(line):
                continue
            for label, pattern in BLOCK_PATTERNS:
                if pattern.search(line):
                    problems.append(f"{rel}:{lineno}: {label}: {line.strip()}")
    if problems:
        print("Sensitive information check failed. Review these lines before commit/push:")
        for item in problems:
            print(f"- {item}")
        return 1
    print("Sensitive information check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
