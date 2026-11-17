"""Offline dashboard and dependency-free XLSX export."""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import sqlite3
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable
from xml.sax.saxutils import escape as xml_escape


def _json(value: Any, default: Any) -> Any:
    try:
        return json.loads(value) if value else default
    except (TypeError, json.JSONDecodeError):
        return default


def _date(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def _local_day(value: str) -> str:
    """把 UTC ISO 时间转为 Asia/Shanghai 自然日 YYYY-MM-DD。"""
    parsed = _date(value)
    if not parsed:
        return ""
    return (parsed + dt.timedelta(hours=8)).date().isoformat()


def _yuan(micros: int) -> str:
    return f"{micros / 1_000_000:.6f}".rstrip("0").rstrip(".") or "0"


class Money(float):
    pass


def dashboard_payload(conn: sqlite3.Connection, recent_days: int) -> dict[str, Any]:
    rows = conn.execute(
        """SELECT ar.*,a.name AS configured_name,a.account_name,a.groups_json
           FROM articles ar JOIN accounts a ON a.id=ar.account_id
           ORDER BY ar.publish_timestamp DESC,ar.first_seen_at DESC LIMIT 2000"""
    ).fetchall()
    accounts = conn.execute(
        """SELECT a.id,a.name,a.account_name,a.groups_json,a.last_success_at,a.last_error,
           COUNT(ar.article_id) AS article_count,
           SUM(CASE WHEN ar.is_baseline=0 THEN 1 ELSE 0 END) AS incremental_count,
           SUM(CASE WHEN ar.analysis_status='analyzed' THEN 1 ELSE 0 END) AS analyzed_count,
           MAX(ar.publish_timestamp) AS latest_timestamp
           FROM accounts a LEFT JOIN articles ar ON ar.account_id=a.id WHERE a.enabled=1
           GROUP BY a.id ORDER BY article_count DESC,a.name"""
    ).fetchall()
    calls = conn.execute(
        """SELECT endpoint,called_at,status_code,charge_micros,duration_ms,succeeded,error_code
           FROM api_calls ORDER BY called_at DESC LIMIT 500"""
    ).fetchall()
    billing = conn.execute(
        "SELECT COUNT(*) AS count,COALESCE(SUM(charge_micros),0) AS charge FROM api_calls WHERE succeeded=1"
    ).fetchone()
    now = dt.datetime.now(dt.timezone.utc)
    topic_counter: Counter[str] = Counter()
    daily_counter: Counter[str] = Counter()
    article_items: list[dict[str, Any]] = []
    analyzed = 0
    incremental = 0
    today_count = 0
    seven_days = 0
    for row in rows:
        topics = _json(row["topics_json"], [])
        topic_counter.update(str(topic) for topic in topics if str(topic).strip())
        published = _date(row["publish_time"])
        if not published and row["publish_timestamp"]:
            published = dt.datetime.fromtimestamp(row["publish_timestamp"], dt.timezone.utc)
        if published:
            local_day = (published + dt.timedelta(hours=8)).date().isoformat()
            daily_counter[local_day] += 1
            today = (now + dt.timedelta(hours=8)).date()
            published_day = (published.astimezone(dt.timezone.utc) + dt.timedelta(hours=8)).date()
            if published_day == today:
                today_count += 1
            if 0 <= (today - published_day).days < 7:
                seven_days += 1
        if row["analysis_status"] == "analyzed":
            analyzed += 1
        if not row["is_baseline"]:
            incremental += 1
        article_items.append({
            "id": row["article_id"],
            "account": row["account_name"] or row["configured_name"],
            "groups": _json(row["groups_json"], []),
            "title": row["title"],
            "digest": row["digest"],
            "publishTime": row["publish_time"],
            "url": row["url"],
            "topics": topics,
            "summary": row["summary"],
            "keyPoints": _json(row["key_points_json"], []),
            "keyData": _json(row["key_data_json"], []),
            "logic": row["logic"],
            "sentiment": row["sentiment"],
            "importance": row["importance"],
            "changeNotes": row["change_notes"],
            "risks": _json(row["risks_json"], []),
            "status": row["analysis_status"],
            "isBaseline": bool(row["is_baseline"]),
        })
    start = (now + dt.timedelta(hours=8)).date() - dt.timedelta(days=max(7, recent_days) - 1)
    daily = []
    for index in range(max(7, recent_days)):
        day = (start + dt.timedelta(days=index)).isoformat()
        daily.append({"date": day, "count": daily_counter[day]})
    # --- 聚合分析层数据：跨号话题对比 / 主题追踪 / 每日摘要 / 公众号立场画像 ---
    cross_topic_compare = []
    topic_tracking = []
    for row in conn.execute(
        """SELECT topic,article_count,account_count,account_positions_json,last_seen_at
           FROM topic_groups WHERE article_count>=2 ORDER BY article_count DESC,last_seen_at DESC LIMIT 30"""
    ).fetchall():
        positions = _json(row["account_positions_json"], [])
        if len({p.get("account") for p in positions}) < 2:
            continue  # 仅单号不构成"跨号对比"
        cross_topic_compare.append({
            "topic": row["topic"], "articleCount": row["article_count"], "accountCount": row["account_count"],
            "lastSeen": row["last_seen_at"],
            "positions": positions[:12],
        })
        # 主题追踪时间线：按该主题文章的入库日聚合账号与立场
        timeline = {}
        for p in positions:
            day = _local_day(p.get("publishTime", ""))
            if not day:
                continue
            entry = timeline.setdefault(day, {"date": day, "accounts": [], "stances": set()})
            if p.get("account") and p["account"] not in entry["accounts"]:
                entry["accounts"].append(p["account"])
            if p.get("stance"):
                entry["stances"].add(p["stance"])
        topic_tracking.append({
            "topic": row["topic"],
            "timeline": [{"date": k, "accounts": v["accounts"], "stances": sorted(v["stances"])} for k, v in
                         sorted(timeline.items(), key=lambda kv: kv[0], reverse=True)],
        })
    # 每日摘要（最近一份）
    daily_brief = None
    brief_row = conn.execute(
        "SELECT brief_date,payload_json FROM daily_briefs ORDER BY brief_date DESC LIMIT 1"
    ).fetchone()
    if brief_row:
        daily_brief = _json(brief_row["payload_json"], {})
        daily_brief["date"] = brief_row["brief_date"]
    # 公众号立场画像
    account_profiles = []
    for row in conn.execute(
        """SELECT a.name AS account_name,ar.topics_json,ar.stance FROM articles ar JOIN accounts a ON a.id=ar.account_id
           WHERE ar.analysis_status='analyzed' ORDER BY a.name"""
    ).fetchall():
        topics = _json(row["topics_json"], [])
        stance = row["stance"] or "informational"
        account_profiles.append({"account": row["account_name"], "topics": topics, "stance": stance})
    profile_map = {}
    for item in account_profiles:
        account = item["account"]
        if account not in profile_map:
            profile_map[account] = {"account": account, "topics": Counter(), "stances": Counter()}
        for topic in item["topics"]:
            profile_map[account]["topics"][topic] += 1
        profile_map[account]["stances"][item["stance"]] += 1
    account_profiles = [
        {"account": account, "topics": [{"name": t, "count": c} for t, c in data["topics"].most_common(8)],
         "stances": [{"stance": s, "count": c} for s, c in data["stances"].most_common()]}
        for account, data in sorted(profile_map.items())
    ]
    return {
        "generatedAt": now.isoformat(),
        "metrics": {
            "accountCount": len(accounts), "articleCount": len(rows), "incrementalCount": incremental,
            "analyzedCount": analyzed, "todayCount": today_count, "sevenDayCount": seven_days,
            "apiCallCount": billing["count"], "actualCostYuan": _yuan(billing["charge"]),
        },
        "accounts": [
            {"id": row["id"], "name": row["account_name"] or row["name"], "groups": _json(row["groups_json"], []),
             "articleCount": row["article_count"] or 0, "incrementalCount": row["incremental_count"] or 0,
             "analyzedCount": row["analyzed_count"] or 0, "latestTimestamp": row["latest_timestamp"] or 0,
             "lastSuccessAt": row["last_success_at"] or "", "lastError": row["last_error"] or ""}
            for row in accounts
        ],
        "topics": [{"name": name, "count": count} for name, count in topic_counter.most_common(20)],
        "daily": daily,
        "articles": article_items,
        "calls": [dict(row) for row in calls],
        "crossTopicCompare": cross_topic_compare,
        "topicTracking": topic_tracking,
        "dailyBrief": daily_brief,
        "accountProfiles": account_profiles,
    }


def build_dashboard(conn: sqlite3.Connection, config: dict[str, Any], target: Path) -> None:
    recent_days = int(config.get("dashboard", {}).get("recentDays", 30) or 30)
    payload = dashboard_payload(conn, max(7, min(90, recent_days)))
    title = html.escape(str(config.get("title") or "公众号情报分析系统"))
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    document = DASHBOARD_HTML.replace("__TITLE__", title).replace("__PAYLOAD__", serialized)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(document, encoding="utf-8", newline="\n")


DASHBOARD_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="color-scheme" content="light"><title>__TITLE__</title>
  <style>
    :root{--ink:#172321;--muted:#687471;--line:#dfe5e3;--surface:#fff;--wash:#f3f6f5;--green:#087f73;--green2:#075c55;--amber:#b66b16;--red:#b43b3b;--blue:#286b9e}
    *{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--wash);font:14px/1.55 "Microsoft YaHei UI","PingFang SC",system-ui,sans-serif;letter-spacing:0}
    button,input,select{font:inherit}.shell{min-height:100vh}.topbar{position:sticky;z-index:20;top:0;color:#fff;background:#1e2b29;border-bottom:3px solid #35a094}
    .topbar-inner,.content{width:min(1460px,calc(100% - 40px));margin:auto}.topbar-inner{display:flex;min-height:68px;align-items:center;justify-content:space-between;gap:20px}
    h1,h2,h3,p{margin:0}.brand h1{font-size:20px}.brand p{margin-top:2px;color:#b9c8c5;font-size:12px}.stamp{color:#c8d4d2;font-size:12px;text-align:right}
    .content{padding:24px 0 40px}.metrics{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));background:var(--surface);border:1px solid var(--line)}
    .metric{min-width:0;padding:18px 20px}.metric+.metric{border-left:1px solid var(--line)}.metric span{display:block;color:var(--muted);font-size:12px}.metric strong{display:block;margin-top:6px;font-size:25px;line-height:1.2}.metric.cost strong{color:var(--green2)}
    .band{margin-top:18px;background:var(--surface);border:1px solid var(--line)}.band-head{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:15px 18px;border-bottom:1px solid var(--line)}
    .band-head h2{font-size:16px}.band-head span{color:var(--muted);font-size:12px}.charts{display:grid;grid-template-columns:1.35fr 1fr 1fr}.chart{min-width:0;padding:18px}.chart+.chart{border-left:1px solid var(--line)}.chart h3{margin-bottom:14px;font-size:13px}
    .daily{display:flex;height:180px;align-items:flex-end;gap:5px;border-bottom:1px solid var(--line)}.day{position:relative;flex:1;min-width:3px;background:#92c9c2}.day:hover{background:var(--green)}.day span{display:none;position:absolute;bottom:calc(100% + 5px);left:50%;padding:3px 5px;transform:translateX(-50%);color:#fff;background:#24302f;font-size:11px;white-space:nowrap}.day:hover span{display:block}
    .bars{display:grid;gap:10px}.bar-row{display:grid;grid-template-columns:minmax(90px,140px) 1fr 34px;align-items:center;gap:9px}.bar-label{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.bar-track{height:8px;background:#edf1f0}.bar-fill{height:100%;background:var(--green)}.bar-count{color:var(--muted);font-size:12px;text-align:right}
    .alerts{display:grid;gap:8px}.alert{padding:9px 10px;border-left:3px solid var(--green);background:#f3f8f7}.alert.error{border-color:var(--red);background:#fff5f5}.alert strong,.alert span{display:block}.alert span{margin-top:2px;color:var(--muted);font-size:12px}
    .toolbar{display:grid;grid-template-columns:minmax(220px,1fr) repeat(3,minmax(130px,190px)) auto;gap:9px;padding:13px 18px;border-bottom:1px solid var(--line)}
    .control{width:100%;height:36px;padding:0 10px;color:var(--ink);background:#fff;border:1px solid #cfd7d5;border-radius:4px}.btn{height:36px;padding:0 14px;color:#fff;background:var(--green);border:0;border-radius:4px;cursor:pointer}.btn:hover{background:var(--green2)}
    .table-wrap{overflow:auto}.table{width:100%;min-width:1050px;border-collapse:collapse}.table th,.table td{padding:12px 14px;border-bottom:1px solid #edf0ef;text-align:left;vertical-align:top}.table th{position:sticky;z-index:1;top:0;color:#53605d;background:#f7f9f8;font-size:12px}.table td{font-size:13px}.title-link{color:#075f58;font-weight:650;text-decoration:none}.title-link:hover{text-decoration:underline}.sub{display:block;margin-top:4px;color:var(--muted);font-size:12px}.tags{display:flex;flex-wrap:wrap;gap:4px}.tag{padding:1px 5px;color:#34534f;background:#eaf4f2;border:1px solid #d2e8e4;border-radius:3px;font-size:11px}.importance{font-weight:700}.i5{color:var(--red)}.i4{color:var(--amber)}.summary{max-width:500px}.empty{padding:40px;color:var(--muted);text-align:center}.foot{padding:13px 18px;color:var(--muted);font-size:12px}
    @media(max-width:1100px){.metrics{grid-template-columns:repeat(3,1fr)}.metric:nth-child(4){border-left:0;border-top:1px solid var(--line)}.metric:nth-child(n+5){border-top:1px solid var(--line)}.charts{grid-template-columns:1fr 1fr}.chart:last-child{grid-column:1/-1;border-top:1px solid var(--line);border-left:0}.toolbar{grid-template-columns:1fr 1fr 1fr}.toolbar .search{grid-column:1/-1}.toolbar .btn{width:100%}}
    @media(max-width:700px){.topbar-inner,.content{width:min(100% - 24px,1460px)}.topbar-inner{min-height:62px}.stamp{display:none}.content{padding-top:12px}.metrics{grid-template-columns:1fr 1fr}.metric{padding:14px}.metric:nth-child(odd){border-left:0}.metric:nth-child(n+3){border-top:1px solid var(--line)}.metric strong{font-size:21px}.charts{grid-template-columns:1fr}.chart+.chart,.chart:last-child{grid-column:auto;border-top:1px solid var(--line);border-left:0}.toolbar{grid-template-columns:1fr}.toolbar .search{grid-column:auto}.band-head{align-items:flex-start;flex-direction:column}.daily{height:130px}}
  </style>
</head>
<body><div class="shell">
  <header class="topbar"><div class="topbar-inner"><div class="brand"><h1>__TITLE__</h1><p>公众号增量监控 · AI 分析 · 成本留痕</p></div><div id="stamp" class="stamp"></div></div></header>
  <main class="content">
    <section id="metrics" class="metrics"></section>
    <section class="band"><div class="band-head"><h2>情报概览</h2><span>统计范围来自本地增量资料库</span></div><div class="charts"><div class="chart"><h3>近 30 日更新</h3><div id="daily" class="daily"></div></div><div class="chart"><h3>公众号产出</h3><div id="accounts" class="bars"></div></div><div class="chart"><h3>主题分布</h3><div id="topics" class="bars"></div></div></div></section>
    <section class="band"><div class="band-head"><h2>每日摘要</h2><span id="brief-date"></span></div><div id="daily-brief" class="chart"></div></section>
    <section class="band"><div class="band-head"><h2>跨号话题对比</h2><span>同一主题不同公众号的立场与侧重点</span></div><div id="cross-topic" class="topic-grid"></div></section>
    <section class="band"><div class="band-head"><h2>主题追踪</h2><span>近期谁在持续讨论某主题</span></div><div id="topic-tracking" class="chart"></div></section>
    <section class="band"><div class="band-head"><h2>公众号立场画像</h2><span>各账号聚焦主题与立场倾向</span></div><div id="account-profiles" class="chart"></div></section>
    <section class="band"><div class="band-head"><h2>监控状态</h2><span id="account-summary"></span></div><div id="alerts" class="chart alerts"></div></section>
    <section class="band"><div class="band-head"><h2>文章情报库</h2><span id="result-count"></span></div><div class="toolbar"><input id="search" class="control search" placeholder="搜索标题、摘要、观点、数据"><select id="account-filter" class="control"><option value="">全部公众号</option></select><select id="topic-filter" class="control"><option value="">全部主题</option></select><select id="importance-filter" class="control"><option value="0">全部重要度</option><option value="4">重要度 4+</option><option value="5">仅重要度 5</option></select><button id="download" class="btn">导出筛选 CSV</button></div><div class="table-wrap"><table class="table"><thead><tr><th>时间 / 公众号</th><th>文章</th><th>主题</th><th>重要度</th><th>AI 摘要与变化</th></tr></thead><tbody id="article-body"></tbody></table></div><div id="empty" class="empty" hidden>没有符合条件的文章</div><div class="foot">AI 结果用于减少重复阅读；关键数据与判断请打开原文复核。</div></section>
  </main>
</div><script>const DATA=__PAYLOAD__;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const date=v=>{if(!v)return '-';const d=new Date(v);return Number.isNaN(d.getTime())?v:d.toLocaleString('zh-CN',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'})};
document.getElementById('stamp').textContent='更新于 '+date(DATA.generatedAt);
const m=DATA.metrics;document.getElementById('metrics').innerHTML=[['监控公众号',m.accountCount],['今日文章',m.todayCount],['近 7 日文章',m.sevenDayCount],['增量入库',m.incrementalCount],['已完成分析',m.analyzedCount],['累计接口费用','¥'+m.actualCostYuan,'cost']].map(x=>`<div class="metric ${x[2]||''}"><span>${x[0]}</span><strong>${x[1]}</strong></div>`).join('');
const dailyMax=Math.max(1,...DATA.daily.map(x=>x.count));document.getElementById('daily').innerHTML=DATA.daily.map(x=>`<div class="day" style="height:${Math.max(x.count?4:1,x.count/dailyMax*100)}%"><span>${x.date} · ${x.count} 篇</span></div>`).join('');
function bars(id,items,label){const max=Math.max(1,...items.map(x=>x.count));document.getElementById(id).innerHTML=items.slice(0,10).map(x=>`<div class="bar-row"><span class="bar-label" title="${esc(x.name)}">${esc(x.name)}</span><span class="bar-track"><span class="bar-fill" style="width:${x.count/max*100}%"></span></span><span class="bar-count">${x.count}</span></div>`).join('')||`<span class="sub">暂无${label}</span>`}
bars('accounts',DATA.accounts.map(x=>({name:x.name,count:x.articleCount})),'数据');bars('topics',DATA.topics,'主题');
const stanceLabel={'support':'利好','question':'质疑','neutral':'中立','informational':'通报'};
const stanceEls=v=>`<span class="stance ${esc(v)}">${stanceLabel[v]||v}</span>`;
// 每日摘要
(function(){const b=DATA.dailyBrief;const el=document.getElementById('daily-brief');if(!b){el.innerHTML='<span class="sub" style="padding:16px 18px">暂无每日摘要，请先运行 make-brief 生成。</span>';document.getElementById('brief-date').textContent='';return;}
document.getElementById('brief-date').textContent=b.date+' · 今日已分析 '+((b.metrics||{}).todayAnalyzed??0)+' 篇';
let html='';
if(b.keyArticles&&b.keyArticles.length){html+='<div class="brief-sec"><h3>今日重点文章</h3>'+b.keyArticles.map(a=>`<div class="brief-item"><a class="title-link" href="${esc(a.url)}" target="_blank" rel="noreferrer">${esc(a.title)}</a><span class="sub">${esc(a.account)} · 重要度 ${a.importance}/5 ${stanceEls(a.stance)}</span>${a.summary?`<span class="sub">${esc(a.summary)}</span>`:''}</div>`).join('')+'</div>';}
if(b.keyData&&b.keyData.length){html+='<div class="brief-sec"><h3>今日关键数据</h3><div class="brief-data">'+b.keyData.map(d=>`<span class="tag">${esc(d)}</span>`).join('')+'</div></div>';}
if(b.risks&&b.risks.length){html+='<div class="brief-sec"><h3>待核实风险</h3>'+b.risks.map(r=>`<div class="brief-item brief-risk"><strong>${esc(r.title)}</strong><span class="sub">${esc(r.account)} · ${esc(r.risk)}</span></div>`).join('')+'</div>';}
if(b.accountPulse&&b.accountPulse.length){html+='<div class="brief-sec"><h3>各号更新节奏</h3><div class="pulse-grid">'+b.accountPulse.map(p=>`<div class="pulse-card"><strong>${esc(p.account)}</strong><span>今日 ${p.today} 篇 · 近7日 ${p.last7} 篇</span></div>`).join('')+'</div></div>';}
el.innerHTML=html||'<span class="sub" style="padding:16px 18px">今日暂无已分析文章。</span>';})();
// 跨号话题对比
(function(){const el=document.getElementById('cross-topic');if(!DATA.crossTopicCompare.length){el.innerHTML='<span class="sub" style="padding:16px 18px;grid-column:1/-1">暂无跨号同主题文章（需≥2个公众号讨论同一主题）。</span>';return;}
el.innerHTML=DATA.crossTopicCompare.map(t=>`<div class="topic-card"><div class="topic-card-head"><h3>${esc(t.topic)}</h3><span>${t.accountCount} 号 · ${t.articleCount} 篇</span></div>${t.positions.map(p=>`<div class="pos"><div class="pos-account"><strong>${esc(p.account)}</strong>${stanceEls(p.stance)}</div>${p.angle?`<div class="pos-angle">${esc(p.angle)}</div>`:''}<div class="pos-summary">${esc(p.summary||'')}</div>${p.keyData&&p.keyData.length?`<div class="pos-summary">数据：${esc(p.keyData.join('；'))}</div>`:''}</div>`).join('')}</div>`).join('');})();
// 主题追踪
(function(){const el=document.getElementById('topic-tracking');if(!DATA.topicTracking.length){el.innerHTML='<span class="sub" style="padding:16px 18px">暂无主题追踪数据。</span>';return;}
el.innerHTML=DATA.topicTracking.map(t=>`<div class="timeline-card"><div class="timeline-title"><strong>${esc(t.topic)}</strong><span class="sub">${t.timeline.length} 个讨论日</span></div>${t.timeline.slice(0,8).map(row=>`<div class="tl-row"><span class="tl-date">${esc(row.date)}</span><span class="tl-acc">${esc(row.accounts.join('、'))}</span><span class="tl-stance">${row.stances.map(stanceEls).join(' ')}</span></div>`).join('')}</div>`).join('');})();
// 公众号立场画像
(function(){const el=document.getElementById('account-profiles');if(!DATA.accountProfiles.length){el.innerHTML='<span class="sub" style="padding:16px 18px">暂无画像数据。</span>';return;}
el.innerHTML='<div class="pulse-grid">'+DATA.accountProfiles.map(p=>`<div class="pulse-card"><strong>${esc(p.account)}</strong><span style="margin-top:6px">立场：${p.stances.map(s=>stanceEls(s.stance)+' ×'+s.count).join(' ')}</span>${p.topics.length?`<span style="margin-top:4px">聚焦：${p.topics.map(t=>`${esc(t.name)}(${t.count})`).join('、')}</span>`:''}</div>`).join('')+'</div>';})();
document.getElementById('account-summary').textContent=`${DATA.accounts.length} 个公众号`;
document.getElementById('alerts').innerHTML=DATA.accounts.map(x=>`<div class="alert ${x.lastError?'error':''}"><strong>${esc(x.name)}</strong><span>${x.lastError?'最近错误：'+esc(x.lastError):`已收录 ${x.articleCount} 篇，已分析 ${x.analyzedCount} 篇，最近成功 ${date(x.lastSuccessAt)}`}</span></div>`).join('')||'<span class="sub">尚未添加公众号</span>';
const accountSelect=document.getElementById('account-filter'),topicSelect=document.getElementById('topic-filter');[...new Set(DATA.articles.map(x=>x.account))].sort().forEach(v=>accountSelect.insertAdjacentHTML('beforeend',`<option>${esc(v)}</option>`));DATA.topics.forEach(x=>topicSelect.insertAdjacentHTML('beforeend',`<option>${esc(x.name)}</option>`));
const fields=['search','account-filter','topic-filter','importance-filter'];fields.forEach(id=>document.getElementById(id).addEventListener(id==='search'?'input':'change',render));
function filtered(){const q=document.getElementById('search').value.trim().toLowerCase(),a=accountSelect.value,t=topicSelect.value,i=Number(document.getElementById('importance-filter').value);return DATA.articles.filter(x=>(!a||x.account===a)&&(!t||x.topics.includes(t))&&(!i||x.importance>=i)&&(!q||[x.title,x.digest,x.summary,x.logic,x.changeNotes,...x.keyPoints,...x.keyData].join(' ').toLowerCase().includes(q)))}
function render(){const rows=filtered();document.getElementById('result-count').textContent=`${rows.length} 篇`;document.getElementById('empty').hidden=rows.length>0;document.getElementById('article-body').innerHTML=rows.map(x=>`<tr><td>${date(x.publishTime)}<span class="sub">${esc(x.account)}</span></td><td><a class="title-link" href="${esc(x.url)}" target="_blank" rel="noreferrer">${esc(x.title||'未命名文章')}</a><span class="sub">${esc(x.digest||'')}</span></td><td><div class="tags">${x.topics.map(v=>`<span class="tag">${esc(v)}</span>`).join('')}</div></td><td><span class="importance i${x.importance}">${x.importance}/5</span><span class="sub">${esc(x.sentiment)}</span></td><td class="summary">${esc(x.summary||'待分析')}${x.changeNotes?`<span class="sub">变化：${esc(x.changeNotes)}</span>`:''}${x.keyData.length?`<span class="sub">数据：${esc(x.keyData.join('；'))}</span>`:''}</td></tr>`).join('')}
document.getElementById('download').addEventListener('click',()=>{const rows=filtered(),header=['发布时间','公众号','标题','主题','重要度','倾向','摘要','变化','文章链接'],csv=[header,...rows.map(x=>[x.publishTime,x.account,x.title,x.topics.join('|'),x.importance,x.sentiment,x.summary,x.changeNotes,x.url])].map(r=>r.map(v=>'"'+String(v??'').replaceAll('"','""')+'"').join(',')).join('\r\n'),blob=new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='公众号情报筛选结果.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),0)});render();</script></body></html>'''


def export_workbook(conn: sqlite3.Connection, target: Path) -> None:
    articles = conn.execute(
        """SELECT ar.*,a.name AS configured_name,a.account_name,a.groups_json FROM articles ar
           JOIN accounts a ON a.id=ar.account_id ORDER BY ar.publish_timestamp DESC,ar.first_seen_at DESC"""
    ).fetchall()
    accounts = conn.execute(
        """SELECT a.name,a.account_name,a.groups_json,a.last_success_at,a.last_error,COUNT(ar.article_id) article_count,
           SUM(CASE WHEN ar.is_baseline=0 THEN 1 ELSE 0 END) incremental_count,
           SUM(CASE WHEN ar.analysis_status='analyzed' THEN 1 ELSE 0 END) analyzed_count,MAX(ar.publish_time) latest_publish
           FROM accounts a LEFT JOIN articles ar ON ar.account_id=a.id GROUP BY a.id ORDER BY article_count DESC"""
    ).fetchall()
    calls = conn.execute(
        """SELECT called_at,endpoint,status_code,succeeded,charge_micros,balance_micros,duration_ms,request_id,error_code,error_message
           FROM api_calls ORDER BY called_at DESC"""
    ).fetchall()
    topic_counts: Counter[str] = Counter()
    account_articles: dict[str, list[list[Any]]] = {}
    article_rows: list[list[Any]] = [[
        "发布时间", "公众号", "分组", "标题", "摘要", "内容类型", "主题", "重要度", "倾向", "AI 摘要",
        "核心观点", "关键数据", "论证逻辑", "变化说明", "风险与待核实", "文章链接", "分析状态", "是否基线",
    ]]
    for row in articles:
        topics = _json(row["topics_json"], [])
        topic_counts.update(topics)
        account_name = row["account_name"] or row["configured_name"]
        account_articles.setdefault(account_name, [["发布时间", "标题", "主题", "重要度", "AI 摘要", "变化说明", "文章链接"]]).append([
            _date(row["publish_time"]), row["title"], " / ".join(topics), row["importance"], row["summary"], row["change_notes"], row["url"],
        ])
        article_rows.append([
            _date(row["publish_time"]), account_name, " / ".join(_json(row["groups_json"], [])),
            row["title"], row["digest"], row["content_type"], " / ".join(topics), row["importance"], row["sentiment"],
            row["summary"], "\n".join(_json(row["key_points_json"], [])), "\n".join(_json(row["key_data_json"], [])),
            row["logic"], row["change_notes"], "\n".join(_json(row["risks_json"], [])), row["url"], row["analysis_status"],
            "是" if row["is_baseline"] else "否",
        ])
    account_rows = [["公众号", "分组", "文章总数", "增量文章", "已分析", "最新文章", "最近同步", "最近错误"]] + [
        [row["account_name"] or row["name"], " / ".join(_json(row["groups_json"], [])), row["article_count"] or 0,
         row["incremental_count"] or 0, row["analyzed_count"] or 0, _date(row["latest_publish"] or ""),
         _date(row["last_success_at"] or ""), row["last_error"] or ""] for row in accounts
    ]
    topic_rows = [["主题", "文章数"]] + [[name, count] for name, count in topic_counts.most_common()]
    call_rows = [["调用时间", "接口", "HTTP 状态", "结果", "实际费用（元）", "扣费后余额（元）", "耗时（毫秒）", "请求 ID", "错误码", "错误信息"]] + [
        [_date(row["called_at"]), row["endpoint"], row["status_code"], "成功" if row["succeeded"] else "失败",
         Money(row["charge_micros"] / 1_000_000), Money(row["balance_micros"] / 1_000_000), row["duration_ms"], row["request_id"],
         row["error_code"], row["error_message"]] for row in calls
    ]
    # --- 聚合分析层 Sheet：跨号话题对比 / 主题追踪 / 每日摘要 ---
    stance_cn = {"support": "利好", "question": "质疑", "neutral": "中立", "informational": "通报"}
    cross_rows = [["主题", "公众号", "立场", "侧重点", "摘要", "关键数据", "文章链接"]]
    for group in conn.execute(
        """SELECT topic,account_positions_json FROM topic_groups WHERE article_count>=2
           ORDER BY article_count DESC,last_seen_at DESC LIMIT 60"""
    ).fetchall():
        positions = _json(group["account_positions_json"], [])
        if len({p.get("account") for p in positions}) < 2:
            continue
        for p in positions:
            cross_rows.append([
                group["topic"], p.get("account", ""), stance_cn.get(p.get("stance", ""), p.get("stance", "")),
                p.get("angle", ""), p.get("summary", ""), "；".join(p.get("keyData", [])), p.get("url", ""),
            ])
    tracking_rows = [["主题", "日期", "讨论公众号", "立场倾向"]]
    for group in conn.execute(
        """SELECT topic,account_positions_json FROM topic_groups ORDER BY article_count DESC,last_seen_at DESC LIMIT 60"""
    ).fetchall():
        timeline = {}
        for p in _json(group["account_positions_json"], []):
            day = _local_day(p.get("publishTime", ""))
            if not day:
                continue
            entry = timeline.setdefault(day, {"accounts": set(), "stances": set()})
            if p.get("account"):
                entry["accounts"].add(p["account"])
            if p.get("stance"):
                entry["stances"].add(p["stance"])
        for day in sorted(timeline, reverse=True):
            tracking_rows.append([
                group["topic"], day, "、".join(timeline[day]["accounts"]),
                "、".join(stance_cn.get(s, s) for s in sorted(timeline[day]["stances"])),
            ])
    brief_rows = [["日期", "公众号", "标题", "主题", "重要度", "摘要", "待核实风险", "文章链接"]]
    brief_row = conn.execute("SELECT brief_date,payload_json FROM daily_briefs ORDER BY brief_date DESC LIMIT 1").fetchone()
    if brief_row:
        brief = _json(brief_row["payload_json"], {})
        for a in brief.get("keyArticles", []):
            brief_rows.append([
                brief_row["brief_date"], a.get("account", ""), a.get("title", ""),
                " / ".join(a.get("topics", [])), a.get("importance", ""), a.get("summary", ""),
                "；".join(a.get("risks", [])), a.get("url", ""),
            ])
    sheets = [
        ("跨号话题对比", cross_rows, [22, 18, 10, 42, 48, 34, 52]),
        ("主题追踪", tracking_rows, [22, 12, 30, 24]),
        ("每日摘要", brief_rows, [12, 16, 40, 22, 10, 48, 40, 52]),
        ("文章明细", article_rows, [20, 16, 14, 36, 42, 12, 18, 10, 10, 48, 42, 32, 42, 42, 42, 52, 14, 10]),
        ("公众号汇总", account_rows, [20, 16, 12, 12, 12, 20, 24, 42]),
        ("主题统计", topic_rows, [24, 12]),
        ("调用成本", call_rows, [24, 46, 12, 10, 16, 18, 14, 34, 18, 42]),
    ]
    used_names = {name for name, _, _ in sheets}
    for account_name, rows in account_articles.items():
        sheets.append((_sheet_name(account_name, used_names), rows, [20, 42, 20, 10, 52, 42, 52]))
    _write_xlsx(target, sheets)


def _sheet_name(value: str, used: set[str]) -> str:
    base = re.sub(r"[\\/?*\[\]:]+", " ", value).strip()[:31] or "未识别公众号"
    name = base
    suffix = 2
    while name in used:
        tag = f" ({suffix})"
        name = base[: max(1, 31 - len(tag))] + tag
        suffix += 1
    used.add(name)
    return name


def _column_name(index: int) -> str:
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def _cell(ref: str, value: Any, header: bool) -> str:
    if isinstance(value, dt.datetime):
        china_time = dt.timezone(dt.timedelta(hours=8))
        local_value = value.astimezone(china_time).replace(tzinfo=None) if value.tzinfo else value
        serial = (local_value - dt.datetime(1899, 12, 30)).total_seconds() / 86400
        return f'<c r="{ref}" s="2" t="n"><v>{serial:.10f}</v></c>'
    if isinstance(value, Money):
        return f'<c r="{ref}" s="3" t="n"><v>{float(value):.6f}</v></c>'
    style = ' s="1"' if header else ""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{ref}"{style} t="n"><v>{value}</v></c>'
    clean = str(value or "")[:32767]
    return f'<c r="{ref}"{style} t="inlineStr"><is><t xml:space="preserve">{xml_escape(clean)}</t></is></c>'


def _sheet_xml(rows: list[list[Any]], widths: list[int]) -> str:
    cols = "".join(f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>' for i, width in enumerate(widths, 1))
    rendered = []
    for row_index, values in enumerate(rows, 1):
        cells = "".join(_cell(f"{_column_name(col_index)}{row_index}", value, row_index == 1) for col_index, value in enumerate(values, 1))
        rendered.append(f'<row r="{row_index}" ht="{26 if row_index == 1 else 20}" customHeight="1">{cells}</row>')
    max_col = _column_name(max((len(row) for row in rows), default=1))
    max_row = max(1, len(rows))
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + (
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
        f'<cols>{cols}</cols><sheetData>{"".join(rendered)}</sheetData><autoFilter ref="A1:{max_col}{max_row}"/>'
        '<pageMargins left="0.3" right="0.3" top="0.5" bottom="0.5" header="0" footer="0"/>'
        '</worksheet>'
    )


def _write_xlsx(target: Path, sheets: list[tuple[str, list[list[Any]], list[int]]]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    content_types = ''.join(
        f'<Override PartName="/xl/worksheets/sheet{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for index in range(1, len(sheets) + 1)
    )
    workbook_sheets = ''.join(
        f'<sheet name="{xml_escape(name)}" sheetId="{index}" r:id="rId{index}"/>'
        for index, (name, _, _) in enumerate(sheets, 1)
    )
    relationships = ''.join(
        f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{index}.xml"/>'
        for index in range(1, len(sheets) + 1)
    )
    relationships += f'<Relationship Id="rId{len(sheets)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    files = {
        "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>' + content_types + '</Types>',
        "_rels/.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        "xl/workbook.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + workbook_sheets + '</sheets></workbook>',
        "xl/_rels/workbook.xml.rels": '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + relationships + '</Relationships>',
        "xl/styles.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><numFmts count="2"><numFmt numFmtId="164" formatCode="yyyy-mm-dd hh:mm"/><numFmt numFmtId="165" formatCode="0.000000"/></numFmts><fonts count="2"><font><sz val="11"/><name val="Microsoft YaHei"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Microsoft YaHei"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF087F73"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="4"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf><xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1" applyAlignment="1"><alignment vertical="top"/></xf><xf numFmtId="165" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1" applyAlignment="1"><alignment vertical="top"/></xf></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>',
    }
    for index, (_, rows, widths) in enumerate(sheets, 1):
        files[f"xl/worksheets/sheet{index}.xml"] = _sheet_xml(rows, widths)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, content in files.items():
            archive.writestr(name, content.encode("utf-8"))
