#!/usr/bin/env python3
"""
综合分析报告生成器 — 合并所有分析结果成一份 HTML/Markdown 报告
"""

import csv, argparse, sys, os
from collections import Counter
from datetime import datetime


def analyze_dlt(path):
    data = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                f_nums = sorted(int(r[f"号码{i}"]) for i in range(1, 6) if r.get(f"号码{i}", "").strip())
                b_nums = sorted(int(r[f"号码{i}"]) for i in range(6, 8) if r.get(f"号码{i}", "").strip())
                if len(f_nums) == 5 and len(b_nums) == 2:
                    data.append((r["期号"], f_nums, b_nums))
            except (ValueError, KeyError):
                continue
    if not data:
        return None

    front_flat = []
    back_flat = []
    front_odd = []
    sums = []
    spans = []

    for q, f, b in data:
        front_flat.extend(f)
        back_flat.extend(b)
        front_odd.append(sum(1 for x in f if x % 2))
        sums.append(sum(f))
        spans.append(max(f) - min(f))

    fc = Counter(front_flat)
    bc = Counter(back_flat)

    def oe_ratio(nums, size=5):
        return f"{sum(1 for x in nums if x%2)}:{size - sum(1 for x in nums if x%2)}"

    return {
        "total": len(data),
        "qihao_range": f"{data[0][0]} ~ {data[-1][0]}",
        "front_freq": fc.most_common(10),
        "back_freq": bc.most_common(6),
        "front_cold": fc.most_common()[-10:],
        "avg_sum": sum(sums) / len(sums) if sums else 0,
        "avg_span": sum(spans) / len(spans) if spans else 0,
        "avg_odd": sum(front_odd) / len(front_odd) if front_odd else 0,
        "front_range_min": min(front_flat),
        "front_range_max": max(front_flat),
    }


def analyze_simple(path, n):
    data = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                nums = sorted(int(r[f"号码{i}"]) for i in range(1, n + 1) if r.get(f"号码{i}", "").strip())
                if len(nums) == n:
                    data.append((r["期号"], nums))
            except (ValueError, KeyError):
                continue
    if not data:
        return None
    nums_flat = [x for _, ns in data for x in ns]
    fc = Counter(nums_flat)
    sums = [sum(ns) for _, ns in data]
    return {
        "total": len(data),
        "qihao_range": f"{data[0][0]} ~ {data[-1][0]}",
        "freq": fc.most_common(10),
        "avg_sum": sum(sums) / len(sums) if sums else 0,
    }


def generate_html(result, lottery, path):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    name = f"{lottery} 分析报告"
    total = result["total"]

    freq_rows = "".join(
        f"<tr><td>{n:02d}</td><td>{c}</td><td>{c/total*100:.1f}%</td><td><div class='bar' style='width: {c/total*100*2}px'></div></td></tr>"
        for n, c in result.get("front_freq", result.get("freq", []))
    )

    cold_rows = ""
    if "front_cold" in result:
        cold_rows = "".join(
            f"<tr><td>{n:02d}</td><td>{c}</td><td>{c/total*100:.1f}%</td></tr>"
            for n, c in result["front_cold"][:5]
        )

    back_rows = ""
    if "back_freq" in result:
        back_rows = "".join(
            f"<tr><td>{n:02d}</td><td>{c}</td><td>{c/total*100:.1f}%</td></tr>"
            for n, c in result["back_freq"]
        )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{name}</title>
<style>
body {{ font-family: -apple-system, "Microsoft YaHei", sans-serif; margin: 20px; background: #f5f6fa; color: #333; }}
.container {{ max-width: 900px; margin: 0 auto; }}
h1 {{ color: #e63946; border-bottom: 3px solid #e63946; padding-bottom: 8px; }}
h2 {{ color: #1d3557; margin-top: 28px; }}
.header {{ background: white; padding: 16px 24px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; }}
.section {{ background: white; padding: 16px 24px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 16px; }}
.stat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
.stat-item {{ padding: 8px 12px; background: #f0f4ff; border-radius: 6px; }}
.stat-label {{ font-size: 12px; color: #666; }}
.stat-value {{ font-size: 18px; font-weight: bold; color: #1d3557; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
th, td {{ padding: 8px 12px; text-align: center; border-bottom: 1px solid #eee; }}
th {{ background: #f0f4ff; font-weight: 600; color: #1d3557; }}
.bar {{ height: 16px; background: linear-gradient(90deg, #e63946, #f4a261); border-radius: 8px; }}
.footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; }}
</style>
</head>
<body>
<div class="container">
  <h1>📊 {name}</h1>
  <div class="header">
    <p>📅 生成时间: {now} | 📋 分析: {total} 期 | 期号范围: {result.get("qihao_range", "")}</p>
  </div>
  <div class="section">
    <h2>📈 基础统计</h2>
    <div class="stat-grid">
      <div class="stat-item"><div class="stat-label">总期数</div><div class="stat-value">{total}</div></div>
      <div class="stat-item"><div class="stat-label">平均和值</div><div class="stat-value">{result.get("avg_sum", 0):.1f}</div></div>
      <div class="stat-item"><div class="stat-label">平均跨度</div><div class="stat-value">{result.get("avg_span", "N/A")}</div></div>
      <div class="stat-item"><div class="stat-label">平均奇号数</div><div class="stat-value">{result.get("avg_odd", "N/A")}</div></div>
    </div>
  </div>
  <div class="section">
    <h2>🔥 热号 TOP10</h2>
    <table>
      <tr><th>号码</th><th>出现次数</th><th>频率</th><th>热度条</th></tr>
      {freq_rows}
    </table>
  </div>
  {"<div class='section'><h2>❄️ 冷号 TOP5</h2><table><tr><th>号码</th><th>出现次数</th><th>频率</th></tr>" + cold_rows + "</table></div>" if cold_rows else ""}
  {"<div class='section'><h2>🔵 后区频率</h2><table><tr><th>号码</th><th>出现次数</th><th>频率</th></tr>" + back_rows + "</table></div>" if back_rows else ""}
  <div class="section">
    <h2>⚠️ 免责声明</h2>
    <p style="color:#666;font-size:13px;">本报告仅供分析参考，不构成任何投注建议。彩票有风险，投注需理性。</p>
  </div>
  <div class="footer">Generated by 体彩筛选 Skill v1.0.0</div>
</div>
</body>
</html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    ap = argparse.ArgumentParser(description="综合分析报告生成器")
    ap.add_argument("file", help="CSV文件")
    ap.add_argument("--lottery", default="大乐透", choices=["大乐透", "排列3", "排列5", "七星彩"])
    ap.add_argument("--output", "-o", help="输出报告路径(默认自动生成)")
    args = ap.parse_args()

    if args.output:
        out_path = args.output
    else:
        base = os.path.splitext(os.path.basename(args.file))[0]
        out_path = f"{base}_report.html"

    try:
        if args.lottery == "大乐透":
            result = analyze_dlt(args.file)
        elif args.lottery == "排列3":
            result = analyze_simple(args.file, 3)
        elif args.lottery == "排列5":
            result = analyze_simple(args.file, 5)
        elif args.lottery == "七星彩":
            result = analyze_simple(args.file, 7)
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        sys.exit(1)

    if result is None:
        print(f"❌ 无法从CSV中提取{args.lottery}数据（格式不匹配或空数据）")
        sys.exit(1)

    path = generate_html(result, args.lottery, out_path)
    print(f"✅ 报告已生成: {path}")
    print(f"📊 数据概要: {result['total']} 期, 期号 {result.get('qihao_range', '')}")


if __name__ == "__main__":
    main()
