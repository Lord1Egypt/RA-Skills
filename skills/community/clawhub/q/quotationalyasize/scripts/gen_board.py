#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_board.py —— 多项目报价对比看板生成器（模板，脱敏可跑）

架构（核心，勿改）：
  ① 数据层（本文件上半部，标 "DATA LAYER"）—— 唯一手工维护区，只放原文数字与口径参数。
  ② 渲染层（本文件下半部，标 "RENDER LAYER"）—— 读数据层出 HTML，不要手改文案。
  ③ Excel 生成器 gen_excel.py 通过 DATA LAYER END 标记切出本文件上半部 exec 复用，
     因此 HTML 与 Excel **永远同一份数据，口径不可能分叉**。

用法：python gen_board.py   → 生成 board.html
"""
import os
import datetime as dt
import html as _html

# ============================================================================
#  DATA LAYER —— 唯一手工维护区（换项目只改这里）
# ============================================================================
BOARD_TITLE = ("项目A与项目B报价分析及定标建议",
               "Project A &amp; B — Quote Analysis &amp; Award Recommendation")
TENDER_DATE   = "2026-01-01"
INVITED_COUNT = 3

PROJECTS = [
    {"id": "p1", "name": "Project A — Display Tray", "area": "450×350×50 mm", "qty": 100},
    {"id": "p2", "name": "Project B — Counter Unit", "area": "600×400×900 mm", "qty": 40},
]

# status: received / pending（pending 自动渲染占位行，不影响任何计算）
SUPPLIERS = [
    {"key": "s1", "name": "Supplier One",   "color": "#3E8E80", "status": "received", "date": "2026-01-05"},
    {"key": "s2", "name": "Supplier Two",   "color": "#6E6486", "status": "received", "date": "2026-01-06"},
    {"key": "s3", "name": "Supplier Three", "color": "#3E6E9E", "status": "received", "date": "2026-01-07"},
]

# QUOTES：全部取自报价原文；prod/trans/inst/total 四值须满足 prod+trans+inst==total（下面有勾稽校验）
QUOTES = {
    "s1": {"p1": {"prod": 2000.00, "trans": 100.00, "inst": 0.0, "total": 2100.00},
           "p2": {"prod": 1500.00, "trans":  80.00, "inst": 0.0, "total": 1580.00}},
    "s2": {"p1": {"prod": 1800.00, "trans": 400.00, "inst": 0.0, "total": 2200.00},
           "p2": {"prod": 1700.00, "trans": 200.00, "inst": 0.0, "total": 1900.00}},
    "s3": {"p1": {"prod": 2400.00, "trans":  75.00, "inst": 0.0, "total": 2475.00},
           "p2": {"prod": 1300.00, "trans": 300.00, "inst": 0.0, "total": 1600.00}},
}

# 明细表数字格的三态文案（运输/安装列），由下面 trans_cell()/inst_cell() 依据这些备注派生
TRANS_NOTE = {
    ("s1", "p1"): "已含在运输费用中",
    ("s2", "p1"): "",
    ("s3", "p1"): "",
    ("s1", "p2"): "已含在运输费用中",
    ("s2", "p2"): "",
    ("s3", "p2"): "",
}

# ---- 工期门槛（定标模块用）----
LEAD_START    = dt.date(2026, 1, 10)   # 统一起算日（下单日）
LEAD_DEADLINE = dt.date(2026, 2, 28)   # 安装完成截止日
LEAD_SPAN = {                          # 各家「自起算至安装完成」总天数（严格取自其报价原文）
    "s1": {"p1": 30, "p2": 35},
    "s2": {"p1": 60, "p2": 55},
    "s3": {"p1": 25, "p2": 45},
}
LEAD_ABS_END   = {}                    # 给绝对日期排期者：{"s3": {"p1": dt.date(2026,2,20)}}
LEAD_BASIS = {                         # 工期依据原文（进"工期满足性判定表"）
    "s1": ("原文 30 / 35 天（未说明起算点）", "As quoted: 30 / 35 days (no start basis stated)"),
    "s2": ("原文 60 / 55 天（未说明起算点）", "As quoted: 60 / 55 days (no start basis stated)"),
    "s3": ("原文 25 / 45 天（未说明起算点）", "As quoted: 25 / 45 days (no start basis stated)"),
}
LEAD_BASIS_PID = {}                    # 按项目覆盖：{("s1","p1"): ("...","...")}

# 条款对比：取值顺序必须 == SUPPLIERS 顺序，否则整列错位
TERMS = [
    ("材质与工艺", "Material &amp; finish", "板材 A + 折边", "板材 B", "板材 C"),
    ("运输口径",   "Freight basis",         "送至单一地点",   "送至单一地点", "送至单一地点"),
    ("VAT",        "VAT",                   "未提供",         "未提供",       "未提供"),
    ("付款条件",   "Payment terms",         "未提供",         "未提供",       "未提供"),
]

# 待澄清清单（P0 > P1 > P2）
CLAR = [
    ("P0", "三家材质口径不同（板材 A / B / C）—— 须先书面确认招标材料标准，再要求按统一材质确认或重报。",
           "The three differ on material (board A / B / C) — confirm the tender material standard in writing first."),
    ("P1", "运输差价过大（示例 €75.50 vs €400）—— 须确认低价方覆盖范围是否同口径。",
           "Freight gap is large (€75.50 vs €400) — confirm the cheaper basis covers the same scope."),
]
# ============================ DATA LAYER END ============================

# ============================================================================
#  RENDER LAYER（一般不需要改动）
# ============================================================================
_recon_ok = True
for _k in QUOTES:
    for _p in PROJECTS:
        d = QUOTES[_k][_p["id"]]
        if round(d["prod"] + d["trans"] + d["inst"], 2) != round(d["total"], 2):
            _recon_ok = False
            print("RECON FAIL:", _k, _p["id"], d)
print("=== RECON (Unit+Transport+Install==Total): %s ===" % ("ALL OK" if _recon_ok else "FAILED"))

RECV_KEYS = [s["key"] for s in SUPPLIERS if s["status"] == "received"]
SUPMAP    = {s["key"]: s for s in SUPPLIERS}


def got(k):
    return k in RECV_KEYS


def esc(x):
    return _html.escape(str(x))


def euro(v):
    return "€{:,.2f}".format(v)


def min_pid(k, pid):
    """该供应商在该项目是否项目最低（渲染高亮用）"""
    return QUOTES[k][pid]["total"] == min(QUOTES[kk][pid]["total"] for kk in RECV_KEYS)


def lead_result(k, pid):
    """工期判定：绝对日期排期者不顺延，其余按 统一起算日 + 总天数"""
    if k in LEAD_ABS_END and pid in LEAD_ABS_END[k]:
        est = LEAD_ABS_END[k][pid]
    else:
        est = LEAD_START + dt.timedelta(days=LEAD_SPAN[k][pid])
    bzh, ben = LEAD_BASIS_PID.get((k, pid), LEAD_BASIS[k])
    return {"days": LEAD_SPAN[k][pid], "est": est, "ok": est <= LEAD_DEADLINE,
            "basis_zh": bzh, "basis_en": ben}


def satisfied(k, pid):
    return lead_result(k, pid)["ok"]


def sched_lowest(pid):
    """满足工期者中报价最低（定标口径；无满足者则回退纯最低）"""
    cand = sorted([k for k in RECV_KEYS if satisfied(k, pid)], key=lambda k: QUOTES[k][pid]["total"])
    if not cand:
        cand = sorted(RECV_KEYS, key=lambda k: QUOTES[k][pid]["total"])
    return cand[0], QUOTES[cand[0]][pid]["total"], cand


def cell_state(pid, k, kind):
    """明细表运输/安装列的三态：数字 / 已含在…费用中 / 未报价待澄清"""
    v = QUOTES[k][pid][kind]
    if v:
        return euro(v), ""
    note = TRANS_NOTE.get((k, pid), "")
    if note:
        return ("已包含在运输费用中", "t-included") if kind == "trans" else ("已包含在安装费用中", "t-included")
    return ("未报价待澄清", "t-na")


def Z(s):
    return '<span class="zh">' + s + '</span>'


def E(s):
    return '<span class="en">' + s + '</span>'


def BI(zh, en):
    return Z(zh) + E(en)


H = []
H.append("""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>@@TITLE@@</title><style>
:root{--bg:#f5f6f4;--card:#fff;--ink:#23282e;--mut:#6b7280;--line:#e4e7e3;
--green:#1f9d55;--greenbg:#e8f3ea;--amber:#b7791f;--amberbg:#fdf3e0;--red:#d6363a;--redbg:#fdeaea;--blue:#3E6E9E;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.6 "Segoe UI",system-ui,"Microsoft YaHei",sans-serif}
.wrap{max-width:1120px;margin:0 auto;padding:16px 20px 60px}
h1{font-size:23px;margin:0 0 4px}
h2{font-size:18px;margin:34px 0 10px;padding-left:9px;border-left:4px solid var(--blue)}
h3{font-size:15px;margin:20px 0 8px;color:#374151}
.sub{color:var(--mut);font-size:13px;margin-bottom:6px}
.zh,.en{display:inline}
.langbar{position:sticky;top:0;z-index:30;background:var(--bg);display:flex;gap:8px;align-items:center;padding:10px 0;margin-bottom:8px;border-bottom:1px solid var(--line)}
.lsw{position:absolute;opacity:0;width:0;height:0}
.swbtn{display:inline-block;line-height:1;font:13px/1 inherit;padding:8px 18px;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:22px;cursor:pointer}
body:has(#lzh:checked) .en{display:none !important}
body:has(#len:checked) .zh{display:none !important}
body:has(#lzh:checked) .zh{display:inline !important}
body:has(#len:checked) .en{display:inline !important}
body:has(#lzh:checked) .swbtn.zhb{background:var(--blue);color:#fff;border-color:var(--blue)}
body:has(#len:checked) .swbtn.enb{background:var(--blue);color:#fff;border-color:var(--blue)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:12px 0}
.note{border-radius:8px;padding:12px 14px;margin:10px 0;font-size:13px}
.note.warn{background:var(--amberbg);border:1px solid #f0d9a8;color:#7a5510}
.note.bad{background:var(--redbg);border:1px solid #f3c2c2;color:#9b2222}
.note.ok{background:var(--greenbg);border:1px solid #bfe3c9;color:#176a3c}
.note.info{background:#eef3fb;border:1px solid #cdddf0;color:#1e4d8b}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0}
@media(max-width:760px){.kpis{grid-template-columns:repeat(2,1fr)}}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.kpi .k{font-size:12px;color:var(--mut)} .kpi .v{font-size:19px;font-weight:700;margin-top:2px} .kpi .n{font-size:11.5px;color:var(--mut);margin-top:2px}
table.t{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px}
table.t th,table.t td{border:1px solid var(--line);padding:8px 10px;text-align:left}
table.t th{background:#eef1ee;font-weight:700}
table.t td.n{text-align:right;font-variant-numeric:tabular-nums}
td.min{background:var(--greenbg);color:var(--green);font-weight:700}
td.na{color:var(--mut);background:#fafbfa}
td.lead{text-align:right;font-size:11.5px;white-space:nowrap;font-variant-numeric:tabular-nums}
td.lead.ok{color:var(--green);font-weight:700} td.lead.bad{color:var(--red);font-weight:700}
table.line4 th.proc,table.line4 th.trans,table.line4 th.inst,table.line4 th.total,
table.line4 td.proc,table.line4 td.trans,table.line4 td.inst,table.line4 td.total{width:130px;min-width:130px;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
table.line4 td.t-included{font-size:11.5px;font-style:italic;color:var(--amber);text-align:right}
table.line4 td.t-na{font-size:11.5px;font-style:italic;color:var(--mut);text-align:right}
.phead{display:flex;justify-content:space-between;align-items:center;gap:14px;margin:6px 0 4px;flex-wrap:wrap}
.phead h3{margin:0}
.chip-min{background:var(--green);color:#fff;font-weight:700;font-size:13px;padding:5px 14px;border-radius:20px;white-space:nowrap}
.pill{display:inline-block;font-size:11.5px;font-weight:700;padding:2px 9px;border-radius:20px;color:#fff}
td.pass{background:var(--greenbg);color:var(--green);font-weight:700;text-align:center}
td.fail{background:var(--redbg);color:var(--red);font-weight:700;text-align:center}
tr.rec-row td{background:var(--greenbg)}
.pick{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:14px 16px;margin:10px 0}
.pick.win{border-left:4px solid var(--green)} .pick.alt{border-left:4px solid var(--blue)}
.pick .ph{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:6px}
.pick .amt{font-weight:700;color:var(--green);font-size:15px}
.tblwrap{overflow-x:auto} .tblwrap table.t{min-width:880px}
.foot{color:var(--mut);font-size:12px;margin-top:30px;border-top:1px solid var(--line);padding-top:12px}
.note-inline{font-size:11.5px;color:var(--mut);font-style:italic}
</style></head><body class="lang-zh"><div class="wrap">""".replace("@@TITLE@@", esc(" — ".join([BOARD_TITLE[0], "中/英切换版"]))))

H.append("<div class='langbar'>"
         "<input type='radio' name='lang' id='lzh' class='lsw' checked>"
         "<input type='radio' name='lang' id='len' class='lsw'>"
         "<span class='sub'>" + BI("语言", "Language") + "</span>"
         "<label for='lzh' class='swbtn zhb'>中文</label>"
         "<label for='len' class='swbtn enb'>English</label></div>")

H.append("<h1>" + BI(BOARD_TITLE[0], BOARD_TITLE[1]) + "</h1>")
_n_pend = INVITED_COUNT - len(RECV_KEYS)
H.append("<div class='sub'>" + BI(
    "发标 " + TENDER_DATE + "　·　邀请 " + str(INVITED_COUNT) + " 家　·　已回标 " + str(len(RECV_KEYS)) +
    " 家　·　待回标 " + str(_n_pend) + " 家　·　" + str(len(PROJECTS)) + " 个项目",
    "Tender " + TENDER_DATE + "　·　" + str(INVITED_COUNT) + " invited　·　" + str(len(RECV_KEYS)) +
    " received　·　" + str(_n_pend) + " pending　·　" + str(len(PROJECTS)) + " projects") + "</div>")

# ---------------- 一、回标状态与总览 ----------------
H.append("<h2>" + BI("一、回标状态与总览", "1. Bid Status &amp; Overview") + "</h2>")
H.append("<div class='kpis'>")
H.append("<div class='kpi'><div class='k'>" + BI("已回标 / 邀请", "Received / Invited") + "</div>"
         "<div class='v'>" + str(len(RECV_KEYS)) + " / " + str(INVITED_COUNT) + "</div>"
         "<div class='n'>" + (BI("全部已回标", "All received") if _n_pend == 0 else BI("另 %d 家待回标" % _n_pend, "%d pending" % _n_pend)) + "</div></div>")
for p in PROJECTS:
    _pk, _pv, _ = sched_lowest(p["id"])
    H.append("<div class='kpi'><div class='k'>" + BI(p["name"] + " 最低（工期满足）", p["name"] + " lowest (schedule-met)") + "</div>"
             "<div class='v' style='color:var(--green)'>" + esc(SUPMAP[_pk]["name"]) + "</div>"
             "<div class='n'>" + euro(_pv) + "</div></div>")
H.append("</div>")

P_SHORT = {p["id"]: p["name"].split("—")[0].strip() for p in PROJECTS}
H.append("<div class='tblwrap'><table class='t'><tr><th>" + BI("供应商", "Supplier") + "</th><th>" + BI("状态", "Status") + "</th>"
         "<th>" + BI("回标日期", "Received") + "</th>"
         + "".join("<th class='n'>" + P_SHORT[p["id"]] + "　" + BI("报价", "Price") + "</th>"
                   "<th class='n'>" + P_SHORT[p["id"]] + "　" + BI("所报工期 → 完成日", "Lead → completion") + "</th>"
                   for p in PROJECTS) + "</tr>")
for s in SUPPLIERS:
    k = s["key"]
    if got(k):
        cells = ""
        for p in PROJECTS:
            pid = p["id"]; lr = lead_result(k, pid)
            cells += "<td class='n%s'>%s</td>" % (" min" if min_pid(k, pid) else "", euro(QUOTES[k][pid]["total"]))
            cells += "<td class='lead %s'>%s</td>" % ("ok" if lr["ok"] else "bad",
                     "%d %s → %s %s" % (lr["days"], BI("天", "d"), lr["est"].strftime("%m/%d"),
                                        BI("✓ 满足", "✓ OK") if lr["ok"] else BI("✗ 超期", "✗ Late")))
    else:
        cells = "".join("<td class='n na'>—</td><td class='lead na'>—</td>" for p in PROJECTS)
    H.append("<tr><td><span class='pill' style='background:%s'>%s</span></td><td>%s</td><td>%s</td>%s</tr>"
             % (s["color"] if s["status"] == "received" else "#9aa0a6", esc(s["name"]),
                BI("已回标", "Received") if s["status"] == "received" else BI("待回标", "Pending"), s["date"] or "—", cells))
H.append("</table></div>")
H.append("<div class='note info'>" + BI(
    "「所报工期 → 完成日」= 按各单位声明的工期，自统一起算日 <b>%s</b> 推算的完成日；✓ 满足 = 能在 <b>%s</b> 前完成安装。"
    "若某家给的是绝对日期排期（起点可能早于统一起算日），其完成日按其原排期固定、不顺延。各口径原文见第三节。" % (LEAD_START.isoformat(), LEAD_DEADLINE.isoformat()),
    "“Lead → completion” = estimated completion counting the declared lead time from the unified start <b>%s</b>; "
    "✓ OK = installation can complete before <b>%s</b>. A supplier quoting absolute dates keeps its own completion (not shifted). See §3 for raw bases." % (LEAD_START.isoformat(), LEAD_DEADLINE.isoformat())) + "</div>")

# ---------------- 二、逐项目明细对比 ----------------
H.append("<h2>" + BI("二、逐项目明细对比", "2. Per-Project Line-Item Comparison") + "</h2>")
for p in PROJECTS:
    pid = p["id"]
    _pk, _pv, _ = sched_lowest(pid)
    H.append("<div class='card'>")
    H.append("<div class='phead'><h3>" + esc(p["name"]) + "　<span class='sub'>(" + esc(p["area"]) + "　·　" + BI("数量 " + str(p["qty"]), "Qty " + str(p["qty"])) + ")</span></h3>"
             "<span class='chip-min'>" + BI("✓ 当前报价最低（工期满足+报价最低）：", "✓ Current lowest (schedule-met + lowest price): ") +
             esc(SUPMAP[_pk]["name"]) + " <b>" + euro(_pv) + "</b></span></div>")
    lo = min(QUOTES[k][pid]["total"] for k in RECV_KEYS)
    H.append("<div class='tblwrap'><table class='t line4'><tr><th>" + BI("供应商", "Supplier") + "</th>"
             "<th class='proc'>" + BI("生产", "Produce") + "</th><th class='trans'>" + BI("运输", "Transport") + "</th>"
             "<th class='inst'>" + BI("安装", "Install") + "</th><th class='total'>" + BI("Total", "Total") + "</th>"
             "<th class='n'>" + BI("VS 最低", "vs lowest") + "</th><th>" + BI("费用结构明细", "Cost note") + "</th></tr>")
    for k in RECV_KEYS:
        d = QUOTES[k][pid]
        tt, tc = cell_state(pid, k, "trans"); it, ic = cell_state(pid, k, "inst")
        note = TRANS_NOTE.get((k, pid), "") or "—"
        H.append("<tr><td><span class='pill' style='background:%s'>%s</span></td>"
                 "<td class='proc'>%s</td><td class='trans %s'>%s</td><td class='inst %s'>%s</td>"
                 "<td class='total%s'>%s</td><td class='n'>%s</td><td class='sub'>%s</td></tr>"
                 % (SUPMAP[k]["color"], esc(SUPMAP[k]["name"]), euro(d["prod"]), tc, tt, ic, it,
                    " min" if d["total"] == lo else "", euro(d["total"]),
                    BI("基准", "base") if d["total"] == lo else "+" + euro(d["total"] - lo), esc(note)))
    H.append("</table></div></div>")

# ---------------- 三、工期对比 ----------------
H.append("<h2>" + BI("三、工期（Lead Time）对比", "3. Lead Time Comparison") + "</h2>")
H.append("<table class='t'><tr><th>" + BI("供应商", "Supplier") + "</th><th class='n'>" + BI("所报工期", "Declared") + "</th>"
         "<th class='n'>" + BI("自起算完成日", "Completion") + "</th><th>" + BI("依据原文", "Basis") + "</th></tr>")
for k in RECV_KEYS:
    for p in PROJECTS:
        lr = lead_result(k, p["id"])
        H.append("<tr><td><span class='pill' style='background:%s'>%s</span></td><td class='n'>%d %s</td>"
                 "<td class='n'>%s</td><td>%s</td></tr>"
                 % (SUPMAP[k]["color"], esc(SUPMAP[k]["name"]), lr["days"], BI("天", "d"),
                    lr["est"].isoformat(), BI(lr["basis_zh"], lr["basis_en"])))
H.append("</table>")

# ---------------- 四、条款对比 ----------------
H.append("<h2>" + BI("四、条款对比", "4. Terms Comparison") + "</h2>")
H.append("<table class='t'><tr><th>" + BI("条款", "Term") + "</th>"
         + "".join("<th>" + esc(s["name"]) + "</th>" for s in SUPPLIERS) + "</tr>")
for zh, en, *vals in TERMS:
    H.append("<tr><td>" + BI(zh, en) + "</td>" + "".join("<td>%s</td>" % esc(v) for v in vals) + "</tr>")
H.append("</table>")

# ---------------- 五、待澄清清单 ----------------
H.append("<h2>" + BI("五、待澄清清单", "5. Clarifications") + "</h2>")
H.append("<table class='t'><tr><th>" + BI("级别", "Level") + "</th><th>" + BI("事项（中）", "Item (ZH)") + "</th>"
         "<th>" + BI("Item (EN)", "Item (EN)") + "</th></tr>")
for pr, zh, en in sorted(CLAR, key=lambda c: {"P0": 0, "P1": 1, "P2": 2}[c[0]]):
    col = "#d6363a" if pr == "P0" else ("#b7791f" if pr == "P1" else "#6b7280")
    H.append("<tr><td><b style='color:%s'>%s</b></td><td>%s</td><td>%s</td></tr>" % (col, pr, esc(zh), esc(en)))
H.append("</table>")

# ---------------- 六、各项目价格排序（不跨项目合计） ----------------
H.append("<h2>" + BI("六、各项目价格排序", "6. Per-Project Price Ranking") + "</h2>")
H.append("<table class='t'><tr><th>" + BI("项目", "Project") + "</th>"
         + "".join("<th class='n'>%s</th>" % esc(SUPMAP[k]["name"]) for k in RECV_KEYS)
         + "<th class='n'>" + BI("差额", "Delta") + "</th><th>" + BI("该列最低", "Lowest") + "</th></tr>")
for p in PROJECTS:
    pid = p["id"]
    vals = {k: QUOTES[k][pid]["total"] for k in RECV_KEYS}
    lo_ = min(vals, key=vals.get); hi_ = max(vals, key=vals.get); d = vals[hi_] - vals[lo_]
    H.append("<tr><td>%s</td>%s<td class='n'>%s</td><td>%s</td></tr>"
             % (esc(p["name"]),
                "".join("<td class='n%s'>%s</td>" % (" min" if k == lo_ else "", euro(vals[k])) for k in RECV_KEYS),
                euro(d), esc(SUPMAP[lo_]["name"])))
H.append("</table>")
H.append("<div class='note info'>" + BI(
    "<b>本节为「纯价格」排序，不含工期条件</b>。Chafiras / Leiria 两个项目分别独立比较，<b>不做跨项目合计</b> —— 两者工程量与交付条件不同，合并总价无决策意义。",
    "<b>Pure price ranking without the schedule condition.</b> The two projects are compared independently; <b>no cross-project total</b> is shown — their scope and delivery terms differ, so a combined figure has no decision value.") + "</div>")

# ---------------- 七、定标建议（满足工期前提下，价格最低优先） ----------------
H.append("<h2>" + BI("七、定标建议（满足工期前提下，价格最低优先）", "7. Award Recommendation — Lowest Price Among Schedule-Compliant Bidders") + "</h2>")
H.append("<div class='note info'>" + BI(
    "<b>判定规则（三条）</b><br>① <b>起算日</b>：统一按 <b>%s</b> 起算；<br>"
    "② <b>工期门槛</b>：所报工期自起算日推算，能在 <b>%s</b> 前完成安装 → 满足；不能 → 列入「需请对方澄清」（非直接淘汰）；<br>"
    "③ <b>定标原则</b>：满足工期者中，报价最低优先。" % (LEAD_START.isoformat(), LEAD_DEADLINE.isoformat()),
    "<b>Award rules (three)</b><br>① <b>Start date</b>: unified at <b>%s</b>;<br>"
    "② <b>Schedule gate</b>: complete installation before <b>%s</b> → meets; otherwise → “to clarify” (not eliminated);<br>"
    "③ <b>Principle</b>: among schedule-compliant bidders, lowest price wins." % (LEAD_START.isoformat(), LEAD_DEADLINE.isoformat())) + "</div>")

H.append("<h3>" + BI("7.1 工期满足性判定", "7.1 Schedule Feasibility") + "</h3>")
H.append("<div class='tblwrap'><table class='t'><tr><th>" + BI("项目", "Project") + "</th><th>" + BI("供应商", "Supplier") + "</th>"
         "<th class='n'>" + BI("所报工期", "Days") + "</th><th>" + BI("依据原文", "Basis") + "</th>"
         "<th class='n'>" + BI("完成日", "Completion") + "</th><th class='n'>" + BI("10/31 前？", "By deadline?") + "</th></tr>")
for p in PROJECTS:
    first = True
    for k in RECV_KEYS:
        lr = lead_result(k, p["id"])
        H.append("<tr><td>%s</td><td><span class='pill' style='background:%s'>%s</span></td>"
                 "<td class='n'>%d %s</td><td>%s</td><td class='n'>%s</td><td class='%s'>%s</td></tr>"
                 % (esc(p["name"]) if first else "", SUPMAP[k]["color"], esc(SUPMAP[k]["name"]),
                    lr["days"], BI("天", "d"), BI(lr["basis_zh"], lr["basis_en"]), lr["est"].isoformat(),
                    "pass" if lr["ok"] else "fail", BI("✓ 满足", "✓ OK") if lr["ok"] else BI("✗ 需澄清", "✗ Clarify")))
        first = False
H.append("</table></div>")

H.append("<h3>" + BI("7.2 满足工期的候选 —— 按报价排序", "7.2 Schedule-Compliant Candidates — by Price") + "</h3>")
H.append("<table class='t'><tr><th>" + BI("项目", "Project") + "</th><th>" + BI("排名", "Rank") + "</th>"
         "<th>" + BI("供应商", "Supplier") + "</th><th class='n'>" + BI("报价", "Quote") + "</th>"
         "<th class='n'>" + BI("完成日", "Completion") + "</th></tr>")
pick_row = {}
for p in PROJECTS:
    pid = p["id"]
    cand = sorted([k for k in RECV_KEYS if satisfied(k, pid)], key=lambda k: QUOTES[k][pid]["total"])
    if not cand:
        cand = sorted(RECV_KEYS, key=lambda k: QUOTES[k][pid]["total"])
    pick_row[pid] = (cand[0], QUOTES[cand[0]][pid]["total"])
    for i, k in enumerate(cand, 1):
        H.append("<tr%s><td>%s</td><td>%s</td><td><span class='pill' style='background:%s'>%s</span></td>"
                 "<td class='n'><b>%s</b></td><td class='n'>%s</td></tr>"
                 % (" class='rec-row'" if i == 1 else "", esc(p["name"]) if i == 1 else "",
                    "① 最低" if i == 1 else "②③④"[i - 2], SUPMAP[k]["color"], esc(SUPMAP[k]["name"]),
                    euro(QUOTES[k][pid]["total"]), lead_result(k, pid)["est"].isoformat()))
H.append("</table>")

H.append("<h3>" + BI("7.3 定标推荐结论", "7.3 Recommended Award") + "</h3>")
_alt = {}
for p in PROJECTS:
    pid = p["id"]
    cand = sorted([k for k in RECV_KEYS if satisfied(k, pid) and k != pick_row[pid][0]], key=lambda k: QUOTES[k][pid]["total"])
    _alt[pid] = (cand[0], QUOTES[cand[0]][pid]["total"]) if cand else pick_row[pid]
for p in PROJECTS:
    pid = p["id"]; wk, wv = pick_row[pid]; ak, av = _alt[pid]
    H.append("<div class='pick win'><div class='ph'><b>%s　→　%s</b><span class='amt'>%s</span></div>%s</div>"
             % (esc(p["name"]), esc(SUPMAP[wk]["name"]), euro(wv),
                BI("满足工期（%s 完成）+ 满足工期者中报价最低 → <b>推荐</b>。备选：%s %s。"
                   % (lead_result(wk, pid)["est"].isoformat(), esc(SUPMAP[ak]["name"]), euro(av)),
                   "Schedule-compliant (completes %s) and lowest among compliant bidders → <b>recommended</b>. Back-up: %s %s."
                   % (lead_result(wk, pid)["est"].isoformat(), esc(SUPMAP[ak]["name"]), euro(av)))))
H.append("<div class='note ok'>" + BI(
    "<b>各项目推荐（分项目独立定标，不做跨项目合计）：</b><br>"
    + "".join("· %s → %s %s（备选 %s %s）<br>" % (esc(p["name"]), esc(SUPMAP[pick_row[p["id"]][0]]["name"]),
                                                   euro(pick_row[p["id"]][1]), esc(SUPMAP[_alt[p["id"]][0]]["name"]), euro(_alt[p["id"]][1]))
              for p in PROJECTS),
    "<b>Per-project recommendations (awarded per project, no combined total):</b><br>"
    + "".join("· %s → %s %s (back-up %s %s)<br>" % (esc(p["name"]), esc(SUPMAP[pick_row[p["id"]][0]]["name"]),
                                                     euro(pick_row[p["id"]][1]), esc(SUPMAP[_alt[p["id"]][0]]["name"]), euro(_alt[p["id"]][1]))
              for p in PROJECTS)) + "</div>")

H.append("<h3>" + BI("7.4 需请对方澄清（工期不满足）", "7.4 To Be Clarified — Schedule") + "</h3>")
H.append("<table class='t'><tr><th>" + BI("供应商", "Supplier") + "</th><th>" + BI("项目", "Project") + "</th>"
         "<th class='n'>" + BI("完成日", "Completion") + "</th><th class='n'>" + BI("超出天数", "Days late") + "</th></tr>")
_cl = 0
for p in PROJECTS:
    for k in RECV_KEYS:
        lr = lead_result(k, p["id"])
        if lr["ok"]:
            continue
        _cl += 1
        H.append("<tr><td><span class='pill' style='background:%s'>%s</span></td><td>%s</td><td class='n'>%s</td><td class='n'><b>%d %s</b></td></tr>"
                 % (SUPMAP[k]["color"], esc(SUPMAP[k]["name"]), esc(p["name"]), lr["est"].isoformat(),
                    (lr["est"] - LEAD_DEADLINE).days, BI("天", "d")))
if _cl == 0:
    H.append("<tr><td colspan='4' class='na'>" + BI("全部候选均满足工期", "All candidates meet the schedule") + "</td></tr>")
H.append("</table>")

H.append("<h3>" + BI("7.5 定标前置条件", "7.5 Pre-conditions Before Award") + "</h3><ol>")
H.append("<li>" + BI("第五节全部 P0 项书面闭环后方可定标；澄清通过前不按当前价格定标。",
                      "Award only after all P0 items in §5 are closed in writing.") + "</li>")
H.append("<li>" + BI("起算日统一定义：需确认各家起算日 ≤ %s，否则上表完成日不成立。" % LEAD_START.isoformat(),
                      "Unified start date: confirm each start ≤ %s, otherwise the completion dates above do not hold." % LEAD_START.isoformat()) + "</li>")
H.append("</ol>")

H.append("<h2>" + BI("八、扩容说明", "8. How to Extend") + "</h2>")
H.append("<div class='note info'>" + BI(
    "数据层与渲染层分离：<b>改报价只动 QUOTES 数值；新增供应商往 SUPPLIERS 加 dict + QUOTES 补条目 + TERMS/TRANS_NOTE/LEAD_* 补列</b>，"
    "本页所有表格、最低标高亮、工期判定、定标结论自动重算；Excel 版（gen_excel.py）共用同一数据层，同步更新。",
    "Data/render separation: <b>a revised quote only changes QUOTES; a new supplier means appending to SUPPLIERS plus entries in QUOTES / TERMS / TRANS_NOTE / LEAD_*</b> — "
    "all tables, highlights, schedule checks and the award conclusion recompute automatically. The Excel generator (gen_excel.py) shares this data layer and updates in sync.") + "</div>")

H.append("<div class='foot'>" + BI(
    "注：所有数字直接取自各家报价原文，未做补全或估算；勾稽 Unit+Transport+Install == Total 已校验（见运行日志）。",
    "Note: all figures are taken directly from the quotes with no filling-in or estimation; reconciliation (Produce+Transport+Install == Total) is verified (see run log).") + "</div>")

H.append("""</div><script>
/* 仅用于记住语言；切换本身由 CSS radio + :has() 完成，禁用脚本也能用 */
(function(){var K='board_lang';function ap(l){var r=document.getElementById(l==='en'?'len':'lzh');if(r)r.checked=true;document.body.className='lang-'+l;try{localStorage.setItem(K,l)}catch(e){}}
var rs=document.getElementsByName('lang');for(var i=0;i<rs.length;i++){rs[i].addEventListener('change',function(){ap(this.id==='len'?'en':'zh')})}
try{var s=localStorage.getItem(K);if(s==='en'||s==='zh')ap(s)}catch(e){}})();
</script></body></html>""")

_out = "board.html"
open(_out, "w", encoding="utf-8").write("".join(H))
print("WROTE %s  bytes=%d" % (_out, os.path.getsize(_out)))
