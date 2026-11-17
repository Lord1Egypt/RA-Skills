#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本脚本是 sycm-shop-report 流水线的【第 2 步 · 图表渲染（周报）】。
职责范围严格受限：读 weekly_data.json（或 example）→ 用 matplotlib 输出 PNG 到 <output_dir>/<charts_subdir>/
不做：不取生意参谋数据、不生成 docx、不做文案分析
完整端到端流程（agent 取数 → 本脚本 → docx）见 SKILL.md 的「流水线」段。
"""
"""周报图表生成器（数据驱动）。
读取同目录 weekly_data.json（不存在则用 weekly_data.example.json），输出 PNG 到 <output_dir>/<charts_subdir>/。
布局与配色锁死在此文件；换店铺/换周期只需改 JSON。
用法： python build_weekly_charts.py [数据json路径]
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
data_path = arg or (os.path.join(HERE, "weekly_data.json") if os.path.exists(os.path.join(HERE, "weekly_data.json")) else os.path.join(HERE, "weekly_data.example.json"))
with open(data_path, "r", encoding="utf-8") as f:
    D = json.load(f)

OUT = os.path.join(D["output_dir"], D.get("charts_subdir", "charts_week"))
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

M = D["metrics"]; SELF = M["self"]; PREV = M["prev"]; LYR = M["last_year"]
CHW = D["channels"]["rows"]

# ---- 图 1 week_trend ----
wt = D["week_trend"]
this_days = [r[0] for r in wt["this_days"]]; this_uv = [r[1] for r in wt["this_days"]]; this_pay = [r[2] for r in wt["this_days"]]
prev_uv = [r[1] for r in wt["prev_days"]]; prev_pay = [r[2] for r in wt["prev_days"]]
x = np.arange(len(this_days)); w = 0.4
fig, ax1 = plt.subplots(figsize=(9.4, 4.2))
ax1.bar(x - w/2, this_pay, w, color=PRIMARY, label="本周支付金额")
ax1.bar(x + w/2, prev_pay, w, color=MUTED, label="上周支付金额")
ax1.set_xticks(x); ax1.set_xticklabels(this_days, fontsize=9); ax1.set_ylabel("支付金额（元）", fontsize=10, color=PRIMARY)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1000:.1f}k" if v >= 1000 else f"{v:.0f}"))
clean_ax(ax1)
for xi, v in zip(x - w/2, this_pay): ax1.text(xi, v + max(this_pay)*0.02, f"{v:,.0f}", ha="center", fontsize=7.5, color=PRIMARY, fontweight="bold")
ax2 = ax1.twinx()
ax2.plot(x, this_uv, color=BAD, marker="o", linewidth=2, markersize=6, label="本周进店")
ax2.plot(x, prev_uv, color=GRAY, marker="s", linewidth=1.6, markersize=5, linestyle="--", label="上周进店")
ax2.set_ylabel("进店人数（人）", fontsize=10, color=BAD); ax2.set_ylim(0, max(this_uv + prev_uv)*1.35)
for xi, v in zip(x, this_uv): ax2.text(xi, v + max(this_uv)*0.03, f"{v}", ha="center", fontsize=7.5, color=BAD)
ax1.set_title("本周 vs 上周 · 每日成交与进店人数", fontsize=13, fontweight="bold", color=PRIMARY, pad=12, loc="left")
h1_, l1_ = ax1.get_legend_handles_labels(); h2_, l2_ = ax2.get_legend_handles_labels()
ax1.legend(h1_+h2_, l1_+l2_, loc="upper left", frameon=False, fontsize=8.5, ncol=2)
plt.tight_layout(); plt.savefig(f"{OUT}/week_trend.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 2 week_channel_donut ----
labels = [r["name"] for r in CHW]; ch_uv = [r["uv"] for r in CHW]; colors = [PRIMARY, ACCENT, LIGHT, WARM, "#82B9F5"][:len(CHW)]
fig, ax = plt.subplots(figsize=(6.4, 4.6))
ax.pie(ch_uv, colors=colors, startangle=90, counterclock=False, autopct=lambda p: f"{p:.1f}%", pctdistance=0.78,
       wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2), textprops=dict(color="white", fontsize=10, fontweight="bold"))
