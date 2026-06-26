#!/usr/bin/env python3

from __future__ import annotations

import json
from typing import Any


DEFAULT_LLM_CONFIG = {
    "provider": "openai_compatible",
    "api_key_env": "STEP_API_KEY",
    "base_url": "https://api.stepfun.com/step_plan/v1",
    "model": "step-3.5-flash",
    "temperature": 0.2,
    "max_tokens": 6000,
    "timeout_seconds": 180,
}

SCRIPT_OVERVIEW_SCHEMA = {
    "title": "string",
    "global_instruction": "string",
    "characters": [
        {
            "id": "string (稳定角色 ID；不要用代词/碎片)",
            "name": "string",
            "instruction": "string (稳定长期成立的声音底色)",
            "voice_trait": "narrator | male_young | female_young | male_elder | female_elder | default",
            "aliases": ["string"],
        }
    ],
}

SCRIPT_CHUNK_SCHEMA = {
    "characters": [
        {
            "id": "string",
            "name": "string",
            "instruction": "string",
            "voice_trait": "narrator | male_young | female_young | male_elder | female_elder | default",
            "aliases": ["string"],
        }
    ],
    "segments": [
        {
            "speaker": "string (角色 ID；旁白固定 narrator)",
            "raw_text": "string (该段真正要说的正文，不要附带 markdown)",
            "delivery_mode": "narration | dialogue | inner_monologue",
            "inline_instruction": "string",
            "scene_instruction": "string",
        }
    ],
}

SCRIPT_FINAL_SCHEMA = {
    "title": "string",
    "global_instruction": "string",
    "characters": [
        {
            "id": "string",
            "name": "string",
            "instruction": "string",
            "voice_trait": "narrator | male_young | female_young | male_elder | female_elder | default",
            "aliases": ["string"],
        }
    ],
    "segments": [
        {
            "speaker": "string (角色 ID；旁白固定 narrator)",
            "raw_text": "string",
            "delivery_mode": "narration | dialogue | inner_monologue",
            "inline_instruction": "string",
            "scene_instruction": "string",
        }
    ],
}

CASTING_ROLE_PROFILE_SCHEMA = {
    "title": "string",
    "roles": [
        {
            "role_id": "string",
            "role_name": "string",
            "role_type": "narrator | character",
            "dialogue_count": 0,
            "role_summary": "string",
            "desired_tags": ["string"],
            "suitable_scenes": ["string"],
            "avoid_scenes": ["string"],
            "current_instruction": "string",
            "sample_lines": ["string"],
        }
    ],
}

CASTING_SELECTION_SCHEMA = {
    "summary": "string",
    "roles": [
        {
            "role_id": "string",
            "role_name": "string",
            "selected_asset_id": "string",
            "selected_source": "official | clone",
            "selected_reason": "string",
            "stable_instruction": "string",
            "recommended_candidates": [
                {
                    "asset_id": "string",
                    "source": "official | clone",
                    "reason": "string",
                }
            ],
        }
    ],
}


