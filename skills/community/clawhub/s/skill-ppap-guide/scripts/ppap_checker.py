#!/usr/bin/env python3
"""
PPAP文件完整性检查工具
检查PPAP提交的18项要求是否完整，并验证格式正确性
"""

import argparse
import json
import sys
from typing import Dict, List, Any

# PPAP 18项提交要求定义
PPAP_REQUIREMENTS = [
    {"id": 1, "name": "设计记录", "chinese": "设计记录", "required_levels": [1, 2, 3, 4, 5], "description": "工程图纸、CAD数据等"},
    {"id": 2, "name": "工程变更文件", "chinese": "工程变更文件", "required_levels": [1, 2, 3, 4, 5], "description": "任何相关工程变更的文件"},
    {"id": 3, "name": "工程批准", "chinese": "工程批准", "required_levels": [1, 2, 3, 4, 5], "description": "设计验证和工程批准证明"},
    {"id": 4, "name": "DFMEA", "chinese": "设计失效模式与影响分析", "required_levels": [1, 2, 3, 4, 5], "description": "设计FMEA（如果供应商负责设计）"},
    {"id": 5, "name": "过程流程图", "chinese": "过程流程图", "required_levels": [1, 2, 3, 4, 5], "description": "生产工艺流程图"},
    {"id": 6, "name": "PFMEA", "chinese": "过程失效模式与影响分析", "required_levels": [1, 2, 3, 4, 5], "description": "过程FMEA"},
    {"id": 7, "name": "过程能力", "chinese": "过程能力", "required_levels": [1, 2, 3, 4, 5], "description": "控制计划"},
    {"id": 8, "name": "初始过程能力研究", "chinese": "初始过程能力研究", "required_levels": [1, 2, 3, 4, 5], "description": "Ppk/Cpk研究数据"},
    {"id": 9, "name": "测量系统分析", "chinese": "测量系统分析", "required_levels": [1, 2, 3, 4, 5], "description": "MSA分析（GR&R等）"},
    {"id": 10, "name": "实验室", "chinese": "实验室要求", "required_levels": [1, 2, 3, 4, 5], "description": "实验室能力声明或认可证书"},
    {"id": 11, "name": "外观批准报告", "chinese": "外观批准报告", "required_levels": [1, 2, 3, 4, 5], "description": "仅适用于有外观要求的零件"},
    {"id": 12, "name": "生产件样品", "chinese": "生产件样品", "required_levels": [1, 2, 3, 4, 5], "description": "代表性样品"},
    {"id": 13, "name": "标准样品", "chinese": "标准样品", "required_levels": [1, 2, 3, 4, 5], "description": "保留的标准样品"},
    {"id": 14, "name": "检查辅具", "chinese": "检查辅具", "required_levels": [1, 2, 3, 4, 5], "description": "检具、夹具等"},
    {"id": 15, "name": "客户特殊要求", "chinese": "客户特殊要求", "required_levels": [1, 2, 3, 4, 5], "description": "客户特定要求满足情况"},
    {"id": 16, "name": "零件提交保证书", "chinese": "零件提交保证书(PSW)", "required_levels": [1, 2, 3, 4, 5], "description": "PSW表格-必须原件签名"},
    {"id": 17, "name": "外观批准报告", "chinese": "外观批准报告", "required_levels": [1, 2, 3, 4, 5], "description": "按客户要求提供"},
    {"id": 18, "name": "补充数据", "chinese": "补充数据/支持数据", "required_levels": [2, 3, 4, 5], "description": "支持性测试数据"}
]

# 提交等级定义
SUBMISSION_LEVELS = {
    1: {"name": "Level 1", "description": "仅提交保证书（PSW）"},
    2: {"name": "Level 2", "description": "提交保证书+样品+有限支持数据"},
    3: {"name": "Level 3", "description": "提交保证书+样品+完整支持数据"},
    4: {"name": "Level 4", "description": "提交保证书+按客户要求"},
    5: {"name": "Level 5", "description": "提交保证书+全部数据+现场审核"}
}


def load_input(input_path: str) -> Dict[str, Any]:
    """加载用户输入的PPAP信息"""
    if input_path.endswith('.json'):
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 假设是JSON字符串
        return json.loads(input_path)


