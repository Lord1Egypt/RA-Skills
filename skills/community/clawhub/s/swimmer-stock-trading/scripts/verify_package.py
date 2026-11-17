#!/usr/bin/env python3
"""Fail closed when required ClawHub package files or references are missing."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
REQUIRED = {
    ".clawhubignore",
    "README.md",
    "SKILL.md",
    "agents/openai.yaml",
    "config.example.json",
    "references/balances.md",
    "references/custody-and-settlement.md",
    "references/keypair-setup.md",
    "references/protocol.md",
    "references/wallet-submission.md",
    "scripts/requirements.txt",
    "scripts/solana_sign_send.py",
    "scripts/verify_package.py",
    "tests/test_solana_sign_send.py",
}
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    present = {
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    missing = sorted(REQUIRED - present)
    if missing:
        fail(f"required package files missing: {', '.join(missing)}")

    for markdown in ROOT.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            target = target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (markdown.parent / target).resolve().is_file():
                fail(f"broken relative link in {markdown.relative_to(ROOT)}: {target}")

    config = json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))
    if not str(config.get("private_key", "")).startswith("REPLACE_"):
        fail("config.example.json must contain only a private-key placeholder")
    if config.get("trusted_stock_mints") != {} or config.get("max_offer_raw_by_mint") != {}:
        fail("config template policy maps must be empty, not unverified examples")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    signer = (ROOT / "scripts/solana_sign_send.py").read_text(encoding="utf-8")
    required_phrases = ["filesystem: true", "network: true", "not an atomic", "irreversible"]
    for phrase in required_phrases:
        if phrase.lower() not in skill.lower():
            fail(f"SKILL.md is missing security disclosure: {phrase}")
    for forbidden in ['add_argument("--config"', 'add_argument("--stock-mint"']:
        if forbidden in signer:
            fail(f"signer exposes forbidden capability: {forbidden}")
    print(f"Package verified: {len(present)} text files present; all required files and links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
