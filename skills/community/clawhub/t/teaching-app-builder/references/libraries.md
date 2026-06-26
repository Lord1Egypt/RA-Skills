# 各库即用片段

每个库给：CDN 标签（URL 见 cdn-catalog.md）+ 最小可用代码 + 最容易踩的坑。目标是贴进单文件就能跑，并和选定的配色变量协调。

## Chart.js — 常规统计图

```html
<!-- 坑：canvas 必须放在固定高度的容器里，否则 responsive 会把页面无限撑高 -->
<div style="height:340px; position:relative;">
  <canvas id="chart1"></canvas>
</div>
<script src="https://cdn.bootcdn.net/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
  const css = getComputedStyle(document.documentElement);
  const C = n => css.getPropertyValue(`--chart-${n}`).trim();
  Chart.defaults.color = css.getPropertyValue('--fg').trim();
  Chart.defaults.borderColor = css.getPropertyValue('--border').trim();
  Chart.defaults.font.family = css.getPropertyValue('--font-sans').trim();

  new Chart(document.getElementById('chart1'), {
    type: 'line',                       // line | bar | pie | doughnut | radar | scatter
    data: {
      labels: ['一月','二月','三月','四月'],
      datasets: [{ label:'销量', data:[12,19,8,15], borderColor:C(1),
                   backgroundColor:C(1)+'33', tension:.3, fill:true }]
    },
    options: { responsive:true, maintainAspectRatio:false,
               plugins:{ legend:{ position:'bottom' } } }
  });
</script>
```
适合常规折线/柱/饼/雷达。要交互教学可加按钮切换 `data` 后 `chart.update()`。

## ECharts — 复杂/国产生态图表

```html
<div id="ec1" style="height:380px;"></div>
<script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.5.0/echarts.min.js"></script>
<script>
  const css = getComputedStyle(document.documentElement);
  const palette = [1,2,3,4,5,6].map(n => css.getPropertyValue(`--chart-${n}`).trim());
  const chart = echarts.init(document.getElementById('ec1'));
  chart.setOption({
    color: palette,
    textStyle:{ color: css.getPropertyValue('--fg').trim(),
                fontFamily: css.getPropertyValue('--font-sans').trim() },
    tooltip:{ trigger:'axis' },
    xAxis:{ type:'category', data:['A','B','C','D'] },
    yAxis:{ type:'value' },
    series:[{ type:'bar', data:[5,20,36,10] }]
  });
  window.addEventListener('resize', () => chart.resize());  // 坑：不监听 resize 不会自适应
</script>
```
关系图、桑基图、地图、大数据散点、需要内置丰富交互时选 ECharts 而非 Chart.js。

## Mermaid — 流程图/时序/结构（讲“关系与过程”首选）

```html
<pre class="mermaid">
flowchart LR
  A[输入文本] --> B{是否含数据?}
  B -- 是 --> C[Chart.js]
  B -- 否 --> D[Mermaid 图解]
</pre>
<script src="https://cdn.bootcdn.net/ajax/libs/mermaid/10.9.0/mermaid.min.js"></script>
<script>
  const dark = matchMedia && false; // 按你的配色明暗决定
  mermaid.initialize({
    startOnLoad: true,              // 自动渲染所有 .mermaid 元素
    theme: 'base',
    themeVariables: {               // 让图配色 = 页面配色
      primaryColor:  getComputedStyle(document.documentElement).getPropertyValue('--primary-weak').trim(),
      primaryBorderColor: getComputedStyle(document.documentElement).getPropertyValue('--primary').trim(),
      lineColor:     getComputedStyle(document.documentElement).getPropertyValue('--fg-muted').trim(),
      textColor:     getComputedStyle(document.documentElement).getPropertyValue('--fg').trim(),
      fontFamily:    getComputedStyle(document.documentElement).getPropertyValue('--font-sans').trim()
    }
  });
</script>
```
- 坑：图定义里**缩进/换行敏感**，`<pre>` 内不要混入 HTML 缩进的多余空格；节点文字含特殊字符用 `["..."]` 包起来。
- 动态生成图：`const {svg} = await mermaid.render('gid', def); container.innerHTML = svg;`（注意 `startOnLoad:false` 时才手动渲染）。
- 支持的图类型：`flowchart` `sequenceDiagram` `classDiagram` `stateDiagram-v2` `gantt` `mindmap` `erDiagram` `timeline` `pie`。

## KaTeX — 数学公式（快）

```html
<link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.9/katex.min.css">
<script src="https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
  // 自动扫描全文里的 $...$ 和 $$...$$ 渲染
  document.addEventListener('DOMContentLoaded', () => {
    renderMathInElement(document.body, {
      delimiters: [
        {left:'$$', right:'$$', display:true},
        {left:'$',  right:'$',  display:false},
        {left:'\\(', right:'\\)', display:false}
      ]
    });
  });
  // 或单点渲染到某元素：
  // katex.render('E = mc^2', document.getElementById('eq'), {throwOnError:false});
</script>
```
- 坑：**必须引 katex.min.css**，否则公式样式全乱。auto-render 要等 DOMContentLoaded。
- 公式联动参数：把可调值拼进 LaTeX 字符串重新 `katex.render`，配滑块做“可调公式”教学。
- 复杂 LaTeX/化学式 mhchem 兼容不好时换 MathJax（`tex-mml-chtml.js`，单文件、无需额外 CSS，但更重）。

