# 单文件骨架 + 质量清单

下面是一个**可直接双击打开运行**的空教学 app 骨架。复制它当地基：换标题、贴上选定的配色 `:root`、按需取消注释 CDN、往 `<main>` 里填内容和交互。它自带一套精炼的通用 UI 原子（card / btn / callout / badge / grid），生成的 app 不用每次从零写样式。

骨架默认用「深空蓝」配色——换配色就把 `:root` 里 `--bg` 起到 `--chart-6` 那一段，替换成 color-schemes.md 里另一套的对应段（变量名一致，其余不用动）。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__标题__</title>

<!-- ===== 按需取消注释引入库（URL/坑见 cdn-catalog.md & libraries.md）=====
<script src="https://cdn.bootcdn.net/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/mermaid/10.9.0/mermaid.min.js"></script>
<link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.9/katex.min.css">
<script src="https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
================================================================= -->

<style>
:root{
  /* —— 排版（所有配色共用，照搬 color-schemes.md）—— */
  --font-sans:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei','Source Han Sans SC',sans-serif;
  --font-serif:Georgia,'Times New Roman','Songti SC','STSong','SimSun',serif;
  --font-mono:'SF Mono','JetBrains Mono',Consolas,'Courier New',monospace;
  --space-1:4px;--space-2:8px;--space-3:12px;--space-4:16px;--space-5:24px;--space-6:32px;--space-8:48px;
  --radius:10px;--radius-sm:6px;--radius-lg:16px;--maxw:1080px;
  /* —— 配色：此处为「深空蓝」，换方案替换这一段 —— */
  --bg:#0b1120;--surface:#141d33;--surface-2:#1c2742;
  --fg:#e6edf7;--fg-muted:#93a4c0;--border:#263149;
  --primary:#4f9dff;--primary-weak:rgba(79,157,255,.12);--accent:#22d3ee;
  --success:#34d399;--warning:#fbbf24;--danger:#f87171;
  --chart-1:#4f9dff;--chart-2:#22d3ee;--chart-3:#a78bfa;--chart-4:#fbbf24;--chart-5:#f472b6;--chart-6:#34d399;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 8px 30px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--font-sans);
     line-height:1.7;font-size:16px;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--maxw);margin:0 auto;padding:var(--space-6) var(--space-5)}
h1{font-size:30px;line-height:1.25;margin:0 0 var(--space-2)}
h2{font-size:22px;margin:var(--space-8) 0 var(--space-3)}
h3{font-size:17px;margin:var(--space-5) 0 var(--space-2)}
p{margin:0 0 var(--space-4)}
a{color:var(--primary)}
.lead{color:var(--fg-muted);font-size:18px;margin-bottom:var(--space-6)}
.muted{color:var(--fg-muted)}
code{font-family:var(--font-mono);background:var(--surface-2);padding:2px 6px;border-radius:4px;font-size:.9em}
/* header */
header.hero{border-bottom:1px solid var(--border);background:var(--surface);
            padding:var(--space-8) 0;margin-bottom:var(--space-6)}
/* card */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
      padding:var(--space-5);box-shadow:var(--shadow);margin-bottom:var(--space-4)}
/* button */
.btn{font:inherit;border:1px solid var(--border);background:var(--surface-2);color:var(--fg);
     padding:var(--space-2) var(--space-4);border-radius:var(--radius-sm);cursor:pointer;transition:.15s}
.btn:hover{border-color:var(--primary)}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-primary{background:var(--primary);border-color:var(--primary);color:#fff}
/* callout */
.callout{border-left:4px solid var(--primary);background:var(--primary-weak);
         padding:var(--space-3) var(--space-4);border-radius:var(--radius-sm);margin:var(--space-4) 0}
.callout-warn{border-left-color:var(--warning);background:color-mix(in srgb,var(--warning) 10%,transparent)}
.callout-success{border-left-color:var(--success);background:color-mix(in srgb,var(--success) 10%,transparent)}
/* badge */
.badge{display:inline-block;font-size:12px;padding:2px 8px;border-radius:999px;
       background:var(--primary-weak);color:var(--primary);font-weight:600}
/* grid */
.grid{display:grid;gap:var(--space-4)}
.grid-2{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.grid-3{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
input[type=range]{accent-color:var(--primary);width:100%}
@media(max-width:600px){.wrap{padding:var(--space-5) var(--space-4)}h1{font-size:24px}}
</style>
</head>
<body>

<header class="hero">
  <div class="wrap">
    <span class="badge">__学科/章节__</span>
    <h1>__主标题：这个 app 教什么__</h1>
    <p class="lead">__一句话副标题：学完能理解什么 / 能动手试什么__</p>
  </div>
</header>

<main class="wrap">
  <!-- 在这里填内容与交互。组件模式见 components.md，图表/公式片段见 libraries.md。 -->
  <section class="card">
    <h2>占位小节</h2>
    <p>正文……</p>
  </section>
</main>

<script>
// 交互逻辑。优先零依赖组件（components.md）；要图表/公式/图解再用库（libraries.md）。
</script>
</body>
</html>
```

## 质量清单（交付前逐条过）

**单文件 & 可运行**
- [ ] 全部 HTML/CSS/JS 在**一个 .html** 里，双击浏览器直接打开能跑，无需服务器/构建。
- [ ] 外部依赖只有 CDN 链接；没有本地文件引用、没有 `import` ES 模块裸路径。
- [ ] 引入的每个库都真的用上了——没用到的 `<script>` 删掉（加载越少越快越稳）。

**CDN 正确**
- [ ] 每个 CDN URL 来自 cdn-catalog.md（验证过），不是凭记忆拼的。
- [ ] 关键脚本库加了 fallback（见 cdn-catalog.md 的 `window.X || document.write(...)`）。
- [ ] 用到 KaTeX 则引了它的 CSS；用到 Highlight.js 则引了主题 CSS。

**配色 & 排版**
- [ ] 用了一套完整配色 `:root`，颜色全走 `var(--…)`，没有散落的硬编码十六进制。
- [ ] 遵守 60-30-10：主色/accent 是点缀不是底色；正文是 `--fg` 不上彩。
- [ ] 图表/Mermaid 的颜色也接了配色变量（见 color-schemes.md「让图表库吃这套变量」）。
- [ ] 移动端不破版（有 viewport meta；宽组件能换行/横向滚动）。

**教学性**
- [ ] 每个交互都在帮理解（揭示过程/参数因果/对比/自测），不是装饰性动效。
- [ ] 内容忠实于输入文本，没编造原文没有的「事实」「数据」「研究」。
- [ ] 信息有层次：先主干后细节，次要内容可折叠（手风琴/details）。
- [ ] 有一个清楚的「入口」——打开就知道这是讲什么的、怎么用。

**健壮**
- [ ] Chart.js 的 canvas 在固定高度容器里；ECharts 监听了 resize。
- [ ] JS 没有未捕获报错（控制台干净）；库未加载时有合理降级（不白屏）。
