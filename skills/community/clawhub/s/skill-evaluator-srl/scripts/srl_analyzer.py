#!/usr/bin/env python3
"""
SRL (Skill Reliability Level) Analyzer v2
接收 AI 评审输出的结构化 JSON 数据，执行加权计算、等级映射、报告生成。
脚本不做任何语义分析或关键词匹配，所有语义判断由 AI 完成。

架构:
  AI 阅读 Skill 内容 → 输出结构化评分 JSON → 本脚本计算 → 输出报告

Usage:
    # 从 stdin 读取 JSON
    echo '{"skill_name":"xxx", ...}' | python3 srl_analyzer.py

    # 从文件读取 JSON
    python3 srl_analyzer.py --input eval-data.json

    # 输出 JSON 格式（默认 Markdown）
    python3 srl_analyzer.py --input eval-data.json --json

    # 批量模式（输入为 JSON 数组）
    python3 srl_analyzer.py --input batch-data.json --batch
"""

import json
import re
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional


# ============================================================
# 常量
# ============================================================

# 五维权重
DIMENSION_WEIGHTS = {
    "anchor_density": 0.25,
    "hallucination_exposure": 0.20,
    "failure_transparency": 0.20,
    "traceability": 0.20,
    "reproducibility": 0.15,
}

DIMENSION_NAMES_CN = {
    "anchor_density": "工程锚点密度",
    "hallucination_exposure": "幻觉暴露面",
    "failure_transparency": "失败语义清晰度",
    "traceability": "溯源性",
    "reproducibility": "可重现性推断",
}

# SRL 等级阈值
SRL_THRESHOLDS = [
    (90, 5, "★★★★★", "全流程工程化，可进入自动化决策链路"),
    (75, 4, "★★★★", "关键步骤锚定可靠平台，结果基本可复现"),
    (60, 3, "★★★", "混入部分弱校验环节，适合在明确边界下使用"),
    (40, 2, "★★", "大量依赖互联网信息或 AI 推理，需人工复核"),
    (0, 1, "★", "全链路 AI 推理，无工程锚点，不建议用于正式决策"),
]


# ============================================================
# 输入数据 Schema
# ============================================================

INPUT_SCHEMA = {
    "skill_name": "str, Skill 名称",
    "skill_path": "str, Skill 目录路径",
    "description": "str, Skill 简短描述",
    "tier": "int (1/2/3), Skill 类型分档: 1=确定性, 2=半确定性, 3=非确定性",
    "evaluation_confidence": "str (optional), 评估置信度: 'normal'(默认) 或 'low'(降级评估)",
    "dimensions": {
        "anchor_density": {
            "score": "int 0-100, AI 对工程锚点密度的评分",
            "sub_scores": {
                "anchor_coverage": "int 0-40, 锚点覆盖率（有锚点的阶段数/总阶段数）",
                "anchor_intensity": "int 0-30, 锚点密度（锚点总数/总阶段数）",
                "verification_loop": "int 0-30, 验证闭环（操作→确认的完整闭环数）",
            },
            "anchoring_answers": "object (optional), 锚定问题的回答记录（Q1/Q2/Q3 的结构化回答，供复核）",
            "evidence": ["str, 关键证据列表"],
        },
        "...": "(其他 4 个维度结构相同，均含 score/sub_scores/anchoring_answers/evidence)",
    },
    "corrections": {
        "timeliness": "int 0-100, 时效性评分（修正因子）",
        "robustness": "int 0-100, 鲁棒性评分（修正因子）",
        "cascade_stability": "int 0-100, 级联稳定性评分（修正因子）",
    },
    "improvement_suggestions": ["str, AI 给出的改进建议列表"],
    "quality_checks": {
        "sub_scores_sum_match": "bool, 每个维度的子项求和是否等于 score",
        "scores_in_range": "bool, 所有分数是否在 0-100 范围内",
        "evidence_count_ok": "bool, 每个维度是否至少 2 条 evidence",
        "anchoring_answers_present": "bool, 每个维度是否包含 anchoring_answers",
        "all_passed": "bool, 以上全部通过",
    },
    "metadata": {
        "total_files": "int, 文件总数",
        "total_lines": "int, 代码总行数",
        "skill_md_lines": "int, SKILL.md 行数",
        "total_phases": "int, 阶段数",
        "total_steps": "int, 步骤数",
        "has_scripts": "bool, 是否有脚本目录",
        "has_references": "bool, 是否有参考文档",
        "script_files": ["str, 脚本文件路径列表"],
    },
}


