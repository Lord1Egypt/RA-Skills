#!/usr/bin/env python3
"""最小圆桌 router CLI。

供 roundtable-forge 的盲测调用：读取用户 prompt，按关键词判定走主路径、
变体路径、runtime tier 或 fallback 路径，输出 JSON 到 stdout。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


EXPLICIT_SKILL_TRIGGERS = re.compile(r"\$?roundtable-forge", re.IGNORECASE)
ROSTER_TRIGGERS = re.compile(
    r"(帮我选.*人|帮我选.*角色|选.*适合讨论|roster|选人)"
)
SINGLE_PERSPECTIVE_TRIGGERS = re.compile(
    r"(用.{0,6}的视角|用.{0,6}的立场|让.{0,6}分析|如果有.{0,6}会|as a .{0,30},)"
)
FACTUAL_TRIGGERS = re.compile(
    r"^(what is|who is|when did|where is|what's the|首都|首都是|什么时候)",
    re.IGNORECASE,
)
SUMMON_TRIGGERS = re.compile(
    r"(召唤|让.{1,16}坐|让.{1,16}讨论|召集.{0,4}讨论|圆桌|roundtable|round table|召集|想.{0,4}讨论|想看.{0,4}讨论|discuss .{0,30}with|panel (on|about)|summit (on|about)|hold .{0,4}discussion|run .{0,4}discussion)"
)
CROSS_DISCIPLINE_TRIGGERS = re.compile(
    r"(跨学科|多角度|多角色|不同.{0,4}领域|不同.{0,4}视角|多领域|多学科|cross[- ]disciplinary|multi[- ]disciplinary|voices? from|diverse (perspectives?|lenses?))"
)
MEMORY_CONTINUE_TRIGGERS = re.compile(
    r"(继续.{0,4}讨论|继续.{0,4}深入|基于.{0,4}Memory|根据.{0,4}Memory|基于.{0,4}上.{0,4}次|继续.{0,4}圆桌|continue.{0,4}discussion|resume.{0,4}discussion|go deeper|延伸.{0,4}一下|延展|extend)"
)
SEAT_EXPANSION_TRIGGERS = re.compile(
    r"(再增加|增加.{0,6}位|加.{0,6}进来|召.{0,6}加入|再召|扩.{0,2}席位|新增.{0,6}角色|expand.{0,4}seat|add .{0,4}character|invite .{0,4}character)"
)
SENSITIVE_DOMAIN_TRIGGERS = re.compile(
    r"(现任.{0,4}政治|在世.{0,4}政治|敏感.{0,2}政治|医疗.{0,2}诊断|法律.{0,2}建议)"
)
USER_INTERJECTION_TRIGGERS = re.compile(
    r"(等一下|打断一下|先停一下|暂停一下|我想问|我想插入|我想加|我想换|加.{0,6}进来|加.{0,6}进圆桌|先停|我想.{0,2}个问题)"
)
INTERJECTION_SEAT_TRIGGERS = re.compile(
    r"(加.{0,12}进圆桌|加.{0,12}进来|加.{0,4}一位|加.{0,4}一个|再召|新增.{0,12}角色|增加.{0,12}位|请加)"
)
INTERJECTION_PIVOT_TRIGGERS = re.compile(
    r"(换.{0,4}个话题|换.{0,4}到|我想换|转到另一个|先停一下.*换|换.{0,4}问题)"
)
MULTI_AGENT_TRIGGERS = re.compile(
    r"(multi[- ]?agent|parallel agents?|每个角色一个 Agent|独立 Agent|独立 agent|多 agent|并行 agent|spawn agents?|real subagent)"
)
CONDUCTOR_INVITATION_TRIGGERS = re.compile(
    r"(主持人.*问|问一下我|我的立场|我的看法|价值分歧|价值分叉|问我.*倾向|邀请用户发言)"
)
CONTINUATION_TRIGGERS = re.compile(
    r"(next_steps|next step|选一个方向继续|继续.*方向|从.*合成.*继续|从 next)"
)
FUSION_THINKER_TRIGGERS = re.compile(
    r"(融思者|fusion thinker|综合视角|跨学科综合|meta.{0,4}视角|synthesize.*perspective|合成.*视角)"
)
TEMPORAL_GROUNDING_TRIGGERS = re.compile(
    r"(时间锚|temporal grounding|current date|2026|当前.*(AI|人工智能)|最新.*(AI|人工智能))"
)
SIX_HATS_TRIGGERS = re.compile(
    r"(六顶思考帽|六帽|six hats|six thinking hats|de Bono|德波诺"
    r"|全面分析|从多个维度|从不同维度|结构化讨论"
    r"|风险和价值|风险与价值|权衡|trade[- ]?off|决策分析)"
)
DELPHI_TRIGGERS = re.compile(
    r"(德尔菲|delphi|匿名讨论|多轮收敛|匿名.*讨论|共识.*收敛)"
)
WORLD_CAFE_TRIGGERS = re.compile(
    r"(世界咖啡|world cafe|world[- ]?café|轮换讨论|桌主|跨桌)"
)
FISHBONE_TRIGGERS = re.compile(
    r"(鱼骨图|fishbone|多套方案|分组讨论|独立.*(?:子组|小组)|交叉评审|互相评审)"
)
DISCUSSION_INTENT_TRIGGERS = re.compile(
    r"(讨论|研讨|辩论|分析|discuss|discussion|debate|panel)",
    re.IGNORECASE,
)
CODE_ACTION_TRIGGERS = re.compile(
    r"(写|编写|实现|开发(?!者|人员|团队|工程师)|生成|创建|搭建|构建"
    r"|\b(?:code|implement|build|create|write|program)\b)",
    re.IGNORECASE,
)
CODE_DELIVERABLE_TRIGGERS = re.compile(
    r"(代码|组件|函数|脚本|程序|接口|应用"
    r"|\b(?:code|component|function|script|program|API|app|application)\b)",
    re.IGNORECASE,
)
DIRECT_CODE_REQUEST_TRIGGERS = re.compile(
    r"(((然后|并且|最后)"
    r"\s*(再|还|也)?\s*(帮我|请|替我|给我|直接)?\s*"
    r"(写|编写|实现|开发(?!者|人员|团队|工程师)|生成|创建|搭建|构建)"
    r"|[，。；;,.]\s*(再|还|也)?\s*(帮我|请|替我|给我|直接)\s*"
    r"(写|编写|实现|开发(?!者|人员|团队|工程师)|生成|创建|搭建|构建))"
    r"|\b(?:then|afterwards|finally)\b\s*(?:please\s*)?"
    r"\b(?:code|implement|build|create|write|program)\b)",
    re.IGNORECASE,
)
DEEP_RESEARCH_TRIGGERS = re.compile(
    r"(深度研究报告|完整.{0,6}研究报告|系统性.{0,4}研究"
    r"|deep research|research report|财务.{0,4}技术.{0,4}竞争)",
    re.IGNORECASE,
)
INSUFFICIENT_CONTEXT_TRIGGERS = re.compile(
    r"(讨论什么都行|聊什么都行|随便聊聊|什么都可以|anything is fine|any topic)",
    re.IGNORECASE,
)
PODCAST_TRIGGERS = re.compile(
    r"(播客|podcast|音频节目|节目文字稿)",
    re.IGNORECASE,
)
MULTI_OUTPUT_TRIGGERS = re.compile(
    r"(同时.{0,12}(minutes|纪要|报告).{0,12}(podcast|播客)"
    r"|同时.{0,12}(podcast|播客).{0,12}(minutes|纪要|报告))",
    re.IGNORECASE,
)


def has_code_delivery_intent(text: str, *, has_discussion: bool) -> bool:
    """Return true only for a locally connected code-delivery request.

    Technology names are valid roundtable topics, and role names such as
    ``开发者`` are not implementation verbs. A discussion that merely asks how
    to build an ecosystem is therefore kept on the roundtable route. When the
    prompt also asks for discussion, only an explicit direct-delivery clause
    may activate the coding fallback.
    """
    actions = list(CODE_ACTION_TRIGGERS.finditer(text))
    deliverables = list(CODE_DELIVERABLE_TRIGGERS.finditer(text))
    locally_connected = any(
        max(action.start(), deliverable.start())
        - min(action.end(), deliverable.end())
        <= 48
        for action in actions
        for deliverable in deliverables
    )
    if not locally_connected:
        return False
    if has_discussion and not DIRECT_CODE_REQUEST_TRIGGERS.search(text):
        return False
    return True


def detect(text: str) -> dict[str, Any]:
    raw_text = text.strip()
    has_explicit_skill = bool(EXPLICIT_SKILL_TRIGGERS.search(raw_text))
    lowered = EXPLICIT_SKILL_TRIGGERS.sub(" ", raw_text)
    has_summon = bool(SUMMON_TRIGGERS.search(lowered))
    if has_explicit_skill and DISCUSSION_INTENT_TRIGGERS.search(lowered):
        has_summon = True
    has_cross = bool(CROSS_DISCIPLINE_TRIGGERS.search(lowered))
    has_memory = bool(MEMORY_CONTINUE_TRIGGERS.search(lowered))
    has_expansion = bool(SEAT_EXPANSION_TRIGGERS.search(lowered))
    has_roster_only = bool(ROSTER_TRIGGERS.search(lowered))
    has_single_perspective = bool(SINGLE_PERSPECTIVE_TRIGGERS.search(lowered))
    has_factual = bool(FACTUAL_TRIGGERS.search(lowered))
    has_sensitive = bool(SENSITIVE_DOMAIN_TRIGGERS.search(lowered))
    has_interjection = bool(USER_INTERJECTION_TRIGGERS.search(lowered))
    has_interjection_seat = bool(INTERJECTION_SEAT_TRIGGERS.search(lowered))
    has_interjection_pivot = bool(INTERJECTION_PIVOT_TRIGGERS.search(lowered))
    has_multi_agent = bool(MULTI_AGENT_TRIGGERS.search(lowered))
    has_conductor_invitation = bool(CONDUCTOR_INVITATION_TRIGGERS.search(lowered))
    has_continuation = bool(CONTINUATION_TRIGGERS.search(lowered))
    has_fusion_thinker = bool(FUSION_THINKER_TRIGGERS.search(lowered))
    has_temporal_grounding = bool(TEMPORAL_GROUNDING_TRIGGERS.search(lowered))
    has_six_hats = bool(SIX_HATS_TRIGGERS.search(lowered))
    has_delphi = bool(DELPHI_TRIGGERS.search(lowered))
    has_world_cafe = bool(WORLD_CAFE_TRIGGERS.search(lowered))
    has_fishbone = bool(FISHBONE_TRIGGERS.search(lowered))
    if DISCUSSION_INTENT_TRIGGERS.search(lowered) and (
        has_six_hats or has_delphi or has_world_cafe or has_fishbone
    ):
        has_summon = True
    has_code_task = has_code_delivery_intent(
        lowered,
        has_discussion=bool(DISCUSSION_INTENT_TRIGGERS.search(lowered) and has_summon),
    )
    has_deep_research = bool(DEEP_RESEARCH_TRIGGERS.search(lowered))
    has_insufficient_context = bool(INSUFFICIENT_CONTEXT_TRIGGERS.search(lowered))
    has_podcast = bool(PODCAST_TRIGGERS.search(lowered))
    has_multi_output = bool(MULTI_OUTPUT_TRIGGERS.search(lowered))

    workflow_bundle = "direct-execution"
    runtime_claim = "single_backend_multi_session"
    process_skills: list[str] = []
    lead_agent = "Roundtable Conductor"
    needs_disclaimer = True
    needs_memory = True
    needs_seat_expansion = False
    fallback: str | None = None
    clarifying_question: str | None = None
    confidence = 0.5
    reason = "default"

    if has_code_task:
        workflow_bundle = "capability-mismatch-fallback"
        lead_agent = "General Assistant"
        process_skills = ["code-task-redirect"]
        runtime_claim = "soft_orchestration_only"
        needs_disclaimer = False
        needs_memory = False
        fallback = "use a coding skill or coding agent"
        confidence = 0.95
        reason = "code-task-out-of-scope"
    elif has_deep_research:
        workflow_bundle = "deep-research-fallback"
        lead_agent = "Research Router"
        process_skills = ["deep-research-redirect"]
        runtime_claim = "soft_orchestration_only"
        needs_disclaimer = False
        needs_memory = False
        fallback = "use deep-research-forge; invoke roundtable-forge later for multi-perspective discussion"
        confidence = 0.95
        reason = "single-subject-deep-research"
    elif has_insufficient_context and has_summon:
        workflow_bundle = "insufficient-context-fallback"
        lead_agent = "General Assistant"
        process_skills = ["clarify-roundtable-question"]
        runtime_claim = "soft_orchestration_only"
        needs_disclaimer = False
        needs_memory = False
        fallback = "ask for a concrete question and discussion goal before selecting characters"
        clarifying_question = "你希望圆桌具体讨论什么问题，并产出判断、方案还是开放探索？"
        confidence = 0.92
        reason = "insufficient-roundtable-context"
    elif has_factual and not has_summon and not has_interjection:
        workflow_bundle = "factual-fallback"
        lead_agent = "General Assistant"
        process_skills = ["direct-answer"]
        runtime_claim = "soft_orchestration_only"
        needs_memory = False
        fallback = "answer directly without summoning characters"
        confidence = 0.85
        reason = "factual-factual-trigger"
    elif has_single_perspective and not has_summon and not has_cross and not has_interjection:
        workflow_bundle = "single-perspective-fallback"
        lead_agent = "Perspective Lens"
        process_skills = ["perspective-redirect"]
        runtime_claim = "soft_orchestration_only"
        needs_memory = False
        fallback = "suggest a perspective skill instead of a roundtable"
        confidence = 0.85
        reason = "single-perspective-trigger"
    elif has_interjection:
        workflow_bundle = "user-interjection"
        lead_agent = "Roundtable Conductor"
        process_skills = ["user-interjection-handler"]
        if has_interjection_seat:
            process_skills = list(process_skills) + ["seat-expansion"]
            needs_seat_expansion = True
            reason = "user-interjection-seat-expansion"
        elif has_interjection_pivot:
            process_skills = list(process_skills) + ["topic-pivot"]
            reason = "user-interjection-topic-pivot"
        else:
            process_skills = list(process_skills) + ["in-round-answer"]
            reason = "user-interjection-question"
        confidence = 0.88
    elif has_roster_only and not has_summon:
        workflow_bundle = "roster-only"
        lead_agent = "Roundtable Conductor"
        process_skills = ["character-selection"]
        runtime_claim = "soft_orchestration_only"
        needs_memory = False
        confidence = 0.8
        reason = "roster-only-trigger"
    elif has_memory or has_expansion:
        workflow_bundle = "continue-memory"
        lead_agent = "Roundtable Conductor"
        process_skills = ["memory-loader", "seat-expansion"]
        needs_seat_expansion = has_expansion
        confidence = 0.9
        reason = "memory-continue-trigger"
    elif has_summon or has_cross:
        workflow_bundle = "full-roundtable"
        lead_agent = "Roundtable Conductor"
        process_skills = [
            "character-selection",
            "memory-init",
            "roundtable-protocol",
        ]
        needs_seat_expansion = True
        confidence = 0.92
        reason = "summon-or-cross-disciplinary"

    if has_multi_agent and workflow_bundle in ("full-roundtable", "continue-memory"):
        runtime_claim = "real_subagent_runtime"
        process_skills = list(process_skills) + ["subagent-spawn"]
        reason = f"{reason}+real-subagent-request"

    if has_sensitive:
        process_skills = list(process_skills) + ["sensitive-domain-guard"]
        confidence = max(0.7, confidence - 0.1)
        reason = f"{reason}+sensitive-domain"

    if has_podcast and workflow_bundle in ("full-roundtable", "continue-memory"):
        process_skills = list(process_skills) + ["podcast-output-handler", "host-character"]
        reason = f"{reason}+podcast-output"

    if has_conductor_invitation:
        process_skills = list(process_skills) + ["conductor-invitation-handler"]
        reason = f"{reason}+conductor-invitation"

    if has_continuation:
        process_skills = list(process_skills) + ["continuation-handler"]
        reason = f"{reason}+continuation"

    if has_fusion_thinker and workflow_bundle in ("full-roundtable", "continue-memory"):
        process_skills = list(process_skills) + ["fusion-thinker-handler"]
        reason = f"{reason}+fusion-thinker"

    if has_temporal_grounding and workflow_bundle in ("full-roundtable", "continue-memory"):
        process_skills = list(process_skills) + ["temporal-grounding-handler"]
        reason = f"{reason}+temporal-grounding"

    if has_delphi and workflow_bundle in ("full-roundtable", "continue-memory"):
        process_skills = list(process_skills) + ["delphi-handler"]
        reason = f"{reason}+delphi"
    elif has_fishbone and workflow_bundle in ("full-roundtable", "continue-memory"):
        process_skills = list(process_skills) + ["fishbone-handler"]
        reason = f"{reason}+fishbone"
    elif has_world_cafe and workflow_bundle in ("full-roundtable", "continue-memory"):
        process_skills = list(process_skills) + ["world-cafe-handler"]
        reason = f"{reason}+world-cafe"
    elif has_six_hats and workflow_bundle in ("full-roundtable", "continue-memory"):
        process_skills = list(process_skills) + ["six-hats-handler"]
        reason = f"{reason}+six-hats"

    if has_delphi:
        discussion_structure = "delphi"
    elif has_fishbone:
        discussion_structure = "fishbone"
    elif has_world_cafe:
        discussion_structure = "world_cafe"
    elif has_six_hats:
        discussion_structure = "six_hats"
    else:
        discussion_structure = "standard"

    if has_multi_output:
        output_formats = ["minutes", "podcast"]
    elif has_podcast:
        output_formats = ["podcast"]
    else:
        output_formats = ["minutes"]

    if workflow_bundle in ("full-roundtable", "continue-memory"):
        output_artifacts = ["argument_graph"]
        process_skills = list(process_skills) + ["argument-graph-handler"]
    else:
        output_artifacts = []

    return {
        "lead_agent": lead_agent,
        "workflow_bundle": workflow_bundle,
        "runtime_claim": runtime_claim,
        "process_skills": process_skills,
        "needs_disclaimer": needs_disclaimer,
        "needs_memory": needs_memory,
        "needs_seat_expansion": needs_seat_expansion,
        "fallback": fallback,
        "clarifying_question": clarifying_question,
        "discussion_structure": discussion_structure,
        "metadata": {
            "output_format": output_formats[0],
            "output_formats": output_formats,
            "output_artifacts": output_artifacts,
            "discussion_structure": discussion_structure,
        },
        "bundle_confidence": round(confidence, 2),
        "reason": reason,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Roundtable Forge router")
    parser.add_argument("--text", required=True, help="User prompt text")
    args = parser.parse_args()

    result = detect(args.text)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
