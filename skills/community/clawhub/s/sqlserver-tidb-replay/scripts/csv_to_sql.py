#!/usr/bin/env python3
"""
SQL Server 慢查询日志 CSV 标准化转换脚本

问题：SQL Server 慢查询日志导出的 CSV 不是标准 XE 格式
- 包含大量 XE 事件前缀
- SQL 文本被截断或换行
- 变量参数化符号混合格式
- N'' Unicode 前缀

本脚本将原始 CSV 转换为标准 SQL 语句格式
"""

import argparse
import csv
import re
import sys
from pathlib import Path

def clean_statement(sql: str) -> str:
    """清洗 SQL 语句"""
    if not sql:
        return ""
    
    # 去除 XE 事件前缀（常见前缀模式）
    prefixes_to_remove = [
        r"sql_statement_completed\s*:\s*",
        r"sp_statement_completed\s*:\s*",
        r"sql_batch_completed\s*:\s*",
        r"--\s*sql_statement_completed.*?\n",
        r"--\s*sp_statement_completed.*?\n",
    ]
    for prefix in prefixes_to_remove:
        sql = re.sub(prefix, "", sql, flags=re.IGNORECASE)
    
    # 去除 XE 内部前缀符号（如 event_data、sql_text 等标签）
    sql = re.sub(r"^\s*event_data\s*[:=]\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^\s*sql_text\s*[:=]\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^\s*statement\s*[:=]\s*", "", sql, flags=re.IGNORECASE)
    
    # 处理换行符：将 CRLF/LF 统一为空格（保留 SQL 结构）
    sql = sql.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    
    # 合并多余空白
    sql = re.sub(r'\s+', ' ', sql)
    
    # 去除首尾空白
    sql = sql.strip()
    
    # 去除常见尾部垃圾
    sql = re.sub(r'\s*[;#]\s*$', '', sql)
    sql = re.sub(r'\s+--.*$', '', sql)  # 去除行尾注释
    
    # 处理 SQL Server Unicode 字符串前缀 N''
    # 保留前缀用于后续转换识别
    # sql = re.sub(r"N'([^']*)'", r"N'\1'", sql)
    
    # 去除不可见字符
    sql = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', sql)
    
    return sql

def is_valid_sql(sql: str) -> bool:
    """判断是否为有效 SQL"""
    if not sql or len(sql) < 5:
        return False
    sql_upper = sql.strip().upper()
    # 必须包含 SQL 关键词
    keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'TRUNCATE', 'MERGE', 'EXEC', 'WITH']
    return any(sql_upper.startswith(kw) for kw in keywords)

def detect_sql_type(sql: str) -> str:
    """检测 SQL 类型"""
    sql_stripped = sql.strip().upper()
    for keyword in ['SELECT', 'WITH']:
        if sql_stripped.startswith(keyword.upper()):
            return 'select'
    if sql_stripped.startswith('INSERT'):
        return 'insert'
    if sql_stripped.startswith('UPDATE'):
        return 'update'
    if sql_stripped.startswith('DELETE'):
        return 'delete'
    if sql_stripped.startswith('EXEC'):
        return 'exec'
    if sql_stripped.startswith('MERGE'):
        return 'merge'
    return 'other'

def convert_duration(duration_str: str) -> float:
    """转换执行时间为毫秒"""
    try:
        val = float(duration_str)
        # 如果值 > 10000000，大概率是微秒
        if val > 10000000:
            return val / 1000  # 微秒转毫秒
        # 如果值 > 10000，大概率是微秒（>10ms）
        elif val > 10000:
            return val / 1000
        # 否则可能是毫秒
        return val
    except (ValueError, TypeError):
        return 0.0

