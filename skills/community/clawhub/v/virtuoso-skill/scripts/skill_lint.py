#!/usr/bin/env python3
"""
Virtuoso Skill代码静态检查工具
功能：检查Skill代码中的API调用是否合法，参数是否正确
基于官方IC213版本10124个API的完整数据库
"""

import json
import re
import argparse
import gzip
from pathlib import Path

# 加载完整API数据库 - 查找多个可能位置
DB_PATHS = [
    Path(__file__).parent.parent / "references" / "skill_api_database_full.json",
    Path(__file__).parent.parent / "references" / "skill_api_database_full.gz.json",
    Path(__file__).parent.parent / "references" / "skill_api_database_full.json.gz",
    Path(__file__).parent / "skill_api_database_full.json",
]

API_DB = None
for db_path in DB_PATHS:
    if db_path.exists():
        if db_path.suffix == '.gz' or 'gz' in db_path.name:
            with gzip.open(db_path, 'rt', encoding="utf-8") as f:
                API_DB = json.load(f)
        else:
            with open(db_path, "r", encoding="utf-8") as f:
                API_DB = json.load(f)
        break

if API_DB is None:
    # 如果找不到完整数据库，回退到精简版
    DB_PATH = Path(__file__).parent.parent / "references" / "skill_api_database.json"
    with open(DB_PATH, "r", encoding="utf-8") as f:
        API_DB = json.load(f)
    print(f"⚠️  未找到完整API数据库，使用精简版 ({len(API_DB['function_index'])} 个函数)")
else:
    print(f"✅ 已加载完整API数据库 ({len(API_DB['function_index'])} 个官方Skill API)")

# 提取所有合法的函数名
VALID_FUNCTIONS = set(API_DB["function_index"].keys())
print(f"已加载 {len(VALID_FUNCTIONS)} 个官方Skill API")

# Skill关键字列表（不是函数）
SKILL_KEYWORDS = {
    "if", "else", "when", "unless", "let", "let*", "lambda", "defun", "procedure",
    "setq", "setf", "quote", "'", "`", ",", "@", "list", "car", "cdr", "cons", "append",
    "length", "nth", "member", "assoc", "strcmp", "strlen", "substring", "strcat",
    "printf", "sprintf", "get_pwd", "set_pwd", "is_file", "is_dir", "read_file",
    "write_file", "t", "nil", "and", "or", "not", "equal", "eq", "ne", "lt", "gt",
    "le", "ge", "+", "-", "*", "/", "%", "sqrt", "sin", "cos", "tan", "exp", "log",
    "max", "min", "abs", "floor", "ceiling", "round", "truncate", "mod", "expt",
    "for", "foreach", "while", "do", "loop", "return", "break", "continue",
    "case", "cond", "progn", "prog1", "prog2", "eval", "apply", "funcall",
    "lambda", "quote", "function", "'", "#'", "`", ",", ",@", "error", "list"
}

# 明确的函数前缀（只有这些前缀的才被认为是函数）
FUNC_PREFIXES = {
    "db", "le", "ge", "sch", "hi", "axl", "pc", "tech", "abe", "abs", 
    "aa", "aaxl", "lm", "env", "parse", "tx", "ciw", "se", "dd", "cdf", 
    "db", "pc", "sch", "le", "ge", "hi", "axl", "ab", "abs", "abe", "aaxl",
    "lm", "env", "parse", "tx", "ciw", "se", "dd", "cdf", "cv", "load",
    "save", "print", "format", "str", "math", "file", "dir", "sys"
}

