# 教学交互组件模式（零依赖）

教学 app 里最常用的交互——分步讲解、并置对比、即时自测、参数联动——**用纯 HTML/CSS/JS 就能做好，不要为它们引框架**。引 Bootstrap 只为一个手风琴、引 Tailwind 只为几个间距，是浪费。下面是即用模式，全部接配色变量。

交互的目的永远是**服务理解**：让抽象可操作、让过程可单步、让对比可并置、让因果可试错。没有这个目的的动效是噪音。

## 1. 步骤器 Stepper（讲“过程/推导/算法”的主力）

把一个过程拆成 N 步，上一步/下一步切换，只看当前步，配进度。比一次性铺满全文更利于理解。

```html
<div class="stepper" id="st">
  <div class="step-bar"><div class="step-fill" id="fill"></div></div>
  <div class="step-body">
    <div class="step" data-step="0"><h3>第 1 步：提出问题</h3><p>……</p></div>
    <div class="step" data-step="1" hidden><h3>第 2 步：建立模型</h3><p>……</p></div>
    <div class="step" data-step="2" hidden><h3>第 3 步：求解</h3><p>……</p></div>
  </div>
  <div class="step-nav">
    <button id="prev">← 上一步</button>
    <span id="ind" class="muted"></span>
    <button id="next">下一步 →</button>
  </div>
</div>
<style>
  .step-bar{height:4px;background:var(--border);border-radius:2px;overflow:hidden;margin-bottom:var(--space-4)}
  .step-fill{height:100%;background:var(--primary);transition:width .3s}
  .step-body{min-height:120px}
  .step-nav{display:flex;justify-content:space-between;align-items:center;margin-top:var(--space-4)}
  .muted{color:var(--fg-muted);font-size:14px}
</style>
<script>
  const steps=[...document.querySelectorAll('#st .step')]; let i=0;
  const show=()=>{ steps.forEach((s,k)=>s.hidden=k!==i);
    document.getElementById('fill').style.width=((i+1)/steps.length*100)+'%';
    document.getElementById('ind').textContent=`${i+1} / ${steps.length}`;
    document.getElementById('prev').disabled=i===0;
    document.getElementById('next').disabled=i===steps.length-1; };
  document.getElementById('prev').onclick=()=>{ if(i>0){i--;show();} };
  document.getElementById('next').onclick=()=>{ if(i<steps.length-1){i++;show();} };
  show();
</script>
```

## 2. 标签页 Tabs（并置对比/分类知识点）

```html
<div class="tabs" id="tb">
  <div class="tab-heads">
    <button class="tab-h active" data-t="0">观点 A</button>
    <button class="tab-h" data-t="1">观点 B</button>
    <button class="tab-h" data-t="2">对比</button>
  </div>
  <div class="tab-panel">内容 A……</div>
  <div class="tab-panel" hidden>内容 B……</div>
  <div class="tab-panel" hidden>对比……</div>
</div>
<style>
  .tab-heads{display:flex;gap:var(--space-1);border-bottom:2px solid var(--border)}
  .tab-h{border:none;background:none;padding:var(--space-3) var(--space-4);cursor:pointer;
         color:var(--fg-muted);border-bottom:2px solid transparent;margin-bottom:-2px;font-size:15px}
  .tab-h.active{color:var(--primary);border-bottom-color:var(--primary);font-weight:600}
  .tab-panel{padding:var(--space-4) 0}
</style>
<script>
  const tb=document.getElementById('tb'), panels=[...tb.querySelectorAll('.tab-panel')];
  tb.querySelectorAll('.tab-h').forEach(b=>b.onclick=()=>{
    tb.querySelectorAll('.tab-h').forEach(x=>x.classList.remove('active'));
    b.classList.add('active'); panels.forEach((p,k)=>p.hidden=k!=b.dataset.t);
  });
</script>
```

## 3. 手风琴 Accordion（FAQ/层层展开/可选深入）

```html
<div class="acc">
  <details><summary>什么是熵？</summary><div class="acc-body">熵衡量不确定性……</div></details>
  <details><summary>它和信息有什么关系？</summary><div class="acc-body">……</div></details>
</div>
<style>
  .acc details{border:1px solid var(--border);border-radius:var(--radius-sm);margin-bottom:var(--space-2);background:var(--surface)}
  .acc summary{padding:var(--space-3) var(--space-4);cursor:pointer;font-weight:600;list-style:none}
  .acc summary::after{content:'+';float:right;color:var(--primary)}
  .acc details[open] summary::after{content:'−'}
  .acc-body{padding:0 var(--space-4) var(--space-4);color:var(--fg-muted)}
</style>
```
用原生 `<details>`，零 JS。渐进式披露的本体——次要细节折叠起来，想深入再点开。

