#!/usr/bin/env python3
"""Portable structural checks for this Skill; standard library only."""
from pathlib import Path
import re, struct, sys

ROOT = Path(__file__).resolve().parents[1]
SLUG = "selfmedia-interview-question-pack-cn"
errors = []

def read(rel):
    p = ROOT / rel
    if not p.is_file():
        errors.append(f"missing file: {rel}")
        return ""
    return p.read_text(encoding="utf-8")

def has(text, fragment, source):
    if fragment not in text:
        errors.append(f"{source}: missing {fragment!r}")

skill = read("SKILL.md")
manifest = read("manifest.yaml")
agent = read("agents/openai.yaml")
for f in ("README.md", "README.en.md", "fixtures/success.md", "fixtures/failure-missing-input.md", "LICENSE"):
    read(f)
has(skill, f"name: {SLUG}", "SKILL.md")
for x in (f"name: {SLUG}", f"slug: {SLUG}", "icon: icon-512.png", "self_test: python3 scripts/self_test.py", f"repository: https://github.com/xxjrq/{SLUG}"):
    has(manifest, x, "manifest.yaml")
for x in ("interface:", "display_name:", "short_description:", "default_prompt:", "icon_small: icon-512.png", "icon_large: icon-512.png", "policy:", "allow_implicit_invocation: true"):
    has(agent, x, "agents/openai.yaml")
d = re.search(r"^description:\s*(.+)$", manifest, re.M)
if not d or not 80 <= len(d.group(1).strip()) <= 240:
    errors.append("manifest.yaml: description must be 80–240 characters")
s = re.search(r"^\s*short_description:\s*(.+)$", agent, re.M)
if not s or not 25 <= len(s.group(1).strip()) <= 64:
    errors.append("agents/openai.yaml: short_description must be 25–64 characters")

def png_size(rel, expected):
    p = ROOT / rel
    if not p.is_file():
        errors.append(f"missing file: {rel}")
        return
    b = p.read_bytes()
    if b[:8] != b"\x89PNG\r\n\x1a\n" or len(b) < 24:
        errors.append(f"{rel}: invalid PNG")
        return
    size = struct.unpack(">II", b[16:24])
    if size != expected:
        errors.append(f"{rel}: expected {expected[0]}x{expected[1]}, got {size[0]}x{size[1]}")

png_size("icon-512.png", (512, 512))
png_size("assets/promo-1600x900.png", (1600, 900))
# Numeric time budget contract; structural check is distinct from actual interviews.
sample = read("fixtures/success.md")
source_input, delivery = sample.split("## 参考交付", 1)
length = re.search(r"时长：\s*(\d+)\s*分钟", source_input)
rows = []
for line in delivery.splitlines():
    cells = [x.strip() for x in line.strip().strip("|").split("|")]
    if cells and re.fullmatch(r"\d{2}:\d{2}–\d{2}:\d{2}", cells[0]):
        rows.append(cells)
if not rows or not length:
    errors.append("interview budget or timed questions missing")
else:
    previous = 0
    for cells in rows:
        def seconds(stamp):
            minute, second = map(int, stamp.split(":"))
            return minute * 60 + second
        start, end = map(seconds, cells[0].split("–"))
        if start != previous or end <= start:
            errors.append("question times must be contiguous and increasing")
        previous = end
        if len(cells) != 4 or "若" not in cells[2]:
            errors.append("each question needs a conditional follow-up")
    if previous != int(length.group(1)) * 60:
        errors.append("question budget differs from supplied interview duration")
if "品牌公开介绍称" not in delivery or "演讲摘要称" not in delivery:
    errors.append("input source attribution must be retained")

if errors:
    print("SELF-TEST FAILED")
    print("\n".join(f"- {x}" for x in errors))
    sys.exit(1)
print("SELF-TEST PASSED: structure, metadata, fixtures, and image dimensions verified")
