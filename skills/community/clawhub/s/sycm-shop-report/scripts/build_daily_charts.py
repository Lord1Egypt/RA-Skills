#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本脚本是 sycm-shop-report 流水线的【第 2 步 · 图表渲染（日报）】。
职责范围严格受限：读 daily_data.json（或 example）→ 用 matplotlib 输出 PNG 到 <output_dir>/<charts_subdir>/
不做：不取生意参谋数据、不生成 docx、不做文案分析
完整端到端流程（agent 取数 → 本脚本 → docx）见 SKILL.md 的「流水线」段。
"""
"""日报图表生成器（数据驱动）。
读取同目录 daily_data.json（不存在则用 daily_data.example.json），输出 PNG 到 <output_dir>/<charts_subdir>/。
布局与配色锁死在此文件；换店铺/换日期只需改 JSON，不要改这里。
用法： python build_daily_charts.py [数据json路径]
"""
import os, sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
arg = sys.argv[1] if len(sys.argv) > 1 else None
data_path = arg or (os.path.join(HERE, "daily_data.json") if os.path.exists(os.path.join(HERE, "daily_data.json")) else os.path.join(HERE, "daily_data.example.json"))
with open(data_path, "r", encoding="utf-8") as f:
    D = json.load(f)

OUT = os.path.join(D["output_dir"], D.get("charts_subdir", "charts"))
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.sans-serif"] = [D.get("font", "Microsoft YaHei"), "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 200
plt.rcParams["savefig.dpi"] = 200
plt.rcParams["text.color"] = "#333333"

PRIMARY, ACCENT, LIGHT = "#1F3864", "#2E5496", "#5B8FF9"
WARM, GOOD, BAD, GRAY, MUTED = "#D68910", "#1E7B34", "#C0392B", "#94A3B8", "#CBD5E1"

def clean_ax(ax, grid_axis="y"):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis=grid_axis, color="#E5E9F0", linestyle="--", linewidth=0.6)
    ax.set_axisbelow(True)

M = D["metrics"]; today = M["today"]; lastYear = M["last_year"]; prevWeek = M["prev_week"]
peer = D["peer"]

# ---- 图 1 trend_7d ----
t = D["trend7"]; days = [r[0] for r in t["days"]]; uv = [r[1] for r in t["days"]]; pay = [r[3] for r in t["days"]]
fig, ax1 = plt.subplots(figsize=(9, 4.2))
bars = ax1.bar(days, pay, color=[ACCENT]*(len(pay)-1) + [WARM], width=0.55, label="支付金额（元）")
ax1.set_ylabel("支付金额（元）", fontsize=10, color=ACCENT); ax1.set_ylim(0, max(pay)*1.18)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1000:.1f}k" if v >= 1000 else f"{v:.0f}"))
clean_ax(ax1)
for b, v in zip(bars, pay): ax1.text(b.get_x()+b.get_width()/2, v+max(pay)*0.02, f"{v:,.0f}", ha="center", fontsize=8)
ax2 = ax1.twinx(); ax2.plot(days, uv, color=BAD, marker="o", linewidth=2, markersize=6, label="进店人数")
for x, y in zip(days, uv): ax2.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8, color=BAD)
ax2.set_ylabel("进店人数（人）", fontsize=10, color=BAD); ax2.set_ylim(0, max(uv)*1.30); ax2.spines["top"].set_visible(False)
if t.get("last_year_payAmt"):
    ax1.axhline(t["last_year_payAmt"], color=MUTED, linewidth=1, linestyle=":")
    ax1.text(len(days)-1, t["last_year_payAmt"]+max(pay)*0.02, f"去年同日 {t['last_year_payAmt']:,.2f} 元", fontsize=8, color="#7A7A7A", ha="right", style="italic")
ax1.set_title("近 7 日成交金额与进店人数走势", fontsize=13, fontweight="bold", color=PRIMARY, pad=14, loc="left")
h1_, l1_ = ax1.get_legend_handles_labels(); h2_, l2_ = ax2.get_legend_handles_labels()
ax1.legend(h1_+h2_, l1_+l2_, loc="upper right", frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig(f"{OUT}/trend_7d.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 2 channel_donut ----
ch = D["channels"]["rows"]; labels = [r["name"] for r in ch]; ch_uv = [r["uv"] for r in ch]
colors = [PRIMARY, ACCENT, WARM, LIGHT][:len(ch)]
fig, ax = plt.subplots(figsize=(6.4, 4.6))
ax.pie(ch_uv, colors=colors, startangle=90, counterclock=False, autopct=lambda p: f"{p:.1f}%", pctdistance=0.78,
       wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2), textprops=dict(color="white", fontsize=10, fontweight="bold"))
ax.text(0, 0.10, f"{today['uv']:,}", ha="center", va="center", fontsize=24, fontweight="bold", color=PRIMARY)
ax.text(0, -0.18, "全店进店人数（去重）", ha="center", va="center", fontsize=9, color="#666666")
ax.legend(handles=[Patch(facecolor=c, label=f"{l}  {v:,} 人") for c, l, v in zip(colors, labels, ch_uv)],
          loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=10)
ax.set_title("昨日各入口进店人数占比（存在交叉）", fontsize=12, fontweight="bold", color=PRIMARY, pad=8)
plt.tight_layout(); plt.savefig(f"{OUT}/channel_donut.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 3 compare_3col ----
it = D["items"]; mets = it["compare_metrics"]; now_v = it["compare_now"]; lw_v = it["compare_prevweek"]; ly_v = it["compare_ly"]
y = np.arange(len(mets)); h = 0.26
fig, ax = plt.subplots(figsize=(9.4, 4.4))
b1 = ax.barh(y-h, now_v, h, color=PRIMARY, label=f"昨日 {D['period']['title_date'][5:]}")
b2 = ax.barh(y, lw_v, h, color=GRAY, label=f"上周同日 {D['period']['prev_week_date'][5:]}")
b3 = ax.barh(y+h, ly_v, h, color=MUTED, label=f"去年同日 {D['period']['yoy_date']}")
ax.set_yticks(y); ax.set_yticklabels(mets, fontsize=10); ax.invert_yaxis(); ax.set_xscale("log")
ax.set_xlim(min([v for v in now_v+lw_v+ly_v if v > 0])*0.5, max(now_v+lw_v+ly_v)*8)
ax.set_xlabel("数值（对数刻度）", fontsize=9, color="#666666")
for bars, data, colr in [(b1, now_v, PRIMARY), (b2, lw_v, "#666666"), (b3, ly_v, "#8A8A8A")]:
    for b, v in zip(bars, data):
        if v > 0: ax.text(v*1.10, b.get_y()+b.get_height()/2, (f"{v:,.0f}" if v >= 100 else f"{v:,.2f}"), va="center", fontsize=8, color=colr)
clean_ax(ax, grid_axis="x")
ax.set_title("关键指标 · 三期对比（对数轴）", fontsize=13, fontweight="bold", color=PRIMARY, pad=10, loc="left")
ax.legend(loc="lower right", frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig(f"{OUT}/compare_3col.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 4 item_top ----
titles = [r["title"] for r in it["rows"]]; item_now = [r["payAmt"] for r in it["rows"]]; total = it["total_payAmt"]
fig, ax = plt.subplots(figsize=(9, 3.6))
bar_colors = [PRIMARY, ACCENT, LIGHT, "#82B9F5", GRAY, "#B8C4D4", "#CBD5E1"][:len(titles)]
bars = ax.barh(range(len(titles)), item_now, color=bar_colors, height=0.55)
ax.set_yticks(range(len(titles))); ax.set_yticklabels(titles, fontsize=9.5); ax.invert_yaxis()
ax.axvline(total, color=BAD, linestyle=":", linewidth=1, alpha=0.7)
for i, (b, v) in enumerate(zip(bars, item_now)):
    ax.text(v+total*0.01, b.get_y()+b.get_height()/2, f"{v:,.2f} 元 · {v/total*100:.1f}%", va="center", fontsize=9)
ax.set_xlim(0, total*1.35); ax.set_xlabel("支付金额（元）", fontsize=10, color="#666666")
clean_ax(ax, grid_axis="x")
ax.set_title(f"昨日商品成交 TOP 榜（合计 {total:,.2f} 元 · {len(titles)} 个 SKU）", fontsize=13, fontweight="bold", color=PRIMARY, pad=10, loc="left")
plt.tight_layout(); plt.savefig(f"{OUT}/item_top.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 5 peer_compare ----
pl = ["进店人数", "浏览量", "支付金额", "买东西人数", "订单数"]
self_v = [peer["self"]["uv"], peer["self"]["pv"], peer["self"]["payAmt"], peer["self"]["payUsr"], peer["self"]["payCnt"]]
avg_v = [peer["avg"]["uv"], peer["avg"]["pv"], peer["avg"]["payAmt"], peer["avg"]["payUsr"], peer["avg"]["payCnt"]]
exc_v = [peer["good"]["uv"], peer["good"]["pv"], peer["good"]["payAmt"], peer["good"]["payUsr"], peer["good"]["payCnt"]]
x = np.arange(len(pl)); w = 0.26
fig, ax = plt.subplots(figsize=(9, 4.2))
b1 = ax.bar(x-w, self_v, w, color=PRIMARY, label="本店"); b2 = ax.bar(x, avg_v, w, color=GRAY, label="同行平均"); b3 = ax.bar(x+w, exc_v, w, color=WARM, label="同行优秀")
ax.set_yscale("log"); ax.set_ylim(max(1, min(self_v)*0.4), max(exc_v)*12); ax.set_xticks(x); ax.set_xticklabels(pl, fontsize=10)
ax.set_ylabel("数值（对数刻度）", fontsize=9, color="#666666")
for bars, data in [(b1, self_v), (b2, avg_v), (b3, exc_v)]:
    for b, v in zip(bars, data): ax.text(b.get_x()+b.get_width()/2, v*1.10, (f"{v:,.0f}" if v >= 1 else f"{v:.2f}"), ha="center", fontsize=7.5)
clean_ax(ax); ax.set_title("本店与同行同层对照（昨日单日）", fontsize=13, fontweight="bold", color=PRIMARY, pad=10, loc="left")
ax.legend(loc="upper left", frameon=False, fontsize=9, ncol=3)
plt.tight_layout(); plt.savefig(f"{OUT}/peer_compare.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 6 yoy_vs_peer ----
pa = peer.get("peer_ly", {}).get("avg", {})
mets6 = ["进店人数", "浏览量", "支付金额", "买东西人数", "成交转化率*"]
self_g = [(today["uv"]/lastYear["uv"]-1)*100, (today["pv"]/lastYear["pv"]-1)*100, (today["payAmt"]/lastYear["payAmt"]-1)*100,
          (today["payByrCnt"]/lastYear["payByrCnt"]-1)*100 if lastYear["payByrCnt"] else 0, (today["payRate"]-lastYear["payRate"])*100]
if pa:
    peer_g = [(peer["avg"]["uv"]/pa["uv"]-1)*100, (peer["avg"]["pv"]/pa["pv"]-1)*100, (peer["avg"]["payAmt"]/pa["payAmt"]-1)*100,
              (peer["avg"]["payUsr"]/pa["payUsr"]-1)*100, (peer["avg"]["tcr"]-pa["tcr"])*100]
else:
    peer_g = [0]*5
x = np.arange(len(mets6)); w = 0.36
fig, ax = plt.subplots(figsize=(9, 4.2))
b1 = ax.bar(x-w/2, self_g, w, color=[BAD if g < 0 else GOOD for g in self_g], label="本店同比")
b2 = ax.bar(x+w/2, peer_g, w, color=MUTED, label="同行平均同比")
ax.axhline(0, color="#666666", linewidth=0.8); ax.set_xticks(x); ax.set_xticklabels(mets6, fontsize=10)
ax.set_ylabel("同比变化（%，转化率*为 pp）", fontsize=9, color="#666666")
for bars, data, is_self in [(b1, self_g, True), (b2, peer_g, False)]:
    for b, v in zip(bars, data):
        ax.text(b.get_x()+b.get_width()/2, v+(3 if v >= 0 else -6), f"{v:+.1f}", ha="center", fontsize=8.5,
                color=(BAD if v < 0 else GOOD) if is_self else "#4A5568", fontweight="bold" if is_self else "normal")
allv = self_g+peer_g; ax.set_ylim(min(allv)-15, max(allv)+25)
clean_ax(ax); ax.set_title("同比对照：本店 vs 同行平均（本期 vs 去年同期）", fontsize=13, fontweight="bold", color=PRIMARY, pad=10, loc="left")
ax.legend(loc="upper left", frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig(f"{OUT}/yoy_vs_peer.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 7 funnel ----
fn = D["funnel"]; stages = fn["stages"]; now_f = fn["now"]; ly_f = fn["ly"]
x = np.arange(len(stages)); w = 0.36
fig, ax = plt.subplots(figsize=(9, 3.6))
b1 = ax.bar(x-w/2, now_f, w, color=PRIMARY, label="本期"); b2 = ax.bar(x+w/2, ly_f, w, color=MUTED, label="去年同期")
ax.set_yscale("log"); ax.set_ylim(max(1, min(now_f+ly_f)*0.5), max(now_f+ly_f)*8)
ax.set_xticks(x); ax.set_xticklabels(stages, fontsize=10)
for bars, data in [(b1, now_f), (b2, ly_f)]:
    for b, v in zip(bars, data): ax.text(b.get_x()+b.get_width()/2, v*1.10, f"{v:,}\n{v/data[0]*100:.1f}%", ha="center", fontsize=8)
ax.set_ylabel("人数（对数刻度）· 标注=占进店比", fontsize=9, color="#666666")
clean_ax(ax); ax.set_title("成交漏斗同比对照（本期 vs 去年同期）", fontsize=13, fontweight="bold", color=PRIMARY, pad=10, loc="left")
ax.legend(loc="upper right", frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig(f"{OUT}/funnel.png", bbox_inches="tight", facecolor="white"); plt.close()

print("Daily charts ->", OUT)
for f_ in sorted(os.listdir(OUT)):
    if f_.endswith(".png"): print(" -", f_, os.path.getsize(os.path.join(OUT, f_)), "bytes")
