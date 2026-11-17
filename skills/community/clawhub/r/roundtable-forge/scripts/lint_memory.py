#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Roundtable Memory 一致性 lint 脚本。

检测 Memory JSON 是否符合 roundtable-forge 的 schema 约束和协议承诺，
覆盖版本一致性、角色引用完整性、六顶思考帽结构、conductor 邀请字段、
next_steps 结构化字段等维度。

用法:
    python lint_memory.py <memory.json>
    python lint_memory.py work/*.json

退出码:
    0 = 无 error（可能有 warning）
    1 = 存在 error
"""

import argparse
import glob
import json
import re
import sys
from pathlib import Path


CURRENT_SCHEMA_VERSION = "2.8.0"
ARGUMENT_GRAPH_SCHEMA_VERSION = "1.0.0"

VALID_CHARACTER_TYPES = {"real_living", "real_historical", "fictional", "archetype"}
VALID_RUNTIME_CLAIMS = {
    "single_backend_multi_session",
    "real_subagent_runtime",
    "soft_orchestration_only",
}
VALID_OUTPUT_FORMATS = {"minutes", "podcast"}
VALID_OUTPUT_ARTIFACTS = {"argument_graph"}
VALID_DISCUSSION_STRUCTURES = {"standard", "six_hats", "delphi", "world_cafe", "fishbone"}
VALID_ACTION_TYPES = {"independent", "extend", "rebut", "question", "interrupt", "pivot"}
VALID_INTERJECTION_TYPES = {
    "question",
    "seat_expansion",
    "topic_pivot",
    "pause",
    "end",
    "conductor_invitation",
    "continuation",
}
VALID_INVITATION_TRIGGERS = {
    "value_fork",
    "experience_gap",
    "abstraction_escalation",
    "character_question",
    "key_decision",
}
VALID_HAT_CODES = {
    "blue_open",
    "white",
    "red",
    "yellow",
    "black",
    "green",
    "blue_close",
    "blue",
}
VALID_NEXT_STEP_SCOPES = {"micro", "meso", "macro"}
VALID_NEXT_STEP_EFFORTS = {"low", "medium", "high"}
VALID_DELPHI_PHASES = {"independent", "feedback", "convergence"}
VALID_WORLD_CAFE_PHASES = {"setup", "rotation_1", "rotation_2", "rotation_3", "harvest"}
VALID_FISHBONE_PHASES = {"grouping", "independent_proposal", "cross_review", "synthesis"}
VALID_ARGUMENT_GRAPH_NODE_TYPES = {
    "question",
    "claim",
    "evidence",
    "assumption",
    "decision",
    "next_step",
}
VALID_ARGUMENT_GRAPH_NODE_STATUSES = {"neutral", "consensus", "divergent", "open"}
VALID_ARGUMENT_GRAPH_RELATIONS = {
    "supports",
    "extends",
    "contradicts",
    "challenges",
    "qualifies",
    "depends_on",
    "answers",
    "raises",
}
VALID_ARGUMENT_GRAPH_CONFIDENCE = {"high", "medium", "low"}

VALID_STATES = {
    "init",
    "round_open",
    "handoff_pending",
    "handoff_consumed",
    "paused",
    "resumed",
    "synthesizing",
    "completed",
}

VALID_STATE_TRANSITIONS = {
    "init": {"round_open", "completed"},
    "round_open": {"handoff_pending", "paused", "synthesizing"},
    "handoff_pending": {"handoff_consumed", "round_open", "paused"},
    "handoff_consumed": {"round_open"},
    "paused": {"resumed"},
    "resumed": {"round_open", "synthesizing"},
    "synthesizing": {"completed"},
    "completed": set(),
}

STABLE_TRIGGER_TOKENS = {
    "first_focus_question_dispatched",
    "last_speech_written",
    "next_round_dispatched",
    "handoff_card_consumed",
    "user_pause_interjection",
    "user_resume",
    "user_continuation_selected",
    "synthesis_started",
    "output_contract_lint_passed",
}


def _parse_version_token(token: str):
    """解析版本号片段，支持数字和 'x' 通配符（按 0 排序便于 max/x 解析）。"""
    text = str(token).strip()
    if text == "x" or text == "X":
        return 0
    return int(text)


def count_chinese(text: str) -> int:
    """统计中文字符数。"""
    return len(re.findall(r"[\u4e00-\u9fff]", text or ""))


class LintReport:
    """收集 lint 发现的问题。"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.errors = []
        self.warnings = []

    def error(self, code: str, message: str, location: str = ""):
        """记录一个 error 级别问题。"""
        self.errors.append({"code": code, "message": message, "location": location})

    def warning(self, code: str, message: str, location: str = ""):
        """记录一个 warning 级别问题。"""
        self.warnings.append({"code": code, "message": message, "location": location})

    @property
    def has_errors(self) -> bool:
        """是否存在 error。"""
        return len(self.errors) > 0

    def summary(self) -> str:
        """生成摘要文本。"""
        lines = []
        status = "FAIL" if self.has_errors else "PASS"
        lines.append(f"[{status}] {self.file_path} — {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        for item in self.errors:
            loc = f" @ {item['location']}" if item["location"] else ""
            lines.append(f"  ERROR {item['code']}: {item['message']}{loc}")
        for item in self.warnings:
            loc = f" @ {item['location']}" if item["location"] else ""
            lines.append(f"  WARN  {item['code']}: {item['message']}{loc}")
        return "\n".join(lines)


def lint_version_consistency(memory: dict, report: LintReport):
    """检查版本字段是否一致并与当前 schema 对齐。"""
    version = memory.get("version", "")
    protocol_version = memory.get("metadata", {}).get("protocol_version", "")

    if not version:
        report.error("VERSION_MISSING", "顶层 version 字段缺失")
    if not protocol_version:
        report.error("PROTOCOL_VERSION_MISSING", "metadata.protocol_version 字段缺失")
    if version and protocol_version and version != protocol_version:
        report.error(
            "VERSION_MISMATCH",
            f"version ({version}) 与 protocol_version ({protocol_version}) 不一致",
        )
    if version and version != CURRENT_SCHEMA_VERSION:
        report.warning(
            "VERSION_OUTDATED",
            f"version {version} 与当前 schema {CURRENT_SCHEMA_VERSION} 不一致",
        )


def lint_characters(memory: dict, report: LintReport):
    """检查角色列表的完整性与引用一致性。"""
    characters = memory.get("characters", [])
    if not isinstance(characters, list):
        report.error(
            "CHARACTERS_NOT_LIST",
            f"characters 应为数组，实际为 {type(characters).__name__}",
        )
        return set()
    if not characters:
        report.warning("NO_CHARACTERS", "角色列表为空")
        return

    seen_ids = set()
    for idx, char in enumerate(characters):
        loc = f"characters[{idx}]"
        char_id = char.get("id", "")
        if not char_id:
            report.error("CHAR_ID_MISSING", "角色缺少 id 字段", loc)
            continue
        if char_id in seen_ids:
            report.error("CHAR_ID_DUPLICATE", f"角色 id 重复: {char_id}", loc)
        seen_ids.add(char_id)

        if not char.get("name"):
            report.error("CHAR_NAME_MISSING", f"角色 {char_id} 缺少 name", loc)
        char_type = char.get("type", "")
        if char_type and char_type not in VALID_CHARACTER_TYPES:
            report.error(
                "CHAR_TYPE_INVALID",
                f"角色 {char_id} 的 type '{char_type}' 不在合法集合中",
                loc,
            )
        if not char.get("agent_profile"):
            report.warning("CHAR_NO_PROFILE", f"角色 {char_id} 缺少 agent_profile", loc)

    return seen_ids


def lint_rounds(memory: dict, report: LintReport, character_ids: set):
    """检查每个 round 的发言引用和结构。"""
    rounds = memory.get("rounds", [])
    if not isinstance(rounds, list):
        report.error(
            "ROUNDS_NOT_LIST",
            f"rounds 应为数组，实际为 {type(rounds).__name__}",
        )
        return
    if not rounds:
        report.warning("NO_ROUNDS", "rounds 列表为空")
        return

    speech_ids_seen = set()

    for r_idx, round_data in enumerate(rounds):
        rn = round_data.get("round_number", r_idx + 1)
        loc_base = f"rounds[{r_idx}] (round {rn})"
        structure = round_data.get("discussion_structure", "")
        speeches = round_data.get("speeches", [])
        if not isinstance(speeches, list):
            report.error(
                "SPEECHES_NOT_LIST",
                f"speeches 应为数组，实际为 {type(speeches).__name__}",
                loc_base,
            )
            speeches = []

        if not round_data.get("focus_question"):
            report.warning("ROUND_NO_FOCUS", "缺少 focus_question", loc_base)

        speech_ids_in_round = set()
        for s_idx, speech in enumerate(speeches):
            loc = f"{loc_base}.speeches[{s_idx}]"
            has_new_id = "character_id" in speech
            has_old_id = "speaker_id" in speech
            has_new_content = "content" in speech
            has_old_content = "line" in speech
            if (has_new_id and has_old_id) or (has_new_content and has_old_content):
                mixed = []
                if has_new_id and has_old_id:
                    mixed.append("character_id/speaker_id")
                if has_new_content and has_old_content:
                    mixed.append("content/line")
                report.warning(
                    "SPEECH_FIELD_MIXED",
                    f"发言同时包含新旧字段名: {', '.join(mixed)}",
                    loc,
                )
            char_id = speech.get("character_id", "")
            if not char_id:
                report.error("SPEECH_NO_CHAR", "发言缺少 character_id", loc)
            elif character_ids and char_id not in character_ids:
                report.error(
                    "SPEECH_DANGLING_CHAR",
                    f"发言引用了不存在的 character_id: {char_id}",
                    loc,
                )

            speech_id = speech.get("speech_id", "")
            if speech_id:
                if speech_id in speech_ids_in_round:
                    report.error(
                        "SPEECH_ID_DUPLICATE",
                        f"speech_id 在同一 round 内重复: {speech_id}",
                        loc,
                    )
                speech_ids_in_round.add(speech_id)
                speech_ids_seen.add(speech_id)
            else:
                report.warning("SPEECH_NO_ID", "发言缺少 speech_id", loc)

            responds_to = speech.get("responds_to", "")
            if responds_to and responds_to not in speech_ids_seen:
                report.warning(
                    "SPEECH_DANGLING_RESPOND",
                    f"responds_to 引用了未见过的 speech_id: {responds_to}",
                    loc,
                )

            action_type = speech.get("action_type", "")
            if action_type and action_type not in VALID_ACTION_TYPES:
                report.warning(
                    "SPEECH_ACTION_INVALID",
                    f"action_type '{action_type}' 不在合法集合中",
                    loc,
                )

            content = speech.get("content", "")
            word_count = count_chinese(content)
            if word_count == 0:
                report.warning("SPEECH_EMPTY", "发言内容为空", loc)

            if structure == "six_hats":
                lint_six_hats_speech(speech, round_data, report, loc, word_count)
            elif structure == "delphi":
                lint_delphi_speech(speech, report, loc, word_count)
            elif structure == "world_cafe":
                lint_world_cafe_speech(speech, report, loc, word_count)
            elif structure == "fishbone":
                lint_fishbone_speech(speech, report, loc, word_count)

        if structure == "delphi":
            lint_delphi_round(round_data, report, loc_base)
        elif structure == "world_cafe":
            lint_world_cafe_round(round_data, report, loc_base)
        elif structure == "fishbone":
            lint_fishbone_round(round_data, report, loc_base)


def lint_six_hats_speech(speech: dict, round_data: dict, report: LintReport, loc: str, word_count: int):
    """检查六顶思考帽模式下单条发言的结构合规性。"""
    ctx = speech.get("structure_context") or {}
    hat = ctx.get("current_hat", "")
    round_ctx = round_data.get("structure_context") or {}
    if not hat:
        hat = round_ctx.get("current_hat", "")

    if not hat:
        report.error("SIX_HATS_NO_HAT", "六帽模式发言缺少 structure_context.current_hat", loc)
        return
    if hat not in VALID_HAT_CODES:
        report.error(
            "SIX_HATS_BAD_HAT",
            f"current_hat '{hat}' 不在合法帽子集合中",
            loc,
        )

    if hat in ("blue_open", "blue_close", "blue"):
        if word_count > 280:
            report.warning(
                "BLUE_HAT_TOO_LONG",
                f"蓝帽发言 {word_count} 字，超过上限 280",
                loc,
            )
    else:
        if word_count > 0 and (word_count < 50 or word_count > 200):
            report.warning(
                "HAT_LENGTH_OUT_OF_RANGE",
                f"非蓝帽发言 {word_count} 字，建议区间 50–200",
                loc,
            )


def lint_delphi_speech(speech: dict, report: LintReport, loc: str, word_count: int):
    """检查德尔菲模式下单条发言的结构合规性。

    关注两点：发言是否携带匿名标签 anonymous_label，以及发言长度是否
    落在协议建议的区间内。两者均为 warning 级，因为缺失匿名标签不破坏
    Memory 结构，只是渲染时无法隐藏身份。
    """
    ctx = speech.get("structure_context") or {}
    if not ctx.get("anonymous_label"):
        report.warning(
            "DELPHI_NO_ANON_LABEL",
            "德尔菲模式发言缺少 structure_context.anonymous_label",
            loc,
        )
    if word_count > 0 and (word_count < 100 or word_count > 400):
        report.warning(
            "DELPHI_LENGTH_OUT_OF_RANGE",
            f"德尔菲发言 {word_count} 字，建议区间 150–300",
            loc,
        )


def lint_delphi_round(round_data: dict, report: LintReport, loc_base: str):
    """检查德尔菲模式 round 级的结构合规性。

    校验 structure_context.delphi_phase 是否为 independent / feedback /
    convergence 之一；当处于 convergence 阶段时，额外检查 round.synthesis
    是否携带 consensus / divergence / open_questions 三个收敛标签。
    """
    ctx = round_data.get("structure_context") or {}
    phase = ctx.get("delphi_phase", "")
    if not phase:
        report.error(
            "DELPHI_NO_PHASE",
            "德尔菲模式 round 缺少 structure_context.delphi_phase",
            loc_base,
        )
        return
    if phase not in VALID_DELPHI_PHASES:
        report.error(
            "DELPHI_BAD_PHASE",
            f"delphi_phase '{phase}' 不在合法集合中 (independent/feedback/convergence)",
            loc_base,
        )
        return

    if phase == "convergence":
        synth = round_data.get("synthesis") or {}
        if not synth:
            report.warning(
                "DELPHI_NO_SYNTHESIS",
                "convergence round 缺少 synthesis",
                loc_base,
            )
        else:
            for key in ("consensus", "divergence", "open_questions"):
                if key not in synth:
                    report.warning(
                        f"DELPHI_SYNTH_MISSING_{key}",
                        f"convergence synthesis.{key} 缺失",
                        loc_base,
                    )


def lint_world_cafe_speech(speech: dict, report: LintReport, loc: str, word_count: int):
    """检查世界咖啡馆模式下单条发言的结构合规性。

    关注两点：发言是否携带 table_id（桌号），以及发言长度是否
    落在协议建议的区间内。harvest 阶段的桌主展示允许更长。
    """
    ctx = speech.get("structure_context") or {}
    if "table_id" not in ctx:
        report.warning(
            "WORLD_CAFE_NO_TABLE_ID",
            "世界咖啡馆模式发言缺少 structure_context.table_id",
            loc,
        )
    if word_count > 0 and (word_count < 60 or word_count > 400):
        report.warning(
            "WORLD_CAFE_LENGTH_OUT_OF_RANGE",
            f"世界咖啡馆发言 {word_count} 字，建议区间 120–300",
            loc,
        )


def lint_world_cafe_round(round_data: dict, report: LintReport, loc_base: str):
    """检查世界咖啡馆模式 round 级的结构合规性。

    校验 structure_context.world_cafe_phase 是否为 setup /
    rotation_1 / rotation_2 / rotation_3 / harvest 之一。
    """
    ctx = round_data.get("structure_context") or {}
    phase = ctx.get("world_cafe_phase", "")
    if not phase:
        report.error(
            "WORLD_CAFE_NO_PHASE",
            "世界咖啡馆模式 round 缺少 structure_context.world_cafe_phase",
            loc_base,
        )
        return
    if phase not in VALID_WORLD_CAFE_PHASES:
        report.error(
            "WORLD_CAFE_BAD_PHASE",
            f"world_cafe_phase '{phase}' 不在合法集合中 (setup/rotation_1/rotation_2/rotation_3/harvest)",
            loc_base,
        )
        return

    if phase != "setup" and not ctx.get("table_count"):
        report.warning(
            "WORLD_CAFE_NO_TABLE_COUNT",
            f"{phase} round 缺少 structure_context.table_count",
            loc_base,
        )


def lint_fishbone_speech(speech: dict, report: LintReport, loc: str, word_count: int):
    """检查鱼骨图分组模式下单条发言的结构合规性。

    关注两点：发言是否携带 group_id（组号），以及发言长度是否
    落在协议建议的区间内。
    """
    ctx = speech.get("structure_context") or {}
    if "group_id" not in ctx:
        report.warning(
            "FISHBONE_NO_GROUP_ID",
            "鱼骨图模式发言缺少 structure_context.group_id",
            loc,
        )
    if word_count > 0 and (word_count < 60 or word_count > 500):
        report.warning(
            "FISHBONE_LENGTH_OUT_OF_RANGE",
            f"鱼骨图发言 {word_count} 字，建议区间 150–300",
            loc,
        )


def lint_fishbone_round(round_data: dict, report: LintReport, loc_base: str):
    """检查鱼骨图分组模式 round 级的结构合规性。

    校验 structure_context.fishbone_phase 是否为 grouping /
    independent_proposal / cross_review / synthesis 之一。
    """
    ctx = round_data.get("structure_context") or {}
    phase = ctx.get("fishbone_phase", "")
    if not phase:
        report.error(
            "FISHBONE_NO_PHASE",
            "鱼骨图模式 round 缺少 structure_context.fishbone_phase",
            loc_base,
        )
        return
    if phase not in VALID_FISHBONE_PHASES:
        report.error(
            "FISHBONE_BAD_PHASE",
            f"fishbone_phase '{phase}' 不在合法集合中 (grouping/independent_proposal/cross_review/synthesis)",
            loc_base,
        )
        return

    if phase != "grouping" and not ctx.get("group_count"):
        report.warning(
            "FISHBONE_NO_GROUP_COUNT",
            f"{phase} round 缺少 structure_context.group_count",
            loc_base,
        )


def lint_interjections(memory: dict, report: LintReport, character_ids: set):
    """检查用户插话和 Conductor 邀请记录。"""
    interjections = memory.get("interjections", [])
    if not isinstance(interjections, list):
        report.error(
            "INTERJECTIONS_NOT_LIST",
            f"interjections 应为数组，实际为 {type(interjections).__name__}",
        )
        return
    for idx, inj in enumerate(interjections):
        loc = f"interjections[{idx}]"
        inj_type = inj.get("type", "")
        if inj_type not in VALID_INTERJECTION_TYPES:
            report.error(
                "INJ_TYPE_INVALID",
                f"type '{inj_type}' 不在合法集合中",
                loc,
            )

        if inj_type == "conductor_invitation":
            trigger = inj.get("trigger", "")
            if not trigger:
                report.error("INVITATION_NO_TRIGGER", "conductor_invitation 缺少 trigger", loc)
            elif trigger not in VALID_INVITATION_TRIGGERS:
                report.warning(
                    "INVITATION_BAD_TRIGGER",
                    f"trigger '{trigger}' 不在标准集合中",
                    loc,
                )
            if not inj.get("options") and not inj.get("raw_text"):
                report.warning(
                    "INVITATION_NO_CONTENT",
                    "conductor_invitation 既无 options 也无 raw_text",
                    loc,
                )

        if inj_type == "continuation":
            if not inj.get("trigger"):
                report.warning("CONTINUATION_NO_TRIGGER", "continuation 缺少 trigger", loc)
            resolved = inj.get("resolved_into", "")
            if not resolved:
                report.warning("CONTINUATION_NO_RESOLVE", "continuation 缺少 resolved_into", loc)


def lint_synthesis(memory: dict, report: LintReport):
    """检查 synthesis 的结构化字段。"""
    synthesis = memory.get("synthesis", {})
    if not synthesis:
        report.warning("NO_SYNTHESIS", "缺少 synthesis 对象")
        return

    for key in ("consensus", "divergence", "open_questions"):
        val = synthesis.get(key)
        if val is None:
            report.warning(f"SYNTH_MISSING_{key}", f"synthesis.{key} 缺失")
        elif not isinstance(val, list):
            report.error(f"SYNTH_NOT_LIST_{key}", f"synthesis.{key} 应为数组", "synthesis")

    next_steps = synthesis.get("next_steps", [])
    if not next_steps:
        report.warning("NO_NEXT_STEPS", "synthesis.next_steps 为空")
        return

    for idx, step in enumerate(next_steps):
        loc = f"synthesis.next_steps[{idx}]"
        if isinstance(step, str):
            report.warning(
                "NEXT_STEP_LEGACY_STRING",
                f"next_step 为纯字符串，建议升级为结构化对象: {step[:40]}",
                loc,
            )
            continue
        if not isinstance(step, dict):
            report.error("NEXT_STEP_NOT_OBJECT", "next_step 既非字符串也非对象", loc)
            continue
        if not step.get("id"):
            report.warning("NEXT_STEP_NO_ID", "next_step 缺少 id", loc)
        if not step.get("title"):
            report.warning("NEXT_STEP_NO_TITLE", "next_step 缺少 title", loc)
        scope = step.get("scope", "")
        if scope and scope not in VALID_NEXT_STEP_SCOPES:
            report.warning("NEXT_STEP_BAD_SCOPE", f"scope '{scope}' 不在 micro/meso/macro 中", loc)
        effort = step.get("effort", "")
        if effort and effort not in VALID_NEXT_STEP_EFFORTS:
            report.warning("NEXT_STEP_BAD_EFFORT", f"effort '{effort}' 不在 low/medium/high 中", loc)


def lint_argument_graph(memory: dict, report: LintReport, character_ids: set):
    """检查观点关系图的引用完整性、受控词表和德尔菲匿名约束。"""
    metadata = memory.get("metadata", {}) or {}
    artifacts = resolve_output_artifacts(metadata, LintReport(report.file_path))
    declared = "argument_graph" in artifacts
    synthesis = memory.get("synthesis", {}) or {}
    graph = synthesis.get("argument_graph")
    is_completed = memory.get("state") == "completed"

    if graph is None:
        if declared:
            if is_completed:
                report.error(
                    "ARG_GRAPH_MISSING",
                    "已声明 argument_graph 产物，但 synthesis.argument_graph 缺失",
                    "synthesis.argument_graph",
                )
            else:
                report.warning(
                    "ARG_GRAPH_PENDING",
                    "已声明 argument_graph 产物，将在 synthesis 阶段生成",
                    "synthesis.argument_graph",
                )
        return

    if not isinstance(graph, dict):
        report.error(
            "ARG_GRAPH_NOT_OBJECT",
            f"synthesis.argument_graph 应为对象，实际为 {type(graph).__name__}",
            "synthesis.argument_graph",
        )
        return

    if not declared:
        report.warning(
            "ARG_GRAPH_UNDECLARED",
            "synthesis.argument_graph 已存在，但 metadata.output_artifacts 未声明 argument_graph",
            "synthesis.argument_graph",
        )

    def incomplete(code: str, message: str, location: str):
        if declared and is_completed:
            report.error(code, message, location)
        else:
            report.warning(code, message, location)

    graph_version = graph.get("schema_version", "")
    if not graph_version:
        incomplete(
            "ARG_GRAPH_NO_SCHEMA_VERSION",
            "argument_graph.schema_version 缺失",
            "synthesis.argument_graph.schema_version",
        )
    elif graph_version != ARGUMENT_GRAPH_SCHEMA_VERSION:
        report.error(
            "ARG_GRAPH_BAD_SCHEMA_VERSION",
            f"argument_graph.schema_version '{graph_version}' 不等于 {ARGUMENT_GRAPH_SCHEMA_VERSION}",
            "synthesis.argument_graph.schema_version",
        )

    if not graph.get("title"):
        incomplete(
            "ARG_GRAPH_NO_TITLE",
            "argument_graph.title 缺失",
            "synthesis.argument_graph.title",
        )

    all_speech_ids = set()
    for round_data in memory.get("rounds", []) or []:
        if not isinstance(round_data, dict):
            continue
        for speech in round_data.get("speeches", []) or []:
            if isinstance(speech, dict) and speech.get("speech_id"):
                all_speech_ids.add(speech["speech_id"])

    nodes = graph.get("nodes", [])
    if not isinstance(nodes, list):
        report.error(
            "ARG_GRAPH_NODES_NOT_LIST",
            "argument_graph.nodes 应为数组",
            "synthesis.argument_graph.nodes",
        )
        return
    if not nodes:
        incomplete(
            "ARG_GRAPH_NO_NODES",
            "argument_graph.nodes 为空",
            "synthesis.argument_graph.nodes",
        )
        return
    if len(nodes) > 15:
        report.warning(
            "ARG_GRAPH_TOO_MANY_NODES",
            f"核心观点图包含 {len(nodes)} 个节点，建议压缩到 8–15 个",
            "synthesis.argument_graph.nodes",
        )

    root_node_id = graph.get("root_node_id", "")
    if not isinstance(root_node_id, str) or not root_node_id.strip():
        incomplete(
            "ARG_GRAPH_NO_ROOT",
            "argument_graph.root_node_id 缺失",
            "synthesis.argument_graph.root_node_id",
        )
        root_node_id = ""
    else:
        root_node_id = root_node_id.strip()

    node_ids = set()
    node_by_id = {}
    delphi_mode = metadata.get("discussion_structure") == "delphi"
    for index, node in enumerate(nodes):
        loc = f"synthesis.argument_graph.nodes[{index}]"
        if not isinstance(node, dict):
            report.error("ARG_GRAPH_NODE_NOT_OBJECT", "graph node 应为对象", loc)
            continue

        node_id = node.get("id", "")
        if not isinstance(node_id, str) or not node_id.strip():
            report.error("ARG_GRAPH_NODE_NO_ID", "graph node 缺少 id", loc)
            node_id = ""
        else:
            node_id = node_id.strip()
        if node_id and node_id in node_ids:
            report.error("ARG_GRAPH_NODE_ID_DUPLICATE", f"graph node id 重复: {node_id}", loc)
        elif node_id:
            node_ids.add(node_id)
            node_by_id[node_id] = node
            if not re.fullmatch(r"ag-n\d{3,}", str(node_id)):
                report.warning(
                    "ARG_GRAPH_NODE_ID_NONSTANDARD",
                    f"graph node id '{node_id}' 建议使用 ag-nNNN 格式",
                    loc,
                )

        if not node.get("label"):
            report.error("ARG_GRAPH_NODE_NO_LABEL", "graph node 缺少 label", loc)

        node_type = node.get("type", "")
        if not isinstance(node_type, str) or node_type not in VALID_ARGUMENT_GRAPH_NODE_TYPES:
            report.error(
                "ARG_GRAPH_NODE_BAD_TYPE",
                f"graph node type '{node_type}' 不在合法集合中",
                loc,
            )

        status = node.get("status", "")
        if not isinstance(status, str) or status not in VALID_ARGUMENT_GRAPH_NODE_STATUSES:
            report.error(
                "ARG_GRAPH_NODE_BAD_STATUS",
                f"graph node status '{status}' 不在合法集合中",
                loc,
            )

        raw_character_ids = node.get("character_ids", [])
        if not isinstance(raw_character_ids, list):
            report.error(
                "ARG_GRAPH_NODE_CHARACTERS_NOT_LIST",
                "graph node character_ids 应为数组",
                loc,
            )
            raw_character_ids = []
        if delphi_mode and raw_character_ids:
            report.error(
                "ARG_GRAPH_DELPHI_IDENTITY_LEAK",
                "德尔菲模式的 argument_graph 不得写入 character_ids",
                loc,
            )
        for character_id in raw_character_ids:
            if not isinstance(character_id, str) or character_id not in character_ids:
                report.error(
                    "ARG_GRAPH_DANGLING_CHARACTER",
                    f"graph node 引用了不存在的 character_id: {character_id}",
                    loc,
                )

        source_speech_ids = node.get("source_speech_ids", [])
        if not isinstance(source_speech_ids, list):
            report.error(
                "ARG_GRAPH_NODE_SOURCES_NOT_LIST",
                "graph node source_speech_ids 应为数组",
                loc,
            )
            source_speech_ids = []
        if node_id != root_node_id and not source_speech_ids:
            report.error(
                "ARG_GRAPH_NODE_NO_SOURCE",
                "非根 graph node 必须引用至少一个 source_speech_ids",
                loc,
            )
        for speech_id in source_speech_ids:
            if not isinstance(speech_id, str) or speech_id not in all_speech_ids:
                report.error(
                    "ARG_GRAPH_DANGLING_SPEECH",
                    f"graph node 引用了不存在的 speech_id: {speech_id}",
                    loc,
                )

    if root_node_id and root_node_id not in node_ids:
        report.error(
            "ARG_GRAPH_DANGLING_ROOT",
            f"root_node_id '{root_node_id}' 不在 nodes 中",
            "synthesis.argument_graph.root_node_id",
        )
    elif root_node_id and node_by_id.get(root_node_id, {}).get("type") != "question":
        report.error(
            "ARG_GRAPH_ROOT_NOT_QUESTION",
            "argument_graph 根节点必须使用 type=question",
            "synthesis.argument_graph.root_node_id",
        )

    edges = graph.get("edges", [])
    if not isinstance(edges, list):
        report.error(
            "ARG_GRAPH_EDGES_NOT_LIST",
            "argument_graph.edges 应为数组",
            "synthesis.argument_graph.edges",
        )
        return
    if not edges:
        incomplete(
            "ARG_GRAPH_NO_EDGES",
            "argument_graph.edges 为空",
            "synthesis.argument_graph.edges",
        )
        return

    edge_ids = set()
    semantic_edges = set()
    for index, edge in enumerate(edges):
        loc = f"synthesis.argument_graph.edges[{index}]"
        if not isinstance(edge, dict):
            report.error("ARG_GRAPH_EDGE_NOT_OBJECT", "graph edge 应为对象", loc)
            continue

        edge_id = edge.get("id", "")
        if not isinstance(edge_id, str) or not edge_id.strip():
            report.error("ARG_GRAPH_EDGE_NO_ID", "graph edge 缺少 id", loc)
            edge_id = ""
        else:
            edge_id = edge_id.strip()
        if edge_id and edge_id in edge_ids:
            report.error("ARG_GRAPH_EDGE_ID_DUPLICATE", f"graph edge id 重复: {edge_id}", loc)
        elif edge_id:
            edge_ids.add(edge_id)
            if not re.fullmatch(r"ag-e\d{3,}", str(edge_id)):
                report.warning(
                    "ARG_GRAPH_EDGE_ID_NONSTANDARD",
                    f"graph edge id '{edge_id}' 建议使用 ag-eNNN 格式",
                    loc,
                )

        raw_source = edge.get("source", "")
        raw_target = edge.get("target", "")
        source = raw_source.strip() if isinstance(raw_source, str) else ""
        target = raw_target.strip() if isinstance(raw_target, str) else ""
        if not source or source not in node_ids:
            report.error(
                "ARG_GRAPH_DANGLING_SOURCE_NODE",
                f"graph edge source '{raw_source}' 不在 nodes 中",
                loc,
            )
        if not target or target not in node_ids:
            report.error(
                "ARG_GRAPH_DANGLING_TARGET_NODE",
                f"graph edge target '{raw_target}' 不在 nodes 中",
                loc,
            )
        if source and source == target:
            report.error("ARG_GRAPH_SELF_EDGE", "graph edge 不得指向自身", loc)

        relation = edge.get("relation", "")
        if not isinstance(relation, str) or relation not in VALID_ARGUMENT_GRAPH_RELATIONS:
            report.error(
                "ARG_GRAPH_BAD_RELATION",
                f"graph edge relation '{relation}' 不在合法集合中",
                loc,
            )
            relation = ""
        semantic_key = (source, target, relation)
        if semantic_key in semantic_edges:
            report.warning(
                "ARG_GRAPH_DUPLICATE_RELATION",
                f"重复关系: {source} -[{relation}]-> {target}",
                loc,
            )
        semantic_edges.add(semantic_key)

        if not edge.get("rationale"):
            report.error("ARG_GRAPH_EDGE_NO_RATIONALE", "graph edge 缺少 rationale", loc)

        confidence = edge.get("confidence", "")
        if not isinstance(confidence, str) or confidence not in VALID_ARGUMENT_GRAPH_CONFIDENCE:
            report.error(
                "ARG_GRAPH_BAD_CONFIDENCE",
                f"graph edge confidence '{confidence}' 不在 high/medium/low 中",
                loc,
            )

        source_speech_ids = edge.get("source_speech_ids", [])
        if not isinstance(source_speech_ids, list):
            report.error(
                "ARG_GRAPH_EDGE_SOURCES_NOT_LIST",
                "graph edge source_speech_ids 应为数组",
                loc,
            )
            source_speech_ids = []
        if not source_speech_ids:
            report.error(
                "ARG_GRAPH_EDGE_NO_SOURCE",
                "graph edge 必须引用至少一个 source_speech_ids",
                loc,
            )
        for speech_id in source_speech_ids:
            if not isinstance(speech_id, str) or speech_id not in all_speech_ids:
                report.error(
                    "ARG_GRAPH_DANGLING_SPEECH",
                    f"graph edge 引用了不存在的 speech_id: {speech_id}",
                    loc,
                )


def lint_metadata(memory: dict, report: LintReport):
    """检查 metadata 的配置字段。"""
    meta = memory.get("metadata", {})
    if not meta:
        report.error("NO_METADATA", "缺少 metadata 对象")
        return

    runtime = meta.get("runtime_claim", "")
    if runtime and runtime not in VALID_RUNTIME_CLAIMS:
        report.error("META_BAD_RUNTIME", f"runtime_claim '{runtime}' 不合法", "metadata")

    resolve_output_formats(meta, report)
    resolve_output_artifacts(meta, report)

    structure = meta.get("discussion_structure", "")
    if structure and structure not in VALID_DISCUSSION_STRUCTURES:
        report.error(
            "META_BAD_STRUCTURE",
            f"discussion_structure '{structure}' 不合法",
            "metadata",
        )

    if not meta.get("current_date"):
        report.warning("META_NO_CURRENT_DATE", "metadata.current_date 缺失，时间锚未设置")


def resolve_output_artifacts(metadata: dict, report: LintReport) -> list[str]:
    """解析并校验附属输出；缺失或空数组均表示不生成附属产物。"""
    if "output_artifacts" not in metadata:
        return []

    output_artifacts = metadata.get("output_artifacts")
    if not isinstance(output_artifacts, list):
        report.error(
            "META_OUTPUT_ARTIFACTS_NOT_LIST",
            f"metadata.output_artifacts 应为数组，实际为 {type(output_artifacts).__name__}",
            "metadata.output_artifacts",
        )
        return []

    resolved: list[str] = []
    for index, artifact in enumerate(output_artifacts):
        location = f"metadata.output_artifacts[{index}]"
        if not isinstance(artifact, str) or not artifact.strip():
            report.error(
                "META_OUTPUT_ARTIFACT_NOT_STRING",
                f"输出附属产物应为非空字符串，实际为 {type(artifact).__name__}",
                location,
            )
            continue
        artifact = artifact.strip()
        if artifact not in VALID_OUTPUT_ARTIFACTS:
            report.error(
                "META_BAD_OUTPUT_ARTIFACT",
                f"output_artifact '{artifact}' 不合法",
                location,
            )
            continue
        if artifact in resolved:
            report.warning(
                "META_DUPLICATE_OUTPUT_ARTIFACT",
                f"output_artifact '{artifact}' 重复",
                location,
            )
            continue
        resolved.append(artifact)
    return resolved


def resolve_output_formats(metadata: dict, report: LintReport) -> list[str]:
    """解析并校验有效输出格式；复数字段存在时优先于单数字段。"""
    if "output_formats" in metadata:
        output_formats = metadata.get("output_formats")
        if not isinstance(output_formats, list):
            report.error(
                "META_OUTPUT_FORMATS_NOT_LIST",
                f"metadata.output_formats 应为数组，实际为 {type(output_formats).__name__}",
                "metadata.output_formats",
            )
            return []
        if not output_formats:
            report.warning(
                "META_NO_OUTPUT_FORMAT",
                "metadata.output_formats 为空，默认 minutes",
                "metadata.output_formats",
            )
            return []

        resolved: list[str] = []
        for index, output_format in enumerate(output_formats):
            location = f"metadata.output_formats[{index}]"
            if not isinstance(output_format, str) or not output_format.strip():
                report.error(
                    "META_OUTPUT_FORMAT_NOT_STRING",
                    f"输出格式应为非空字符串，实际为 {type(output_format).__name__}",
                    location,
                )
                continue
            output_format = output_format.strip()
            if output_format not in VALID_OUTPUT_FORMATS:
                report.error(
                    "META_BAD_OUTPUT_FORMAT",
                    f"output_format '{output_format}' 不合法",
                    location,
                )
                continue
            if output_format in resolved:
                report.warning(
                    "META_DUPLICATE_OUTPUT_FORMAT",
                    f"output_format '{output_format}' 重复",
                    location,
                )
                continue
            resolved.append(output_format)
        return resolved

    output_format = metadata.get("output_format", "")
    if not output_format:
        report.warning("META_NO_OUTPUT_FORMAT", "metadata.output_format 缺失，默认 minutes")
        return []
    if not isinstance(output_format, str):
        report.error(
            "META_OUTPUT_FORMAT_NOT_STRING",
            f"metadata.output_format 应为字符串，实际为 {type(output_format).__name__}",
            "metadata.output_format",
        )
        return []
    output_format = output_format.strip()
    if output_format not in VALID_OUTPUT_FORMATS:
        report.error(
            "META_BAD_OUTPUT_FORMAT",
            f"output_format '{output_format}' 不合法",
            "metadata.output_format",
        )
        return []
    return [output_format]


def lint_podcast_script(memory: dict, report: LintReport):
    """当 output_formats/output_format 包含 podcast 时，检查 podcast_script 的完整性。"""
    metadata = memory.get("metadata", {})
    formats = resolve_output_formats(metadata, LintReport(report.file_path))
    if "podcast" not in formats:
        return

    ps = memory.get("podcast_script", {})
    if not ps:
        report.warning("PODCAST_NO_SCRIPT", "output_format=podcast 但缺少 podcast_script 对象")
        return

    if not ps.get("show_title"):
        report.warning("PODCAST_NO_TITLE", "podcast_script.show_title 缺失")
    if not ps.get("host_id"):
        report.warning("PODCAST_NO_HOST", "podcast_script.host_id 缺失")
    else:
        raw_chars = memory.get("characters", [])
        character_ids = (
            {c.get("id") for c in raw_chars} if isinstance(raw_chars, list) else set()
        )
        if ps["host_id"] not in character_ids:
            report.error("PODCAST_DANGLING_HOST", f"host_id '{ps['host_id']}' 不在角色列表中")

    segments = ps.get("segments", [])
    if not isinstance(segments, list):
        report.error(
            "SEGMENTS_NOT_LIST",
            f"podcast_script.segments 应为数组，实际为 {type(segments).__name__}",
            "podcast_script",
        )
        segments = []
    if not segments:
        report.warning("PODCAST_NO_SEGMENTS", "podcast_script.segments 为空")
    for idx, seg in enumerate(segments):
        loc = f"podcast_script.segments[{idx}]"
        if not seg.get("dialogue"):
            report.warning("PODCAST_SEG_NO_DIALOGUE", f"章节 {seg.get('segment_id', idx)} 无对话", loc)

    # v2.7.0+ cross_promotion 交叉引用校验：防止凭空捏造节目/书/文章引用
    cross_promotion = ps.get("shownotes", {}).get("cross_promotion", []) or []
    if cross_promotion:
        top_sources = memory.get("sources", []) or []
        top_source_keys = set()
        for src in top_sources:
            if isinstance(src, dict):
                key = src.get("key") or src.get("title") or src.get("id")
                if key:
                    top_source_keys.add(str(key))
            elif isinstance(src, str):
                top_source_keys.add(src)
        for idx, cp in enumerate(cross_promotion):
            loc = f"podcast_script.shownotes.cross_promotion[{idx}]"
            if not isinstance(cp, dict):
                continue
            topic = cp.get("topic")
            if topic and not cp.get("source"):
                report.error(
                    "CROSS_PROMOTION_NO_SOURCE",
                    f"cross_promotion[{idx}] 有 topic 但缺 source 字段——请从 Memory 顶层 sources 中引用",
                    loc,
                )
            elif cp.get("source") and top_source_keys:
                src_val = str(cp["source"])
                if src_val not in top_source_keys:
                    matched = any(src_val in k for k in top_source_keys)
                    if not matched:
                        report.error(
                            "CROSS_PROMOTION_SOURCE_NOT_IN_TOP",
                            f"cross_promotion[{idx}].source '{src_val}' 不在 Memory 顶层 sources 中——请补充到 sources 列表",
                            loc,
                        )


def lint_output_contract(memory: dict, report: LintReport):
    """检查 Memory 是否满足渲染所需的最小输出契约。

    根据 output-template-contract.md，渲染器需要 topic、user_question、
    runtime_claim、disclaimer 四个顶层字段才能产出合法输出。本函数检查
    这些字段是否存在且非空，并在 runtime_claim 与 metadata.runtime_claim
    不一致时报 warning。
    """
    topic = memory.get("topic", "")
    if not topic:
        report.error("OUTPUT_NO_TOPIC", "顶层 topic 字段缺失或为空，渲染器无法生成标题")

    user_question = memory.get("user_question", "")
    if not user_question:
        report.warning(
            "OUTPUT_NO_USER_QUESTION",
            "顶层 user_question 字段缺失，背景段将缺少原始问题引用",
        )

    runtime_claim = memory.get("runtime_claim", "")
    if not runtime_claim:
        report.error("OUTPUT_NO_RUNTIME_CLAIM", "顶层 runtime_claim 缺失，路由摘要无法声明运行时")
    elif runtime_claim not in VALID_RUNTIME_CLAIMS:
        report.error(
            "OUTPUT_BAD_RUNTIME_CLAIM",
            f"runtime_claim '{runtime_claim}' 不在合法集合中",
        )

    meta_runtime = memory.get("metadata", {}).get("runtime_claim", "")
    if runtime_claim and meta_runtime and runtime_claim != meta_runtime:
        report.warning(
            "OUTPUT_RUNTIME_MISMATCH",
            f"顶层 runtime_claim ({runtime_claim}) 与 metadata.runtime_claim ({meta_runtime}) 不一致",
        )

    disclaimer = memory.get("disclaimer", "")
    if not disclaimer:
        report.warning(
            "OUTPUT_NO_DISCLAIMER",
            "顶层 disclaimer 缺失，输出将缺少免责声明",
        )


def lint_state_machine(memory: dict, report: LintReport):
    """检查 state 字段和 state_log 是否符合状态机契约。

    校验 state 是否在合法集合中、每条 state_log 转移是否合法，以及 state
    与 metadata.completed 是否一致。详见 state-machine.md。
    """
    state = memory.get("state", "")
    if not state:
        report.warning(
            "STATE_MISSING",
            "顶层 state 字段缺失，建议补上以追踪圆桌生命周期",
        )
        return

    if state not in VALID_STATES:
        report.error(
            "STATE_INVALID",
            f"state '{state}' 不在合法集合中",
            "state",
        )
        return

    completed_flag = bool(memory.get("metadata", {}).get("completed"))
    if state == "completed" and not completed_flag:
        report.warning(
            "STATE_COMPLETED_MISMATCH",
            "state=completed 但 metadata.completed 为 false",
        )
    if completed_flag and state != "completed":
        report.warning(
            "STATE_COMPLETED_MISMATCH",
            f"metadata.completed=true 但 state='{state}'，建议 state 也设为 completed",
        )

    state_log = memory.get("state_log", [])
    if not isinstance(state_log, list):
        report.error("STATE_LOG_NOT_LIST", "state_log 应为数组", "state_log")
        return

    seen_transitions = set()
    for idx, entry in enumerate(state_log):
        loc = f"state_log[{idx}]"
        if not isinstance(entry, dict):
            report.error("STATE_LOG_ENTRY_NOT_OBJECT", f"{loc} 不是对象", loc)
            continue
        from_state = entry.get("from", "")
        to_state = entry.get("to", "")
        if not to_state:
            report.error("STATE_LOG_NO_TO", f"{loc} 缺少 to 字段", loc)
            continue
        if to_state not in VALID_STATES:
            report.error(
                "STATE_LOG_BAD_TO",
                f"{loc} 的 to '{to_state}' 不在合法集合中",
                loc,
            )
            continue
        if from_state and from_state not in VALID_STATES:
            report.error(
                "STATE_LOG_BAD_FROM",
                f"{loc} 的 from '{from_state}' 不在合法集合中",
                loc,
            )
            continue
        if from_state and from_state in VALID_STATE_TRANSITIONS:
            allowed = VALID_STATE_TRANSITIONS[from_state]
            if to_state not in allowed:
                report.error(
                    "STATE_LOG_BAD_TRANSITION",
                    f"{loc} 的转移 {from_state} -> {to_state} 不合法",
                    loc,
                )
        # The same transition is expected to recur across rounds
        # (round_open -> handoff_pending, for example). Only flag a repeated
        # event identity, not a repeated transition type.
        transition_key = (
            from_state,
            to_state,
            entry.get("round_number"),
            entry.get("trigger"),
            entry.get("at"),
        )
        if transition_key in seen_transitions:
            report.warning(
                "STATE_LOG_DUPLICATE",
                f"{loc} 的状态事件 {from_state} -> {to_state} 重复",
                loc,
            )
        seen_transitions.add(transition_key)


def lint_handoff_cards(memory: dict, report: LintReport):
    """检查 rounds[].handoff_card 是否符合轮间记忆卡契约。

    当 metadata.enforce_handoff_cards 为 true 时，每个非最后 round 必须
    有 handoff_card 且字段完整；当为 false 时，全部降级为 warning。
    """
    meta = memory.get("metadata", {})
    enforce = bool(meta.get("enforce_handoff_cards", False))
    rounds = memory.get("rounds", [])
    if not isinstance(rounds, list) or not rounds:
        return

    last_idx = len(rounds) - 1
    seen_card_ids = set()

    for r_idx, round_data in enumerate(rounds):
        if not isinstance(round_data, dict):
            continue
        is_last = r_idx == last_idx
        card = round_data.get("handoff_card")
        loc = f"rounds[{r_idx}].handoff_card"

        if not card:
            if enforce and not is_last:
                report.error(
                    "HANDOFF_CARD_MISSING",
                    f"rounds[{r_idx}] 是非最后 round，缺少 handoff_card（enforce_handoff_cards=true）",
                    f"rounds[{r_idx}]",
                )
            elif not enforce and not is_last:
                report.warning(
                    "HANDOFF_CARD_RECOMMENDED",
                    f"rounds[{r_idx}] 缺少 handoff_card，建议补上以提升跨轮交接质量",
                    f"rounds[{r_idx}]",
                )
            continue

        if not isinstance(card, dict):
            report.error("HANDOFF_CARD_NOT_OBJECT", f"{loc} 不是对象", loc)
            continue

        card_id = card.get("card_id", "")
        if not card_id:
            report.error("HANDOFF_CARD_NO_ID", f"{loc} 缺少 card_id", loc)
        elif card_id in seen_card_ids:
            report.error(
                "HANDOFF_CARD_ID_DUPLICATE",
                f"{loc} 的 card_id '{card_id}' 重复",
                loc,
            )
        else:
            seen_card_ids.add(card_id)

        if not card.get("summary"):
            msg = f"{loc} 缺少 summary"
            if enforce:
                report.error("HANDOFF_CARD_NO_SUMMARY", msg, loc)
            else:
                report.warning("HANDOFF_CARD_NO_SUMMARY", msg, loc)

        summary = card.get("summary", "")
        if summary and count_chinese(summary) > 200:
            report.warning(
                "HANDOFF_CARD_SUMMARY_TOO_LONG",
                f"{loc} summary 超过 200 字，建议精简到 80 字内",
                loc,
            )

        takeaways = card.get("key_takeaways", [])
        if not isinstance(takeaways, list):
            report.error(
                "HANDOFF_CARD_TAKEAWAYS_NOT_LIST",
                f"{loc} key_takeaways 应为数组",
                loc,
            )
        elif len(takeaways) > 5:
            report.warning(
                "HANDOFF_CARD_TOO_MANY_TAKEAWAYS",
                f"{loc} key_takeaways 有 {len(takeaways)} 项，建议 1-5 项",
                loc,
            )
        for t_idx, t in enumerate(takeaways):
            if not isinstance(t, str):
                continue
            if count_chinese(t) > 100:
                report.warning(
                    "HANDOFF_CARD_TAKEAWAY_TOO_LONG",
                    f"{loc}.key_takeaways[{t_idx}] 超过 100 字",
                    f"{loc}.key_takeaways[{t_idx}]",
                )

        consumed_by = card.get("consumed_by", [])
        if not is_last and enforce and isinstance(consumed_by, list) and not consumed_by:
            report.warning(
                "HANDOFF_NOT_CONSUMED",
                f"{loc} 没有 consumed_by 条目，下一轮可能未引用本卡",
                loc,
            )


def lint_versioned_contract(memory: dict, report: LintReport):
    """检查 contract_version 与 contract_compat 是否符合版本化契约。

    contract_version 应与 version 字段一致；如不一致需 WARNING 显式说明
    forward-compat 意图。contract_compat.min_compatible 与 max_compatible
    必须存在且可解析为版本号。
    """
    version = memory.get("version", "")
    contract_version = memory.get("contract_version", "")

    if not contract_version:
        return

    if version and contract_version != version:
        report.warning(
            "CONTRACT_VERSION_DIVERGED",
            f"contract_version ({contract_version}) 与 version ({version}) 不一致，"
            "如果是有意 forward-compat 请忽略",
        )

    compat = memory.get("contract_compat")
    if not compat:
        return
    if not isinstance(compat, dict):
        report.error("CONTRACT_COMPAT_NOT_OBJECT", "contract_compat 应为对象", "contract_compat")
        return

    min_compat = compat.get("min_compatible", "")
    max_compat = compat.get("max_compatible", "")
    if not min_compat:
        report.warning("CONTRACT_COMPAT_NO_MIN", "contract_compat.min_compatible 缺失")
    if not max_compat:
        report.warning("CONTRACT_COMPAT_NO_MAX", "contract_compat.max_compatible 缺失")

    if min_compat and max_compat:
        try:
            min_parts = tuple(_parse_version_token(x) for x in str(min_compat).split("."))
            max_parts = tuple(_parse_version_token(x) for x in str(max_compat).split("."))
            if min_parts > max_parts:
                report.error(
                    "CONTRACT_COMPAT_INVERTED",
                    f"min_compatible ({min_compat}) 大于 max_compatible ({max_compat})",
                    "contract_compat",
                )
        except ValueError:
            report.warning(
                "CONTRACT_COMPAT_UNPARSED",
                "contract_compat 版本号格式无法解析，应为点分数字串如 2.5.0 或 2.5.x",
                "contract_compat",
            )


def lint_file(path: str) -> LintReport:
    """对单个 Memory 文件执行全部 lint 检查。"""
    report = LintReport(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            memory = json.load(f)
    except json.JSONDecodeError as exc:
        report.error("JSON_PARSE_ERROR", f"JSON 解析失败: {exc}")
        return report
    except (FileNotFoundError, IsADirectoryError, PermissionError, UnicodeDecodeError) as exc:
        report.error("FILE_READ_ERROR", f"文件读取失败: {type(exc).__name__}: {exc}")
        return report

    if not isinstance(memory, dict):
        report.error(
            "MEMORY_NOT_OBJECT",
            f"Memory 顶层应为 JSON 对象，实际为 {type(memory).__name__}",
        )
        return report

    lint_version_consistency(memory, report)
    character_ids = lint_characters(memory, report) or set()
    lint_metadata(memory, report)
    lint_output_contract(memory, report)
    lint_rounds(memory, report, character_ids)
    lint_interjections(memory, report, character_ids)
    lint_synthesis(memory, report)
    lint_argument_graph(memory, report, character_ids)
    lint_podcast_script(memory, report)
    lint_state_machine(memory, report)
    lint_handoff_cards(memory, report)
    lint_versioned_contract(memory, report)

    return report


def main() -> int:
    """脚本入口，支持单文件或通配符。"""
    parser = argparse.ArgumentParser(description="Lint roundtable Memory JSON files.")
    parser.add_argument("paths", nargs="+", help="Memory JSON 文件路径或通配符")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="warning 也视为失败（退出码 1）",
    )
    args = parser.parse_args()

    files = []
    for pattern in args.paths:
        matched = sorted(glob.glob(pattern))
        if matched:
            files.extend(matched)
        elif Path(pattern).exists():
            files.append(pattern)

    if not files:
        print("No files matched.", file=sys.stderr)
        return 1

    has_failures = False
    for path in files:
        report = lint_file(path)
        print(report.summary())
        if report.has_errors:
            has_failures = True
        if args.strict and report.warnings:
            has_failures = True

    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