# ============================================================
# 子项 Schema 定义（名称 → 满分上限）
# ============================================================

DIMENSION_SUB_SCHEMA = {
    "anchor_density": {
        "anchor_coverage": 40,
        "anchor_intensity": 30,
        "verification_loop": 30,
    },
    "hallucination_exposure": {
        "speculative_ratio": 40,
        "external_validation": 30,
        "output_determinism": 30,
    },
    "failure_transparency": {
        "error_handling_strategy": 40,
        "confidence_degradation": 30,
        "idk_capability": 30,
    },
    "traceability": {
        "source_classification": 40,
        "citation_annotation": 30,
        "independent_verifiability": 30,
    },
    "reproducibility": {
        "tier_determinism": 40,
        "state_management": 30,
        "step_determinism": 30,
    },
}

CORRECTION_KEYS = ["timeliness", "robustness", "cascade_stability"]


# ============================================================
# 计算引擎
# ============================================================

def validate_input(data: dict) -> Tuple[List[str], List[str]]:
    """严格校验输入数据的完整性和一致性。

    返回 (errors, warnings):
      - errors: 阻断性错误，必须修复后重新提交
      - warnings: 非阻断性警告，不影响计算但建议修复

    校验项：
      1. 顶层必填字段: skill_name, dimensions
      2. 五个维度是否齐全
      3. 每个维度的 score 是否为 0-100 的数字
      4. 每个维度的 sub_scores:
         a. 子项名称是否正确（不能多、不能少、不能拼错）
         b. 每个子项是否为数字且 ≥ 0
         c. 每个子项是否 ≤ 满分上限
         d. 子项求和是否等于 score（允许 ±1 容差）
      5. evidence 是否为非空列表（至少 2 条）
      6. corrections 三个修正因子是否为 0-100
      7. tier 是否为 1/2/3
      8. improvement_suggestions 是否为非空列表
    """
    errors = []
    warnings = []

    # ---- 1. 顶层必填字段 ----
    if not data.get("skill_name"):
        errors.append("缺少 skill_name（Skill 名称）")

    if "dimensions" not in data or not isinstance(data.get("dimensions"), dict):
        errors.append("缺少 dimensions 对象（五维评分数据）")
        return errors, warnings  # 无法继续校验

    # tier 校验
    tier = data.get("tier")
    if tier is not None:
        if tier not in (1, 2, 3):
            errors.append(f"tier 应为 1/2/3，当前值: {tier}")
    else:
        warnings.append("缺少 tier 字段（Skill 类型分档），将默认为 2")

    # ---- 2. 五维度齐全性 ----
    dims = data["dimensions"]
    required_dims = list(DIMENSION_WEIGHTS.keys())
    for dim_key in required_dims:
        if dim_key not in dims:
            errors.append(
                f"缺少维度 '{dim_key}'（{DIMENSION_NAMES_CN[dim_key]}），"
                f"需要包含 score, sub_scores, evidence 三个字段"
            )

    # ---- 3-5. 逐维度校验 ----
    for dim_key in required_dims:
        if dim_key not in dims:
            continue

        dim = dims[dim_key]
        dim_cn = DIMENSION_NAMES_CN[dim_key]
        prefix = f"dimensions.{dim_key}"

        # 3. score 存在性和范围
        if "score" not in dim:
            errors.append(f"{prefix}.score 缺失（{dim_cn}的总分）")
            continue

        score = dim["score"]
        if not isinstance(score, (int, float)):
            errors.append(f"{prefix}.score 应为数字，当前类型: {type(score).__name__}")
            continue
        if score < 0 or score > 100:
            errors.append(f"{prefix}.score 应为 0-100，当前值: {score}")

        # 4. sub_scores 校验
        expected_subs = DIMENSION_SUB_SCHEMA.get(dim_key, {})
        actual_subs = dim.get("sub_scores", {})

        if not actual_subs:
            warnings.append(f"{prefix}.sub_scores 为空，建议提供子项评分以提高透明度")
        else:
            # 4a. 检查多余的子项（拼写错误）
            extra_keys = set(actual_subs.keys()) - set(expected_subs.keys())
            if extra_keys:
                errors.append(
                    f"{prefix}.sub_scores 包含未知子项: {sorted(extra_keys)}，"
                    f"允许的子项为: {sorted(expected_subs.keys())}"
                )

            # 4a. 检查缺失的子项
            missing_keys = set(expected_subs.keys()) - set(actual_subs.keys())
            if missing_keys:
                errors.append(
                    f"{prefix}.sub_scores 缺少子项: {sorted(missing_keys)}，"
                    f"每个子项都必须提供评分"
                )

            # 4b-c. 逐子项校验
            sub_sum = 0
            for sub_key, max_val in expected_subs.items():
                if sub_key not in actual_subs:
                    continue
                sub_val = actual_subs[sub_key]

                if not isinstance(sub_val, (int, float)):
                    errors.append(
                        f"{prefix}.sub_scores.{sub_key} 应为数字，"
                        f"当前类型: {type(sub_val).__name__}"
                    )
                    continue

                if sub_val < 0:
                    errors.append(f"{prefix}.sub_scores.{sub_key} 不能为负数，当前值: {sub_val}")

                if sub_val > max_val:
                    errors.append(
                        f"{prefix}.sub_scores.{sub_key} 超出满分上限 "
                        f"(当前 {sub_val} > 满分 {max_val})"
                    )

                sub_sum += sub_val

            # 4d. 子项求和 vs score 一致性（允许 ±1 容差，兼容四舍五入）
            if not missing_keys and not extra_keys and isinstance(score, (int, float)):
                if abs(sub_sum - score) > 1:
                    errors.append(
                        f"{prefix}: 子项求和={sub_sum} ≠ score={score}，"
                        f"差值={abs(sub_sum - score)}（允许误差 ±1）。"
                        f"请确保 score 等于所有 sub_scores 之和"
                    )

        # 5. evidence 校验
        evidence = dim.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"{prefix}.evidence 应为列表，当前类型: {type(evidence).__name__}")
        elif len(evidence) < 2:
            warnings.append(
                f"{prefix}.evidence 仅有 {len(evidence)} 条（建议至少 2 条），"
                f"证据不足会降低评估报告的说服力"
            )
        else:
            # 5b. evidence 格式校验：检查是否包含文件引用
            # 合法格式示例: "SKILL.md:47 xxx", "scripts/foo.py:135 xxx", "SKILL.md 第 47 行 xxx"
            ref_pattern = re.compile(
                r'(?:'
                r'[\w./\-]+\.(?:md|py|js|ts|sh|json|yaml|yml)[\s:：]'  # 文件名+扩展名
                r'|第\s*\d+\s*行'  # "第 X 行"
                r'|:\d+'  # ":行号"
                r'|阶段\s*\d+'  # "阶段 X"
                r')',
                re.IGNORECASE,
            )
            unref_evidence = []
            for ev in evidence:
                if isinstance(ev, str) and not ref_pattern.search(ev):
                    unref_evidence.append(ev[:60])
            if unref_evidence:
                warnings.append(
                    f"{prefix}.evidence 中有 {len(unref_evidence)} 条缺少文件/行号引用"
                    f"（证据应包含具体位置如 'SKILL.md:47' 或 '第 X 行'），"
                    f"示例: \"{unref_evidence[0]}...\""
                )

    # ---- 6. corrections 校验 ----
    corrections = data.get("corrections", {})
    if not corrections:
        warnings.append("缺少 corrections（修正因子），将默认不触发任何修正")
    else:
        if not isinstance(corrections, dict):
            errors.append(f"corrections 应为对象，当前类型: {type(corrections).__name__}")
        else:
            for ck in CORRECTION_KEYS:
                if ck not in corrections:
                    warnings.append(f"corrections.{ck} 缺失，将默认为 100（不触发修正）")
                else:
                    cv = corrections[ck]
                    if not isinstance(cv, (int, float)):
                        errors.append(
                            f"corrections.{ck} 应为数字，当前类型: {type(cv).__name__}"
                        )
                    elif cv < 0 or cv > 100:
                        errors.append(f"corrections.{ck} 应为 0-100，当前值: {cv}")

    # ---- 7. improvement_suggestions 校验 ----
    suggestions = data.get("improvement_suggestions", [])
    if not isinstance(suggestions, list):
        warnings.append("improvement_suggestions 应为列表")
    elif len(suggestions) == 0:
        warnings.append("improvement_suggestions 为空，建议至少提供 3 条改进建议")

    # ---- 8. anchoring_answers 校验（每个维度应包含锚定问题回答） ----
    for dim_key in required_dims:
        if dim_key not in dims:
            continue
        dim = dims[dim_key]
        prefix = f"dimensions.{dim_key}"
        if "anchoring_answers" not in dim or not dim["anchoring_answers"]:
            warnings.append(
                f"{prefix}.anchoring_answers 缺失或为空，"
                f"建议包含锚定问题的回答记录以确保评分可复核"
            )

    # ---- 9. quality_checks 校验 ----
    qc = data.get("quality_checks")
    if qc is None:
        warnings.append("缺少 quality_checks（评分质量自检结果），建议包含以提高透明度")
    elif isinstance(qc, dict):
        if qc.get("all_passed") is False:
            warnings.append(
                "quality_checks.all_passed = false，AI 自检发现问题，请关注报告中的警告"
            )

    # ---- 10. evaluation_confidence 校验 ----
    ec = data.get("evaluation_confidence")
    if ec is not None and ec not in ("normal", "low"):
        warnings.append(f"evaluation_confidence 应为 'normal' 或 'low'，当前值: {ec}")

    return errors, warnings


