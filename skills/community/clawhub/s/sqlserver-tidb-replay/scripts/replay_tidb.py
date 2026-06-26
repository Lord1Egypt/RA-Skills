#!/usr/bin/env python3
"""
SQL Server → TiDB SQL 回放脚本
读取 JSON 中间格式，并行回放至 TiDB
"""

import argparse
import json
import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import pymysql
except ImportError:
    print("[ERROR] 请安装 pymysql: pip3 install pymysql", file=sys.stderr)
    sys.exit(1)

# 全局统计
stats_lock = threading.Lock()
stats = {
    "total": 0,
    "success": 0,
    "error": 0,
    "errors_by_type": {},
}

@dataclass
class ReplayResult:
    """单条SQL回放结果"""
    conn_id: str
    sql: str
    sql_type: str
    duration_us: int
    replay_duration_us: int
    error: Optional[str]
    error_code: Optional[int]
    row_count: int
    start_time: str
    replay_time: str

def create_connection(host: str, port: int, user: str, password: str, database: str):
    """创建 TiDB 连接"""
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        connect_timeout=10,
        read_timeout=30,
        write_timeout=30,
    )

def replay_sql(conn, sql: str, sql_type: str) -> tuple[int, Optional[str], Optional[int], int]:
    """
    执行单条SQL
    返回: (replay_duration_us, error_msg, error_code, row_count)
    """
    start = time.perf_counter()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            if sql_type.lower() in ("select", "cte", "merge"):
                results = cursor.fetchall()
                row_count = len(results)
            else:
                row_count = cursor.rowcount
            row_count = row_count if row_count is not None else 0
    except pymysql.err.OperationalError as e:
        return int((time.perf_counter() - start) * 1_000_000), str(e), e.args[0] if e.args else None, 0
    except pymysql.err.IntegrityError as e:
        return int((time.perf_counter() - start) * 1_000_000), str(e), e.args[0] if e.args else None, 0
    except pymysql.err.ProgrammingError as e:
        return int((time.perf_counter() - start) * 1_000_000), str(e), e.args[0] if e.args else None, 0
    except pymysql.err.DataError as e:
        return int((time.perf_counter() - start) * 1_000_000), str(e), e.args[0] if e.args else None, 0
    except Exception as e:
        return int((time.perf_counter() - start) * 1_000_000), str(e), -1, 0
    else:
        return int((time.perf_counter() - start) * 1_000_000), None, None, row_count

