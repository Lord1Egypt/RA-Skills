#!/usr/bin/env python3
"""
SQL 回放结果分析器
读取回放结果 JSON，生成 HTML 兼容性报告（含语法转换对照表）
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

# 语法转换规则定义
SQLSERVER_TO_TIDB_RULES = [
    {
        "pattern": r"(?i)OUTPUT\s+inserted\.(\w+)",
        "tidb_sql": "SELECT LAST_INSERT_ID() AS {col}",
        "description": "OUTPUT inserted.id → SELECT LAST_INSERT_ID()",
        "reason": "TiDB 不支持 OUTPUT clause",
        "category": "output_clause",
        "conversion_type": "output_clause",
    },
    {
        "pattern": r"(?i)OUTPUT\s+deleted\.(\w+)",
        "tidb_sql": "-- OUTPUT deleted 不支持，建议在 WHERE 条件中处理",
        "description": "OUTPUT deleted 语法",
        "reason": "TiDB 不支持 OUTPUT clause",
        "category": "output_clause",
        "conversion_type": "output_clause",
    },
    {
        "pattern": r"(?i)N'([^']*)'",
        "tidb_sql": "CAST('{content}' AS CHAR)",
        "description": "N'Unicode字符串' → CAST() 转换",
        "reason": "TiDB 字符集与 SQL Server 不同，N'' 前缀需显式转换",
        "category": "nchar_prefix",
        "conversion_type": "charset",
    },
    {
        "pattern": r"(?i)OPENJSON\s*\(",
        "tidb_sql": "JSON_EXTRACT(json_col, '$')",
        "description": "OPENJSON → JSON_EXTRACT",
        "reason": "TiDB 不支持 OPENJSON 函数",
        "category": "openjson",
        "conversion_type": "json_function",
    },
    {
        "pattern": r"(?i)NEXT\s+VALUE\s+FOR\s+(\w+)",
        "tidb_sql": "NEXTVAL('{seq}')",
        "description": "NEXT VALUE FOR seq → NEXTVAL(seq)",
        "reason": "TiDB 序列语法不同",
        "category": "sequence",
        "conversion_type": "sequence",
    },
    {
        "pattern": r"(?i)OFFSET\s+(\d+)\s+ROWS\s+FETCH\s+NEXT\s+(\d+)\s+ROWS\s+ONLY",
        "tidb_sql": "LIMIT {limit} OFFSET {offset}",
        "description": "OFFSET...FETCH → LIMIT...OFFSET（顺序相反）",
        "reason": "TiDB LIMIT...OFFSET 顺序与 SQL Server 相反",
        "category": "offset_fetch",
        "conversion_type": "pagination",
    },
    {
        "pattern": r"(?i)SELECT\s+TOP\s+(\d+)\s+(.+)",
        "tidb_sql": "SELECT {rest} LIMIT {top}",
        "description": "SELECT TOP N → SELECT ... LIMIT N",
        "reason": "TiDB 用 LIMIT 替代 TOP",
        "category": "top_keyword",
        "conversion_type": "select_limit",
    },
    {
        "pattern": r"(?i)SELECT\s+(.+)\s+INTO\s+#(\w+)",
        "tidb_sql": "CREATE TEMPORARY TABLE #{table} AS SELECT {cols}",
        "description": "SELECT INTO #temp → CREATE TEMPORARY TABLE",
        "reason": "TiDB 不支持 SELECT INTO 临时表语法",
        "category": "temp_table_select_into",
        "conversion_type": "temp_table",
    },
    {
        "pattern": r"(?i)MERGE\s+INTO\s+(\w+)\s+USING",
        "tidb_sql": "INSERT ... ON DUPLICATE KEY UPDATE",
        "description": "MERGE INTO → INSERT ON DUPLICATE KEY UPDATE (IODU)",
        "reason": "TiDB 不支持 MERGE 语句，需改写为 IODU",
        "category": "merge_statement",
        "conversion_type": "merge",
    },
    {
        "pattern": r"(?i)GETDATE\s*\(\s*\)",
        "tidb_sql": "NOW()",
        "description": "GETDATE() → NOW()",
        "reason": "TiDB 日期函数差异",
        "category": "datetime_function",
        "conversion_type": "function",
    },
    {
        "pattern": r"(?i)DATEADD\s*\(",
        "tidb_sql": "DATE_ADD() 或 INTERVAL",
        "description": "DATEADD() → DATE_ADD/INTERVAL",
        "reason": "TiDB 日期函数差异",
        "category": "datetime_function",
        "conversion_type": "function",
    },
    {
        "pattern": r"(?i)SCOPE_IDENTITY\s*\(\s*\)",
        "tidb_sql": "LAST_INSERT_ID()",
        "description": "SCOPE_IDENTITY() → LAST_INSERT_ID()",
        "reason": "TiDB 自增 ID 获取方式",
        "category": "identity",
        "conversion_type": "identity",
    },
    {
        "pattern": r"(?i)ISNULL\s*\(",
        "tidb_sql": "IFNULL() 或 COALESCE()",
        "description": "ISNULL() → IFNULL()",
        "reason": "TiDB 使用 IFNULL 或 COALESCE",
        "category": "null_function",
        "conversion_type": "function",
    },
    {
        "pattern": r"(?i)CHARINDEX\s*\(",
        "tidb_sql": "LOCATE() 或 INSTR()",
        "description": "CHARINDEX() → LOCATE()",
        "reason": "TiDB 字符串函数差异",
        "category": "string_function",
        "conversion_type": "function",
    },
    {
        "pattern": r"(?i)LEN\s*\(",
        "tidb_sql": "CHAR_LENGTH() 或 LENGTH()",
        "description": "LEN() → CHAR_LENGTH()（区分字符长度/字节长度）",
        "reason": "TiDB 字符串函数差异",
        "category": "string_function",
        "conversion_type": "function",
    },
]

def apply_conversion(sql: str) -> tuple[str, list[dict]]:
    """对 SQL 应用转换规则，返回 (转换后SQL, 转换记录列表)"""
    conversions = []
    result_sql = sql
    
    for rule in SQLSERVER_TO_TIDB_RULES:
        import re
        matches = list(re.finditer(rule["pattern"], result_sql))
        if matches:
            for match in matches:
                conv_record = {
                    "description": rule["description"],
                    "reason": rule["reason"],
                    "category": rule["category"],
                    "matched_text": match.group(0),
                    "tidb_suggestion": rule["tidb_sql"],
                }
                conversions.append(conv_record)
    
    # 如果有转换，生成转换后的 SQL（仅做示例性替换）
    if conversions:
        result_sql = apply_sample_conversion(sql, conversions)
    
    return result_sql, conversions

def apply_sample_conversion(sql: str, conversions: list) -> str:
    """生成转换后的 SQL 示例（基于第一条匹配规则）"""
    if not conversions:
        return sql
    
    first_conv = conversions[0]
    category = first_conv["category"]
    
    # 针对性替换
    sql_upper = sql.upper()
    
    if category == "output_clause":
        # 处理 OUTPUT inserted.id
        import re
        m = re.search(r"(?i)OUTPUT\s+inserted\.(\w+)", sql)
        if m:
            col = m.group(1)
            # 找到 INSERT 语句，在 VALUES 后添加 SELECT LAST_INSERT_ID()
            parts = sql.rsplit("VALUES", 1)
            if len(parts) == 2:
                return f"{parts[0]}VALUES{parts[1]};\nSELECT LAST_INSERT_ID() AS {col};"
        return sql + "\n-- 需添加: SELECT LAST_INSERT_ID() 获取自增ID"
    
    elif category == "nchar_prefix":
        # N'' 字符串
        import re
        result = re.sub(r"N'([^']*)'", r"CAST('\\1' AS CHAR)", sql)
        return result
    
    elif category == "offset_fetch":
        import re
        m = re.search(r"(?i)OFFSET\s+(\d+)\s+ROWS\s+FETCH\s+NEXT\s+(\d+)\s+ROWS\s+ONLY", sql)
        if m:
            offset = m.group(1)
            limit = m.group(2)
            # 找到 LIMIT 位置，替换
            result = re.sub(r"(?i)OFFSET\s+\d+\s+ROWS\s+FETCH\s+NEXT\s+\d+\s+ROWS\s+ONLY", 
                           f"LIMIT {limit} OFFSET {offset}", sql)
            return result
        return sql
    
    elif category == "top_keyword":
        import re
        m = re.search(r"(?i)SELECT\s+TOP\s+(\d+)\s+(.+)", sql)
        if m:
            top = m.group(1)
            rest = m.group(2)
            result = re.sub(r"(?i)SELECT\s+TOP\s+\d+\s+", "SELECT ", sql)
            result = result + f"\n-- 改写: SELECT {rest.strip()} LIMIT {top};"
            return result
        return sql
    
    elif category == "openjson":
        return sql + "\n-- 改写: 使用 JSON_EXTRACT() 替代 OPENJSON()"
    
    elif category == "sequence":
        import re
        m = re.search(r"(?i)NEXT\s+VALUE\s+FOR\s+(\w+)", sql)
        if m:
            seq = m.group(1)
            return re.sub(r"(?i)NEXT\s+VALUE\s+FOR\s+\w+", f"NEXTVAL('{seq}')", sql)
        return sql
    
    elif category == "merge_statement":
        return "-- 需改写为 INSERT ... ON DUPLICATE KEY UPDATE\n" + sql
    
    elif category == "temp_table_select_into":
        return "-- 需改写: CREATE TEMPORARY TABLE ... AS SELECT ...\n" + sql
    
    return sql

def classify_error(error_code: Optional[int], error_msg: str) -> tuple[str, str]:
    """分类错误类型"""
    if not error_code:
        return ("unknown", "未知错误")
    
    if error_code == 1064:
        return ("syntax", "语法不兼容（TiDB 不支持的 SQL 语法）")
    elif error_code == 1146:
        return ("missing_table", "表不存在")
    elif error_code == 1054:
        return ("unknown_column", "列名不存在")
    elif error_code == 1366:
        return ("charset", "字符集/编码不兼容")
    elif error_code == 1406:
        return ("data_too_long", "字段长度不足")
    elif error_code == 1048:
        return ("null_not_allowed", "字段不允许 NULL")
    elif error_code == 1213:
        return ("deadlock", "死锁（并发回放正常现象）")
    elif error_code == 1205:
        return ("lock_wait", "锁等待超时")
    elif error_code in (2013, 2006, 2003):
        return ("connection", "连接问题")
    elif error_code in (300, 301, 302, 303, 304):
        return ("data_truncation", "数据截断")
    elif 1000 <= error_code < 2000:
        return ("ddl_error", "DDL 相关错误")
    elif 4000 <= error_code < 5000:
        return ("tidb_internal", "TiDB 内部错误")
    else:
        msg_lower = error_msg.lower()
        if "output clause" in msg_lower:
            return ("output_clause", "OUTPUT clause 不兼容")
        elif "openjson" in msg_lower:
            return ("json_function", "JSON 函数不兼容")
        elif "char" in msg_lower and "charset" in msg_lower:
            return ("charset", "字符集不兼容")
        elif "nchar" in msg_lower or "nvarchar" in msg_lower:
            return ("nchar_nvarchar", "NCHAR/NVARCHAR 类型差异")
        elif "sequence" in msg_lower:
            return ("sequence", "序列（SEQUENCE）不支持")
        elif "identity" in msg_lower:
            return ("identity", "IDENTITY 列特性差异")
        elif "cursor" in msg_lower:
            return ("cursor", "游标语法不兼容")
        elif "temp table" in msg_lower:
            return ("temp_table", "临时表语法差异")
        elif "table variable" in msg_lower:
            return ("table_variable", "表变量语法差异")
        elif "merge" in msg_lower and "into" in msg_lower:
            return ("merge_statement", "MERGE 语句差异")
        elif "top" in msg_lower:
            return ("top_keyword", "TOP 关键字差异")
        elif "offset" in msg_lower or "fetch" in msg_lower:
            return ("offset_fetch", "OFFSET/FETCH 语法差异")
        else:
            return ("other", f"其他错误（code={error_code}）")

def load_summary(summary_path: Path) -> dict:
    """加载汇总文件"""
    with open(summary_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_all_results(results_dir: Path, task_name: str) -> list[dict]:
    """加载所有 conn_* JSON 结果文件"""
    results = []
    for f in results_dir.glob(f"{task_name}_conn_*.json"):
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            results.extend(data)
    return results

def generate_html_report(
    summary: dict,
    results: list[dict],
    output_path: str,
    source_db: str,
    target_db: str,
) -> str:
    """生成 HTML 报告"""
    
    total = summary["total_sqls"]
    success = summary["success"]
    errors = summary["errors"]
    compat_rate = summary["compatibility_rate"]
    
    sql_types_stats = summary.get("sql_types", {})
    
    error_classification = defaultdict(list)
    error_sqls = [r for r in results if r.get("error")]
    
    # 对错误 SQL 生成语法转换
    conversion_records = []
    for r in error_sqls:
        err_code = r.get("error_code")
        err_msg = r.get("error", "")
        sql = r.get("sql", "")
        category, desc = classify_error(err_code, err_msg)
        
        # 应用转换规则
        converted_sql, conversions = apply_conversion(sql)
        
        conv_record = {
            "sql": sql[:300] if len(sql) > 300 else sql,
            "converted_sql": converted_sql[:300] if len(converted_sql) > 300 else converted_sql,
            "error": err_msg[:100],
            "error_code": err_code,
            "category": category,
            "description": desc,
            "conversions": conversions,
        }
        error_classification[category].append(conv_record)
        
        if conversions:
            conversion_records.append(conv_record)
    
    slow_sqls = sorted(results, key=lambda x: -x.get("replay_duration_us", 0))[:10]
    
    # 性能对比数据（如果有原 duration 数据）
    perf_data = []
    for r in results:
        orig_dur = r.get("duration_us", 0)
        replay_dur = r.get("replay_duration_us", 0)
        if orig_dur > 0 and replay_dur > 0:
            perf_data.append({
                "sql": r.get("sql", "")[:100],
                "sqlserver_ms": round(orig_dur / 1000, 2),
                "tidb_ms": round(replay_dur / 1000, 2),
                "speedup": round(orig_dur / replay_dur, 2) if replay_dur > 0 else 0,
            })
    
    avg_speedup = sum(p["speedup"] for p in perf_data) / len(perf_data) if perf_data else 0
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>SQL 兼容性评估报告</title>
<style>
    body {{ font-family: -apple-system, "Microsoft YaHei", sans-serif; margin: 40px; background: #f5f5f5; }}
    .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }}
    h1 {{ color: #1a1a2e; border-bottom: 3px solid #0066cc; padding-bottom: 16px; }}
    h2 {{ color: #2d3436; margin-top: 40px; border-left: 4px solid #0066cc; padding-left: 12px; }}
    h3 {{ color: #2d3436; margin-top: 24px; }}
    .meta {{ color: #636e72; margin-bottom: 30px; }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
    .summary-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 24px; border-radius: 12px; text-align: center; }}
    .summary-card.green {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }}
    .summary-card.red {{ background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }}
    .summary-card.orange {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
    .summary-card .number {{ font-size: 36px; font-weight: bold; }}
    .summary-card .label {{ font-size: 14px; opacity: 0.9; margin-top: 8px; }}
    .compat-rate {{ font-size: 72px; font-weight: bold; color: #11998e; text-align: center; margin: 40px 0; }}
    .compat-rate.low {{ color: #eb3349; }}
    .compat-rate.medium {{ color: #f093fb; }}
    .section {{ margin: 30px 0; }}
    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
    th {{ background: #0066cc; color: white; padding: 12px; text-align: left; }}
    td {{ padding: 12px; border-bottom: 1px solid #e0e0e0; }}
    tr:hover {{ background: #f8f9fa; }}
    .error-tag {{ display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
    .error-tag.syntax {{ background: #ff6b6b; color: white; }}
    .error-tag.output_clause {{ background: #ffa502; color: white; }}
    .error-tag.missing_table {{ background: #ffa502; color: white; }}
    .error-tag.charset {{ background: #7bed9f; color: #2d3436; }}
    .error-tag.other {{ background: #dfe6e9; color: #2d3436; }}
    .sql-block {{ font-family: "Consolas", "Monaco", monospace; background: #f8f9fa; padding: 12px; border-radius: 6px; font-size: 13px; word-break: break-all; white-space: pre-wrap; margin: 8px 0; }}
    .sql-block.before {{ background: #fff3cd; border-left: 4px solid #ffc107; }}
    .sql-block.after {{ background: #d4edda; border-left: 4px solid #28a745; }}
    .risk-high {{ color: #eb3349; font-weight: bold; }}
    .risk-medium {{ color: #f093fb; font-weight: bold; }}
    .risk-low {{ color: #11998e; font-weight: bold; }}
    .footer {{ margin-top: 40px; text-align: center; color: #b2bec3; font-size: 12px; }}
    .conversion-table {{ width: 100%; border: 1px solid #dee2e6; border-radius: 8px; margin: 16px 0; }}
    .conversion-header {{ background: #343a40; color: white; padding: 12px 16px; font-weight: bold; }}
    .conversion-row {{ display: grid; grid-template-columns: 1fr; gap: 0; border-bottom: 1px solid #dee2e6; }}
    .conversion-row:last-child {{ border-bottom: none; }}
    .conv-section {{ padding: 12px 16px; border-bottom: 1px solid #dee2e6; }}
    .conv-section:last-child {{ border-bottom: none; }}
    .conv-label {{ font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 4px; }}
    .conv-value {{ color: #212529; }}
    .conv-arrow {{ text-align: center; padding: 8px; color: #0066cc; font-size: 20px; }}
    .perf-badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; }}
    .perf-badge.fast {{ background: #d4edda; color: #155724; }}
    .perf-badge.slow {{ background: #f8d7da; color: #721c24; }}
</style>
</head>
<body>
<div class="container">
    <h1>SQL 兼容性评估报告</h1>
    <div class="meta">
        <p>源数据库：<strong>{source_db}</strong></p>
        <p>目标数据库：<strong>{target_db}</strong></p>
        <p>回放耗时：{summary.get('elapsed_seconds', 'N/A')} 秒</p>
        <p>回放任务：{summary.get('task_name', 'N/A')}</p>
    </div>

    <div class="summary-grid">
        <div class="summary-card">
            <div class="number">{total}</div>
            <div class="label">总 SQL 数</div>
        </div>
        <div class="summary-card green">
            <div class="number">{success}</div>
            <div class="label">成功</div>
        </div>
        <div class="summary-card red">
            <div class="number">{errors}</div>
            <div class="label">失败</div>
        </div>
        <div class="summary-card orange">
            <div class="number">{len(conversion_records)}</div>
            <div class="label">需语法转换</div>
        </div>
    </div>

    <div class="compat-rate {"low" if float(compat_rate.rstrip("%")) < 90 else "medium" if float(compat_rate.rstrip("%")) < 98 else ""}">
        {compat_rate}
    </div>
    <p style="text-align:center; color:#636e72; font-size: 18px;">兼容性</p>
"""

    # 性能对比
    if perf_data:
        html += """
    <h2>一、性能对比分析</h2>
    <p>成功回放的 SQL 与 SQL Server 原生执行时间对比：</p>
    <table>
        <tr><th>SQL（截断）</th><th>SQL Server (ms)</th><th>TiDB (ms)</th><th>加速比</th></tr>
"""
        for p in perf_data[:20]:
            badge = f'<span class="perf-badge fast">↑ {p["speedup"]}x</span>' if p["speedup"] > 1 else f'<span class="perf-badge slow">↓ {p["speedup"]}x</span>'
            html += f"""        <tr>
            <td>{p['sql'][:60]}...</td>
            <td>{p['sqlserver_ms']}</td>
            <td>{p['tidb_ms']}</td>
            <td>{badge}</td>
        </tr>
"""
        html += f"""    </table>
    <p><strong>平均加速比：{avg_speedup:.2f}x</strong>（>1 表示 TiDB 更快）</p>
"""

    # SQL 类型统计
    if sql_types_stats:
        html += """
    <h2>二、按 SQL 类型统计</h2>
    <table>
        <tr><th>SQL 类型</th><th>总数</th><th>错误数</th><th>通过率</th></tr>
"""
        for sql_type, stat in sorted(sql_types_stats.items()):
            t = stat["total"]
            e = stat["errors"]
            rate = f"{(t-e)/t*100:.1f}%" if t > 0 else "N/A"
            rate_val = float(rate.rstrip("%"))
            risk_cls = "risk-high" if rate_val < 90 else "risk-medium" if rate_val < 98 else "risk-low"
            html += f"""        <tr>
            <td>{sql_type}</td>
            <td>{t}</td>
            <td>{e}</td>
            <td class="{risk_cls}">{rate}</td>
        </tr>
"""
        html += """    </table>
"""

    # 错误分布
    if error_classification:
        html += """
    <h2>三、错误分布</h2>
    <table>
        <tr><th>错误类型</th><th>数量</th><th>说明</th></tr>
"""
        for category, items in sorted(error_classification.items(), key=lambda x: -len(x[1])):
            desc = items[0]["description"] if items else ""
            html += f"""        <tr>
            <td><span class="error-tag {category}">{category}</span></td>
            <td>{len(items)}</td>
            <td>{desc}</td>
        </tr>
"""
        html += """    </table>
"""

    # 语法转换对照表
    if conversion_records:
        html += f"""
    <h2>四、语法转换对照表（{len(conversion_records)} 条）</h2>
    <p style="color:#636e72;">以下 SQL 需要语法转换才能在 TiDB 中执行，已提供转换建议：</p>
"""
        for i, rec in enumerate(conversion_records[:20], 1):
            conv_points_html = ""
            for conv in rec["conversions"]:
                conv_points_html += f"""            <li><strong>{conv['description']}</strong>：{conv['reason']}</li>
"""
            
            html += f"""
    <div class="conversion-table">
        <div class="conversion-header">语法转换 #{i} — {rec['category'].upper()}</div>
        <div class="conv-section">
            <div class="conv-label">【转换前 - SQL Server】</div>
            <div class="sql-block before">{rec['sql']}</div>
        </div>
        <div class="conv-arrow">↓ 转换 ↓</div>
        <div class="conv-section">
            <div class="conv-label">【转换后 - TiDB】</div>
            <div class="sql-block after">{rec['converted_sql']}</div>
        </div>
        <div class="conv-section">
            <div class="conv-label">【转换点】</div>
            <ul class="conv-value">
{conv_points_html}            </ul>
        </div>
        <div class="conv-section">
            <div class="conv-label">【原始错误】</div>
            <div class="sql-block">{rec['error']}</div>
        </div>
    </div>
"""

    # 错误 SQL 明细
    if error_sqls:
        html += f"""
    <h2>五、错误 SQL 明细（共 {len(error_sqls)} 条）</h2>
    <table>
        <tr><th>#</th><th>SQL（截断）</th><th>错误信息</th><th>分类</th></tr>
"""
        for i, item in enumerate(error_sqls[:30], 1):
            category, _ = classify_error(item.get("error_code"), item.get("error", ""))
            html += f"""        <tr>
            <td>{i}</td>
            <td><div class="sql-block">{item['sql'][:150]}...</div></td>
            <td>{item.get('error', 'N/A')[:80]}</td>
            <td><span class="error-tag {category}">{category}</span></td>
        </tr>
"""
        if len(error_sqls) > 30:
            html += f"""        <tr><td colspan="4" style="color:#636e72;">... 还有 {len(error_sqls) - 30} 条错误未显示</td></tr>
"""
        html += """    </table>
"""

    # 慢 SQL Top 10
    if slow_sqls:
        html += """
    <h2>六、回放耗时 Top 10</h2>
    <table>
        <tr><th>#</th><th>SQL（截断）</th><th>类型</th><th>回放耗时</th></tr>
"""
        for i, item in enumerate(slow_sqls, 1):
            duration_ms = item.get("replay_duration_us", 0) / 1000
            html += f"""        <tr>
            <td>{i}</td>
            <td><div class="sql-block">{item['sql'][:100]}...</div></td>
            <td>{item.get('sql_type', 'N/A')}</td>
            <td>{duration_ms:.2f} ms</td>
        </tr>
"""
        html += """    </table>
"""

    # 迁移风险评估
    compat_pct = float(compat_rate.rstrip("%"))
    if compat_pct >= 99:
        risk = ("risk-low", "低风险", "SQL 兼容性优秀，可直接进行迁移")
    elif compat_pct >= 95:
        risk = ("risk-medium", "中风险", "存在少量不兼容 SQL，建议逐条分析并手动改写")
    elif compat_pct >= 90:
        risk = ("risk-medium", "中高风险", "部分核心 SQL 不兼容，需要重点关注")
    else:
        risk = ("risk-high", "高风险", "兼容性较低，建议先完成不兼容 SQL 的改写再迁移")
    
    html += f"""
    <h2>七、迁移风险评估</h2>
    <div class="section">
        <p class="{risk[0]}" style="font-size:20px; padding:20px; background:#f8f9fa; border-radius:8px;">
            风险等级：<strong>{risk[1]}</strong><br>
            {risk[2]}
        </p>
"""
    
    if error_classification:
        html += """        <h3>主要风险点</h3>
        <ul>
"""
        for category, items in sorted(error_classification.items(), key=lambda x: -len(x[1]))[:5]:
            html += f"""            <li><strong>{category}</strong>：{len(items)} 条 SQL 存在此问题，{items[0]['description'] if items else ''}</li>
"""
        html += """        </ul>
"""
    
    html += """    </div>

    <div class="footer">
        <p>报告由 sqlserver-tidb-replay skill 生成 | Powered by 大鹅虾 🦢🦐</p>
    </div>
</div>
</body>
</html>
"""
    return html

def main():
    parser = argparse.ArgumentParser(description="SQL 回放结果分析器，生成 HTML 报告（含语法转换）")
    parser.add_argument("--input-dir", "-i", required=True, help="回放结果目录")
    parser.add_argument("--task-name", "-t", required=True, help="任务名称")
    parser.add_argument("--output", "-o", required=True, help="输出 HTML 报告路径")
    parser.add_argument("--source-db", default="SQL Server", help="源数据库名称")
    parser.add_argument("--target-db", default="TiDB", help="目标数据库名称")
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    summary_file = input_dir / f"{args.task_name}_summary.json"
    
    if not summary_file.exists():
        print(f"[ERROR] 汇总文件不存在: {summary_file}", file=sys.stderr)
        return 1
    
    print(f"[INFO] 加载汇总: {summary_file}")
    summary = load_summary(summary_file)
    
    print(f"[INFO] 加载详细结果...")
    results = load_all_results(input_dir, args.task_name)
    print(f"[INFO] 共 {len(results)} 条结果")
    
    print(f"[INFO] 生成 HTML 报告（含语法转换）...")
    html = generate_html_report(
        summary, results,
        output_path=args.output,
        source_db=args.source_db,
        target_db=args.target_db,
    )
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"[OK] 报告已生成: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
