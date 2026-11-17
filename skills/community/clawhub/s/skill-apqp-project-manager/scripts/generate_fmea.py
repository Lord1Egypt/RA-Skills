#!/usr/bin/env python3
"""
FMEA生成脚本 - 支持DFMEA和PFMEA
生成符合AIAG-VDA标准的FMEA文档
"""

import argparse
import json
import os
from datetime import datetime
from jinja2 import Template

# FMEA模板
FMEA_TEMPLATE = """# {{ fmea_type }} - {{ project_name }}

## 项目信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {{ project_name }} |
| FMEA类型 | {{ fmea_type }} |
| 版本 | {{ version }} |
| 日期 | {{ date }} |
| 负责人 | {{ owner }} |

---

## 评分标准

### 严重度(S)评分准则

| 评分 | 描述 | 说明 |
|------|------|------|
| 10 | 危险无警告 | 潜在失效模式影响安全/法规，无警告 |
| 9 | 危险有警告 | 潜在失效模式影响安全/法规，有警告 |
| 8 | 很高 | 产品不工作，丧失基本功能 |
| 7 | 高 | 产品能工作但性能下降，客户严重不满 |
| 6 | 中等 | 产品能工作但舒适度下降，客户不满 |
| 5 | 低 | 产品能工作但存在不便，客户轻度不满 |
| 4 | 很低 | 产品能工作但存在小瑕疵 |
| 3 | 轻微 | 存在轻微缺陷，几乎不被注意 |
| 2 | 极轻微 | 几乎不被注意的缺陷 |
| 1 | 无 | 无可察觉的影响 |

### 频度(O)评分准则

| 评分 | 描述 | 预计PPM |
|------|------|---------|
| 10 | 极高 | >100 |
| 9 | 很高 | 50-100 |
| 8 | 高 | 20-50 |
| 7 | 中高 | 10-20 |
| 6 | 中等 | 2-10 |
| 5 | 中低 | 0.5-2 |
| 4 | 低 | 0.1-0.5 |
| 3 | 很低 | 0.01-0.1 |
| 2 | 极低 | <0.01 |
| 1 | 极不可能 | 失效几乎不可能 |

### 探测度(D)评分准则

| 评分 | 描述 | 探测方法 |
|------|------|----------|
| 10 | 绝对不确定 | 无法探测或未计划探测 |
| 9 | 很渺茫 | 探测方法几乎无效 |
| 8 | 渺茫 | 探测方法效果很差 |
| 7 | 很低的概率 | 探测方法效果低 |
| 6 | 低 | 探测方法效果有限 |
| 5 | 中等 | 探测方法效果中等 |
| 4 | 中高 | 探测方法效果较好 |
| 3 | 高 | 探测方法效果好 |
| 2 | 很高 | 探测方法效果很好 |
| 1 | 几乎确定 | 探测方法几乎完美 |

---

## FMEA分析表

### 风险优先级数(RPN) = S × O × D

| 项目 | 项号 | 功能 | 潜在失效模式 | 潜在失效影响 | 严重度S | 潜在原因 | 频度O | 现行控制-预防 | 现行控制-探测 | 探测度D | RPN | 推荐措施 | 责任人 | 目标日期 | 措施结果 |
|:----:|:----:|:-----|:------------|:------------|:-------:|:--------|:-----:|:------------|:------------|:-------:|:---:|:--------|:------:|:--------:|:-------:|
{% for item in items %}
| {{ fmea_type[:2] }} | {{ loop.index }} | {{ item.function }} | {{ item.failure_mode }} | {{ item.effect }} | {{ item.severity }} | {{ item.cause }} | {{ item.occurrence }} | {{ item.prevention }} | {{ item.detection }} | {{ item.detection_d }} | {{ item.severity * item.occurrence * item.detection_d }} | {{ item.action }} | {{ item.owner }} | {{ item.target_date }} | {{ item.result }} |
{% endfor %}

---

## 高RPN项追踪 (RPN > {{ rpn_threshold }})

{% set high_rpn = [] %}
{% for item in items %}
{% if item.severity * item.occurrence * item.detection_d > rpn_threshold %}
{% set _ = high_rpn.append(item) %}
{% endif %}
{% endfor %}

{% if high_rpn %}
| 排名 | 项号 | 功能 | 失效模式 | RPN | 优先级 |
|:----:|:----:|:-----|:--------|:---:|:------:|
{% for item in high_rpn|sort(attribute='severity * occurrence * detection_d', reverse=True) %}
| {{ loop.index }} | {{ loop.index }} | {{ item.function }} | {{ item.failure_mode }} | {{ item.severity * item.occurrence * item.detection_d }} | {{ '高' if item.severity * item.occurrence * item.detection_d > 200 else '中' }} |
{% endfor %}
{% else %}
无高RPN项（当前RPN均低于{{ rpn_threshold }}）
{% endif %}

---

## 团队成员

| 角色 | 姓名 | 职责 |
|------|------|------|
| FMEA负责人 | {{ owner }} | 主导FMEA编制与维护 |
| 设计工程师 | {{ designer }} | 提供设计输入与评审 |
| 质量工程师 | {{ quality_engineer }} | 质量标准与验证 |
| 工艺工程师 | {{ process_engineer }} | 工艺可行性评估 |

---

## 版本历史

| 版本 | 日期 | 修改内容 | 审核人 |
|------|------|----------|--------|
| {{ version }} | {{ date }} | 初始版本 | {{ owner }} |

---

*文档生成时间: {{ generate_time }}*
"""

