# -*- coding: utf-8 -*-
"""全流程量化策略工作台 - 需求→策略→回测→结果 实时监控"""
import sys, os, json, time, threading, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

STATE = {"run_id": "", "status": "waiting", "stage": "", "pct": 0, "dates": [], "points": [],
    "stats": {}, "logs": [], "done": False, "steps": {}, "requirement": {}, "code": "",
    "code_file": "", "final": None, "trades": None, "positions": None, "position_snapshots": [], "bench_data": None, "report_urls": {}, "error": None, "result_warnings": None, "_ts": 0}
LOCK = threading.Lock()
CLIENTS = []

def _slim_state():
    """返回轻量状态快照（去掉大体积字段）用于 /api/state 和轮询"""
    with LOCK: s = dict(STATE)
    req = s.get("requirement", {})
    slim_req = {k: (f"{len(v)}只" if k == "symbols" and isinstance(v, list) else v) for k, v in (req.items() if isinstance(req, dict) else [])}
    return {"run_id": s.get("run_id", ""), "status": s.get("status", "waiting"), "stage": s.get("stage", ""), "pct": s.get("pct", 0),
        "done": s.get("done", False), "steps": s.get("steps", {}), "stats": s.get("stats", {}), "logs": s.get("logs", [])[-20:],
        "has_code": bool(s.get("code")), "code_file": s.get("code_file", ""), "has_curve": bool(s.get("final") or s.get("points")),
        "has_trades": s.get("trades") is not None and len(s.get("trades", [])) > 0, "trade_count": len(s.get("trades") or []),
        "point_count": len(s.get("points", [])) or len((s.get("final") or {}).get("navs", [])), "requirement_summary": slim_req, "report_urls": s.get("report_urls", {}),
        "error": s.get("error"), "result_warnings": s.get("result_warnings"), "ts": s.get("_ts", 0)}