def apply_corrections(dimensions: dict, corrections: dict) -> dict:
    """应用修正因子，返回修正后的维度评分。

    修正逻辑（线性连续，非二值触发）：
    - 时效性: 修正量 = max(0, (50 - score) / 50) * 20%，影响可重现性
    - 级联稳定性: 修正量 = max(0, (50 - score) / 50) * 20%，影响可重现性
    - 鲁棒性: 修正量 = max(0, (50 - score) / 50) * 10%，影响幻觉暴露面
    评分 ≥ 50 时不修正，< 50 时线性扣减，0 分时扣减最大。
    """
    corrected = {}
    correction_log = []

    for key, dim in dimensions.items():
        corrected[key] = dim.get("score", 0)

    if not corrections:
        return corrected, correction_log

    timeliness = corrections.get("timeliness", 100)
    robustness = corrections.get("robustness", 100)
    cascade = corrections.get("cascade_stability", 100)

    # 时效性 → 修正可重现性（最大扣 20%）
    if timeliness < 50:
        penalty = max(0, (50 - timeliness) / 50) * 0.20
        old = corrected["reproducibility"]
        corrected["reproducibility"] = round(old * (1 - penalty), 1)
        correction_log.append(
            f"时效性={timeliness} (<50) → 可重现性从 {old} 扣减 {penalty:.1%} 至 {corrected['reproducibility']}"
        )

    # 级联稳定性 → 修正可重现性（最大扣 20%）
    if cascade < 50:
        penalty = max(0, (50 - cascade) / 50) * 0.20
        old = corrected["reproducibility"]
        corrected["reproducibility"] = round(old * (1 - penalty), 1)
        correction_log.append(
            f"级联稳定性={cascade} (<50) → 可重现性从 {old} 扣减 {penalty:.1%} 至 {corrected['reproducibility']}"
        )

    # 鲁棒性 → 修正幻觉暴露面（最大扣 10%）
    if robustness < 50:
        penalty = max(0, (50 - robustness) / 50) * 0.10
        old = corrected["hallucination_exposure"]
        corrected["hallucination_exposure"] = round(old * (1 - penalty), 1)
        correction_log.append(
            f"鲁棒性={robustness} (<50) → 幻觉暴露面从 {old} 扣减 {penalty:.1%} 至 {corrected['hallucination_exposure']}"
        )

    return corrected, correction_log