def extract_function_calls(code):
    """从Skill代码中提取函数调用"""
    function_calls = []
    
    # 先移除注释
    code = re.sub(r';;.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r';.*$', '', code, flags=re.MULTILINE)
    
    # 匹配函数调用模式：(function-name arg1 arg2 ...)
    # 匹配左括号后面紧跟的函数名
    pattern = r'\(([a-zA-Z][a-zA-Z0-9_\-\?\!]*)(\s+[^)]*)?\)'
    matches = re.findall(pattern, code)
    
    for func_name, args_str in matches:
        # 跳过关键字
        if func_name in SKILL_KEYWORDS:
            continue
            
        # 只有在官方数据库中的或者有明确函数前缀的才认为是函数
        is_function = False
        
        # 检查是否在官方API列表中
        if func_name in VALID_FUNCTIONS:
            is_function = True
        else:
            # 检查是否有明确的函数前缀
            for prefix in FUNC_PREFIXES:
                if func_name.startswith(prefix) and len(func_name) > len(prefix):
                    is_function = True
                    break
        
        if not is_function:
            continue  # 不是函数，跳过
            
        # 解析参数
        args = []
        if args_str:
            # 简单分割参数
            args = [arg.strip() for arg in args_str.split() if arg.strip()]
            
        function_calls.append({
            "name": func_name,
            "args": args,
            "arg_count": len(args)
        })
    
    return function_calls

def check_function(func_call):
    """检查函数调用是否合法"""
    func_name = func_call["name"]
    errors = []
    warnings = []
    
    # 检查函数是否存在
    if func_name not in VALID_FUNCTIONS:
        errors.append(f"❌ 未定义的函数调用: {func_name} (不在官方API数据库中)")
        return errors, warnings
    
    # 获取函数定义
    func_def = API_DB["function_index"][func_name]
    
    # 检查参数数量
    syntax = func_def.get("syntax", "")
    if syntax:
        # 统计语法中的参数数量
        lines = [line.strip() for line in syntax.split('\n') if line.strip()]
        param_count = len(lines) - 1  # 第一行是函数名
        if param_count > 0:
            actual_args = func_call["arg_count"]
            if actual_args < param_count:
                errors.append(f"⚠️ 函数 {func_name} 参数不足: 至少需要 {param_count} 个，实际提供 {actual_args} 个")
            elif actual_args > param_count + 5:  # 允许一些可选参数
                warnings.append(f"ℹ️ 函数 {func_name} 参数过多: 通常需要 {param_count} 个，实际提供 {actual_args} 个")
    
    return errors, warnings

def lint_code(code, filename=None):
    """检查Skill代码"""
    errors = []
    warnings = []
    
    # 提取函数调用
    function_calls = extract_function_calls(code)
    
    print(f"\n🔍 分析代码，发现 {len(function_calls)} 个函数调用:")
    
    # 检查每个函数调用
    for func_call in function_calls:
        func_name = func_call["name"]
        print(f"  → {func_name} (参数: {func_call['arg_count']}个)")
        
        func_errors, func_warnings = check_function(func_call)
        errors.extend(func_errors)
        warnings.extend(func_warnings)
    
    # 输出结果
    if filename:
        print(f"\n📄 检查文件: {filename}")
    
    if errors:
        print("\n❌ 发现错误:")
        for error in errors:
            print(f"  {error}")
    else:
        print("\n✅ 所有API调用均为官方定义，没有发现错误!")
    
    if warnings:
        print("\n⚠️ 警告信息:")
        for warning in warnings:
            print(f"  {warning}")
    
    return len(errors) == 0

def lint_file(file_path):
    """检查单个文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        return lint_code(code, str(file_path))
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

def search_function(query):
    """搜索函数信息"""
    results = []
    for func_name in VALID_FUNCTIONS:
        if query.lower() in func_name.lower():
            results.append(func_name)
    
    if not results:
        print(f"🔍 没有找到包含 '{query}' 的函数")
        return
    
    print(f"🔍 找到 {len(results)} 个匹配的函数:\n")
    for func_name in sorted(results):
        func_def = API_DB["function_index"][func_name]
        desc = func_def.get("description", "").strip()
        short_desc = desc[:80] + "..." if len(desc) > 80 else desc
        print(f"• {func_name}")
        if short_desc:
            print(f"  {short_desc}\n")

def show_function_detail(func_name):
    """显示函数详细信息"""
    if func_name not in VALID_FUNCTIONS:
        print(f"❌ 函数 {func_name} 不存在于官方API数据库中")
        return
    
    func_def = API_DB["function_index"][func_name]
    
    print(f"\n📖 {func_name} 函数详情:")
    print("=" * 60)
    
    if func_def.get("syntax"):
        print("\n📝 语法:")
        print(f"```skill\n{func_def['syntax']}\n```")
    
    if func_def.get("description"):
        print("\n📄 描述:")
        print(f"  {func_def['description']}")
    
    if func_def.get("arguments"):
        print("\n📋 参数:")
        args = func_def["arguments"].replace('\\n', '\n').strip()
        for line in args.split('\n'):
            if line.strip():
                print(f"  {line.strip()}")
    
    if func_def.get("return_type"):
        print("\n📤 返回值:")
        ret = func_def["return_type"].replace('\\n', '\n').strip()
        for line in ret.split('\n'):
            if line.strip():
                print(f"  {line.strip()}")
    
    if func_def.get("example"):
        print("\n💡 示例:")
        example = func_def["example"].replace('\\n', '\n').strip()
        print(f"```skill\n{example}\n```")
    
    if func_def.get("reference"):
        print("\n📚 参考:")
        print(f"  {func_def['reference']}")

def main():
    parser = argparse.ArgumentParser(description="Virtuoso Skill代码静态检查工具 (基于官方IC213 API数据库)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="要检查的Skill文件路径")
    group.add_argument("--dir", help="要检查的目录路径（递归检查所有.il/.skill文件）")
    group.add_argument("--code", help="要检查的Skill代码字符串")
    group.add_argument("--search", help="搜索包含指定关键词的函数")
    group.add_argument("--show", help="显示指定函数的详细信息")
    group.add_argument("--stats", action="store_true", help="显示API数据库统计信息")
    group.add_argument("--list-categories", action="store_true", help="列出所有API分类")
    
    args = parser.parse_args()
    
    if args.stats:
        print("📊 API数据库统计:")
        print(f"  总函数数: {API_DB['metadata']['total_functions']}")
        print(f"  版本: {API_DB['metadata']['version']}")
        print(f"  更新时间: {API_DB['metadata']['last_updated']}")
        print("\n分类统计:")
        for cat, funcs in sorted(API_DB["categories"].items()):
            print(f"  {cat}: {len(funcs)} 个函数")
        return
    
    if args.list_categories:
        print("📋 API分类列表:")
        for cat, funcs in sorted(API_DB["categories"].items()):
            print(f"  {cat}: {len(funcs)} 个函数")
        return
    
    if args.search:
        search_function(args.search)
        return
    
    if args.show:
        show_function_detail(args.show)
        return
    
    if args.code:
        success = lint_code(args.code)
        exit(0 if success else 1)
    
    if args.file:
        success = lint_file(Path(args.file))
        exit(0 if success else 1)
    
    if args.dir:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            print(f"❌ 错误: {args.dir} 不是有效的目录")
            exit(1)
        
        # 查找所有.il和.skill文件
        skill_files = list(dir_path.rglob("*.il")) + list(dir_path.rglob("*.skill"))
        
        if not skill_files:
            print("ℹ️ 没有找到Skill文件")
            exit(0)
        
        print(f"📂 找到 {len(skill_files)} 个Skill文件\n")
        
        all_success = True
        for file_path in skill_files:
            print("-" * 60)
            success = lint_file(file_path)
            if not success:
                all_success = False
            print()
        
        print("=" * 60)
        if all_success:
            print("✅ 所有文件检查通过")
            exit(0)
        else:
            print("❌ 部分文件存在错误")
            exit(1)

if __name__ == "__main__":
    main()
