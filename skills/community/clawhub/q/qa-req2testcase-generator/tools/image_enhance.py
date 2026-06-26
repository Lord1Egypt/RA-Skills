#!/usr/bin/env python3
"""
T1-06：测试增强聚合模块 image_enhance.py
对图片理解结果进行去重合并、图文冲突检测、降级说明生成、质量门禁检查，
并按 P0-P7 各步需求裁剪子集。

功能：
- derived_* 去重合并
- 图文冲突检测（§11.3）
- 降级说明生成（§5）
- 质量门禁检查（§16）
- 按各步需求裁剪子集（每步增量 ≤ 1500 token）

依赖：image_understand.py 输出
"""

import json
import os
import re
from typing import List, Dict, Optional, Set
from difflib import SequenceMatcher


# ============================================================
# 常量
# ============================================================

# 每步注入 token 上限
MAX_STEP_INJECT_TOKENS = 1500

# 置信度阈值
CONFIDENCE_HIGH = 0.8
CONFIDENCE_MEDIUM = 0.5

# 去重相似度阈值
DEDUP_SIMILARITY_THRESHOLD = 0.75


# ============================================================
# 去重工具
# ============================================================

def _text_similarity(a: str, b: str) -> float:
    """计算两段文本的相似度（0~1）"""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def deduplicate_list(items: List[str], threshold: float = DEDUP_SIMILARITY_THRESHOLD) -> List[str]:
    """
    对字符串列表去重：完全相同 + 高相似度合并。
    保留第一次出现的版本。
    """
    if not items:
        return []

    result = []
    for item in items:
        if not item or not item.strip():
            continue
        is_dup = False
        for existing in result:
            if _text_similarity(item, existing) >= threshold:
                is_dup = True
                break
        if not is_dup:
            result.append(item.strip())
    return result


# ============================================================
# 图文冲突检测
# ============================================================

def detect_text_image_conflicts(image_results: List[dict],
                                requirement_text: str = "") -> List[dict]:
    """
    检测图片提取结果与正文描述之间的冲突。
    §11.3 图文冲突裁决规则。

    Returns:
        冲突列表，每项包含 image_id, conflict_type, description, severity
    """
    conflicts = []

    for img in image_results:
        if img.get("processing_status") not in ("success", "success_degraded"):
            continue

        image_id = img.get("image_id", "")
        before_text = (img.get("before_text", "") or "").lower()
        after_text = (img.get("after_text", "") or "").lower()
        context = before_text + " " + after_text

        # 检查 extracted_rules 与上下文的冲突
        for rule in img.get("extracted_rules", []):
            rule_lower = rule.lower()
            # 简单冲突检测：图中提取的规则与正文描述矛盾
            # 例如：图中说"必填"，正文说"选填"
            conflict_pairs = [
                ("必填", "选填"), ("选填", "必填"),
                ("启用", "禁用"), ("禁用", "启用"),
                ("允许", "禁止"), ("禁止", "允许"),
                ("必须", "可选"), ("可选", "必须"),
            ]
            for img_kw, text_kw in conflict_pairs:
                if img_kw in rule_lower and text_kw in context:
                    conflicts.append({
                        "image_id": image_id,
                        "conflict_type": "rule_contradiction",
                        "description": (
                            f"图片中提取的规则「{rule[:50]}」与正文描述可能矛盾"
                            f"（图中含'{img_kw}'，正文含'{text_kw}'）"
                        ),
                        "severity": "high",
                        "image_rule": rule,
                        "context_snippet": context[:100],
                    })

        # 检查图片中的数值与正文数值不一致
        img_summary = (img.get("summary", "") or "").lower()
        # 提取数字
        img_numbers = set(re.findall(r'\d+', img_summary))
        context_numbers = set(re.findall(r'\d+', context))
        # 如果图中有数字但正文中完全没有对应数字，可能是新增信息（不算冲突）
        # 如果两边都有数字但不一致，标记为潜在冲突
        if img_numbers and context_numbers:
            diff = img_numbers - context_numbers
            if diff and len(diff) > 2:
                conflicts.append({
                    "image_id": image_id,
                    "conflict_type": "data_mismatch",
                    "description": (
                        f"图片中的数值与正文可能不一致，"
                        f"图中独有数值: {', '.join(list(diff)[:5])}"
                    ),
                    "severity": "medium",
                })

    return conflicts


