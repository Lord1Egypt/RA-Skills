#!/usr/bin/env python3
"""Check package metadata and fixture contracts; do not simulate qualitative analysis."""
from __future__ import annotations
import json, re, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
def text(name):
    p = ROOT / name
    if not p.is_file(): errors.append(f"missing file: {name}"); return ""
    return p.read_text(encoding="utf-8")
def png(name, expected):
    p = ROOT / name
    try:
        data = p.read_bytes()[:24]
        if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR": raise ValueError("not PNG")
        actual = struct.unpack(">II", data[16:24])
        if actual != expected: errors.append(f"{name} is {actual}, expected {expected}")
    except (OSError, ValueError, struct.error) as e: errors.append(f"invalid {name}: {e}")

skill, manifest, agent = text("SKILL.md"), text("manifest.yaml"), text("agents/openai.yaml")
text("README.md"); text("README.en.md"); text("LICENSE")
fm = re.match(r"^---\n(.*?)\n---", skill, re.S)
if not fm or not re.search(r"^name: shop-review-miner-cn$", fm.group(1), re.M): errors.append("invalid SKILL.md name")
desc = re.search(r"^description: (.+)$", fm.group(1) if fm else "", re.M)
if not desc or not 80 <= len(desc.group(1)) <= 240: errors.append("SKILL description must be 80–240 characters")
for value in ("name: shop-review-miner-cn", "slug: shop-review-miner-cn", "repository: https://github.com/xxjrq/shop-review-miner-cn", "self_test: python3 scripts/self_test.py"):
    if value not in manifest: errors.append(f"manifest missing {value}")
mdesc = re.search(r"^description: (.+)$", manifest, re.M)
if not mdesc or not 80 <= len(mdesc.group(1)) <= 240: errors.append("manifest description must be 80–240 characters")
for value in ("display_name:", "short_description:", "default_prompt:", "icon_small:", "icon_large:", "policy:\n  allow_implicit_invocation: true"):
    if value not in agent: errors.append(f"agents/openai.yaml missing {value}")
short = re.search(r'^  short_description: "(.+)"$', agent, re.M)
if not short or not 25 <= len(short.group(1)) <= 64: errors.append("short_description must be 25–64 characters")
for field in ("display_name", "short_description", "default_prompt", "icon_small", "icon_large"):
    found = re.search(r'^  ' + field + r': "([^"\n]+)"$', agent, re.M)
    if not found:
        errors.append(f"agent field must be quoted: {field}")
        continue
    value = found.group(1)
    if field == "default_prompt" and "$shop-review-miner-cn" not in value:
        errors.append("default_prompt must reference this Skill")
    if field.startswith("icon_"):
        target = (ROOT / value).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
            errors.append("agent icon must exist inside Skill directory")
for value in (
    "商品/作品名称、品类和每条评价原文（均必需）",
    "任一项缺失时，逐项列出缺少字段、对分析的影响与补充方式，停止分析",
    "单条评价只可作为单次信号或个案反馈，不得写为“常见诉求”",
):
    if value not in skill: errors.append(f"SKILL.md missing required input policy: {value}")
png("icon-512.png", (512, 512)); png("assets/promo-1600x900.png", (1600, 900))
try:
    success = json.loads(text("fixtures/success.json")); failure = json.loads(text("fixtures/failure-missing-reviews.json"))
    if not isinstance(success.get("reviews"), list) or not success["reviews"] or not all(x.get("text") for x in success["reviews"]): errors.append("invalid success fixture")
    expected_success = success.get("expected_result", {})
    if expected_success.get("analysis_status") != "complete_with_limited_sample": errors.append("success fixture must declare limited-sample completion")
    if expected_success.get("common_needs") != []: errors.append("success fixture must not label one-off signals as common needs")
    if len(expected_success.get("one_off_signals", [])) < 2: errors.append("success fixture must identify its one-off signals")
    facts, recommendations = expected_success.get("facts_or_feedback"), expected_success.get("recommendations")
    if not isinstance(facts, list) or not facts or not isinstance(recommendations, list) or not recommendations: errors.append("success fixture must separate facts/feedback from recommendations")
    if "reviews" in failure: errors.append("failure fixture must lack reviews")
    expected_failure = failure.get("expected_result", {})
    if expected_failure.get("analysis_status") != "insufficient_input": errors.append("failure fixture must declare insufficient input")
    if "reviews" not in expected_failure.get("missing_fields", []): errors.append("failure fixture must explicitly report missing review text")
    if expected_failure.get("analysis_stopped") is not True: errors.append("failure fixture must stop analysis")
    if not expected_failure.get("forbidden_output_sections"): errors.append("failure fixture must forbid insight sections after a missing required field")
except json.JSONDecodeError as e: errors.append(f"invalid fixture JSON: {e}")
if errors:
    print("SELF-TEST FAILED"); print("\n".join("- " + e for e in errors)); sys.exit(1)
print("SELF-TEST PASSED: package structure and explicit fixture contracts are valid.")
print("Checked fixture semantics: one-off signals are not common needs, facts are separate from recommendations, and missing review text stops analysis.")
print("Note: this does not execute qualitative analysis; validate real outcomes with authorized reviews.")
