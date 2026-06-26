#!/usr/bin/env python3
"""
SQL Query Explain / SQL解释器
支持: EXPLAIN解析 | 自然语言转SQL | SQL格式化 | 语法检查
"""

import sqlparse
from sqlparse.sql import Statement, Token
from sqlparse.tokens import Keyword, DML, DDL, Name
import re
import sys
import json
from typing import Optional


def format_sql(sql: str) -> str:
    """格式化 SQL"""
    formatted = sqlparse.format(
        sql,
        keyword_case='upper',
        indent_width=2,
        comma_first=False,
        reindent=True,
        indent_columns_after=True
    )
    return formatted


def check_syntax(sql: str) -> dict:
    """检查 SQL 语法"""
    errors = []
    try:
        parsed = sqlparse.parse(sql)
        if not parsed:
            errors.append("无法解析 SQL，请检查语法")
        else:
            for stmt in parsed:
                # 检查是否有有效 token
                tokens = [t for t in stmt.flatten() if not t.is_whitespace]
                if not tokens:
                    errors.append(f"解析异常: {stmt}")
    except Exception as e:
        errors.append(f"语法错误: {str(e)}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "statement_count": len(parsed) if sql.strip() else 0
    }


def extract_tables(sql: str) -> list:
    """提取 SQL 中的表名 (使用正则)"""
    tables = []
    # 匹配 FROM/JOIN 后的表名
    patterns = [
        r'(?:FROM|JOIN|INTO|UPDATE)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        r'FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:WHERE|JOIN|ORDER|GROUP|LIMIT|;|$)',
    ]
    for p in patterns:
        matches = re.findall(p, sql, re.IGNORECASE)
        tables.extend(matches)
    return list(set(tables))


def analyze_sql_structure(sql: str) -> dict:
    """分析 SQL 语句结构"""
    parsed = sqlparse.parse(sql)
    if not parsed:
        return {"type": "UNKNOWN", "tables": [], "complexity": "UNKNOWN"}
    
    stmt = parsed[0]
    tokens = [t for t in stmt.flatten() if not t.is_whitespace]
    
    stmt_type = "UNKNOWN"
    if tokens:
        first = tokens[0]
        if first.ttype in (DML, DDL):
            stmt_type = first.value.upper()
        elif first.ttype is Keyword:
            stmt_type = first.value.upper()
    
    tables = extract_tables(sql)
    
    # 复杂度评估
    sql_upper = sql.upper()
    complexity_factors = []
    if 'JOIN' in sql_upper:
        complexity_factors.append('+JOIN')
    if sql_upper.count('(') >= 1:
        complexity_factors.append('+子查询')
    if 'GROUP BY' in sql_upper:
        complexity_factors.append('+GROUP BY')
    if 'HAVING' in sql_upper:
        complexity_factors.append('+HAVING')
    if 'ORDER BY' in sql_upper:
        complexity_factors.append('+ORDER BY')
    if 'LIMIT' in sql_upper:
        complexity_factors.append('+LIMIT')
    if len(tokens) > 50:
        complexity_factors.append('+长语句')
    if ' OR ' in sql_upper or ' OR\n' in sql:
        complexity_factors.append('+OR条件')
    
    complexity = 'SIMPLE'
    if len(complexity_factors) >= 3:
        complexity = 'COMPLEX'
    elif len(complexity_factors) >= 1:
        complexity = 'MODERATE'
    
    return {
        "type": stmt_type,
        "tables": tables,
        "complexity": complexity,
        "complexity_factors": complexity_factors,
        "token_count": len(tokens)
    }


