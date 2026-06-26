#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
查询客流数据 (openclaw_fetch_zwc_keliu)

用法：
  python query.py --start 2026-04-01 --end 2026-04-10

输出：
  {"status":"ok","columns":[...],"rows":[...]}

环境变量：
  MY_SQL_SERVER   - xxx.xx.xx
  MY_SQL_DATABASE - xxxxx
  MY_SQL_USER     - xxxx
  MY_SQL_PASSWORD - xx
"""

import os
import sys
import logging
import pyodbc
import pandas as pd
from typing import List, Dict, Any
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

def subtract_one_year_pro(date_str):

    d = date_str - relativedelta(years=1)
    return d.strftime("%Y-%m-%d")

# 你可以把这个值改为你实际的偏差（正数表示数据库时间晚）
TIMEZONE_OFFSET_DAYS = 0  

def parse_date(date_str):
    # 把字符串转换为 datetime，默认是本地时间
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    # 调整到数据库时间
    return d + timedelta(days=TIMEZONE_OFFSET_DAYS)
# -------------------------------
# ① 环境变量配置
# -------------------------------
SQL_SERVER   = os.getenv("MY_SQL_SERVER", "")
SQL_DATABASE = os.getenv("MY_SQL_DATABASE", "")
SQL_USER     = os.getenv("MY_SQL_USER", "")
SQL_PASSWORD = os.getenv("MY_SQL_PASSWORD", "") 

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s – %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# -------------------------------
# ② 数据库连接
# -------------------------------
def connect_to_db() -> pyodbc.Connection:
    """返回一个新的 pyodbc 连接"""
    conn_str = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USER};"
        f"PWD={SQL_PASSWORD}"
    )
    return pyodbc.connect(conn_str, timeout=30)

# -------------------------------
# ③ 执行存储过程
# -------------------------------
def execute_procedure(proc_name: str, params: List[Any]) -> pd.DataFrame | None:
    """执行存储过程并返回 DataFrame"""
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            ph = ", ".join(["?"] * len(params))
            cur.execute(f"EXEC {proc_name} {ph}", params)
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
            return pd.DataFrame.from_records(rows, columns=cols)
    finally:
        conn.close()

# -------------------------------
# ④ 主入口（被 skill 调用）
# -------------------------------
def main(start_curr: str, end_curr: str, start_prev: str | None = None, end_prev: str | None = None) -> Dict[str, Any]:
    """查询并返回 JSON"""
    if start_prev is None:
        start_prev = subtract_one_year_pro(start_curr)
    if end_prev is None:
        end_prev = subtract_one_year_pro(end_curr)

    df = execute_procedure(

        "openclaw_fetch_zwc_keliu",
        [start_curr, end_curr, start_prev, end_prev]
    )

    if df is None or df.empty:
        return {"status": "empty"}

    return {
        "status": "ok",
        "columns": df.columns.tolist(),
        "rows": df.to_dict(orient="records")
    }

# -------------------------------
# ⑤ 命令行入口
# -------------------------------
if __name__ == "__main__":
    # 简单解析参数，支持 --start / --end
    args = {k.lstrip("--"): v for k, v in zip(sys.argv[1::2], sys.argv[2::2])}
    start = parse_date(args.get("start"))
    end   = parse_date(args.get("end"))

    if not start or not end:
        print("用法: python query.py --start YYYY-MM-DD --end YYYY-MM-DD")
        sys.exit(1)

    result = main(start, end)
    print(result)
