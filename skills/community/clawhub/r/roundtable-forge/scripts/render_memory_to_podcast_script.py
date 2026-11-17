#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 roundtable Memory JSON 渲染为播客文字稿 Markdown。

用法:
    python render_memory_to_podcast_script.py <memory.json> [--output <script.md>]

说明:
    - 输入文件为 roundtable Memory Schema 定义的 JSON。
    - 若 Memory 已包含 podcast_script 对象，优先按其结构渲染。
    - 否则，从 rounds/synthesis 自动转换为播客对话体。
    - 输出文件默认与输入文件同名，扩展名改为 .podcast.md。
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


CHAR_TYPE_LABELS = {
    "real_living": "真实在世人物",
    "real_historical": "历史人物",
    "fictional": "虚构角色",
    "archetype": "典型角色",
}


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="Render a roundtable Memory JSON file to a podcast transcript Markdown."
    )
    parser.add_argument("memory", help="Path to the roundtable Memory JSON file.")
    parser.add_argument(
        "--output",
        "-o",
        help="Path to the output Markdown file. Defaults to <memory>.podcast.md.",
    )
    return parser.parse_args()


def load_memory(path: str) -> dict:
    """加载 Memory JSON 文件。"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_timestamp(iso_string: str) -> str:
    """将 ISO 8601 时间戳格式化为易读字符串。"""
    if not iso_string:
        return ""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return iso_string


def build_character_lookup(characters: list) -> dict:
    """建立角色 id 到角色信息的映射。"""
    return {c["id"]: c for c in characters}


def build_delphi_labels(memory: dict) -> dict:
    """扫描所有发言，提取 character_id 到 anonymous_label 的稳定映射。

    用于德尔菲模式下统一匿名化嘉宾姓名（播客 cast 列表、开场介绍等）。
    同一角色的标签取首次出现值，保证跨轮一致。
    """
    labels = {}
    rounds = memory.get("rounds", [])
    if not isinstance(rounds, list):
        return labels
    for rnd in rounds:
        speeches = rnd.get("speeches", [])
        if not isinstance(speeches, list):
            continue
        for sp in speeches:
            cid = sp.get("character_id", "")
            ctx = sp.get("structure_context") or {}
            label = ctx.get("anonymous_label", "")
            if cid and label and cid not in labels:
                labels[cid] = label
    return labels


def char_type_label(char_type: str) -> str:
    """将角色 type 转换为中文标签。"""
    return CHAR_TYPE_LABELS.get(char_type, char_type)


def is_fusion_thinker(char: dict) -> bool:
    """判断角色是否为融思者，用于渲染视觉标签。"""
    name = char.get("name", "")
    return "融思者" in name


def is_host_character(char: dict, podcast_script: dict) -> bool:
    """判断角色是否为播客 Host。"""
    if podcast_script and char.get("id") == podcast_script.get("host_id"):
        return True
    name = char.get("name", "")
    role = char.get("role", "")
    tags = ["主播", "Host", "host", "主持人"]
    return any(tag in name for tag in tags) or role == "host"


def find_host(characters: list, podcast_script: dict) -> dict:
    """从角色列表中定位 Host。"""
    for char in characters:
        if is_host_character(char, podcast_script):
            return char
    return {}


def estimate_duration(total_words: int) -> str:
    """根据字数估算播客时长（按每分钟 220 字）。"""
    minutes = max(1, round(total_words / 220))
    return f"约 {minutes} 分钟"


def word_count(text: str) -> int:
    """粗略统计中文字数。"""
    return len(re.findall(r"[\u4e00-\u9fff]", text)) + len(text.split())


def render_cast_line(char: dict, is_host: bool = False, delphi_label: str = "") -> str:
    """渲染 shownotes 中的嘉宾一行。

    delphi_label 非空时（德尔菲模式）用它替代真实姓名，保护专家匿名身份。
    """
    name = delphi_label or char.get("name", char.get("id", ""))
    char_type = char_type_label(char.get("type", ""))
    source = char.get("source_domain", "")
    role_tag = "（主播）" if is_host else ""
    source_part = f" / {source}" if source else ""
    return f"- {name}{role_tag} — {char_type}{source_part}"


def render_shownotes(shownotes: dict, characters: list, lookup: dict, memory: dict) -> str:
    """渲染 shownotes 区域（v2.7.0+ production-quality spec）。"""
    if not isinstance(shownotes, dict):
        shownotes = {}
    lines = []
    lines.append("## Shownotes")
    lines.append("")

    lines.append("### 本期嘉宾")
    lines.append("")
    podcast_script = memory.get("podcast_script", {})
    host = find_host(characters, podcast_script)
    delphi_labels = build_delphi_labels(memory)
    for char in characters:
        lines.append(
            render_cast_line(
                char,
                is_host=(char.get("id") == host.get("id")),
                delphi_label=delphi_labels.get(char.get("id"), ""),
            )
        )
    lines.append("")

    lines.append("### 创作者们")
    lines.append("")
    team = shownotes.get("team") or {}
    team_lines = []
    if isinstance(team, dict):
        for role in ("host", "editor", "producer"):
            value = team.get(role, "")
            if value:
                team_lines.append(f"- {role.title()} {value}")
    lines.extend(team_lines or ["- 暂未提供"])
    lines.append("")

    lines.append("### 关于本节目")
    lines.append("")
    about_show = str(shownotes.get("about_show") or "").strip()
    lines.append(about_show or "暂未提供节目简介。")
    lines.append("")

    theme_song = shownotes.get("theme_song")
    if theme_song and any(theme_song.values()):
        lines.append("### 主题曲")
        lines.append("")
        title = theme_song.get("title", "").strip()
        artist = theme_song.get("artist", "").strip()
        license_info = theme_song.get("license", "").strip()
        if title:
            line = f"《{title}》"
            if artist:
                line += f" - {artist}"
            if license_info:
                line += f"（{license_info}）"
            lines.append(line)
        lines.append("")

    sponsor = shownotes.get("sponsor")
    if sponsor and sponsor.get("name"):
        lines.append("### 节目外延 / 商务合作")
        lines.append("")
        lines.append(f"- 合作方：{sponsor.get('name', '')}")
        if sponsor.get("description"):
            lines.append(f"- {sponsor.get('description', '')}")
        lines.append("")

    timestamps = shownotes.get("timestamps", [])
    if timestamps:
        lines.append("### 时间轴")
        lines.append("")
        for ts in timestamps:
            time_label = ts.get("time", "")
            topic = ts.get("topic", "")
            lines.append(f"- {time_label} {topic}")
        lines.append("")

    mid_breaks = shownotes.get("mid_breaks", [])
    if mid_breaks:
        lines.append("### 中场休息")
        lines.append("")
        for brk in mid_breaks:
            lines.append(f"- {brk.get('time', '')} {brk.get('label', '中场休息')}")
        lines.append("")

    resources = shownotes.get("resources", [])
    if resources:
        lines.append("### 参考资源")
        lines.append("")
        for resource in resources:
            if isinstance(resource, dict):
                time_label = resource.get("time", "")
                rtype = resource.get("type", "")
                rtitle = resource.get("title", "")
                rsource = resource.get("source", "")
                line = f"- {time_label} ".lstrip()
                if rtype:
                    line += f"[{rtype}] "
                if rtitle:
                    line += f"《{rtitle}》"
                if rsource:
                    line += f" — {rsource}"
                lines.append(line.rstrip())
            else:
                lines.append(f"- {resource}")
        lines.append("")

    cross_promotion = shownotes.get("cross_promotion", [])
    if cross_promotion:
        lines.append("### 相关节目")
        lines.append("")
        for cp in cross_promotion:
            if isinstance(cp, dict):
                show = cp.get("show", "")
                episode = cp.get("episode", "")
                topic = cp.get("topic", "")
                line_parts = []
                if show: line_parts.append(show)
                if episode: line_parts.append(episode)
                if topic: line_parts.append(topic)
                lines.append(f"- {' / '.join(line_parts)}")
            else:
                lines.append(f"- {cp}")
        lines.append("")

    social = shownotes.get("social")
    if social:
        social_lines = []
        for key in ("website", "xiaohongshu", "wechat", "weibo"):
            value = social.get(key, "")
            if value:
                social_lines.append(f"- {key.title()}: {value}")
        other = social.get("other", [])
        for item in other if isinstance(other, list) else []:
            social_lines.append(f"- {item}")
        if social_lines:
            lines.append("### 互动方式")
            lines.append("")
            lines.extend(social_lines)
            lines.append("")

    lines.append("### 免责声明")
    lines.append("")
    legal_disclaimer = str(shownotes.get("legal_disclaimer") or "").strip()
    lines.append(legal_disclaimer or "本期内容仅供信息交流，不构成专业建议。")
    lines.append("")

    lines.append("### AI 生成说明")
    lines.append("")
    ai_disclaimer = str(shownotes.get("ai_generated_disclaimer") or "").strip()
    lines.append(ai_disclaimer or "本期文本由 AI 辅助生成，请结合原始资料核验。")
    lines.append("")

    return "\n".join(lines)


def render_dialogue_line(speaker_name: str, line: str, stage_direction: str = "") -> str:
    """渲染单句对话。"""
    direction = f" *{stage_direction}*" if stage_direction else ""
    return f"**{speaker_name}**：{line}{direction}"


def _strip_host_prefix(text: str, host_name: str) -> str:
    """防御性：如果用户手写的内容里已经带了 `**host_name**：` 前缀，去掉它。
    适用于 intro / transition / outro —— 这三处都是 Host 独白，渲染器会自动加前缀，
    但用户可能误把前缀写进去了。"""
    if not host_name:
        return text
    stripped = text.lstrip()
    prefix_patterns = [
        f"**{host_name}**：",
        f"**{host_name}**:",
        f"{host_name}：",
        f"{host_name}:",
    ]
    for pattern in prefix_patterns:
        if stripped.startswith(pattern):
            return stripped[len(pattern):].lstrip()
    return text


def render_segment(segment: dict, characters: dict, host_name: str = "") -> str:
    """渲染单个播客章节。"""
    lines = []
    title = segment.get("title", "")
    intro = segment.get("intro", "")
    transition = segment.get("transition", "")
    dialogue = segment.get("dialogue", [])

    if title:
        lines.append(f"## {title}")
        lines.append("")

    if intro:
        intro = _strip_host_prefix(intro, host_name)
        for paragraph in intro.split("\n"):
            if paragraph.strip():
                if host_name and not paragraph.strip().startswith(f"**{host_name}**"):
                    lines.append(f"**{host_name}**：{paragraph.strip()}")
                else:
                    lines.append(paragraph.strip())
        lines.append("")

    for item in dialogue:
        character_id = item.get("character_id", "") or item.get("speaker_id", "")
        speaker_name = item.get("speaker_name", "")
        if not speaker_name:
            speaker_name = characters.get(character_id, {}).get("name", character_id)
        line = item.get("content") or item.get("line", "")
        stage_direction = item.get("stage_direction", "")
        if not line:
            continue
        lines.append(render_dialogue_line(speaker_name, line, stage_direction))
        lines.append("")

    if transition:
        transition = _strip_host_prefix(transition, host_name)
        transition_speaker = f"**{host_name}**：" if host_name else ""
        for paragraph in transition.split("\n"):
            if paragraph.strip():
                lines.append(f"{transition_speaker}{paragraph.strip()}")
        lines.append("")

    return "\n".join(lines)


PODCAST_HAT_LABELS = {
    "blue_open": "开场蓝图（蓝帽）",
    "white": "白帽 · 事实",
    "red": "红帽 · 直觉",
    "yellow": "黄帽 · 价值",
    "black": "黑帽 · 风险",
    "green": "绿帽 · 创意",
    "blue_close": "收束蓝图（蓝帽）",
    "blue": "蓝图（蓝帽）",
}

PODCAST_HAT_INTRO = {
    "blue_open": "我们先用蓝帽框定今天的讨论流程和目标。",
    "white": "现在戴上白帽，我们只看事实和数据，不做判断。",
    "red": "换上红帽，说说直觉、情绪和第一反应。",
    "yellow": "戴上黄帽，我们找找其中的价值和机会。",
    "black": "换上黑帽，我们谨慎地审视风险和问题。",
    "green": "戴上绿帽，我们发散一下创意和替代方案。",
    "blue_close": "最后回到蓝帽，我们把今天的讨论收束起来。",
    "blue": "我们回到蓝帽，梳理一下讨论。",
}

PODCAST_DELPHI_PHASES = {
    "independent": "独立作答",
    "feedback": "反馈修正",
    "convergence": "收敛总结",
}

PODCAST_DELPHI_INTROS = {
    "independent": "接下来进入独立作答环节，各位专家身份匿名，互不知晓彼此立场。",
    "feedback": "现在进入反馈修正环节，我们看看匿名专家们互相回应了哪些观点。",
    "convergence": "最后进入收敛总结环节，我们汇总共识与分歧。",
}

PODCAST_WORLD_CAFE_PHASES = {
    "setup": "分组",
    "rotation_1": "第一轮轮换",
    "rotation_2": "第二轮轮换",
    "rotation_3": "第三轮轮换",
    "harvest": "收获",
}

PODCAST_WORLD_CAFE_INTROS = {
    "setup": "我们先分组入座，每桌选出一位桌主。",
    "rotation_1": "现在进入第一轮讨论，各桌围绕问题展开独立讨论。",
    "rotation_2": "成员轮换到新桌子，桌主先总结上一轮要点，新成员在此基础上展开。",
    "rotation_3": "进入第三轮轮换，继续跨桌交叉授粉。",
    "harvest": "各桌桌主分享累积洞察，我们汇总跨桌共识。",
}

PODCAST_FISHBONE_PHASES = {
    "grouping": "分组",
    "independent_proposal": "独立方案",
    "cross_review": "交叉评审",
    "synthesis": "综合",
}

PODCAST_FISHBONE_INTROS = {
    "grouping": "我们分成几个独立小组，各自拿同一道题。",
    "independent_proposal": "各小组独立产出完整方案，互不沟通。",
    "cross_review": "现在各组交叉评审对方的方案，指出优点和缺口。",
    "synthesis": "最后综合所有方案的精华，形成统一建议。",
}


def extract_hat_from_speech(speech: dict, round_data: dict) -> str:
    """从发言或其所属轮次中提取当前帽子阶段代码。"""
    ctx = speech.get("structure_context") or {}
    hat = ctx.get("current_hat", "")
    if hat:
        return hat
    round_ctx = round_data.get("structure_context") or {}
    return round_ctx.get("current_hat", "")


def is_six_hats_round(round_data: dict) -> bool:
    """判断该轮是否采用六顶思考帽讨论结构。"""
    if round_data.get("discussion_structure") == "six_hats":
        return True
    ctx = round_data.get("structure_context") or {}
    return bool(ctx.get("hat_sequence")) or bool(ctx.get("current_hat"))


def is_delphi_round(round_data: dict) -> bool:
    """判断该轮是否采用德尔菲讨论结构。"""
    if round_data.get("discussion_structure") == "delphi":
        return True
    ctx = round_data.get("structure_context") or {}
    return bool(ctx.get("delphi_phase"))


def is_world_cafe_round(round_data: dict) -> bool:
    """判断该轮是否采用世界咖啡馆讨论结构。"""
    if round_data.get("discussion_structure") == "world_cafe":
        return True
    ctx = round_data.get("structure_context") or {}
    return bool(ctx.get("world_cafe_phase"))


def is_fishbone_round(round_data: dict) -> bool:
    """判断该轮是否采用鱼骨图分组讨论结构。"""
    if round_data.get("discussion_structure") == "fishbone":
        return True
    ctx = round_data.get("structure_context") or {}
    return bool(ctx.get("fishbone_phase"))


def group_speeches_by_hat(speeches: list, round_data: dict) -> list:
    """将发言按连续的帽子阶段分组，返回 [(hat_code, [speeches]), ...]。"""
    groups = []
    current_hat = ""
    bucket = []
    for speech in speeches:
        hat = extract_hat_from_speech(speech, round_data)
        if hat and hat != current_hat:
            if bucket:
                groups.append((current_hat, bucket))
            current_hat = hat
            bucket = [speech]
        else:
            bucket.append(speech)
    if bucket:
        groups.append((current_hat, bucket))
    return groups


def build_auto_segments(memory: dict) -> tuple:
    """从 rounds 自动派生 segments 和 shownotes timestamps。

    返回 (segments, shownotes_timestamps) 元组。当用户提供了
    podcast_script.show_title 但 segments 为空时，调用此函数
    确保播客文字稿始终包含正文对话。
    """
    characters = memory.get("characters", [])
    if not isinstance(characters, list):
        characters = []
    lookup = build_character_lookup(characters)

    segments = []
    time_offset = 0
    shownotes_timestamps = [{"time": "00:00", "topic": "开场"}]
    seg_counter = 0

    def append_segment(title, intro, dialogue, ts_topic):
        nonlocal seg_counter, time_offset
        seg_counter += 1
        segments.append({
            "segment_id": f"ps-{seg_counter:03d}",
            "title": title,
            "intro": intro,
            "dialogue": dialogue,
            "transition": "",
        })
        time_offset += 8
        shownotes_timestamps.append({
            "time": f"{time_offset:02d}:00",
            "topic": ts_topic,
        })

    def speech_to_dialogue(speech):
        char_id = speech.get("character_id", "") or speech.get("speaker_id", "")
        char = lookup.get(char_id, {})
        content = speech.get("content", "") or speech.get("line", "")
        if not content.strip():
            return None
        ctx = speech.get("structure_context") or {}
        speaker_name = ctx.get("anonymous_label") or char.get("name", char_id)
        return {
            "speaker_id": char_id,
            "speaker_name": speaker_name,
            "line": content,
        }

    rounds = memory.get("rounds", [])
    if not isinstance(rounds, list):
        rounds = []
    for round_data in rounds:
        rn = round_data.get("round_number", 0)
        focus = round_data.get("focus_question", f"议题段 {rn}")
        speeches = round_data.get("speeches", [])
        if not isinstance(speeches, list):
            speeches = []
        if not speeches:
            continue

        if is_six_hats_round(round_data):
            for hat_code, phase_speeches in group_speeches_by_hat(speeches, round_data):
                dialogue = [d for d in (speech_to_dialogue(s) for s in phase_speeches) if d]
                if not dialogue:
                    continue
                label = PODCAST_HAT_LABELS.get(hat_code, hat_code or "讨论")
                intro = PODCAST_HAT_INTRO.get(hat_code, f"我们进入{label}环节。")
                append_segment(f"{label}｜{focus}", intro, dialogue, f"{label}：{focus}")
        elif is_delphi_round(round_data):
            phase_ctx = round_data.get("structure_context") or {}
            phase = phase_ctx.get("delphi_phase", "")
            label = PODCAST_DELPHI_PHASES.get(phase, phase or "讨论")
            intro = PODCAST_DELPHI_INTROS.get(phase, f"我们进入{label}环节。")
            dialogue = [d for d in (speech_to_dialogue(s) for s in speeches) if d]
            if not dialogue:
                continue
            append_segment(f"{label}｜{focus}", intro, dialogue, f"{label}：{focus}")
        elif is_world_cafe_round(round_data):
            phase_ctx = round_data.get("structure_context") or {}
            phase = phase_ctx.get("world_cafe_phase", "")
            label = PODCAST_WORLD_CAFE_PHASES.get(phase, phase or "讨论")
            intro = PODCAST_WORLD_CAFE_INTROS.get(phase, f"我们进入{label}环节。")
            dialogue = [d for d in (speech_to_dialogue(s) for s in speeches) if d]
            if not dialogue:
                continue
            append_segment(f"{label}｜{focus}", intro, dialogue, f"{label}：{focus}")
        elif is_fishbone_round(round_data):
            phase_ctx = round_data.get("structure_context") or {}
            phase = phase_ctx.get("fishbone_phase", "")
            label = PODCAST_FISHBONE_PHASES.get(phase, phase or "讨论")
            intro = PODCAST_FISHBONE_INTROS.get(phase, f"我们进入{label}环节。")
            dialogue = [d for d in (speech_to_dialogue(s) for s in speeches) if d]
            if not dialogue:
                continue
            append_segment(f"{label}｜{focus}", intro, dialogue, f"{label}：{focus}")
        else:
            dialogue = [d for d in (speech_to_dialogue(s) for s in speeches) if d]
            if not dialogue:
                continue
            intro = f"好，我们进入下一个话题：{focus}。"
            append_segment(focus, intro, dialogue, focus)

    return segments, shownotes_timestamps


def auto_podcast_script_from_memory(memory: dict) -> dict:
    """当 podcast_script 为空时，从 rounds/synthesis 自动生成。"""
    topic = memory.get("topic", "")
    user_question = memory.get("user_question", "")
    characters = memory.get("characters", [])
    if not isinstance(characters, list):
        characters = []
    podcast_script = memory.get("podcast_script", {})
    host = find_host(characters, podcast_script)
    host_name = host.get("name", "主播")

    show_title = podcast_script.get("show_title") or f"圆桌播客：{topic}"
    tagline = podcast_script.get("tagline") or user_question

    segments, shownotes_timestamps = build_auto_segments(memory)

    synthesis = memory.get("synthesis", {})
    consensus = synthesis.get("consensus", [])
    divergence = synthesis.get("divergence", [])
    open_questions = synthesis.get("open_questions", [])

    outro_lines = [
        f"好，这期关于「{topic}」的圆桌播客就到这里。",
    ]
    if consensus:
        outro_lines.append("我们达成的共识包括：" + "；".join(consensus[:3]) + "。")
    if divergence:
        outro_lines.append("但仍有分歧：" + "；".join(divergence[:3]) + "。")
    if open_questions:
        outro_lines.append("留给听众继续思考的问题：" + "；".join(open_questions[:3]) + "。")
    outro_lines.append("感谢收听，我们下期再见。")
    outro = "\n\n".join(outro_lines)

    delphi_labels = build_delphi_labels(memory)
    host_id = host.get("id", "")

    return {
        "show_title": show_title,
        "tagline": tagline,
        "host_id": host_id,
        "intro_narrative": {
            "context_entry": f"今天我们聊「{topic}」。",
            "guest_intro": "",
            "emotional_promise": "听完这期，希望你对这个问题有新的视角。",
        },
        "structure_mode": "free",
        "segments": segments,
        "outro": outro,
        "shownotes": {
            "cast": [
                render_cast_line(
                    c,
                    c.get("id") == host_id,
                    delphi_labels.get(c.get("id"), ""),
                )
                for c in characters
            ],
            "team": {
                "host": host.get("name", "") if host else "",
                "editor": "",
                "producer": "",
            },
            "about_show": "",
            "timestamps": shownotes_timestamps,
            "resources": [],
            "theme_song": {"title": "", "artist": "", "license": ""},
            "sponsor": {},
            "social": {
                "website": "",
                "xiaohongshu": "",
                "wechat": "",
                "weibo": "",
                "other": [],
            },
            "mid_breaks": [],
            "cross_promotion": [],
            "legal_disclaimer": "本期内容为嘉宾个人观点，不代表所在机构立场。",
            "ai_generated_disclaimer": memory.get("disclaimer", "") or "本圆桌讨论由 AI 生成。",
        },
    }


def render_podcast_script(memory: dict) -> str:
    """将 Memory 数据渲染为完整播客文字稿。"""
    topic = memory.get("topic", "")
    created_at = format_timestamp(memory.get("created_at", ""))
    characters = memory.get("characters", [])
    if not isinstance(characters, list):
        characters = []
    lookup = build_character_lookup(characters)
    disclaimer = memory.get("disclaimer", "")

    podcast_script = memory.get("podcast_script", {})
    if not podcast_script or not podcast_script.get("show_title"):
        podcast_script = auto_podcast_script_from_memory(memory)
        is_fallback_script = True
    else:
        is_fallback_script = False

    show_title = podcast_script.get("show_title", f"圆桌播客：{topic}")
    tagline = podcast_script.get("tagline", "")
    segments = podcast_script.get("segments", [])
    if not isinstance(segments, list):
        segments = []
    outro = podcast_script.get("outro", "")
    shownotes = podcast_script.get("shownotes", {})
    if not isinstance(shownotes, dict):
        shownotes = {}
    host = find_host(characters, podcast_script)
    host_name = host.get("name", "主播")

    if not segments and not is_fallback_script:
        auto_segments, auto_timestamps = build_auto_segments(memory)
        if auto_segments:
            segments = auto_segments
            if isinstance(shownotes, dict) and not shownotes.get("timestamps"):
                shownotes["timestamps"] = auto_timestamps

    lines = []
    lines.append(f"# {show_title}")
    lines.append("")
    if tagline:
        lines.append(f"> {tagline}")
        lines.append("")

    if created_at:
        lines.append(f"*录制时间：{created_at}*")
        lines.append("")

    if disclaimer:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("> **AI 模拟声明**：本圆桌讨论、嘉宾发言、Host 串场均由 AI 生成。所涉及真实人物（包括已故思想家）的发言均为基于公开资料的推演与思想实验，不构成任何真实个人、机构或版权角色的官方立场；请勿用于商业目的或对外冒充真实人物观点。")
        lines.append("")

    has_user_provided_script = not is_fallback_script


    if not has_user_provided_script:
        lines.append("## 开场")
        lines.append("")
        lines.append(f"**{host_name}**：欢迎来到本期圆桌播客。今天我们要聊的是「{topic}」。")
        lines.append("")

        if characters:
            delphi_labels = build_delphi_labels(memory)
            host_id = host.get("id", "")
            guest_names = [
                delphi_labels.get(c.get("id"), "") or c.get("name", c.get("id", ""))
                for c in characters
                if c.get("id") != host_id
            ]
            lines.append(
                f"**{host_name}**：今天坐在我对面的是：{', '.join(guest_names)}。"
            )
            lines.append("")

    if has_user_provided_script:
        intro_narrative = podcast_script.get("intro_narrative", {})
        if intro_narrative and any(intro_narrative.values()):
            lines.append("## 开场")
            lines.append("")
            context_entry = intro_narrative.get("context_entry", "")
            guest_intro = intro_narrative.get("guest_intro", "")
            emotional_promise = intro_narrative.get("emotional_promise", "")
            if context_entry:
                lines.append(f"**{host_name}**：{context_entry}")
                lines.append("")
            if guest_intro:
                lines.append(f"**{host_name}**：{guest_intro}")
                lines.append("")
            if emotional_promise:
                lines.append(f"**{host_name}**：{emotional_promise}")
                lines.append("")

    # 正文
    for segment in segments:
        lines.append(render_segment(segment, lookup, host_name))

    # 结尾：整段一次性渲染为 Host 独白，不再逐段重复 Host 前缀
    if outro:
        lines.append("## 结尾")
        lines.append("")
        outro_text = _strip_host_prefix(outro, host_name).strip()
        if host_name and not outro_text.startswith(f"**{host_name}**"):
            lines.append(f"**{host_name}**：{outro_text}")
        else:
            lines.append(outro_text)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(render_shownotes(shownotes, characters, lookup, memory))

    if disclaimer:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(disclaimer)
    return "\n".join(lines)


def main() -> int:
    """脚本入口。"""
    args = parse_args()
    memory_path = Path(args.memory)
    if not memory_path.exists():
        print(f"Error: Memory file not found: {memory_path}", file=sys.stderr)
        return 1

    memory = load_memory(str(memory_path))
    markdown = render_podcast_script(memory)

    output_path = Path(args.output) if args.output else memory_path.with_suffix(".podcast.md")
    output_path.write_text(markdown, encoding="utf-8")

    total_words = word_count(markdown)
    print(f"Rendered podcast script: {output_path}")
    print(f"Estimated duration: {estimate_duration(total_words)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
