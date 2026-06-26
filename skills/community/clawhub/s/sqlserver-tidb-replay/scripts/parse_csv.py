#!/usr/bin/env python3
"""
SQL Server XE CSV 解析器
将 Extended Events 导出的 CSV 转换为 sql-replay 兼容的 JSON 中间格式
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# SQL Server 系统语句过滤模式
ADMIN_PATTERNS = [
    r"^\s*--",
    r"^\s*DBCC",
    r"^\s*SET\s+ANSI",
    r"^\s*SET\s+NOCOUNT",
    r"^\s*KILL",
    r"^\s*USE\s+",
    r"sp_reset_connection",
    r"sp_trace_",
    r"sys\.x_",
    r"sys\.sp_",
    r"xp_",
    r"sp_MSforeachtable",
    r"sp_MSforeachdb",
    r"@.*=.*@.*=",
]

# SQL 类型关键词
SQL_TYPE_KEYWORDS = {
    "select": "select",
    "insert": "insert",
    "update": "update",
    "delete": "delete",
    "exec ": "exec",
    "create": "create",
    "alter": "alter",
    "drop": "drop",
    "truncate": "truncate",
    "merge": "merge",
    "with ": "cte",
}

def is_admin_sql(sql: str) -> bool:
    """判断是否为系统/管理员SQL"""
    sql_upper = sql.strip().upper()
    for pattern in ADMIN_PATTERNS:
        if re.search(pattern, sql, re.IGNORECASE):
            return True
    return False

def detect_sql_type(sql: str) -> str:
    """检测SQL类型"""
    sql_stripped = sql.strip().upper()
    # 跳过注释
    if sql_stripped.startswith("--") or sql_stripped.startswith("/*"):
        return "comment"
    for keyword, sql_type in SQL_TYPE_KEYWORDS.items():
        if sql_stripped.startswith(keyword.upper()):
            return sql_type
    return "other"

def normalize_sql(sql: str) -> str:
    """SQL 规范化"""
    # 移除多余空白
    sql = re.sub(r'\s+', ' ', sql)
    sql = sql.strip()
    # 移除前后空白字符
    sql = sql.strip('\r\n\t ')
    # 处理 N'' 前缀（SQL Server Unicode 字符串）
    # 保留，因为 TiDB 需注意字符集差异
    return sql

def is_valid_sql(sql: str) -> bool:
    """判断是否为有效业务SQL"""
    if not sql or len(sql) < 10:
        return False
    # 过滤纯系统调用
    if re.match(r'^\s*(exec|execute)\s+sys?\.', sql, re.IGNORECASE):
        return False
    # 过滤空或极短的语句
    if len(sql.strip()) < 8:
        return False
    return True

def parse_row(row: dict, filter_duration_ms: int = 0) -> dict | None:
    """解析单行CSV数据"""
    try:
        statement = row.get("statement", "").strip()
        
        if not is_valid_sql(statement):
            return None
        
        if is_admin_sql(statement):
            return None
        
        # duration_us 字段
        duration_us_str = row.get("duration_us", "0")
        try:
            duration_us = int(float(duration_us_str))
        except (ValueError, TypeError):
            duration_us = 0
        
        # 按阈值过滤
        if filter_duration_ms > 0 and duration_us < filter_duration_ms * 1000:
            return None
        
        # 数据库名
        database = row.get("database_name", "unknown")
        if not database or database == "0":
            database = "unknown"
        
        # session_id
        session_id = row.get("session_id", "0")
        
        # start_time
        start_time_str = row.get("start_time", "")
        try:
            if start_time_str:
                dt = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
                start_time = dt.isoformat()
            else:
                start_time = datetime.now().isoformat()
        except Exception:
            start_time = datetime.now().isoformat()
        
        # SQL 类型
        sql_type = detect_sql_type(statement)
        
        # 规范化
        statement = normalize_sql(statement)
        
        return {
            "conn_id": str(session_id),
            "start_time": start_time,
            "sql": statement,
            "sql_type": sql_type,
            "duration_us": duration_us,
            "database": database,
            "cpu_us": int(float(row.get("cpu_us", 0) or 0)),
            "logical_reads": int(float(row.get("logical_reads", 0) or 0)),
            "physical_reads": int(float(row.get("physical_reads", 0) or 0)),
            "row_count": int(float(row.get("row_count", 0) or 0)),
        }
    except Exception as e:
        print(f"[WARN] 解析行失败: {e}", file=sys.stderr)
        return None

def load_csv(input_path: str) -> list[dict]:
    """加载CSV文件"""
    rows = []
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def main():
    parser = argparse.ArgumentParser(
        description="解析 SQL Server Extended Events CSV，生成回放 JSON"
    )
    parser.add_argument("--input", "-i", required=True, help="输入 CSV 文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出 JSON 文件路径")
    parser.add_argument(
        "--filter-type", "-t",
        default="all",
        help="过滤SQL类型，逗号分隔，如 select,insert,update,delete（默认 all）"
    )
    parser.add_argument(
        "--filter-duration-ms", "-d",
        type=int,
        default=0,
        help="过滤最小执行时间，毫秒（默认 0，不过滤）"
    )
    parser.add_argument(
        "--remove-admin",
        action="store_true",
        default=True,
        help="移除管理员/SYSTEM SQL（默认开启）"
    )
    parser.add_argument(
        "--lang",
        default="cn",
        choices=["cn", "en"],
        help="输出语言（cn/en）"
    )
    
    args = parser.parse_args()
    
    # 解析过滤类型
    if args.filter_type == "all":
        filter_types = None
    else:
        filter_types = set(args.filter_type.split(","))
    
    # 加载 CSV
    print(f"[INFO] 加载 CSV: {args.input}")
    csv_rows = load_csv(args.input)
    print(f"[INFO] 总行数: {len(csv_rows)}")
    
    # 解析
    results = []
    skipped_admin = 0
    skipped_duration = 0
    skipped_type = 0
    skipped_invalid = 0
    
    for row in csv_rows:
        parsed = parse_row(row, args.filter_duration_ms)
        if not parsed:
            skipped_invalid += 1
            continue
        
        # 类型过滤
        if filter_types and parsed["sql_type"] not in filter_types:
            skipped_type += 1
            continue
        
        results.append(parsed)
    
    # 按 start_time 排序
    results.sort(key=lambda x: x["start_time"])
    
    # 输出
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 统计
    total_input = len(csv_rows)
    total_output = len(results)
    
    print("")
    print(f"[SUMMARY] 解析完成")
    print(f"  输入总行数:  {total_input}")
    print(f"  输出SQL数:   {total_output}")
    print(f"  无效跳过:    {skipped_invalid}")
    print(f"  类型过滤:    {skipped_type}")
    print(f"  管理员跳过:  {skipped_admin}")
    print(f"  时长过滤:    {skipped_duration}")
    print(f"  输出文件:    {args.output}")
    
    if total_output == 0:
        print(f"\n[WARN] 无有效SQL输出，请检查输入文件或过滤参数", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
