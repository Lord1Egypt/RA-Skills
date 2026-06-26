#!/usr/bin/env python3
"""Build the full HTML page for the brand marketing skill package."""

SKILL_MD = open('/workspace/skills/qizheng-brand-marketing/SKILL.md').read()

HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>七政·品牌营销技能包 | 玉衡</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0a0f;--surface:#111118;--surface2:#1a1a24;--border:#2a2a3a;--text:#e8e6f0;--dim:#8880a0;--accent:#c9a227;--red:#ff4d6a;--green:#00e5a0;--blue:#4a9eff;--purple:#9b6dff}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(10,10,15,0.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:0 16px;display:flex;align-items:center;gap:14px;height:50px}
.nav-brand{font-size:11px;color:var(--accent);font-weight:700;letter-spacing:2px;white-space:nowrap}
.nav-tabs{display:flex;gap:2px;flex:1}
.nav-tab{padding:4px 10px;border-radius:5px;font-size:10px;color:var(--dim);cursor:pointer;transition:all .2s;border:none;background:none;white-space:nowrap}
.nav-tab:hover{color:var(--text);background:var(--surface2)}
.nav-tab.active{color:var(--accent);background:rgba(201,162,39,.12)}
.hero{padding:82px 16px 36px;text-align:center}
.hero-badge{display:inline-block;background:rgba(201,162,39,.1);border:1px solid rgba(201,162,39,.3);color:var(--accent);font-size:9px;padding:2px 10px;border-radius:20px;margin-bottom:12px;letter-spacing:1px}
.hero h1{font-size:26px;font-weight:800;background:linear-gradient(135deg,#fff 0%,var(--accent) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;line-height:1.3}
.hero p{font-size:12px;color:var(--dim);max-width:480px;margin:0 auto 20px;line-height:1.7}
.hero-meta{display:flex;justify-content:center;gap:16px;flex-wrap:wrap}
.hero-stat{text-align:center}
.hero-stat .num{font-size:22px;font-weight:800;color:var(--accent)}
.hero-stat .label{font-size:9px;color:var(--dim);margin-top:2px}
.section{padding:16px;max-width:1080px;margin:0 auto}
.section-label{font-size:9px;letter-spacing:2px;color:var(--accent);margin-bottom:6px;text-transform:uppercase}
.section-title{font-size:16px;font-weight:700;margin-bottom:4px}
.section-desc{font-size:11px;color:var(--dim);margin-bottom:16px;line-height:1.6}
.divider{height:1px;background:var(--border);margin:0 16px 24px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:24px}
.grid2{grid-template-columns:repeat(2,1fr)}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px 12px;cursor:pointer;transition:all .25s;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.card:nth-child(1)::before{background:var(--accent)}
.card:nth-child(2)::before{background:var(--blue)}
.card:nth-child(3)::before{background:var(--red)}
.card:nth-child(4)::before{background:var(--purple)}
.card:hover{transform:translateY(-2px);border-color:var(--accent);box-shadow:0 6px 18px rgba(0,0,0,.4)}
.card .icon{font-size:22px;margin-bottom:7px}
.card h3{font-size:12px;margin-bottom:4px}
.card p{font-size:10px;color:var(--dim);line-height:1.6}
.tag{display:inline-block;font-size:9px;padding:2px 7px;border-radius:10px;background:rgba(255,255,255,.05);color:var(--dim);margin-top:7px}
.box{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:24px;overflow-x:auto}
.flow{display:flex;align-items:center;min-width:560px}
.step{flex:1;display:flex;flex-direction:column;align-items:center;cursor:pointer}
.circle{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;border:2px solid var(--border);background:var(--surface2);transition:all .3s;z-index:1}
.step:hover .circle{border-color:var(--accent);box-shadow:0 0 14px rgba(201,162,39,.3);transform:scale(1.1)}
.fl{font-size:9px;margin-top:6px;color:var(--dim);text-align:center}
.fs{font-size:8px;color:var(--dim);opacity:.6;text-align:center;margin-top:1px}
.arr{flex-shrink:0;color:var(--border);font-size:14px;padding:0 3px}
.case{background:linear-gradient(135deg,rgba(201,162,39,.08),rgba(74,158,255,.05));border:1px solid rgba(201,162,39,.2);border-radius:12px;padding:20px;margin-bottom:24px}
.ch{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:14px;gap:10px}
.ctag{background:rgba(0,229,160,.1);border:1px solid rgba(0,229,160,.3);color:var(--green);font-size:9px;padding:2px 9px;border-radius:20px;white-space:nowrap}
.m4{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:14px}
.m{background:var(--surface);border-radius:8px;padding:10px;text-align:center}
.m .v{font-size:16px;font-weight:800;color:var(--accent)}
.m .l{font-size:8px;color:var(--dim);margin-top:2px}
.out{display:flex;gap:7px;flex-wrap:wrap}
.o{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:6px 10px;font-size:9px;display:flex;align-items:center;gap:6px;text-decoration:none;color:var(--text);transition:all .2s}
.o:hover{border-color:var(--accent);color:var(--accent)}
.dot{width:4px;height:4px;border-radius:50%;background:var(--accent);flex-shrink:0}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:12px;overflow:hidden;margin-bottom:24px}
.ph{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;gap:8px}
.pt{font-size:12px;font-weight:600}
.tabs{display:flex;gap:2px}
.tab{padding:4px 10px;border-radius:5px;font-size:9px;border:none;cursor:pointer;background:var(--surface2);color:var(--dim);transition:all .2s}
.tab.on{background:rgba(201,162,39,.15);color:var(--accent)}
.pb{padding:16px}
.row{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:10px}
.in{background:var(--surface2);border:1px solid var(--border);border-radius:7px;padding:8px 10px}
.in label{font-size:9px;color:var(--dim);display:block;margin-bottom:2px}
.in input{width:100%;background:none;border:none;color:var(--text);font-size:12px;outline:none}
.btn{width:100%;padding:9px;border-radius:7px;border:none;font-size:11px;font-weight:600;cursor:pointer;background:linear-gradient(135deg,var(--accent),#e0b830);color:#000;margin-bottom:14px;transition:all .2s}
.btn:hover{opacity:.9;transform:translateY(-1px)}
.res{background:var(--surface2);border-radius:10px;padding:14px;margin-bottom:12px;display:none}
.res.on{display:block}
.res h4{font-size:10px;color:var(--accent);margin-bottom:10px}
.k3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px}
.k{background:var(--surface);border-radius:7px;padding:10px;text-align:center}
.k .v{font-size:15px;font-weight:800;margin-bottom:2px}
.k .l{font-size:8px;color:var(--dim)}
.k.g .v{color:var(--green)}
.k.y .v{color:#f5c518}
.k.r .v{color:var(--red)}
.cr{background:var(--surface);border-radius:8px;padding:12px;margin-bottom:10px}
.cr-title{font-size:9px;color:var(--dim);margin-bottom:7px}
.bars{display:flex;align-items:flex-end;gap:4px;height:60px}
.bg{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px}
.bar{width:100%;border-radius:2px 2px 0 0;background:linear-gradient(180deg,rgba(201,162,39,.8),rgba(201,162,39,.2));transition:height .5s ease}
.bl{font-size:7px;color:var(--dim)}
.bv{font-size:8px;font-weight:600;color:var(--accent)}
.d2{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:24px}
.dc{background:var(--surface);border:1px solid var(--border);border-radius:11px;padding:18px;cursor:pointer;transition:all .25s;text-decoration:none;color:var(--text)}
.dc:hover{border-color:var(--accent);transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.3)}
.di{font-size:24px;margin-bottom:7px}
.dc h3{font-size:12px;margin-bottom:3px}
.dc p{font-size:10px;color:var(--dim);line-height:1.6;margin-bottom:7px}
.db{display:inline-block;font-size:8px;padding:2px 6px;border-radius:10px;margin-right:3px}
.db.core{background:rgba(201,162,39,.15);color:var(--accent)}
.db.exec{background:rgba(74,158,255,.15);color:var(--blue)}
.db.koc{background:rgba(155,109,255,.15);color:var(--purple)}
.db.crisis{background:rgba(255,77,106,.15);color:var(--red)}
.k5{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:24px}
.kt{background:var(--surface);border:1px solid var(--border);border-radius:9px;padding:10px 8px;transition:all .2s}
.kt:hover{border-color:var(--purple);transform:translateY(-2px)}
.kt .e{font-size:18px;margin-bottom:4px}
.kt h4{font-size:10px;margin-bottom:1px}
.kt p{font-size:8px;color:var(--dim)}
.kt .m{font-size:8px;color:var(--green);background:rgba(0,229,160,.1);padding:1px 6px;border-radius:10px;display:inline-block;margin-top:4px}
.cta{background:linear-gradient(135deg,rgba(201,162,39,.1),rgba(74,158,255,.05));border:1px solid rgba(201,162,39,.2);border-radius:12px;padding:28px;text-align:center;margin-bottom:24px}
.cta h2{font-size:16px;margin-bottom:4px}
.cta p{font-size:11px;color:var(--dim);margin-bottom:16px}
.btn2{display:inline-block;padding:9px 22px;background:linear-gradient(135deg,var(--accent),#e0b830);color:#000;font-weight:700;font-size:11px;border-radius:8px;text-decoration:none;border:none;cursor:pointer;transition:all .2s}
.btn2:hover{opacity:.9;transform:translateY(-2px)}
.sv{background:var(--surface);border:1px solid var(--border);border-radius:11px;padding:18px;font-size:11px;line-height:1.8;color:var(--dim);max-height:65vh;overflow-y:auto;white-space:pre-wrap;margin-bottom:24px}
.sv::-webkit-scrollbar{width:4px}
.sv::-webkit-scrollbar-track{background:var(--surface2)}
.sv::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
.notif{position:fixed;bottom:16px;right:16px;background:var(--surface);border:1px solid var(--green);border-radius:8px;padding:10px 14px;font-size:10px;color:var(--green);box-shadow:0 6px 18px rgba(0,0,0,.4);z-index:200;display:none;animation:su .3s ease}
.notif.on{display:flex;align-items:center;gap:6px}
@keyframes su{from{transform:translateY(12px);opacity:0}to{transform:translateY(0);opacity:1}}
.ft{text-align:center;padding:24px 16px;border-top:1px solid var(--border);font-size:9px;color:var(--dim)}
.ftb{color:var(--accent);font-weight:600}
.mt16{margin-top:16px}
.dark{background:var(--surface2);border-radius:7px;padding:10px;margin-top:8px;font-size:10px;line-height:1.7}
.nd{display:none}
.nd.on{display:block}
.hidden{display:none}
@media(max-width:768px){
.grid4{grid-template-columns:repeat(2,1fr)}
.m4{grid-template-columns:repeat(2,1fr)}
.row{grid-template-columns:1fr}
.d2{grid-template-columns:1fr}
.k5{grid-template-columns:repeat(2,1fr)}
.flow{min-width:420px}
}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-brand">七政·玉衡</div>
  <div class="nav-tabs">
    <button class="nav-tab active" onclick="showTab('overview')">总览</button>
    <button class="nav-tab" onclick="showTab('method')">方法论</button>
    <button class="nav-tab" onclick="showTab('case')">成山案例</button>
    <button class="nav-tab" onclick="showTab('simulate')">推演模拟</button>
    <button class="nav-tab" onclick="showTab('deliver')">交付物</button>
    <button class="nav-tab" onclick="showTab('skill')">SKILL.md</button>
  </div>
</nav>

<!-- ====== OVERVIEW ====== -->
<div id="page-overview">
<div class="hero">
  <div class="hero-badge">SKILL PACKAGE v1.0</div>
  <h1>七政·品牌营销技能包<br>四大家 &times; OASIS &times; 完整闭环</h1>
  <p>融合奥美/BBDO/盛世长城/扬罗必凯四大家实战方法论<br>舆情推演 &times; 品牌叙事 &times; 执行落地，5步闭环，48小时交付</p>
  <div class="hero-meta">
    <div class="hero-stat"><div class="num">4</div><div class="label">广告方法论</div></div>
    <div class="hero-stat"><div class="num">5</div><div class="label">执行步骤</div></div>
    <div class="hero-stat"><div class="num">20</div><div class="label">KOC人设</div></div>
    <div class="hero-stat"><div class="num">2</div><div class="label">推演模型</div></div>
    <div class="hero-stat"><div class="num">48h</div><div class="label">标准交付</div></div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <div class="section-label">核心能力</div>
  <div class="section-title">四大家广告方法论融合</div>
  <div class="section-desc">不是堆砌概念。奥美叙事打底，BBDO差异进攻，盛世长城爆发，扬罗必凯评估。每个环节选最优工具。</div>
  <div class="grid4">
    <div class="card" onclick="showTab('method')"><div class="icon">&#127919;</div><h3>奥美 &middot; 品牌叙事</h3><p>不是说服，是让人爱上你。创始人故事、品牌宣言、情感共鸣文案。</p><span class="tag">情感连接</span></div>
    <div class="card" onclick="showTab('method')"><div class="icon">&#9876;</div><h3>BBDO &middot; 差异进攻</h3><p>先找差异化，再放大差异。品牌阶梯，竞品格局图，定位地图。</p><span class="tag">竞争定位</span></div>
    <div class="card" onclick="showTab('method')"><div class="icon">&#128293;</div><h3>盛世长城 &middot; 爆发</h3><p>没有注意力就没有品牌。PESO传播模型，爆款钩子，K值计算。</p><span class="tag">传播爆发</span></div>
    <div class="card" onclick="showTab('method')"><div class="icon">&#128202;</div><h3>扬罗必凯 &middot; 资产</h3><p>品牌是资产不是包装。BrandZ评估，品牌动力矩阵，20类人设分型。</p><span class="tag">品牌健康度</span></div>
  </div>

  <div class="section-label mt16">执行流程</div>
  <div class="section-title" style="margin-bottom:14px">5步闭环（点击每步）</div>
  <div class="box">
    <div class="flow">
      <div class="step" onclick="showTab('method')"><div class="circle">&#9312;</div><div class="fl">品牌定位诊断</div><div class="fs">SWOT+市场扫描</div></div>
      <div class="arr">&rarr;</div>
      <div class="step" onclick="showTab('method')"><div class="circle">&#9313;</div><div class="fl">核心叙事构建</div><div class="fs">故事+Slogan+KV</div></div>
      <div class="arr">&rarr;</div>
      <div class="step" onclick="showTab('simulate')"><div class="circle" style="border-color:var(--accent);color:var(--accent)">&#9314;</div><div class="fl">OASIS推演</div><div class="fs">爆款+舆情预测</div></div>
      <div class="arr">&rarr;</div>
      <div class="step" onclick="showTab('deliver')"><div class="circle">&#9315;</div><div class="fl">策略制定</div><div class="fs">执行包+话术</div></div>
      <div class="arr">&rarr;</div>
      <div class="step" onclick="showTab('deliver')"><div class="circle">&#9316;</div><div class="fl">交付执行</div><div class="fs">网页链接可分享</div></div>
    </div>
  </div>
</div>

<div class="section" style="padding-top:0">
  <div class="section-label">已验证案例</div>
  <div class="case">
    <div class="ch">
      <div>
        <h2 style="font-size:15px;margin-bottom:2px">成山农场 &middot; 新店开业推广执行包</h2>
        <p style="font-size:10px;color:var(--dim)">西安北郊 &middot; 7年12家店 &middot; 第13家新店 &middot; 2026-04-22交付</p>
      </div>
      <div class="ctag">已交付</div>
    </div>
    <div class="m4">
      <div class="m"><div class="v">K=1.5</div><div class="l">传播系数</div></div>
      <div class="m"><div class="v">25h</div><div class="l">出圈时间</div></div>
      <div class="m"><div class="v">72h</div><div class="l">库存安全</div></div>
      <div class="m"><div class="v">R0&gt;3</div><div class="l">危机指数</div></div>
    </div>
    <div class="out">
      <a href="https://846o436d9esq.space.minimaxi.com/index.html" target="_blank" class="o"><span class="dot"></span>总览入口</a>
      <a href="https://846o436d9esq.space.minimaxi.com/brand-copy.html" target="_blank" class="o"><span class="dot"></span>品牌文案</a>
      <a href="https://846o436d9esq.space.minimaxi.com/execution-14days.html" target="_blank" class="o"><span class="dot"></span>14天手册</a>
      <a href="https://846o436d9esq.space.minimaxi.com/koc-personas.html" target="_blank" class="o"><span class="dot"></span>20类KOC</a>
      <a href="https://846o436d9esq.space.minimaxi.com/crisis-playbook.html" target="_blank" class="o"><span class="dot"></span>危机预案</a>
    </div>
  </div>
</div>

<div class="section" style="padding-top:0">
  <div class="cta">
    <h2>给你的品牌做一套？</h2>
    <p>提供产品资料，48小时内交付完整品牌营销执行包</p>
    <button class="btn2" onclick="notify('请在对话框告诉我您的品牌信息，我来为您规划')">立即开始 &rarr;</button>
  </div>
</div>
</div>

<!-- ====== METHOD ====== -->
<div id="page-method" class="nd">
<div class="hero">
  <div class="hero-badge">方法论详解</div>
  <h1>四大家 &times; OASIS推演系统</h1>
  <p>每个环节选最优工具，不是堆砌概念</p>
</div>
<div class="section">
  <div class="grid4 grid2">
    <div class="card">
      <div class="icon">&#127919;</div>
      <h3>奥美 &middot; 品牌叙事法</h3>
      <p>核心：不是说服，是让人爱上你。品牌是产品与用户之间的情感纽带。</p>
      <div class="dark"><strong style="color:var(--accent)">代表工具</strong><br><span style="color:var(--dim)">大卫&middot;奥格威品牌形象论 / 品牌金字塔 / 360度接触点</span></div>
      <div class="dark"><strong style="color:var(--accent)">成山农场应用</strong><br><span style="color:var(--dim)">"他1994年生，7年前开了间小店，规矩只有一条：今天的菜，昨晚不能在地里。"</span></div>
    </div>
    <div class="card">
      <div class="icon">&#9876;</div>
      <h3>BBDO &middot; 差异进攻法</h3>
      <p>核心：先找差异化，再放大差异。品牌阶梯：属性&rarr;利益&rarr;价值观&rarr;品牌精髓。</p>
      <div class="dark"><strong style="color:var(--accent)">代表工具</strong><br><span style="color:var(--dim)">品牌阶梯分析 / 竞争格局图 / 定位地图</span></div>
      <div class="dark"><strong style="color:var(--accent)">成山农场应用</strong><br><span style="color:var(--dim)">"不卖隔夜菜"4个字，与永辉/盒马/社区夫妻店全部区隔</span></div>
    </div>
    <div class="card">
      <div class="icon">&#128293;</div>
      <h3>盛世长城 &middot; 爆发法则</h3>
      <p>核心：没有注意力就没有品牌。PESO模型：付费/赢得/共享/自有媒体。</p>
      <div class="dark"><strong style="color:var(--accent)">代表工具</strong><br><span style="color:var(--dim)">PESO传播模型 / 钩子设计 / 病毒K值</span></div>
      <div class="dark"><strong style="color:var(--accent)">成山农场应用</strong><br><span style="color:var(--dim)">D7-D9引爆：抖音直播+小红书KOC+社群同步爆发，K=1.5爆款级</span></div>
    </div>
    <div class="card">
      <div class="icon">&#128202;</div>
      <h3>扬罗必凯 &middot; 资产评估</h3>
      <p>核心：品牌是资产不是包装。BrandZ品牌资产评估，量化品牌强度和扩散度。</p>
      <div class="dark"><strong style="color:var(--accent)">代表工具</strong><br><span style="color:var(--dim)">BrandZ评估 / 品牌动力矩阵 / 20类用户分型</span></div>
      <div class="dark"><strong style="color:var(--accent)">成山农场应用</strong><br><span style="color:var(--dim)">"西北小胖东来"借势强势品牌背书，快速建立认知</span></div>
    </div>
  </div>

  <div class="section-label mt16">推演系统</div>
  <div class="section-title">OASIS双模型推演</div>
  <div class="section-desc">SIR传播模型 + IC舆情演化曲线，双模型叠加，量化预测推广效果</div>
  <div class="grid4 grid2">
    <div class="card">
      <div class="icon">&#127754;</div>
      <h3>SIR传播预测模型</h3>
      <p>S=易感人群 / I=传播者 / R=衰退者，K&gt;1.5为爆款级</p>
      <div class="dark"><strong style="color:var(--accent)">成山农场实测</strong><br><span style="color:var(--dim)">K=1.5，出圈时间25小时，500份库存72小时不售罄</span></div>
    </div>
    <div class="card">
      <div class="icon">&#128201;</div>
      <h3>IC舆情演化曲线</h3>
      <p>I=舆情强度（0-100）/ C=转化率，R0&gt;3为爆点级舆情</p>
      <div class="dark"><strong style="color:var(--accent)">成山农场危机推演</strong><br><span style="color:var(--dim)">农药残留场景R0&gt;3，极化指数0.6，竞品抢客204次</span></div>
    </div>
  </div>
</div>
</div>

<!-- ====== CASE ====== -->
<div id="page-case" class="nd">
<div class="hero">
  <div class="hero-badge">已验证案例</div>
  <h1>成山农场 &middot; 新店开业推广</h1>
  <p>西北精品生鲜，第13家新店，48小时完整交付</p>
</div>
<div class="section">
  <div class="case" style="margin-bottom:18px">
    <div class="ch">
      <div>
        <h2 style="font-size:14px;margin-bottom:2px">成山农场新店开业推广执行包</h2>
        <p style="font-size:10px;color:var(--dim)">2026-04-22 &middot; 玉衡（七政&middot;联合创始人）交付</p>
      </div>
      <div class="ctag">完整交付</div>
    </div>
    <div class="m4">
      <div class="m"><div class="v">K=1.5</div><div class="l">传播系数</div></div>
      <div class="m"><div class="v">25h</div><div class="l">出圈时间</div></div>
      <div class="m"><div class="v">72h</div><div class="l">库存安全</div></div>
      <div class="m"><div class="v">R0&gt;3</div><div class="l">危机指数</div></div>
    </div>
    <div style="background:var(--surface);border-radius:8px;padding:12px;margin-bottom:12px;font-size:10px;line-height:1.8;color:var(--dim)">
      <strong style="color:var(--text)">品牌核心：</strong>"西北，不卖隔夜菜"<br>
      <strong style="color:var(--text)">叙事锚点：</strong>刘帅伟，1994年生，凌晨4点田间，06:00采摘&rarr;09:00货架<br>
      <strong style="color:var(--text)">促销主线：</strong>14天，每天1款9.9元爆款，D7-D9抖音直播引爆
    </div>
    <div class="out">
      <a href="https://846o436d9esq.space.minimaxi.com/index.html" target="_blank" class="o"><span class="dot"></span>总览</a>
      <a href="https://846o436d9esq.space.minimaxi.com/brand-copy.html" target="_blank" class="o"><span class="dot"></span>品牌文案</a>
      <a href="https://846o436d9esq.space.minimaxi.com/execution-14days.html" target="_blank" class="o"><span class="dot"></span>14天手册</a>
      <a href="https://846o436d9esq.space.minimaxi.com/koc-personas.html" target="_blank" class="o"><span class="dot"></span>KOC人设</a>
      <a href="https://846o436d9esq.space.minimaxi.com/crisis-playbook.html" target="_blank" class="o"><span class="dot"></span>危机预案</a>
    </div>
  </div>

  <div class="section-label">KOC人设卡（部分展示）</div>
  <div class="k5">
    <div class="kt"><div class="e">&#129388;</div><h4>减脂健康党</h4><p>健身爱好者，常年带饭</p><div class="m">K5</div></div>
    <div class="kt"><div class="e">&#128104;&#127859;</div><h4>家常菜妈妈</h4><p>两个孩子妈妈，每天做饭</p><div class="m">K5</div></div>
    <div class="kt"><div class="e">&#129370;</div><h4>美食博主</h4><p>大众点评V6，餐饮从业者</p><div class="m">K4</div></div>
    <div class="kt"><div class="e">&#128118;</div><h4>新中产宝爸</h4><p>注重食品安全，有一孩</p><div class="m">K4</div></div>
    <div class="kt"><div class="e">&#127984;</div><h4>团购群主</h4><p>社区团购，邻里信任高</p><div class="m">K5</div></div>
  </div>
</div>
</div>

<!-- ====== SIMULATE ====== -->
<div id="page-simulate" class="nd">
<div class="hero">
  <div class="hero-badge">交互推演</div>
  <h1>爆款推广效果模拟</h1>
  <p>输入参数，实时预测传播效果和舆情演化</p>
</div>
<div class="section">
  <div class="panel">
    <div class="ph">
      <div class="pt">推广参数设置</div>
      <div class="tabs">
        <button class="tab on" onclick="setMode('promo',this)">开业推广</button>
        <button class="tab" onclick="setMode('crisis',this)">舆情危机</button>
      </div>
    </div>
    <div class="pb">
      <div class="row" id="inputs-promo">
        <div class="in"><label>促销折扣</label><input type="text" id="discount" value="8折" placeholder="如：8折"></div>
        <div class="in"><label>限量份数</label><input type="text" id="stock" value="500" placeholder="如：500"></div>
        <div class="in"><label>推广时长(小时)</label><input type="text" id="hours" value="72" placeholder="如：72"></div>
      </div>
      <div class="row nd" id="inputs-crisis">
        <div class="in"><label>危机场景</label><input type="text" id="crisis" value="食品安全" placeholder="如：食品安全"></div>
        <div class="in"><label>初始负面数</label><input type="text" id="neg" value="50" placeholder="如：50"></div>
        <div class="in"><label>推演时长(小时)</label><input type="text" id="chours" value="48" placeholder="如：48"></div>
      </div>
      <button class="btn" onclick="runSim()" id="simBtn">&#9654; 运行推演</button>

      <!-- PROMO RESULT -->
      <div class="res" id="res-promo">
        <h4>&#127775; 开业推广推演结果（基于SIR模型）</h4>
        <div class