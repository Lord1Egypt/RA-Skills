#!/usr/bin/env python3
"""
PPAP文件清单生成脚本
生成符合AIAG标准的PPAP提交清单
"""

import argparse
import json
import os
from datetime import datetime
from jinja2 import Template

# PPAP 19项要素定义
PPAP_ELEMENTS = [
    {"id": 1, "name": "设计记录", "chinese": "设计记录", "required_levels": [1,2,3,4,5], "description": "生产用设计记录(工程变更已体现)"},
    {"id": 2, "name": "工程变更文件", "chinese": "工程变更文件", "required_levels": [1,2,3,4,5], "description": "任何影响产品设计的工程变更文件"},
    {"id": 3, "name": "工程批准", "chinese": "工程批准", "required_levels": [1,2,3,4,5], "description": "如设计记录要求，需有工程批准签字"},
    {"id": 4, "name": "DFMEA", "chinese": "设计FMEA", "required_levels": [3,4,5], "description": "设计失效模式及影响分析"},
    {"id": 5, "name": "过程流程图", "chinese": "过程流程图", "required_levels": [1,2,3,4,5], "description": "描述生产过程的流程图"},
    {"id": 6, "name": "PFMEA", "chinese": "过程FMEA", "required_levels": [3,4,5], "description": "过程失效模式及影响分析"},
    {"id": 7, "name": "控制计划", "chinese": "控制计划", "required_levels": [1,2,3,4,5], "description": "描述控制方法和反应计划"},
    {"id": 8, "name": "测量系统分析", "chinese": "测量系统分析(MSA)", "required_levels": [3,4,5], "description": "量具R&R研究"},
    {"id": 9, "name": "全尺寸结果", "chinese": "全尺寸测量结果", "required_levels": [1,2,3,4,5], "description": "产品尺寸验证报告"},
    {"id": 10, "name": "材料/性能结果", "chinese": "材料/性能测试结果", "required_levels": [1,2,3,4,5], "description": "材料成分和机械性能测试"},
    {"id": 11, "name": "初始过程能力研究", "chinese": "初始过程能力研究", "required_levels": [1,2,3,4,5], "description": "Ppk研究报告"},
    {"id": 12, "name": "合格实验室", "chinese": "合格实验室文件", "required_levels": [3,4,5], "description": "内部或外部实验室资质证明"},
    {"id": 13, "name": "外观批准报告", "chinese": "外观批准报告(AAR)", "required_levels": [1,2,3,4,5], "description": "适用于外观件"},
    {"id": 14, "name": "生产件批准", "chinese": "生产件样品", "required_levels": [1,2,3,4,5], "description": "标准样品"},
    {"id": 15, "name": "标准样品", "chinese": "标准样品", "required_levels": [1,2,3,4,5], "description": "与生产件一致"},
    {"id": 16, "name": "检查辅具", "chinese": "检查辅具", "required_levels": [1,2,3,4,5], "description": "检具/夹具清单及认可"},
    {"id": 17, "name": "客户特殊要求", "chinese": "客户特殊要求符合性", "required_levels": [1,2,3,4,5], "description": "顾客规定的特殊要求"},
    {"id": 18, "name": "零件提交保证书", "chinese": "零件提交保证书(PSW)", "required_levels": [1,2,3,4,5], "description": "PSW表格-每位零件号一份"},
    {"id": 19, "name": "aira要求", "chinese": "AIRA要求", "required_levels": [1,2,3,4,5], "description": "顾客自行规定的其他要求"}
]

# PPAP提交等级说明
PPAP_LEVELS = {
    1: "仅提交零件提交保证书(PSW)",
    2: "提交PSW及样品和部分支持数据",
    3: "提交PSW、样品及完整支持数据",
    4: "提交PSW及其他规定要求",
    5: "提交PSW、样品及全部支持数据，现场审核"
}


def generate_ppap(args):
    """生成PPAP文件清单"""
    
    level = args.level
    
    # 根据提交等级确定需要提交的要素
    checklist = []
    for elem in PPAP_ELEMENTS:
        required = level in elem["required_levels"]
        item = {
            "id": elem["id"],
            "name": elem["name"],
            "chinese": elem["chinese"],
            "required": required,
            "description": elem["description"],
            "status": "pending",
            "notes": ""
        }
        checklist.append(item)
    
    # 创建输出目录
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
    
    # 生成JSON结果
    result_data = {
        "submission_info": {
            "customer": args.customer,
            "part_number": args.part_number,
            "level": level,
            "level_description": PPAP_LEVELS.get(level, "未知"),
            "submission_type": args.submission_type,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "required_elements": len([x for x in checklist if x["required"]]),
            "optional_elements": len([x for x in checklist if not x["required"]])
        },
        "checklist": checklist,
        "status_summary": {
            "total": len(checklist),
            "required": len([x for x in checklist if x["required"]]),
            "pending": len([x for x in checklist if x["required"]]),
            "completed": 0,
            "not_applicable": 0
        }
    }
    
    # 写入JSON文件
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    # 同时生成Markdown报告
    md_output = args.output.replace('.json', '.md')
    md_content = f"""# PPAP文件提交清单

## 提交信息

| 项目 | 内容 |
|------|------|
| 客户 | {args.customer} |
| 零件号 | {args.part_number} |
| 提交等级 | 等级{level} |
| 等级说明 | {PPAP_LEVELS.get(level)} |
| 提交类型 | {args.submission_type} |
| 提交日期 | {datetime.now().strftime('%Y-%m-%d')} |
| 必需要素数 | {len([x for x in checklist if x['required']])} |

---

## 状态说明

| 状态 | 说明 |
|------|------|
| pending | 待准备/待提交 |
| completed | 已完成 |
| not_applicable | 不适用 |

---

## PPAP 19项要素清单

| 序号 | 要素名称 | 必需 | 状态 | 备注 |
|:----:|:---------|:----:|:----:|------|
"""
    
    for item in checklist:
        md_content += f"| {item['id']} | {item['chinese']} | {'是' if item['required'] else '否'} | {item['status']} | {item['notes']} |\n"
    
    md_content += f"""
---

## 提交追踪

- [ ] 准备所有必需文件
- [ ] 完成内部审核
- [ ] 获取工程批准
- [ ] 提交客户
- [ ] 跟踪客户审批结果

---

*文件生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # 返回JSON结果
    result = {
        "status": "success",
        "json_output": args.output,
        "md_output": md_output,
        "submission_info": result_data["submission_info"],
        "status_summary": result_data["status_summary"]
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description='生成PPAP文件清单')
    parser.add_argument('--level', type=int, required=True, choices=[1,2,3,4,5], help='PPAP提交等级')
    parser.add_argument('--submission-type', dest='submission_type', required=True, 
                       help='提交类型:首次提交/重新提交/设计变更')
    parser.add_argument('--customer', required=True, help='客户名称')
    parser.add_argument('--part-number', dest='part_number', required=True, help='零件号')
    parser.add_argument('--output', required=True, help='输出JSON文件路径')
    
    args = parser.parse_args()
    generate_ppap(args)


if __name__ == "__main__":
    main()
