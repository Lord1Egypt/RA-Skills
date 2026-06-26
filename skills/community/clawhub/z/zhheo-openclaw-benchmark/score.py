#!/usr/bin/env python3
"""
OpenClaw Benchmark Scorer — 3DMark-style unbounded score
Usage: python3 score.py metrics.json [--out report.html]
"""

import json
import sys
import os
from datetime import datetime

def compute_score(m):
    """
    Compute 3DMark-style unbounded score.
    
    Formula:
      Score = (Base + TTFT_bonus + Tool_bonus) × Context_ratio × Recovery
    
    Components:
      Base         = gen_tok_s × 10            (unbounded, primary factor)
      TTFT_bonus   = 10000 / ttft_ms           (reward fast first token)
      Tool_bonus   = 10000 / tool_avg_ms       (reward fast tool calls)
      Context_ratio= actual_tok/s ÷ raw_tok/s  (penalty for context burden)
      Recovery     = passed / total             (penalty for failures)
    """
    gen = m.get("gen_tok_s", 1)
    ttft = m.get("ttft_ms", 1000)
    tool = m.get("tool_avg_ms", 5000)
    ctx_ratio = m.get("context_ratio", 1.0)
    recovery = m.get("recovery_rate", 1.0)

    gen = max(gen, 0.1)
    ttft = max(ttft, 10)
    tool = max(tool, 100)

    base = gen * 10
    ttft_bonus = 10000.0 / ttft
    tool_bonus = 10000.0 / tool
    score = (base + ttft_bonus + tool_bonus) * ctx_ratio * recovery
    return round(score, 1)

def grade(score):
    if score >= 2000: return "S+", "#ff6b35"
    if score >= 1000: return "S", "#3fb950"
    if score >= 500:  return "A", "#58a6ff"
    if score >= 200:  return "B", "#8b949e"
    if score >= 50:   return "C", "#d29922"
    return "D", "#f85149"

def generate_html(m, score, grade_str, grade_color):
    tests_html = ""
    for t in m.get("tests", []):
        status_class = "ok" if t.get("status") == "ok" else "warn"
        status_text = "✅" if t.get("status") == "ok" else "⚠️"
        dur = t.get("duration_s", 0)
        tools = t.get("tool_calls", 0)
        tokens = t.get("total_tokens", 0)
        extra = ""
        if t.get("failed"):
            extra = f' <span class="tag tag-warn">{t["failed"]}失败</span>'
        tests_html += f"""
        <tr>
          <td>{t.get('id','')}</td>
          <td>{t.get('name','')}</td>
          <td>{dur}s</td>
          <td>{tokens//1000}k</td>
          <td>{tools}</td>
          <td><span class="tag tag-{status_class}">{status_text}</span>{extra}</td>
        </tr>"""

    sys_info = m.get("system", {})
    model_info = m.get("model", {})

    # Component score bars
    gen = m.get("gen_tok_s", 1)
    ttft = m.get("ttft_ms", 1000)
    tool = m.get("tool_avg_ms", 5000)
    ctx_r = m.get("context_ratio", 1.0)
    recovery = m.get("recovery_rate", 1.0)

    base = gen * 10
    ttft_b = 10000.0 / max(ttft, 10)
    tool_b = 10000.0 / max(tool, 100)
    total_raw = base + ttft_b + tool_b

    def pct(v, total):
        return min(round(v / total * 100), 100) if total > 0 else 0

    components = [
        ("基础吞吐 (tok/s×10)", base, pct(base, total_raw), "#58a6ff"),
        ("首 Token 响应", ttft_b, pct(ttft_b, total_raw), "#3fb950"),
        ("工具效率", tool_b, pct(tool_b, total_raw), "#d29922"),
    ]

    comp_html = ""
    for label, val, p, color in components:
        comp_html += f"""
        <div class="score-row">
          <div class="score-label">{label}</div>
          <div class="score-bar"><div class="score-fill" style="width:{p}%;background:{color};">{val:.0f}</div></div>
          <div class="score-val">{val:.0f}</div>
        </div>"""

    # Penalty indicators
    penalty_html = ""
    if ctx_r < 0.8:
        penalty_html += f'<div class="tip"><strong>⚠️ 上下文负担过重:</strong> 可用吞吐仅为原始的 {ctx_r*100:.0f}%，考虑精简 system prompt 或减少 skill 数量</div>\n'
    if recovery < 1.0:
        penalty_html += f'<div class="tip"><strong>⚠️ 测试未全部通过:</strong> 恢复率 {recovery*100:.0f}%，部分工具调用失败</div>\n'
    if not penalty_html:
        penalty_html = '<div class="tip" style="border-left-color:#3fb950;"><strong>✅ 无扣分项</strong> — 所有测试通过，上下文负担合理</div>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>OpenClaw Benchmark — {score}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'SF Pro','Helvetica Neue',sans-serif;background:#0d1117;color:#e6edf3;padding:24px;line-height:1.6}}
