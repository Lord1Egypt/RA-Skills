#!/usr/bin/env python3
"""yaoyao-memory 用户交互增强模块"""
import sys
import json
from datetime import datetime

# 颜色定义
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def colored(text, color):
    """给文本添加颜色"""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.ENDC}"
    return text

def print_header(text):
    print(colored(f"\n{'='*50}", Colors.HEADER))
    print(colored(f"  {text}", Colors.HEADER))
    print(colored(f"{'='*50}", Colors.HEADER))

def print_success(text):
    print(colored(f"✅ {text}", Colors.GREEN))

def print_error(text):
    print(colored(f"❌ {text}", Colors.RED))

def print_info(text):
    print(colored(f"ℹ️  {text}", Colors.BLUE))

def print_warning(text):
    print(colored(f"⚠️  {text}", Colors.YELLOW))

def print_result(data, pretty=True):
    """格式化输出结果"""
    if pretty:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))

def print_table(headers, rows):
    """打印表格"""
    col_widths = [max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))]
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(colored(header_line, Colors.BOLD))
    print(colored("-" * len(header_line), Colors.BLUE))
    for row in rows:
        print(" | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))))

def print_memory_list(memories):
    """打印记忆列表"""
    if not memories:
        print_info("没有找到记忆")
        return
    print_header("记忆列表")
    headers = ["ID", "标题", "类型", "重要"]
    rows = [[m.get("id", "")[:8], m.get("title", "")[:30], m.get("type", "info")[0].upper(), m.get("importance", "N")[0].upper()] for m in memories]
    print_table(headers, rows)

def print_stats(stats):
    """打印统计信息"""
    print_header("记忆统计")
    print(f"总计: {colored(str(stats.get('total', 0)), Colors.BOLD)} 条记忆\n")
    
    if "by_type" in stats:
        print("按类型:")
        for t, count in stats["by_type"].items():
            print(f"  {t}: {count}")
    
    if "by_importance" in stats:
        print("\n按重要性:")
        for imp, count in stats["by_importance"].items():
            color = Colors.GREEN if imp in ["Critical", "High"] else Colors.ENDC
            print(colored(f"  {imp}: {count}", color))

def print_search_results(query, results):
    """打印搜索结果"""
    print_header(f"搜索结果: {query}")
    if not results:
        print_warning("没有找到匹配的记忆")
        return
    print(f"找到 {colored(str(len(results)), Colors.BOLD)} 条记忆:\n")
    for i, r in enumerate(results, 1):
        title = r.get("title", r.get("s", ""))[:40]
        score = r.get("score", r.get("rerank_score", 0))
        print(f"  {i}. {title}")
        if score:
            print(f"     匹配度: {score:.2f}")

def confirm(prompt):
    """确认提示"""
    try:
        response = input(f"{prompt} [Y/n]: ").strip().lower()
        return response != 'n'
    except:
        return True

def progress_bar(current, total, prefix='', length=30):
    """显示进度条"""
    if total == 0:
        percent = 100
    else:
        percent = int(100 * current / total)
    filled = int(length * current / total) if total > 0 else 0
    bar = '█' * filled + '░' * (length - filled)
    print(f"\r{prefix} |{bar}| {percent}% ", end='', flush=True)
    if current >= total:
        print()

def welcome():
    """欢迎信息"""
    print(colored("""
    ╔═══════════════════════════════════════════╗
    ║   yaoyao-memory 记忆系统 v2.0.6         ║
    ║   你的智能记忆助手                       ║
    ╚═══════════════════════════════════════════╝
    """, Colors.HEADER))