def calculate_final_score(corrected_scores: dict) -> float:
    """加权求和计算最终得分。"""
    total = 0.0
    for key, weight in DIMENSION_WEIGHTS.items():
        total += corrected_scores.get(key, 0) * weight
    return round(total, 1)


def map_srl_level(score: float) -> Tuple[int, str, str]:
    """映射最终得分到 SRL 等级。返回 (等级, 星级, 使用建议)。"""
    for threshold, level, stars, recommendation in SRL_THRESHOLDS:
        if score >= threshold:
            return level, stars, recommendation
    return 1, "★", "全链路 AI 推理，无工程锚点，不建议用于正式决策"


# ============================================================
# 报告生成
# ============================================================

def generate_markdown_report(data: dict, corrected_scores: dict,
                             correction_log: List[str],
                             final_score: float, srl_level: int,
                             stars: str, recommendation: str,
                             warnings: List[str] = None) -> str:
    """生成 Markdown 格式报告。"""
    lines = []
    skill_name = data.get("skill_name", "Unknown")
    skill_path = data.get("skill_path", "N/A")
    description = data.get("description", "")
    tier = data.get("tier", 2)
    dims = data.get("dimensions", {})
    corrections = data.get("corrections", {})
    metadata = data.get("metadata", {})
    improvements = data.get("improvement_suggestions", [])

    lines.append(f"# SRL 评估报告: {skill_name}")
    lines.append("")
    lines.append(f"> 路径: `{skill_path}`")
    if description:
        lines.append(f"> 描述: {description}")
    lines.append(f"> Tier 分类: Tier {tier}")
    lines.append("")

    # 总评
    lines.append("## 总评")
    lines.append("")
    lines.append("| 指标 | 值 |")
    lines.append("|------|-----|")
    lines.append(f"| **最终得分** | **{final_score}/100** |")
    lines.append(f"| **SRL 等级** | **SRL-{srl_level}** |")
    lines.append(f"| **星级** | {stars} |")
    lines.append(f"| **使用建议** | {recommendation} |")
    lines.append("")

    # 五维评分
    lines.append("## 五维评分明细")
    lines.append("")
    lines.append("| 维度 | 原始分 | 修正后 | 权重 | 加权 |")
    lines.append("|------|--------|--------|------|------|")
    for key in DIMENSION_WEIGHTS:
        weight = DIMENSION_WEIGHTS[key]
        name_cn = DIMENSION_NAMES_CN[key]
        raw = dims.get(key, {}).get("score", 0)
        corrected = corrected_scores.get(key, 0)
        weighted = round(corrected * weight, 1)
        bar = "█" * int(corrected / 10) + "░" * (10 - int(corrected / 10))
        corrected_mark = f" ⚠️" if raw != corrected else ""
        lines.append(f"| {name_cn} | {raw} | {corrected}{corrected_mark} {bar} | {int(weight*100)}% | {weighted} |")
    lines.append("")

    # 子项评分
    lines.append("## 子项评分明细")
    lines.append("")
    for key in DIMENSION_WEIGHTS:
        name_cn = DIMENSION_NAMES_CN[key]
        dim = dims.get(key, {})
        sub_scores = dim.get("sub_scores", {})
        if not sub_scores:
            continue

        lines.append(f"### {name_cn}")
        lines.append("")
        lines.append("| 子项 | 得分 |")
        lines.append("|------|------|")
        for sub_key, sub_val in sub_scores.items():
            lines.append(f"| {sub_key} | {sub_val} |")
        lines.append("")

        evidence = dim.get("evidence", [])
        if evidence:
            lines.append("**评估证据:**")
            for ev in evidence:
                lines.append(f"- {ev}")
            lines.append("")

    # 修正因子
    if corrections:
        lines.append("## 修正因子")
        lines.append("")
        lines.append("| 因子 | 评分 | 是否触发修正 | 影响 |")
        lines.append("|------|------|-------------|------|")
        timeliness = corrections.get("timeliness", 100)
        robustness = corrections.get("robustness", 100)
        cascade = corrections.get("cascade_stability", 100)
        lines.append(f"| 时效性 | {timeliness} | {'✅ 是' if timeliness < 50 else '否'} | 可重现性线性扣减，最大20% |")
        lines.append(f"| 鲁棒性 | {robustness} | {'✅ 是' if robustness < 50 else '否'} | 幻觉暴露面线性扣减，最大10% |")
        lines.append(f"| 级联稳定性 | {cascade} | {'✅ 是' if cascade < 50 else '否'} | 可重现性线性扣减，最大20% |")
        lines.append("")

    if correction_log:
        lines.append("**修正记录:**")
        for log in correction_log:
            lines.append(f"- {log}")
        lines.append("")

    # 元数据
    if metadata:
        lines.append("## 关键指标")
        lines.append("")
        lines.append("| 指标 | 值 |")
        lines.append("|------|-----|")
        for mk, mv in metadata.items():
            if isinstance(mv, list):
                mv = ", ".join(str(v) for v in mv) if mv else "无"
            lines.append(f"| {mk} | {mv} |")
        lines.append("")

    # 改进建议
    if improvements:
        lines.append("## 改进行动清单")
        lines.append("")
        for i, action in enumerate(improvements, 1):
            lines.append(f"{i}. {action}")
        lines.append("")

    # 校验警告
    if warnings:
        lines.append("## ⚠️ 数据质量警告")
        lines.append("")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    return "\n".join(lines)


