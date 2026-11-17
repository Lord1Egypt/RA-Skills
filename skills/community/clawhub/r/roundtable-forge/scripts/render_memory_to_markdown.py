#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 roundtable Memory JSON 渲染为人类可读的 Markdown 圆桌讨论记录。

用法:
    python render_memory_to_markdown.py <memory.json> [--output <report.md>]

说明:
    - 输入文件为 roundtable Memory Schema 定义的 JSON。
    - 输出文件默认与输入文件同名，扩展名改为 .md。
    - 输出包含议题背景、与会角色、逐段发言、回应关系、发言意向、
      议题段小结、合成、如何继续与免责声明。
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


CHAR_TYPE_LABELS = {
    "real_living": "真实在世人物",
    "real_historical": "历史人物",
    "fictional": "虚构角色",
    "archetype": "典型角色",
}


ACTION_LABELS = {
    "independent": "独立发言",
    "extend": "延伸",
    "rebut": "反驳",
    "question": "追问",
    "interrupt": "插话",
    "pivot": "换角度",
    "pass": "暂止",
}


INTENT_LABELS = {
    "extend": "想延伸",
    "rebut": "想反驳",
    "question": "想追问",
    "pivot": "想换角度",
    "pass": "暂不发言",
}


HAT_LABELS = {
    "blue_open": "蓝帽 · 开场（流程管控）",
    "white": "白帽 · 事实与数据",
    "red": "红帽 · 情绪与直觉",
    "yellow": "黄帽 · 价值与乐观",
    "black": "黑帽 · 风险与谨慎",
    "green": "绿帽 · 创意与替代",
    "blue_close": "蓝帽 · 收束（综合判断）",
    "blue": "蓝帽 · 流程管控",
}


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="Render a roundtable Memory JSON file to a readable Markdown report."
    )
    parser.add_argument("memory", help="Path to the roundtable Memory JSON file.")
    parser.add_argument(
        "--output",
        "-o",
        help="Path to the output Markdown file. Defaults to <memory>.md.",
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


def char_type_label(char_type: str) -> str:
    """将角色 type 转换为中文标签。"""
    return CHAR_TYPE_LABELS.get(char_type, char_type)


def action_label(action_type: str) -> str:
    """将 action_type 转换为中文标签。"""
    return ACTION_LABELS.get(action_type, action_type)


def intent_label(intent_type: str) -> str:
    """将 intent_type 转换为中文标签。"""
    return INTENT_LABELS.get(intent_type, intent_type)


def hat_label(hat_code: str) -> str:
    """将帽子代号转换为中文标签，未知代号原样返回。"""
    return HAT_LABELS.get(hat_code, hat_code)


def extract_hat(speech: dict, round_data: dict) -> str:
    """从 speech 或 round 的 structure_context 中提取当前帽子代号。"""
    ctx = speech.get("structure_context") or {}
    hat = ctx.get("current_hat", "")
    if hat:
        return hat
    round_ctx = round_data.get("structure_context") or {}
    return round_ctx.get("current_hat", "")


def group_speeches_by_hat(speeches: list, round_data: dict) -> list:
    """将六顶思考帽模式下的发言按帽子阶段分组。

    返回 [(hat_code, [speech, ...]), ...]，保持原始顺序。
    """
    groups = []
    current_hat = ""
    current_bucket = []
    for speech in speeches:
        hat = extract_hat(speech, round_data)
        if hat and hat != current_hat:
            if current_bucket:
                groups.append((current_hat, current_bucket))
            current_hat = hat
            current_bucket = [speech]
        else:
            current_bucket.append(speech)
    if current_bucket:
        groups.append((current_hat, current_bucket))
    return groups


def is_fusion_thinker(char: dict) -> bool:
    """判断角色是否为融思者，用于渲染视觉标签。"""
    name = char.get("name", "")
    return "融思者" in name


def render_character(char: dict) -> str:
    """渲染单个角色介绍。"""
    name = char.get("name", char.get("id", ""))
    char_type = char_type_label(char.get("type", ""))
    source = char.get("source_domain", "")
    expertise_raw = char.get("expertise", "")
    if isinstance(expertise_raw, (list, tuple)):
        expertise = ", ".join(str(item) for item in expertise_raw)
    else:
        expertise = str(expertise_raw)
    reason = char.get("invited_reason", "")
    fusion_tag = "[融思者] " if is_fusion_thinker(char) else ""
    return (
        f"- **{fusion_tag}{name}**（{char_type}）\n"
        f"  - 来源：{source}\n"
        f"  - 专长：{expertise}\n"
        f"  - 入席原因：{reason}\n"
    )


def build_speech_id(round_number: int, speech_index: int) -> str:
    """生成发言锚点 ID。"""
    return f"s{round_number}e{speech_index + 1}"


def build_round_anchor(round_number: int) -> str:
    """生成议题段锚点。"""
    return f"round-{round_number}"


def render_toc(rounds: list) -> str:
    """渲染目录导航。"""
    lines = []
    lines.append("## 目录")
    lines.append("")
    lines.append("- [议题背景](#议题背景)")
    lines.append("- [与会角色](#与会角色)")
    lines.append("- [讨论过程](#讨论过程)")
    for round_data in rounds:
        rn = round_data.get("round_number", 0)
        anchor = build_round_anchor(rn)
        focus = round_data.get("focus_question", f"议题段 {rn}")
        lines.append(f"  - [议题段 {rn}：{focus}](#{anchor})")
    lines.append("- [合成](#合成)")
    lines.append("- [如何继续](#如何继续)")
    lines.append("")
    return "\n".join(lines)


def generate_round_summary(round_data: dict, characters: dict, anonymous: bool = False) -> str:
    """基于本段发言生成简要的 Conductor 小结。

    anonymous 为 True 时（德尔菲模式）用匿名标签替代真实姓名，避免在小结
    文本里泄露发言者身份。
    """
    focus = round_data.get("focus_question", "")
    speeches = round_data.get("speeches", [])
    if not isinstance(speeches, list):
        speeches = []
    if not speeches:
        return ""

    names = []
    key_themes = []
    tensions = []

    for speech in speeches:
        char_id = speech.get("character_id", "")
        if anonymous:
            ctx = speech.get("structure_context") or {}
            char_name = ctx.get("anonymous_label") or characters.get(char_id, {}).get("name", char_id)
        else:
            char_name = characters.get(char_id, {}).get("name", char_id)
        if char_name not in names:
            names.append(char_name)
        action = speech.get("action_type", "independent")
        if action in ("rebut", "question", "interrupt"):
            tensions.append(f"{char_name} 对前文进行了{action_label(action)}")
        for kp in speech.get("key_points", [])[:1]:
            key_themes.append(f"{char_name} 提出：{kp}")

    lines = []
    lines.append(f"**本段小结**：围绕「{focus}」，{', '.join(names)} 先后发言。")
    if key_themes:
        lines.append("主要视角包括：" + "；".join(key_themes[:4]) + "。")
    if tensions:
        lines.append("核心张力：" + "；".join(tensions[:3]) + "。")
    lines.append("")
    return " ".join(lines)


def render_speech_block(speech: dict, characters: dict, round_number: int, idx: int, all_speeches: list, anonymous: bool = False) -> list:
    """渲染单条发言的完整 Markdown 行（含锚点、回应关系、内容、要点）。

    anonymous 为 True 时（德尔菲模式）优先用 anonymous_label 替代真实姓名，
    同时把 responds_to 指向的目标发言者也匿名化，确保回应关系不泄露身份。
    """
    lines = []
    char_id = speech.get("character_id", "")
    char = characters.get(char_id, {})
    char_name = char.get("name", char_id)
    if anonymous:
        ctx = speech.get("structure_context") or {}
        char_name = ctx.get("anonymous_label") or char_name
    fusion_tag = "[融思者] " if is_fusion_thinker(char) else ""
    action = action_label(speech.get("action_type", "independent"))
    responds_to = speech.get("responds_to")
    speech_id = speech.get("speech_id") or build_speech_id(round_number, idx)
    responds_text = ""
    if responds_to:
        responds_text = f"（[回应 → {responds_to}](#{responds_to})）"
    lines.append(f'<p id="{speech_id}"></p>')
    lines.append(f"**{fusion_tag}{char_name}** [{action}]{responds_text}")
    lines.append("")

    responds_target = ""
    if responds_to:
        target_char = "前文"
        for s in all_speeches:
            sid = s.get("speech_id") or ""
            if sid == responds_to:
                target_cid = s.get("character_id", "")
                target_char = characters.get(target_cid, {}).get("name", target_cid)
                if anonymous:
                    tctx = s.get("structure_context") or {}
                    target_char = tctx.get("anonymous_label") or target_char
                break
        target_text = next(
            (s.get("content", "").split("\n")[0][:80] + "……"
             for s in all_speeches if (s.get("speech_id") or "") == responds_to),
            "",
        )
        if target_text:
            responds_target = f"↑ 回应 {target_char}：{target_text}"

    content = speech.get("content", "")
    paragraphs = [p for p in content.split("\n") if p.strip()]
    for i, paragraph in enumerate(paragraphs):
        lines.append(f"> {paragraph}")
        if i < len(paragraphs) - 1:
            lines.append(">")
    lines.append("")
    if responds_target:
        lines.append(f"*{responds_target}*")
        lines.append("")
    key_points = speech.get("key_points", [])
    if key_points:
        lines.append("- 要点：")
        for point in key_points:
            lines.append(f"  - {point}")
        lines.append("")
    return lines


def render_hat_phase(hat_code: str, phase_speeches: list, characters: dict, round_number: int, speech_counter: list) -> list:
    """渲染六顶思考帽模式下的单个帽子阶段。

    speech_counter 是一个单元素列表，用于在跨阶段时保持全局发言序号连续。
    """
    lines = []
    label = hat_label(hat_code) if hat_code else "未标注帽子阶段"
    lines.append(f"#### {label}")
    lines.append("")

    for speech in phase_speeches:
        block = render_speech_block(
            speech, characters, round_number, speech_counter[0], phase_speeches
        )
        lines.extend(block)
        speech_counter[0] += 1
    return lines


DELPHI_PHASE_LABELS = {
    "independent": "独立作答阶段",
    "feedback": "反馈修正阶段",
    "convergence": "收敛总结阶段",
}
WORLD_CAFE_PHASE_LABELS = {
    "setup": "分组阶段",
    "rotation_1": "第一轮轮换",
    "rotation_2": "第二轮轮换",
    "rotation_3": "第三轮轮换",
    "harvest": "收获阶段",
}
FISHBONE_PHASE_LABELS = {
    "grouping": "分组阶段",
    "independent_proposal": "独立方案阶段",
    "cross_review": "交叉评审阶段",
    "synthesis": "综合阶段",
}


def render_delphi_synthesis(synthesis: dict) -> list:
    """渲染德尔菲收敛阶段的共识、分歧与待解问题。

    将 round.synthesis 中的 consensus / divergence / open_questions 三个标签
    转为可读的 Markdown 列表，供 convergence round 在无发言时展示收敛结论。
    """
    lines = []
    labels = [
        ("consensus", "共识"),
        ("divergence", "分歧"),
        ("open_questions", "待解问题"),
    ]
    found = False
    for key, label in labels:
        items = synthesis.get(key, [])
        if not isinstance(items, list) or not items:
            continue
        found = True
        lines.append(f"- **{label}**：" + "；".join(str(i) for i in items))
    if found:
        lines.insert(0, "#### 收敛结论")
        lines.insert(1, "")
    return lines


def render_world_cafe_speeches(speeches: list, characters: dict, round_number: int) -> list:
    """世界咖啡馆模式：按 table_id 分组渲染发言。

    rotation 阶段每桌的发言归为一组，桌主发言标注 [桌主]。
    harvest 阶段 table_id 为 null，按普通顺序渲染。
    """
    lines = []
    table_groups: dict = {}
    plenary = []
    for speech in speeches:
        ctx = speech.get("structure_context") or {}
        tid = ctx.get("table_id")
        if tid is None:
            plenary.append(speech)
        else:
            table_groups.setdefault(tid, []).append(speech)

    for tid in sorted(table_groups.keys()):
        lines.append(f"#### {tid}")
        lines.append("")
        for idx, speech in enumerate(table_groups[tid]):
            lines.extend(render_speech_block(speech, characters, round_number, idx, speeches))
        lines.append("")

    if plenary:
        lines.append("#### 全体分享")
        lines.append("")
        for idx, speech in enumerate(plenary):
            lines.extend(render_speech_block(speech, characters, round_number, idx, speeches))
        lines.append("")

    return lines


def render_fishbone_speeches(speeches: list, characters: dict, round_number: int) -> list:
    """鱼骨图模式：按 group_id 分组渲染发言。

    independent_proposal 阶段每组的发言归为一组。
    cross_review 阶段发言携带 reviewing_group_id，在发言头标注被评审组。
    synthesis 阶段 group_id 为 null，按普通顺序渲染。
    """
    lines = []
    group_speeches: dict = {}
    plenary = []
    for speech in speeches:
        ctx = speech.get("structure_context") or {}
        gid = ctx.get("group_id")
        if gid is None:
            plenary.append(speech)
        else:
            group_speeches.setdefault(gid, []).append(speech)

    for gid in sorted(group_speeches.keys()):
        lines.append(f"#### {gid}")
        lines.append("")
        for idx, speech in enumerate(group_speeches[gid]):
            lines.extend(render_speech_block(speech, characters, round_number, idx, speeches))
        lines.append("")

    if plenary:
        lines.append("#### 综合讨论")
        lines.append("")
        for idx, speech in enumerate(plenary):
            lines.extend(render_speech_block(speech, characters, round_number, idx, speeches))
        lines.append("")

    return lines


def render_round(round_data: dict, characters: dict) -> str:
    """渲染单个议题段。six_hats 模式下按帽子分组渲染。"""
    lines = []
    round_number = round_data.get("round_number", 0)
    focus = round_data.get("focus_question", "")
    speaking_order = round_data.get("speaking_order", [])
    speeches = round_data.get("speeches", [])
    if not isinstance(speeches, list):
        speeches = []
    exchange = round_data.get("exchange", [])
    anchor = build_round_anchor(round_number)
    structure = round_data.get("discussion_structure", "") or ""

    lines.append(f'<a id="{anchor}"></a>')
    lines.append(f"### 议题段 {round_number}：{focus}")
    lines.append("")
    speeches_preview = round_data.get("speeches", [])
    if isinstance(speeches_preview, list) and speeches_preview:
        lines.append(f"> **速览**：{focus}，{len(speeches_preview)} 条发言")
        lines.append("")

    if structure == "six_hats":
        structure_tag = "六顶思考帽"
    elif structure == "delphi":
        structure_tag = "德尔菲法"
    elif structure == "world_cafe":
        structure_tag = "世界咖啡馆"
    elif structure == "fishbone":
        structure_tag = "鱼骨图分组"
    elif structure:
        structure_tag = structure
    else:
        structure_tag = "标准圆桌"
    lines.append(f"**讨论结构**：{structure_tag}")
    lines.append("")

    lines.append(f"**聚焦问题**：{focus}")
    lines.append("")

    order_names = [characters.get(cid, {}).get("name", cid) for cid in speaking_order]
    if order_names and structure != "delphi":
        lines.append(f"**实际发言顺序**：{' → '.join(order_names)}")
        lines.append("")

    if not speeches:
        if structure == "delphi":
            phase_ctx = round_data.get("structure_context") or {}
            phase = phase_ctx.get("delphi_phase", "")
            phase_label = DELPHI_PHASE_LABELS.get(phase, phase or "德尔菲阶段")
            lines.append(f"**德尔菲阶段**：{phase_label}")
            lines.append("")
            synth = round_data.get("synthesis") or {}
            if synth:
                lines.extend(render_delphi_synthesis(synth))
                lines.append("")
        lines.append("**Conductor 小结**")
        lines.append("")
        lines.append(generate_round_summary(round_data, characters, anonymous=(structure == "delphi")))
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("[↑ 返回目录](#目录)")
        lines.append("")
        return "\n".join(lines)

    if structure == "six_hats":
        hat_groups = group_speeches_by_hat(speeches, round_data)
        speech_counter = [0]
        if hat_groups:
            for hat_code, phase_speeches in hat_groups:
                lines.extend(
                    render_hat_phase(hat_code, phase_speeches, characters, round_number, speech_counter)
                )
        else:
            lines.append("**发言**")
            lines.append("")
            for idx, speech in enumerate(speeches):
                lines.extend(render_speech_block(speech, characters, round_number, idx, speeches))
    elif structure == "delphi":
        phase_ctx = round_data.get("structure_context") or {}
        phase = phase_ctx.get("delphi_phase", "")
        phase_label = DELPHI_PHASE_LABELS.get(phase, phase or "德尔菲阶段")
        lines.append(f"**德尔菲阶段**：{phase_label}")
        lines.append("")
        lines.append("**发言（身份匿名）**")
        lines.append("")
        for idx, speech in enumerate(speeches):
            lines.extend(render_speech_block(speech, characters, round_number, idx, speeches, anonymous=True))
        synth = round_data.get("synthesis") or {}
        if synth:
            lines.extend(render_delphi_synthesis(synth))
            lines.append("")
    elif structure == "world_cafe":
        phase_ctx = round_data.get("structure_context") or {}
        phase = phase_ctx.get("world_cafe_phase", "")
        phase_label = WORLD_CAFE_PHASE_LABELS.get(phase, phase or "世界咖啡馆阶段")
        lines.append(f"**世界咖啡馆阶段**：{phase_label}")
        lines.append("")
        lines.extend(render_world_cafe_speeches(speeches, characters, round_number))
    elif structure == "fishbone":
        phase_ctx = round_data.get("structure_context") or {}
        phase = phase_ctx.get("fishbone_phase", "")
        phase_label = FISHBONE_PHASE_LABELS.get(phase, phase or "鱼骨图阶段")
        lines.append(f"**鱼骨图阶段**：{phase_label}")
        lines.append("")
        lines.extend(render_fishbone_speeches(speeches, characters, round_number))
    else:
        lines.append("**发言**")
        lines.append("")
        for idx, speech in enumerate(speeches):
            lines.extend(render_speech_block(speech, characters, round_number, idx, speeches))

    if exchange:
        lines.append("**发言意向与插话**")
        lines.append("")
        for item in exchange:
            if "intent_id" in item:
                char_id = item.get("character_id", "")
                char_name = characters.get(char_id, {}).get("name", char_id)
                intent = intent_label(item.get("intent_type", "pass"))
                trigger = item.get("trigger_speech_id", "")
                reason = item.get("one_line_reason", "")
                lines.append(f"- {char_name} 在 [{trigger}](#{trigger}) 后 {intent}：{reason}")
            elif "interrupt_id" in item:
                char_id = item.get("character_id", "")
                char_name = characters.get(char_id, {}).get("name", char_id)
                interrupted = item.get("interrupted_speech_id", "")
                content = item.get("content", "")
                lines.append(f"- {char_name} 插话 [{interrupted}](#{interrupted})：{content}")
        lines.append("")

    lines.append("**Conductor 小结**")
    lines.append("")
    lines.append(generate_round_summary(round_data, characters, anonymous=(structure == "delphi")))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("[↑ 返回目录](#目录)")
    lines.append("")

    return "\n".join(lines)


def render_next_step(item) -> str:
    """渲染单条下一步建议，支持字符串或结构化对象。"""
    if isinstance(item, dict):
        step_id = item.get("id", "")
        title = item.get("title", "")
        scope = item.get("scope", "")
        effort = item.get("effort", "")
        rationale = item.get("rationale", "")
        tags = "/".join(t for t in [scope, effort] if t)
        tag_part = f" [{tags}]" if tags else ""
        line = f"- **{step_id}**{tag_part} {title}"
        if rationale:
            line += f"\n  - 理由：{rationale}"
        return line
    return f"- {item}"


def render_synthesis(synthesis: dict) -> str:
    """渲染合成部分。"""
    lines = []
    lines.append("## 合成")
    lines.append("")

    for section, title in [
        ("consensus", "共识"),
        ("divergence", "分歧"),
        ("open_questions", "开放问题"),
    ]:
        lines.append(f"### {title}")
        lines.append("")
        items = synthesis.get(section, [])
        if items:
            for item in items:
                lines.append(f"- {item}")
        else:
            lines.append("- 暂无")
        lines.append("")

    lines.append("### 下一步建议")
    lines.append("")
    next_steps = synthesis.get("next_steps", [])
    if not isinstance(next_steps, list):
        next_steps = []
    if next_steps:
        for item in next_steps:
            lines.append(render_next_step(item))
            lines.append("")
    else:
        lines.append("- 暂无")
        lines.append("")

    return "\n".join(lines)


def render_memory(memory: dict) -> str:
    """将 Memory 数据渲染为完整 Markdown。"""
    topic = memory.get("topic", "")
    user_question = memory.get("user_question", "")
    created_at = format_timestamp(memory.get("created_at", ""))
    updated_at = format_timestamp(memory.get("updated_at", ""))
    runtime = memory.get("runtime_claim", "")
    disclaimer = memory.get("disclaimer", "")
    characters_raw = memory.get("characters", [])
    if not isinstance(characters_raw, list):
        characters_raw = []
    characters = build_character_lookup(characters_raw)
    rounds = memory.get("rounds", [])
    if not isinstance(rounds, list):
        rounds = []
    synthesis = memory.get("synthesis", {})
    metadata = memory.get("metadata", {})
    expansion_count = metadata.get("expansion_count", 0)

    lines = []
    lines.append(f"# 圆桌讨论记录：{topic}")
    lines.append("")

    if disclaimer:
        lines.append(disclaimer)
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(render_toc(rounds))

    lines.append("## 议题背景")
    lines.append("")
    current_date = metadata.get("current_date", "")
    temporal_notes = metadata.get("temporal_notes", "")
    if current_date:
        lines.append(f"**时间锚**：{current_date}")
        lines.append("")
    if temporal_notes:
        lines.append(f"**时效性说明**：{temporal_notes}")
        lines.append("")
    if user_question:
        lines.append("**用户原问题**：")
        lines.append("")
        for paragraph in user_question.split("\n"):
            if paragraph.strip():
                lines.append(f"> {paragraph}")
        lines.append("")
    lines.append(f"本次圆桌围绕 **{topic}** 展开讨论。为便于深入，讨论被拆分为若干议题段，每段聚焦一个子问题。")
    lines.append("")
    focus_questions = [r.get("focus_question", "") for r in rounds if r.get("focus_question")]
    if focus_questions:
        lines.append("**讨论脉络**：")
        for idx, fq in enumerate(focus_questions, 1):
            lines.append(f"{idx}. {fq}")
        lines.append("")

    lines.append("## 与会角色")
    lines.append("")
    delphi_labels = {}
    for rnd in rounds:
        for sp in rnd.get("speeches", []) or []:
            if not isinstance(sp, dict):
                continue
            cid = sp.get("character_id", "")
            ctx = sp.get("structure_context") or {}
            label = ctx.get("anonymous_label", "")
            if cid and label and cid not in delphi_labels:
                delphi_labels[cid] = label
    for char in characters_raw:
        anon = delphi_labels.get(char.get("id", ""), "")
        if anon:
            char = {**char, "name": anon}
        lines.append(render_character(char))

    lines.append("## 讨论过程")
    lines.append("")
    for round_data in rounds:
        lines.append(render_round(round_data, characters))

    lines.append(render_synthesis(synthesis))

    lines.append("## 如何继续")
    lines.append("")
    lines.append("本次讨论的完整事实源保存在同目录下的 Memory JSON 文件中。你可以基于该文件：")
    lines.append("- 继续同一议题的下一个议题段；")
    lines.append("- 中途插入问题、增加席位或转换话题；")
    lines.append("- 导出到其他技能做进一步分析或可视化。")
    lines.append("")

    if disclaimer:
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
    markdown = render_memory(memory)

    output_path = Path(args.output) if args.output else memory_path.with_suffix(".md")
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Rendered roundtable report: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