ax.text(0, 0.10, f"{SELF['uv']:,}", ha="center", va="center", fontsize=24, fontweight="bold", color=PRIMARY)
ax.text(0, -0.18, "全店进店人数（周去重）", ha="center", va="center", fontsize=9, color="#666666")
ax.legend(handles=[Patch(facecolor=c, label=f"{l}  {v:,} 人") for c, l, v in zip(colors, labels, ch_uv)], loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=10)
ax.set_title("本周各入口进店人数占比（存在交叉）", fontsize=12, fontweight="bold", color=PRIMARY, pad=8)
plt.tight_layout(); plt.savefig(f"{OUT}/week_channel_donut.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 3 week_compare_3 ----
c3 = D["compare3"]; mets = c3["metrics"]; self_v = c3["self"]; prev_v = c3["prev"]; ly_v = c3["last_year"]
y = np.arange(len(mets)); h = 0.26
fig, ax = plt.subplots(figsize=(9.4, 4.4))
b1 = ax.barh(y-h, self_v, h, color=PRIMARY, label="本周"); b2 = ax.barh(y, prev_v, h, color=GRAY, label="上周"); b3 = ax.barh(y+h, ly_v, h, color=MUTED, label="去年同周")
ax.set_yticks(y); ax.set_yticklabels(mets, fontsize=10); ax.invert_yaxis(); ax.set_xscale("log")
allv = [v for v in self_v+prev_v+ly_v if v > 0]
ax.set_xlim(min(allv)*0.5, max(allv)*8); ax.set_xlabel("数值（对数刻度）", fontsize=9, color="#666666")
for bars, data, colr in [(b1, self_v, PRIMARY), (b2, prev_v, "#666666"), (b3, ly_v, "#8A8A8A")]:
    for b, v in zip(bars, data):
        if v > 0: ax.text(v*1.05, b.get_y()+b.get_height()/2, f"{v:,.0f}", va="center", fontsize=7.5, color=colr)
clean_ax(ax, grid_axis="x"); ax.set_title("关键指标 · 三期对比（对数轴）", fontsize=13, fontweight="bold", color=PRIMARY, pad=10, loc="left")
ax.legend(loc="lower right", frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig(f"{OUT}/week_compare_3.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 4 week_channel_yoy ----
ch_names = [r["name"] for r in CHW]; x = np.arange(len(ch_names)); w = 0.26
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
for ax, key_now, key_prev, key_ly, ttl, yl in [
    (ax1, "uv", "uv_prev", "uv_ly", "各入口进店人数 · 三期对比", "进店人数（人）"),
    (ax2, "pay", "pay_prev", "pay_ly", "各入口带动成交 · 三期对比", "带动成交（元）")]:
    bn = ax.bar(x-w, [r[key_now] for r in CHW], w, color=PRIMARY, label="本周")
    bp = ax.bar(x,   [r[key_prev] for r in CHW], w, color=GRAY, label="上周")
    bl = ax.bar(x+w, [max(r[key_ly], 0.5) for r in CHW], w, color=MUTED, label="去年同周")
    ax.set_xticks(x); ax.set_xticklabels(ch_names, fontsize=10); ax.set_ylabel(yl, fontsize=10); ax.set_yscale("log")
    vals = [r[key_now] for r in CHW]+[r[key_prev] for r in CHW]+[r[key_ly] for r in CHW]
    pos = [v for v in vals if v > 0]; ax.set_ylim(max(0.3, min(pos)*0.4), max(pos)*10)
    for bars in [bn, bp, bl]:
        for b in bars:
            v = b.get_height(); ax.text(b.get_x()+b.get_width()/2, v*1.05, (f"{v:,.0f}" if v >= 1 else f"{v:.1f}"), ha="center", fontsize=7)
    ax.set_title(ttl, fontsize=11, fontweight="bold", color=PRIMARY, pad=8, loc="left"); clean_ax(ax); ax.legend(frameon=False, fontsize=8.5)
plt.tight_layout(); plt.savefig(f"{OUT}/week_channel_yoy.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 5 week_growth_story ----
gs = D["growth_story"]; mets5 = gs["metrics"]
item_pay_now = next((r["pay"] for r in CHW if r["name"] == "商品页"), SELF["payAmt"])
item_pay_prev = next((r["pay_prev"] for r in CHW if r["name"] == "商品页"), PREV["payAmt"])
item_pay_ly = next((r["pay_ly"] for r in CHW if r["name"] == "商品页"), LYR["payAmt"])
wow_g = [(SELF["payAmt"]/PREV["payAmt"]-1)*100, (SELF["uv"]/PREV["uv"]-1)*100, (SELF["payByrCnt"]/PREV["payByrCnt"]-1)*100, (SELF["payPct"]/PREV["payPct"]-1)*100, (item_pay_now/item_pay_prev-1)*100]
yoy_g = [(SELF["payAmt"]/LYR["payAmt"]-1)*100, (SELF["uv"]/LYR["uv"]-1)*100, (SELF["payByrCnt"]/LYR["payByrCnt"]-1)*100, (SELF["payPct"]/LYR["payPct"]-1)*100, (item_pay_now/item_pay_ly-1)*100]
x = np.arange(len(mets5)); w = 0.36
fig, ax = plt.subplots(figsize=(9, 4.4))
b1 = ax.bar(x-w/2, wow_g, w, color=[GOOD if g > 0 else BAD for g in wow_g], label="环比上周")
b2 = ax.bar(x+w/2, yoy_g, w, color=[ACCENT if g > 0 else MUTED for g in yoy_g], label="同比去年")
ax.axhline(0, color="#666666", linewidth=0.8); ax.set_xticks(x); ax.set_xticklabels(mets5, fontsize=10); ax.set_ylabel("变化率（%）", fontsize=10, color="#666666")
allg = wow_g+yoy_g; ax.set_ylim(min(allg)-15, max(allg)+30)
for bars, data in [(b1, wow_g), (b2, yoy_g)]:
    for b, v in zip(bars, data): ax.text(b.get_x()+b.get_width()/2, v+(3 if v >= 0 else -7), f"{v:+.1f}%", ha="center", fontsize=8.5, fontweight="bold")
clean_ax(ax); ax.set_title("增长双视角：环比上周 vs 同比去年", fontsize=13, fontweight="bold", color=PRIMARY, pad=10, loc="left")
ax.legend(loc="upper left", frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig(f"{OUT}/week_growth_story.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---- 图 6 week_refund ----
rf = D["refund"]; periods = rf["periods"]; rfd_amt = rf["rfd_amt"]; pay_amt = rf["pay_amt"]
rfd_rate = [r/p*100 for r, p in zip(rfd_amt, pay_amt)]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.6))
bars = ax1.bar(periods, rfd_amt, color=[BAD, GRAY, MUTED], width=0.55)
for b, v in zip(bars, rfd_amt): ax1.text(b.get_x()+b.get_width()/2, v+max(rfd_amt)*0.02, f"{v:,.0f}", ha="center", fontsize=9, fontweight="bold")
ax1.set_title("退款金额（元）", fontsize=11, fontweight="bold", color=PRIMARY, pad=8); ax1.tick_params(axis="x", labelsize=9); ax1.set_ylim(0, max(rfd_amt)*1.2); clean_ax(ax1)
bars = ax2.bar(periods, rfd_rate, color=[BAD, GRAY, MUTED], width=0.55)
for b, v in zip(bars, rfd_rate): ax2.text(b.get_x()+b.get_width()/2, v+max(rfd_rate)*0.02, f"{v:.2f}%", ha="center", fontsize=9, fontweight="bold")
ax2.set_title("退款率 = 退款金额 / 销售额（%）", fontsize=11, fontweight="bold", color=PRIMARY, pad=8); ax2.tick_params(axis="x", labelsize=9); ax2.set_ylim(0, max(rfd_rate)*1.25); clean_ax(ax2)
plt.tight_layout(); plt.savefig(f"{OUT}/week_refund.png", bbox_inches="tight", facecolor="white"); plt.close()

print("Weekly charts ->", OUT)
for f_ in sorted(os.listdir(OUT)):
    if f_.endswith(".png"): print(" -", f_, os.path.getsize(os.path.join(OUT, f_)), "bytes")
