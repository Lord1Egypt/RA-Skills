#!/usr/bin/env python3
"""
解析Cadence Skill API Finder HTML文件，提取所有API数据
"""

import re
import json
from pathlib import Path

def parse_html_file(html_path):
    """解析HTML文件，提取所有API数据"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取functionData部分
    match = re.search(r'const functionData = ({.*?});', content, re.DOTALL)
    if not match:
        print("无法找到functionData")
        return None
    
    data_str = match.group(1)
    
    # 解析JSON数据
    try:
        function_data = json.loads(data_str)
        return function_data
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None

def convert_to_standard_format(functions_by_letter):
    """转换为标准的API数据库格式"""
    standard_db = {
        "metadata": {
            "version": "IC213",
            "description": "Cadence Virtuoso IC213 官方Skill API数据库",
            "last_updated": "2026-03-13",
            "total_functions": 0
        },
        "categories": {}
    }
    
    total = 0
    function_index = {}
    
    for letter, functions in functions_by_letter.items():
        for func in functions:
            func_name = func.get("funcName", func.get("name", ""))
            if not func_name:
                continue
                
            # 分类函数（按前缀）
            category = "其他函数"
            if func_name.startswith("db"):
                category = "数据库操作"
            elif func_name.startswith("le"):
                category = "版图编辑"
            elif func_name.startswith("ge"):
                category = "图形界面"
            elif func_name.startswith("sch"):
                category = "原理图编辑"
            elif func_name.startswith("hi"):
                category = "用户界面"
            elif func_name.startswith("axl"):
                category = "扩展接口"
            elif func_name.startswith("pc"):
                category = "工艺相关"
            elif func_name.startswith("tech"):
                category = "工艺技术"
            elif func_name.startswith("parse"):
                category = "解析工具"
            elif func_name.startswith("lm"):
                category = "许可管理"
            elif func_name.startswith("env"):
                category = "环境变量"
            elif func_name.startswith("load") or func_name.startswith("save"):
                category = "文件操作"
            elif func_name.startswith("print") or func_name.startswith("format"):
                category = "输出格式化"
            elif func_name.startswith("str"):
                category = "字符串操作"
            elif func_name.startswith("list") or func_name.startswith("cons") or func_name.startswith("car") or func_name.startswith("cdr"):
                category = "列表操作"
            elif func_name.startswith("math") or func_name in ["abs", "min", "max", "sqrt", "sin", "cos", "tan"]:
                category = "数学运算"
            elif func_name.startswith("abe"):
                category = "布尔运算引擎"
            elif func_name.startswith("abs"):
                category = "抽象生成器"
            elif func_name.startswith("aaxl") or func_name.startswith("aa"):
                category = "高级分析"
            
            # 创建分类
            if category not in standard_db["categories"]:
                standard_db["categories"][category] = {}
            
            # 转换为标准格式
            standard_func = {
                "name": func_name,
                "description": func.get("description", "").strip(),
                "syntax": func.get("synx", "").strip(),
                "parameters": [],
                "arguments": func.get("arguments", "").strip(),
                "return_type": func.get("valueReturn", "").strip(),
                "example": func.get("example", "").strip(),
                "related": func.get("related", "").strip(),
                "reference": func.get("ref", "").strip()
            }
            
            # 解析参数
            args_str = func.get("arguments", "").strip()
            if args_str and args_str != "None":
                # 简单按行分割参数
                lines = [line.strip() for line in args_str.split('\n') if line.strip()]
                for line in lines:
                    if line and not line.startswith((' ', '\t', '■', '•')):
                        # 可能是参数名
                        param_name = line.split()[0] if line.split() else line
                        standard_func["parameters"].append({
                            "name": param_name,
                            "type": "any",
                            "required": True,
                            "description": line
                        })
            
            standard_db["categories"][category][func_name] = standard_func
            function_index[func_name] = standard_func
            total += 1
    
    standard_db["metadata"]["total_functions"] = total
    standard_db["function_index"] = function_index
    
    return standard_db

def main():
    input_path = Path("/root/.openclaw/qqbot/downloads/CadenceSkillAPIFinder_1773394844827.html")
    output_path = Path(__file__).parent / "skill_api_database_full.json"
    
    print(f"开始解析 {input_path}...")
    function_data = parse_html_file(input_path)
    
    if not function_data:
        print("解析失败")
        return
    
    functions_by_letter = function_data.get("functionsByLetter", {})
    print(f"找到 {len(functions_by_letter)} 个字母分类")
    
    # 统计函数总数
    total = sum(len(funcs) for funcs in functions_by_letter.values())
    print(f"总函数数: {total}")
    
    # 转换为标准格式
    standard_db = convert_to_standard_format(functions_by_letter)
    
    # 保存到文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(standard_db, f, ensure_ascii=False, indent=2)
    
    print(f"转换完成，已保存到 {output_path}")
    print(f"分类统计:")
    for category, funcs in sorted(standard_db["categories"].items()):
        print(f"  {category}: {len(funcs)} 个函数")

if __name__ == "__main__":
    main()
