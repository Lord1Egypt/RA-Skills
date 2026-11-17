# 通用 HTML 演示文稿骨架（兜底）

> 当 L2 风格正文缺失/建设中时，按本骨架降级生成，并在交付说明中明示「以下基于通用骨架生成」。

## 单文件 HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>演示标题</title>
<style>
  :root{
    --bg:#ffffff; --ink:#111111; --ac:#2563eb; --card:#f5f5f7;
    --mu:#666666; --line:#e5e5e5; --font:'Noto Sans SC',system-ui,sans-serif;
  }
  *{ box-sizing:border-box; margin:0; padding:0; }
  body{ font-family:var(--font); background:var(--bg); color:var(--ink);
        -webkit-font-smoothing:antialiased; }
  .slide{ min-height:100vh; display:flex; flex-direction:column;
          justify-content:center; padding:8vh 8vw; }
  .slide.cover{ align-items:center; text-align:center; }
  h1{ font-size:clamp(2rem,5vw,4rem); font-weight:700; line-height:1.15; }
  h2{ font-size:clamp(1.4rem,3vw,2.2rem); font-weight:600; margin-bottom:1.5rem; }
  p,li{ font-size:1.05rem; line-height:1.7; color:var(--ink); }
  .muted{ color:var(--mu); }
  .grid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1.25rem; }
  .card{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:1.5rem; }
  .accent{ color:var(--ac); }
  .btn{ display:inline-block; background:var(--ac); color:#fff; padding:.8rem 2rem;
        border-radius:999px; font-weight:600; text-decoration:none; }
  /* 翻页：默认只显示当前页 */
  .slide{ display:none; }
  .slide.on{ display:flex; animation:fadeIn .4s ease; }
  @keyframes fadeIn{ from{opacity:0; transform:translateY(8px);} to{opacity:1; transform:none;} }
  /* 左右箭头按钮 */
  .arrow{ position:fixed; top:50%; transform:translateY(-50%); z-index:99;
          width:44px; height:44px; border:none; border-radius:50%; cursor:pointer;
          background:var(--card); color:var(--ink); font-size:1.2rem;
          box-shadow:0 4px 14px rgba(0,0,0,.12); }
  .arrow.prev{ left:16px; } .arrow.next{ right:16px; }
  .arrow:disabled{ opacity:.3; cursor:default; }
  /* 底部页码 + 进度条 */
  .progress-bar{ position:fixed; left:0; right:0; bottom:0; z-index:99;
          display:flex; align-items:center; gap:12px; padding:10px 24px;
          background:var(--card); border-top:1px solid var(--line);
          font-size:.85rem; color:var(--mu); }
  .progress-bar .track{ flex:1; height:4px; background:var(--line); border-radius:999px; overflow:hidden; }
  .progress-bar .fill{ height:100%; background:var(--ac); border-radius:999px; transition:width .3s ease; }
  /* 圆点跳页 */
  .dots{ flex:1; display:flex; align-items:center; justify-content:center; gap:10px; }
  .dot{ width:8px; height:8px; border-radius:999px; border:none; padding:0;
        background:var(--line); cursor:pointer; transition:all .25s ease; }
  .dot:hover{ background:var(--ac); transform:scale(1.3); }
  .dot.on{ width:24px; background:var(--ac); }
  @media (max-width:640px){ .slide{ padding:6vh 6vw; } .arrow{ width:36px; height:36px; } .dot{ width:7px; height:7px; } .dot.on{ width:18px; } }
</style>
</head>
<body>
  <!-- 封面页 -->
  <section class="slide cover on">
    <h1>演示主标题</h1>
    <p class="muted">副标题 / 品牌 / 日期</p>
  </section>
  <!-- 内容页 -->
  <section class="slide">
    <h2>章节标题</h2>
    <div class="grid">
      <div class="card"><h3>要点一</h3><p>说明文字…</p></div>
      <div class="card"><h3>要点二</h3><p>说明文字…</p></div>
    </div>
  </section>
  <!-- 结尾页 -->
  <section class="slide cover">
    <h1>谢谢</h1>
    <p class="muted">联系方式 / 行动号召</p>
  </section>
  <!-- 翻页控件 -->
  <button class="arrow prev" onclick="go(cur-1)">‹</button>
  <button class="arrow next" onclick="go(cur+1)">›</button>
  <div class="progress-bar">
    <span id="pageNum">1 / 3</span>
    <div class="dots" id="dots"></div>
    <div class="track"><div class="fill" id="pageFill" style="width:33.3%"></div></div>
  </div>
<script>
  const slides=[...document.querySelectorAll('.slide')]; let cur=0;
  const dotsWrap=document.getElementById('dots');
  dotsWrap.innerHTML=slides.map((_,i)=>
    `<button class="dot" title="第 ${i+1} 页" onclick="go(${i})"></button>`).join('');
  function go(i){ cur=Math.max(0,Math.min(slides.length-1,i));
    slides.forEach((s,k)=>s.classList.toggle('on',k===cur));
    document.getElementById('pageNum').textContent=(cur+1)+' / '+slides.length;
    document.getElementById('pageFill').style.width=((cur+1)/slides.length*100)+'%';
    dotsWrap.querySelectorAll('.dot').forEach((d,k)=>d.classList.toggle('on',k===cur));
    document.querySelector('.arrow.prev').disabled=cur===0;
    document.querySelector('.arrow.next').disabled=cur===slides.length-1; }
  document.addEventListener('keydown',e=>{ if(e.key==='ArrowRight')go(cur+1); if(e.key==='ArrowLeft')go(cur-1); });
  let tx=0; document.addEventListener('touchstart',e=>tx=e.touches[0].clientX);
  document.addEventListener('touchend',e=>{ const dx=e.changedTouches[0].clientX-tx; if(dx<-40)go(cur+1); if(dx>40)go(cur-1); });
</script>
</body>
</html>
```

## 关键原则

1. **CSS 变量承载 token**：所有颜色走 `--bg/--ink/--ac/--card/--mu/--line`，风格切换只改 `:root`。
2. **clamp() 流式字号**：标题用 `clamp()` 保证跨屏可读。
3. **grid + auto-fit**：卡片网格自适应列数。
4. **语义化**：`<section>` 分页、`<h1>-<h3>` 层级、`<p>/<li>` 正文。
5. **左右翻页**：`.slide{ display:none }` 只显示当前页；键盘 `←`/`→` + 箭头按钮 + 触屏滑动三通道切换。
6. **底部进度 + 圆点跳页**：固定底栏「当前页 / 总页数」+ 进度条（宽 = N/M）+ 可点击圆点（当前页拉长胶囊高亮，点击直达），随翻页实时同步，强调色填充。
7. **零外部依赖**：无 CDN、无网络请求；字体用系统字体栈。