## 4. 滑块联动 Live Parameter（“可调参数”教学，威力最大）

把抽象关系变成可手动调的实时反馈。配合公式/图表/SVG，让学习者亲手试出因果。

```html
<label>温度 T = <strong id="tval">300</strong> K</label>
<input type="range" id="t" min="0" max="1000" value="300" style="width:100%">
<p>分子平均动能 ∝ T：<span id="out"></span></p>
<style>
  input[type=range]{accent-color:var(--primary)}   /* 一行让滑块用主色 */
</style>
<script>
  const t=document.getElementById('t');
  const update=()=>{ document.getElementById('tval').textContent=t.value;
    document.getElementById('out').textContent=(t.value*0.0138).toFixed(2)+' (相对值)'; };
  t.addEventListener('input', update); update();
</script>
```
联动目标可以是：KaTeX 公式重渲染、Chart 数据更新后 `chart.update()`、SVG 元素属性、Canvas 重绘。

## 5. 即时反馈测验 Quiz（巩固/自测）

```html
<div class="quiz" data-answer="1">
  <p class="q">下列哪项是渐进式披露的核心？</p>
  <button class="opt" data-i="0">把所有内容一次展示</button>
  <button class="opt" data-i="1">按需逐层展开细节</button>
  <button class="opt" data-i="2">只用图片</button>
  <p class="fb" hidden></p>
</div>
<style>
  .opt{display:block;width:100%;text-align:left;margin:var(--space-1) 0;padding:var(--space-3);
       border:1px solid var(--border);border-radius:var(--radius-sm);background:var(--surface);cursor:pointer}
  .opt:hover{border-color:var(--primary)}
  .opt.right{border-color:var(--success);background:color-mix(in srgb,var(--success) 12%,transparent)}
  .opt.wrong{border-color:var(--danger);background:color-mix(in srgb,var(--danger) 12%,transparent)}
  .fb{margin-top:var(--space-2);font-size:14px}
</style>
<script>
  document.querySelectorAll('.quiz').forEach(q=>{
    const ans=+q.dataset.answer, fb=q.querySelector('.fb');
    q.querySelectorAll('.opt').forEach(o=>o.onclick=()=>{
      q.querySelectorAll('.opt').forEach(x=>x.classList.remove('right','wrong'));
      const ok=+o.dataset.i===ans; o.classList.add(ok?'right':'wrong');
      if(!ok) q.querySelector(`[data-i="${ans}"]`).classList.add('right');
      fb.hidden=false; fb.textContent=ok?'✓ 正确！':'再想想——正确答案已标绿。';
      fb.style.color=ok?'var(--success)':'var(--danger)';
    });
  });
</script>
```

## 6. 点击高亮/术语解释 Reveal-on-hover

```html
<p>这是一个 <span class="term" data-tip="衡量信息不确定性的量">熵</span> 的例子。</p>
<style>
  .term{border-bottom:1.5px dotted var(--primary);cursor:help;position:relative}
  .term:hover::after{content:attr(data-tip);position:absolute;left:0;bottom:130%;
    background:var(--fg);color:var(--bg);padding:6px 10px;border-radius:6px;
    font-size:13px;white-space:nowrap;box-shadow:var(--shadow);z-index:10}
</style>
```
正文里给术语挂即时释义，不打断阅读。纯 CSS。

## 7. 锚点导航 / 目录（长教学页）

长内容用左侧/顶部目录跳转，比 Reveal 翻页更适合“可回看的讲义”。

```html
<nav class="toc">
  <a href="#s1">1 引入</a><a href="#s2">2 原理</a><a href="#s3">3 应用</a>
</nav>
<style>
  .toc{position:sticky;top:0;display:flex;gap:var(--space-4);padding:var(--space-3) 0;
       background:var(--bg);border-bottom:1px solid var(--border);z-index:5}
  .toc a{color:var(--fg-muted);text-decoration:none}
  .toc a:hover{color:var(--primary)}
  html{scroll-behavior:smooth}
</style>
```

## 组合建议

- **概念讲解类**：锚点导航 + 术语高亮 + 手风琴（深入内容折叠）+ 文末测验。
- **过程/算法类**：步骤器 + 每步配 SVG/Canvas 图 + 文末测验。
- **数据/实验类**：滑块联动 + 实时图表（Chart.js/ECharts）。
- **对比类**：标签页 或 左右并置两栏。

不确定要不要做成交互的，问自己：**“静态文字+一张图能不能讲清？”** 能就别加交互。交互只用在静态讲不清的地方（过程演化、参数因果、需要亲手试）。