# 默认FMEA项目数据
DEFAULT_ITEMS = [
    {
        "function": "待补充-功能1",
        "failure_mode": "待补充",
        "effect": "待补充",
        "severity": 5,
        "cause": "待补充",
        "occurrence": 5,
        "prevention": "待补充",
        "detection": "待补充",
        "detection_d": 5,
        "action": "待补充",
        "owner": "待定",
        "target_date": "待定",
        "result": "待执行"
    }
]


def generate_fmea(args):
    """生成FMEA文档"""
    
    # 解析类型
    fmea_type = "DFMEA" if args.type.lower() == "dfmea" else "PFMEA"
    
    # 如果没有提供数据，生成模板
    if not args.data:
        items = DEFAULT_ITEMS.copy()
    else:
        try:
            with open(args.data, 'r', encoding='utf-8') as f:
                items = json.load(f)
        except:
            items = DEFAULT_ITEMS.copy()
    
    # 创建输出目录
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
    
    # 准备模板数据
    template_data = {
        "fmea_type": fmea_type,
        "project_name": args.project,
        "version": args.version or "V1.0",
        "date": args.date or datetime.now().strftime("%Y-%m-%d"),
        "owner": args.owner or "待定",
        "designer": args.designer or "待定",
        "quality_engineer": args.quality_engineer or "待定",
        "process_engineer": args.process_engineer or "待定",
        "items": items,
        "rpn_threshold": args.rpn_threshold or 100,
        "generate_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 渲染模板
    template = Template(FMEA_TEMPLATE)
    output_content = template.render(**template_data)
    
    # 写入文件
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    # 返回JSON结果
    result = {
        "status": "success",
        "output": args.output,
        "fmea_type": fmea_type,
        "project": args.project,
        "item_count": len(items),
        "high_rpn_count": sum(1 for item in items if item.get('severity', 5) * item.get('occurrence', 5) * item.get('detection_d', 5) > (args.rpn_threshold or 100))
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description='生成FMEA文档（DFMEA/PFMEA）')
    parser.add_argument('--type', required=True, choices=['dfmea', 'pfmea'], help='FMEA类型')
    parser.add_argument('--project', required=True, help='项目名称')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--data', help='FMEA数据JSON文件路径(可选)')
    parser.add_argument('--version', help='文档版本')
    parser.add_argument('--date', help='文档日期')
    parser.add_argument('--owner', help='FMEA负责人')
    parser.add_argument('--designer', help='设计工程师')
    parser.add_argument('--quality-engineer', dest='quality_engineer', help='质量工程师')
    parser.add_argument('--process-engineer', dest='process_engineer', help='工艺工程师')
    parser.add_argument('--rpn-threshold', dest='rpn_threshold', type=int, default=100, help='RPN阈值(默认100)')
    
    args = parser.parse_args()
    generate_fmea(args)


if __name__ == "__main__":
    main()
