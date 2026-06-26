#!/usr/bin/env python3
"""
social-matrix-manager-claw: 自媒体矩阵数据分析核心脚本
用途：解析账号数据（CSV/Excel），计算指标，检测异常，生成日报
"""

import sys
import json
import csv
import argparse
from datetime import datetime, timedelta
from pathlib import Path


def load_data(file_path: str) -> list[dict]:
    """加载账号数据文件（CSV 格式）"""
    path = Path(file_path)
    if not path.exists():
        print(f"[ERROR] 文件不存在: {file_path}", file=sys.stderr)
        sys.exit(1)

    rows = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def calc_metrics(row: dict) -> dict:
    """计算单账号核心指标"""
    try:
        plays = float(row.get("plays", 0) or 0)
        likes = float(row.get("likes", 0) or 0)
        comments = float(row.get("comments", 0) or 0)
        shares = float(row.get("shares", 0) or 0)
        new_fans = float(row.get("new_fans", 0) or 0)
        total_fans = float(row.get("total_fans", 1) or 1)
        avg_plays_30d = float(row.get("avg_plays_30d", 0) or 0)

        engagement_rate = (likes + comments + shares) / plays * 100 if plays > 0 else 0
        fan_growth_rate = new_fans / total_fans * 100 if total_fans > 0 else 0
        viral_score = plays / avg_plays_30d if avg_plays_30d > 0 else 0

        return {
            "engagement_rate": round(engagement_rate, 2),
            "fan_growth_rate": round(fan_growth_rate, 4),
            "viral_score": round(viral_score, 2),
        }
    except (ValueError, ZeroDivisionError):
        return {"engagement_rate": 0, "fan_growth_rate": 0, "viral_score": 0}


def detect_anomalies(row: dict, metrics: dict, config: dict) -> list[str]:
    """检测异常并返回预警列表"""
    alerts = []
    viral_threshold = config.get("viral_threshold", 3.0)
    decline_days = config.get("decline_days", 3)

    if metrics["viral_score"] >= viral_threshold:
        alerts.append(f"🔥 爆款预警：播放量是30日均值的 {metrics['viral_score']:.1f} 倍")

    consecutive_decline = int(row.get("consecutive_decline_days", 0) or 0)
    if consecutive_decline >= decline_days:
        alerts.append(f"📉 数据下滑：已连续 {consecutive_decline} 天下降")

    if row.get("risk_signal", "").strip():
        alerts.append(f"⚠️ 账号风险：{row['risk_signal']}")

    return alerts


def generate_report(data: list[dict], config: dict) -> str:
    """生成矩阵日报文本"""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"# 自媒体矩阵日报 {today}\n"]

    total_plays = 0
    total_new_fans = 0
    anomaly_accounts = []
    viral_accounts = []

    account_rows = []
    for row in data:
        metrics = calc_metrics(row)
        alerts = detect_anomalies(row, metrics, config)
        plays = float(row.get("plays", 0) or 0)
        new_fans = float(row.get("new_fans", 0) or 0)
        total_plays += plays
        total_new_fans += new_fans

        if alerts:
            anomaly_accounts.append((row.get("account_name", "未知"), alerts))
        if metrics["viral_score"] >= config.get("viral_threshold", 3.0):
            viral_accounts.append(row.get("account_name", "未知"))

        account_rows.append({
            "name": row.get("account_name", "未知"),
            "platform": row.get("platform", "-"),
            "plays": int(plays),
            "new_fans": int(new_fans),
            "engagement_rate": metrics["engagement_rate"],
            "viral_score": metrics["viral_score"],
            "alerts": alerts,
        })

    # 汇总
    lines.append(f"## 📊 矩阵总览")
    lines.append(f"- 账号总数：{len(data)} 个")
    lines.append(f"- 总播放量：{int(total_plays):,}")
    lines.append(f"- 总涨粉数：{int(total_new_fans):,}")
    lines.append(f"- 异常账号：{len(anomaly_accounts)} 个")
    lines.append("")

    # 异常预警
    if anomaly_accounts:
        lines.append("## 🚨 异常预警")
        for name, alerts in anomaly_accounts:
            lines.append(f"\n**{name}**")
            for alert in alerts:
                lines.append(f"  - {alert}")
        lines.append("")

    # 账号明细
    lines.append("## 📋 账号明细")
    lines.append("| 账号 | 平台 | 播放量 | 涨粉 | 互动率 | 爆款系数 | 状态 |")
    lines.append("|------|------|--------|------|--------|----------|------|")
    for r in account_rows:
        status = "🔥 爆款" if r["viral_score"] >= config.get("viral_threshold", 3.0) else \
                 "⚠️ 异常" if r["alerts"] else "✅ 正常"
        lines.append(
            f"| {r['name']} | {r['platform']} | {r['plays']:,} | "
            f"{r['new_fans']:,} | {r['engagement_rate']}% | "
            f"{r['viral_score']:.1f}x | {status} |"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="自媒体矩阵数据分析")
    parser.add_argument("file", help="账号数据 CSV 文件路径")
    parser.add_argument("--viral-threshold", type=float, default=3.0,
                        help="爆款预警阈值（默认3倍均值）")
    parser.add_argument("--decline-days", type=int, default=3,
                        help="连续下滑预警天数（默认3天）")
    parser.add_argument("--output", help="输出报告文件路径（不填则打印到终端）")
    args = parser.parse_args()

    config = {
        "viral_threshold": args.viral_threshold,
        "decline_days": args.decline_days,
    }

    data = load_data(args.file)
    report = generate_report(data, config)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"[OK] 报告已保存到: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
