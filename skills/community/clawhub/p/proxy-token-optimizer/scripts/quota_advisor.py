#!/usr/bin/env python3
"""
套餐匹配建议 — 分析实际用量 vs 套餐上限

检测:
  - 套餐过高 (浪费): 实际用量远低于套餐上限
  - 频繁限流: 实际用量接近/超过套餐上限

需要在 openclaw-manager 项目环境中运行。
"""

import json
import sys
from datetime import datetime, timedelta


def _get_db():
    try:
        from app.database import SessionLocal
        return SessionLocal()
    except ImportError:
        print("错误: 需要在 openclaw-manager 项目环境中运行")
        sys.exit(1)


def _load_quota_plans() -> dict:
    """从 llm_proxy.yaml 加载套餐定义"""
    try:
        from app.settings import settings
        plans = {}
        for name, plan in settings.llm_proxy.quota_plans.items():
            plans[name] = {
                "window_seconds": plan.window_seconds,
                "max_calls": plan.max_calls,
                "max_tokens": plan.max_tokens,
                "max_qps": plan.max_qps,
                "monthly_max_tokens": getattr(plan, "monthly_max_tokens", 0),
            }
        return plans
    except Exception as e:
        return {"error": str(e)}


def analyze_all() -> dict:
    """分析所有实例的套餐匹配情况。"""
    from sqlalchemy import text

    db = _get_db()
    try:
        plans = _load_quota_plans()
        if "error" in plans:
            return plans

        # 获取所有实例 + 套餐
        instances = db.execute(text("""
            SELECT
                i.id, i.name, i.total_calls, i.total_tokens,
                COALESCE(q.plan, 'standard') as plan
            FROM instances i
            LEFT JOIN instance_quotas q ON i.id = q.instance_id
            WHERE i.deleted_at IS NULL AND i.status != 'deleted'
        """)).fetchall()

        # 最近 24h 用量
        since_24h = datetime.utcnow() - timedelta(hours=24)
        recent_usage = db.execute(text("""
            SELECT
                instance_id,
                SUM(calls) as calls,
                SUM(tokens_in + tokens_out) as tokens
            FROM usage_records
            WHERE recorded_at >= :since
            GROUP BY instance_id
        """), {"since": since_24h}).fetchall()

        usage_map = {r[0]: {"calls": r[1], "tokens": r[2]} for r in recent_usage}

        wasteful = []   # 套餐过高
        throttled = []  # 可能限流

        for inst in instances:
            inst_id, name, total_calls, total_tokens, plan_name = inst
            plan = plans.get(plan_name, plans.get("standard", {}))
            if not plan or isinstance(plan, str):
                continue

            recent = usage_map.get(inst_id, {"calls": 0, "tokens": 0})
            max_calls = plan.get("max_calls", 0)
            max_tokens = plan.get("max_tokens", 0)

            if max_calls <= 0:
                continue

            calls_ratio = recent["calls"] / max_calls if max_calls > 0 else 0
            tokens_ratio = recent["tokens"] / max_tokens if max_tokens > 0 else 0

            # 套餐过高: 24h 用量不到上限的 20%
            if calls_ratio < 0.2 and tokens_ratio < 0.2 and total_calls > 10:
                wasteful.append({
                    "name": name,
                    "plan": plan_name,
                    "calls_24h": recent["calls"],
                    "max_calls": max_calls,
                    "usage_ratio": round(max(calls_ratio, tokens_ratio) * 100, 1),
                    "suggestion": "考虑降级套餐",
                })

            # 频繁限流: 24h 用量超过上限的 80%
            if calls_ratio > 0.8 or tokens_ratio > 0.8:
                throttled.append({
                    "name": name,
                    "plan": plan_name,
                    "calls_24h": recent["calls"],
                    "max_calls": max_calls,
                    "tokens_24h": recent["tokens"],
                    "max_tokens": max_tokens,
                    "usage_ratio": round(max(calls_ratio, tokens_ratio) * 100, 1),
                    "suggestion": "考虑升级套餐或调整 QPS",
                })

        return {
            "total_instances": len(instances),
            "plans_available": list(plans.keys()),
            "wasteful": wasteful,
            "wasteful_count": len(wasteful),
            "throttled": throttled,
            "throttled_count": len(throttled),
        }
    finally:
        db.close()


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  quota_advisor.py analyze    # 分析所有实例")
        print("  quota_advisor.py plans      # 显示可用套餐")
        sys.exit(1)

    command = sys.argv[1]

    if command == "analyze":
        result = analyze_all()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "plans":
        plans = _load_quota_plans()
        print(json.dumps(plans, indent=2, ensure_ascii=False))

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