def generate_json_report(data: dict, corrected_scores: dict,
                          correction_log: List[str],
                          final_score: float, srl_level: int,
                          stars: str, recommendation: str,
                          warnings: List[str] = None) -> str:
    """生成 JSON 格式报告。"""
    dims = data.get("dimensions", {})
    corrections = data.get("corrections", {})

    report = {
        "skill_name": data.get("skill_name", ""),
        "skill_path": data.get("skill_path", ""),
        "description": data.get("description", ""),
        "evaluation_confidence": data.get("evaluation_confidence", "normal"),
        "tier": data.get("tier", 2),
        "final_score": final_score,
        "srl_level": srl_level,
        "star_rating": stars,
        "usage_recommendation": recommendation,
        "dimensions": {},
        "corrected_scores": corrected_scores,
        "corrections": {
            "input": corrections,
            "log": correction_log,
            "timeliness_triggered": corrections.get("timeliness", 100) < 50,
            "robustness_triggered": corrections.get("robustness", 100) < 50,
            "cascade_triggered": corrections.get("cascade_stability", 100) < 50,
        },
        "metadata": data.get("metadata", {}),
        "improvement_suggestions": data.get("improvement_suggestions", []),
        "validation_warnings": warnings or [],
    }

    for key in DIMENSION_WEIGHTS:
        dim = dims.get(key, {})
        report["dimensions"][key] = {
            "name_cn": DIMENSION_NAMES_CN[key],
            "weight": DIMENSION_WEIGHTS[key],
            "raw_score": dim.get("score", 0),
            "corrected_score": corrected_scores.get(key, 0),
            "weighted_score": round(corrected_scores.get(key, 0) * DIMENSION_WEIGHTS[key], 1),
            "sub_scores": dim.get("sub_scores", {}),
            "evidence": dim.get("evidence", []),
        }

    return json.dumps(report, ensure_ascii=False, indent=2)


