#!/usr/bin/env python3
"""Standalone release checks for selfmedia-batch-shoot-plan-cn."""
from pathlib import Path
import re
import json
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
SLUG = "selfmedia-batch-shoot-plan-cn"

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def png_size(path):
    data = (ROOT / path).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise AssertionError(f"{path} is not a PNG with IHDR")
    return struct.unpack(">II", data[16:24])

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def scalar(text, key):
    match = re.search(r"^\s*" + re.escape(key) + r":\s*(.+?)\s*$", text, re.M)
    require(match is not None, f"missing scalar {key}")
    value = match.group(1)
    if value.startswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value

def main():
    for p in ["SKILL.md", "manifest.yaml", "agents/openai.yaml", "README.md", "README.en.md", "LICENSE", "fixtures/success-input.md", "fixtures/success-output.md", "fixtures/failure-input.md", "fixtures/failure-output.md"]:
        require((ROOT / p).is_file(), f"missing {p}")
    skill, manifest, agent, readme, success, failure = map(read, ["SKILL.md", "manifest.yaml", "agents/openai.yaml", "README.md", "fixtures/success-output.md", "fixtures/failure-output.md"])
    require(re.search(r"^name: selfmedia-batch-shoot-plan-cn$", skill, re.M), "SKILL frontmatter name mismatch")
    require(re.search(r"^name: selfmedia-batch-shoot-plan-cn$", manifest, re.M), "manifest name mismatch")
    require(re.search(r"^slug: selfmedia-batch-shoot-plan-cn$", manifest, re.M), "manifest slug mismatch")
    require(all(scalar(text, key).removeprefix("./") == "icon-512.png" for text, key in [(manifest, "icon"), (agent, "icon_small"), (agent, "icon_large")]), "icon references mismatch")
    require("allow_implicit_invocation: true" in agent and "policy:" in agent, "agent policy missing")
    short = scalar(agent, "short_description")
    require(25 <= len(short) <= 64, "short_description must be 25–64 characters")
    for label, text in [("SKILL", skill), ("manifest", manifest)]:
        desc = re.search(r"^description: (.+)$", text, re.M).group(1)
        require(80 <= len(desc) <= 240, f"{label} description must be 80–240 characters")
    require(len(re.findall(r"^  - ", manifest, re.M)) >= 10, "tags and triggers incomplete")
    require("npx skills add xxjrq/selfmedia-batch-shoot-plan-cn" in readme, "install command missing")
    require(png_size("icon-512.png") == (512, 512), "icon must be exactly 512×512")
    require(png_size("assets/promo-1600x900.png") == (1600, 900), "promo must be exactly 1600×900")
    require("保留3秒空镜" not in success and "连续拍3条" not in success, "success fixture must not invent shots or take counts")
    require("项目代号与拍摄日期，才能生成唯一素材文件名" not in failure, "optional project/date must not block scheduling")
    require("成片计划时长" in success and "实际拍摄耗时" in success, "final duration and shoot time must have distinct columns")
    input_rows = [line for line in read("fixtures/success-input.md").splitlines() if line.startswith("| S")]
    input_durations = {}
    for line in input_rows:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        input_durations[cells[0]] = cells[4]
    schedule = success.split("## 拍摄顺序表", 1)[1].split("## 素材命名表", 1)[0]
    actual_rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in schedule.splitlines() if line.startswith("| ") and "| S" in line]
    require(len(actual_rows) == len(input_durations), "schedule must preserve supplied script count")
    for cells in actual_rows:
        require(len(cells) == 9, "schedule must have 9 columns")
        require(cells[6] == input_durations[cells[3]], "final duration must keep original input value")
        require(cells[7] == "待确认", "shoot time is unknown, must not use final duration")
    require("非钟点" in success and "布置、排练、重拍" in success, "unknown production effort must not become clock schedule")
    require("场地/嘉宾可用时段是可选信息" in read("fixtures/forward-failure.md") and "缺失不作为必填失败" in read("fixtures/forward-failure.md"), "optional availability must not be mandatory failure")
    require("待定" in failure, "unknown camera must remain pending")
    extra = json.loads(read("fixtures/forward-additional-input.json"))
    extra_result = read("fixtures/forward-additional.md")
    require(extra["success"]["available_window"] == "10:00–10:20", "independent 20 minute input retained")
    require(sum(x["final_duration_seconds"] for x in extra["success"]["scripts"]) == 15, "independent final-duration input retained")
    require("不能承诺20分钟窗口内完成" in extra_result, "20 minute window cannot imply known shoot duration")
    require("现场布置、排练、拍摄与重拍时间均待确认" in extra_result, "independent shoot costs remain unknown")
    require("缺脚本编号与动作/台词摘要" in extra_result, "additional case missing core fields must stop full delivery")
    optional_input = read("fixtures/failure-input.md")
    optional_output = read("fixtures/failure-output.md")
    require("未提供" in optional_input and "采访区" in optional_input and "嘉宾" in optional_input, "true failure input must retain confirmed fields and missing core values")
    require("并非缺少必填脚本而失败" in read("fixtures/forward-failure.md"), "legacy forward evidence must remain classified as non-failure")
    require("已确认项" in optional_output and "脚本编号" in optional_output and "动作/台词摘要" in optional_output, "true failure output must show known and missing fields")
    require("不生成完整顺序表" in optional_output and "可拍时段和场地映射" in optional_output, "true failure output must stop full delivery only for core omissions")
    print("PASS: release structure, semantic YAML, distinct duration fields, optional-vs-required inputs, true missing-core case, and independent 20-minute case.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
