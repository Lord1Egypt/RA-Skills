# CDN 清单（中国大陆可访问，已逐条验证）

本表所有 URL 均用 `curl` 实测返回 200。**优先从这里取 URL，不要凭记忆拼**——库名大小写、版本号、文件名很容易记错（例如 Chart.js 的库名首字母大写、bootstrap 在 cdnjs 系里叫 `twitter-bootstrap`）。

## 四大 CDN 与 URL 模板

国内三家（BootCDN / staticfile / 360）都镜像自 cdnjs，**库名 / 版本 / 文件路径完全一致**，所以同一个库换域名即可互为备用。npmmirror 是 npm 全量镜像，覆盖最广（冷门库去这里），但路径格式不同。

| CDN | 维护方 | URL 模板 | 特点 |
|---|---|---|---|
| **BootCDN** | 七牛/Bootstrap 中文 | `https://cdn.bootcdn.net/ajax/libs/<库>/<版本>/<文件>` | 默认首选，库全速度好 |
| **staticfile** | 七牛云 | `https://cdn.staticfile.net/<库>/<版本>/<文件>` | 备用 1，路径同 BootCDN |
| **360 前端库** | 奇虎 360 | `https://lib.baomitu.com/<库>/<版本>/<文件>` | 备用 2，路径同 BootCDN |
| **npmmirror** | 阿里巴巴 | `https://registry.npmmirror.com/<包>/<版本>/files/<包内路径>` | 全量 npm 镜像，覆盖冷门库 |

> 注：`cdn.staticfile.org` 是旧域名，新域名 `cdn.staticfile.net` 更稳；`cdn.bootcss.com` 已并入 bootcdn.net。

## 经验证的库 URL（直接复制）

### 图表

```
Chart.js 4.4.1   https://cdn.bootcdn.net/ajax/libs/Chart.js/4.4.1/chart.umd.min.js
ECharts 5.5.0    https://cdn.bootcdn.net/ajax/libs/echarts/5.5.0/echarts.min.js
```
- **Chart.js**：库名 `Chart.js`（C 大写），文件 `chart.umd.min.js`（不是 `chart.min.js`）。轻量、API 简单，适合常规折线/柱/饼/雷达。
- **ECharts**：百度出品，国内生态最熟。适合地图、关系图、桑基图、复杂大数据、需要丰富默认主题时。

### 图解 / 流程图

```
Mermaid 10.9.0   https://cdn.bootcdn.net/ajax/libs/mermaid/10.9.0/mermaid.min.js
```
流程图、时序图、类图、状态图、甘特图、思维导图、ER 图——用文本描述结构自动排版，**教学讲"流程/关系/结构"首选**。

### CSS 框架 / 布局

```
Bootstrap 5.3.3 CSS  https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.3.3/css/bootstrap.min.css
Bootstrap 5.3.3 JS   https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.3.3/js/bootstrap.bundle.min.js
Tailwind Play CDN    https://cdn.tailwindcss.com/3.4.16
Tailwind 全量(备用)  https://cdn.bootcdn.net/ajax/libs/tailwindcss/2.2.19/tailwind.min.css
```
- **Bootstrap**：库名 `twitter-bootstrap`。组件齐全（导航/卡片/手风琴/标签页/模态框/工具提示），开箱即用，国内 CDN 稳。`bootstrap.bundle.min.js` 已含 Popper，交互组件直接能用。
- **Tailwind**：官方 Play CDN `cdn.tailwindcss.com/3.4.16`（**固定到 3.4.16，不要用裸 `cdn.tailwindcss.com` 滚动版**）。它走 Cloudflare，国内偶尔慢——若担心可达性，退回 bootcdn 的 `tailwindcss/2.2.19/tailwind.min.css`（v2 全量预编译，无 JIT 但够用），或干脆不用 Tailwind 改用本仓的配色变量 + 手写 CSS。

### SVG / 绘图 / 动画

```
D3 7.9.0         https://cdn.bootcdn.net/ajax/libs/d3/7.9.0/d3.min.js
SVG.js 3.2.4     https://cdn.bootcdn.net/ajax/libs/svg.js/3.2.4/svg.min.js
Snap.svg 0.5.1   https://cdn.bootcdn.net/ajax/libs/snap.svg/0.5.1/snap.svg-min.js
anime.js 3.2.2   https://cdn.bootcdn.net/ajax/libs/animejs/3.2.2/anime.min.js
GSAP 3.12.5      https://cdn.bootcdn.net/ajax/libs/gsap/3.12.5/gsap.min.js
Rough.js 4.6.6   https://registry.npmmirror.com/roughjs/4.6.6/files/bundled/rough.js
three.js r128    https://cdn.bootcdn.net/ajax/libs/three.js/r128/three.min.js
p5.js 1.9.4      https://cdn.bootcdn.net/ajax/libs/p5.js/1.9.4/p5.min.js
```
- **D3**：数据驱动 SVG 的瑞士军刀，自定义可视化/力导向图/地理/坐标轴。学习曲线陡，简单图别用它（用 Chart.js）。
- **SVG.js / Snap.svg**：轻量 SVG 操作库，画自定义示意图、几何图形、动画。SVG.js API 更现代。
- **anime.js / GSAP**：补间动画。给 SVG/DOM 做分步演示动画。GSAP 更强，anime.js 更轻。
- **Rough.js**：手绘风格图形，板书/草图感，亲和力强（**bootcdn 没有，走 npmmirror**）。
- **three.js / p5.js**：3D（three）、创意编程画布（p5）。仅在确需 3D 或生成艺术时引入。