# ============================================================
# 主控流程
# ============================================================

def process_single(data: dict, output_json: bool = False) -> str:
    """处理单个 Skill 评估数据，返回报告字符串。"""
    errors, warnings = validate_input(data)
    if errors:
        error_msg = "❌ 输入数据验证失败（请修复后重新提交）:\n\n"
        for i, e in enumerate(errors, 1):
            error_msg += f"  {i}. {e}\n"
        if warnings:
            error_msg += "\n⚠️ 另有以下警告:\n\n"
            for w in warnings:
                error_msg += f"  - {w}\n"
        error_msg += f"\n💡 提示: 运行 `python3 srl_analyzer.py --schema` 查看完整输入格式说明"
        if output_json:
            return json.dumps({"error": errors, "warnings": warnings}, ensure_ascii=False, indent=2)
        return error_msg

    # warnings 不阻断，但会记录到报告中
    dims = data.get("dimensions", {})
    corrections = data.get("corrections", {})

    corrected_scores, correction_log = apply_corrections(dims, corrections)
    final_score = calculate_final_score(corrected_scores)
    srl_level, stars, recommendation = map_srl_level(final_score)

    if output_json:
        return generate_json_report(
            data, corrected_scores, correction_log,
            final_score, srl_level, stars, recommendation,
            warnings=warnings,
        )
    else:
        return generate_markdown_report(
            data, corrected_scores, correction_log,
            final_score, srl_level, stars, recommendation,
            warnings=warnings,
        )


