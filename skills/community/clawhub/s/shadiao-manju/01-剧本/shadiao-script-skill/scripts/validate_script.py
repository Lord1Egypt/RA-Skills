#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""沙雕剧本校验器（v0.1）

用法：
  python3 validate_script.py 第01集.md
  python3 validate_script.py 第01集.md --json 剧本.json
  python3 validate_script.py 剧本.json --json

检查：
  1. 必备章节：本集目标 / 角色表 / 场景表 / 台词表
  2. 台词表列：序号 | 角色 | 台词 | 情绪 | 音效 | 场景
  3. 序号连续、台词 ≤ 30 字、角色在角色表、场景在场景表、情绪合法
  4. 行数 / 场景数 / 角色数在合理区间
  5. JSON 与 Markdown 是否一致（给了 --json 时）
退出码：0 = 通过（可能有 warning）；1 = 有 error
"""

import argparse
import json
import re
import sys

# 基础情绪（IndexTTS 原生支持，见 02-配音/references/情绪表.md）
BASE_EMOTIONS = {
    "平静", "中性", "开心", "喜悦", "高兴", "惊喜", "惊讶", "压抑", "隐忍",
    "悲伤", "低落", "哽咽", "哭腔", "愤怒", "暴怒", "生气", "惊恐", "害怕",
    "恐惧", "厌恶", "嘲讽", "冷笑", "急切", "催促", "疑惑", "温柔", "慵懒",
    "坚定", "无奈",
}
# 沙雕常用扩展情绪（02 会映射到基础情绪，不直接进引擎）
EXTENDED_EMOTIONS = {
    "得意", "无语", "崩溃", "尴尬", "心虚", "震惊", "委屈", "嫌弃",
    "敷衍", "抓狂", "社死", "摆烂", "震惊",
}
EMOTIONS = BASE_EMOTIONS | EXTENDED_EMOTIONS
NARRATION_SPEAKERS = {"旁白", "叙述", "解说"}
MAX_LINE_CHARS = 30
MIN_LINES, MAX_LINES = 8, 160
MIN_SCENES, MAX_SCENES = 1, 8
MIN_CHARS, MAX_CHARS = 1, 8


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def note(self, msg):
        self.info.append(msg)

    def print(self):
        for m in self.info:
            print(f"  · {m}")
        for m in self.warnings:
            print(f"  ! {m}")
        for m in self.errors:
            print(f"  ✗ {m}")
        print()
        if self.errors:
            print(f"结果：不通过（{len(self.errors)} 个错误，{len(self.warnings)} 个警告）")
        elif self.warnings:
            print(f"结果：通过（{len(self.warnings)} 个警告，建议逐条看）")
        else:
            print("结果：通过")
        return 1 if self.errors else 0


def split_sections(text):
    """按二级标题切段，返回 {标题: 内容}。"""
    sections = {}
    current = None
    buf = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def parse_table(block):
    """解析 Markdown 表格，返回 (header, rows)。"""
    lines = [l.strip() for l in block.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    def cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]
    header = cells(lines[0])
    rows = []
    for line in lines[1:]:
        cs = cells(line)
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cs if c):
            continue
        if len(cs) < len(header):
            cs += [""] * (len(header) - len(cs))
        rows.append(dict(zip(header, cs)))
    return header, rows


def find_section(sections, keyword):
    for title, body in sections.items():
        if keyword in title:
            return title, body
    return None, ""


def is_narration(speaker):
    return speaker.strip().rstrip("：:") in NARRATION_SPEAKERS


def normalize_speaker(speaker):
    return speaker.strip().rstrip("：:")


def parse_markdown(path, rep):
    text = open(path, encoding="utf-8-sig").read()
    sections = split_sections(text)

    for key in ("本集目标", "角色表", "场景表", "台词表"):
        if not find_section(sections, key)[0]:
            rep.error(f"缺少必备章节：## {key}")

    # 角色表
    _, char_body = find_section(sections, "角色表")
    char_header, char_rows = parse_table(char_body)
    characters = []
    for row in char_rows:
        name = (row.get("角色") or "").strip()
        if name:
            characters.append(name)
    if not characters:
        rep.error("角色表为空")
    elif len(characters) > MAX_CHARS:
        rep.warn(f"角色数 {len(characters)} 超过 {MAX_CHARS}，观众可能记不住")
    elif len(characters) < MIN_CHARS:
        rep.error("至少需要 1 个角色")

    # 场景表
    _, scene_body = find_section(sections, "场景表")
    scene_header, scene_rows = parse_table(scene_body)
    scenes = []
    for row in scene_rows:
        sid = (row.get("场景") or row.get("编号") or "").strip()
        if sid:
            scenes.append(sid)
    if not scenes:
        rep.error("场景表为空")
    elif len(scenes) > MAX_SCENES:
        rep.warn(f"场景数 {len(scenes)} 超过 {MAX_SCENES}，建议合并到 2–6 场")

    # 台词表
    title, line_body = find_section(sections, "台词表")
    if not line_body:
        return rep, characters, scenes, []

    header, rows = parse_table(line_body)
    required = ["序号", "角色", "台词", "情绪"]
    for col in required:
        if col not in header:
            rep.error(f"台词表缺少列：{col}（当前表头：{', '.join(header) or '空'}）")

    lines = []
    last_seq = 0
    for i, row in enumerate(rows, start=1):
        seq_raw = (row.get("序号") or "").strip()
        if not seq_raw:
            rep.warn(f"台词第 {i} 行没有序号，已跳过")
            continue
        if not seq_raw.isdigit():
            rep.error(f"台词第 {i} 行序号不是数字：{seq_raw}")
            continue
        seq = int(seq_raw)
        if seq != last_seq + 1 and last_seq != 0:
            rep.warn(f"序号不连续：{last_seq} → {seq}")
        last_seq = seq

        speaker = normalize_speaker(row.get("角色", ""))
        text = (row.get("台词") or "").strip()
        emotion = (row.get("情绪") or "").strip()
        scene = (row.get("场景") or "").strip()
        sfx = (row.get("音效") or "").strip()

        if not text:
            rep.error(f"第 {seq} 行台词为空")
            continue
        clean = re.sub(r"[\s，。！？、；：…—\-—「」『』“”‘’（）()]", "", text)
        if len(clean) > MAX_LINE_CHARS:
            rep.error(f"第 {seq} 行 {len(clean)} 字，超过 {MAX_LINE_CHARS} 字，请拆行")

        if not is_narration(speaker) and speaker not in characters:
            rep.error(f"第 {seq} 行角色「{speaker}」不在角色表")

        if emotion and emotion not in EMOTIONS:
            if not re.fullmatch(r"[\d.,，\s]{15,}", emotion):
                rep.error(f"第 {seq} 行情绪「{emotion}」不在情绪表（见 02-配音/references/情绪表.md）")

        if scene and scene not in scenes:
            rep.error(f"第 {seq} 行场景「{scene}」不在场景表")

        if not sfx:
            pass

        lines.append({
            "seq": seq, "speaker": speaker, "text": text,
            "emotion": emotion, "sfx": sfx, "scene": scene,
        })

    if not lines:
        rep.error("台词表没有可解析的行")
    else:
        if len(lines) < MIN_LINES:
            rep.warn(f"台词只有 {len(lines)} 行，短于 {MIN_LINES} 行，可能撑不到 30 秒")
        if len(lines) > MAX_LINES:
            rep.warn(f"台词 {len(lines)} 行，超过 {MAX_LINES} 行，单集会太长")

        narration = sum(1 for l in lines if is_narration(l["speaker"]))
        ratio = narration / len(lines)
        if ratio < 0.2:
            rep.warn(f"旁白占比 {ratio:.0%}，偏低；纯对白容易丢信息")
        if ratio > 0.8:
            rep.warn(f"旁白占比 {ratio:.0%}，偏高；容易变成有声小说")

        used_scenes = {l["scene"] for l in lines if l["scene"]}
        if len(used_scenes) < len(scenes):
            missing = set(scenes) - used_scenes
            rep.warn(f"场景表里有场景没有台词：{', '.join(sorted(missing))}")

        rep.note(f"角色 {len(characters)} 个；场景 {len(scenes)} 个；台词 {len(lines)} 行；旁白 {ratio:.0%}")

    # 本集目标
    _, goal_body = find_section(sections, "本集目标")
    if goal_body:
        for key in ("钩子", "结尾"):
            if key not in goal_body:
                rep.warn(f"「本集目标」缺少「{key}」")
    return rep, characters, scenes, lines


def check_json(path, md_lines, md_chars, md_scenes, rep):
    try:
        data = json.load(open(path, encoding="utf-8-sig"))
    except Exception as e:
        rep.error(f"JSON 读取失败：{e}")
        return

    for key in ("title", "season", "episode", "characters", "scenes", "lines"):
        if key not in data:
            rep.error(f"JSON 缺少字段：{key}")

    chars = {c.get("name") for c in data.get("characters", []) if c.get("name")}
    scenes = {s.get("id") for s in data.get("scenes", []) if s.get("id")}
    lines = data.get("lines", [])

    if md_chars and chars != set(md_chars):
        rep.warn(f"JSON 角色与 Markdown 不一致：JSON={sorted(chars)} / MD={sorted(md_chars)}")
    if md_scenes and scenes != set(md_scenes):
        rep.warn(f"JSON 场景与 Markdown 不一致：JSON={sorted(scenes)} / MD={sorted(md_scenes)}")

    for i, line in enumerate(lines, start=1):
        seq = line.get("seq", i)
        if not line.get("text"):
            rep.error(f"JSON 第 {seq} 行缺 text")
        speaker = normalize_speaker(line.get("speaker", ""))
        if not is_narration(speaker) and speaker not in chars:
            rep.error(f"JSON 第 {seq} 行角色「{speaker}」不在 characters")
        if line.get("scene") not in scenes:
            rep.error(f"JSON 第 {seq} 行场景「{line.get('scene')}」不在 scenes")
        if line.get("emotion") not in EMOTIONS:
            rep.error(f"JSON 第 {seq} 行情绪「{line.get('emotion')}」不合法")

    if md_lines and len(lines) != len(md_lines):
        rep.warn(f"JSON 台词 {len(lines)} 行 / Markdown {len(md_lines)} 行，不一致")
    elif md_lines:
        # 行数一致还不够：JSON 被改过但 Markdown 没改时，下游会念出没审过的台词
        def norm(t):
            return re.sub(r"[\s，。！？、；：…—\-「」『』“”‘’（）()]", "", (t or ""))

        mismatch = 0
        for jl, ml in zip(lines, md_lines):
            if norm(jl.get("text")) != norm(ml.get("text")):
                mismatch += 1
                rep.error(
                    f"JSON 第 {jl.get('seq', '?')} 行台词与 Markdown 不一致："
                    f"JSON「{(jl.get('text') or '')[:20]}」/ MD「{(ml.get('text') or '')[:20]}」"
                )
        if mismatch:
            rep.error(f"共 {mismatch} 行台词对不上：配音念的是 JSON，会绕过 Markdown 审稿，先对齐再合成")

    rep.note(f"JSON：{len(chars)} 角色 / {len(scenes)} 场景 / {len(lines)} 行")


def main():
    ap = argparse.ArgumentParser(description="沙雕剧本校验器")
    ap.add_argument("path", help="剧本 Markdown 或 JSON 路径")
    ap.add_argument("--json", help="配套的结构化剧本 JSON，用于一致性检查")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    rep = Report()
    if args.path.endswith(".json"):
        target_json = args.path
        md_path = args.json
    else:
        md_path = args.path
        target_json = args.json

    md_lines, md_chars, md_scenes = [], [], []
    if md_path:
        if not md_path.endswith(".md"):
            print("提示：Markdown 路径应以 .md 结尾", file=sys.stderr)
        rep, md_chars, md_scenes, md_lines = parse_markdown(md_path, rep)
    elif target_json:
        pass
    else:
        print("请给一个 .md 或 .json 路径", file=sys.stderr)
        return 2

    if target_json:
        check_json(target_json, md_lines, md_chars, md_scenes, rep)

    print(f"\n校验：{args.path}")
    print("-" * 48)
    return rep.print()


if __name__ == "__main__":
    sys.exit(main())