def _merge_mapping(base: dict[str, Any], incoming: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(incoming, dict):
        return base
    merged = dict(base)
    for key, value in incoming.items():
        if value in (None, ""):
            continue
        merged[key] = value
    return merged


def resolve_llm_task_config(
    library: dict[str, Any],
    task_name: str,
    *,
    cli_overrides: dict[str, Any] | None = None,
    legacy_config: dict[str, Any] | None = None,
    default_model: str = "step-3.5-flash",
) -> dict[str, Any]:
    llm_root = (library.get("llm") or {}) if isinstance(library, dict) else {}
    task_config = ((llm_root.get("tasks") or {}).get(task_name) or {}) if isinstance(llm_root, dict) else {}
    merged = dict(DEFAULT_LLM_CONFIG)
    merged = _merge_mapping(merged, (llm_root.get("defaults") or {}) if isinstance(llm_root, dict) else {})
    merged = _merge_mapping(merged, legacy_config or {})
    merged = _merge_mapping(merged, task_config if isinstance(task_config, dict) else {})
    merged = _merge_mapping(merged, cli_overrides or {})
    merged["provider"] = str(merged.get("provider") or "openai_compatible")
    merged["api_key_env"] = str(merged.get("api_key_env") or "STEP_API_KEY")
    merged["base_url"] = str(merged.get("base_url") or "https://api.stepfun.com/step_plan/v1")
    merged["model"] = str(merged.get("model") or default_model)
    merged["temperature"] = float(merged.get("temperature") or 0.2)
    merged["max_tokens"] = int(merged.get("max_tokens") or 6000)
    merged["timeout_seconds"] = max(10, int(merged.get("timeout_seconds") or 180))
    return merged


def build_script_overview_messages(sample_text: str, file_stem: str) -> list[dict[str, Any]]:
    return [
        {
            "role": "system",
            "content": "\n".join(
                [
                    "你是有声书结构化脚本规划助手。",
                    "任务是先从原始小说文本中抽取稳定的人物注册表和整体朗读风格，为后续逐段 script generation 提供约束。",
                    "尽量直接基于语义理解判断人物性别、年龄层、气质与稳定声线底色，不要靠硬编码关键词打分。",
                    "只输出合法 JSON 对象，不要 markdown，不要解释。",
                    "不要把 narrator 写进 characters；旁白会在本地自动补上。",
                    "不要把代词、动作残片、场景碎片当作角色。",
                    "如果证据不足，不要硬猜，instruction 用中性描述，voice_trait 用 default。",
                    f"如果无法可靠抽出标题，可以用文件名 {file_stem} 做兜底。",
                    f"输出 schema: {json.dumps(SCRIPT_OVERVIEW_SCHEMA, ensure_ascii=False)}",
                ]
            ),
        },
        {
            "role": "user",
            "content": "\n".join(
                [
                    "请先提取这个故事片段的标题建议、全局朗读风格、以及稳定角色注册表。",
                    "",
                    sample_text,
                ]
            ),
        },
    ]


def build_script_chunk_messages(
    *,
    chunk_text: str,
    chunk_index: int,
    total_chunks: int,
    title: str,
    global_instruction: str,
    known_characters: list[dict[str, Any]],
    section_title: str = "",
) -> list[dict[str, Any]]:
    registry_text = json.dumps(
        {"title": title, "global_instruction": global_instruction, "characters": known_characters},
        ensure_ascii=False,
        indent=2,
    )
    return [
        {
            "role": "system",
            "content": "\n".join(
                [
                    "你是有声书结构化脚本生成助手。",
                    "任务是把给定原文 chunk 转成新的 audiobook skill 可直接消费的结构化 script 片段。",
                    "输出必须覆盖输入 chunk 的主要叙述和对白顺序，不要摘要，不要乱改剧情。",
                    "默认尽量走 LLM 语义理解，而不是硬编码规则；本地代码只负责切块、校验和合并。",
                    "segments 里 narrator 用于叙述性文字；角色对白和内心独白要落到稳定角色 ID。",
                    "如果同一人出现简称/全名/称谓，必须复用已有稳定角色 ID。",
                    "如果出现新的稳定角色，可以加到 characters；但不要把路人碎片或代词当角色。",
                    "inline_instruction 只写“怎么说”，不要复述剧情；通常 6-24 个字，最多两小句。",
                    "scene_instruction 只写轻微场景漂移，不改变角色底色；没有必要可以留空。",
                    "不要输出 markdown、emoji、项目符号、无意义特殊符号。",
                    "只输出合法 JSON 对象，不要解释。",
                    f"输出 schema: {json.dumps(SCRIPT_CHUNK_SCHEMA, ensure_ascii=False)}",
                ]
            ),
        },
        {
            "role": "user",
            "content": "\n".join(
                [
                    f"当前是第 {chunk_index + 1}/{total_chunks} 个 chunk。",
                    "",
                    "已知故事注册表如下，请尽量复用这些角色 ID：",
                    registry_text,
                    "",
                    "请把下面原文转换为结构化 script chunk：",
                    *(["", f"当前章节/小节标题：{section_title}"] if section_title else []),
                    chunk_text,
                ]
            ),
        },
    ]


def build_script_finalize_messages(
    *,
    provisional_script: dict[str, Any],
    chunk_count: int,
) -> list[dict[str, Any]]:
    return [
        {
            "role": "system",
            "content": "\n".join(
                [
                    "你是有声书结构化脚本总编审。",
                    "任务是把前面按 chunk 生成出的 provisional structured script 收口成最终可执行版本。",
                    "重点处理：统一同一角色的 ID/别名、修正误分配的 speaker、删除明显误识别的碎片角色，并保持段落顺序。",
                    "不要摘要，不要删掉正文主要内容，不要改变剧情信息。",
                    "如果 characters 里有重复角色，要合并到一个稳定角色 ID；segments 必须同步改用合并后的 ID。",
                    "不要凭空新增大量角色；只有在 segment 里已经有稳定说话人证据时才保留。",
                    "旁白固定使用 narrator；不要把 narrator 放进普通角色里。",
                    "segments 的 raw_text 必须保留真正朗读正文；inline_instruction / scene_instruction 只保留轻量朗读控制语。",
                    "尽量基于语义理解做归并，而不是机械按字面字符串。",
                    "只输出合法 JSON 对象，不要 markdown，不要解释。",
                    f"当前 provisional script 来自 {chunk_count} 个 chunk。",
                    f"输出 schema: {json.dumps(SCRIPT_FINAL_SCHEMA, ensure_ascii=False)}",
                ]
            ),
        },
        {
            "role": "user",
            "content": "\n".join(
                [
                    "请把下面的 provisional structured script 收口成最终版本：",
                    json.dumps(provisional_script, ensure_ascii=False, indent=2),
                ]
            ),
        },
    ]


def build_casting_role_profile_messages(user_payload: str) -> list[dict[str, Any]]:
    return [
        {
            "role": "system",
            "content": "\n".join(
                [
                    "你是有声书角色选角规划助手。",
                    "你的任务是先把输入内容整理成适合后续选音色的角色画像 JSON。",
                    "尽量减少硬编码规则推断，直接基于文本证据总结角色的稳定声音需求。",
                    "请合并同一角色的别名，不要把一闪而过的路人都提成主要角色。",
                    "如果存在 narrator / 旁白，请保留为一个独立角色。",
                    "如果输入里已经包含 role_evidence、sample_lines、delivery_modes 或 aliases，把它们当作证据来综合判断，不要机械照抄。",
                    "只输出一个合法 JSON 对象，不要 markdown，不要解释。",
                    "role_type 只能是 narrator 或 character。",
                    "desired_tags / suitable_scenes / avoid_scenes / sample_lines 都必须是数组。",
                    "current_instruction 只写稳定长期成立的声音描述，不写瞬时情绪变化。",
                    f"输出 schema: {json.dumps(CASTING_ROLE_PROFILE_SCHEMA, ensure_ascii=False)}",
                ]
            ),
        },
        {
            "role": "user",
            "content": "\n".join(["请从下面输入中提取有声书角色画像。", "", user_payload]),
        },
    ]


def build_casting_selection_messages(
    role_profiles: list[dict[str, Any]],
    candidate_payload: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "role": "system",
            "content": "\n".join(
                [
                    "你是有声书音色选角导演。",
                    "你必须只从给定候选池里选择音色，不要发明不存在的 asset_id。",
                    "目标是为每个角色选出最匹配的声音，并给出可复核的原因。",
                    "尽量减少硬编码规则；直接基于角色画像和候选池语义做判断。",
                    "官方音色的 display_name 只作为标识，不要被名字误导；优先依据 official_description、official_recommended_scenes 和 selection_summary 判断。",
                    "如果某个官方音色 information_quality=missing，表示官方接口没有返回足够描述；这种低信息候选默认只应作为备选，不要因为名字好听就优先选择。",
                    f"输入里有 {len(role_profiles)} 个角色，你输出的 roles 里也必须有 {len(role_profiles)} 项，且每个 role_id 都必须覆盖一次。",
                    "如果官方音色与某个待 clone 的分析型 clone 拟合度接近，优先官方 ready 音色。",
                    "只有当某个 clone 明显更贴角色，才推荐它，并允许标记为 requires_paid_clone。",
                    "尽量避免 narrator 和核心对白角色使用同一个候选；多个主要角色也尽量不要撞音。",
                    "只输出一个合法 JSON 对象，不要 markdown，不要解释。",
                    f"输出 schema: {json.dumps(CASTING_SELECTION_SCHEMA, ensure_ascii=False)}",
                ]
            ),
        },
        {
            "role": "user",
            "content": "\n".join(
                [
                    "角色画像如下：",
                    json.dumps({"roles": role_profiles}, ensure_ascii=False, indent=2),
                    "",
                    "统一候选池如下：",
                    json.dumps({"voices": candidate_payload}, ensure_ascii=False, indent=2),
                ]
            ),
        },
    ]