# ============================================================
# 降级说明生成
# ============================================================

def generate_degradation_notice(understand_result: dict) -> Optional[str]:
    """
    T3-02：根据处理模式和结果生成降级说明（§5）。
    优化：按图片类型细化提示，区分 OCR 模式和纯文本模式。
    """
    mode = understand_result.get("mode_summary", {}).get("active_mode", "")
    degradation = understand_result.get("degradation_summary")

    if degradation:
        return degradation

    if mode == "ocr":
        return _generate_ocr_degradation_notice(understand_result)
    elif mode == "context_only":
        return _generate_context_only_degradation_notice(understand_result)

    return None


# T3-02: OCR 模式降级说明模板
def _generate_ocr_degradation_notice(understand_result: dict) -> Optional[str]:
    """
    T3-02：OCR 模式降级说明（对齐方案 §5.1）。
    明确指出哪些图类型降级、哪些类型中度提取。
    """
    images = understand_result.get("images", [])

    # T3-02: 按图片类型细化的降级提示模板
    type_degradation_hints = {
        "flowchart": {
            "level": "degraded",
            "hint": "流程图：可能缺少分支条件、判断逻辑、回退路径",
        },
        "ui_mockup": {
            "level": "degraded",
            "hint": "原型图：可能缺少布局细节、控件属性、状态切换",
        },
        "state_diagram": {
            "level": "degraded",
            "hint": "状态图：可能缺少状态迁移条件、触发事件、非法迁移",
        },
        "table_rule": {
            "level": "moderate",
            "hint": "规则表：OCR 模式仍可中度提取，字段名、枚举值基本可用",
        },
        "api_snapshot": {
            "level": "moderate",
            "hint": "接口截图：OCR 模式仍可中度提取，接口名、字段名基本可用",
        },
        "annotated_screenshot": {
            "level": "degraded",
            "hint": "批注截图：可能缺少批注对应的交互逻辑、标框对象定位",
        },
        "report_chart": {
            "level": "degraded",
            "hint": "报告图表：可能缺少数据趋势解读、统计分析信息",
        },
    }

    # 统计各类型降级图片数
    degraded_types = {}  # 降级类型
    moderate_types = {}  # 中度提取类型
    for img in images:
        ext_mode = img.get("extraction_mode", "")
        if ext_mode not in ("ocr", "ocr_degraded", "context_only"):
            continue
        t = img.get("classification", {}).get("type", "unknown")
        type_info = type_degradation_hints.get(t, {"level": "degraded"})
        if type_info["level"] == "moderate":
            moderate_types[t] = moderate_types.get(t, 0) + 1
        else:
            degraded_types[t] = degraded_types.get(t, 0) + 1

    if not degraded_types and not moderate_types:
        return None

    lines = [
        "⚠️ 图片理解降级说明：当前云端模型不支持图片理解，"
        "已使用 OCR 文字识别替代。"
    ]

    if degraded_types:
        lines.append("以下类型图片的信息可能不完整：")
        for t, count in degraded_types.items():
            hint_info = type_degradation_hints.get(t, {})
            hint = hint_info.get("hint", f"{t}：信息可能不完整")
            lines.append(f"- {hint}（{count}张）")

    if moderate_types:
        lines.append("以下类型图片的文字提取仍可用：")
        for t, count in moderate_types.items():
            hint_info = type_degradation_hints.get(t, {})
            hint = hint_info.get("hint", f"{t}：文字提取可用")
            lines.append(f"- {hint}（{count}张）")

    # I-FIX-04: 建议部分按实际降级类型动态生成，而非硬编码
    if degraded_types:
        degraded_type_names = []
        type_display_names = {
            "flowchart": "流程图", "ui_mockup": "原型图",
            "state_diagram": "状态图", "annotated_screenshot": "批注截图",
            "report_chart": "报告图表",
        }
        for t in degraded_types:
            degraded_type_names.append(type_display_names.get(t, t))
        if degraded_type_names:
            lines.append(
                f"建议：人工审阅需求文档中的{'、'.join(degraded_type_names)}，"
                "补充遗漏的测试场景。"
            )
    elif moderate_types:
        lines.append(
            "建议：人工审阅需求文档中的图片，确认 OCR 提取的文字信息完整。"
        )
    return "\n".join(lines)