def normalize_row(row: dict, args) -> dict | None:
    """标准化单行数据"""
    try:
        # 提取 SQL 文本（尝试多个可能的字段名）
        raw_sql = (
            row.get('statement', '') or
            row.get('sql_text', '') or
            row.get('sqltext', '') or
            row.get('text', '') or
            row.get('query', '') or
            row.get('command', '')
        )
        
        # 提取 duration
        raw_duration = (
            row.get('duration', '') or
            row.get('duration_us', '') or
            row.get('total_elapsed_time', '') or
            row.get('cpu_time', '') or
            row.get('ElapsedTime', '') or
            '0'
        )
        duration_ms = convert_duration(raw_duration)
        
        # 过滤阈值
        if args.filter_duration_ms and duration_ms < args.filter_duration_ms:
            return None
        
        # 清洗 SQL
        sql = clean_statement(raw_sql)
        
        # 验证有效性
        if not is_valid_sql(sql):
            return None
        
        # 提取数据库名
        db_name = (
            row.get('database_name', '') or
            row.get('db_name', '') or
            row.get('database', '') or
            row.get('dbname', '') or
            'unknown'
        )
        
        # 提取 session_id
        session_id = (
            row.get('session_id', '') or
            row.get('spid', '') or
            row.get('session_id', '') or
            '0'
        )
        
        # 提取 start_time
        start_time = (
            row.get('start_time', '') or
            row.get('start_time', '') or
            row.get('starttime', '') or
            row.get('timestamp', '') or
            ''
        )
        
        # 检测特殊语法标记
        syntax_flags = []
        sql_upper = sql.upper()
        if 'OUTPUT ' in sql_upper and 'INSERT' in sql_upper:
            syntax_flags.append('output_clause')
        if 'N\'' in sql:
            syntax_flags.append('nchar_prefix')
        if 'OPENJSON' in sql_upper:
            syntax_flags.append('openjson')
        if 'NEXT VALUE FOR' in sql_upper:
            syntax_flags.append('sequence')
        if 'OFFSET ' in sql_upper and 'FETCH ' in sql_upper:
            syntax_flags.append('offset_fetch')
        if 'INTO #' in sql_upper or 'INTO #temp' in sql_upper:
            syntax_flags.append('temp_table_select_into')
        if 'MERGE ' in sql_upper:
            syntax_flags.append('merge_statement')
        if re.search(r'\bTOP\s+\d+', sql_upper):
            syntax_flags.append('top_keyword')
        
        return {
            'sql_text': sql,
            'sql_type': detect_sql_type(sql),
            'duration_ms': round(duration_ms, 2),
            'database_name': db_name.strip(),
            'session_id': str(session_id).strip(),
            'start_time': start_time.strip(),
            'syntax_flags': ','.join(syntax_flags) if syntax_flags else '',
            'original_raw': raw_sql[:500],  # 保存原始片段用于对比
        }
    except Exception as e:
        print(f"[WARN] 处理行失败: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="SQL Server 慢查询日志 CSV 标准化转换工具"
    )
    parser.add_argument("--input", "-i", required=True, help="原始 CSV 文件路径")
    parser.add_argument("--output", "-o", required=True, help="标准 SQL CSV 输出路径")
    parser.add_argument("--normalize", action="store_true", default=True,
                        help="规范化 SQL 格式（默认开启）")
    parser.add_argument("--remove-prefix", action="store_true", default=True,
                        help="去除 XE 事件前缀（默认开启）")
    parser.add_argument("--filter-duration-ms", type=int, default=0,
                        help="过滤最小执行时间（毫秒）")
    
    args = parser.parse_args()
    
    # 读取输入
    print(f"[INFO] 读取原始 CSV: {args.input}")
    with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"[INFO] 总行数: {len(rows)}")
    
    # 处理
    results = []
    skipped = 0
    for i, row in enumerate(rows):
        normalized = normalize_row(row, args)
        if normalized:
            results.append(normalized)
        else:
            skipped += 1
    
    # 输出
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = ['sql_text', 'sql_type', 'duration_ms', 'database_name', 'session_id', 'start_time', 'syntax_flags', 'original_raw']
    
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"")
    print(f"[SUMMARY] 转换完成")
    print(f"  输入总行数:  {len(rows)}")
    print(f"  有效SQL数:   {len(results)}")
    print(f"  跳过行数:    {skipped}")
    print(f"  输出文件:    {args.output}")
    
    # 统计语法标记
    all_flags = {}
    for r in results:
        if r['syntax_flags']:
            for flag in r['syntax_flags'].split(','):
                all_flags[flag] = all_flags.get(flag, 0) + 1
    
    if all_flags:
        print(f"\n[FLAGS] 特殊语法统计:")
        for flag, cnt in sorted(all_flags.items(), key=lambda x: -x[1]):
            print(f"  {flag}: {cnt}")
    
    if len(results) == 0:
        print(f"\n[WARN] 没有有效 SQL 输出，请检查输入文件格式", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
