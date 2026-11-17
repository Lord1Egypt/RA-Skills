#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""留学助理 skill — 输出渲染（markdown）。"""
from datetime import date

TIER_CN = {"reach": "冲刺", "match": "匹配", "safety": "保底", "example": "示例"}


def render_assess(d: dict) -> str:
    s = d["scores"]
    lines = [
        f"## 竞争力画像（综合 {d['total']}/100 · 参考档位 {TIER_CN.get(d['tier'], d['tier'])})",
        "",
        "| 维度 | 得分 | 依据 |", "|---|---|---|",
    ]
    for k, v in s.items():
        basis = d.get("rationale", {}).get(k, "")
        lines.append(f"| {k} | {v} | {basis} |")
    if d["shortboards"]:
        lines += ["", "**短板与建议：**", ""]
        for sb in d["shortboards"]:
            lines.append(f"- **{sb['dimension']}** ({sb['score']}): {sb['reason']}")
    lines += ["", "**下一步：**"]
    for n in d["next_steps"]:
        lines.append(f"- {n}")
    lines.append("")
    lines.append(f"> 引擎模式: {d.get('llm_mode', 'mock')} · 仅供参考，不构成录取承诺")
    return "\n".join(lines)


def _gre_cn(v):
    return {"not_required": "不需GRE", "optional": "GRE可选", "required": "需GRE"}.get(v) or "GRE待查"


def render_schools(d: dict) -> str:
    lines = [f"## 选校清单（模式: {'个性化' if d['mode']=='profile' else '通用框架'}）", ""]
    if d["mode"] == "profile":
        lines.append(f"竞争力档位: {d['competitiveness']}")
    cur = None
    for i in d["items"]:
        if i["tier"] != cur:
            cur = i["tier"]
            lines.append(f"\n### {TIER_CN.get(cur, cur)}")
        conn = "📌 " if i.get("connection") else ""
        safe = "🛡" if i.get("safeFriendly") else ""
        lines.append(f"- {conn}{safe}{i['school']} · {i['program']}"
                     + (f"（匹配 {i.get('match', '')}）" if i.get("match") is not None else "")
                     + f"  [{_gre_cn(i.get('gre'))}]"
                     + f"  {i.get('sourceUrl', '')}")
    lines.append("\n> 以官网为准；deadline/学费/录取率待核实；GRE 要求为公开资料倾向，以官网为准。")
    return "\n".join(lines)


def render_professors(d: dict) -> str:
    lines = [f"## 教授短名单（竞争力档位: {d['competitiveness']}）", ""]
    cur = None
    for i in d["items"]:
        if i["tier"] != cur:
            cur = i["tier"]
            lines.append(f"\n### {TIER_CN.get(cur, cur)}")
        lines.append(f"- {i['school']} · {i['name']}（{i['field']}）  [方向匹配 {i['match']}]")
        lines.append(f"  topics: {', '.join(i['topics'])}")
        lines.append(f"  {i['sourceUrl']}")
    lines.append("\n> 教授姓名为占位（待按 faculty 页核实）；以各系官网为准。")
    return "\n".join(lines)


def render_feedback(d: dict) -> str:
    lines = [f"## 文书逐段反馈（来源: {d['source']}）", ""]
    if not d["comments"]:
        lines.append("未发现问题。")
    for c in d["comments"]:
        sev = {"high": "🔴", "mid": "🟡", "low": "🟢"}.get(c["severity"], "⚪")
        lines.append(f"- {sev} **{c['text']}**（{c['severity']}）")
        lines.append(f"  → {c['suggestion']}")
    lines.append("")
    lines.append(f"> {d.get('note', '')}")
    if d.get("source") == "mock":
        lines.append("> ⚠️ 这是引擎兜底模板（引擎未配 LLM）。在对话中可让助手直接基于你的背景生成更高质量的反馈。")
    return "\n".join(lines)


def render_outreach(d: dict) -> str:
    lines = [
        f"## 套磁草稿（来源: {d['source']}）", "",
        f"**Subject:** {d['subject']}", "",
        "```", d["body"], "```", "",
        "**发送前检查：**",
    ]
    for t in d.get("tips", []):
        lines.append(f"- {t}")
    lines.append("")
    lines.append(f"> {d.get('note', '')}")
    if d.get("source") == "mock":
        lines.append("> ⚠️ 这是引擎兜底模板（引擎未配 LLM）。在对话中可让助手直接基于你的背景和教授方向生成更高质量版本。")
    return "\n".join(lines)


