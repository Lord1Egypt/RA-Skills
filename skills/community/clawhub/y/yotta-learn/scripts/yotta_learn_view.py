#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_learn_view.py — 元习知识库本地图形化管理台（yotta-learn view）。

零依赖（Python 3.8+ 标准库）：http.server + 面板模板（嵌入副本为运行时真源；
assets/view.html 为编辑真源，由 tools/sync_learn_view_html.py 同步 —— 精简分发副本不带 assets/）。
安全壳（对齐元忆 / 元阁面板口径）：
- 仅绑定 127.0.0.1；Host / Origin / Sec-Fetch-Site 校验；
- 页面内嵌本机会话令牌；写操作必须携带 X-Yotta-View-Token（timing-safe 比较）；
- 破坏性动作需确认串；请求体上限 64 KB；写操作串行化；
- 严格 CSP / no-store / X-Frame-Options: DENY；零远程资源；
- 所有写操作走 yotta_kb 内核（与 CLI 同一真源）并写审计。

启动：yotta-learn view [--port 8791] [--dir <KB>]
"""

import hmac
import json
import os
import re
import secrets
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import yotta_kb  # noqa: E402
import yotta_kb_index  # noqa: E402
import yotta_learn  # noqa: E402

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8791
TOKEN_HEADER = "x-yotta-view-token"
BODY_LIMIT = 64 * 1024
DRAIN_TIMEOUT_SECONDS = 3.0  # 排空请求体的总时间预算（超时即放弃并关闭连接，BUG-L-03）
TOKEN_PLACEHOLDER = "__YOTTA_VIEW_TOKEN__"
VIEW_VERSION = "0.6.6"
AUDIT_TAIL_LIMIT = 200

# @generated view-html:start
VIEW_HTML_EMBEDDED = "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<meta name=\"yotta-view-token\" content=\"__YOTTA_VIEW_TOKEN__\">\n<meta name=\"robots\" content=\"noindex, nofollow\">\n<title>元习知识库 · 管理台</title>\n<style>\n:root{\n  --bg:#f6f7f8; --panel:#ffffff; --line:#e3e6e9; --line-strong:#cbd1d6;\n  --ink:#1b1f23; --ink-2:#4b5560; --ink-3:#78828c;\n  --accent:#0f766e; --accent-soft:#e6f3f1; --warn:#b45309; --warn-soft:#fdf3e3;\n  --danger:#b91c1c; --danger-soft:#fdecec; --ok:#15803d; --ok-soft:#eaf6ee;\n  --radius:8px; --mono:ui-monospace,Consolas,\"Cascadia Mono\",monospace;\n}\n*{box-sizing:border-box}\nhtml,body{margin:0;padding:0}\nbody{background:var(--bg);color:var(--ink);font:14px/1.55 \"Segoe UI\",\"Microsoft YaHei\",system-ui,sans-serif}\nbutton,input,select,textarea{font:inherit;color:inherit}\nbutton{cursor:pointer}\na{color:var(--accent)}\n#app{display:grid;grid-template-columns:236px minmax(0,1fr);min-height:100vh}\n.side{background:var(--panel);border-right:1px solid var(--line);padding:16px 12px;display:flex;flex-direction:column;gap:14px;position:sticky;top:0;height:100vh;overflow:auto}\n.brand{display:flex;gap:10px;align-items:center;padding:2px 6px}\n.logo{width:34px;height:34px;border-radius:8px;background:var(--accent);color:#fff;display:grid;place-items:center;font-weight:700}\n.brand strong{display:block;font-size:14px}\n.brand small{color:var(--ink-3)}\nnav{display:flex;flex-direction:column;gap:2px}\nnav button{display:flex;align-items:center;gap:9px;width:100%;border:0;background:transparent;color:var(--ink-2);padding:8px 10px;border-radius:6px;text-align:left}\nnav button svg{width:16px;height:16px;flex:none}\nnav button:hover{background:#f1f3f5;color:var(--ink)}\nnav button.active{background:var(--accent-soft);color:var(--accent);font-weight:600}\n.side-foot{margin-top:auto;border-top:1px solid var(--line);padding-top:10px;display:flex;flex-direction:column;gap:8px}\n#kbRoot{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);word-break:break-all}\nmain{min-width:0;padding:18px 22px 40px}\n.top{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}\n.top h1{font-size:20px;margin:0}\n.badge{display:inline-flex;align-items:center;gap:6px;background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:3px 10px;font-size:12px;color:var(--ink-2)}\n.badge.ok{background:var(--ok-soft);border-color:#cde7d5;color:var(--ok)}\n.badge.warn{background:var(--warn-soft);border-color:#f0ddb8;color:var(--warn)}\n.grid{display:grid;gap:12px}\n.metrics{grid-template-columns:repeat(4,minmax(0,1fr))}\n.metric{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:12px 14px}\n.metric b{display:block;font-size:22px;line-height:1.2}\n.metric span{color:var(--ink-3);font-size:12.5px}\n.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:14px;margin-top:12px}\n.panel h2{font-size:14px;margin:0 0 10px;display:flex;align-items:center;gap:8px}\n.panel h2 .hint{font-weight:400;color:var(--ink-3);font-size:12px}\ntable{width:100%;border-collapse:collapse;font-size:13px}\nth,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}\nth{color:var(--ink-3);font-weight:600;font-size:12px;white-space:nowrap}\ntr.click{cursor:pointer}\ntr.click:hover td{background:#f8fafb}\n.mono{font-family:var(--mono);font-size:12px}\n.muted{color:var(--ink-3)}\n.pill{display:inline-block;border-radius:999px;padding:1px 8px;font-size:12px;border:1px solid var(--line-strong);color:var(--ink-2);background:#fafbfc}\n.pill.verified{background:var(--ok-soft);border-color:#cde7d5;color:var(--ok)}\n.pill.draft{background:var(--warn-soft);border-color:#f0ddb8;color:var(--warn)}\n.pill.deprecated{background:#f1f3f5;color:var(--ink-3)}\n.row{display:flex;gap:8px;flex-wrap:wrap;align-items:end}\n.field{display:flex;flex-direction:column;gap:4px;min-width:120px}\n.field.grow{flex:1;min-width:220px}\n.field label{font-size:12px;color:var(--ink-3)}\ninput,select,textarea{border:1px solid var(--line-strong);border-radius:6px;padding:6px 8px;background:#fff;min-width:0}\ntextarea{min-height:110px;resize:vertical;font-family:var(--mono);font-size:12.5px}\nbutton.primary{background:var(--accent);border:1px solid var(--accent);color:#fff;border-radius:6px;padding:7px 12px}\nbutton.primary:hover{filter:brightness(1.05)}\nbutton.ghost{background:#fff;border:1px solid var(--line-strong);border-radius:6px;padding:6px 11px;color:var(--ink-2)}\nbutton.ghost:hover{border-color:var(--ink-3);color:var(--ink)}\nbutton.danger{background:var(--danger);border:1px solid var(--danger);color:#fff;border-radius:6px;padding:7px 12px}\nbutton:disabled{opacity:.5;cursor:not-allowed}\n.split{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:12px;align-items:start}\n.checks{max-height:300px;overflow:auto}\n.checkline{display:flex;gap:8px;padding:5px 0;border-bottom:1px dashed var(--line);font-size:12.5px}\n.checkline .st{width:52px;flex:none;font-weight:600}\n.st.ok{color:var(--ok)} .st.warn{color:var(--warn)} .st.error{color:var(--danger)}\npre.body{background:#fbfcfd;border:1px solid var(--line);border-radius:6px;padding:10px;white-space:pre-wrap;word-break:break-word;font-family:var(--mono);font-size:12.5px;max-height:420px;overflow:auto}\n.qa{background:#fbfcfd;border:1px solid var(--line);border-radius:6px;padding:10px;font-size:13px;color:var(--ink-2)}\n.qa b{color:var(--ink)}\n/* advanced cli */\n.quick-group{margin-top:12px}\n.quick-group h4{margin:0 0 6px;font-size:12.5px;color:var(--ink-3)}\n.quick-item{display:flex;gap:10px;align-items:center;justify-content:space-between;border:1px solid var(--line);border-radius:6px;padding:7px 9px;margin-bottom:6px;background:#fbfcfd}\n.quick-item code{font-family:var(--mono);font-size:12px;word-break:break-all}\n.quick-item .note{color:var(--ink-3);font-size:12px;margin-top:2px}\n.quick-item button{flex:none}\n.cli-full{margin-top:10px;max-height:520px;overflow:auto}\n.help-cmd{border:1px solid var(--line);border-radius:6px;background:#fbfcfd;margin-top:8px;min-width:0}\n.help-cmd summary{cursor:pointer;padding:8px 11px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;list-style:none}\n.help-cmd summary::-webkit-details-marker{display:none}\n.help-cmd summary::before{content:'';width:6px;height:6px;border-right:1.6px solid var(--ink-3);border-bottom:1.6px solid var(--ink-3);transform:rotate(-45deg);transition:transform .15s;flex:none}\n.help-cmd[open] summary::before{transform:rotate(45deg)}\n.help-body{padding:10px 11px;display:flex;flex-direction:column;gap:7px;border-top:1px solid var(--line)}\n.help-sub{border-top:1px dashed var(--line);padding-top:7px;margin-top:2px;display:flex;flex-direction:column;gap:5px}\n.help-sub .cmd-name{color:var(--ink)}\n.cmd-name{font-family:var(--mono);font-size:12px;color:var(--accent)}\n.cmd-what{font-weight:600;font-size:13px}\n.cmd-when{color:var(--ink-3);font-size:12px}\n.code-line{display:flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--line);border-radius:6px;padding:5px 8px;min-width:0}\n.code-line code{flex:1;min-width:0;font-family:var(--mono);font-size:12px;overflow-x:auto;white-space:nowrap}\n.code-line button{flex:none;padding:3px 9px;font-size:12px}\n.opt-row{display:grid;grid-template-columns:minmax(140px,auto) minmax(0,1fr);gap:2px 10px;padding:6px 0;border-top:1px dashed var(--line);font-size:12px}\n.opt-row:first-child{border-top:0}\n.opt-flag{font-family:var(--mono);word-break:break-all}\n.opt-what{color:var(--ink-2)}\n.opt-when{color:var(--ink-3)}\n.opt-risk{color:var(--danger)}\n.notice{border-radius:6px;padding:8px 10px;font-size:12.5px;margin-top:8px}\n.notice.warn{background:var(--warn-soft);color:var(--warn);border:1px solid #f0ddb8}\n.notice.err{background:var(--danger-soft);color:var(--danger);border:1px solid #f2caca}\n.notice.ok{background:var(--ok-soft);color:var(--ok);border:1px solid #cde7d5}\n.empty{color:var(--ink-3);padding:14px 2px}\n#toast{position:fixed;right:16px;bottom:16px;display:flex;flex-direction:column;gap:8px;z-index:50;max-width:420px}\n.toast{background:#1f2937;color:#fff;border-radius:8px;padding:10px 12px;font-size:13px;box-shadow:0 6px 18px rgba(0,0,0,.18)}\n.toast.err{background:var(--danger)}\n.toast.ok{background:var(--accent)}\n.mask{position:fixed;inset:0;background:rgba(15,23,42,.45);display:none;align-items:center;justify-content:center;z-index:45;padding:20px}\n.mask.open{display:flex}\n.modal{width:min(480px,100%);max-height:86vh;overflow:auto;background:var(--panel);border:1px solid var(--line-strong);border-radius:10px;padding:16px;box-shadow:0 12px 32px rgba(0,0,0,.2)}\n.modal.wide{width:min(720px,100%)}\n.modal h3{margin:0 0 10px;font-size:15px}\n.modal h3 .hint{font-weight:400;color:var(--ink-3);font-size:12px}\n.modal .field{margin-bottom:10px}\n.modal-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:12px}\n.checkline-inline{display:flex;gap:8px;align-items:center;font-size:12.5px;color:var(--ink-2)}\n.checkline-inline input{width:auto;min-width:0}\n@media (max-width:860px){\n  #app{grid-template-columns:1fr}\n  .side{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)}\n  nav{flex-direction:row;flex-wrap:wrap}\n  nav button{width:auto}\n  .metrics{grid-template-columns:repeat(2,minmax(0,1fr))}\n  .split{grid-template-columns:1fr}\n  main{padding:14px 12px 40px}\n  table{display:block;overflow-x:auto;white-space:nowrap}\n}\n</style>\n</head>\n<body>\n<div id=\"app\">\n  <aside class=\"side\">\n    <div class=\"brand\"><span class=\"logo\">习</span><div><strong>元习知识库</strong><small>yotta-learn view</small></div></div>\n    <nav id=\"nav\"></nav>\n    <div class=\"side-foot\">\n      <div id=\"kbRoot\" class=\"mono\">…</div>\n      <button class=\"ghost\" id=\"btnRefresh\">刷新当前页</button>\n    </div>\n  </aside>\n  <main>\n    <header class=\"top\">\n      <h1 id=\"viewTitle\">总览</h1>\n      <div class=\"top-actions\"><span class=\"badge\" id=\"originBadge\">加载中</span></div>\n    </header>\n    <section id=\"view\"><div class=\"empty\">加载中…</div></section>\n  </main>\n</div>\n<div id=\"toast\"></div>\n<div class=\"mask\" id=\"modalMask\"><div class=\"modal\" id=\"modalBox\"></div></div>\n<script>\nconst TOKEN = (document.querySelector('meta[name=\"yotta-view-token\"]')||{}).content || '';\nconst CONFIRM = {\n  entryDeprecate:'entry-deprecate', indexRebuild:'index-rebuild',\n  locationSet:'location-set', locationMove:'location-move',\n  trashPurge:'trash-purge', snapshotRestore:'snapshot-restore',\n  reviewForce:'review-force',\n  categoryMerge:'category-merge', categoryDeprecate:'category-deprecate'\n};\nconst ICONS = {\n  overview:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M3 12h4l3-8 4 16 3-8h4\"/></svg>',\n  categories:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\"/></svg>',\n  entries:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01\"/></svg>',\n  search:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><circle cx=\"11\" cy=\"11\" r=\"7\"/><path d=\"m20 20-3.5-3.5\"/></svg>',\n  review:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M9 11l3 3L22 4\"/><path d=\"M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11\"/></svg>',\n  location:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0z\"/><circle cx=\"12\" cy=\"10\" r=\"3\"/></svg>',\n  ops:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M14.7 6.3a4 4 0 0 0 5 5L21 21l-3-3-9.7-9.7a4 4 0 0 1-5-5L6 6l3 3\"/></svg>',\n  cli:'<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"m4 17 6-6-6-6\"/><path d=\"M12 19h8\"/></svg>'\n};\nconst NAV = [['overview','总览'],['categories','分类'],['entries','条目'],['search','搜索'],['review','审核'],['location','位置'],['ops','运维'],['cli','高级 / CLI']];\nconst state = {view:'overview', overview:null, categories:[], entry:null, opsBackup:''};\nlet viewSeq=0;\nfunction stale(seq){return seq!==viewSeq;}\n\nfunction esc(v){return String(v==null?'':v).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));}\nfunction $(sel,root){return (root||document).querySelector(sel);}\nfunction toast(msg,kind){\n  const box=document.createElement('div');box.className='toast '+(kind||'');\n  box.textContent=String(msg);$('#toast').appendChild(box);\n  setTimeout(()=>box.remove(),4200);\n}\nlet modalOkFn=null;\nfunction closeModal(){$('#modalMask').classList.remove('open');$('#modalBox').classList.remove('wide');modalOkFn=null;}\nfunction openModal(title,bodyHtml,onOk,okText,danger){\n  $('#modalBox').classList.remove('wide');\n  $('#modalBox').innerHTML='<h3>'+esc(title)+'</h3>'+bodyHtml+\n    '<div class=\"modal-actions\"><button class=\"ghost\" id=\"modalCancel\">取消</button>'+\n    '<button class=\"'+(danger?'danger':'primary')+'\" id=\"modalOk\">'+esc(okText||'确认')+'</button></div>';\n  modalOkFn=onOk||null;\n  $('#modalCancel').onclick=closeModal;\n  $('#modalOk').onclick=async()=>{ if(modalOkFn) await modalOkFn(); };\n  $('#modalMask').classList.add('open');\n}\n$('#modalMask').addEventListener('click',e=>{if(e.target===$('#modalMask'))closeModal();});\nasync function api(path,opts){\n  const res=await fetch(path,opts||{});\n  let data=null;try{data=await res.json();}catch(e){data={error:'响应不是 JSON'};}\n  if(!res.ok||data.error){throw new Error((data&&data.error)||('HTTP '+res.status));}\n  return data;\n}\nasync function act(action,payload){\n  return api('/api/action',{method:'POST',\n    headers:{'Content-Type':'application/json','X-Yotta-View-Token':TOKEN},\n    body:JSON.stringify(Object.assign({action:action},payload||{}))});\n}\nfunction pill(status){return '<span class=\"pill '+esc(status)+'\">'+esc(status)+'</span>';}\nfunction fmtTime(v){return esc(String(v||'').replace('T',' ').slice(0,19));}\n\nfunction renderNav(){\n  const nav=$('#nav');\n  if(nav.children.length!==NAV.length){\n    nav.innerHTML=NAV.map(([id,label])=>\n      '<button data-nav=\"'+id+'\" class=\"'+(state.view===id?'active':'')+'\">'+ICONS[id]+'<span>'+label+'</span></button>').join('');\n    nav.querySelectorAll('button').forEach(b=>b.onclick=()=>go(b.dataset.nav));\n  }\n  nav.querySelectorAll('button').forEach(b=>b.classList.toggle('active',b.dataset.nav===state.view));\n}\nfunction setTitle(t){$('#viewTitle').textContent=t;}\nfunction setOrigin(text,ok){const b=$('#originBadge');b.textContent=text;b.className='badge '+(ok===false?'warn':'ok');}\nasync function go(view){\n  const seq=++viewSeq;\n  state.view=view;renderNav();\n  const v=$('#view');v.innerHTML='<div class=\"empty\">加载中…</div>';\n  try{\n    if(view==='overview')await renderOverview(seq);\n    else if(view==='categories')await renderCategories(seq);\n    else if(view==='entries')await renderEntries(seq);\n    else if(view==='search')await renderSearch(seq);\n    else if(view==='review')await renderReview(seq);\n    else if(view==='location')await renderLocation(seq);\n    else if(view==='ops')await renderOps(seq);\n    else if(view==='cli')await renderCli(seq);\n  }catch(e){if(stale(seq))return;v.innerHTML='<div class=\"notice err\">'+esc(e.message)+'</div>';}\n}\n\nasync function copyText(text){\n  try{\n    if(navigator.clipboard&&navigator.clipboard.writeText){\n      await navigator.clipboard.writeText(text);return true;\n    }\n  }catch(e){}\n  try{\n    const ta=document.createElement('textarea');ta.value=text;\n    ta.style.position='fixed';ta.style.opacity='0';\n    document.body.appendChild(ta);ta.select();\n    const ok=document.execCommand('copy');ta.remove();return ok;\n  }catch(e){return false;}\n}\n\nfunction helpOptRows(options){\n  return (options||[]).map(o=>'<div class=\"opt-row\"><div class=\"opt-flag\">'+esc(o.flag+(o.arg?' '+o.arg:''))+'</div><div>'+\n    '<div class=\"opt-what\">'+esc(o.what||'')+'</div>'+\n    (o.when?'<div class=\"opt-when\">'+esc(o.when)+'</div>':'')+\n    (o.caution?'<div class=\"opt-risk\">'+esc(o.caution)+'</div>':'')+\n    '</div></div>').join('');\n}\nfunction helpCodeLine(text){\n  return '<div class=\"code-line\"><code>'+esc(text)+'</code><button class=\"ghost\" data-copy=\"'+esc(text)+'\">复制</button></div>';\n}\nfunction helpSubHtml(parent,s){\n  const full=parent+' '+s.name;\n  const inner=(s.subcommands||[]).map(ss=>helpSubHtml(full,ss)).join('');\n  return '<div class=\"help-sub\"><div><code class=\"cmd-name\">'+esc(s.name)+'</code></div>'+\n    (s.what?'<div class=\"cmd-what\">'+esc(s.what)+'</div>':'')+\n    (s.when?'<div class=\"cmd-when\">'+esc(s.when)+'</div>':'')+\n    helpCodeLine('yotta-learn '+full+' '+s.usage)+helpOptRows(s.options)+inner+'</div>';\n}\nfunction renderFullHelp(d){\n  return (d.groups||[]).map(g=>'<div class=\"quick-group\"><h4>'+esc(g.group)+'</h4>'+\n    (g.commands||[]).map(c=>{\n      const subs=(c.subcommands||[]).map(s=>helpSubHtml(c.name,s)).join('');\n      return '<details class=\"help-cmd\"><summary><code class=\"cmd-name\">'+esc(c.name)+'</code><span class=\"cmd-what\">'+esc(c.what)+'</span></summary>'+\n        '<div class=\"help-body\">'+(c.when?'<div class=\"cmd-when\">'+esc(c.when)+'</div>':'')+\n        helpCodeLine('yotta-learn '+c.usage)+helpOptRows(c.options)+subs+'</div></details>';\n    }).join('')+'</div>').join('');\n}\nasync function renderCli(seq){\n  setTitle('高级 / CLI');\n  const d=await api('/api/cli');\n  if(stale(seq))return;\n  const quick=(d.quick||[]).map(g=>'<div class=\"quick-group\"><h4>'+esc(g.group)+'</h4>'+\n    (g.items||[]).map(it=>'<div class=\"quick-item\"><div><code>'+esc(it.cmd)+'</code>'+\n      '<div class=\"note\">'+esc(it.note||'')+'</div></div>'+\n      '<button class=\"ghost\" data-copy=\"'+esc(it.cmd)+'\">复制</button></div>').join('')+\n    '</div>').join('');\n  $('#view').innerHTML='<div class=\"panel\"><h2>常用命令 <span class=\"hint\">点「复制」直接在终端执行；技能目录直跑等价：python3 scripts/yotta_learn.py …</span></h2>'+\n    quick+\n    '<div style=\"margin-top:10px\"><button class=\"ghost\" id=\"btnFullHelp\">查看完整帮助</button> '+\n    '<button class=\"ghost\" id=\"btnCopyFull\" hidden>复制全部</button></div>'+\n    '<div class=\"cli-full\" id=\"cliFull\" hidden></div></div>';\n  const bindCopy=root=>{root.querySelectorAll('button[data-copy]').forEach(b=>{\n    b.onclick=async()=>{const ok=await copyText(b.dataset.copy);\n      toast(ok?'已复制：'+b.dataset.copy:'复制失败，请手动选择复制',ok?'ok':'err');};\n  });};\n  bindCopy($('#view'));\n  $('#btnFullHelp').onclick=()=>{\n    const el=$('#cliFull');\n    if(el.hidden&&!el.dataset.rendered){el.innerHTML=renderFullHelp(d);el.dataset.rendered='1';bindCopy(el);}\n    el.hidden=!el.hidden;\n    $('#btnCopyFull').hidden=el.hidden;\n    $('#btnFullHelp').textContent=el.hidden?'查看完整帮助':'收起完整帮助';\n  };\n  $('#btnCopyFull').onclick=async()=>{\n    const ok=await copyText(d.full||'');\n    toast(ok?'已复制完整帮助':'复制失败，请手动选择复制',ok?'ok':'err');\n  };\n}\n\nasync function loadRootBadge(){\n  try{\n    const info=await api('/api/location');\n    $('#kbRoot').textContent='KB：'+info.root;\n    const parts=String(info.root||'').split(/[\\\\/]/).filter(Boolean);\n    document.title='元习知识库 · 管理台'+(parts.length?' · '+parts[parts.length-1]:'');\n    setOrigin('位置来源：'+info.origin+(info.initialized?'':'（未初始化）'),info.initialized);\n  }catch(e){setOrigin('位置不可用：'+e.message,false);}\n}\n\nasync function renderOverview(seq){\n  setTitle('总览');\n  const d=await api('/api/overview');\n  if(stale(seq))return;\n  const s=d.stats;\n  const checks=d.doctor.checks.map(c=>'<div class=\"checkline\"><span class=\"st '+esc(c.status)+'\">'+esc(c.status)+'</span><span>'+esc(c.name)+'：'+esc(c.detail||'')+'</span></div>').join('');\n  const audit=(d.audit||[]).slice().reverse().map(r=>'<tr><td class=\"mono\">'+fmtTime(r.ts||r.at||'')+'</td><td>'+esc(r.action||'')+'</td><td>'+esc(r.target||'')+'</td><td>'+esc(r.actor||'')+'</td></tr>').join('');\n  $('#view').innerHTML=\n    '<div class=\"grid metrics\">'+\n      '<div class=\"metric\"><b>'+esc(s.total)+'</b><span>条目总数</span></div>'+\n      '<div class=\"metric\"><b>'+esc(s.categories)+'</b><span>分类</span></div>'+\n      '<div class=\"metric\"><b>'+esc(s.trash)+'</b><span>回收站</span></div>'+\n      '<div class=\"metric\"><b>'+(s.index_drift?'漂移':'健康')+'</b><span>索引状态</span></div>'+\n    '</div>'+\n    '<div class=\"panel\"><h2>体检 <span class=\"hint\">错误 '+esc(d.doctor.errors)+' / 警告 '+esc(d.doctor.warnings)+'</span></h2><div class=\"checks\">'+checks+'</div></div>'+\n    '<div class=\"panel\"><h2>最近审计</h2>'+(audit?'<table><thead><tr><th>时间</th><th>动作</th><th>对象</th><th>身份</th></tr></thead><tbody>'+audit+'</tbody></table>':'<div class=\"empty\">暂无记录</div>')+'</div>';\n}\n\nasync function renderCategories(seq){\n  setTitle('分类');\n  const d=await api('/api/categories');state.categories=d.categories;\n  if(stale(seq))return;\n  const rows=d.categories.map(c=>{\n    const ops=(c.status==='deprecated')\n      ? '<span class=\"muted\">已停用</span>'\n      : '<button class=\"ghost\" data-cat-rename=\"'+esc(c.slug)+'\">重命名</button> '+\n        '<button class=\"ghost\" data-cat-merge=\"'+esc(c.slug)+'\">合并</button> '+\n        '<button class=\"ghost\" data-cat-deprecate=\"'+esc(c.slug)+'\">停用</button>';\n    return '<tr><td class=\"mono\">'+esc(c.slug)+'</td><td>'+esc(c.name)+'</td><td>'+esc(c.description)+'</td><td>'+pill(c.status||'active')+'</td><td class=\"muted\">'+esc((c.aliases||[]).join(', '))+'</td><td class=\"muted\">'+esc(c.created_by||'-')+'</td><td class=\"muted\">'+fmtTime(c.created_at)+'</td><td>'+ops+'</td></tr>';\n  }).join('');\n  $('#view').innerHTML=\n    '<div class=\"panel\"><h2>新建分类</h2><div class=\"row\">'+\n      '<div class=\"field\"><label>slug（小写连字符）</label><input id=\"catSlug\" placeholder=\"agent-skills\"></div>'+\n      '<div class=\"field\"><label>中文名</label><input id=\"catName\" placeholder=\"智能体与技能开发\"></div>'+\n      '<div class=\"field grow\"><label>一句话说明</label><input id=\"catDesc\" placeholder=\"技能开发与编排相关知识\"></div>'+\n      '<button class=\"primary\" id=\"catCreate\">创建</button>'+\n    '</div><div id=\"catNotice\"></div></div>'+\n    '<div class=\"panel\"><h2>分类列表 <span class=\"hint\">'+esc(d.count)+' 个</span></h2>'+\n      (rows?'<table><thead><tr><th>slug</th><th>名称</th><th>说明</th><th>状态</th><th>别名</th><th>创建者</th><th>创建时间</th><th>操作</th></tr></thead><tbody>'+rows+'</tbody></table>':'<div class=\"empty\">暂无分类</div>')+'</div>';\n  $('#catCreate').onclick=async()=>{\n    try{\n      const r=await act('category.create',{slug:$('#catSlug').value.trim(),name:$('#catName').value.trim(),description:$('#catDesc').value.trim()});\n      toast('已创建分类 '+r.slug,'ok');go('categories');\n    }catch(e){$('#catNotice').innerHTML='<div class=\"notice err\">'+esc(e.message)+'</div>';}\n  };\n  $('#view').querySelectorAll('button[data-cat-rename]').forEach(b=>b.onclick=()=>openCatRename(b.dataset.catRename));\n  $('#view').querySelectorAll('button[data-cat-merge]').forEach(b=>b.onclick=()=>openCatMerge(b.dataset.catMerge));\n  $('#view').querySelectorAll('button[data-cat-deprecate]').forEach(b=>b.onclick=()=>openCatDeprecate(b.dataset.catDeprecate));\n}\nfunction openCatRename(slug){\n  const cat=state.categories.filter(c=>c.slug===slug)[0]||{};\n  openModal('重命名分类 '+slug,\n    '<div class=\"field\"><label>新中文名</label><input id=\"mCatName\" value=\"'+esc(cat.name||'')+'\"></div>'+\n    '<div class=\"muted\" style=\"font-size:12.5px\">只改显示名；slug 与别名不变。</div>',\n    async()=>{\n      try{\n        const r=await act('category.rename',{slug:slug,name:$('#mCatName').value.trim()});\n        closeModal();toast('已重命名 '+r.slug+' → '+r.name,'ok');go('categories');\n      }catch(e){toast(e.message,'err');}\n    },'保存');\n}\nfunction openCatMerge(slug){\n  const options=state.categories.filter(c=>c.slug!==slug&&c.status!=='deprecated')\n    .map(c=>'<option value=\"'+esc(c.slug)+'\">'+esc(c.name)+'（'+esc(c.slug)+'）</option>').join('');\n  openModal('合并分类 '+slug,\n    '<p class=\"muted\" style=\"font-size:12.5px\">源分类条目将迁入目标分类，源分类保留为别名并停用；操作前自动快照。</p>'+\n    '<div class=\"field\"><label>目标分类</label><select id=\"mCatInto\">'+(options||'<option value=\"\">（没有可合并的目标）</option>')+'</select></div>'+\n    '<div class=\"field\"><label>确认串（category-merge）</label><input id=\"mCatConfirm\" placeholder=\"category-merge\"></div>',\n    async()=>{\n      try{\n        const r=await act('category.merge',{from:slug,into:$('#mCatInto').value,confirm:$('#mCatConfirm').value.trim()});\n        closeModal();toast('已合并：迁移 '+r.moved+' 条到 '+r.into,'ok');go('categories');\n      }catch(e){toast(e.message,'err');}\n    },'合并',true);\n}\nfunction openCatDeprecate(slug){\n  openModal('停用分类 '+slug,\n    '<p class=\"muted\" style=\"font-size:12.5px\">分类下仍有条目时默认拒绝；勾选「强制停用」可保留条目并停用分类。操作前自动快照。</p>'+\n    '<div class=\"field\"><label>原因（记入审计，可选）</label><input id=\"mCatReason\" placeholder=\"例：已被新分类替代\"></div>'+\n    '<label class=\"checkline-inline\"><input type=\"checkbox\" id=\"mCatForce\"> 强制停用（分类下条目不移走）</label>'+\n    '<div class=\"field\" style=\"margin-top:10px\"><label>确认串（category-deprecate）</label><input id=\"mCatConfirm\" placeholder=\"category-deprecate\"></div>',\n    async()=>{\n      try{\n        const r=await act('category.deprecate',{slug:slug,reason:$('#mCatReason').value.trim(),force:$('#mCatForce').checked,confirm:$('#mCatConfirm').value.trim()});\n        closeModal();toast('已停用分类 '+r.slug,'ok');go('categories');\n      }catch(e){toast(e.message,'err');}\n    },'停用',true);\n}\n\nasync function renderEntries(seq){\n  setTitle('条目');\n  const d=await api('/api/entries');\n  if(stale(seq))return;\n  const cats=(state.categories.length?state.categories:(await api('/api/categories')).categories);\n  if(stale(seq))return;\n  const options='<option value=\"\">全部分类</option>'+cats.map(c=>'<option value=\"'+esc(c.slug)+'\">'+esc(c.name)+'（'+esc(c.slug)+'）</option>').join('');\n  const rows=d.entries.map(e=>'<tr class=\"click\" data-id=\"'+esc(e.id)+'\"><td class=\"mono\">'+esc(e.id)+'</td><td>'+pill(e.status)+'</td><td>'+esc(e.category)+'</td><td>'+esc(e.title)+'</td><td class=\"muted\">'+esc((e.tags||[]).join(', '))+'</td><td class=\"muted\">'+fmtTime(e.updated)+'</td></tr>').join('');\n  $('#view').innerHTML=\n    '<div class=\"panel\"><h2>写入条目（默认草稿，核验后生效）</h2><div class=\"row\">'+\n      '<div class=\"field\"><label>分类</label><select id=\"addCat\">'+options+'</select></div>'+\n      '<div class=\"field grow\"><label>标题</label><input id=\"addTitle\"></div>'+\n      '<div class=\"field\"><label>置信度</label><select id=\"addConf\"><option>medium</option><option>high</option><option>low</option></select></div>'+\n    '</div><div class=\"row\" style=\"margin-top:8px\">'+\n      '<div class=\"field grow\"><label>正文（Markdown）</label><textarea id=\"addMsg\"></textarea></div>'+\n    '</div><div class=\"row\" style=\"margin-top:8px\">'+\n      '<div class=\"field\"><label>来源</label><input id=\"addSource\"></div>'+\n      '<div class=\"field\"><label>标签（逗号分隔）</label><input id=\"addTags\"></div>'+\n      '<div class=\"field grow\"><label>证据（核验用）</label><input id=\"addEvidence\"></div>'+\n      '<button class=\"primary\" id=\"addBtn\">写入草稿</button>'+\n    '</div><div id=\"addNotice\"></div></div>'+\n    '<div class=\"panel\"><h2>条目列表 <span class=\"hint\">'+esc(d.count)+' 条</span></h2><div class=\"row\">'+\n      '<div class=\"field\"><label>分类</label><select id=\"fCat\">'+options+'</select></div>'+\n      '<div class=\"field\"><label>状态</label><select id=\"fStatus\"><option value=\"\">全部</option><option>draft</option><option>verified</option><option>deprecated</option></select></div>'+\n      '<div class=\"field\"><label>标签</label><input id=\"fTag\"></div><button class=\"ghost\" id=\"fApply\">筛选</button>'+\n    '</div><div id=\"entryTable\">'+(rows?'<table><thead><tr><th>ID</th><th>状态</th><th>分类</th><th>标题</th><th>标签</th><th>更新</th></tr></thead><tbody>'+rows+'</tbody></table>':'<div class=\"empty\">暂无条目</div>')+'</div></div>';\n  $('#addBtn').onclick=async()=>{\n    try{\n      const r=await act('entry.add',{category:$('#addCat').value,title:$('#addTitle').value.trim(),message:$('#addMsg').value,\n        source:$('#addSource').value.trim(),tags:$('#addTags').value.trim(),evidence:$('#addEvidence').value.trim(),confidence:$('#addConf').value});\n      let extra='';\n      if((r.sensitive||[]).length)extra+='<div class=\"notice warn\">敏感命中 '+r.sensitive.length+' 处，核验将被阻断（需 force 放行）。</div>';\n      if((r.similar||[]).length)extra+='<div class=\"notice warn\">标题相近：'+r.similar.map(s=>esc(s.id)).join(', ')+'</div>';\n      $('#addNotice').innerHTML='<div class=\"notice ok\">已写入草稿 '+esc(r.id)+'</div>'+extra;\n      toast('已写入草稿 '+r.id,'ok');loadRootBadge();\n    }catch(e){$('#addNotice').innerHTML='<div class=\"notice err\">'+esc(e.message)+'</div>';}\n  };\n  $('#fApply').onclick=async()=>{\n    try{\n      const params=new URLSearchParams();\n      if($('#fCat').value)params.set('category',$('#fCat').value);\n      if($('#fStatus').value)params.set('status',$('#fStatus').value);\n      if($('#fTag').value.trim())params.set('tag',$('#fTag').value.trim());\n      const dd=await api('/api/entries?'+params.toString());\n      const rr=dd.entries.map(e=>'<tr class=\"click\" data-id=\"'+esc(e.id)+'\"><td class=\"mono\">'+esc(e.id)+'</td><td>'+pill(e.status)+'</td><td>'+esc(e.category)+'</td><td>'+esc(e.title)+'</td><td class=\"muted\">'+esc((e.tags||[]).join(', '))+'</td><td class=\"muted\">'+fmtTime(e.updated)+'</td></tr>').join('');\n      $('#entryTable').innerHTML=rr?'<table><thead><tr><th>ID</th><th>状态</th><th>分类</th><th>标题</th><th>标签</th><th>更新</th></tr></thead><tbody>'+rr+'</tbody></table>':'<div class=\"empty\">无匹配条目</div>';\n      bindRows();\n    }catch(e){toast(e.message,'err');}\n  };\n  function bindRows(){$('#entryTable').querySelectorAll('tr.click').forEach(r=>r.onclick=()=>openEntry(r.dataset.id));}\n  bindRows();\n}\n\nasync function openEntry(id){\n  try{\n    const e=await api('/api/entry?id='+encodeURIComponent(id));\n    state.entry=e;\n    const verified=e.status==='verified'?'<div class=\"notice ok\">已核验（'+esc(e.verified_by||'')+' @ '+fmtTime(e.verified_at)+'）</div>':'';\n    $('#modalBox').classList.add('wide');\n    $('#modalBox').innerHTML=\n      '<h3>'+esc(e.id)+' <span class=\"hint\">'+esc(e.title)+'</span> '+pill(e.status)+'</h3>'+verified+\n      '<pre class=\"body\">'+esc(e.body||'')+'</pre>'+\n      '<div class=\"row\" style=\"margin-top:10px\">'+\n        '<div class=\"field grow\"><label>标题</label><input id=\"edTitle\" value=\"'+esc(e.title)+'\"></div>'+\n        '<div class=\"field\"><label>置信度</label><select id=\"edConf\"><option'+(e.confidence==='high'?' selected':'')+'>high</option><option'+(e.confidence==='medium'?' selected':'')+'>medium</option><option'+(e.confidence==='low'?' selected':'')+'>low</option></select></div>'+\n        '<div class=\"field\"><label>标签（逗号分隔）</label><input id=\"edTags\" value=\"'+esc((e.tags||[]).join(', '))+'\"></div>'+\n      '</div>'+\n      '<div class=\"row\" style=\"margin-top:8px\">'+\n        '<div class=\"field grow\"><label>正文</label><textarea id=\"edMsg\">'+esc(e.body||'')+'</textarea></div>'+\n      '</div><div class=\"row\" style=\"margin-top:8px\">'+\n        '<div class=\"field\"><label>来源</label><input id=\"edSource\" value=\"'+esc(e.source||'')+'\"></div>'+\n        '<div class=\"field grow\"><label>证据</label><input id=\"edEvidence\" value=\"'+esc(e.evidence||'')+'\"></div>'+\n        '<button class=\"primary\" id=\"edSave\">保存修改</button>'+\n        '<button class=\"danger\" id=\"edDep\">停用条目</button>'+\n      '</div><div id=\"edNotice\"></div>'+\n      '<div class=\"row\" style=\"margin-top:10px\">'+\n        '<div class=\"field\"><label>停用确认串</label><input id=\"edConfirm\" placeholder=\"'+CONFIRM.entryDeprecate+'\"></div>'+\n        '<div class=\"field grow\"><label>停用原因</label><input id=\"edReason\"></div>'+\n      '</div>'+\n      '<div class=\"modal-actions\"><button class=\"ghost\" id=\"modalCancel\">关闭</button></div>';\n    $('#modalCancel').onclick=closeModal;\n    $('#modalMask').classList.add('open');\n    $('#edSave').onclick=async()=>{\n      try{\n        await act('entry.update',{id:e.id,title:$('#edTitle').value.trim(),message:$('#edMsg').value,\n          tags:$('#edTags').value.trim(),source:$('#edSource').value.trim(),\n          evidence:$('#edEvidence').value.trim(),confidence:$('#edConf').value});\n        toast('已保存 '+e.id,'ok');openEntry(e.id);\n      }catch(err){$('#edNotice').innerHTML='<div class=\"notice err\">'+esc(err.message)+'</div>';}\n    };\n    $('#edDep').onclick=async()=>{\n      try{\n        await act('entry.deprecate',{id:e.id,confirm:$('#edConfirm').value.trim(),reason:$('#edReason').value.trim()});\n        toast('已停用 '+e.id,'ok');openEntry(e.id);\n      }catch(err){$('#edNotice').innerHTML='<div class=\"notice err\">'+esc(err.message)+'</div>';}\n    };\n  }catch(err){toast(err.message,'err');}\n}\n\nasync function renderSearch(seq){\n  setTitle('搜索');\n  $('#view').innerHTML=\n    '<div class=\"panel\"><h2>关键词查询 <span class=\"hint\">默认只出已核验条目</span></h2><div class=\"row\">'+\n      '<div class=\"field grow\"><label>关键词</label><input id=\"qText\" placeholder=\"例如：发布 流程\"></div>'+\n      '<div class=\"field\"><label>分类</label><input id=\"qCat\" placeholder=\"可选 slug\"></div>'+\n      '<div class=\"field\"><label>返回上限</label><input id=\"qLimit\" type=\"number\" value=\"20\" min=\"1\" max=\"100\"></div>'+\n      '<label class=\"field\"><span><input type=\"checkbox\" id=\"qDraft\"> 含草稿</span><span><input type=\"checkbox\" id=\"qDep\"> 含停用</span></label>'+\n      '<button class=\"primary\" id=\"qBtn\">搜索</button>'+\n    '</div><div id=\"qResult\" style=\"margin-top:10px\"></div></div>';\n  $('#qBtn').onclick=async()=>{\n    try{\n      const p=new URLSearchParams({q:$('#qText').value.trim(),limit:$('#qLimit').value||'20'});\n      if($('#qCat').value.trim())p.set('category',$('#qCat').value.trim());\n      if($('#qDraft').checked)p.set('include_draft','1');\n      if($('#qDep').checked)p.set('include_deprecated','1');\n      const d=await api('/api/search?'+p.toString());\n      const rows=d.results.map(r=>'<tr class=\"click\" data-id=\"'+esc(r.id)+'\"><td class=\"mono\">'+esc(r.id)+'</td><td>'+Number(r.score).toFixed(2)+'</td><td>'+pill(r.status)+'</td><td>'+esc(r.title)+'</td><td class=\"muted\">'+esc(r.category)+'</td></tr>').join('');\n      $('#qResult').innerHTML=(d.stale?'<div class=\"notice warn\">索引漂移，已降级线性扫描；建议到「运维」重建索引。</div>':'')+\n        (rows?'<table><thead><tr><th>ID</th><th>分数</th><th>状态</th><th>标题</th><th>分类</th></tr></thead><tbody>'+rows+'</tbody></table>':'<div class=\"empty\">无匹配结果</div>');\n      $('#qResult').querySelectorAll('tr.click').forEach(r=>r.onclick=()=>openEntry(r.dataset.id));\n    }catch(e){toast(e.message,'err');}\n  };\n}\n\nasync function renderReview(seq){\n  setTitle('审核');\n  const d=await api('/api/entries?status=draft');\n  if(stale(seq))return;\n  const rows=d.entries.map(e=>'<tr class=\"click\" data-id=\"'+esc(e.id)+'\"><td class=\"mono\">'+esc(e.id)+'</td><td>'+esc(e.title)+'</td><td class=\"muted\">'+esc(e.category)+'</td><td class=\"muted\">'+fmtTime(e.updated)+'</td></tr>').join('');\n  $('#view').innerHTML=\n    '<div class=\"panel\"><h2>待审核草稿 <span class=\"hint\">'+esc(d.count)+' 条</span></h2>'+\n      (rows?'<table><thead><tr><th>ID</th><th>标题</th><th>分类</th><th>更新</th></tr></thead><tbody>'+rows+'</tbody></table>':'<div class=\"empty\">没有待审核草稿</div>')+'</div>';\n  $('#view').querySelectorAll('tr.click').forEach(r=>r.onclick=()=>openReview(r.dataset.id));\n}\n\nasync function openReview(id){\n  const e=await api('/api/entry?id='+encodeURIComponent(id));\n  $('#modalBox').classList.add('wide');\n  $('#modalBox').innerHTML=\n    '<h3>'+esc(e.id)+' <span class=\"hint\">'+esc(e.title)+'</span></h3>'+\n    '<div class=\"qa\"><b>质检三问</b><br>1）验证过？有可验证的证据<br>2）自包含？不依赖会话上下文即可复用<br>3）无敏感？无密钥 / 个人信息 / 本机路径</div>'+\n    '<pre class=\"body\" style=\"margin-top:10px\">'+esc(e.body||'')+'</pre>'+\n    '<div class=\"row\" style=\"margin-top:10px\">'+\n      '<div class=\"field grow\"><label>证据（pass 必填）</label><input id=\"rvEvidence\" value=\"'+esc(e.evidence||'')+'\"></div>'+\n      '<div class=\"field grow\"><label>备注 / 拒绝原因</label><input id=\"rvNote\"></div>'+\n    '</div><div class=\"row\" style=\"margin-top:8px\">'+\n      '<label class=\"field\"><span><input type=\"checkbox\" id=\"rvForce\"> 敏感命中时 force 放行</span></label>'+\n      '<div class=\"field\"><label>force 确认串</label><input id=\"rvConfirm\" placeholder=\"'+CONFIRM.reviewForce+'\"></div>'+\n      '<button class=\"primary\" id=\"rvPass\">核验通过</button>'+\n      '<button class=\"danger\" id=\"rvReject\">拒绝并移入回收站</button>'+\n      '<button class=\"ghost\" id=\"modalCancel\">关闭</button>'+\n    '</div><div id=\"rvNotice\"></div>';\n  $('#modalCancel').onclick=closeModal;\n  $('#modalMask').classList.add('open');\n  const send=async(decision)=>{\n    try{\n      const body={id:e.id,decision:decision,evidence:$('#rvEvidence').value.trim(),note:$('#rvNote').value.trim()};\n      if($('#rvForce').checked){body.force=true;body.confirm=$('#rvConfirm').value.trim();}\n      const r=await act('entry.review',body);\n      toast(decision==='pass'?('已核验 '+e.id):('已拒绝 '+e.id),'ok');\n      if((r.findings||[]).length)toast('force 放行 '+r.findings.length+' 处敏感命中（已记审计）','');\n      closeModal();\n      go('review');\n    }catch(err){$('#rvNotice').innerHTML='<div class=\"notice err\">'+esc(err.message)+'</div>';}\n  };\n  $('#rvPass').onclick=()=>send('pass');\n  $('#rvReject').onclick=()=>send('reject');\n}\n\nasync function renderLocation(seq){\n  setTitle('位置');\n  const info=await api('/api/location');\n  if(stale(seq))return;\n  const lm=info.lastMigration||null;const un=info.unmigrated||null;\n  $('#view').innerHTML=\n    '<div class=\"panel\"><h2>当前位置</h2>'+\n      '<table><tbody>'+\n      '<tr><th>KB 根目录</th><td class=\"mono\">'+esc(info.root)+'</td></tr>'+\n      '<tr><th>来源</th><td>'+esc(info.origin)+'</td></tr>'+\n      '<tr><th>配置文件</th><td class=\"mono\">'+esc(info.configFile)+(info.configExists?'':'（尚未写入）')+'</td></tr>'+\n      '<tr><th>库状态</th><td>'+(info.initialized?'已初始化（schema '+esc(info.schema||'')+'，'+esc(info.entries||0)+' 条）':'未初始化')+'</td></tr>'+\n      '</tbody></table>'+\n      (info.legacyHint?'<div class=\"notice warn\">'+esc(info.legacyHint)+'</div>':'')+\n      (un?'<div class=\"notice warn\">旧库未迁移：'+esc(un.from)+'（'+esc(un.entries)+' 条）<br>迁移命令：yotta-learn kb config set --dir '+esc(info.root)+' --move --from '+esc(un.from)+'</div>':'')+\n      (lm?'<div class=\"notice ok\">最近迁移：'+esc(lm.from)+' → '+esc(lm.to)+'（'+fmtTime(lm.at)+'，'+esc(lm.entries)+' 条 / '+esc(lm.categories)+' 分类）'+(lm.movedTo?'<br>旧库已移出：<span class=\"mono\">'+esc(lm.movedTo)+'</span>':'')+(lm.sourceLeftAt?'<br>旧库仍在原位：<span class=\"mono\">'+esc(lm.sourceLeftAt)+'</span>':'')+'</div>':'')+\n    '</div>'+\n    '<div class=\"panel\"><h2>切换 / 迁移位置</h2><div class=\"row\">'+\n      '<div class=\"field grow\"><label>目标目录</label><input id=\"locDir\" placeholder=\"D:\\\\AI_WorkDir\\\\.yottalearn\\\\knowledge\"></div>'+\n      '<div class=\"field\"><label>方式</label><select id=\"locMode\"><option value=\"move\">迁移（复制校验后切，旧库移出）</option><option value=\"switch\">仅切换（目标须已初始化）</option></select></div>'+\n      '<div class=\"field\"><label>确认串</label><input id=\"locConfirm\" placeholder=\"'+CONFIRM.locationMove+'\"></div>'+\n      '<button class=\"primary\" id=\"locBtn\">执行</button>'+\n    '</div><div class=\"notice warn\">迁移会先复制到暂存目录并做 doctor + 内容摘要双校验；校验失败不会切换配置、旧库不动。</div><div id=\"locNotice\"></div></div>';\n  const modeSel=$('#locMode');\n  const syncConfirm=()=>{$('#locConfirm').placeholder=modeSel.value==='move'?CONFIRM.locationMove:CONFIRM.locationSet;};\n  modeSel.onchange=syncConfirm;syncConfirm();\n  $('#locBtn').onclick=async()=>{\n    try{\n      const r=await act('location.set',{dir:$('#locDir').value.trim(),move:modeSel.value==='move',confirm:$('#locConfirm').value.trim()});\n      let msg='位置已更新：'+r.target;\n      if(r.movedTo)msg+='；旧库已移出：'+r.movedTo;\n      (r.warnings||[]).forEach(w=>toast(w,'err'));\n      toast(msg,'ok');await loadRootBadge();go('location');\n    }catch(e){$('#locNotice').innerHTML='<div class=\"notice err\">'+esc(e.message)+'</div>';}\n  };\n}\n\nasync function renderOps(seq){\n  setTitle('运维');\n  const d=await api('/api/ops'+(state.opsBackup?'?backup_dir='+encodeURIComponent(state.opsBackup):''));\n  if(stale(seq))return;\n  const checks=d.doctor.checks.map(c=>'<div class=\"checkline\"><span class=\"st '+esc(c.status)+'\">'+esc(c.status)+'</span><span>'+esc(c.name)+'：'+esc(c.detail||'')+'</span></div>').join('');\n  const trash=d.trash.map(t=>'<tr><td class=\"mono\">'+esc(t.name||t.id||'')+'</td><td>'+esc(t.age_days)+' 天</td></tr>').join('');\n  const snaps=d.snapshots.map(s=>'<tr><td class=\"mono\">'+esc(s.name)+'</td><td class=\"muted\">'+fmtTime(s.created||'')+'</td><td><button class=\"ghost\" data-restore=\"'+esc(s.name)+'\">恢复</button></td></tr>').join('');\n  const backups=d.backups.map(b=>'<tr><td class=\"mono\">'+esc(b.name)+'</td><td class=\"muted\">'+fmtTime(b.created||'')+'</td></tr>').join('');\n  $('#view').innerHTML=\n    '<div class=\"panel\"><h2>体检 <span class=\"hint\">错误 '+esc(d.doctor.errors)+' / 警告 '+esc(d.doctor.warnings)+'</span></h2><div class=\"checks\">'+checks+'</div>'+\n      '<div class=\"row\" style=\"margin-top:10px\"><div class=\"field\"><label>重建确认串</label><input id=\"idxConfirm\" placeholder=\"'+CONFIRM.indexRebuild+'\"></div><button class=\"ghost\" id=\"idxBtn\">重建索引</button></div></div>'+\n    '<div class=\"split\">'+\n      '<div class=\"panel\"><h2>回收站 <span class=\"hint\">'+esc(d.trash.length)+' 项</span></h2>'+\n        (trash?'<table><thead><tr><th>条目</th><th>存放</th></tr></thead><tbody>'+trash+'</tbody></table>':'<div class=\"empty\">空</div>')+\n        '<div class=\"row\" style=\"margin-top:10px\"><div class=\"field\"><label>清理确认串</label><input id=\"purgeConfirm\" placeholder=\"'+CONFIRM.trashPurge+'\"></div><label class=\"field\"><span><input type=\"checkbox\" id=\"purgeAll\"> 全部（忽略保留期）</span></label><button class=\"ghost\" id=\"purgeBtn\">清理</button></div></div>'+\n      '<div class=\"panel\"><h2>快照 <span class=\"hint\">'+esc(d.snapshots.length)+' 个</span></h2>'+\n        (snaps?'<table><thead><tr><th>名称</th><th>时间</th><th></th></tr></thead><tbody>'+snaps+'</tbody></table>':'<div class=\"empty\">暂无快照</div>')+\n        '<div class=\"row\" style=\"margin-top:10px\"><div class=\"field\"><label>恢复确认串</label><input id=\"snapConfirm\" placeholder=\"'+CONFIRM.snapshotRestore+'\"></div></div></div>'+\n    '</div>'+\n    '<div class=\"panel\"><h2>备份 <span class=\"hint\">独立目录</span></h2><div class=\"row\">'+\n      '<div class=\"field grow\"><label>备份目录</label><input id=\"bkOut\" value=\"'+esc(state.opsBackup||d.backup_dir||'')+'\" placeholder=\"D:\\\\YottaLearnBackups\"></div>'+\n      '<button class=\"ghost\" id=\"bkLoad\">读取</button><button class=\"primary\" id=\"bkCreate\">创建备份</button></div>'+\n      (backups?'<table style=\"margin-top:10px\"><thead><tr><th>备份</th><th>时间</th></tr></thead><tbody>'+backups+'</tbody></table>':'<div class=\"empty\">该目录暂无备份</div>')+'</div>';\n  $('#idxBtn').onclick=async()=>{\n    try{const r=await act('index.rebuild',{confirm:$('#idxConfirm').value.trim()});toast('索引已重建：'+r.total_entries+' 条 / '+r.terms+' 词条','ok');go('ops');}\n    catch(e){toast(e.message,'err');}\n  };\n  $('#purgeBtn').onclick=async()=>{\n    try{const r=await act('trash.purge',{confirm:$('#purgeConfirm').value.trim(),all:$('#purgeAll').checked});toast('回收站清理：删除 '+r.removed+' / 保留 '+r.kept,'ok');go('ops');}\n    catch(e){toast(e.message,'err');}\n  };\n  $('#view').querySelectorAll('button[data-restore]').forEach(b=>b.onclick=async()=>{\n    try{await act('snapshot.restore',{name:b.dataset.restore,confirm:$('#snapConfirm').value.trim()});toast('已恢复快照 '+b.dataset.restore,'ok');go('ops');}\n    catch(e){toast(e.message,'err');}\n  });\n  $('#bkLoad').onclick=()=>{state.opsBackup=$('#bkOut').value.trim();go('ops');};\n  $('#bkCreate').onclick=async()=>{\n    try{const r=await act('backup.create',{out:$('#bkOut').value.trim()});toast('已创建备份：'+r.dest,'ok');go('ops');}\n    catch(e){toast(e.message,'err');}\n  };\n}\n\n$('#btnRefresh').onclick=()=>go(state.view);\nrenderNav();loadRootBadge();go('overview');\n</script>\n</body>\n</html>\n"
# @generated view-html:end

CONFIRM = {
    "entry_deprecate": "entry-deprecate",
    "index_rebuild": "index-rebuild",
    "location_set": "location-set",
    "location_move": "location-move",
    "trash_purge": "trash-purge",
    "snapshot_restore": "snapshot-restore",
    "review_force": "review-force",
    "category_merge": "category-merge",
    "category_deprecate": "category-deprecate",
}

CSP = ("default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
       "connect-src 'self'; img-src 'self' data:; font-src 'self'; base-uri 'none'; "
       "form-action 'none'; frame-ancestors 'none'")


# ── 安全壳 ──────────────────────────────────────────────────────────────────

def host_allowed(host_header, port):
    """Host 头只允许 loopback（127.0.0.1 / localhost / [::1]，端口须一致）。"""
    host = str(host_header or "").strip().lower()
    if not host:
        return False
    if host.startswith("["):
        name, _, rest = host.partition("]")
        name = name + "]"
    else:
        name, _, rest = host.partition(":")
    if name not in ("127.0.0.1", "localhost", "[::1]"):
        return False
    if rest:
        return rest.isdigit() and int(rest) == int(port)
    return True


def origin_allowed(origin, host_header):
    """Origin（浏览器跨域标记）必须与请求 Host 严格一致；无 Origin 放行。"""
    if not origin:
        return True
    try:
        parsed = urlparse(str(origin))
    except ValueError:
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    origin_host = (parsed.netloc or "").lower()
    request_host = str(host_header or "").strip().lower()
    return bool(origin_host) and origin_host == request_host


def fetch_site_allowed(value):
    """Sec-Fetch-Site 只允许 same-origin / none（缺省放行，兼容旧客户端）。"""
    return str(value or "").strip().lower() in ("", "same-origin", "none")


def token_allowed(provided, token):
    if not provided or not token:
        return False
    return hmac.compare_digest(str(provided), str(token))


def _read_jsonl_tail(path, limit):
    p = Path(path)
    if not p.exists():
        return []
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    out = []
    for line in lines[-max(1, int(limit)):]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


# ── 上下文与只读负载 ────────────────────────────────────────────────────────

class ViewContext:
    def __init__(self, explicit_dir=None, token="", html=""):
        self.explicit_dir = explicit_dir
        self.token = token
        self.html = html
        self.lock = threading.Lock()

    def root(self):
        root, source = yotta_kb.resolve_kb_root(self.explicit_dir)
        yotta_kb.load_kb(root)
        return root, source


def overview_payload(ctx):
    root, source = ctx.root()
    stats = yotta_kb_index.stats(root)
    report = yotta_kb.doctor(root)
    return {
        "root": str(root), "origin": source, "version": VIEW_VERSION,
        "stats": stats,
        "doctor": {"errors": report["errors"], "warnings": report["warnings"],
                   "checks": report["checks"]},
        "audit": _read_jsonl_tail(yotta_kb.audit_path(root), 8),
    }


def categories_payload(ctx):
    root, source = ctx.root()
    cats = yotta_kb.list_categories(root)
    return {"root": str(root), "origin": source, "count": len(cats), "categories": cats}


def entries_payload(ctx, query):
    root, source = ctx.root()
    category = (query.get("category") or [""])[0].strip() or None
    if category:
        category = yotta_kb.resolve_category(root, category)["slug"]
    status = (query.get("status") or [""])[0].strip()
    tag = (query.get("tag") or [""])[0].strip().lower()
    limit = int((query.get("limit") or ["200"])[0] or 200)
    entries = []
    for entry in yotta_kb.iter_entries(root, category=category):
        if status and entry.status != status:
            continue
        if tag and tag not in [t.lower() for t in entry.tags]:
            continue
        entries.append(entry)
    entries.sort(key=lambda e: (e.updated, e.id), reverse=True)
    if limit > 0:
        entries = entries[:limit]
    return {"root": str(root), "origin": source, "count": len(entries),
            "entries": [e.to_dict() for e in entries]}


def search_payload(ctx, query):
    root, source = ctx.root()
    q = (query.get("q") or [""])[0].strip()
    if not q:
        raise yotta_kb.KbUsageError("搜索需要 q 参数（关键词）")
    statuses = None
    status = (query.get("status") or [""])[0].strip()
    if status:
        statuses = [s.strip() for s in status.split(",") if s.strip()]
    result = yotta_kb_index.query(
        root, q, category=((query.get("category") or [""])[0].strip() or None),
        statuses=statuses, tags=[t.strip() for t in (query.get("tag") or []) if t.strip()],
        limit=int((query.get("limit") or ["20"])[0] or 20),
        include_draft=(query.get("include_draft") or ["0"])[0] in ("1", "true", "yes"),
        include_deprecated=(query.get("include_deprecated") or ["0"])[0] in ("1", "true", "yes"))
    result["root"] = str(root)
    result["origin"] = source
    return result


def entry_payload(ctx, query):
    root, source = ctx.root()
    eid = (query.get("id") or [""])[0].strip()
    if not eid:
        raise yotta_kb.KbUsageError("需要 id 参数（KB-YYYYMMDD-XXX）")
    entry = yotta_kb.find_entry(root, eid)
    if entry is None:
        raise yotta_kb.KbNotFound("未找到条目：%s" % eid)
    data = entry.to_dict(include_body=True)
    data["path"] = str(entry.path)
    data["root"] = str(root)
    data["origin"] = source
    return data


def location_payload(ctx):
    info = yotta_kb.location_info(ctx.explicit_dir)
    return info


def ops_payload(ctx, query):
    root, source = ctx.root()
    backup_dir = (query.get("backup_dir") or [""])[0].strip() or None
    report = yotta_kb.doctor(root, backup_dir=backup_dir)
    return {
        "root": str(root), "origin": source,
        "doctor": {"errors": report["errors"], "warnings": report["warnings"],
                   "checks": report["checks"]},
        "trash": yotta_kb.list_trash(root),
        "snapshots": yotta_kb.list_snapshots(root),
        "backup_dir": backup_dir,
        "backups": yotta_kb.backup_list(backup_dir) if backup_dir else [],
    }


def audit_payload(ctx, query):
    root, source = ctx.root()
    limit = int((query.get("limit") or ["50"])[0] or 50)
    limit = max(1, min(limit, AUDIT_TAIL_LIMIT))
    return {"root": str(root), "origin": source, "limit": limit,
            "records": _read_jsonl_tail(yotta_kb.audit_path(root), limit)}


def cli_payload(ctx):
    """高级 / CLI：命令面单一真源（结构化模型 + argparse 帮助 + 常用命令速查）。"""
    return {"version": VIEW_VERSION,
            "quick": yotta_learn.cli_quick_commands(),
            "groups": yotta_learn.cli_help_model(),
            "full": yotta_learn.cli_help_text()}


# ── 写操作（内核同一真源 + 审计） ───────────────────────────────────────────

def _need_confirm(body, key):
    if str(body.get("confirm") or "") != CONFIRM[key]:
        raise yotta_kb.KbUsageError('确认串不匹配（需要 "%s"）' % CONFIRM[key])


def execute_action(ctx, body):
    if not isinstance(body, dict):
        raise yotta_kb.KbUsageError("请求体必须是 JSON 对象")
    action = str(body.get("action") or "").strip()
    root, _source = ctx.root()
    actor = yotta_kb.resolve_actor("view")
    target = ""
    detail = {}

    if action == "category.create":
        slug = str(body.get("slug") or "").strip()
        name = str(body.get("name") or "").strip()
        description = str(body.get("description") or "").strip()
        aliases = body.get("aliases") or []
        if isinstance(aliases, str):
            aliases = [a.strip() for a in aliases.split(",") if a.strip()]
        cat = yotta_kb.create_category(root, slug, name, description, aliases, actor)
        target = cat["slug"]
        detail = {"name": cat["name"]}
        result = {"slug": cat["slug"], "name": cat["name"]}

    elif action == "category.rename":
        slug = str(body.get("slug") or "").strip()
        new_name = str(body.get("name") or "").strip()
        cat = yotta_kb.rename_category(root, slug, new_name, actor)
        target = cat["slug"]
        detail = {"name": cat["name"]}
        result = {"slug": cat["slug"], "name": cat["name"]}

    elif action == "category.merge":
        _need_confirm(body, "category_merge")
        from_slug = str(body.get("from") or "").strip()
        into_slug = str(body.get("into") or "").strip()
        merged = yotta_kb.merge_category(root, from_slug, into_slug, actor)
        target = merged["from"]
        detail = {"into": merged["into"], "moved": merged["moved"]}
        result = {"from": merged["from"], "into": merged["into"], "moved": merged["moved"]}

    elif action == "category.deprecate":
        _need_confirm(body, "category_deprecate")
        slug = str(body.get("slug") or "").strip()
        force = bool(body.get("force"))
        cat = yotta_kb.deprecate_category(root, slug, actor,
                                          body.get("reason") or "", force=force)
        target = cat["slug"]
        detail = {"reason": body.get("reason") or "", "force": force}
        result = {"slug": cat["slug"], "status": cat["status"]}

    elif action == "entry.add":
        tags = body.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        entry = yotta_kb.add_entry(
            root, str(body.get("category") or "").strip(),
            str(body.get("title") or "").strip(), body.get("message") or "",
            tags, body.get("source") or "", body.get("evidence") or "",
            str(body.get("confidence") or "medium"), actor)
        text = "\n".join([entry.title, " ".join(entry.tags), entry.body])
        target = entry.id
        detail = {"category": entry.category}
        result = {"id": entry.id, "status": entry.status,
                  "sensitive": yotta_kb.scan_sensitive(text),
                  "similar": yotta_kb.similar_titles(root, entry)}

    elif action == "entry.review":
        eid = str(body.get("id") or "").strip()
        decision = str(body.get("decision") or "").strip().lower()
        force = bool(body.get("force"))
        if force:
            _need_confirm(body, "review_force")
        entry, extra = yotta_kb.review_entry(
            root, eid, decision, body.get("note") or "",
            body.get("evidence") or "", actor, force=force)
        target = entry.id
        detail = {"decision": decision, "force": force}
        result = {"id": entry.id, "status": entry.status,
                  "findings": extra.get("findings") or [],
                  "similar": extra.get("similar") or []}

    elif action == "entry.update":
        eid = str(body.get("id") or "").strip()
        changes = {}
        for key in ("title", "message", "source", "evidence", "confidence"):
            if body.get(key) is not None:
                changes[key] = body[key]
        if body.get("tags") is not None:
            tags = body.get("tags")
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",") if t.strip()]
            changes["tags"] = tags
        if not changes:
            raise yotta_kb.KbUsageError("至少需要一个可更新字段")
        entry = yotta_kb.update_entry(root, eid, changes, actor)
        target = entry.id
        detail = {"fields": sorted(changes.keys())}
        result = {"id": entry.id, "updated": sorted(changes.keys())}

    elif action == "entry.deprecate":
        _need_confirm(body, "entry_deprecate")
        entry = yotta_kb.deprecate_entry(root, str(body.get("id") or "").strip(),
                                         body.get("reason") or "", actor)
        target = entry.id
        result = {"id": entry.id, "status": entry.status}

    elif action == "index.rebuild":
        _need_confirm(body, "index_rebuild")
        with yotta_kb.KbLock(root):
            stats = yotta_kb_index.rebuild_all(root)
        target = str(root)
        detail = {"entries": stats["total_entries"], "terms": stats["terms"]}
        result = {"total_entries": stats["total_entries"], "terms": stats["terms"]}

    elif action == "location.set":
        move = bool(body.get("move"))
        _need_confirm(body, "location_move" if move else "location_set")
        target_dir = str(body.get("dir") or "").strip()
        if not target_dir:
            raise yotta_kb.KbUsageError("location.set 需要 dir 参数（目标位置）")
        if not move and not yotta_kb.is_initialized(Path(target_dir).expanduser().resolve()):
            raise yotta_kb.KbIntegrityError(
                "目标位置未初始化；如要迁往新位置请使用迁移（move=true）")
        current_root, _src = yotta_kb.resolve_kb_root(ctx.explicit_dir)
        result = yotta_kb.set_location(target_dir, move=move, current_root=current_root)
        ctx.explicit_dir = result["target"]  # 会话内立即切到新位置
        root = Path(result["target"]).resolve()  # 迁移后的审计写入新库
        target = result["target"]
        detail = {"move": move, "from": result["source"]}

    elif action == "trash.purge":
        _need_confirm(body, "trash_purge")
        days = int(body.get("days") or yotta_kb.TRASH_RETENTION_DAYS)
        result = yotta_kb.purge_trash(root, actor, days=days,
                                      purge_all=bool(body.get("all")))
        target = str(root)
        detail = dict(result)

    elif action == "snapshot.restore":
        _need_confirm(body, "snapshot_restore")
        name = yotta_kb.restore_snapshot(root, str(body.get("name") or "").strip(), actor)
        target = name
        result = {"restored": name}

    elif action == "backup.create":
        out = str(body.get("out") or "").strip()
        if not out:
            raise yotta_kb.KbUsageError("backup.create 需要 out 参数（独立备份目录）")
        dest, manifest = yotta_kb.backup_create(root, out, actor)
        target = str(dest)
        detail = {"entries": manifest["entries"]}
        result = {"dest": str(dest), "entries": manifest["entries"],
                  "files": len(manifest["files"])}

    else:
        raise yotta_kb.KbUsageError("未知操作：%s" % (action or "(空)"))

    yotta_kb.audit(root, actor, "view." + action, target, "ok", detail)
    result["action"] = action
    return result


# ── HTTP ────────────────────────────────────────────────────────────────────

def _kb_http_code(exc):
    if isinstance(exc, yotta_kb.KbUsageError):
        return 400
    if isinstance(exc, yotta_kb.KbGateError):
        return 409
    if isinstance(exc, yotta_kb.KbIntegrityError):
        return 409
    if isinstance(exc, yotta_kb.KbNotFound):
        return 404
    return 500


class ViewHandler(BaseHTTPRequestHandler):
    server_version = "yotta-learn-view/" + VIEW_VERSION
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # noqa: A003
        if os.environ.get("YOTTA_LEARN_VIEW_DEBUG"):
            sys.stderr.write("[view] " + (fmt % args) + "\n")

    # -- 基础输出 --

    def _send(self, code, body, content_type, extra_headers=None):
        data = body if isinstance(body, bytes) else str(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        for key, value in (extra_headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            try:
                self.wfile.write(data)
            except OSError:
                pass

    def _json(self, code, payload):
        self._send(code, json.dumps(payload, ensure_ascii=False), "application/json; charset=utf-8")

    def _text(self, code, text):
        self._send(code, text, "text/plain; charset=utf-8")

    def _html(self, html):
        self._send(200, html, "text/html; charset=utf-8", {
            "Content-Security-Policy": CSP,
            "X-Frame-Options": "DENY",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
        })

    def _drain_body(self, limit=1 << 20, timeout=None):
        """读掉未处理的请求体（有界 + 有超时），避免 Windows RST 与阻塞挂线程（BUG-L-02 / BUG-L-03）。"""
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return
        remaining = max(0, min(length, limit))
        if remaining <= 0:
            return
        budget = DRAIN_TIMEOUT_SECONDS if timeout is None else timeout
        original = self.connection.gettimeout()
        deadline = time.monotonic() + budget
        try:
            while remaining > 0:
                left = deadline - time.monotonic()
                if left <= 0:
                    self.close_connection = True
                    break
                self.connection.settimeout(left)
                try:
                    chunk = self.rfile.read(min(remaining, 65536))
                except OSError:
                    # 读超时 / 套接字异常：放弃排空并关闭连接，不再等待（BUG-L-03）
                    self.close_connection = True
                    break
                if not chunk:
                    break
                remaining -= len(chunk)
        finally:
            try:
                self.connection.settimeout(original)
            except OSError:
                pass

    # -- 安全壳 --

    def _guard(self):
        ctx = self.server.view_ctx  # type: ignore[attr-defined]
        if (not host_allowed(self.headers.get("Host"), self.server.server_port)
                or not origin_allowed(self.headers.get("Origin"), self.headers.get("Host"))
                or not fetch_site_allowed(self.headers.get("Sec-Fetch-Site"))):
            if self.command == "POST":
                self._drain_body()
            self._text(403, "forbidden")
            return False
        return ctx

    # -- 路由 --

    def do_GET(self):  # noqa: N802
        ctx = self._guard()
        if not ctx:
            return
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        if path == "/":
            return self._html(ctx.html)
        if path == "/favicon.ico":
            return self._send(204, b"", "image/x-icon")
        routes = {
            "/api/overview": lambda: overview_payload(ctx),
            "/api/categories": lambda: categories_payload(ctx),
            "/api/entries": lambda: entries_payload(ctx, query),
            "/api/search": lambda: search_payload(ctx, query),
            "/api/entry": lambda: entry_payload(ctx, query),
            "/api/location": lambda: location_payload(ctx),
            "/api/ops": lambda: ops_payload(ctx, query),
            "/api/audit": lambda: audit_payload(ctx, query),
            "/api/cli": lambda: cli_payload(ctx),
        }
        handler = routes.get(path)
        if handler is None:
            return self._text(404, "not found")
        try:
            return self._json(200, handler())
        except yotta_kb.KbError as exc:
            return self._json(_kb_http_code(exc), {"error": exc.message, "code": exc.code})
        except Exception as exc:  # noqa: BLE001
            return self._json(500, {"error": str(exc)})

    def do_POST(self):  # noqa: N802
        ctx = self._guard()
        if not ctx:
            return
        parsed = urlparse(self.path)
        if parsed.path != "/api/action":
            self._drain_body()
            return self._text(404, "not found")
        if not token_allowed(self.headers.get(TOKEN_HEADER), ctx.token):
            self._drain_body()
            return self._json(403, {"error": "写操作需要有效的本机会话令牌；"
                                             "请从 yotta-learn view 页面操作。"})
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            # 长度未知无法可靠排空：标记连接不复用，尽量降低 RST 影响
            self.close_connection = True
            return self._json(400, {"error": "Content-Length 非法"})
        if length <= 0:
            return self._json(400, {"error": "请求体为空"})
        if length > BODY_LIMIT:
            # 丢弃超量请求体（上限 1 MB），避免污染 keep-alive 连接
            self._drain_body()
            return self._json(413, {"error": "请求体过大（上限 %d 字节）" % BODY_LIMIT})
        raw = self.rfile.read(length)
        try:
            body = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return self._json(400, {"error": "请求体不是合法 JSON"})
        with ctx.lock:
            try:
                result = execute_action(ctx, body)
            except yotta_kb.KbError as exc:
                return self._json(_kb_http_code(exc), {"error": exc.message, "code": exc.code})
            except Exception as exc:  # noqa: BLE001
                return self._json(500, {"error": str(exc)})
        return self._json(200, result)


# ── 启动 ────────────────────────────────────────────────────────────────────

def load_html():
    """面板模板：嵌入副本为运行时真源（精简分发副本不带 assets/，仍可直接服务）。

    assets/view.html 是编辑真源，由 tools/sync_learn_view_html.py 同步；
    漂移由 test_yotta_learn_view.py 与 preflight-publish.py 双向门禁拦截。
    """
    if not VIEW_HTML_EMBEDDED:
        raise yotta_kb.KbIntegrityError(
            "面板资源缺失：嵌入模板为空（先运行 python tools/sync_learn_view_html.py）")
    return VIEW_HTML_EMBEDDED


def render_html(source, token):
    html = str(source or "")
    if TOKEN_PLACEHOLDER in html:
        return html.replace(TOKEN_PLACEHOLDER, token)
    meta = '<meta name="yotta-view-token" content="%s">' % token
    if "</head>" in html:
        return html.replace("</head>", meta + "</head>")
    return meta + html


class ViewHTTPServer(ThreadingHTTPServer):
    """本地面板服务器：禁用地址复用（防 Windows 同端口双绑，BUG-L-01）。"""

    allow_reuse_address = False
    daemon_threads = True


def create_view_server(root_dir=None, port=DEFAULT_PORT, token=None):
    """创建（未启动）本地面板服务器；返回 (server, token, url)。"""
    requested = token or secrets.token_urlsafe(24)
    safe_token = requested if token_format_ok(requested) else secrets.token_urlsafe(24)
    html = render_html(load_html(), safe_token)
    ctx = ViewContext(explicit_dir=root_dir, token=safe_token, html=html)
    # fail-closed：启动前确认当前位置是可用知识库
    ctx.root()
    try:
        server = ViewHTTPServer((DEFAULT_HOST, int(port)), ViewHandler)
    except OSError as exc:
        raise yotta_kb.KbUsageError(
            "端口 %s 已被占用，可能已有面板在运行；请换一个端口"
            "（yotta-learn view --port <其它端口>），或先关闭已有面板。（%s）"
            % (port, exc)
        ) from exc
    server.view_ctx = ctx  # type: ignore[attr-defined]
    actual_port = server.server_address[1]
    return server, safe_token, "http://%s:%d/" % (DEFAULT_HOST, actual_port)


def token_format_ok(value):
    return bool(re.match(r"^[A-Za-z0-9_-]{8,128}$", str(value or "")))


def serve(root_dir=None, port=DEFAULT_PORT):
    server, token, url = create_view_server(root_dir=root_dir, port=port)
    root, source = server.view_ctx.root()  # type: ignore[attr-defined]
    print("元习知识库管理台已启动：%s" % url, flush=True)
    print("  KB: %s（来源: %s）" % (root, source), flush=True)
    print("  安全: 仅本机 127.0.0.1 / 页面内嵌会话令牌 / 写操作需确认串", flush=True)
    print("  退出: Ctrl+C", flush=True)
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        print("\n已停止。")
    finally:
        server.server_close()
    return 0
