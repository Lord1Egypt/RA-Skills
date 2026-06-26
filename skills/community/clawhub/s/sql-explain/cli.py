#!/usr/bin/env python3
"""
sql-explain CLI - keyword 风格入口
提供 sql-explain format/check/analyze/nl2sql 命令
"""

import sys
import os

# 确保同目录的 sql_explain 可导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sql_explain import format_sql, check_syntax, analyze_sql_structure, nl_to_sql, explain_sql


def main():
    if len(sys.argv) < 2:
        print("sql-explain - SQL 解释器 CLI 工具")
        print("")
        print("用法:")
        print("  sql-explain format <SQL>        格式化 SQL")
        print("  sql-explain check <SQL>         检查语法")
        print("  sql-explain analyze <SQL>      分析结构")
        print("  sql-explain nl2sql <描述>       自然语言转 SQL")
        print("  sql-explain explain <输出>     解析 EXPLAIN")
        print("  sql-explain help                显示帮助")
        print("")
        print("示例:")
        print('  sql-explain format "SELECT * FROM users"')
        print('  sql-explain check "SELECT * FROM users"')
        print('  sql-explain analyze "SELECT u.name FROM users u JOIN orders o ON u.id=o.user_id"')
        print('  sql-explain nl2sql "查询所有订单"')
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "help":
        print(__doc__ if __doc__ else "sql-explain - SQL 解释器 CLI 工具")
        print("")
        print("用法:")
        print("  sql-explain format <SQL>        格式化 SQL")
        print("  sql-explain check <SQL>         检查语法")
        print("  sql-explain analyze <SQL>      分析结构")
        print("  sql-explain nl2sql <描述>       自然语言转 SQL")
        print("  sql-explain explain <输出>     解析 EXPLAIN")
        sys.exit(0)

    # 读取 SQL/描述（支持多词参数）
    if len(sys.argv) >= 3:
        # 合并剩余参数为完整字符串
        query = " ".join(sys.argv[2:])
    else:
        print(f"❌ 命令 '{cmd}' 需要参数")
        print(f"   用法: sql-explain {cmd} <SQL或描述>")
        sys.exit(1)

    if cmd == "format":
        result = format_sql(query)
        print(result)

    elif cmd == "check":
        import json
        result = check_syntax(query)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "analyze":
        import json
        result = analyze_sql_structure(query)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "nl2sql":
        result = nl_to_sql(query)
        print(result)

    elif cmd == "explain":
        db_type = sys.argv[3] if len(sys.argv) >= 4 else "POSTGRESQL"
        result = explain_sql(query, db_type)
        print(result)

    else:
        print(f"❌ 未知命令: {cmd}")
        print("   可用命令: format, check, analyze, nl2sql, explain, help")
        sys.exit(1)


if __name__ == "__main__":
    main()
