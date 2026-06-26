#!/usr/bin/env python3
"""
直接从HTML中提取所有函数定义
"""

import re
import json
from pathlib import Path

def extract_functions(html_path):
    """直接提取所有函数对象"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配函数对象模式
    pattern = r'{\s*"funcName":\s*"([^"]+)"(.*?)}'
    matches = re.findall(pattern, content, re.DOTALL)
    
    print(f"找到 {len(matches)} 个函数定义")
    
    functions = {}
    categories = {}
    
    for func_name, func_content in matches:
        # 提取各个字段
        desc_match = re.search(r'"description":\s*"((?:\\"|[^"])*)"', func_content)
        synx_match = re.search(r'"synx":\s*"((?:\\"|[^"])*)"', func_content)
        args_match = re.search(r'"arguments":\s*"((?:\\"|[^"])*)"', func_content)
        ret_match = re.search(r'"valueReturn":\s*"((?:\\"|[^"])*)"', func_content)
        example_match = re.search(r'"example":\s*"((?:\\"|[^"])*)"', func_content)
        ref_match = re.search(r'"ref":\s*"((?:\\"|[^"])*)"', func_content)
        
        func = {
            "name": func_name,
            "description": desc_match.group(1).replace('\\"', '"') if desc_match else "",
            "syntax": synx_match.group(1).replace('\\"', '"') if synx_match else "",
            "arguments": args_match.group(1).replace('\\"', '"') if args_match else "",
            "return_type": ret_match.group(1).replace('\\"', '"') if ret_match else "",
            "example": example_match.group(1).replace('\\"', '"') if example_match else "",
            "reference": ref_match.group(1).replace('\\"', '"') if ref_match else ""
        }
        
        # 分类
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
        elif func_name.startswith("abe"):
            category = "布尔运算引擎"
        elif func_name.startswith("abs"):
            category = "抽象生成器"
        elif func_name.startswith("aa") or func_name.startswith("aaxl"):
            category = "高级分析"
        elif func_name.startswith("str"):
            category = "字符串操作"
        elif func_name.startswith("list") or func_name in ["car", "cdr", "cons", "append", "length", "nth", "member", "assoc"]:
            category = "列表操作"
        elif func_name in ["abs", "min", "max", "sqrt", "sin", "cos", "tan", "exp", "log"]:
            category = "数学运算"
        
        if category not in categories:
            categories[category] = {}
        
        categories[category][func_name] = func
        functions[func_name] = func
    
    # 构建数据库
    db = {
        "metadata": {
            "version": "IC213",
            "description": "Cadence Virtuoso IC213 官方Skill API数据库",
            "last_updated": "2026-03-13",
            "total_functions": len(functions)
        },
        "categories": categories,
        "function_index": functions
    }
    
    return db

def main():
    input_path = Path("/root/.openclaw/qqbot/downloads/CadenceSkillAPIFinder_1773394844827.html")
    output_path = Path(__file__).parent / "skill_api_database_full.json"
    
    print("开始提取函数...")
    db = extract_functions(input_path)
    
    print(f"提取完成，共 {db['metadata']['total_functions']} 个函数")
    
    # 保存
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"已保存到 {output_path}")
    
    # 显示分类统计
    print("\n分类统计:")
    for cat, funcs in sorted(db["categories"].items()):
        print(f"  {cat}: {len(funcs)} 个函数")

if __name__ == "__main__":
    main()
