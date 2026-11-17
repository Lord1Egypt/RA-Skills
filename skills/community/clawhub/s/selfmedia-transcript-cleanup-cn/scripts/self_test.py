#!/usr/bin/env python3
"""Independent contract checks for the bundled reference deliveries."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def must(condition, message):
    if not condition:
        raise AssertionError(message)

def main():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
    agent = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    success = (ROOT / "fixtures" / "success.md").read_text(encoding="utf-8")
    failure = (ROOT / "fixtures" / "failure.md").read_text(encoding="utf-8")
    must("name: selfmedia-transcript-cleanup-cn" in skill, "SKILL slug mismatch")
    must("slug: selfmedia-transcript-cleanup-cn" in manifest, "manifest slug mismatch")
    must((ROOT / "icon-512.png").is_file(), "missing root icon")
    must("我不是说全部不用改，只改两处。" in success, "success loses original meaning")
    must("不得把原意误改为“全部不用改”" in success, "success regression assertion absent")
    must("[待确认：原文“听不清”，无音频证据]" in failure, "failure must retain uncertainty")
    must("不得将待确认词替换为任何品牌" in failure, "failure must forbid guessing")
    must("allow_implicit_invocation: true" in agent, "policy must be boolean true")
    for field in ("display_name:", "short_description:", "default_prompt:", "icon_small:", "icon_large:"):
        must(field in agent, f"missing interface {field}")
    desc = re.search(r"^description: (.+)$", manifest, re.M).group(1)
    must(80 <= len(desc) <= 240, "manifest description length out of range")
    print("self-test passed: reference success and uncertainty-preservation failure contracts verified")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"self-test failed: {error}", file=sys.stderr)
        sys.exit(1)