## D3 — 自定义数据可视化

```html
<svg id="d3svg" width="480" height="240"></svg>
<script src="https://cdn.bootcdn.net/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
  const data = [4, 8, 15, 16, 23, 42];
  const svg = d3.select('#d3svg');
  const x = d3.scaleBand().domain(data.map((_,i)=>i)).range([30,470]).padding(.2);
  const y = d3.scaleLinear().domain([0, d3.max(data)]).range([220,20]);
  svg.selectAll('rect').data(data).join('rect')
     .attr('x', (_,i)=>x(i)).attr('y', d=>y(d))
     .attr('width', x.bandwidth()).attr('height', d=>220-y(d))
     .attr('fill', getComputedStyle(document.documentElement).getPropertyValue('--chart-1').trim());
  svg.append('g').attr('transform','translate(0,220)').call(d3.axisBottom(x));
  svg.append('g').attr('transform','translate(30,0)').call(d3.axisLeft(y));
</script>
```
D3 学习曲线陡——**简单图别用 D3，用 Chart.js**。只在需要力导向图、地理投影、完全自定义的交互可视化时上 D3。

## SVG.js — 轻量画自定义示意图

```html
<div id="svgbox"></div>
<script src="https://cdn.bootcdn.net/ajax/libs/svg.js/3.2.4/svg.min.js"></script>
<script>
  const draw = SVG().addTo('#svgbox').size(400, 200);
  const c = getComputedStyle(document.documentElement);
  draw.rect(120,60).move(40,40).fill(c.getPropertyValue('--primary').trim()).radius(8);
  draw.text('概念A').move(60,62).font({fill:'#fff', size:16});
  const dot = draw.circle(20).center(300,70).fill(c.getPropertyValue('--accent').trim());
  dot.animate(1500).center(300,140).loop(true, true);   // 自带补间动画
</script>
```
画几何示意、状态机、自定义图示。比裸操作 SVG DOM 顺手。

## 动画：anime.js / GSAP

```html
<script src="https://cdn.bootcdn.net/ajax/libs/animejs/3.2.2/anime.min.js"></script>
<script>
  anime({ targets:'.box', translateX:240, rotate:'1turn',
          duration:1200, easing:'easeInOutQuad', delay:anime.stagger(120) });
</script>
```
分步演示（依次点亮步骤、元素入场）。GSAP（`gsap.min.js`，`gsap.to('.box',{x:240,duration:1})`）更强、时间线更好控，复杂编排时用。

## Rough.js — 手绘/板书风（npmmirror）

```html
<canvas id="rc" width="400" height="200"></canvas>
<script src="https://registry.npmmirror.com/roughjs/4.6.6/files/bundled/rough.js"></script>
<script>
  const rc = rough.canvas(document.getElementById('rc'));
  rc.rectangle(20,20,160,90, {stroke:'#c2410c', roughness:1.8});
  rc.line(20,150, 380,150, {stroke:'#333'});
</script>
```
草图/板书质感，亲和力强，适合轻松的科普。注意它在 bootcdn 没有，用 npmmirror。

## 代码教学：Highlight.js + marked

```html
<link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/highlight.js/11.10.0/styles/github-dark.min.css">
<script src="https://cdn.bootcdn.net/ajax/libs/highlight.js/11.10.0/highlight.min.js"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/marked/12.0.2/marked.min.js"></script>
<script>
  // 把一段 Markdown 渲染成 HTML 再高亮其中代码块
  document.getElementById('article').innerHTML = marked.parse(mdText);
  document.querySelectorAll('pre code').forEach(el => hljs.highlightElement(el));
</script>
```
亮色配色选 `github.min.css` 主题，暗色选 `github-dark.min.css`。

## Reveal.js — 翻页幻灯片（仅当明确要“课件/PPT”）

```html
<link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/reveal.js/5.1.0/reveal.min.css">
<link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/reveal.js/5.1.0/theme/white.min.css">
<div class="reveal"><div class="slides">
  <section><h2>标题页</h2></section>
  <section>第二页<aside class="notes">演讲备注</aside></section>
</div></div>
<script src="https://cdn.bootcdn.net/ajax/libs/reveal.js/5.1.0/reveal.min.js"></script>
<script>Reveal.initialize({ hash:true });</script>
```
坑：Reveal 接管整页全屏布局，**和自定义滚动页面布局互斥**——只在要做“一页页翻”的演示时用，否则用普通滚动页 + 锚点导航。

## 选型一句话总结

- 有数据要画 → **Chart.js**（简单）/ **ECharts**（复杂、国产生态）
- 讲流程/结构/关系 → **Mermaid**
- 自定义示意图/几何 → **SVG.js** / 原生 SVG；草图感加 **Rough.js**
- 完全自定义的数据可视化交互 → **D3**
- 数学公式 → **KaTeX**（常规）/ **MathJax**（复杂）
- 动画演示 → **anime.js**（轻）/ **GSAP**（强）
- 代码 → **Highlight.js**(+marked)
- 翻页课件 → **Reveal.js**
- 排版/组件 → **Tailwind**（原子类、灵活）/ **Bootstrap**（现成组件）；也可只用本仓配色变量手写
- 能用纯 HTML/CSS/JS 讲清的（标签页、手风琴、步骤器、测验）→ 不引库，见 components.md
