#!/usr/bin/env python3
"""Package/fixture validation only; it does not simulate model reasoning."""
from __future__ import annotations
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "video-character-reference-pack-cn"

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)

def require(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")

def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        fail("icon-512.png is not a valid PNG")
    return struct.unpack(">II", data[16:24])

def main() -> None:
    skill = require(ROOT / "SKILL.md")
    manifest = require(ROOT / "manifest.yaml")
    agent = require(ROOT / "agents/openai.yaml")
    require(ROOT / "README.md")
    require(ROOT / "README.en.md")
    for asset in (ROOT / "icon-512.png", ROOT / "assets/icon-512.png", ROOT / "assets/promo-1600x900.png"):
        if not asset.is_file():
            fail(f"missing required asset: {asset.relative_to(ROOT)}")
    require(ROOT / "LICENSE")
    for text, label in [(skill, "SKILL.md"), (manifest, "manifest.yaml")]:
        if f"name: {SLUG}" not in text:
            fail(f"{label} name must be {SLUG}")
    if f"slug: {SLUG}" not in manifest:
        fail("manifest slug is incorrect")
    if "license: MIT-0" not in manifest:
        fail("manifest license must be MIT-0")
    if "MIT No Attribution" not in require(ROOT / "LICENSE"):
        fail("LICENSE must declare MIT-0")
    if "[MIT-0](LICENSE)" not in require(ROOT / "README.md") or "[MIT-0](LICENSE)" not in require(ROOT / "README.en.md"):
        fail("README license labels must match MIT-0")
    for field in ("display_name:", "short_description:", "default_prompt:", "icon_small: assets/icon-512.png", "icon_large: assets/icon-512.png"):
        if field not in agent:
            fail(f"agents/openai.yaml lacks {field}")
    if "allow_implicit_invocation: true" not in agent:
        fail("agents/openai.yaml policy is invalid")
    short = next(line.split(":", 1)[1].strip() for line in agent.splitlines() if "short_description:" in line)
    if not 25 <= len(short) <= 64:
        fail("short_description must be 25–64 characters")
    icon = ROOT / "assets/icon-512.png"
    if png_size(icon) != (512, 512):
        fail("icon-512.png must be exactly 512x512")
    promo = ROOT / "assets/promo-1600x900.png"
    if png_size(promo) != (1600, 900):
        fail("promo-1600x900.png must be exactly 1600x900")
    success = json.loads(require(ROOT / "fixtures/success-input.json"))
    if set(success) != {"authorized_reference_description", "story", "costume_constraints"} or not all(success.values()):
        fail("success fixture must contain all non-empty required inputs")
    success_text = require(ROOT / "fixtures/success-expected.md")
    required_success_sections = (
        "## 使用范围",
        "- 资料状态：",
        "## 已知事实",
        "## 服装基线",
        "- 色彩与材质：",
        "- 必须保留：",
        "## 动作与表演约束",
        "- 视线与姿态：",
        "- 禁用动作：",
        "## 跨镜头一致性检查",
        "## 建议（非已知事实）",
    )
    missing_sections = [item for item in required_success_sections if item not in success_text]
    if missing_sections:
        fail("success fixture lacks required delivery items: " + ", ".join(missing_sections))
    suggestion_marker = "## 建议（非已知事实）"
    if any(action in success_text[:success_text.index(suggestion_marker)] for action in ("翻阅", "展示", "轻放")):
        fail("unsupported actions must not appear as known facts in the success fixture")
    suggestions = success_text[success_text.index(suggestion_marker):]
    if not all(action in suggestions for action in ("翻阅", "展示", "轻放")) or "建议：" not in suggestions:
        fail("optional actions must be explicitly labelled as suggestions")
    failed = json.loads(require(ROOT / "fixtures/failure-missing-story.json"))
    failure_text = require(ROOT / "fixtures/failure-expected.md")
    if "story" in failed or "缺少：故事" not in failure_text or "不推断" not in failure_text:
        fail("failure fixture must explicitly report the missing story without invention")
    print("PASS: package structure and fixture checks passed (not a model-behavior test).")

if __name__ == "__main__":
    main()
