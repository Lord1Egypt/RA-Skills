#!/usr/bin/env python3
"""
管理体系审核报告生成脚本
生成带时间戳的 Markdown 格式审核报告
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="生成管理体系审核报告")
    parser.add_argument("--scope", required=True, help="审核范围描述")
    parser.add_argument("--files", required=True, help="文件清单 JSON")
    parser.add_argument("--analysis", required=True, help="分析结果 JSON")
    parser.add_argument("--output-dir", default=".", help="输出目录，默认为当前目录")
    parser.add_argument("--standard", default="未指定", help="比对的标准")
    return parser.parse_args()


def generate_timestamp():
    """生成时间戳"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def parse_files_json(files_str):
    """解析文件清单 JSON"""
    try:
        return json.loads(files_str)
    except json.JSONDecodeError:
        return []


def parse_analysis_json(analysis_str):
    """解析分析结果 JSON"""
    try:
        return json.loads(analysis_str)
    except json.JSONDecodeError:
        return {}


def generate_report(scope, files, analysis, standard, timestamp):
    """生成 Markdown 格式报告"""

    report = f"""# 管理体系审核报告

## 基本信息

| 项目 | 内容 |
|-----|------|
| 审核范围 | {scope} |
| 比对标准 | {standard} |
| 审核日期 | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |
| 报告编号 | AUD-{timestamp} |

---

## 一、文件清单

"""

    if files:
        report += "| 序号 | 文件编号 | 文件名称 | 版本 | 文件类型 | 关键要素 |\n"
        report += "|------|---------|---------|------|---------|--------|\n"
        for idx, f in enumerate(files, 1):
            report += f"| {idx} | {f.get('code', '-')} | {f.get('name', '-')} | {f.get('version', '-')} | {f.get('type', '-')} | {f.get('summary', '-')} |\n"
    else:
        report += "*未提供文件清单*\n"

    report += "\n---\n\n## 二、体系逻辑分析\n\n"

    # 体系架构分析
    system_architecture = analysis.get("system_architecture", {})
    report += "### 2.1 架构完整性评估\n\n"

    if system_architecture:
        report += f"- **范围定义**: {system_architecture.get('scope', '-')}\n"
        report += f"- **方针目标**: {system_architecture.get('policy_objectives', '-')}\n"
        report += f"- **组织职能**: {system_architecture.get('org_structure', '-')}\n"
        report += f"- **过程网络**: {system_architecture.get('process_network', '-')}\n"
        report += f"- **架构评估**: {system_architecture.get('assessment', '-')}\n"
    else:
        report += "*未提供架构分析数据*\n"

    report += "\n### 2.2 职责分工评估\n\n"

    responsibility = analysis.get("responsibility", {})
    if responsibility:
        report += f"- **组织架构**: {responsibility.get('org_chart', '-')}\n"
        report += f"- **职责分配**: {responsibility.get('assignment', '-')}\n"
        report += f"- **接口关系**: {responsibility.get('interfaces', '-')}\n"
        report += f"- **评估结论**: {responsibility.get('conclusion', '-')}\n"
    else:
        report += "*未提供职责分析数据*\n"

    report += "\n### 2.3 流程顺畅度评估\n\n"

    process = analysis.get("process", {})
    if process:
        report += f"- **流程闭环**: {process.get('closure', '-')}\n"
        report += f"- **瓶颈识别**: {process.get('bottlenecks', '-')}\n"
        report += f"- **评估结论**: {process.get('conclusion', '-')}\n"
    else:
        report += "*未提供流程分析数据*\n"

    report += "\n### 2.4 过程划分评估\n\n"

    process_division = analysis.get("process_division", {})
    if process_division:
        report += f"- **划分依据**: {process_division.get('basis', '-')}\n"
        report += f"- **合理性评价**: {process_division.get('reasonableness', '-')}\n"
        report += f"- **评估结论**: {process_division.get('conclusion', '-')}\n"
    else:
        report += "*未提供过程划分分析数据*\n"

    report += "\n---\n\n## 三、差异点清单\n\n"

    gaps = analysis.get("gaps", [])
    if gaps:
        report += "| 序号 | 差异类型 | 位置/模块 | 差异描述 | 风险等级 | 依据 |\n"
        report += "|------|---------|----------|---------|---------|------|\n"
        for idx, gap in enumerate(gaps, 1):
            report += f"| {idx} | {gap.get('type', '-')} | {gap.get('location', '-')} | {gap.get('description', '-')} | {gap.get('risk_level', '-')} | {gap.get('basis', '-')} |\n"
    else:
        report += "*未识别到差异点*\n"

    report += "\n---\n\n## 四、风险评估\n\n"

    risks = analysis.get("risks", [])
    if risks:
        report += "| 风险项 | 风险等级 | 风险描述 | 可能后果 | 改进建议 | 优先级 |\n"
        report += "|--------|---------|---------|---------|---------|------|\n"
        for risk in risks:
            report += f"| {risk.get('item', '-')} | {risk.get('level', '-')} | {risk.get('description', '-')} | {risk.get('consequence', '-')} | {risk.get('suggestion', '-')} | {risk.get('priority', '-')} |\n"
    else:
        report += "*未识别到风险项*\n"

    report += "\n---\n\n## 五、符合性评价\n\n"

    compliance = analysis.get("compliance", {})
    if compliance:
        report += "### 5.1 标准条款符合性\n\n"
        report += "| 条款 | 要求 | 符合性 | 说明 |\n"
        report += "|------|------|--------|------|\n"
        for clause in compliance.get("clauses", []):
            report += f"| {clause.get('id', '-')} | {clause.get('requirement', '-')} | {clause.get('status', '-')} | {clause.get('remark', '-')} |\n"

        report += f"\n### 5.2 符合率统计\n\n"
        report += f"- **总体符合率**: {compliance.get('compliance_rate', '-')}\n"
        report += f"- **严重不符合**: {compliance.get('critical', 0)} 项\n"
        report += f"- **重要不符合**: {compliance.get('major', 0)} 项\n"
        report += f"- **轻微不符合**: {compliance.get('minor', 0)} 项\n"
    else:
        report += "*未提供符合性评价数据*\n"

    report += "\n---\n\n## 六、改进建议\n\n"

    suggestions = analysis.get("suggestions", [])
    if suggestions:
        for idx, suggestion in enumerate(suggestions, 1):
            report += f"### {idx}. {suggestion.get('title', '改进项')}\n\n"
            report += f"- **问题描述**: {suggestion.get('problem', '-')}\n"
            report += f"- **改进目标**: {suggestion.get('goal', '-')}\n"
            report += f"- **建议措施**: {suggestion.get('measures', '-')}\n"
            report += f"- **预期效果**: {suggestion.get('expected', '-')}\n"
            report += f"- **实施建议**: {suggestion.get('implementation', '-')}\n\n"
    else:
        report += "*未提供改进建议*\n"

    report += "---\n\n## 七、审核结论\n\n"

    conclusion = analysis.get("conclusion", {})
    if conclusion:
        report += f"### 7.1 总体评价\n\n{conclusion.get('overall', '-')}\n\n"
        report += "### 7.2 改进优先级\n\n"
        for priority in conclusion.get('priorities', []):
            report += f"- **{priority.get('level', '-')}**: {priority.get('description', '-')}\n"
        report += "\n### 7.3 下一步工作建议\n\n"
        for action in conclusion.get('next_actions', []):
            report += f"- {action}\n"
    else:
        report += "*未提供审核结论*\n"

    report += f"""

---

## 附录

### A. 风险等级说明

| 等级 | 标识 | 说明 |
|-----|------|------|
| 严重 | CRITICAL | 可能导致认证失败、重大合规风险或体系失效 |
| 重要 | MAJOR | 可能影响体系有效性或客户满意度 |
| 轻微 | MINOR | 不影响体系有效性，但存在改进空间 |

### B. 符合性标识

| 标识 | 含义 |
|-----|------|
| 符合 | 完全满足标准要求 |
| 部分符合 | 基本满足但存在不足 |
| 不符合 | 未满足标准要求 |
| 不适用 | 该条款不适用于本组织 |

---

*本报告由管理体系审核技能自动生成*
*报告编号: AUD-{timestamp}*
"""

    return report


def main():
    args = parse_args()

    # 生成时间戳
    timestamp = generate_timestamp()

    # 解析 JSON 数据
    files = parse_files_json(args.files)
    analysis = parse_analysis_json(args.analysis)

    # 生成报告
    report = generate_report(
        scope=args.scope,
        files=files,
        analysis=analysis,
        standard=args.standard,
        timestamp=timestamp
    )

    # 生成文件名
    filename = f"audit_report_{timestamp}.md"
    output_path = Path(args.output_dir) / filename

    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    # 输出结果（JSON 格式供调用方解析）
    result = {
        "status": "success",
        "filename": filename,
        "path": str(output_path),
        "timestamp": timestamp
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 同时输出报告内容
    print("\n---REPORT_START---")
    print(report)
    print("---REPORT_END---")


if __name__ == "__main__":
    main()
