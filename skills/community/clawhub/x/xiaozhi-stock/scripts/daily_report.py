#!/usr/bin/env python3
"""
小智每日市场报告 — 一键生成大盘+板块+持仓分析
输出JSON + Markdown 双格式，供定时任务自动推送
"""
import sys, os, json
from datetime import datetime

if sys.stdout.encoding and 'UTF-8' not in sys.stdout.encoding.upper():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_stock import fetch_indices, fetch_hot_sectors, fetch_stock
from score import score_biga, score_timing

WATCHLIST = ["600519", "300750", "688981", "601899", "603993", "000630", "600036", "000001"]
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "memory")


def generate_report() -> dict:
    """生成完整市场报告"""
    start = datetime.now()
    
    # 1. 大盘指数
    indices = fetch_indices()
    
    # 2. 热点板块TOP10
    sectors = fetch_hot_sectors()[:10]
    
    # 3. 持仓池评分
    pool = []
    for code in WATCHLIST:
        try:
            data = fetch_stock(code)
            if "error" not in data and data.get("current", 0) > 0:
                biga = score_biga(data)
                timing = score_timing(data)
                pool.append({
                    "code": code,
                    "name": data.get("name", ""),
                    "price": data.get("current", 0),
                    "change_pct": data.get("change_pct", 0),
                    "biga": biga["total"],
                    "timing": timing["timing_score"],
                    "signal": timing["signal"],
                    "long_ok": biga["total"] >= 50,
                    "short_ok": timing["timing_score"] >= 0,
                    "source": data.get("source", ""),
                })
        except Exception:
            continue
    
    # 排序：涨幅降序
    pool.sort(key=lambda x: x["change_pct"], reverse=True)
    
    # 4. 统计
    up = sum(1 for s in pool if s["change_pct"] > 0)
    down = sum(1 for s in pool if s["change_pct"] < 0)
    limit_up = sum(1 for s in pool if s["change_pct"] >= 9.5)
    all_pass = sum(1 for s in pool if s["long_ok"] and s["short_ok"])
    
    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_seconds": round((datetime.now() - start).total_seconds(), 2),
        "indices": indices,
        "sectors": sectors,
        "pool": pool,
        "stats": {
            "total": len(pool),
            "up": up,
            "down": down,
            "limit_up": limit_up,
            "avg_change": round(sum(s["change_pct"] for s in pool) / len(pool), 2) if pool else 0,
            "dual_signal_pass": all_pass,
        },
    }
    return report


def fmt_markdown(report: dict) -> str:
    """Markdown格式化"""
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines.append(f"# 🦊 小智市场报告 · {now}")
    lines.append("")

    # 大盘
    lines.append("## 📊 大盘指数")
    for idx in report.get("indices", []):
        sign = "+" if idx["change_pct"] >= 0 else ""
        emoji = "🔴" if idx["change_pct"] >= 0 else "🟢"
        lines.append(f"- {emoji} **{idx['name']}**: {idx['current']:,.2f} ({sign}{idx['change_pct']:.2f}%) 成交{idx['amount_yi']}亿")
    lines.append("")

    # 热点板块
    lines.append("## 🔥 热点板块 TOP10")
    for i, sec in enumerate(report.get("sectors", []), 1):
        sign = "+" if sec["change_pct"] >= 0 else ""
        lines.append(f"- {i}. {sec['name']}: {sign}{sec['change_pct']}%")
    lines.append("")

    # 持仓池评分
    lines.append("## 📋 持仓池评分")
    lines.append(f"| 代码 | 名称 | 现价 | 涨跌幅 | BigA | 择时 | 长线 | 短线 |")
    lines.append(f"|:----:|:----:|:----:|:------:|:----:|:----:|:----:|:----:|")
    for s in report.get("pool", []):
        chg = f"+{s['change_pct']}%" if s['change_pct'] >= 0 else f"{s['change_pct']}%"
        lines.append(f"| {s['code']} | {s['name']} | {s['price']} | {chg} | {s['biga']} | {s['timing']:+d} | {'✅' if s['long_ok'] else '❌'} | {'✅' if s['short_ok'] else '❌'} |")
    lines.append("")

    # 统计
    stats = report.get("stats", {})
    lines.append("## 📈 统计")
    lines.append(f"- 总数: {stats['total']} | 上涨: {stats['up']} | 下跌: {stats['down']} | 涨停: {stats['limit_up']}")
    lines.append(f"- 平均涨幅: {stats['avg_change']:+.2f}%")
    lines.append(f"- 双信号全通: {stats['dual_signal_pass']}/{stats['total']}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"生成耗时: {report['elapsed_seconds']}s | 数据来源: 新浪/东财/腾讯")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="小智每日市场报告")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--save", action="store_true", help="保存到memory目录")
    args = parser.parse_args()

    report = generate_report()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.save:
        date_str = datetime.now().strftime("%Y%m%d_%H%M")
        # JSON
        json_path = os.path.join(OUTPUT_DIR, f"report_{date_str}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        # Markdown
        md_path = os.path.join(OUTPUT_DIR, f"report_{date_str}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(fmt_markdown(report))
        print(f"✅ 报告已保存:")
        print(f"  JSON: {json_path}")
        print(f"  MD:   {md_path}")
        print()
        print(fmt_markdown(report))
    else:
        print(fmt_markdown(report))


if __name__ == "__main__":
    main()