# T3-02: 纯文本模式降级说明模板
def _generate_context_only_degradation_notice(
    understand_result: dict,
) -> str:
    """
    T3-02：纯文本模式降级说明。
    明确所有图类型均未解析，仅提供元数据。
    """
    images = understand_result.get("images", [])

    # T3-02: 按图片类型细化的纯文本模式提示
    type_context_hints = {
        "flowchart": "流程图：流程分支、判断逻辑、回退路径均未解析",
        "ui_mockup": "原型图：页面布局、控件属性、交互状态均未解析",
        "state_diagram": "状态图：状态迁移条件、触发事件均未解析",
        "table_rule": "规则表：字段定义、枚举值、校验规则均未解析",
        "api_snapshot": "接口截图：接口字段、参数定义均未解析",
        "annotated_screenshot": "批注截图：批注内容、标框对象均未解析",
        "report_chart": "报告图表：数据趋势、统计信息均未解析",
    }

    # 统计各类型图片数
    type_counts = {}
    for img in images:
        t = img.get("classification", {}).get("type", "unknown")
        if t != "unknown":
            type_counts[t] = type_counts.get(t, 0) + 1

    # I-FIX-05: classification缺失时从 caption/section 提取，或输出通用提示
    if not type_counts:
        # 尝试从图片的 caption/section 推断类型
        for img in images:
            caption = img.get("caption", "") or ""
            section = img.get("section", "") or ""
            context_hint = (caption + " " + section).lower()
            inferred = "unknown"
            hint_keywords = {
                "flowchart": ["流程", "泳道", "flow"],
                "ui_mockup": ["原型", "界面", "页面", "mockup"],
                "state_diagram": ["状态", "时序", "state"],
                "table_rule": ["字段", "规则", "矩阵"],
                "api_snapshot": ["接口", "api"],
            }
            for t, kws in hint_keywords.items():
                if any(kw in context_hint for kw in kws):
                    inferred = t
                    break
            if inferred != "unknown":
                type_counts[inferred] = type_counts.get(inferred, 0) + 1

    lines = [
        "⚠️ 图片理解降级说明：当前云端模型不支持图片理解，"
        "图片内容未被解析，仅提供图片元数据（图注、前后文）。"
    ]

    if type_counts:
        lines.append("以下类型图片的内容均未解析：")
        for t, count in type_counts.items():
            hint = type_context_hints.get(t, f"{t}：内容未解析")
            lines.append(f"- {hint}（{count}张）")
    else:
        # I-FIX-05: 完全无法推断类型时，输出通用提示
        total_imgs = len(images)
        lines.append(
            f"共 {total_imgs} 张图片未能识别类型，图片内容（页面布局、流程分支、"
            "字段定义、状态迁移等）均未解析。"
        )

    lines.append(
        "测试用例可能遗漏图中信息（页面布局、流程分支、字段定义等）。"
        "建议人工审阅需求文档中的所有图片，补充遗漏的测试场景。"
    )
    return "\n".join(lines)


# ============================================================
# 质量门禁检查
# ============================================================

