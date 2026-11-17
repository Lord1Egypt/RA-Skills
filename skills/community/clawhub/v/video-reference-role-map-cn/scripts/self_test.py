#!/usr/bin/env python3
"""Standalone structural and fixture checks for this Skill."""
from pathlib import Path
import struct
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
required = ["SKILL.md", "manifest.yaml", "agents/openai.yaml", "fixtures/success.md", "fixtures/failure.md", "README.md", "README.en.md", "icon-512.png", "LICENSE", "assets/promo-1600x900.png"]
missing = [p for p in required if not (ROOT / p).is_file()]
if missing:
    print("missing: " + ", ".join(missing)); sys.exit(1)
def png_size(path):
    raw = path.read_bytes()[:24]
    if raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR": raise ValueError(f"invalid PNG: {path.name}")
    return struct.unpack(">II", raw[16:24])
if png_size(ROOT / "icon-512.png") != (512, 512): print("icon-512.png must be 512x512 PNG"); sys.exit(1)
if png_size(ROOT / "assets/promo-1600x900.png") != (1600, 900): print("promo must be 1600x900 PNG"); sys.exit(1)
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
agent = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
for text, label in ((skill, "SKILL.md"), (manifest, "manifest.yaml")):
    if "video-reference-role-map-cn" not in text: print(f"slug absent from {label}"); sys.exit(1)
for key in ("display_name:", "short_description:", "default_prompt:", "icon_small:", "icon_large:"):
    if key not in agent: print(f"agents/openai.yaml lacks {key}"); sys.exit(1)
if "allow_implicit_invocation: true" not in agent: print("agents/openai.yaml policy invalid"); sys.exit(1)
for name in ("success.md", "failure.md"):
    if "| 参考 |" not in (ROOT / "fixtures" / name).read_text(encoding="utf-8"): print(f"fixture {name} lacks delivery table"); sys.exit(1)
# Independent semantic guards for the published reference case. Actual model delivery
# was recorded separately; these guards prevent known sample regressions.
case = json.loads((ROOT / "fixtures/source-limited-input.json").read_text())
assert len(case["success"]["授权素材列表"]) == 3
assert all(x["可见内容"] == "未提供具体描述" for x in case["success"]["授权素材列表"])
result = (ROOT / "fixtures/forward-success.md").read_text()
assert "没有图片或具体可见内容描述" in result
assert "生成要求" in result and "不能当作A/B/C已经呈现" in result
assert "轻快转身缺少动作/时序参考" in result
assert "开始姿态、过程与结束姿态" in result
for invented in ("深色风衣", "蓝紫高反差", "肩向右", "短发"):
    assert invented not in result, invented
for name in ("success", "failure"):
    delivered = (ROOT / f"fixtures/forward-{name}.md").read_text()
    public = (ROOT / f"fixtures/{name}.md").read_text()
    assert public.split("## 参考交付\n", 1)[1].strip() == delivered.strip()
print("PASS: package, original limited-material case, and published delivery regression guards passed. Actual behavior is recorded separately.")