### 数学公式

```
KaTeX 0.16.9 JS    https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.9/katex.min.js
KaTeX 0.16.9 CSS   https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.9/katex.min.css
KaTeX auto-render  https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js
MathJax 3.2.2      https://cdn.bootcdn.net/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js
```
- **KaTeX**：库名大小写敏感 `KaTeX`。渲染快、需配 CSS。适合大量公式即时渲染。
- **MathJax**：兼容更全（复杂 LaTeX、化学式 mhchem），单文件无需额外 CSS，但更重。常规公式用 KaTeX。

### 代码 / 文本

```
Highlight.js 11.10.0 JS   https://cdn.bootcdn.net/ajax/libs/highlight.js/11.10.0/highlight.min.js
Highlight.js 主题(暗)     https://cdn.bootcdn.net/ajax/libs/highlight.js/11.10.0/styles/github-dark.min.css
Highlight.js 主题(亮)     https://cdn.bootcdn.net/ajax/libs/highlight.js/11.10.0/styles/github.min.css
marked 12.0.2             https://cdn.bootcdn.net/ajax/libs/marked/12.0.2/marked.min.js
```
代码教学：Highlight.js 高亮 + marked 把 Markdown 转 HTML。

### 幻灯片

```
Reveal.js 5.1.0 JS    https://cdn.bootcdn.net/ajax/libs/reveal.js/5.1.0/reveal.min.js
Reveal.js 5.1.0 CSS   https://cdn.bootcdn.net/ajax/libs/reveal.js/5.1.0/reveal.min.css
Reveal 主题(白)       https://cdn.bootcdn.net/ajax/libs/reveal.js/5.1.0/theme/white.min.css
```
做课件式翻页演示时用。注意它接管全屏，与自定义布局冲突——只在明确要"幻灯片"时用。

### 图标 / 中文字体（可选润色）

```
Font Awesome 6.5.2   https://cdn.bootcdn.net/ajax/libs/font-awesome/6.5.2/css/all.min.css
霞鹜文楷 webfont      https://cdn.staticfile.net/lxgw-wenkai-screen-webfont/1.7.0/style.css
```
- Font Awesome：图标。`<i class="fa-solid fa-lightbulb"></i>`。
- 霞鹜文楷：免费开源中文楷体 webfont（`font-family: 'LXGW WenKai Screen'`），人文/语文类教学很有气质。中文字体文件大，按需用；多数情况系统字体栈足够（见 color-schemes.md）。

## 多 CDN 自动 fallback（关键稳健性技巧）

国内 CDN 偶发抽风。**对脚本类资源**加一行 fallback，主源失败自动切备源，几乎零成本提升可靠性：

```html
<script src="https://cdn.bootcdn.net/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
  window.Chart || document.write('<script src="https://cdn.staticfile.net/Chart.js/4.4.1/chart.umd.min.js"><\/script>');
</script>
```

通用写法：主源 `<script>` 后紧跟一个检测该库全局变量是否存在的 `<script>`，不存在就 `document.write` 写入备源。各库的全局变量名：

| 库 | 全局变量 | 库 | 全局变量 |
|---|---|---|---|
| Chart.js | `Chart` | D3 | `d3` |
| ECharts | `echarts` | SVG.js | `SVG` |
| Mermaid | `mermaid` | anime.js | `anime` |
| KaTeX | `katex` | GSAP | `gsap` |
| Highlight.js | `hljs` | marked | `marked` |
| Reveal.js | `Reveal` | Rough.js | `rough` |

> CSS 资源无法用此法检测；CSS 出问题样式降级但不致命，保持单一可靠源（bootcdn）即可。
> `document.write` fallback 必须放在 `<head>` 或 body 解析阶段（页面加载中），不能在 DOMContentLoaded 之后调用。

## 版本/路径易错点

- **Chart.js**：库名 `Chart.js`，文件 `chart.umd.min.js`。
- **Bootstrap**：库名 `twitter-bootstrap`，要 `bootstrap.bundle.min.js`（含 Popper）。
- **KaTeX**：库名 `KaTeX`（大小写敏感），用 0.16.9（高版本号在国内镜像可能缺）。
- **Rough.js**：bootcdn/staticfile 都没有，走 npmmirror 的 `roughjs/<版本>/files/bundled/rough.js`。
- **Tailwind**：Play CDN 固定 `cdn.tailwindcss.com/3.4.16`，别用无版本号的滚动地址。
- 升级版本前先 `curl -sI <url>` 验证该版本在目标 CDN 上存在，再写进文件。