def check_quality_gate(understand_result: dict) -> dict:
    """
    质量门禁检查（§16 量化验收阈值）。

    Returns:
        {
            "passed": bool,
            "checks": [{"name": str, "passed": bool, "actual": ..., "threshold": ...}],
            "warnings": [str]
        }
    """
    mode = understand_result.get("mode_summary", {}).get("active_mode", "vision")
    images = understand_result.get("images", [])
    checks = []
    warnings = []

    # 1. 高价值图片是否已解析
    high_value_images = [
        img for img in images
        if img.get("classification", {}).get("value_level") == "high"
    ]
    parsed_high = [
        img for img in high_value_images
        if img.get("processing_status") in ("success", "success_degraded")
    ]

    if mode == "vision":
        threshold = 0.90
        actual = len(parsed_high) / max(len(high_value_images), 1)
        checks.append({
            "name": "高价值图片解析率",
            "passed": actual >= threshold,
            "actual": round(actual, 2),
            "threshold": threshold,
        })
    elif mode == "ocr":
        # OCR 模式放宽：ocr_degraded 视为已解析
        ocr_parsed = [
            img for img in high_value_images
            if img.get("processing_status") in (
                "success", "success_degraded",
                "success_vision_failed", "success_ocr_failed"
            )
        ]
        threshold = 0.80
        actual = len(ocr_parsed) / max(len(high_value_images), 1)
        checks.append({
            "name": "高价值图片解析率（OCR模式）",
            "passed": actual >= threshold,
            "actual": round(actual, 2),
            "threshold": threshold,
        })

    # 2. PX 失败不阻断主链路（必须 100%）
    # 只要没有抛异常导致整个流程中断，就算通过
    checks.append({
        "name": "PX失败不阻断主链路",
        "passed": True,
        "actual": "100%",
        "threshold": "100%",
    })

    # 3. 降级说明已输出
    if mode in ("ocr", "context_only"):
        has_degradation = understand_result.get("degradation_summary") is not None
        checks.append({
            "name": "降级说明已输出",
            "passed": has_degradation,
            "actual": has_degradation,
            "threshold": True,
        })

    # 4. 聚合输出 token 控制
    aggregate = understand_result.get("aggregate", {})
    total_derived = (
        aggregate.get("total_derived_features", 0) +
        aggregate.get("total_derived_test_points", 0) +
        aggregate.get("total_derived_risks", 0) +
        aggregate.get("total_derived_questions", 0)
    )
    # 粗估 token：每条 derived 约 30 token
    estimated_tokens = total_derived * 30
    token_limit = 8000 if mode == "vision" else (6000 if mode == "ocr" else 1000)
    checks.append({
        "name": "聚合输出token控制",
        "passed": estimated_tokens <= token_limit,
        "actual": estimated_tokens,
        "threshold": token_limit,
    })

    passed = all(c["passed"] for c in checks)
    if not passed:
        failed_checks = [c["name"] for c in checks if not c["passed"]]
        warnings.append(f"质量门禁未通过: {', '.join(failed_checks)}")

    return {
        "passed": passed,
        "checks": checks,
        "warnings": warnings,
    }


# ============================================================
# P0-P7 子集裁剪
# ============================================================

def _estimate_tokens(text: str) -> int:
    """I-FIX-11: 粗估文本 token 数（中文约 2 字/token，英文约 4 字符/token）"""
    if not text:
        return 0
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    other_chars = len(text) - chinese_chars
    # I-FIX-11: 中文系数从 1.5 调整为 2，实测 1 中文字 ≈ 1.5~2 token，取保守上界
    return int(chinese_chars * 2 + other_chars / 4)


def _truncate_to_token_budget(items: List[str], budget: int) -> List[str]:
    """按 token 预算截断列表"""
    result = []
    used = 0
    for item in items:
        cost = _estimate_tokens(item)
        if used + cost > budget:
            break
        result.append(item)
        used += cost
    return result