def explain_sql(explain_output: str, db_type: str = 'POSTGRESQL') -> str:
    """解析 EXPLAIN 输出并给出分析报告"""
    if not explain_output.strip():
        return "❌ 无效的 EXPLAIN 输出"
    
    total_cost = None
    estimated_rows = None
    scan_type = "Unknown"
    concerns = []
    suggestions = []
    
    # 提取成本 (PostgreSQL format: cost=123.45..678.90)
    cost_match = re.search(r'cost=([\d.]+)\.\.([\d.]+)', explain_output, re.IGNORECASE)
    if cost_match:
        total_cost = float(cost_match.group(2))
    
    # 提取行数
    rows_match = re.search(r'rows=(\d+)', explain_output, re.IGNORECASE)
    if rows_match:
        estimated_rows = int(rows_match.group(1))
    
    # 扫描类型分析
    explain_lower = explain_output.lower()
    if 'seq scan' in explain_lower:
        scan_type = 'Seq Scan (全表扫描)'
        concerns.append('🔴 使用全表扫描，数据量大时性能差')
        suggestions.append('💡 考虑在 WHERE 条件列上建立索引')
    elif 'index only scan' in explain_lower:
        scan_type = 'Index Only Scan (仅索引扫描)'
        suggestions.append('✅ 使用了覆盖索引，无需回表，最佳性能')
    elif 'index scan' in explain_lower:
        scan_type = 'Index Scan (索引扫描)'
        suggestions.append('✅ 使用了索引扫描，性能良好')
    elif 'bitmap heap scan' in explain_lower:
        scan_type = 'Bitmap Heap Scan (位图堆扫描)'
        suggestions.append('⚠️ 位图扫描，适合中等数据量')
    elif 'ctescan' in explain_lower:
        scan_type = 'CTE Scan (CTE扫描)'
        suggestions.append('💡 使用了 CTE，注意临时结果集大小')
    
    # 连接类型
    if 'hash join' in explain_lower:
        concerns.append('🟡 Hash Join：需构建哈希表，适合大表连接')
        suggestions.append('💡 确保连接列有索引，且哈希表能放入内存')
    elif 'nested loop' in explain_lower:
        concerns.append('🟡 Nested Loop：外层行数多时性能差')
        suggestions.append('💡 确保内表有良好索引，减少内层循环次数')
    elif 'merge join' in explain_lower:
        concerns.append('🟡 Merge Join：需排序，适合已排序数据')
        suggestions.append('💡 确保连接列有索引或显式排序')
    
    # 成本分析
    if total_cost:
        if total_cost > 10000:
            concerns.append(f'🔴 总成本极高 ({total_cost:.0f})，查询耗时可能很长')
        elif total_cost > 1000:
            concerns.append(f'🟡 总成本较高 ({total_cost:.0f})')
        else:
            suggestions.append(f'✅ 总成本较低 ({total_cost:.0f})')
    
    # 行数分析
    if estimated_rows:
        if estimated_rows > 100000:
            concerns.append(f'🔴 预计返回 {estimated_rows:,} 行，数据量很大')
            suggestions.append('💡 使用 LIMIT 限制返回行数')
        elif estimated_rows > 10000:
            concerns.append(f'🟡 预计返回 {estimated_rows:,} 行')
    
    # 去重建议
    seen = set()
    unique_suggestions = []
    for s in suggestions:
        if s not in seen:
            seen.add(s)
            unique_suggestions.append(s)
    suggestions = unique_suggestions
    
    # 生成报告
    report_lines = []
    report_lines.append("📊 **EXPLAIN 查询计划分析**\n")
    report_lines.append(f"🎯 **总成本**: {total_cost if total_cost else 'N/A'}")
    report_lines.append(f"📦 **预计返回**: {estimated_rows if estimated_rows else 'N/A'} 行\n")
    report_lines.append("🔍 **扫描分析**:")
    report_lines.append(f"  - 扫描类型: {scan_type}")
    report_lines.append(f"  - 数据库: {db_type}\n")
    
    if concerns:
        report_lines.append("⚠️ **性能关注点**:")
        for c in concerns:
            report_lines.append(f"  - {c}")
        report_lines.append("")
    
    if suggestions:
        report_lines.append("💡 **优化建议**:")
        for s in suggestions:
            report_lines.append(f"  - {s}")
    
    return '\n'.join(report_lines).strip()


