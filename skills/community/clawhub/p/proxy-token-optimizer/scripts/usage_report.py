#!/usr/bin/env python3
"""
用量报告 — 从 PostgreSQL usage_records 表读取真实数据

需要在 openclaw-manager 项目环境中运行 (需要 DB 连接)。
"""

import json
import sys
from datetime import datetime, timedelta

# 延迟导入，仅在实际运行时需要
def _get_db():
    """获取数据库 session"""
    try:
        from app.database import SessionLocal
        return SessionLocal()
    except ImportError:
        print("错误: 需要在 openclaw-manager 项目环境中运行")
        print("请使用: cd /path/to/openclaw-manager && python -m my_skills.openclaw-token-optimizer.scripts.usage_report")
        sys.exit(1)


def overview(days: int = 30) -> dict:
    """全平台用量概览。

    Args:
        days: 统计天数

    Returns:
        dict with overview data
    """
    from sqlalchemy import func, text
    from app.models import UsageRecord, Instance

    db = _get_db()
    try:
        since = datetime.utcnow() - timedelta(days=days)

        # 总量统计
        totals = db.execute(text("""
            SELECT
                COUNT(*) as total_records,
                COALESCE(SUM(calls), 0) as total_calls,
                COALESCE(SUM(tokens_in), 0) as total_tokens_in,
                COALESCE(SUM(tokens_out), 0) as total_tokens_out,
                COALESCE(SUM(tokens_in + tokens_out), 0) as total_tokens
            FROM usage_records
            WHERE recorded_at >= :since
        """), {"since": since}).fetchone()

        # 按 Provider 分布
        by_provider = db.execute(text("""
            SELECT
                provider,
                SUM(calls) as calls,
                SUM(tokens_in + tokens_out) as tokens
            FROM usage_records
            WHERE recorded_at >= :since
            GROUP BY provider
            ORDER BY tokens DESC
        """), {"since": since}).fetchall()

        # 按 Model 分布
        by_model = db.execute(text("""
            SELECT
                model,
                provider,
                SUM(calls) as calls,
                SUM(tokens_in) as tokens_in,
                SUM(tokens_out) as tokens_out
            FROM usage_records
            WHERE recorded_at >= :since
            GROUP BY model, provider
            ORDER BY (SUM(tokens_in) + SUM(tokens_out)) DESC
        """), {"since": since}).fetchall()

        # Top 10 高消耗实例
        top_instances = db.execute(text("""
            SELECT
                u.instance_id,
                i.name as instance_name,
                SUM(u.calls) as calls,
                SUM(u.tokens_in + u.tokens_out) as tokens
            FROM usage_records u
            LEFT JOIN instances i ON u.instance_id = i.id
            WHERE u.recorded_at >= :since
              AND u.instance_id NOT LIKE '__%%'
            GROUP BY u.instance_id, i.name
            ORDER BY tokens DESC
            LIMIT 10
        """), {"since": since}).fetchall()

        # 日趋势 (最近 7 天)
        daily_trend = db.execute(text("""
            SELECT
                DATE(recorded_at) as day,
                SUM(calls) as calls,
                SUM(tokens_in + tokens_out) as tokens
            FROM usage_records
            WHERE recorded_at >= :since7
            GROUP BY DATE(recorded_at)
            ORDER BY day
        """), {"since7": datetime.utcnow() - timedelta(days=7)}).fetchall()

        return {
            "period_days": days,
            "totals": {
                "records": totals[0],
                "calls": totals[1],
                "tokens_in": totals[2],
                "tokens_out": totals[3],
                "tokens_total": totals[4],
            },
            "by_provider": [
                {"provider": r[0], "calls": r[1], "tokens": r[2]}
                for r in by_provider
            ],
            "by_model": [
                {"model": r[0], "provider": r[1], "calls": r[2],
                 "tokens_in": r[3], "tokens_out": r[4]}
                for r in by_model
            ],
            "top_instances": [
                {"instance_id": r[0][:8] + "...", "name": r[1] or "unknown",
                 "calls": r[2], "tokens": r[3]}
                for r in top_instances
            ],
            "daily_trend": [
                {"day": str(r[0]), "calls": r[1], "tokens": r[2]}
                for r in daily_trend
            ],
        }
    finally:
        db.close()


def instance_report(instance_name: str, days: int = 30) -> dict:
    """单实例用量报告。

    Args:
        instance_name: 实例名称
        days: 统计天数
    """
    from sqlalchemy import text
    from app.models import Instance

    db = _get_db()
    try:
        # 查找实例
        instance = db.execute(
            text("SELECT id, name, total_calls, total_tokens, total_tokens_in, total_tokens_out FROM instances WHERE name = :name"),
            {"name": instance_name}
        ).fetchone()

        if not instance:
            return {"error": f"实例不存在: {instance_name}"}

        instance_id = instance[0]
        since = datetime.utcnow() - timedelta(days=days)

        # 按 model 分布
        by_model = db.execute(text("""
            SELECT
                model, provider,
                SUM(calls) as calls,
                SUM(tokens_in) as tokens_in,
                SUM(tokens_out) as tokens_out
            FROM usage_records
            WHERE instance_id = :iid AND recorded_at >= :since
            GROUP BY model, provider
            ORDER BY (SUM(tokens_in) + SUM(tokens_out)) DESC
        """), {"iid": instance_id, "since": since}).fetchall()

        # 日趋势
        daily = db.execute(text("""
            SELECT
                DATE(recorded_at) as day,
                SUM(calls) as calls,
                SUM(tokens_in + tokens_out) as tokens
            FROM usage_records
            WHERE instance_id = :iid AND recorded_at >= :since
            GROUP BY DATE(recorded_at)
            ORDER BY day
        """), {"iid": instance_id, "since": since}).fetchall()

        return {
            "instance": {
                "name": instance[1],
                "total_calls": instance[2],
                "total_tokens": instance[3],
                "total_tokens_in": instance[4],
                "total_tokens_out": instance[5],
            },
            "period_days": days,
            "by_model": [
                {"model": r[0], "provider": r[1], "calls": r[2],
                 "tokens_in": r[3], "tokens_out": r[4]}
                for r in by_model
            ],
            "daily_trend": [
                {"day": str(r[0]), "calls": r[1], "tokens": r[2]}
                for r in daily
            ],
        }
    finally:
        db.close()


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  usage_report.py overview [days]")
        print("  usage_report.py instance <name> [days]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "overview":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        result = overview(days)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "instance":
        if len(sys.argv) < 3:
            print("用法: usage_report.py instance <name> [days]")
            sys.exit(1)
        name = sys.argv[2]
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        result = instance_report(name, days)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