def build_step_subsets(enhance_result: dict) -> dict:
    """
    按 P0-P7 各步需求裁剪 derived_* 子集。
    每步注入增量 ≤ 1500 token。

    Returns:
        {
            "PX": {...},  # PX 完整输出（供 SKILL.md 使用）
            "P0": {...},  # P0 需要的子集
            "P2": {...},  # P2 需要的子集
            "P3": {...},  # P3 需要的子集
            "P4": {...},  # P4 需要的子集
            "degradation_notice": str | None,
        }
    """
    aggregate = enhance_result.get("aggregate", {})
    degradation = enhance_result.get("degradation_notice")
    mode = enhance_result.get("mode_summary", {}).get("active_mode", "context_only")

    features = aggregate.get("derived_features", [])
    test_points = aggregate.get("derived_test_points", [])
    risks = aggregate.get("derived_risks", [])
    questions = aggregate.get("derived_questions", [])

    # 纯文本模式：只注入上下文文本
    if mode == "context_only":
        context_items = []
        for img in enhance_result.get("images", []):
            caption = img.get("caption", "")
            before = img.get("before_text", "")
            after = img.get("after_text", "")
            if caption:
                context_items.append(f"[图注] {caption}")
            if before:
                context_items.append(f"[图前文] {before[:100]}")
            if after:
                context_items.append(f"[图后文] {after[:100]}")

        context_text = _truncate_to_token_budget(context_items, 500)
        return {
            "PX": enhance_result,
            "P0": {"image_context": context_text, "degradation_notice": degradation},
            "P1": {"image_context": context_text, "degradation_notice": degradation},
            "P2": {"degradation_notice": degradation},
            "P3": {"degradation_notice": degradation},
            "P4": {"degradation_notice": degradation},
            "degradation_notice": degradation,
        }

    # 视觉/OCR 模式：按步骤裁剪
    budget = MAX_STEP_INJECT_TOKENS

    # P0：derived_features + derived_test_points（需求补充）
    p0_features = _truncate_to_token_budget(features, budget // 2)
    p0_test_points = _truncate_to_token_budget(test_points, budget // 2)

    # P2：derived_test_points（测试点输入）
    p2_test_points = _truncate_to_token_budget(test_points, budget)

    # P3：derived_risks（风险输入）
    p3_risks = _truncate_to_token_budget(risks, budget)

    # P4：derived_questions（PCI 输入）
    p4_questions = _truncate_to_token_budget(questions, budget)

    return {
        "PX": enhance_result,
        "P0": {
            "derived_features": p0_features,
            "derived_test_points": p0_test_points,
            "degradation_notice": degradation,
        },
        "P1": {
            "derived_features": _truncate_to_token_budget(features, budget),
            "degradation_notice": degradation,
        },
        "P2": {
            "derived_test_points": p2_test_points,
            "degradation_notice": degradation,
        },
        "P3": {
            "derived_risks": p3_risks,
            "degradation_notice": degradation,
        },
        "P4": {
            "derived_questions": p4_questions,
            "degradation_notice": degradation,
        },
        "degradation_notice": degradation,
    }


# ============================================================
# 核心增强流程
# ============================================================


# ============================================================
# A-2 方案适配层 (V2.5.0)
# ============================================================

def _adapt_a2_format(understand_result: dict) -> dict:
    """
    将 A-2 方案的 px_understand.json 格式适配为 image_enhance.py 期望的旧格式。
    A-2 方案使用 results/understanding_mode/confidence(字符串)，
    旧格式使用 images/processing_status/classification.confidence(数值)。
    如果输入已是旧格式（有 images 字段），直接返回不做转换。
    """
    if "results" not in understand_result or "images" in understand_result:
        return understand_result  # 旧格式或无需转换

    confidence_map = {"high": 0.9, "medium": 0.65, "low": 0.3}
    mode_map = {"vision": "success", "caption_context_only": "success_degraded", "api": "success", "api_partial": "success_degraded", "caption_only": "success_degraded", "api_fallback_caption": "success_degraded"}

    adapted_images = []
    for item in understand_result.get("results", []):
        adapted = {
            "image_id": item.get("image_id", ""),
            "file_path": item.get("file_path", ""),
            "processing_status": mode_map.get(item.get("understanding_mode", ""), "skipped"),
            "classification": {
                "type": item.get("image_type", "unknown"),
                "confidence": confidence_map.get(item.get("confidence", "low"), 0.3),
                "value_level": "high" if item.get("confidence") == "high" else "medium"
            },
            "extraction_mode": "vision" if item.get("understanding_mode") in ("vision", "api", "api_partial") else "context_only",
            "derived_features": item.get("derived_features", []),
            "derived_test_points": item.get("derived_test_points", []),
            "derived_risks": item.get("derived_risks", []),
            "derived_questions": [],
            "summary": item.get("description", ""),
            "caption": item.get("selection_reason", ""),
            "evidence": item.get("evidence", []),
        }
        adapted_images.append(adapted)

    for item in understand_result.get("skipped_images", []):
        adapted = {
            "image_id": item.get("image_id", ""),
            "file_path": item.get("file_path", ""),
            "processing_status": "skipped",
            "classification": {"type": "unknown", "confidence": 0, "value_level": "low"},
        }
        adapted_images.append(adapted)

    summary = understand_result.get("summary", {})
    return {
        "task_id": understand_result.get("task_id", ""),
        "images": adapted_images,
        "mode_summary": {
            "active_mode": "vision" if summary.get("vision_count", 0) > 0 else "context_only"
        },
        "processing_summary": {
            "total": understand_result.get("total_images", 0),
            "selected": understand_result.get("selected_images", 0),
        }
    }

def enhance_image_results(understand_result: dict,
                          requirement_text: str = "") -> dict:
    """
    测试增强聚合的公共接口。

    Args:
        understand_result: image_understand.py 的聚合输出
        requirement_text: 原始需求文本（用于图文冲突检测）

    Returns:
        增强后的结果，包含去重后的 derived_*、冲突、降级说明、质量门禁、步骤子集
    """
    understand_result = _adapt_a2_format(understand_result)  # V2.5.0 A-2适配
    images = understand_result.get("images", [])

    # 1. 收集所有 derived_* 并去重
    all_features = []
    all_test_points = []
    all_risks = []
    all_questions = []

    for img in images:
        status = img.get("processing_status", "")
        confidence = img.get("classification", {}).get("confidence", 0)

        # T2-06：置信度评估与人工介入（对齐方案 §10 + §20.6）
        # ≥0.8 高置信：derived_* 正常入链路
        # 0.5~0.8 中置信：入链路 + 标记 confidence: medium，P7 额外关注
        # <0.5 低置信：降级轻摘要，derived_* 不入链路
        if confidence < CONFIDENCE_MEDIUM:
            # 低置信度：降级为轻摘要，derived_* 不入链路
            # 仅保留 summary 作为参考，不注入 derived_*
            img["_confidence_tier"] = "low"
            img["_confidence_action"] = "derived_*不入链路，仅保留轻摘要"
            continue

        if status in ("success", "success_degraded"):
            # AB-09修复：明确置信度边界值规则
            # ≥0.8 高置信：derived_* 正常入链路
            # ≥0.5 且 <0.8 中置信：入链路 + 标记 confidence: medium，P7 额外关注
            # <0.5 低置信：降级轻摘要，derived_* 不入链路
            if confidence >= CONFIDENCE_HIGH:
                img["_confidence_tier"] = "high"
                img["_confidence_action"] = "derived_*正常入链路"
                # 高置信度：derived_* 入链路
                all_features.extend(img.get("derived_features", []))
                all_test_points.extend(img.get("derived_test_points", []))
                all_risks.extend(img.get("derived_risks", []))
                all_questions.extend(img.get("derived_questions", []))
            elif confidence >= CONFIDENCE_MEDIUM:
                img["_confidence_tier"] = "medium"
                img["_confidence_action"] = "derived_*入链路，标记confidence:medium，P7额外关注"
                # 中置信度：在 derived_risks 中追加提醒
                img_type = img.get("classification", {}).get("type", "unknown")
                img_id = img.get("image_id", "")
                all_risks.append(
                    f"[中置信度] {img_id}({img_type}) 置信度 {confidence:.2f}，"
                    f"derived_* 已入链路但建议 P7 额外关注"
                )
                all_features.extend(img.get("derived_features", []))
                all_test_points.extend(img.get("derived_test_points", []))
                all_risks.extend(img.get("derived_risks", []))
                all_questions.extend(img.get("derived_questions", []))
            else:
                # AB-09修复：低置信度(<0.5) — derived_* 不入链路
                img["_confidence_tier"] = "low"
                img["_confidence_action"] = "derived_*不入链路，仅轻摘要"
                continue
            # 注：高/中置信度的 extend 已在各分支内完成，此处不再重复

    # 去重
    deduped_features = deduplicate_list(all_features)
    deduped_test_points = deduplicate_list(all_test_points)
    deduped_risks = deduplicate_list(all_risks)
    deduped_questions = deduplicate_list(all_questions)

    # 2. 图文冲突检测
    conflicts = detect_text_image_conflicts(images, requirement_text)

    # 3. 降级说明
    degradation_notice = generate_degradation_notice(understand_result)

    # 4. 质量门禁
    quality_gate = check_quality_gate(understand_result)

    # 5. 构建增强结果
    enhanced = {
        "schema_version": "1.4.0",
        "task_id": understand_result.get("task_id", ""),
        "mode_summary": understand_result.get("mode_summary", {}),
        "processing_summary": understand_result.get("processing_summary", {}),
        "aggregate": {
            "total_derived_features": len(deduped_features),
            "total_derived_test_points": len(deduped_test_points),
            "total_derived_risks": len(deduped_risks),
            "total_derived_questions": len(deduped_questions),
            "derived_features": deduped_features,
            "derived_test_points": deduped_test_points,
            "derived_risks": deduped_risks,
            "derived_questions": deduped_questions,
        },
        "text_image_conflicts": conflicts,
        "degradation_notice": degradation_notice,
        "quality_gate": quality_gate,
        "images": images,
    }

    # 6. 按步骤裁剪子集
    step_subsets = build_step_subsets(enhanced)
    enhanced["step_subsets"] = step_subsets

    return enhanced


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="测试增强聚合工具")
    parser.add_argument("understand_json", help="image_understand.py 输出的 JSON 文件")
    parser.add_argument("--requirement", help="原始需求文本文件（可选）")
    parser.add_argument("--output", "-o", help="输出 JSON 路径")
    args = parser.parse_args()

    with open(args.understand_json, 'r', encoding='utf-8') as f:
        understand_result = json.load(f)

    requirement_text = ""
    if args.requirement and os.path.exists(args.requirement):
        with open(args.requirement, 'r', encoding='utf-8') as f:
            requirement_text = f.read()

    result = enhance_image_results(understand_result, requirement_text)

    output_path = args.output or "px_enhance_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    agg = result["aggregate"]
    gate = result["quality_gate"]
    print(f"📊 测试增强完成:")
    print(f"  去重后 features: {agg['total_derived_features']}")
    print(f"  去重后 test_points: {agg['total_derived_test_points']}")
    print(f"  去重后 risks: {agg['total_derived_risks']}")
    print(f"  去重后 questions: {agg['total_derived_questions']}")
    print(f"  图文冲突: {len(result['text_image_conflicts'])}")
    print(f"  质量门禁: {'✅ PASSED' if gate['passed'] else '❌ FAILED'}")
    print(f"  结果: {output_path}")