def process_batch(data_list: list, output_json: bool = False) -> str:
    """处理批量评估数据。"""
    if output_json:
        results = []
        for data in data_list:
            result = json.loads(process_single(data, output_json=True))
            results.append(result)
        return json.dumps(results, ensure_ascii=False, indent=2)

    lines = []

    # 汇总表
    lines.append("## Skill SRL 评估汇总\n")
    lines.append(f"| {'Skill':<30} | {'得分':>6} | {'SRL':>5} | {'星级':<10} | {'Tier':>4} |")
    lines.append(f"|{'-'*32}|{'-'*8}|{'-'*7}|{'-'*12}|{'-'*6}|")

    reports = []
    skipped = []
    for data in data_list:
        errors, warnings = validate_input(data)
        if errors:
            skipped.append((data.get("skill_name", "Unknown"), errors))
            continue
        dims = data.get("dimensions", {})
        corrections = data.get("corrections", {})
        corrected_scores, correction_log = apply_corrections(dims, corrections)
        final_score = calculate_final_score(corrected_scores)
        srl_level, stars, recommendation = map_srl_level(final_score)

        reports.append((data, corrected_scores, correction_log,
                       final_score, srl_level, stars, recommendation, warnings))

    reports.sort(key=lambda x: x[3], reverse=True)

    for data, cs, cl, fs, sl, st, rec, _w in reports:
        name = data.get("skill_name", "Unknown")
        tier = data.get("tier", 2)
        lines.append(f"| {name:<30} | {fs:>5.1f} | SRL-{sl} | {st:<10} | T{tier:>3} |")

    lines.append("\n---\n")

    for data, cs, cl, fs, sl, st, rec, w in reports:
        md = generate_markdown_report(data, cs, cl, fs, sl, st, rec, warnings=w)
        lines.append(md)
        lines.append("\n---\n")

    if skipped:
        lines.append("## ❌ 校验失败，已跳过的 Skill\n")
        for name, errs in skipped:
            lines.append(f"### {name}\n")
            for e in errs:
                lines.append(f"- {e}")
            lines.append("")

    return "\n".join(lines)


def print_schema():
    """打印输入 JSON Schema 说明。"""
    print("=" * 60)
    print("SRL Analyzer v2 — 输入 JSON Schema")
    print("=" * 60)
    print()
    print("本脚本接收 AI 评审输出的结构化 JSON，执行加权计算和报告生成。")
    print("所有语义分析由 AI 完成，脚本只做数学计算。")
    print()
    print("输入 Schema:")
    print(json.dumps(INPUT_SCHEMA, ensure_ascii=False, indent=2))
    print()
    print("示例最小输入:")
    minimal = {
        "skill_name": "example-skill",
        "skill_path": "/path/to/skill",
        "description": "一个示例 Skill",
        "tier": 2,
        "dimensions": {
            "anchor_density": {"score": 70, "sub_scores": {}, "evidence": []},
            "hallucination_exposure": {"score": 65, "sub_scores": {}, "evidence": []},
            "failure_transparency": {"score": 55, "sub_scores": {}, "evidence": []},
            "traceability": {"score": 60, "sub_scores": {}, "evidence": []},
            "reproducibility": {"score": 50, "sub_scores": {}, "evidence": []},
        },
        "corrections": {
            "timeliness": 70,
            "robustness": 60,
            "cascade_stability": 55,
        },
        "improvement_suggestions": [
            "在关键 API 调用后添加返回值校验",
            "为不确定的步骤添加置信度标注",
        ],
    }
    print(json.dumps(minimal, ensure_ascii=False, indent=2))


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="SRL Analyzer v2 — 接收 AI 结构化评分，计算 SRL 等级",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从 stdin 读取
  echo '{"skill_name":"xxx", ...}' | python3 srl_analyzer.py

  # 从文件读取
  python3 srl_analyzer.py --input eval-data.json

  # JSON 输出
  python3 srl_analyzer.py --input eval-data.json --json

  # 批量模式
  python3 srl_analyzer.py --input batch-data.json --batch

  # 查看输入 Schema
  python3 srl_analyzer.py --schema
        """,
    )
    parser.add_argument("--input", "-i", help="输入 JSON 文件路径（不指定则从 stdin 读取）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式（默认 Markdown）")
    parser.add_argument("--batch", action="store_true", help="批量模式（输入为 JSON 数组）")
    parser.add_argument("--schema", action="store_true", help="打印输入 JSON Schema 说明")

    args = parser.parse_args()

    if args.schema:
        print_schema()
        sys.exit(0)

    # 读取输入
    try:
        if args.input:
            with open(args.input, "r", encoding="utf-8") as f:
                raw = f.read()
        else:
            raw = sys.stdin.read()

        if not raw.strip():
            print("Error: 输入为空。使用 --schema 查看输入格式说明。", file=sys.stderr)
            sys.exit(1)

        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: 文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 处理
    if args.batch:
        if not isinstance(data, list):
            print("Error: 批量模式需要 JSON 数组输入", file=sys.stderr)
            sys.exit(1)
        result = process_batch(data, output_json=args.json)
    else:
        if isinstance(data, list):
            print("Error: 非批量模式不接受数组输入，使用 --batch 标志", file=sys.stderr)
            sys.exit(1)
        result = process_single(data, output_json=args.json)

    print(result)


if __name__ == "__main__":
    main()