def replay_worker(
    sql_batch: list[dict],
    conn_params: dict,
    worker_id: int,
    speed: float,
    results_dict: dict
):
    """并发回放worker"""
    conn = None
    try:
        conn = create_connection(**conn_params)
        for item in sql_batch:
            conn_id = item["conn_id"]
            sql = item["sql"]
            sql_type = item["sql_type"]
            original_duration_us = item.get("duration_us", 0)
            start_time = item.get("start_time", "")
            
            # 跳过 COMMENT 类型
            if sql_type == "comment":
                continue
            
            # 速度控制：原始执行时间 / speed = 本次等待
            if speed > 0 and original_duration_us > 0:
                target_interval = original_duration_us / speed / 1_000_000
                # 不等待，因为是并发回放，不是1:1回放
            
            # 执行SQL
            replay_duration_us, error, error_code, row_count = replay_sql(conn, sql, sql_type)
            replay_time = datetime.now().isoformat()
            
            result = ReplayResult(
                conn_id=conn_id,
                sql=sql,
                sql_type=sql_type,
                duration_us=original_duration_us,
                replay_duration_us=replay_duration_us,
                error=error,
                error_code=error_code,
                row_count=row_count,
                start_time=start_time,
                replay_time=replay_time,
            )
            
            # 统计
            with stats_lock:
                stats["total"] += 1
                if error:
                    stats["error"] += 1
                    error_key = f"{error_code}:{error[:50]}"
                    stats["errors_by_type"][error_key] = stats["errors_by_type"].get(error_key, 0) + 1
                else:
                    stats["success"] += 1
            
            # 按 conn_id 存储
            if conn_id not in results_dict:
                results_dict[conn_id] = []
            results_dict[conn_id].append(result)
            
    except Exception as e:
        print(f"[WORKER-{worker_id}] 连接错误: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

def load_json(input_path: str) -> list[dict]:
    """加载回放JSON"""
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def group_by_conn_id(items: list[dict]) -> dict[str, list[dict]]:
    """按 conn_id 分组"""
    groups = {}
    for item in items:
        conn_id = item.get("conn_id", "unknown")
        if conn_id not in groups:
            groups[conn_id] = []
        groups[conn_id].append(item)
    return groups

def main():
    parser = argparse.ArgumentParser(description="SQL Server → TiDB SQL 回放工具")
    parser.add_argument("--input", "-i", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--host", default=os.getenv("TIDB_HOST", "127.0.0.1"), help="TiDB 地址")
    parser.add_argument("--port", type=int, default=int(os.getenv("TIDB_PORT", "4000")), help="TiDB 端口")
    parser.add_argument("--user", default=os.getenv("TIDB_USER", "root"), help="TiDB 用户")
    parser.add_argument("--password", default=os.getenv("TIDB_PASSWORD", ""), help="TiDB 密码")
    parser.add_argument("--database", default=os.getenv("TIDB_DATABASE", "test"), help="目标数据库")
    parser.add_argument("--speed", type=float, default=1.0, help="回放速度倍率（默认 1.0）")
    parser.add_argument("--workers", type=int, default=4, help="并发连接数（默认 4）")
    parser.add_argument("--output-dir", "-o", default="./replay_results", help="结果输出目录")
    parser.add_argument("--task-name", "-t", default="replay", help="任务名称")
    
    args = parser.parse_args()
    
    # 加载数据
    print(f"[INFO] 加载回放文件: {args.input}")
    items = load_json(args.input)
    print(f"[INFO] 待回放 SQL 数: {len(items)}")
    
    if not items:
        print("[ERROR] 没有可回放的 SQL", file=sys.stderr)
        return 1
    
    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 按 conn_id 分组
    conn_groups = group_by_conn_id(items)
    print(f"[INFO] 分组 conn_id 数: {len(conn_groups)}")
    
    # 连接参数
    conn_params = {
        "host": args.host,
        "port": args.port,
        "user": args.user,
        "password": args.password,
        "database": args.database,
    }
    
    print(f"[INFO] TiDB: {args.host}:{args.port}/{args.database}")
    print(f"[INFO] 并发 workers: {args.workers}")
    print(f"[INFO] 开始回放...")
    
    # 合并所有 SQL 到一个列表，按 conn_id 分批
    # 每个 worker 处理一部分 conn_id
    conn_ids = list(conn_groups.keys())
    batch_size = max(1, len(conn_ids) // args.workers)
    
    results_dict = {}  # conn_id -> results
    threads = []
    
    start_ts = time.time()
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for i in range(0, len(conn_ids), batch_size):
            batch_conn_ids = conn_ids[i:i+batch_size]
            batch_items = []
            for cid in batch_conn_ids:
                batch_items.extend(conn_groups[cid])
            
            worker_id = i // batch_size
            t = executor.submit(
                replay_worker,
                batch_items,
                conn_params,
                worker_id,
                args.speed,
                results_dict
            )
            threads.append(t)
    
    # 等待完成
    for t in as_completed(threads):
        try:
            t.result()
        except Exception as e:
            print(f"[WARN] Worker 异常: {e}", file=sys.stderr)
    
    elapsed = time.time() - start_ts
    
    # 写入结果文件
    all_results = []
    for cid, results in results_dict.items():
        result_file = output_dir / f"{args.task_name}_conn_{cid}.json"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump([r.__dict__ for r in results], f, ensure_ascii=False, indent=2)
        all_results.extend(results)
    
    # 写入汇总
    summary = {
        "task_name": args.task_name,
        "total_sqls": stats["total"],
        "success": stats["success"],
        "errors": stats["error"],
        "compatibility_rate": f"{(stats['success'] / stats['total'] * 100):.2f}%" if stats["total"] > 0 else "N/A",
        "elapsed_seconds": round(elapsed, 2),
        "workers": args.workers,
        "source": "SQL Server XE",
        "target": f"TiDB {args.host}:{args.port}/{args.database}",
        "error_distribution": stats["errors_by_type"],
        "sql_types": {},
    }
    
    # 按类型统计
    for r in all_results:
        t = r.sql_type
        if t not in summary["sql_types"]:
            summary["sql_types"][t] = {"total": 0, "errors": 0}
        summary["sql_types"][t]["total"] += 1
        if r.error:
            summary["sql_types"][t]["errors"] += 1
    
    summary_file = output_dir / f"{args.task_name}_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 打印结果
    print("")
    print(f"[RESULT] 回放完成，耗时 {elapsed:.1f}s")
    print(f"  总SQL数:    {stats['total']}")
    print(f"  成功:       {stats['success']}")
    print(f"  失败:       {stats['error']}")
    print(f"  兼容性:     {summary['compatibility_rate']}")
    print(f"  结果目录:   {output_dir}")
    
    if stats["error"] > 0:
        print(f"\n[ERRORS] 错误分布 Top5:")
        sorted_errors = sorted(stats["errors_by_type"].items(), key=lambda x: -x[1])[:5]
        for err, cnt in sorted_errors:
            print(f"  [{cnt:4d}] {err}")
    
    return 0 if stats["error"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