def render_profile(d: dict) -> str:
    p = d.get("profile") or {}
    lines = [f"## 申请人档案（{d.get('identity', 'anon')}）", ""]
    if not p:
        lines.append("（空）用 `guide.py profile update --gpa 3.9 --direction \"ai,ml\" ...` 逐步建立。")
        return "\n".join(lines)
    rows = [
        ("gpa", p.get("gpa")), ("toefl", p.get("toefl")), ("gre", p.get("gre")),
        ("目标学位", p.get("targetDegree")), ("学科", p.get("disciplines")),
        ("方向", p.get("direction")), ("连接校", p.get("school_ids")),
    ]
    for k, v in rows:
        if v is not None:
            lines.append(f"- **{k}**: {v}")
    if p.get("research"):
        lines.append(f"- **科研** ({len(p['research'])} 段): " + "; ".join(
            f"{r.get('topic','')} {'·'+str(r.get('output',''))[:20] if r.get('output') else ''}" for r in p["research"]))
    if p.get("intern"):
        lines.append(f"- **实习** ({len(p['intern'])} 段): " + "; ".join(
            f"{i.get('company','')} {i.get('role','')}" for i in p["intern"]))
    lines.append("")
    lines.append("> 档案为多轮对话累积结果；画像/选校自动采用（请求参数优先覆盖）。")
    return "\n".join(lines)


def render_apps(d: dict) -> str:
    items = d.get("items", [])
    summ = d.get("summary", {})
    lines = [f"## 申请清单（共 {summ.get('total', 0)} 条 · 14 天内截止 {summ.get('urgent', 0)} 条）", ""]
    if summ.get("countdown"):
        lines.append("**deadline 倒计时：**")
        for c in summ["countdown"]:
            flag = "🔴" if c.get("urgent") else "⬜"
            lines.append(f"- {flag} {c['school']} {c['program']}（{c['deadline']}，剩 {c['days']} 天）")
    if items:
        lines += ["", "**清单：**"]
        for it in items:
            extra = f"（deadline {it['deadline']}）" if it.get("deadline") else ""
            lines.append(f"- [{it['status']}] {it['school']} {it['program']}{extra}")
            if it.get("notes"):
                lines.append(f"  ↳ {it['notes']}")
    else:
        lines.append("（空）用 `guide.py apps add --program ... --school ... --deadline ...` 添加。")
    return "\n".join(lines)


def render_report(d: dict) -> str:
    lines = [f"## {d['title']}", ""]
    for sec in d["sections"]:
        lines.append(f"### {sec['heading']}")
        if sec.get("table"):
            cols = list(sec["table"][0].keys())
            lines.append("| " + " | ".join(cols) + " |")
            lines.append("|" + "---|" * len(cols))
            for row in sec["table"]:
                lines.append("| " + " | ".join(str(row.get(c, "")) for c in cols) + " |")
        elif sec.get("content"):
            lines.append(sec["content"])
        lines.append("")
    return "\n".join(lines)


def render_plan(d: dict) -> str:
    p = d.get("plan")
    if not p:
        return f"## 申请计划\n\n尚未生成本季计划（{d.get('season')}）。先运行 `guide.py plan --season <年份>` 生成。"
    prog = d.get("progress", {})
    lines = [
        f"## 申请计划 · {p['season']}",
        "",
        f"**总体进度: {prog.get('done', 0)}/{prog.get('total', 0)} 完成（{prog.get('rate', 0)}%）**",
        f"> 今日: {p.get('today')} · 生成于: {p['created_at'][:10]}", "",
    ]
    today = date.today()
    for ph in p["phases"]:
        n_done = sum(1 for t in ph["tasks"] if t["status"] == "done")
        n_total = len(ph["tasks"])
        # 最近/逾期任务
        tasks = []
        for t in sorted(ph["tasks"], key=lambda x: x["due"]):
            mark = "✅" if t["status"] == "done" else ("🔶" if t["status"] == "in_progress" else "⬜")
            if t.get("overdue"):
                mark = "⏰"
            tasks.append(f"{mark} {t['title']}（{t['due']}，剩 {t['countdown']} 天）")
        lines.append(f"### {ph['name']} [{n_done}/{n_total}]")
        lines.append(f"> 窗口: {ph['window'][0]} ~ {ph['window'][1]} · 里程碑: {ph['milestone']}")
        lines.extend("- " + t for t in tasks)
        lines.append("")
    lines.append("> 使用 `guide.py done --task <id> --season <年份>` 标记完成；`guide.py status` 查看进度。")
    return "\n".join(lines)