def check_requirement(req: Dict, user_data: Dict, level: int) -> Dict[str, Any]:
    """检查单个PPAP要求"""
    req_id = req["id"]
    req_name = req["name"]
    
    # 检查该要求在当前提交等级下是否必需
    if level not in req["required_levels"]:
        return {
            "id": req_id,
            "name": req_name,
            "chinese": req["chinese"],
            "status": "not_required",
            "message": f"提交等级{level}无需提交此项",
            "compliant": True
        }
    
    # 检查用户数据中是否提供此项信息
    key_variants = [
        f"req_{req_id}",
        f"requirement_{req_id}",
        req_name.lower().replace(" ", "_").replace("-", "_"),
        req["chinese"]
    ]
    
    provided = False
    details = ""
    for key in key_variants:
        if key in user_data:
            provided = True
            details = user_data[key]
            break
    
    # 检查特定要求的特殊条件
    if req_id == 11:  # 外观批准报告 - 仅当有外观要求时必需
        if user_data.get("has_appearance_requirement", False) == False:
            return {
                "id": req_id,
                "name": req_name,
                "chinese": req["chinese"],
                "status": "not_applicable",
                "message": "无外观要求，此项不适用",
                "compliant": True
            }
    
    if not provided:
        return {
            "id": req_id,
            "name": req_name,
            "chinese": req["chinese"],
            "status": "missing",
            "message": f"缺少{req['chinese']}文件或信息",
            "compliant": False
        }
    
    # 检查格式合规性
    compliant = True
    warnings = []
    
    if req_id == 16:  # PSW必须签名
        if not details.get("signed", False):
            compliant = False
            warnings.append("PSW未签名或签名不完整")
        if not details.get("date", ""):
            compliant = False
            warnings.append("PSW缺少日期")
    
    if req_id == 8:  # 初始过程能力研究
        cpk = details.get("cpk", 0)
        if cpk < 1.33:
            warnings.append(f"Cpk={cpk}<1.33，不满足要求（通常需要≥1.33）")
    
    if req_id == 9:  # MSA
        grr = details.get("grr_percent", 0)
        if grr > 30:
            warnings.append(f"GRR={grr}%>30%，测量系统能力不足")
        elif grr > 10:
            warnings.append(f"GRR={grr}%，建议改进")
    
    return {
        "id": req_id,
        "name": req_name,
        "chinese": req["chinese"],
        "status": "provided",
        "message": f"已提供{req['chinese']}" + (f"; 警告: {'; '.join(warnings)}" if warnings else ""),
        "compliant": compliant,
        "warnings": warnings,
        "details": details
    }


def check_ppap_completeness(user_data: Dict, level: int) -> Dict[str, Any]:
    """检查PPAP文件完整性"""
    results = []
    missing_count = 0
    warning_count = 0
    not_required_count = 0
    
    for req in PPAP_REQUIREMENTS:
        result = check_requirement(req, user_data, level)
        results.append(result)
        
        if result["status"] == "missing":
            missing_count += 1
        elif result["status"] == "provided" and result.get("warnings"):
            warning_count += 1
        elif result["status"] in ["not_required", "not_applicable"]:
            not_required_count += 1
    
    # 计算必需项的完成率
    required_results = [r for r in results if r["status"] not in ["not_required", "not_applicable"]]
    completed = len([r for r in required_results if r["status"] == "provided" and r["compliant"]])
    total_required = len(required_results)
    completion_rate = (completed / total_required * 100) if total_required > 0 else 0
    
    return {
        "submission_level": level,
        "level_description": SUBMISSION_LEVELS.get(level, {}).get("description", ""),
        "summary": {
            "total_requirements": len(PPAP_REQUIREMENTS),
            "required": total_required,
            "completed": completed,
            "missing": missing_count,
            "warnings": warning_count,
            "not_applicable": not_required_count,
            "completion_rate": f"{completion_rate:.1f}%"
        },
        "results": results,
        "recommendation": generate_recommendation(missing_count, warning_count, completion_rate)
    }


def generate_recommendation(missing: int, warnings: int, completion_rate: float) -> str:
    """生成建议"""
    if missing > 0:
        return f"请补充缺失的{missing}项文件后重新提交"
    elif warnings > 0:
        return f"文件基本完整，但有{warnings}项需要注意，建议整改后提交"
    elif completion_rate >= 100:
        return "文件完整且格式合规，可以提交"
    else:
        return "请检查并完善文件内容"


def main():
    parser = argparse.ArgumentParser(description="PPAP文件完整性检查工具")
    parser.add_argument("--input", "-i", required=True, help="JSON文件路径或JSON字符串")
    parser.add_argument("--level", "-l", type=int, default=3, choices=[1, 2, 3, 4, 5], help="提交等级(1-5)")
    parser.add_argument("--output", "-o", help="输出文件路径(可选)")
    parser.add_argument("--format", "-f", choices=["json", "text"], default="json", help="输出格式")
    
    args = parser.parse_args()
    
    try:
        # 加载输入数据
        user_data = load_input(args.input)
        
        # 执行检查
        result = check_ppap_completeness(user_data, args.level)
        
        # 输出结果
        if args.format == "json":
            output = json.dumps(result, ensure_ascii=False, indent=2)
        else:
            # 文本格式输出
            lines = [
                f"=== PPAP文件检查报告 ===",
                f"提交等级: Level {result['submission_level']} - {result['level_description']}",
                f"",
                f"【汇总】",
                f"总要求项: {result['summary']['total_requirements']}",
                f"必需项: {result['summary']['required']}",
                f"已完成: {result['summary']['completed']}",
                f"缺失: {result['summary']['missing']}",
                f"警告: {result['summary']['warnings']}",
                f"不适用: {result['summary']['not_applicable']}",
                f"完成率: {result['summary']['completion_rate']}",
                f"",
                f"【详细结果】"
            ]
            for r in result["results"]:
                status_icon = {"provided": "✓", "missing": "✗", "not_required": "-", "not_applicable": "○"}.get(r["status"], "?")
                lines.append(f"{status_icon} [{r['id']:02d}] {r['chinese']}: {r['message']}")
                if r.get("warnings"):
                    for w in r["warnings"]:
                        lines.append(f"    ⚠ {w}")
            
            lines.extend([
                f"",
                f"【建议】: {result['recommendation']}"
            ])
            output = "\n".join(lines)
        
        # 输出
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"检查报告已保存至: {args.output}")
        else:
            print(output)
            
    except FileNotFoundError:
        print("错误: 输入文件不存在", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("错误: JSON格式解析失败", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
