#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推荐结果验证系统
追踪历史推荐的股票，验证后续表现
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_scan")
VERIFICATION_FILE = DATA_DIR / "verification_results.json"


def load_verification():
    """加载验证数据"""
    if VERIFICATION_FILE.exists():
        with open(VERIFICATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "history": [],  # 历史推荐记录
        "performance": [],  # 后续表现记录
        "stats": {
            "total_recommendations": 0,
            "avg_5d_gain": 0,
            "avg_10d_gain": 0,
            "avg_20d_gain": 0,
            "win_rate_5d": 0,
            "win_rate_10d": 0,
            "win_rate_20d": 0,
        }
    }


def save_verification(data):
    """保存验证数据"""
    VERIFICATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VERIFICATION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_recommendation_record(code, name, score, price, date=None):
    """记录一次推荐"""
    data = load_verification()
    
    record = {
        "code": code,
        "name": name,
        "score": score,
        "recommend_price": price,
        "recommend_date": date or datetime.now().strftime("%Y-%m-%d"),
        "status": "pending",  # pending, verified
    }
    
    data["history"].append(record)
    data["stats"]["total_recommendations"] += 1
    save_verification(data)
    return True


def calculate_performance(code, current_price, current_date=None):
    """计算某只股票的当前收益"""
    data = load_verification()
    date_str = current_date or datetime.now().strftime("%Y-%m-%d")
    current_date = datetime.strptime(date_str, "%Y-%m-%d")
    
    updated = False
    for rec in data["history"]:
        if rec["code"] == code and rec["status"] == "pending":
            rec_date = datetime.strptime(rec["recommend_date"], "%Y-%m-%d")
            days_diff = (current_date - rec_date).days
            
            gain = (current_price / rec["recommend_price"] - 1) * 100
            
            # 记录表现
            perf = {
                "code": rec["code"],
                "name": rec["name"],
                "score": rec["score"],
                "recommend_date": rec["recommend_date"],
                "check_date": date_str,
                "days_held": days_diff,
                "recommend_price": rec["recommend_price"],
                "current_price": current_price,
                "gain_pct": round(gain, 2),
            }
            
            # 计算不同时间段的收益
            data["performance"].append(perf)
            rec["status"] = "verified"
            updated = True
    
    if updated:
        # 更新统计
        update_stats(data)
        save_verification(data)
    
    return updated


def update_stats(data):
    """更新统计数据"""
    if not data["performance"]:
        return
    
    recent_perf = data["performance"][-100:]  # 最近100条记录
    
    gains_5d = [p["gain_pct"] for p in recent_perf if p["days_held"] >= 5]
    gains_10d = [p["gain_pct"] for p in recent_perf if p["days_held"] >= 10]
    gains_20d = [p["gain_pct"] for p in recent_perf if p["days_held"] >= 20]
    
    if gains_5d:
        data["stats"]["avg_5d_gain"] = round(sum(gains_5d) / len(gains_5d), 2)
        data["stats"]["win_rate_5d"] = round(len([g for g in gains_5d if g > 0]) / len(gains_5d) * 100, 1)
    
    if gains_10d:
        data["stats"]["avg_10d_gain"] = round(sum(gains_10d) / len(gains_10d), 2)
        data["stats"]["win_rate_10d"] = round(len([g for g in gains_10d if g > 0]) / len(gains_10d) * 100, 1)
    
    if gains_20d:
        data["stats"]["avg_20d_gain"] = round(sum(gains_20d) / len(gains_20d), 2)
        data["stats"]["win_rate_20d"] = round(len([g for g in gains_20d if g > 0]) / len(gains_20d) * 100, 1)


def get_performance_report():
    """生成表现报告"""
    data = load_verification()
    stats = data["stats"]
    
    lines = []
    lines.append("📊 推荐效果验证报告")
    lines.append(f"更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 40)
    lines.append("")
    lines.append(f"总推荐次数: {stats['total_recommendations']}")
    lines.append("")
    lines.append("【平均收益】")
    lines.append(f"  5日后: {stats['avg_5d_gain']:+.2f}%")
    lines.append(f"  10日后: {stats['avg_10d_gain']:+.2f}%")
    lines.append(f"  20日后: {stats['avg_20d_gain']:+.2f}%")
    lines.append("")
    lines.append("【胜率】")
    lines.append(f"  5日正收益: {stats['win_rate_5d']:.1f}%")
    lines.append(f"  10日正收益: {stats['win_rate_10d']:.1f}%")
    lines.append(f"  20日正收益: {stats['win_rate_20d']:.1f}%")
    lines.append("")
    
    # 按评分分组统计
    if data["performance"]:
        score_groups = defaultdict(list)
        for p in data["performance"]:
            if p["days_held"] >= 5:
                score_groups[min(p["score"] // 10 * 10, 100)].append(p["gain_pct"])
        
        lines.append("【按评分分组（5日收益）】")
        for score_range in sorted(score_groups.keys(), reverse=True):
            gains = score_groups[score_range]
            avg = sum(gains) / len(gains)
            wins = len([g for g in gains if g > 0]) / len(gains) * 100
            lines.append(f"  {score_range}-{score_range+9}分: 平均{avg:+.1f}%  胜率{wins:.0f}%")
    
    lines.append("")
    lines.append("=" * 40)
    lines.append("⚠ 数据仅供参考，不代表未来表现")
    
    return "\n".join(lines)


def get_score_distribution():
    """获取推荐评分的分布"""
    data = load_verification()
    
    if not data["history"]:
        return {}
    
    scores = [r["score"] for r in data["history"]]
    distribution = defaultdict(int)
    for s in scores:
        bucket = min(s // 10 * 10, 100)
        distribution[bucket] += 1
    
    return dict(sorted(distribution.items(), reverse=True))


if __name__ == "__main__":
    # 测试
    print("验证系统测试")
    print("-" * 40)
    
    # 添加测试记录
    add_recommendation_record("000001", "平安银行", 100, 11.00, "2026-03-25")
    add_recommendation_record("002460", "赣锋锂业", 95, 40.00, "2026-03-25")
    add_recommendation_record("603259", "药明康德", 90, 70.00, "2026-03-25")
    
    # 模拟计算收益
    calculate_performance("000001", 11.50, "2026-03-30")  # +4.5%
    calculate_performance("002460", 42.00, "2026-03-30")  # +5%
    calculate_performance("603259", 68.00, "2026-03-30")  # -2.9%
    
    # 生成报告
    print(get_performance_report())
