#!/usr/bin/env python3
"""
风险分析脚本
综合分析FMEA和控制计划，输出风险评估报告
"""

import argparse
import json
import os
import re
from datetime import datetime
from jinja2 import Template

# 风险分析报告模板
RISK_REPORT_TEMPLATE = """# APQP项目风险分析报告

## 项目信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {{ project_name }} |
| 分析日期 | {{ date }} |
| 分析依据 | FMEA、控制计划 |

---

## 执行摘要

- **整体风险等级**: {{ overall_risk_level }}
- **高风险项数量**: {{ high_risk_count }}
- **中风险项数量**: {{ medium_risk_count }}
- **低风险项数量**: {{ low_risk_count }}
- **建议优先级**: {{ priority_recommendation }}

---

## 风险矩阵

### RPN分布统计

| RPN范围 | 风险等级 | 数量 | 占比 | 建议行动 |
|---------|----------|------|------|----------|
| RPN > 200 | 高 | {{ rpn_high }} | {{ rpn_high_pct }}% | 立即处理 |
| 100 < RPN <= 200 | 中 | {{ rpn_medium }} | {{ rpn_medium_pct }}% | 尽快处理 |
| RPN <= 100 | 低 | {{ rpn_low }} | {{ rpn_low_pct }}% | 监控 |

### 严重度分布

| 严重度 | 数量 | 占比 | 说明 |
|--------|------|------|------|
| S >= 8 | {{ severity_high }} | {{ severity_high_pct }}% | 安全/法规相关，需重点关注 |
| 5 <= S < 8 | {{ severity_medium }} | {{ severity_medium_pct }}% | 功能受影响 |
| S < 5 | {{ severity_low }} | {{ severity_low_pct }}% | 一般问题 |

---

## 高风险项清单 (RPN > 100)

{% if high_risk_items %}
| 优先级 | 编号 | 项目 | 失效模式 | RPN | S | O | D | 建议措施 |
|:------:|:----:|:-----|:---------|:---:|:-:|:-:|:-:|:--------|
{% for item in high_risk_items %}
| {{ loop.index }} | {{ item.id }} | {{ item.project }} | {{ item.failure_mode }} | **{{ item.rpn }}** | {{ item.severity }} | {{ item.occurrence }} | {{ item.detection }} | {{ item.action }} |
{% endfor %}
{% else %}
无高风险项
{% endif %}

---

## 特殊特性风险分析

{% if special_characteristics %}
### 产品特殊特性 (SC) - 客户指定

| 特性 | 控制方法 | 当前状态 | 风险评估 |
|:-----|:---------|:---------|:---------|
{% for char in special_characteristics %}
| {{ char.name }} | {{ char.control }} | {{ char.status }} | {{ char.risk }} |
{% endfor %}

{% else %}
暂无特殊特性信息
{% endif %}

---

## 关键过程风险

{% if key_processes %}
| 工序 | 风险类型 | 当前控制 | 建议改进 |
|:-----|:---------|:---------|:---------|
{% for proc in key_processes %}
| {{ proc.name }} | {{ proc.risk_type }} | {{ proc.current_control }} | {{ proc.improvement }} |
{% endfor %}

{% else %}
暂无关键过程风险
{% endif %}

---

## 改进建议

### 紧急措施 (立即执行)
1. {{ urgent_action1 }}
2. {{ urgent_action2 }}
3. {{ urgent_action3 }}

### 短期措施 (1-2周内)
1. {{ short_action1 }}
2. {{ short_action2 }}

### 中期措施 (1个月内)
1. {{ medium_action1 }}
2. {{ medium_action2 }}

---

## 下次审查计划

- **审查日期**: {{ next_review_date }}
- **审查重点**: {{ review_focus }}
- **责任人**: {{ review_owner }}

---

*报告生成时间: {{ generate_time }}*
"""


def parse_fmea_file(file_path):
    """解析FMEA文件提取风险数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        items = []
        
        # 解析表格行
        lines = content.split('\n')
        in_table = False
        for line in lines:
            if '|' in line and line.strip().startswith('|'):
                parts = [p.strip() for p in line.split('|')]
                # 检查是否是FMEA数据行(包含数字)
                if len(parts) >= 12:
                    try:
                        # 尝试提取RPN相关数据
                        if any(p.isdigit() for p in parts):
                            severity = int(parts[5]) if parts[5].isdigit() else 5
                            occurrence = int(parts[7]) if parts[7].isdigit() else 5
                            detection = int(parts[9]) if parts[9].isdigit() else 5
                            rpn = severity * occurrence * detection
                            
                            items.append({
                                "failure_mode": parts[3] if len(parts) > 3 else "",
                                "effect": parts[4] if len(parts) > 4 else "",
                                "severity": severity,
                                "cause": parts[6] if len(parts) > 6 else "",
                                "occurrence": occurrence,
                                "detection": detection,
                                "rpn": rpn,
                                "action": parts[10] if len(parts) > 10 else ""
                            })
                    except (ValueError, IndexError):
                        continue
        
        return items
    except Exception as e:
        print(f"解析FMEA文件出错: {e}")
        return []


def parse_control_plan(file_path):
    """解析控制计划文件提取特殊特性"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        special_chars = []
        
        # 查找包含SC/CC/KCC/KPC的行
        for line in content.split('\n'):
            if '|' in line and any(marker in line for marker in ['SC', 'CC', 'KCC', 'KPC']):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 8:
                    special_chars.append({
                        "name": parts[3] if len(parts) > 3 else "",
                        "control": parts[7] if len(parts) > 7 else "",
                        "status": "需确认",
                        "risk": "待评估"
                    })
        
        return special_chars
    except Exception as e:
        print(f"解析控制计划文件出错: {e}")
        return []


