#!/usr/bin/env python3
"""Local-only packaging/security sanity check; no hosted API requests."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
skill = (root / "SKILL.md").read_text(encoding="utf-8")
readme = (root / "README.md").read_text(encoding="utf-8")
assert skill.startswith("---\n")
frontmatter, _, body = skill[4:].partition("\n---\n")
assert body, "SKILL.md frontmatter is unclosed"
assert re.search(r"^name: signallayer-preflight$", frontmatter, re.M)
assert re.search(r"^description: .{50,1024}$", frontmatter, re.M)
assert "https://signallayer.floot.app/_api/v1/agent/preflight" in body
assert "eip155:8453" in body
assert "0x60B3C6c053E926460D1E1053c516c859C95365e6" in body
assert "0.01" in body
assert "private key" in skill.lower()
assert "openclaw skills install git:xavierleterrible-hub/signallayer-preflight@main" in readme
for disallowed in ("mnemonic=", "PRIVATE_KEY=", "sk_live_", "ghp_", "clh_"):
    assert disallowed not in skill + readme, "possible secret in published docs"
for path in ("LICENSE", "scripts/check-offer.mjs", "scripts/offer-terms.mjs", "scripts/test-offer.mjs", "docs/DISTRIBUTION.md", ".github/workflows/validate.yml"):
    assert (root / path).is_file(), path
print("PASS: local Agent Skills packaging checks; no network requests")
