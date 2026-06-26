#!/usr/bin/env python3
"""
P5 分批预处理脚本 p5_prepare.py
读取 P2/P3/P4 输出 JSON，按模块分组，提取摘要，生成分批上下文文件。

集成模块:
  - p5_validate: 对每条测试点执行13项完整性自检
  - context_truncator: 基于字段优先级的智能截断，替代固定截断逻辑

变更日志:
  - _summarize_test_point: 输出从4字段扩展到22字段，不再截断description
  - generate_batch_contexts: 增加 p5_validate 自检 + context_truncator 智能截断
  - CLI: 新增 --model-name / --model-context-window / --context-used 参数

用法:
    python3 p5_prepare.py \
        --data-dir {DATA_DIR} \
        --output-dir {DATA_DIR}/p5_batches \
        --batch-size 8 \
        --model-name deepseek-v4-pro

无外部依赖，仅使用 Python 标准库。
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

# 新模块导入
from p5_validate import validate_prepared_point
from context_truncator import smart_truncate_for_batch

# 从orchestrator导入统一的batch_size常量（修复：p5与p6批次大小不一致问题）
try:
    from orchestrator import P6_BATCH_SIZE as _DEFAULT_BATCH_SIZE
except ImportError:
    _DEFAULT_BATCH_SIZE = 8  # 与orchestrator.py中P6_BATCH_SIZE保持一致


# ============================================================
# 摘要提取（22字段完整输出，由 context_truncator 负责智能截断）
# ============================================================

def _summarize_test_point(tp: dict, requirement_context: str = "") -> dict:
    """
    提取测试点完整摘要，输出22字段。
    不再截断 description，保留完整内容供下游消费。

    Args:
        tp: 原始测试点 dict
        requirement_context: 需求上下文（用于智能截断时的参考）

    Returns:
        dict: 包含22个标准字段的测试点摘要
    """
    # 22字段完整输出（按优先级分组：P0 → P1 → P2 → P3）
    # V4.7.0: 新增 step_expected_pairs + field_checklist（供给P6 Agent具体参考）
    return {
        # P0 - 绝对保留
        "id":                      tp.get("id", ""),
        "title":                   tp.get("title", ""),
        "description":             tp.get("description", ""),  # 不再截断
        "status":                  tp.get("status", ""),

        # P1 - 必备字段
        "page_path":               tp.get("page_path", ""),
        "operations_chain":        tp.get("operations_chain", []),
        "field_specs":             tp.get("field_specs", []),
        "business_rules":          tp.get("business_rules", []),
        # V4.7.0: 步骤-期望骨架（从operations_chain提取，供给P6 Agent引用）
        "step_expected_pairs":     tp.get("step_expected_pairs", []),
        # V4.7.0: 需求字段清单（从P0 field_specs汇总，供给G1/G7引用）
        "field_checklist":         tp.get("field_checklist", []),

        # P2 - 推荐字段
        "precondition":            tp.get("precondition", ""),
        "category":                tp.get("category", ""),
        "priority":                tp.get("priority", tp.get("priority_hint", "")),
        "priority_reason":         tp.get("priority_reason", ""),
        "requirement_completeness": tp.get("requirement_completeness", None),
        "field_target":            tp.get("field_target", ""),
        "related_roles":           tp.get("related_roles", []),
        "related_rules":           tp.get("related_rules", []),
        "source_scenario":         tp.get("source_scenario", ""),
        "is_smoke_candidate":      tp.get("is_smoke_candidate", False),

        # P3 - 可截断字段
        "exception_scenarios":     tp.get("exception_scenarios", []),
        "ui_elements":             tp.get("ui_elements", []),
        "test_data_matrix":        tp.get("test_data_matrix", []),
        "meta":                    tp.get("meta", {}),
    }


def _summarize_risk(risk: dict) -> dict:
    """提取风险点摘要"""
    return {
        "id": risk.get("id", risk.get("risk_id", "")),
        "description": risk.get("description", "")[:120],
        "severity": risk.get("severity", risk.get("impact", "")),
    }


def _summarize_pci(pci: dict) -> dict:
    """提取 PCI 摘要"""
    return {
        "id": pci.get("id", pci.get("pci_id", "")),
        "question": pci.get("question", pci.get("description", ""))[:120],
        "blocking": pci.get("blocking", pci.get("impact", "") == "blocker"),
    }


# ============================================================
# 模块前缀提取
# ============================================================

def _extract_module_prefix(source_scenario: str) -> str:
    """
    从 source_scenario 提取一级模块前缀。
    例如: "REQ-001-M01-F01-S01" → "REQ-001-M01"
          "REQ-001-M01-登录功能" → "REQ-001-M01"
    规则: 取前三段（以 '-' 分隔），如果不足三段则取全部。
    """
    if not source_scenario:
        return "UNKNOWN"
    parts = source_scenario.split("-")
    # 标准格式: REQ-001-M01-...，取前3段
    if len(parts) >= 3:
        return "-".join(parts[:3])
    return source_scenario


# ============================================================
# 关联匹配：将 risk/pci 关联到模块
# ============================================================

def _match_risks_to_module(risks: list, module_prefix: str, tp_ids: set) -> list:
    """筛选与模块相关的风险点"""
    matched = []
    for risk in risks:
        # 通过 related_scenario 或 affected_test_points 关联
        related = risk.get("related_scenario", risk.get("source_scenario", ""))
        affected = set(risk.get("affected_test_points", []))
        if (related and related.startswith(module_prefix)) or (affected & tp_ids):
            matched.append(_summarize_risk(risk))
    return matched


def _match_pcis_to_module(pcis: list, module_prefix: str, tp_ids: set) -> list:
    """筛选与模块相关的 PCI"""
    matched = []
    for pci in pcis:
        blocked = set(pci.get("blocked_scenarios", pci.get("blocked_test_points", [])))
        related = pci.get("related_scenario", pci.get("source_scenario", ""))
        if (related and related.startswith(module_prefix)) or (blocked & tp_ids):
            matched.append(_summarize_pci(pci))
    return matched


# ============================================================
# 核心逻辑
# ============================================================

def load_json_safe(path: str, key: str) -> list:
    """安全加载 JSON 文件并提取指定数组字段"""
    if not os.path.exists(path):
        print(f"[p5_prepare] 警告: 文件不存在 {path}", file=sys.stderr)
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 支持直接数组或嵌套在对象中
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get(key, [])
        return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"[p5_prepare] 错误: 读取 {path} 失败: {e}", file=sys.stderr)
        return []


def group_by_module(test_points: list) -> dict:
    """按一级模块前缀分组"""
    groups = defaultdict(list)
    for tp in test_points:
        scenario = tp.get("source_scenario", tp.get("id", ""))
        module = _extract_module_prefix(scenario)
        groups[module].append(tp)
    return dict(groups)


def split_into_batches(module_groups: dict, batch_size: int) -> list:
    """
    将模块分组拆分为批次。
    每组 ≤ batch_size 个测试点，超出则拆分为多个子批。
    返回: [(module, [test_points]), ...]
    """
    batches = []
    for module, tps in sorted(module_groups.items()):
        if len(tps) <= batch_size:
            batches.append((module, tps))
        else:
            # 拆分为多个子批
            for i in range(0, len(tps), batch_size):
                chunk = tps[i:i + batch_size]
                suffix = f"-part{i // batch_size + 1}" if len(tps) > batch_size else ""
                batches.append((f"{module}{suffix}", chunk))
    return batches


def generate_batch_contexts(data_dir: str, output_dir: str, batch_size: int,
                              model_name: str = None, model_context_window: int = None,
                              context_used: int = 0) -> dict:
    """
    主流程：读取上游数据 → 分组 → 分批 → 生成上下文文件。
    集成 p5_validate (13项自检) + context_truncator (智能截断)。
    返回 prepare_summary。

    Args:
        data_dir: 上游数据目录
        output_dir: 输出目录
        batch_size: 每批最大测试点数
        model_name: 模型名称（用于 context_truncator 自动选择窗口大小）
        model_context_window: 手动指定上下文窗口大小（优先于 model_name）
        context_used: 已使用的上下文 token 数
    """
    # 1. 读取上游数据
    p2_path = os.path.join(data_dir, "p2_output.json")
    p3_path = os.path.join(data_dir, "p3_output.json")
    p4_path = os.path.join(data_dir, "p4_output.json")

    test_points = load_json_safe(p2_path, "test_points")
    risk_points = load_json_safe(p3_path, "risk_points")
    pci_list = load_json_safe(p4_path, "pci_list")

    print(f"[p5_prepare] 读取完成: test_points={len(test_points)}, "
          f"risk_points={len(risk_points)}, pci_list={len(pci_list)}", file=sys.stderr)

    # 2. 按模块分组
    module_groups = group_by_module(test_points)
    print(f"[p5_prepare] 模块分组: {len(module_groups)} 个模块", file=sys.stderr)

    # 3. 拆分为批次
    batches = split_into_batches(module_groups, batch_size)
    print(f"[p5_prepare] 拆分为 {len(batches)} 个批次", file=sys.stderr)

    # 4. 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 5. 生成每个批次的上下文文件
    summary_batches = []
    total_tp_count = 0
    total_validation_issues = 0

    for idx, (module, tps) in enumerate(batches, start=1):
        tp_ids = {tp.get("id", "") for tp in tps}

        # 使用22字段完整摘要，传入需求上下文
        requirement_context = f"模块: {module}, 测试点数: {len(tps)}"
        tp_summaries = [_summarize_test_point(tp, requirement_context=requirement_context)
                        for tp in tps]

        # ---- p5_validate: 13项自检 ----
        validation_issues = []
        for tp in tp_summaries:
            issues = validate_prepared_point(tp)
            if issues:
                validation_issues.append({
                    "id": tp.get("id", "UNKNOWN"),
                    "issues": issues,
                })
                total_validation_issues += len(issues)

        if validation_issues:
            print(f"[p5_prepare] 批次 {idx} 自检发现 {len(validation_issues)} 条测试点有问题 "
                  f"({total_validation_issues} 项issue)", file=sys.stderr)

        # ---- context_truncator: 智能截断 ----
        truncated_summaries, truncation_report = smart_truncate_for_batch(
            tp_summaries,
            model_name=model_name,
            model_context_window=model_context_window,
            context_used=context_used,
        )

        # 关联风险点和 PCI
        module_prefix = module.split("-part")[0]  # 去掉 -partN 后缀
        related_risks = _match_risks_to_module(risk_points, module_prefix, tp_ids)
        related_pcis = _match_pcis_to_module(pci_list, module_prefix, tp_ids)

        batch_context = {
            "batch_id": idx,
            "module": module,
            "p2_test_points": truncated_summaries,
            "p3_risks": related_risks,
            "p4_pcis": related_pcis,
            "validation": {
                "issues_count": len(validation_issues),
                "details": validation_issues if validation_issues else None,
            },
            "stats": {
                "test_point_count": len(truncated_summaries),
                "risk_count": len(related_risks),
                "pci_count": len(related_pcis),
            },
        }

        # 写入批次文件
        batch_path = os.path.join(output_dir, f"batch_{idx}_context.json")
        with open(batch_path, "w", encoding="utf-8") as f:
            json.dump(batch_context, f, ensure_ascii=False, indent=2)

        # 写入截断报告
        truncation_path = os.path.join(output_dir, f"batch_{idx}_truncation_report.md")
        with open(truncation_path, "w", encoding="utf-8") as f:
            f.write(truncation_report)

        summary_batches.append({
            "batch_id": idx,
            "module": module,
            "test_point_count": len(truncated_summaries),
            "validation_issues": len(validation_issues),
        })
        total_tp_count += len(truncated_summaries)

    # 6. 生成汇总文件
    summary = {
        "total_batches": len(batches),
        "total_test_points": total_tp_count,
        "batch_size": batch_size,
        "total_validation_issues": total_validation_issues,
        "batches": summary_batches,
    }

    summary_path = os.path.join(output_dir, "prepare_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"[p5_prepare] 完成: {len(batches)} 个批次, {total_tp_count} 个测试点, "
          f"{total_validation_issues} 项自检问题", file=sys.stderr)
    return summary


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="P5 分批预处理：读取 P2/P3/P4 输出，按模块分组生成分批上下文"
    )
    parser.add_argument("--data-dir", required=True,
                        help="上游数据目录（含 p2_output.json, p3_output.json, p4_output.json）")
    parser.add_argument("--output-dir", default=None,
                        help="输出目录（默认 {data-dir}/p5_batches）")
    parser.add_argument("--batch-size", type=int, default=None,
                        help=f"每批最大测试点数（默认 {_DEFAULT_BATCH_SIZE}，与orchestrator P6_BATCH_SIZE一致）")
    parser.add_argument("--model-name", default=None,
                        help="模型名称（用于智能截断自动选择上下文窗口大小）")
    parser.add_argument("--model-context-window", type=int, default=None,
                        help="手动指定模型上下文窗口大小（tokens）")
    parser.add_argument("--context-used", type=int, default=0,
                        help="已使用的上下文 token 数（默认 0）")
    args = parser.parse_args()

    output_dir = args.output_dir or os.path.join(args.data_dir, "p5_batches")

    # 未指定batch_size时使用与orchestrator统一的常量
    batch_size = args.batch_size if args.batch_size is not None else _DEFAULT_BATCH_SIZE

    result = generate_batch_contexts(
        args.data_dir, output_dir, batch_size,
        model_name=args.model_name,
        model_context_window=args.model_context_window,
        context_used=args.context_used,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
