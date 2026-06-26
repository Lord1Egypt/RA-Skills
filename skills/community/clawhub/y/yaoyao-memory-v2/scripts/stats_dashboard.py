#!/usr/bin/env python3
"""
stats_dashboard.py - 记忆统计面板
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
STATE_FILE = MEMORY_DIR / "heartbeat-state.json"
OUTPUT_DIR = MEMORY_DIR / "reports"


def get_memory_stats() -> Dict:
    try:
        from memory import Memory
        m = Memory()
        return m.stats()
    except Exception as e:
        return {"error": str(e)}


def scan_memory_files() -> List[Dict]:
    memories = []
    if not MEMORY_DIR.exists():
        return memories
    
    for f in MEMORY_DIR.glob("*.md"):
        if f.name.startswith(".") or "合并版" in f.name:
            continue
        try:
            content = f.read_text(encoding="utf-8")
            stat = f.stat()
            created = datetime.fromtimestamp(stat.st_ctime)
            modified = datetime.fromtimestamp(stat.st_mtime)
            
            memory_type = "info"
            importance = "Normal"
            for line in content.split("\n")[:20]:
                if line.startswith("类型:") or line.startswith("type:"):
                    memory_type = line.split(":")[1].strip().lower()
                if line.startswith("重要性:") or line.startswith("importance:"):
                    importance = line.split(":")[1].strip()
            
            memories.append({
                "file": f.name,
                "size": stat.st_size,
                "created": created,
                "modified": modified,
                "type": memory_type,
                "importance": importance,
            })
        except:
            pass
    return memories


def get_state_info() -> Dict:
    if not STATE_FILE.exists():
        return {}
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {}


def calc_type_distribution(memories):
    return dict(Counter(m["type"] for m in memories))


def calc_importance_distribution(memories):
    return dict(Counter(m["importance"] for m in memories))


def calc_daily_distribution(memories, days=30):
    now = datetime.now()
    cutoff = now - timedelta(days=days)
    daily = defaultdict(int)
    for m in memories:
        if m["modified"] >= cutoff:
            date_key = m["modified"].strftime("%Y-%m-%d")
            daily[date_key] += 1
    return dict(daily)


def calc_health_score(stats, memories):
    score = 100
    total = stats.get("total", len(memories))
    if total < 10:
        score -= 20
    elif total < 50:
        score -= 10
    error_count = stats.get("by_type", {}).get("error", 0)
    if error_count > 10:
        score -= 15
    elif error_count > 5:
        score -= 5
    return max(0, score)


def generate_html_report(stats, memories, state):
    type_dist = calc_type_distribution(memories)
    importance_dist = calc_importance_distribution(memories)
    health_score = calc_health_score(stats, memories)
    by_type = stats.get("by_type", type_dist)
    by_importance = stats.get("by_importance", importance_dist)
    total = stats.get("total", len(memories))
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build type bars
    max_type = max(by_type.values()) if by_type else 1
    type_bars = ""
    for t, v in sorted(by_type.items(), key=lambda x: -x[1]):
        pct = v / max_type * 100
        type_bars += f'<div class="bar-item"><div class="bar-label">{t}</div><div class="bar"><div class="bar-fill" style="width:{pct}%"></div></div><div class="bar-value">{v}</div></div>'
    
    # Build importance bars
    max_imp = max(by_importance.values()) if by_importance else 1
    imp_bars = ""
    for t, v in sorted(by_importance.items(), key=lambda x: -x[1]):
        pct = v / max_imp * 100
        imp_bars += f'<div class="bar-item"><div class="bar-label">{t}</div><div class="bar"><div class="bar-fill" style="width:{pct}%"></div></div><div class="bar-value">{v}</div></div>'
    
    # Last sync
    last_sync = state.get("lastChecks", {}).get("imaSync", "从未")
    if last_sync and last_sync != "never":
        last_sync = last_sync[:19]
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>摇摇记忆 - 统计面板</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f5f5;padding:20px}}
.container{{max-width:1200px;margin:0 auto}}
h1{{color:#333;margin-bottom:20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}}
.card{{background:white;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.1)}}
.card h2{{color:#666;font-size:14px;margin-bottom:15px}}
.stat{{font-size:48px;font-weight:bold;color:#333}}
.bar-chart{{display:flex;flex-direction:column;gap:8px}}
.bar-item{{display:flex;align-items:center;gap:10px}}
.bar-label{{width:80px;font-size:13px;color:#666}}
.bar{{flex:1;height:20px;background:#e0e0e0;border-radius:4px;overflow:hidden}}
.bar-fill{{height:100%;background:linear-gradient(90deg,#4CAF50,#8BC34A);border-radius:4px}}
.bar-value{{width:40px;text-align:right;font-size:13px}}
.timeline{{display:flex;flex-direction:column;gap:4px}}
.timeline-item{{display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #eee}}
.timeline-date{{color:#999;font-size:12px}}
.timeline-value{{font-weight:bold}}
.status-ok{{color:#4CAF50}}
.status-warn{{color:#FF9800}}
.status-error{{color:#F44336}}
.footer{{text-align:center;color:#999;font-size:12px;margin-top:30px}}
</style>
</head>
<body>
<div class="container">
<h1>🦞 摇摇记忆系统 - 统计面板</h1>
<div class="grid">
<div class="card"><h2>📚 总记忆数</h2><div class="stat">{total}</div></div>
<div class="card"><h2>💚 健康度</h2><div class="stat status-ok">{health_score}</div></div>
<div class="card"><h2>✅ 决策记录</h2><div class="stat">{by_type.get('decision', 0)}</div></div>
<div class="card"><h2>❌ 错误记录</h2><div class="stat status-ok">{by_type.get('error', 0)}</div></div>
</div>
<div class="grid" style="margin-top:20px">
<div class="card"><h2>📊 类型分布</h2><div class="bar-chart">{type_bars}</div></div>
<div class="card"><h2>⭐ 重要性分布</h2><div class="bar-chart">{imp_bars}</div></div>
</div>
<div class="grid" style="margin-top:20px">
<div class="card"><h2>🔧 系统状态</h2><div class="timeline">
<div class="timeline-item"><span class="timeline-date">向量缓存</span><span class="timeline-value">{total} 条</span></div>
<div class="timeline-item"><span class="timeline-date">最后同步</span><span class="timeline-value">{last_sync}</span></div>
</div></div>
</div>
<div class="footer"><p>生成时间：{generated_at}</p><p>摇摇记忆系统 v3.5.0</p></div>
</div>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="记忆统计面板")
    parser.add_argument("--html", action="store_true", help="生成 HTML 报告")
    parser.add_argument("--json", action="store_true", help="生成 JSON 报告")
    parser.add_argument("--open", action="store_true", help="打开报告")
    args = parser.parse_args()
    
    stats = get_memory_stats()
    memories = scan_memory_files()
    state = get_state_info()
    
    if args.html or args.open:
        html = generate_html_report(stats, memories, state)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / "dashboard.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML: {output_path}")
        if args.open:
            import webbrowser
            webbrowser.open(f"file://{output_path}")
    
    elif args.json:
        report = {
            "generated_at": datetime.now().isoformat(),
            "total": stats.get("total", len(memories)),
            "by_type": stats.get("by_type", calc_type_distribution(memories)),
            "by_importance": stats.get("by_importance", calc_importance_distribution(memories)),
        }
        output_path = OUTPUT_DIR / "stats.json"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"JSON: {output_path}")
    
    else:
        total = stats.get("total", len(memories))
        hs = calc_health_score(stats, memories)
        print(f"📊 摇摇记忆 - 统计摘要")
        print(f"总记忆: {total}")
        print(f"健康度: {hs}分")
        print(f"报告: {OUTPUT_DIR}/dashboard.html")


if __name__ == "__main__":
    main()