def broadcast(event, data):
    msg = f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n".encode()
    with LOCK:
        STATE["_ts"] = int(time.time())
        dead = []
        for wfile in CLIENTS[:]:
            try: wfile.write(msg); wfile.flush()
            except Exception: dead.append(wfile)
        for d in dead:
            try: CLIENTS.remove(d)
            except ValueError: pass

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>策略监控</title>
<script defer src="https://cdn.bootcdn.net/ajax/libs/echarts/5.5.0/echarts.min.js" onerror="this.onerror=function(){this.onerror=null;this.src='https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js'};this.src='https://unpkg.com/echarts@5.5.0/dist/echarts.min.js'"></script>
<link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css" onerror="this.onerror=null;this.href='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/atom-one-light.min.css'">
<script defer src="https://cdn.bootcdn.net/ajax/libs/highlight.js/11.9.0/highlight.min.js" onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js'"></script>
<script defer src="https://cdn.bootcdn.net/ajax/libs/highlight.js/11.9.0/languages/python.min.js" onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/languages/python.min.js'"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:linear-gradient(180deg,#e8f4f8,#f0f9ff);min-height:100vh;color:#1e293b}
.hdr{padding:20px 32px;display:flex;align-items:center;gap:16px;background:#fff;border-bottom:1px solid #dbeafe}
.hdr h1{font-size:22px;font-weight:700;color:#1e40af}
.hdr .rid{font-size:12px;color:#64748b;font-family:monospace;margin-left:auto;background:#f1f5f9;padding:6px 14px;border-radius:8px}
.hdr .pill{padding:6px 16px;border-radius:20px;font-size:13px;font-weight:700}
.pill-w{background:#fef3c7;color:#d97706;border:1px solid #fcd34d}
.pill-r{background:#dbeafe;color:#2563eb;border:1px solid #93c5fd;animation:pulse 1.5s infinite}
.pill-s{background:#dcfce7;color:#16a34a;border:1px solid #86efac}
.pill-f{background:#fee2e2;color:#dc2626;border:1px solid #fca5a5}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.tl{display:flex;align-items:center;justify-content:center;padding:14px 32px;background:#fff;border-bottom:1px solid #e2e8f0;gap:0}
.tl-s{display:flex;flex-direction:column;align-items:center;gap:4px;z-index:1}
.tl-d{width:32px;height:32px;border-radius:50%;background:#e2e8f0;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#94a3b8;transition:all .3s}
.tl-d.run{background:#dbeafe;color:#2563eb;animation:pulse 1.5s infinite}
.tl-d.ok{background:#dcfce7;color:#16a34a}
.tl-d.warn{background:#fef3c7;color:#d97706}
.tl-d.err{background:#fee2e2;color:#dc2626}
.tl-t{font-size:11px;color:#64748b;font-weight:600;white-space:nowrap}
.tl-ln{flex:1;height:2px;background:#e2e8f0;min-width:48px;transition:background .3s}
.tl-ln.ok{background:#86efac}
.rpt-ban{display:none;padding:14px 32px;background:linear-gradient(90deg,#dcfce7,#d1fae5);border-bottom:1px solid #86efac;text-align:center;font-size:14px;font-weight:600;color:#166534}
.rpt-ban a{color:#1e40af;text-decoration:underline;margin-left:12px;font-weight:700}
.err-card{display:none;margin:0 auto 20px;max-width:1200px;padding:0 20px}
.err-inner{background:linear-gradient(135deg,#fef2f2,#fff1f2);border:2px solid #fca5a5;border-radius:16px;padding:24px;box-shadow:0 4px 16px rgba(220,38,38,.1)}
.err-inner h3{color:#dc2626;font-size:18px;font-weight:800;margin-bottom:8px;display:flex;align-items:center;gap:8px}
.err-type{display:inline-block;background:#dc2626;color:#fff;font-size:11px;padding:3px 10px;border-radius:6px;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.err-msg{color:#7f1d1d;font-size:14px;margin:12px 0;line-height:1.6}
.err-tb{background:#1e1e1e;color:#f1f5f9;font-size:12px;padding:14px;border-radius:10px;max-height:200px;overflow:auto;font-family:'Cascadia Code','Fira Code',monospace;line-height:1.5;margin:12px 0;display:none}
.err-toggle{background:none;border:1px solid #fca5a5;color:#dc2626;padding:6px 14px;border-radius:8px;cursor:pointer;font-size:12px;font-weight:600}
.err-toggle:hover{background:#fee2e2}
.err-guide{margin-top:16px;padding:16px 20px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border-radius:12px;border:1px solid #93c5fd;color:#1e40af;font-size:14px;line-height:1.7}
.err-guide strong{color:#1e3a8a;font-size:15px}
.warn-card{display:none;margin:0 auto 20px;max-width:1200px;padding:0 20px}
.warn-inner{background:linear-gradient(135deg,#fefce8,#fef9c3);border:2px solid #fcd34d;border-radius:16px;padding:24px;box-shadow:0 4px 16px rgba(217,119,6,.1)}
.warn-inner h3{color:#d97706;font-size:18px;font-weight:800;margin-bottom:8px;display:flex;align-items:center;gap:8px}
.warn-inner ul{color:#92400e;font-size:14px;margin:12px 0;line-height:1.8;list-style:disc;padding-left:20px}
.warn-inner .warn-hint{padding:12px;background:linear-gradient(135deg,#fffbeb,#fef3c7);border-radius:10px;border:1px solid #fde68a;font-size:13px;color:#92400e;margin-top:12px}
.wrap{max-width:1200px;margin:0 auto;padding:24px 20px}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:16px;margin-bottom:20px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.card-h{padding:16px 20px;display:flex;align-items:center;gap:12px;background:#f8fafc;border-bottom:1px solid #e2e8f0}
.card-h .title{font-size:16px;font-weight:700;color:#1e293b}
.card-h .badge{margin-left:auto;padding:4px 12px;border-radius:12px;font-size:12px;font-weight:600}
.card-b{padding:20px}
.card-b.empty{color:#94a3b8;font-style:italic;font-size:14px;text-align:center;padding:40px 20px}
.req-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}
.req-item{background:#f8fafc;border-radius:10px;padding:14px;border:1px solid #e2e8f0}
.req-item .k{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.req-item .v{font-size:14px;font-weight:600;margin-top:6px;color:#1e293b}
.code-wrap{background:#fafafa;border-radius:12px;border:1px solid #e2e8f0;overflow:hidden}
.code-h{padding:12px 16px;background:#f1f5f9;border-bottom:1px solid #e2e8f0;font-size:12px;color:#64748b;display:flex;align-items:center;gap:8px}
.code-h svg{width:16px;height:16px}
.code-h .spacer{flex:1}
.code-btn{padding:4px 12px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;font-size:12px;color:#475569;cursor:pointer;transition:all .15s;display:inline-flex;align-items:center;gap:4px}
.code-btn:hover{background:#f1f5f9;border-color:#94a3b8;color:#1e293b}
.code-btn:active{transform:scale(.96)}
.code-btn.copied{background:#dcfce7;border-color:#86efac;color:#16a34a}
pre.code-block{background:#fafafa;margin:0;padding:16px;font-size:13px;max-height:420px;overflow:auto;line-height:1.7}
pre.code-block code{font-family:'Cascadia Code','Fira Code','Consolas',monospace}
.progress-outer{height:8px;background:#e2e8f0;border-radius:4px;overflow:hidden}
.progress-inner{height:100%;border-radius:4px;background:linear-gradient(90deg,#3b82f6,#06b6d4);transition:width .5s ease}
#chart{width:100%;height:380px}
#dailyChart{width:100%;height:280px}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}
.sc{background:#f8fafc;border-radius:12px;padding:16px;text-align:center;border:1px solid #e2e8f0;transition:transform .15s}
.sc:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,.06)}
.sc .lb{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.sc .vl{font-size:22px;font-weight:800;margin-top:6px}
.sc .vl.pos{color:#dc2626}.sc .vl.neg{color:#16a34a}.sc .vl.neu{color:#475569}
.trade-table{width:100%;border-collapse:collapse;font-size:13px}
.trade-table th{background:#f8fafc;color:#64748b;font-weight:600;text-align:left;padding:12px 14px;border-bottom:2px solid #e2e8f0;font-size:11px;text-transform:uppercase}
.trade-table td{padding:12px 14px;border-bottom:1px solid #f1f5f9;color:#1e293b}
.trade-table tr:hover{background:#f8fafc}
.trade-table .buy{color:#dc2626;font-weight:600}.trade-table .sell{color:#16a34a;font-weight:600}
.page-nav{display:flex;justify-content:center;gap:8px;margin-top:16px}
.page-nav button{padding:8px 14px;border:1px solid #e2e8f0;background:#fff;border-radius:8px;cursor:pointer;font-size:13px;color:#475569}
.page-nav button:hover{background:#f1f5f9}
.page-nav button.active{background:#3b82f6;color:#fff;border-color:#3b82f6}
.page-nav button:disabled{opacity:.4;cursor:not-allowed}
.log-box{background:#f8fafc;border-radius:12px;padding:14px;max-height:140px;overflow-y:auto;font-size:11.5px;font-family:'Cascadia Code','Fira Code',monospace;color:#64748b;border:1px solid #e2e8f0}
</style></head><body>
<div class="hdr">
  <div style="font-size:28px">📊</div><h1>量化策略监控</h1>
  <span class="rid" id="rid">-</span>
  <span class="pill pill-w" id="gpill">连接中...</span>
  <span style="font-size:11px;color:#94a3b8;margin-left:8px" id="_hb"></span>
</div>
<div class="tl">
  <div class="tl-s"><div class="tl-d" id="td1">1</div><div class="tl-t">需求确认</div></div>
  <div class="tl-ln" id="tln1"></div>
  <div class="tl-s"><div class="tl-d" id="td2">2</div><div class="tl-t">策略生成</div></div>
  <div class="tl-ln" id="tln2"></div>
  <div class="tl-s"><div class="tl-d" id="td3">3</div><div class="tl-t">回测执行</div></div>
  <div class="tl-ln" id="tln3"></div>
  <div class="tl-s"><div class="tl-d" id="td4">4</div><div class="tl-t">结果展示</div></div>
</div>
<div class="rpt-ban" id="rptBan">✅ 回测完成 <a id="rptLink" href="#" target="_blank">查看完整报告 →</a></div>
<div class="err-card" id="errCard"><div class="err-inner">
  <h3>⚠️ 执行失败 <span class="err-type" id="errType">ERROR</span></h3>
  <div class="err-msg" id="errMsg"></div>
  <button class="err-toggle" onclick="var t=document.getElementById('errTb');t.style.display=t.style.display==='none'?'block':'none'">展开详细堆栈</button>
  <div class="err-tb" id="errTb"></div>
  <div class="err-guide"><strong>如何处理？</strong><br>请回到对话页输入「查看结果」，AI 将为您诊断错误原因并尝试修复。<br>您也可以输入「重新生成」让 AI 重新生成策略代码。</div>
</div></div>
<div class="warn-card" id="warnCard"><div class="warn-inner">
  <h3>⚠️ 结果校验告警</h3>
  <ul id="warnList"></ul>
  <div class="warn-hint">💡 请回到对话页输入「查看结果」，AI 将分析告警原因并尝试修复策略逻辑。</div>
</div></div>
<div class="wrap">
  <div class="card" id="p1">
    <div class="card-h"><span class="title">📋 策略描述</span><span class="badge pill-w" id="b1">等待</span></div>
    <div class="card-b empty" id="c1">等待策略描述...</div>
  </div>
  <div class="card" id="p2">
    <div class="card-h"><span class="title">💻 策略代码</span><span class="badge pill-w" id="b2">等待</span></div>
    <div class="card-b empty" id="c2">等待策略代码生成...</div>
  </div>
  <div class="card" id="p3">
    <div class="card-h"><span class="title">📈 收益曲线图</span><span class="badge pill-w" id="b3">等待</span></div>
    <div class="card-b"><div class="progress-outer"><div class="progress-inner" id="bar3" style="width:0%"></div></div><div id="chart"></div></div>
  </div>
  <div class="card" id="p4">
    <div class="card-h"><span class="title">📊 每日收益图</span><span class="badge pill-w" id="b4">等待</span></div>
    <div class="card-b"><div id="dailyChart"></div></div>
  </div>
  <div class="card" id="p5">
    <div class="card-h"><span class="title">📉 回测结果统计</span><span class="badge pill-w" id="b5">等待</span></div>
    <div class="card-b empty" id="c5">等待回测完成...</div>
  </div>
  <div class="card" id="p-conclusion" style="display:none">
    <div class="card-h"><span class="title">🏆 策略体检</span><span class="badge pill-s" id="b-conclusion">评估</span></div>
    <div class="card-b" id="c-conclusion"></div>
  </div>
  <div class="card" id="p6">
    <div class="card-h"><span class="title">📝 交易记录</span></div>
    <div class="card-b" id="c6"><div class="empty">暂无交易记录</div></div>
    <div class="page-nav" id="pageNav" style="display:none"></div>
  </div>
  <div class="card" id="p7">
    <div class="card-h"><span class="title">📦 每日持仓变化</span></div>
    <div class="card-b" id="c7"><div class="empty">等待持仓数据...</div></div>
  </div>
  <div style="font-size:12px;color:#64748b;padding:0 4px;margin-top:16px">
    <strong>📌 日志</strong>
    <div class="log-box" id="logs">系统就绪，等待连接...</div>
  </div>
  <div style="font-size:12px;color:#94a3b8;text-align:right;padding:10px 4px 0">
    Powered by <a href="https://quantgo.ai/data" target="_blank" style="color:#2563eb;text-decoration:underline">QuantGo</a>
  </div>
</div>
<script>
const RID=location.pathname.split('/').pop()||'';
document.getElementById('rid').textContent='run: '+RID;
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function setBadge(id,st){const e=document.getElementById(id);if(!e)return;e.className='badge '+({running:'pill-r',success:'pill-s',failed:'pill-f',warning:'pill-w'}[st]||'pill-w');e.textContent={pending:'等待',running:'进行中',success:'完成',failed:'失败',warning:'告警'}[st]||st}
function setTL(n,st){
  const map={1:[1],2:[2],3:[2],4:[3],5:[4],6:[4],9:[4]};
  (map[n]||[]).forEach(d=>{const el=document.getElementById('td'+d);if(!el)return;
    if(st==='running'){el.className='tl-d run'}
    else if(st==='success'){el.className='tl-d ok';el.textContent='✓';const ln=document.getElementById('tln'+d);if(ln)ln.className='tl-ln ok'}
    else if(st==='warning'){el.className='tl-d warn';el.textContent='⚠'}
    else if(st==='failed'){el.className='tl-d err';el.textContent='✗'}
  })
}
function addLog(m){const e=document.getElementById('logs');const ml=m.replace(/(https?:\/\/[^\s<]+)/g,'<a href="$1" target="_blank" style="color:#2563eb">$1</a>');e.innerHTML+='<div>['+new Date().toLocaleTimeString()+'] '+ml+'</div>';e.scrollTop=e.scrollHeight}
let chart=null,dailyChart=null,_chartOk=false;
function _ensureChart(){ //确定性渲染：从API拉取完整数据，不依赖SSE事件时序
  if(_chartOk||!chart)return;
  fetch('/api/chart?run_id='+RID).then(r=>r.json()).then(ch=>{
    if(!ch||!ch.navs||ch.navs.length===0)return;
    chartOpt.xAxis.data=ch.dates;chartOpt.series[0].data=ch.navs;chartOpt.series[1].data=ch.bench||[];
    chart.setOption(chartOpt,true);chart.resize();_chartOk=true;
    const daily=[],dds=[];
    for(let i=1;i<ch.navs.length;i++){const p=ch.navs[i-1]||1;daily.push(parseFloat(((ch.navs[i]-p)/p*100).toFixed(3)));dds.push(ch.dates[i])}
    dailyOpt.xAxis.data=dds;dailyOpt.series[0].data=daily;
    if(dailyChart){dailyChart.setOption(dailyOpt,true);dailyChart.resize();setBadge('b4','success')}
    setTimeout(()=>{if(chart){chart.resize();chart.setOption(chartOpt,true)}if(dailyChart){dailyChart.resize();dailyChart.setOption(dailyOpt,true)}},500) //延迟二次强制重绘
  }).catch(()=>{})}
let _echartsRetry=0;
function _initCharts(){
  if(chart)return;
  if(typeof echarts==='undefined'){_echartsRetry++;
    if(_echartsRetry>=35){const ce=document.getElementById('chart');if(ce&&!ce.querySelector('.chart-fallback')){ce.innerHTML='<div class="chart-fallback" style="display:flex;align-items:center;justify-content:center;height:100%;color:#94a3b8;flex-direction:column"><p>图表库加载超时</p><button onclick="location.reload()" style="margin-top:8px;padding:6px 16px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;cursor:pointer;color:#3b82f6">点击刷新</button></div>'}}
    setTimeout(_initCharts,500);return}
  try{chart=echarts.init(document.getElementById('chart'),null,{renderer:'canvas'});dailyChart=echarts.init(document.getElementById('dailyChart'),null,{renderer:'canvas'});
    if(chart){chart.setOption(chartOpt);chart.resize()}if(dailyChart){dailyChart.setOption(dailyOpt);dailyChart.resize()}addLog('📈 图表库加载完成');_ensureChart();
    setTimeout(()=>{if(chart)chart.resize();if(dailyChart)dailyChart.resize()},300);
    setTimeout(()=>{if(chart&&!_chartOk)_ensureChart()},2000)}catch(e){addLog('⚠️ 图表库初始化失败('+e.message+')')}
}
setTimeout(_initCharts,100);
window.addEventListener('resize',()=>{if(chart)chart.resize();if(dailyChart)dailyChart.resize()});
document.addEventListener('visibilitychange',()=>{if(!document.hidden&&chart){chart.resize();_ensureChart();if(dailyChart)dailyChart.resize()}});
window.addEventListener('load',()=>{setTimeout(()=>{if(chart){chart.resize();if(!_chartOk)_ensureChart()}if(dailyChart)dailyChart.resize()},500)});
if(typeof IntersectionObserver!=='undefined'){const io=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting&&chart){chart.resize();if(!_chartOk)_ensureChart();if(dailyChart)dailyChart.resize()}})},{threshold:0.1});
  setTimeout(()=>{const c=document.getElementById('chart');const d=document.getElementById('dailyChart');if(c)io.observe(c);if(d)io.observe(d)},200)}
const chartOpt={animation:true,animationDuration:300,animationEasing:'cubicOut',
  tooltip:{trigger:'axis',backgroundColor:'rgba(255,255,255,.98)',borderColor:'#e2e8f0',textStyle:{color:'#1e293b',fontSize:13},padding:[10,14],shadowBlur:8,shadowColor:'rgba(0,0,0,.1)',formatter:function(ps){var h=ps[0].axisValue;ps.forEach(function(p){if(p.value!=null){h+='<br/>'+p.marker+p.seriesName+': '+p.value.toFixed(4)+' <b>('+((p.value-1)*100).toFixed(2)+'%)</b>'}});return h}},
  legend:{data:['策略净值','沪深 300 基准'],top:10,right:16,textStyle:{color:'#64748b',fontSize:12}},
  grid:{left:64,right:32,top:52,bottom:48},
  xAxis:{type:'category',data:[],axisLabel:{color:'#94a3b8',fontSize:11,rotate:0},axisLine:{lineStyle:{color:'#e2e8f0'}},boundaryGap:false},
  yAxis:{type:'value',name:'净值',nameTextStyle:{color:'#64748b',fontSize:12},axisLabel:{color:'#64748b',fontSize:11,formatter:v=>v.toFixed(2)},axisLine:{lineStyle:{color:'#e2e8f0'}},splitLine:{lineStyle:{color:'#f1f5f9'}},min:'dataMin'},
  series:[
    {name:'策略净值',type:'line',data:[],smooth:.25,lineStyle:{width:3,color:'#2563eb'},areaStyle:{color:{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(37,99,235,.15)'},{offset:1,color:'rgba(37,99,235,0)'}]}},symbol:'none',symbolSize:6},
    {name:'沪深 300 基准',type:'line',data:[],smooth:.25,lineStyle:{width:2,color:'#dc2626',type:'dashed'},symbol:'none'}
  ]};
const dailyOpt={animation:true,animationDuration:300,
  tooltip:{trigger:'axis',backgroundColor:'rgba(255,255,255,.98)',borderColor:'#e2e8f0',textStyle:{color:'#1e293b',fontSize:13},padding:[10,14]},
  grid:{left:56,right:24,top:36,bottom:48},
  xAxis:{type:'category',data:[],axisLabel:{color:'#94a3b8',fontSize:10},axisLine:{lineStyle:{color:'#e2e8f0'}}},
  yAxis:{type:'value',name:'日收益%',nameTextStyle:{color:'#64748b'},axisLabel:{color:'#64748b',fontSize:11,formatter:v=>v.toFixed(2)+'%'},axisLine:{lineStyle:{color:'#e2e8f0'}},splitLine:{lineStyle:{color:'#f1f5f9'}}},
  series:[{name:'日收益',type:'bar',data:[],itemStyle:{color:function(p){return p.data>=0?'#dc2626':'#16a34a'}},barWidth:'60%',showBackground:true,backgroundStyle:{color:'rgba(0,0,0,.02)'}}]};
window.addEventListener('resize',()=>{if(chart)chart.resize();if(dailyChart)dailyChart.resize()});
var STATE_DONE=false;
let dateIdx={},tradeData=[],currentPage=1,pageSize=10;
function renderTrades(){
  const start=(currentPage-1)*pageSize,end=start+pageSize;
  const page=tradeData.slice(start,end);
  let h='<table class="trade-table"><thead><tr><th>日期</th><th>标的</th><th>方向</th><th>价格</th><th>数量</th><th>金额</th><th>盈亏</th></tr></thead><tbody>';
  page.forEach(t=>{const isBuy=t.direction==='买入'||t.direction==='BUY';const cls=isBuy?'buy':'sell';const dir=isBuy?'买入':'卖出';const pnl=t.pnl||'';const ps=pnl?(parseFloat(pnl)>=0?'color:#dc2626;font-weight:600':'color:#16a34a;font-weight:600'):'';const sym=t.symbol||'';h+='<tr><td>'+t.date+'</td><td>'+sym+'</td><td class="'+cls+'">'+dir+'</td><td>'+t.price+'</td><td>'+t.volume+'</td><td>'+t.amount+'</td><td style="'+ps+'">'+pnl+'</td></tr>'});
  h+='</tbody></table>';document.getElementById('c6').innerHTML=h||'<div class="empty">暂无交易记录</div>';
  const total=Math.ceil(tradeData.length/pageSize);
  const nav=document.getElementById('pageNav');
  if(total>1){nav.style.display='flex';let p='';for(let i=1;i<=total;i++)p+='<button class="'+(i===currentPage?'active':'')+'" onclick="currentPage='+i+',renderTrades()">'+i+'</button>';nav.innerHTML=p}
  else nav.style.display='none'
}
const es=new EventSource('/api/sse?run_id='+RID);
es.addEventListener('step',e=>{const d=JSON.parse(e.data);addLog('['+d.step+'] '+d.title+': '+(d.msg||d.status));
  const sn=parseInt(d.step)||0;setTL(sn,d.status);
  if(sn<=2){setBadge('b1',d.status);if(d.status==='running'){const g=document.getElementById('gpill');g.className='pill pill-r';g.textContent='执行中'}}
  if(sn===3||d.step.includes('3')){setBadge('b2',d.status)}
  if(sn===4){setBadge('b3',d.status)}
  if(sn>=5){setBadge('b5',_warnRendered?'warning':d.status)}
});
es.addEventListener('requirement',e=>{const d=JSON.parse(e.data);setBadge('b1','success');
  const el=document.getElementById('c1');el.classList.remove('empty');
  const km={symbols:'标的',interval:'K线周期',mode:'策略模式',requirement:'需求描述',run_id:'运行ID',fast_window:'快线周期',slow_window:'慢线周期',direction:'方向',k_period:'K周期',d_period:'D周期',j_threshold:'J阈值',rsi_period:'RSI周期',boll_window:'布林窗口',boll_dev:'布林偏差',macd_fast:'MACD快线',macd_slow:'MACD慢线',macd_signal:'MACD信号',atr_period:'ATR周期',cci_window:'CCI窗口',trailing_pct:'追踪止损%',stop_loss:'止损%',take_profit:'止盈%'};
  const vm={bullish:'看涨',bearish:'看跌',DAILY:'日线','5MIN':'5分钟',MINUTE:'分钟线','15MIN':'15分钟','30MIN':'30分钟',HOUR:'小时线',WEEKLY:'周线',cta:'CTA单标的',portfolio:'Portfolio组合'};
  const skip=new Set(['pool_warning','data_blocked','_ma_fallback']);
  let h='<div class="req-grid">';for(const[k,v] of Object.entries(d)){if(skip.has(k)||!v)continue;const lbl=km[k]||k;const val=Array.isArray(v)?v.join(', '):(vm[v]||v);h+='<div class="req-item"><div class="k">'+lbl+'</div><div class="v">'+val+'</div></div>'}
  el.innerHTML=h+'</div>'});
let _codeContent='',_codeFilename='strategy.py';
function _copyCode(){const b=document.getElementById('copyBtn');function _ok(){b.classList.add('copied');b.textContent='✓ 已复制';setTimeout(()=>{b.classList.remove('copied');b.textContent='📋 复制代码'},1500)}function _fb(){const ta=document.createElement('textarea');ta.value=_codeContent;ta.style.cssText='position:fixed;left:-9999px';document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);_ok()}if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(_codeContent).then(_ok).catch(_fb)}else{_fb()}}
function _saveCode(){const blob=new Blob([_codeContent],{type:'text/x-python'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=_codeFilename;a.click();URL.revokeObjectURL(a.href)}
es.addEventListener('code',e=>{const d=JSON.parse(e.data);setBadge('b2','success');
  _codeContent=d.content||'';_codeFilename=d.filename||'strategy.py';
  const el=document.getElementById('c2');el.classList.remove('empty');
  el.innerHTML='<div class="code-wrap"><div class="code-h"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>📄 '+(d.filename||'strategy.py')+' · 已保存至绝对路径<span class="spacer"></span><button class="code-btn" id="copyBtn" onclick="_copyCode()">📋 复制代码</button><button class="code-btn" onclick="_saveCode()">💾 保存策略</button></div><pre class="code-block"><code class="language-python">'+esc(d.content)+'</code></pre></div>';
  try{hljs.highlightAll()}catch(e){}});
es.addEventListener('progress',e=>{const d=JSON.parse(e.data);
  if(d.run_id)document.getElementById('rid').textContent='run: '+d.run_id;
  const pct=parseInt(d.pct)||0;document.getElementById('bar3').style.width=pct+'%';
  if(d.status==='running'||pct>0){setBadge('b3',d.status||'running')}
  if(d.status==='failed'){setBadge('b3','failed');const g=document.getElementById('gpill');g.className='pill pill-f';g.textContent='失败'}
});
let allDates=[],benchMap={};
es.addEventListener('init_axis',e=>{const d=JSON.parse(e.data);dateIdx={};allDates=d.dates;
  d.dates.forEach((dt,i)=>dateIdx[dt]=i);setBadge('b3','running')});
es.addEventListener('point',e=>{const d=JSON.parse(e.data);
  const nav=parseFloat(d.nav);
  const last=chartOpt.xAxis.data[chartOpt.xAxis.data.length-1];
  if(last&&d.dt<=last)return;
  chartOpt.xAxis.data.push(d.dt);chartOpt.series[0].data.push(nav);
  chartOpt.series[1].data.push(benchMap[d.dt]||null);
  const n=chartOpt.series[0].data.length;
  if(n>=2){const prev=chartOpt.series[0].data[n-2]||1;
    dailyOpt.xAxis.data.push(d.dt);
    dailyOpt.series[0].data.push(parseFloat(((nav-prev)/prev*100).toFixed(3)));
    if(dailyChart)dailyChart.setOption(dailyOpt)}
  if(chart){chart.setOption(chartOpt);chart.resize();_chartOk=true}});
es.addEventListener('bench_data',e=>{const d=JSON.parse(e.data);
  if(d.dates&&d.bench){d.dates.forEach((dt,i)=>{benchMap[dt]=d.bench[i]})}});
es.addEventListener('final_chart',e=>{const d=JSON.parse(e.data);
  chartOpt.xAxis.data=d.dates;chartOpt.series[0].data=d.navs;chartOpt.series[1].data=d.bench||[];
  if(chart){chart.setOption(chartOpt,true);chart.resize();_chartOk=true}setBadge('b3','success');document.getElementById('bar3').style.width='100%';
  const daily=[];const dailyDates=[];
  for(let i=1;i<d.navs.length&&i<d.dates.length;i++){
    const prev=d.navs[i-1]||1,curr=d.navs[i];
    daily.push(((curr-prev)/prev*100).toFixed(3));
    dailyDates.push(d.dates[i]);
  }
  dailyOpt.xAxis.data=dailyDates;dailyOpt.series[0].data=daily.map(v=>parseFloat(v));if(dailyChart)dailyChart.setOption(dailyOpt,true);
  setBadge('b4','success')});
es.addEventListener('stats',e=>{const d=JSON.parse(e.data);setBadge('b5','success');
  const el=document.getElementById('c5');el.classList.remove('empty');
  const fmt={total_return:['总收益率',true],annual_return:['年化收益',true],max_ddpercent:['最大回撤',true],sharpe_ratio:['夏普比率',false],winning_rate:['胜率',true],total_net_pnl:['总盈亏',false],total_trade_count:['交易次数',false],total_days:['交易天数',false],profit_days:['盈利天数',false],loss_days:['亏损天数',false]};
  let h='<div class="stats-grid">';for(const[k,[lb,isPct]] of Object.entries(fmt)){const v=d[k];if(v===undefined)continue;
    const n=typeof v==='number';let disp=n?(isPct?v.toFixed(2)+'%':v.toFixed(2)):v;
    const c=n?(v>=0?'pos':'neg'):'neu';
    h+='<div class="sc"><div class="lb">'+lb+'</div><div class="vl '+c+'">'+disp+'</div></div>'}
  el.innerHTML=h+'</div>';
  var tr=parseFloat(d.total_return)||0,sr=parseFloat(d.sharpe_ratio)||0,dd=Math.abs(parseFloat(d.max_ddpercent)||0),wr=parseFloat(d.winning_rate)||0;
  var sc=0;if(sr>=1.5)sc+=3;else if(sr>=1)sc+=2;else if(sr>=0.5)sc+=1;if(tr>=30)sc+=3;else if(tr>=10)sc+=2;else if(tr>=0)sc+=1;if(dd<=10)sc+=2;else if(dd<=20)sc+=1;if(wr>=50)sc+=2;else if(wr>=40)sc+=1;
  var gs=[['S',10],['A',7],['B',5],['C',3],['D',0]],gd='D',gc='#dc2626';
  for(var i=0;i<gs.length;i++)if(sc>=gs[i][1]){gd=gs[i][0];break}
  gc=sc>=7?'#dc2626':sc>=5?'#d97706':'#16a34a';
  var gl=sc>=7?'策略表现优秀':sc>=5?'策略表现良好':sc>=3?'策略表现一般':'策略表现较差';
  var pts=[];
  pts.push((tr>=20?'✅ ':tr>=0?'⚠️ ':'❌ ')+'总收益 '+tr.toFixed(1)+'%'+(tr>=20?'，表现出色':tr>=0?'，收益偏低':'，策略亏损'));
  pts.push((sr>=1?'✅ ':sr>=0.5?'⚠️ ':'❌ ')+'夏普比率 '+sr.toFixed(2)+(sr>=1?'，风险收益良好':sr>=0.5?'，风险收益一般':'，风险收益较差'));
  pts.push((dd<=15?'✅ ':dd<=25?'⚠️ ':'❌ ')+'最大回撤 '+dd.toFixed(1)+'%'+(dd<=15?'，风控良好':dd<=25?'，有一定风险':'，回撤过大'));
  if(wr>0)pts.push((wr>=50?'✅ ':wr>=40?'⚠️ ':'❌ ')+'胜率 '+wr.toFixed(1)+'%'+(wr>=50?'，胜率健康':wr>=40?'，胜率偏低':'，胜率不足'));
  var nxt=sc>=7?'可尝试「优化参数」进一步提升，或进入「模拟盘」验证实盘效果。':sc>=5?'建议通过「优化参数」调整策略参数以提升表现。':'当前策略需改进，请调整策略逻辑后重新回测。';
  var cc=document.getElementById('p-conclusion');cc.style.display='block';
  document.getElementById('c-conclusion').innerHTML='<div style="text-align:center;padding:16px 0"><div style="font-size:32px;font-weight:900;color:'+gc+'">'+gd+'级</div><div style="font-size:14px;font-weight:600;color:#475569;margin-top:4px">'+gl+'</div></div><div style="display:flex;flex-direction:column;gap:6px;margin:12px 0">'+pts.map(function(p){return'<div style="padding:10px 14px;background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;font-size:13px">'+p+'</div>'}).join('')+'</div><div style="padding:12px;background:linear-gradient(135deg,#eff6ff,#f0f9ff);border-radius:10px;border:1px solid #dbeafe;font-size:13px;color:#1e40af;font-weight:600">💡 '+nxt+'</div>'});
es.addEventListener('trades',e=>{const d=JSON.parse(e.data);tradeData=d.trades||[];currentPage=1;renderTrades()});
es.addEventListener('log',e=>{const d=JSON.parse(e.data);addLog(d.msg||'')});
es.addEventListener('done',e=>{const g=document.getElementById('gpill');g.className='pill pill-s';g.textContent='已完成';STATE_DONE=true;
  setBadge('b3','success');setBadge('b5',_warnRendered?'warning':'success');setTL(6,_warnRendered?'warning':'success');addLog('✅ 全部完成');
  if(dailyChart&&dailyOpt.series[0].data.length>0){setBadge('b4','success')}else{_ensureChart()}});
es.addEventListener('report_urls',e=>{const d=JSON.parse(e.data);const url=d.report_url||'';
  if(url){document.getElementById('rptLink').href=url;document.getElementById('rptBan').style.display='block'}});
es.addEventListener('error_info',e=>{const d=JSON.parse(e.data);
  document.getElementById('errCard').style.display='block';
  document.getElementById('errType').textContent=(d.error_type||'ERROR').toUpperCase();
  document.getElementById('errMsg').textContent=(d.step?'['+d.step+'] ':'')+d.message;
  if(d.traceback){document.getElementById('errTb').textContent=d.traceback}
  const g=document.getElementById('gpill');g.className='pill pill-f';g.textContent='失败';
  addLog('❌ '+d.error_type+': '+d.message);addLog('💡 请回到对话页输入「查看结果」，AI 将自动诊断并修复')});
let _warnRendered=false;
function _renderWarnings(ws){if(_warnRendered||!ws||!ws.length)return;_warnRendered=true;
  const el=document.getElementById('warnCard');el.style.display='block';
  const ul=document.getElementById('warnList');ul.innerHTML=ws.map(w=>'<li>'+esc(w)+'</li>').join('');
  addLog('⚠️ 结果校验告警: '+ws.join('; '))}
es.addEventListener('result_warnings',e=>{const d=JSON.parse(e.data);_renderWarnings(d.warnings)});
const posHistory=[];
es.addEventListener('position_snapshot',e=>{const d=JSON.parse(e.data);
  if(d.positions&&d.positions.length>0){posHistory.push(d);renderPositions()}});
es.addEventListener('positions',e=>{const d=JSON.parse(e.data);const ps=d.positions||[];
  if(ps.length>0){posHistory.push({date:'最终',positions:ps});renderPositions()}});
function renderPositions(){
  const el=document.getElementById('c7');
  const last20=posHistory.slice(-20);
  let h='<table class="trade-table"><thead><tr><th>日期</th><th>标的</th><th>持仓(股)</th><th>现价</th><th>市值</th></tr></thead><tbody>';
  last20.forEach(snap=>{const dt=snap.date||'';snap.positions.forEach((p,i)=>{
    h+='<tr><td>'+(i===0?dt:'')+'</td><td>'+p.symbol+'</td><td>'+p.volume+'</td><td>'+(p.price||'-')+'</td><td>'+(p.value||p.market_value||'-')+'</td></tr>'})});
  h+='</tbody></table>';
  if(posHistory.length>20)h+='<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px">显示最近20条，共'+posHistory.length+'条持仓快照</div>';
  el.innerHTML=h}
let _lastTs=0,_sseOk=true,_pollIv=3000,_pollTimer=null,_pollFails=0;
function _sseTouch(){_lastTs=Math.floor(Date.now()/1000);if(!_sseOk){_sseOk=true;_adaptPoll();addLog('✅ SSE已恢复')}}
es.addEventListener('progress',()=>_sseTouch());
es.addEventListener('step',()=>_sseTouch());
es.addEventListener('point',()=>_sseTouch());
es.onerror=()=>{if(_sseOk){_sseOk=false;addLog('⚠️ SSE断开，轮询兜底中...');_adaptPoll()}};
function _adaptPoll(){
  clearInterval(_pollTimer);
  _pollIv=STATE_DONE?30000:(_sseOk?15000:3000);
  _pollTimer=setInterval(_pollState,_pollIv);
}
function _renderPollLogs(logs){
  if(!logs||!logs.length)return;
  const el=document.getElementById('logs');
  const existing=el.innerText||'';
  logs.forEach(m=>{if(m&&existing.indexOf(m)===-1)addLog(m)});
}
function _renderPollStats(stats){
  if(!stats||Object.keys(stats).length===0)return;
  const el=document.getElementById('c5');
  if(el.classList.contains('empty')){
    setBadge('b5','success');el.classList.remove('empty');
    const fmt={total_return:['总收益率',true],annual_return:['年化收益',true],max_ddpercent:['最大回撤',true],sharpe_ratio:['夏普比率',false],winning_rate:['胜率',true],total_net_pnl:['总盈亏',false],total_trade_count:['交易次数',false],total_days:['交易天数',false]};
    let h='<div class="stats-grid">';for(const[k,[lb,isPct]] of Object.entries(fmt)){const v=stats[k];if(v===undefined)continue;
      const n=typeof v==='number';let disp=n?(isPct?v.toFixed(2)+'%':v.toFixed(2)):v;
      const c=n?(v>=0?'pos':'neg'):'neu';
      h+='<div class="sc"><div class="lb">'+lb+'</div><div class="vl '+c+'">'+disp+'</div></div>'}
    el.innerHTML=h+'</div>';
  }
}
function _pollState(){
  fetch('/api/state?run_id='+RID).then(r=>{if(!r.ok)throw r;return r.json()}).then(d=>{
    _pollFails=0;
    if(!d||!d.run_id)return;
    const g=document.getElementById('gpill');
    if(d.ts>_lastTs){_lastTs=d.ts}
    if(d.status==='done'&&!STATE_DONE){
      g.className='pill pill-s';g.textContent='已完成';STATE_DONE=true;
      addLog('✅ 回测已完成（轮询恢复）');_adaptPoll();
    }else if(d.status==='running'&&(g.textContent==='等待启动'||g.textContent==='连接中...')){
      g.className='pill pill-r';g.textContent='执行中';
    }else if(d.status==='waiting'&&g.textContent==='连接中...'){
      g.className='pill pill-w';g.textContent='等待启动';
    }else if(d.status==='failed'){
      g.className='pill pill-f';g.textContent='失败';
    }
    if(d.stage){document.getElementById('bar3').style.width=(d.pct||0)+'%'}
    Object.values(d.steps||{}).forEach(st=>{const sn=parseInt(st.step)||0;setTL(sn,st.status)});
    if(d.error&&d.error.message){
      document.getElementById('errCard').style.display='block';
      document.getElementById('errMsg').textContent=d.error.message;
      g.className='pill pill-f';g.textContent='失败';
    }
    if(!_sseOk){_renderPollLogs(d.logs);_renderPollStats(d.stats)}
    if(d.has_code&&!_codeContent){fetch('/api/code').then(r=>r.json()).then(cd=>{if(cd&&cd.content){_codeContent=cd.content;_codeFilename=cd.filename||'strategy.py';setBadge('b2','success');const el=document.getElementById('c2');el.classList.remove('empty');el.innerHTML='<div class="code-wrap"><div class="code-h"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>📄 '+esc(cd.filename||'strategy.py')+' · 已保存至绝对路径<span class="spacer"></span><button class="code-btn" id="copyBtn" onclick="_copyCode()">📋 复制代码</button><button class="code-btn" onclick="_saveCode()">💾 保存策略</button></div><pre class="code-block"><code class="language-python">'+esc(cd.content)+'</code></pre></div>';try{hljs.highlightAll()}catch(e){}}}).catch(()=>{})}
    if(d.result_warnings)_renderWarnings(d.result_warnings);
    if(chart&&!_chartOk&&(d.point_count||0)>0)_ensureChart();
    if(chart&&(d.point_count||0)>chartOpt.series[0].data.length){fetch('/api/chart').then(r=>r.json()).then(ch=>{
      if(!ch||!ch.navs||ch.navs.length<=chartOpt.series[0].data.length)return;
      const cur=chartOpt.series[0].data.length;
      for(let i=cur;i<ch.navs.length;i++){
        chartOpt.xAxis.data.push(ch.dates[i]);chartOpt.series[0].data.push(ch.navs[i]);
        chartOpt.series[1].data.push((ch.bench&&ch.bench[i])||benchMap[ch.dates[i]]||null)}
      chart.setOption(chartOpt);chart.resize();_chartOk=true;
      const dailyCur=dailyOpt.series[0].data.length,navArr=chartOpt.series[0].data;
      for(let i=Math.max(1,dailyCur+1);i<navArr.length;i++){
        const prev=navArr[i-1]||1;dailyOpt.xAxis.data.push(chartOpt.xAxis.data[i]);
        dailyOpt.series[0].data.push(parseFloat(((navArr[i]-prev)/prev*100).toFixed(3)))}
      if(dailyChart&&dailyOpt.series[0].data.length>dailyCur){dailyChart.setOption(dailyOpt);dailyChart.resize()}}).catch(()=>{})}
    const now=Math.floor(Date.now()/1000);
    const ago=_lastTs>0?now-_lastTs:0;
    const hb=document.getElementById('_hb');
    if(hb){hb.textContent=ago<5?'刚刚更新':ago<60?ago+'秒前更新':Math.floor(ago/60)+'分钟前更新'}
  }).catch(()=>{_pollFails++;
    if(_pollFails>=3&&!STATE_DONE){const g=document.getElementById('gpill');g.className='pill pill-f';g.textContent='服务已断开';addLog('❌ 监控服务无响应，可能已关闭。请回到对话页重新提交回测。')}
    if(_pollFails>=3&&STATE_DONE){clearInterval(_pollTimer)}})
}
_pollTimer=setInterval(_pollState,3000);
setTimeout(_pollState,1500);
</script></body></html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _mark_done(self):
        with LOCK: STATE["done"] = True; STATE["status"] = "done"; STATE["pct"] = 100
        broadcast("done", {}); broadcast("progress", STATE)
    def do_GET(self):
        path = urlparse(self.path).path; qs = parse_qs(urlparse(self.path).query)
        if path == "/" or path.startswith("/runs/"):
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store"); self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        elif path == "/api/sse" or path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream"); self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
            with LOCK: CLIENTS.append(self.wfile)
            with LOCK: s = dict(STATE)
            slim_prog = {k: v for k, v in s.items() if k not in ("points", "trades", "positions", "position_snapshots", "logs", "requirement", "code", "final", "bench_data", "dates")}
            self._sse_send("progress", slim_prog)
            req = s.get("requirement", {})
            if req:
                slim_req = dict(req) if isinstance(req, dict) else req
                if isinstance(slim_req, dict) and "symbols" in slim_req and isinstance(slim_req["symbols"], list): slim_req["symbols"] = f"共{len(slim_req['symbols'])}只标的"
                self._sse_send("requirement", slim_req)
            if s.get("code"): self._sse_send("code", {"filename": s["code_file"], "content": s["code"]})
            if s.get("dates"): self._sse_send("init_axis", {"dates": s["dates"]})
            if s.get("bench_data"): self._sse_send("bench_data", s["bench_data"])
            for pt in s.get("points", []): self._sse_send("point", pt)
            if s.get("final"): self._sse_send("final_chart", s["final"])
            if s.get("stats"): self._sse_send("stats", s["stats"])
            if s.get("trades") is not None: self._sse_send("trades", {"trades": s["trades"]})
            if s.get("positions") is not None: self._sse_send("positions", {"positions": s["positions"]})
            for ps in s.get("position_snapshots", []): self._sse_send("position_snapshot", ps)
            if s.get("report_urls"): self._sse_send("report_urls", s["report_urls"])
            if s.get("error"): self._sse_send("error_info", s["error"])
            if s.get("result_warnings"): self._sse_send("result_warnings", {"warnings": s["result_warnings"]})
            for st in s.get("steps", {}).values(): self._sse_send("step", st)
            if s.get("done"): self._sse_send("done", {})
            self.wfile.flush()
            try:
                _hb = 0
                # done后仍保持SSE连接，避免浏览器自动重连触发事件回放导致日志重复刷屏
                while True:
                    time.sleep(1); _hb += 1
                    if _hb >= 15:
                        _hb = 0
                        try: self.wfile.write(b": heartbeat\n\n"); self.wfile.flush()
                        except Exception: break
            except Exception: pass
        elif path == "/api/step":
            self._json_ok()
            d = {"step": qs.get("step",[""])[0], "status": qs.get("status",["running"])[0], "title": qs.get("title",[""])[0], "msg": qs.get("msg",[""])[0]}
            with LOCK: STATE["steps"][d["step"]] = d; STATE["run_id"] = qs.get("run_id", [STATE["run_id"]])[0]
            broadcast("step", d)
        elif path == "/api/progress":
            self._json_ok()
            with LOCK:
                STATE["run_id"] = qs.get("run_id", [STATE["run_id"]])[0]; STATE["status"] = qs.get("status", [STATE["status"]])[0]
                STATE["stage"] = qs.get("stage", [STATE["stage"]])[0]; STATE["pct"] = int(qs.get("pct", [STATE["pct"]])[0])
            broadcast("progress", STATE)
        elif path == "/api/point":
            self._json_ok()
            pt = {"dt": qs.get("dt",[""])[0], "nav": float(qs.get("nav",[1])[0])}
            with LOCK: STATE["points"].append(pt)
            broadcast("point", pt)
        elif path == "/api/stats":
            self._json_ok()
            stats = {}
            for k, v in qs.items():
                try: stats[k] = float(v[0])
                except Exception: stats[k] = v[0]
            with LOCK: STATE["stats"] = stats
            broadcast("stats", stats)
        elif path == "/api/trades":
            self._json_ok()
            trades = json.loads(qs.get("data", ["[]"])[0])
            with LOCK: STATE["trades"] = trades
            broadcast("trades", {"trades": trades})
        elif path == "/api/log":
            self._json_ok()
            msg = qs.get("msg",[""])[0]
            with LOCK: STATE["logs"].append(msg)
            broadcast("log", {"msg": msg})
        elif path == "/api/done":
            self._json_ok()
            self._mark_done()
        elif path == "/api/state":
            self.send_response(200); self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store"); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
            self.wfile.write(json.dumps(_slim_state(), ensure_ascii=False).encode())
        elif path == "/api/chart":
            self.send_response(200); self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store"); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
            with LOCK:
                if STATE.get("final"): chart_data = STATE["final"] #回测完成：返回精确final数据
                elif STATE.get("points"): chart_data = {"dates": [p["dt"] for p in STATE["points"]], "navs": [p["nav"] for p in STATE["points"]], "bench": []} #回测中：返回实时累积点
                else: chart_data = {}
            self.wfile.write(json.dumps(chart_data, ensure_ascii=False).encode())
        elif path == "/api/code":
            self.send_response(200); self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store"); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
            with LOCK: self.wfile.write(json.dumps({"filename": STATE.get("code_file",""), "content": STATE.get("code","")}, ensure_ascii=False).encode())
        elif path == "/api/health":
            self._json_ok()
        elif path.startswith("/reports/"):
            name = (path.split("/reports/", 1)[1] or "").strip("/")
            allow_suffix = (".html", ".json", ".png")
            if (
                not name
                or "/" in name
                or ".." in name
                or not name.startswith("run_")
                or not name.endswith(allow_suffix)
            ):
                self.send_response(400); self.end_headers(); return
            fp = os.path.join(os.path.dirname(__file__), name)
            if not os.path.isfile(fp):
                self.send_response(404); self.end_headers(); return
            ctype = "application/octet-stream"
            if name.endswith(".html"): ctype = "text/html; charset=utf-8"
            elif name.endswith(".json"): ctype = "application/json; charset=utf-8"
            elif name.endswith(".png"): ctype = "image/png"
            self.send_response(200); self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-cache, no-store"); self.end_headers()
            with open(fp, "rb") as f: self.wfile.write(f.read())
        else:
            self.send_response(404); self.end_headers()
    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        data = json.loads(body) if body else {}
        if path == "/api/requirement":
            self._json_ok()
            with LOCK: STATE["requirement"] = data
            broadcast("requirement", data)
        elif path == "/api/code":
            self._json_ok()
            with LOCK: STATE["code"] = data.get("content", ""); STATE["code_file"] = data.get("filename", "strategy.py")
            broadcast("code", data)
        elif path == "/api/init_axis":
            self._json_ok()
            with LOCK: STATE["dates"] = data.get("dates", [])
            broadcast("init_axis", data)
        elif path == "/api/final":
            self._json_ok()
            with LOCK: STATE["final"] = data
            broadcast("final_chart", data)
        elif path == "/api/trades":
            self._json_ok()
            with LOCK: STATE["trades"] = data.get("trades", [])
            broadcast("trades", data)
        elif path == "/api/positions":
            self._json_ok()
            with LOCK: STATE["positions"] = data.get("positions", [])
            broadcast("positions", data)
        elif path == "/api/position_snapshot":
            self._json_ok()
            with LOCK: STATE["position_snapshots"].append(data)
            broadcast("position_snapshot", data)
        elif path == "/api/bench_data":
            self._json_ok()
            with LOCK: STATE["bench_data"] = data
            broadcast("bench_data", data)
        elif path == "/api/stats":
            self._json_ok()
            with LOCK: STATE["stats"] = data
            broadcast("stats", data)
        elif path == "/api/report_urls":
            self._json_ok()
            with LOCK: STATE["report_urls"] = data
            broadcast("report_urls", data)
        elif path == "/api/result_warnings":
            self._json_ok()
            with LOCK: STATE["result_warnings"] = data.get("warnings", [])
            broadcast("result_warnings", data)
        elif path == "/api/error":
            self._json_ok()
            with LOCK: STATE["error"] = data
            broadcast("error_info", data)
        elif path == "/api/done":
            self._json_ok()
            self._mark_done()
        else:
            self.send_response(404); self.end_headers()
    def _json_ok(self):
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers()
        self.wfile.write(b'{"ok":true}')
    def _sse_send(self, event, data):
        try: self.wfile.write(f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n".encode())
        except Exception: pass

def _kill_port(port):
    import socket, subprocess, platform
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1)
        if s.connect_ex(("127.0.0.1", port)) != 0: s.close(); return
        s.close()
    except Exception: return
    is_win = platform.system() == "Windows"
    for _ in range(3):
        try:
            if is_win:
                subprocess.run(["powershell", "-NoProfile", "-Command",
                    f"(Get-NetTCPConnection -LocalPort {port} -State Listen -ErrorAction SilentlyContinue).OwningProcess | Sort-Object -Unique | ForEach-Object {{ Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }}"],
                    timeout=8, capture_output=True, text=True)
            else:
                subprocess.run(f"lsof -ti:{port} | xargs -r kill -9 2>/dev/null || fuser -k {port}/tcp 2>/dev/null", shell=True, timeout=5, capture_output=True, text=True)
        except Exception: pass
        time.sleep(1.5 if is_win else 0.5)
        try:
            t = socket.socket(socket.AF_INET, socket.SOCK_STREAM); t.settimeout(1)
            if t.connect_ex(("127.0.0.1", port)) != 0: t.close(); return
            t.close()
        except Exception: return
    print(f"[warn] 端口 {port} 清理 3 次仍被占用", flush=True)

MONITOR_MAX_IDLE_SEC = int(os.environ.get("MONITOR_MAX_IDLE_SEC", "1800"))  # 30min 兜底自杀
MONITOR_DONE_KEEPALIVE_SEC = int(os.environ.get("MONITOR_DONE_KEEPALIVE_SEC", "600"))  # done后保留10min供用户查看


def _recover_state(run_id):
    """启动时从 state.json + report_data.json 恢复完整状态（含图表/交易/统计），避免重启丢数据"""
    if not run_id: return
    import pathlib
    base = pathlib.Path(__file__).parent; run_dir = base / "orchestrator_runs" / run_id
    sf = run_dir / "state.json"
    if not sf.exists(): return
    try:
        s = json.loads(sf.read_text())
        if s.get("status") not in ("failed", "completed", "done"): return
        with LOCK:
            STATE["run_id"] = run_id; STATE["_ts"] = int(time.time())
            if s.get("status") == "failed": STATE["status"] = "failed"; STATE["done"] = True; STATE["pct"] = 100
            elif s.get("status") in ("completed", "done"): STATE["status"] = "done"; STATE["done"] = True; STATE["pct"] = 100
            req = {**s.get("payload", {}), **s.get("payload", {}).get("parsed", {})}
            _skip = {"parsed","payload","capability_check","monitor_base","monitor_port","monitor_public_base","monitor_public_reachable","monitor_public_probe_error","report_public_base","report_public_dir","report_url","report_replay_url","report_summary_url","python_bin","qgdata_token_present","qgdata_token_source","timeout_sec","strategy_file","strategy_module","strategy_class","pool_warning","data_blocked","_ma_fallback","monitor_url","monitor_url_local","start","end","capital","rate","slippage","size","pricetick","title"}
            STATE["requirement"] = {k: v for k, v in req.items() if k not in _skip and v and not k.startswith("_")}
            if isinstance(STATE["requirement"].get("symbols"), list): STATE["requirement"]["symbols"] = f"共{len(STATE['requirement']['symbols'])}只标的"
            errs = s.get("errors", [])
            if errs:
                e = errs[-1]; STATE["error"] = {"error_type": e.get("error_type", ""), "step": e.get("step", ""), "message": e.get("message", ""), "traceback": e.get("traceback", "")}
            for step_k, step_v in s.get("steps", {}).items():
                STATE["steps"][step_k] = {"step": step_k, "status": step_v.get("status", ""), "title": step_v.get("detail", ""), "msg": ""}
            rpt = base / f"run_{run_id}_report_data.json" #恢复图表/交易/统计/持仓数据
            if rpt.exists():
                rd = json.loads(rpt.read_text())
                STATE["final"] = {"dates": rd.get("dates", []), "navs": rd.get("navs", []), "bench": rd.get("bench", [])}
                STATE["stats"] = rd.get("stats", {})
                STATE["trades"] = rd.get("trades", [])
                STATE["position_snapshots"] = rd.get("position_snapshots", [])
                if STATE["position_snapshots"]: STATE["positions"] = STATE["position_snapshots"][-1].get("positions", [])
                print(f"[monitor] recovered chart/trades/positions from {rpt.name} (dates={len(rd.get('dates',[]))} trades={len(rd.get('trades',[]))} pos_snaps={len(STATE['position_snapshots'])})", flush=True)
            if s.get("result_warnings"): STATE["result_warnings"] = s["result_warnings"] #恢复结果校验告警
            pl = s.get("payload", {}) #恢复报告链接
            STATE["report_urls"] = {k: pl.get(k, "") for k in ("report_url", "report_replay_url", "report_summary_url") if pl.get(k)}
            snap = run_dir / "strategy_snapshot.py" #恢复策略代码
            if snap.exists():
                STATE["code"] = snap.read_text(encoding="utf-8"); STATE["code_file"] = snap.name
        print(f"[monitor] recovered state from {sf.name} (status={s.get('status')})", flush=True)
    except Exception as e: print(f"[monitor] state recovery failed: {e}", flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--run-id", default="")
    args = ap.parse_args()
    _kill_port(args.port)
    STATE["run_id"] = args.run_id
    _recover_state(args.run_id)
    srv = ThreadedHTTPServer((args.host, args.port), Handler)
    shown_host = "127.0.0.1" if args.host == "0.0.0.0" else args.host
    print(f"[monitor] http://{shown_host}:{args.port}/runs/{args.run_id}", flush=True)
    print(f"[monitor] pid={os.getpid()}", flush=True)
    boot = time.time()
    def auto_stop():
        while not STATE["done"]:
            if time.time() - boot > MONITOR_MAX_IDLE_SEC:
                print(f"[monitor] idle timeout ({MONITOR_MAX_IDLE_SEC}s), shutting down", flush=True)
                break
            time.sleep(2)
        time.sleep(MONITOR_DONE_KEEPALIVE_SEC if STATE["done"] else 5)
        srv.shutdown()
    threading.Thread(target=auto_stop, daemon=True).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: pass
    srv.server_close()

if __name__ == "__main__":
    main()
