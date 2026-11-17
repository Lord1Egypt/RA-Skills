#!/usr/bin/env python3
"""
控制计划生成脚本
生成符合AIAG APQP标准的控制计划文档
"""

import argparse
import json
import os
from datetime import datetime
from jinja2 import Template

# 控制计划模板
CONTROL_PLAN_TEMPLATE = """# 控制计划 - {{ project_name }}

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {{ project_name }} |
| 版本 | {{ version }} |
| 日期 | {{ date }} |
| 编制人 | {{ author }} |
| 审核人 | {{ reviewer }} |

---

## 控制计划表头

| 公司名称 | {{ company_name }} |
|----------|-------------------|
| 控制计划编号 | {{ plan_number }} |
| 零件编号 | {{ part_number }} |
| 零件名称 | {{ part_name }} |
| 工艺编号 | {{ process_number }} |
| 关键联系人 | {{ contact }} |
| 客户名称 | {{ customer }} |
| 供应商/工厂 | {{ supplier }} |

---

## 阶段说明

| 阶段 | 说明 |
|------|------|
| 样件 |Prototype (prototype manufacturing) |
| 预生产 |Pre-Launch (pilot run) |
| 生产 |Production (mass production) |

---

## 控制计划内容

### 特殊特性符号说明

- **SC**: 特殊产品特性 (Special Characteristic - Customer designated)
- **CC**: 关键特性 (Critical Characteristic - Company designated)
- **KCC**: 关键控制特性 (Key Control Characteristic)
- **KPC**: 关键产品特性 (Key Product Characteristic)

---

| 序号 | 工序名称 | 工序编号 | 特殊特性 | 产品/过程特性 | 公差/规格 | 测量方法 | 样本容量 | 频率 | 控制方法 | 反应计划 | 责任人 |
|:----:|:---------|:--------:|:--------:|:--------------|:---------:|:---------|:--------:|:----:|:---------|:---------|:------:|
{% for item in items %}
| {{ loop.index }} | {{ item.process_name }} | {{ item.process_code }} | {{ item.special_chars }} | {{ item.characteristic }} | {{ item.tolerance }} | {{ item.measurement }} | {{ item.sample_size }} | {{ item.frequency }} | {{ item.control_method }} | {{ item.reaction }} | {{ item.owner }} |
{% endfor %}

---

## 不合格品处理流程

1. **隔离**: 发现不合格品立即隔离
2. **标识**: 使用红色标签标识
3. **记录**: 填写不合格品处理单
4. **评审**: 质量工程师评审
5. **处置**: 返工/返修/报废/让步接受
6. **追踪**: 分析根本原因，实施纠正措施

---

## 测量系统分析(MSA)要求

| 特性类型 | MSA要求 | 接受准则 |
|----------|--------|----------|
| 特殊特性 | 100%测量系统分析 | GRR < 10% |
| 关键特性 | 完整MSA | GRR < 20% |
| 一般特性 | 初始MSA | GRR < 30% |

---

## 过程能力要求

| 特性类型 | Cpk要求 | 备注 |
|----------|--------|------|
| 特殊产品特性(SC) | Cpk >= 1.67 | 客户指定 |
| 关键产品特性(CC) | Cpk >= 1.33 | 公司指定 |
| 一般产品特性 | Cpk >= 1.00 | 最低要求 |

---

## 版本历史

| 版本 | 日期 | 修改内容 | 审核人 |
|------|------|----------|--------|
| {{ version }} | {{ date }} | 初始版本 | {{ reviewer }} |

---

*文档生成时间: {{ generate_time }}*
"""

# 默认控制计划项目
DEFAULT_ITEMS = [
    {
        "process_name": "待补充-工序1",
        "process_code": "PC-001",
        "special_chars": "-",
        "characteristic": "待补充",
        "tolerance": "待补充",
        "measurement": "待补充",
        "sample_size": "待补充",
        "frequency": "待补充",
        "control_method": "待补充",
        "reaction": "待补充",
        "owner": "待定"
    }
]


def generate_control_plan(args):
    """生成控制计划文档"""
    
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
        "project_name": args.project,
        "version": args.version or "V1.0",
        "date": args.date or datetime.now().strftime("%Y-%m-%d"),
        "author": args.author or "待定",
        "reviewer": args.reviewer or "待定",
        "company_name": args.company_name or "公司名称",
        "plan_number": args.plan_number or "CP-001",
        "part_number": args.part_number or "待定",
        "part_name": args.part_name or "待定",
        "process_number": args.process_number or "待定",
        "contact": args.contact or "待定",
        "customer": args.customer or "待定",
        "supplier": args.supplier or "待定",
        "items": items,
        "generate_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 渲染模板
    template = Template(CONTROL_PLAN_TEMPLATE)
    output_content = template.render(**template_data)
    
    # 写入文件
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    # 返回JSON结果
    result = {
        "status": "success",
        "output": args.output,
        "project": args.project,
        "item_count": len(items),
        "special_char_count": sum(1 for item in items if item.get('special_chars', '-') != '-')
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description='生成控制计划文档')
    parser.add_argument('--project', required=True, help='项目名称')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--data', help='控制计划数据JSON文件路径(可选)')
    parser.add_argument('--version', help='文档版本')
    parser.add_argument('--date', help='文档日期')
    parser.add_argument('--author', help='编制人')
    parser.add_argument('--reviewer', help='审核人')
    parser.add_argument('--company-name', dest='company_name', help='公司名称')
    parser.add_argument('--plan-number', dest='plan_number', help='控制计划编号')
    parser.add_argument('--part-number', dest='part_number', help='零件编号')
    parser.add_argument('--part-name', dest='part_name', help='零件名称')
    parser.add_argument('--process-number', dest='process_number', help='工艺编号')
    parser.add_argument('--contact', help='联系人')
    parser.add_argument('--customer', help='客户名称')
    parser.add_argument('--supplier', help='供应商/工厂')
    
    args = parser.parse_args()
    generate_control_plan(args)


if __name__ == "__main__":
    main()