def nl_to_sql(description: str, db_type: str = 'GENERIC') -> str:
    """自然语言转 SQL"""
    desc_lower = description.lower()
    
    if any(k in desc_lower for k in ['查询', '获取', 'select', '找', '看', '列出']):
        table_match = re.search(r'(?:表|table|数据表)[\s:：]*([a-zA-Z0-9_\u4e00-\u9fa5]+)', description)
        table = table_match.group(1) if table_match else 'your_table'
        
        where_match = re.search(r'(?:条件|where|满足)[\s:：]*(.+?)(?:\s+排序|\s+分组|\s+limit|;|$)', desc_lower)
        where_clause = f" WHERE {where_match.group(1).strip()}" if where_match else ""
        
        order_match = re.search(r'(?:排序|order by)[\s:：]*(.+?)(?:\s+limit|$)', desc_lower)
        order_clause = f" ORDER BY {order_match.group(1).strip()}" if order_match else ""
        
        limit_match = re.search(r'(?:limit|限制|前|取)[\s:：]*(\d+)', desc_lower)
        limit_clause = f" LIMIT {limit_match.group(1)}" if limit_match else " LIMIT 10"
        
        sql = f"SELECT * FROM {table}{where_clause}{order_clause}{limit_clause};"
        return sql
    
    elif any(k in desc_lower for k in ['插入', 'insert', '新增', '添加数据']):
        table_match = re.search(r'(?:表|table|数据表)[\s:：]*([a-zA-Z0-9_\u4e00-\u9fa5]+)', description)
        table = table_match.group(1) if table_match else 'your_table'
        sql = f"INSERT INTO {table} (column1, column2) VALUES ('value1', 'value2');"
        return sql
    
    elif any(k in desc_lower for k in ['更新', 'update', '修改']):
        table_match = re.search(r'(?:表|table|数据表)[\s:：]*([a-zA-Z0-9_\u4e00-\u9fa5]+)', description)
        table = table_match.group(1) if table_match else 'your_table'
        sql = f"UPDATE {table} SET column1 = 'new_value' WHERE condition;"
        return sql
    
    elif any(k in desc_lower for k in ['删除', 'delete', '移除']):
        table_match = re.search(r'(?:表|table|数据表)[\s:：]*([a-zA-Z0-9_\u4e00-\u9fa5]+)', description)
        table = table_match.group(1) if table_match else 'your_table'
        sql = f"DELETE FROM {table} WHERE condition;"
        return sql
    
    else:
        return "-- 无法识别意图，请描述清楚：查询/插入/更新/删除 + 表名 + 条件"


def main():
    if len(sys.argv) < 2:
        print("SQL Explain Tool - 用法:")
        print("  python sql_explain.py explain '<EXPLAIN输出>'")
        print("  python sql_explain.py format '<SQL语句>'")
        print("  python sql_explain.py check '<SQL语句>'")
        print("  python sql_explain.py analyze '<SQL语句>'")
        print("  python sql_explain.py nl2sql '<自然语言描述>'")
        print("  python sql_explain.py help")
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'help':
        print(__doc__)
    elif cmd == 'format' and len(sys.argv) >= 3:
        print(format_sql(sys.argv[2]))
    elif cmd == 'check' and len(sys.argv) >= 3:
        result = check_syntax(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == 'analyze' and len(sys.argv) >= 3:
        result = analyze_sql_structure(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == 'explain' and len(sys.argv) >= 3:
        db_type = sys.argv[3] if len(sys.argv) >= 4 else 'POSTGRESQL'
        print(explain_sql(sys.argv[2], db_type))
    elif cmd == 'nl2sql' and len(sys.argv) >= 3:
        print(nl_to_sql(sys.argv[2]))
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
