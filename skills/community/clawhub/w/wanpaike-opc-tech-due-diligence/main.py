#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
万湃客-OPC-技术尽调 - 通用入口（Coze环境主入口）
提供参数化的技术尽调报告生成功能，支持任意公司/项目的技术尽调。

用法:
    python main.py <json_data>
    python main.py '{"company_name": "某科技公司", "industry": "AI", "findings": {...}}'

输出:
    结构化JSON报告（含四层评估、评分、投资建议）
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


def generate_dd_report(company_name: str, industry: str, findings: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成通用技术尽调报告

    Args:
        company_name: 被调公司名称
        industry: 所属行业
        findings: 尽调发现，支持以下字段：
            - basic_info: Dict[str, Dict] 公司基本信息，每个值为 {"claimed": "声明值", "verified": "核实结果", "note": "说明"}
            - team_info: Dict[str, Any] 团队信息
            - patent_info: Dict[str, Dict] 专利信息，每个值为 {"claimed": "声明值", "verified": "核实结果", "note": "说明"}
            - tech_claims: List[Dict] 技术声明列表，每个含 {"声明": "", "核实结果": "", "说明": "", "质疑点": ""}
            - financial_indicators: Dict[str, str] 财务指标
            - risk_assessment: List[Dict] 风险评估，每个含 {"风险类型": "", "等级": "高/中/低", "描述": ""}
            - overall_score: float 综合评分（1-10）
            - investment_advice: str 投资建议
            - data_sources: List[str] 数据来源列表
            - follow_up: List[Dict] 后续跟进事项
            - tech_score/team_score/market_score/finance_score/commercial_score/risk_score: float 各维度评分
            - pros/cons: List[str] 推荐/谨慎理由

    Returns:
        结构化报告字典
    """
    report = {
        "report_title": f"{company_name}技术尽调报告",
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "company_name": company_name,
        "industry": industry,
        "executive_summary": _generate_executive_summary(company_name, findings),
        "core_conclusion": {
            "score": findings.get("overall_score", 5.0),
            "advice": findings.get("investment_advice", "待评估"),
            "one_line_conclusion": _generate_one_line_conclusion(findings)
        },
        "layers": {
            "layer1_fact_check": _generate_layer1(company_name, findings),
            "layer2_cross_verify": _generate_layer2(findings),
            "layer3_risk_analysis": _generate_layer3(findings),
            "layer4_investment_advice": _generate_layer4(findings)
        },
        "appendix": {
            "data_sources": findings.get("data_sources", []),
            "follow_up_items": _generate_follow_up(findings)
        }
    }
    return report


def _generate_executive_summary(company_name: str, findings: Dict) -> str:
    """生成摘要"""
    score = findings.get("overall_score", 5.0)
    if score >= 8:
        return f"{company_name}技术实力强，团队背景可靠，建议重点关注。"
    elif score >= 6:
        return f"{company_name}技术有一定基础，但存在若干风险点，需进一步核实后决策。"
    elif score >= 4:
        return f"{company_name}技术存在较多不确定性，建议谨慎评估，深入尽调后再决定。"
    else:
        return f"{company_name}存在重大风险，不建议投资。"


def _generate_one_line_conclusion(findings: Dict) -> str:
    """生成一句话结论"""
    risks = findings.get("risk_assessment", [])
    high_risks = [r for r in risks if r.get("等级") == "高"]
    if len(high_risks) >= 3:
        return "存在重大风险，不建议投资"
    elif len(high_risks) >= 1:
        return "存在风险，需进一步核实"
    else:
        return "技术基本可靠，可进入下一轮评估"


def _generate_layer1(company_name: str, findings: Dict) -> List[Dict]:
    """第一层：信息提取与核实"""
    items = []
    basic = findings.get("basic_info", {})
    for key, value in basic.items():
        items.append({
            "核查项": key,
            "声明内容": value.get("claimed", ""),
            "核实结果": value.get("verified", "待核实"),
            "说明": value.get("note", "")
        })

    patents = findings.get("patent_info", {})
    for key, value in patents.items():
        items.append({
            "核查项": f"专利-{key}",
            "声明内容": value.get("claimed", ""),
            "核实结果": value.get("verified", "待核实"),
            "说明": value.get("note", "")
        })

    return items


def _generate_layer2(findings: Dict) -> List[Dict]:
    """第二层：交叉验证与质疑"""
    items = []
    for claim in findings.get("tech_claims", []):
        items.append({
            "技术声明": claim.get("声明", ""),
            "核实结果": claim.get("核实结果", "待核实"),
            "说明": claim.get("说明", ""),
            "质疑点": claim.get("质疑点", "")
        })
    return items


def _generate_layer3(findings: Dict) -> List[Dict]:
    """第三层：深度风险分析"""
    risks = []
    for risk in findings.get("risk_assessment", []):
        risks.append({
            "风险类型": risk.get("风险类型", ""),
            "风险等级": risk.get("等级", "中"),
            "具体描述": risk.get("描述", "")
        })
    return risks


def _generate_layer4(findings: Dict) -> Dict:
    """第四层：投资建议与评分"""
    return {
        "综合评分": {
            "技术壁垒": findings.get("tech_score", 5.0),
            "团队实力": findings.get("team_score", 5.0),
            "市场前景": findings.get("market_score", 5.0),
            "财务健康": findings.get("finance_score", 5.0),
            "商业化能力": findings.get("commercial_score", 5.0),
            "风险可控性": findings.get("risk_score", 5.0),
        },
        "投资建议": findings.get("investment_advice", "待评估"),
        "推荐理由": findings.get("pros", []),
        "谨慎理由": findings.get("cons", [])
    }


def _generate_follow_up(findings: Dict) -> List[Dict]:
    """生成后续跟进事项"""
    items = []
    for i, item in enumerate(findings.get("follow_up", []), 1):
        items.append({
            "序号": i,
            "核实事项": item.get("事项", ""),
            "优先级": item.get("优先级", "中"),
            "说明": item.get("说明", "")
        })
    return items


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("❌ 用法: python main.py '<json_data>'")
        print("")
        print("json_data示例:")
        print('  python main.py \'{"company_name": "某科技公司", "industry": "AI", "findings": {}}\'')
        print("")
        print("findings结构说明:")
        print("  basic_info:       公司基本信息核查结果")
        print("  patent_info:      专利信息核查结果")
        print("  tech_claims:      技术声明列表")
        print("  risk_assessment:  风险评估列表")
        print("  overall_score:    综合评分(1-10)")
        print("  investment_advice: 投资建议")
        print("  data_sources:     数据来源列表")
        sys.exit(1)

    try:
        input_data = json.loads(sys.argv[1])
        company_name = input_data.get("company_name", "未知公司")
        industry = input_data.get("industry", "未知行业")
        findings = input_data.get("findings", {})

        report = generate_dd_report(company_name, industry, findings)
        print(json.dumps(report, ensure_ascii=False, indent=2))

    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        print("请检查JSON格式是否正确。")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()