def analyze_risk(args):
    """执行风险分析"""
    
    project_name = args.project or "APQP项目"
    
    # 解析FMEA文件
    all_fmea_items = []
    if args.fmea_files:
        for fmea_file in args.fmea_files.split(','):
            fmea_file = fmea_file.strip()
            if os.path.exists(fmea_file):
                items = parse_fmea_file(fmea_file)
                all_fmea_items.extend(items)
    
    # 解析控制计划文件
    special_chars = []
    if args.control_plan and os.path.exists(args.control_plan):
        special_chars = parse_control_plan(args.control_plan)
    
    # 计算风险统计
    high_risk = [item for item in all_fmea_items if item['rpn'] > 100]
    medium_risk = [item for item in all_fmea_items if 50 < item['rpn'] <= 100]
    low_risk = [item for item in all_fmea_items if item['rpn'] <= 50]
    
    severity_high = len([item for item in all_fmea_items if item['severity'] >= 8])
    severity_medium = len([item for item in all_fmea_items if 5 <= item['severity'] < 8])
    severity_low = len([item for item in all_fmea_items if item['severity'] < 5])
    
    total = len(all_fmea_items) if all_fmea_items else 1
    
    # 确定整体风险等级
    if len(high_risk) > 5 or severity_high > 3:
        overall_risk = "高风险"
        priority = "必须优先处理所有高RPN项"
    elif len(high_risk) > 0 or severity_high > 0:
        overall_risk = "中风险"
        priority = "建议近期处理高RPN项"
    else:
        overall_risk = "低风险"
        priority = "持续监控即可"
    
    # 排序高风险项
    high_risk_sorted = sorted(high_risk, key=lambda x: x['rpn'], reverse=True)[:20]
    
    # 生成默认的特殊特性和关键过程
    key_processes = [
        {"name": "待补充", "risk_type": "待评估", "current_control": "待补充", "improvement": "待补充"}
    ]
    
    # 创建输出目录
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
    
    # 准备模板数据
    template_data = {
        "project_name": project_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "overall_risk_level": overall_risk,
        "high_risk_count": len(high_risk),
        "medium_risk_count": len(medium_risk),
        "low_risk_count": len(low_risk),
        "priority_recommendation": priority,
        "rpn_high": len(high_risk),
        "rpn_medium": len(medium_risk),
        "rpn_low": len(low_risk),
        "rpn_high_pct": round(len(high_risk) / total * 100, 1),
        "rpn_medium_pct": round(len(medium_risk) / total * 100, 1),
        "rpn_low_pct": round(len(low_risk) / total * 100, 1),
        "severity_high": severity_high,
        "severity_medium": severity_medium,
        "severity_low": severity_low,
        "severity_high_pct": round(severity_high / total * 100, 1),
        "severity_medium_pct": round(severity_medium / total * 100, 1),
        "severity_low_pct": round(severity_low / total * 100, 1),
        "high_risk_items": high_risk_sorted,
        "special_characteristics": special_chars if special_chars else None,
        "key_processes": key_processes,
        "urgent_action1": "审查所有RPN>150的失效模式" if high_risk else "当前无紧急高风险项",
        "urgent_action2": "确认严重度>=8项的预防措施" if severity_high > 0 else "持续监控质量指标",
        "urgent_action3": "更新控制计划特殊特性标识",
        "short_action1": "组织FMEA评审会议" if all_fmea_items else "完善FMEA数据",
        "short_action2": "制定纠正措施计划",
        "medium_action1": "验证纠正措施有效性",
        "medium_action2": "更新FMEA和控制计划",
        "next_review_date": "一周内",
        "review_focus": "高RPN项改进措施落实情况",
        "review_owner": "质量工程师",
        "generate_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 渲染模板
    template = Template(RISK_REPORT_TEMPLATE)
    report_content = template.render(**template_data)
    
    # 写入文件
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    # 返回JSON结果
    result = {
        "status": "success",
        "output": args.output,
        "project": project_name,
        "overall_risk_level": overall_risk,
        "risk_summary": {
            "high_risk": len(high_risk),
            "medium_risk": len(medium_risk),
            "low_risk": len(low_risk)
        },
        "severity_summary": {
            "high": severity_high,
            "medium": severity_medium,
            "low": severity_low
        },
        "priority_recommendation": priority
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description='APQP项目风险分析')
    parser.add_argument('--fmea-files', dest='fmea_files', help='FMEA文件路径(逗号分隔多个文件)')
    parser.add_argument('--control-plan', dest='control_plan', help='控制计划文件路径')
    parser.add_argument('--output', required=True, help='输出报告路径')
    parser.add_argument('--project', help='项目名称')
    
    args = parser.parse_args()
    analyze_risk(args)


if __name__ == "__main__":
    main()
