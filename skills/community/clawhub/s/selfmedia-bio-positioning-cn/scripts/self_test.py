#!/usr/bin/env python3
"""Validate package structure and fixture contracts; no copy-generation engine is bundled."""
from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "selfmedia-bio-positioning-cn"

def need(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def png_size(path: Path) -> tuple[int, int]:
    raw = path.read_bytes()
    need(raw[:8] == b"\x89PNG\r\n\x1a\n", f"{path.name} is not PNG")
    return struct.unpack(">II", raw[16:24])

def is_real_credential(value: object) -> bool:
    """Reject an aspiration as a credential; substantive inputs are reviewed by the Skill."""
    if not isinstance(value, str) or not value.strip():
        return False
    return value.strip() not in {"想开始做自媒体", "想做自媒体"}

def main() -> int:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
    agent = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    need(f"name: {SLUG}" in skill.split("---", 2)[1], "SKILL frontmatter name")
    need(f"name: {SLUG}" in manifest and f"slug: {SLUG}" in manifest, "manifest identity")
    need("self_test: \"python3 scripts/self_test.py\"" in manifest, "runnable self_test command")
    need("allow_implicit_invocation: true" in agent, "boolean invocation policy")
    description_match = re.search(r'^  short_description: "([^\n"]+)"$', agent, re.M)
    need(description_match is not None, "interface short_description present")
    description = description_match.group(1)
    need(25 <= len(description) <= 64, "interface short_description length")
    need("icon: icon-512.png" in manifest, "manifest root icon reference")
    for asset, size in (("icon-512.png", (512, 512)), ("assets/icon-512.png", (512, 512)), ("assets/promo-1600x900.png", (1600, 900))):
        need(png_size(ROOT / asset) == size, f"{asset} dimensions")
    success = json.loads((ROOT / "fixtures/success.json").read_text(encoding="utf-8"))
    failed = json.loads((ROOT / "fixtures/failure-missing-fields.json").read_text(encoding="utf-8"))
    required = ("真实资历", "内容方向", "目标受众")
    need(all(success.get(key) for key in required), "success fixture must be complete")
    expected_success = success.get("预期结果", {})
    need(len(expected_success.get("主页简介", [])) == 3, "success fixture must expect three bios")
    need(3 <= len(expected_success.get("栏目定位", [])) <= 5, "success fixture must expect 3-5 content pillars")
    need(len(expected_success.get("置顶内容建议", [])) == 3, "success fixture must expect three pinned suggestions")
    actual = (ROOT / "fixtures/forward-success.md").read_text(encoding="utf-8")
    need(all(success[key] in actual for key in required), "forward output preserves all supplied facts")
    need(all("经营一家社区烘焙小店 4 年" in bio for bio in expected_success["主页简介"]), "bios preserve the supplied four-year credential")
    need("主理人" not in actual and not re.search(r"第\s*4\s*年", actual), "forward output must not invent identity or change duration")
    need(all(column.get("标记") == "建议" for column in expected_success["栏目定位"]), "every proposed column is labeled as a suggestion")
    need(actual.count("### 建议栏目") == len(expected_success["栏目定位"]), "every forward column is individually labeled")
    for invented in ("担心口感", "不知道如何安排备货", "难以理解真实经营决策"):
        need(invented not in actual, "forward output must not invent an audience pain point")

    missing = [key for key in required if not (is_real_credential(failed.get(key)) if key == "真实资历" else failed.get(key))]
    expected_failure = failed.get("预期结果", {})
    need(missing == ["真实资历", "内容方向", "目标受众"], "failure fixture must expose all missing fields")
    need(expected_failure.get("缺失项") == missing, "failure fixture expected missing fields")
    need(len(expected_failure.get("补充问题", [])) == len(missing), "failure fixture must expect one question per missing field")
    need(expected_failure.get("不应生成") == ["主页简介", "栏目定位", "置顶内容建议"], "failure fixture must forbid deliverables")
    failure_output = (ROOT / "fixtures/forward-failure.md").read_text(encoding="utf-8")
    need(all(key in failure_output for key in missing), "forward failure identifies all absent/invalid fields")
    need(not re.search(r'^#{1,3} (?:版本|建议栏目)', failure_output, re.M), "incomplete input does not receive finished bios or columns")
    print("PASS: structure and fixture contracts validated.")
    print("NOTE: this checks expected fixture data, not real Skill behavior; generated copy and factual accuracy need user review.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