.header{{text-align:center;margin-bottom:32px;padding:32px 0;border-bottom:1px solid #30363d}}
.header h1{{font-size:24px;margin-bottom:4px}}
.header .meta{{color:#8b949e;font-size:13px;margin-bottom:16px}}
.header .score{{font-size:72px;font-weight:800;letter-spacing:-2px;color:{grade_color}}}
.header .grade{{display:inline-block;font-size:28px;font-weight:700;color:{grade_color};border:3px solid {grade_color};border-radius:8px;padding:4px 16px;margin-left:16px}}
.header .score-label{{color:#8b949e;font-size:13px;margin-top:8px}}
.meta-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}}
.meta-card{{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;font-size:13px}}
.meta-card h3{{font-size:12px;color:#8b949e;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px}}
.meta-card .row{{display:flex;justify-content:space-between;padding:3px 0}}
.meta-card .label{{color:#8b949e}}
table{{width:100%;border-collapse:collapse;margin-bottom:24px;background:#161b22;border-radius:8px;overflow:hidden}}
th{{background:#21262d;padding:10px 14px;text-align:left;font-size:12px;color:#8b949e;text-transform:uppercase;letter-spacing:0.5px}}
td{{padding:10px 14px;border-top:1px solid #21262d;font-size:13px}}
tr:hover td{{background:#1c2128}}
.section{{margin-bottom:28px}}
.section h2{{font-size:16px;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #21262d}}
.score-row{{display:flex;align-items:center;margin-bottom:8px}}
.score-label{{width:160px;font-size:13px;flex-shrink:0;color:#8b949e}}
.score-bar{{flex:1;height:22px;background:#21262d;border-radius:4px;overflow:hidden}}
.score-fill{{height:100%;border-radius:4px;display:flex;align-items:center;justify-content:flex-end;padding-right:8px;font-size:11px;font-weight:600;color:#fff;min-width:40px}}
.score-val{{width:60px;text-align:right;font-size:13px;font-weight:600;margin-left:8px}}
.tip{{background:#161b22;border-left:3px solid #58a6ff;padding:10px 14px;margin-bottom:8px;border-radius:0 6px 6px 0;font-size:13px}}
.tag{{display:inline-block;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600}}
.tag-ok{{background:rgba(63,185,80,0.15);color:#3fb950}}
.tag-warn{{background:rgba(210,153,34,0.15);color:#d29922}}
.footer{{text-align:center;color:#484f58;font-size:12px;margin-top:32px;padding-top:16px;border-top:1px solid #21262d}}
</style>
</head>
<body>

<div class="header">
  <h1>⚡ OpenClaw Performance Benchmark</h1>
  <div class="meta">{datetime.now().strftime('%Y-%m-%d %H:%M')} · {sys_info.get('os','')} · {sys_info.get('arch','')}</div>
  <div>
    <span class="score">{score}</span>
    <span class="grade">{grade_str}</span>
  </div>
  <div class="score-label">Composite Score — higher is better, no upper limit</div>
</div>

<div class="meta-grid">
  <div class="meta-card">
    <h3>🧠 模型</h3>
    <div class="row"><span class="label">模型</span><span>{model_info.get('name','—')}</span></div>
    <div class="row"><span class="label">上下文窗口</span><span>{model_info.get('context_window','—')}</span></div>
    <div class="row"><span class="label">生成速度</span><span>{gen:.1f} tok/s</span></div>
    <div class="row"><span class="label">首 Token</span><span>{ttft:.0f} ms</span></div>
  </div>
  <div class="meta-card">
    <h3>⚙️ 系统</h3>
    <div class="row"><span class="label">OpenClaw</span><span>{sys_info.get('openclaw_version','—')}</span></div>
    <div class="row"><span class="label">Node.js</span><span>{sys_info.get('node_version','—')}</span></div>
    <div class="row"><span class="label">Skills 数量</span><span>{sys_info.get('skill_count','—')}</span></div>
    <div class="row"><span class="label">System Prompt</span><span>{sys_info.get('system_prompt_tokens','—')} tokens</span></div>
  </div>
</div>

<div class="section">
  <h2>📊 评分构成</h2>
  {comp_html}
  <div class="score-row" style="margin-top:12px;padding-top:12px;border-top:1px solid #21262d">
    <div class="score-label" style="font-weight:700">上下文效率比</div>
    <div class="score-bar"><div class="score-fill" style="width:{ctx_r*100:.0f}%;background:{'#3fb950' if ctx_r>0.8 else '#d29922'};">{ctx_r*100:.0f}%</div></div>
    <div class="score-val" style="color:{'#3fb950' if ctx_r>0.8 else '#d29922'}">{ctx_r*100:.0f}%</div>
  </div>
  <div class="score-row">
    <div class="score-label" style="font-weight:700">测试恢复率</div>
    <div class="score-bar"><div class="score-fill" style="width:{recovery*100:.0f}%;background:{'#3fb950' if recovery>0.8 else '#d29922'};">{recovery*100:.0f}%</div></div>
    <div class="score-val" style="color:{'#3fb950' if recovery>0.8 else '#d29922'}">{recovery*100:.0f}%</div>
  </div>
</div>

<div class="section">
  <h2>📋 测试详情</h2>
  <table>
    <tr><th>#</th><th>测试项</th><th>耗时</th><th>Token</th><th>工具</th><th>状态</th></tr>
    {tests_html}
  </table>
</div>

<div class="section">
  <h2>🔍 扣分分析</h2>
  {penalty_html}
</div>

<div class="section">
  <h2>📐 评分公式</h2>
  <div class="tip" style="border-left-color:#8b949e;">
    <strong>Score = (Base + TTFT_bonus + Tool_bonus) × Context_ratio × Recovery</strong><br><br>
    Base = gen_tok/s × 10 — 生成速度，主要分值，无上限<br>
    TTFT_bonus = 10000 ÷ TTFT_ms — 首 Token 响应速度奖励<br>
    Tool_bonus = 10000 ÷ tool_avg_ms — 工具调用效率奖励<br>
    Context_ratio = 实际吞吐 ÷ 原始吞吐 — 上下文负担惩罚（0~1）<br>
    Recovery = 通过数 ÷ 总数 — 失败惩罚（0~1）
  </div>
</div>

<div class="footer">
  OpenClaw Benchmark v1 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · 评分无上限，越高越好 · <a href="https://zhheo.com" target="_blank" style="color:#58a6ff;text-decoration:none;">开发者: zhheo</a>
</div>

</body>
</html>"""
    return html


def compare_reports(current, baseline):
    """Compare current metrics against baseline and show deltas."""
    score_cur = compute_score(current)
    score_base = compute_score(baseline)
    delta = score_cur - score_base
    pct = (delta / score_base * 100) if score_base > 0 else 0

    def fmt_delta(v, unit="", lower_is_better=False):
        if v == 0: return f"{unit} 🟡 持平"
        improved = (v < 0) if lower_is_better else (v > 0)
        icon = "🟢" if improved else "🔴"
        sign = "" if v < 0 else "+"
        return f"{sign}{v:.1f}{unit} {icon}"

    lines = [""]
    lines.append("=" * 50)
    lines.append("📊 前后对比")
    lines.append("=" * 50)
    lines.append(f"当前: {score_cur} ({grade(score_cur)[0]})  vs  基线: {score_base} ({grade(score_base)[0]})")
    lines.append(f"总分变化: {delta:+.1f} ({pct:+.1f}%) {'🟢 改善' if delta > 0 else '🔴 退步' if delta < 0 else '🟡 持平'}")
    lines.append("")

    metrics_compare = [
        ("gen_tok_s", "生成速度", "tok/s", False),
        ("ttft_ms", "首 Token", "ms", True),
        ("tool_avg_ms", "工具耗时", "ms", True),
        ("context_ratio", "上下文效率", "", False),
        ("recovery_rate", "恢复率", "", False),
    ]

    for key, label, unit, lower_better in metrics_compare:
        cv = current.get(key, 0)
        bv = baseline.get(key, 0)
        d = cv - bv
        lines.append(f"  {label}: {bv:.1f}{unit} → {cv:.1f}{unit}  {fmt_delta(d, unit, lower_better)}")

    print("\n".join(lines))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 score.py metrics.json [--out report.html] [--compare baseline.json]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        metrics = json.load(f)

    score = compute_score(metrics)
    grade_str, grade_color = grade(score)

    if "--compare" in sys.argv:
        base_path = sys.argv[sys.argv.index("--compare") + 1]
        with open(base_path) as f:
            baseline = json.load(f)
        compare_reports(metrics, baseline)

    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
    else:
        out_dir = os.path.expanduser("~/Downloads/OpenClaw-Benchmark/results")
        os.makedirs(out_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(out_dir, f"bench_{ts}.html")

    html = generate_html(metrics, score, grade_str, grade_color)
    with open(out_path, "w") as f:
        f.write(html)

    print(f"\nScore: {score} ({grade_str})")
    print(f"Report: {out_path}")
