# SVG 动画：两条路线

做「动图」前先分清目标，选对路线，别白费力气。

## 路线对比

| 需求 | 路线 | 产物 | 说明 |
|---|---|---|---|
| 只在网页/HTML 里播放 | **A. 动画 SVG** | 一个 .svg | 浏览器原生播放，无需转换，文件最小 |
| 要一个动图文件分享 | **B. 导出动图** | .gif/.webp/.apng/.mp4 | 多帧 SVG → 逐帧 PNG → 合成 |

GIF/PNG/JPG 等位图格式**无法表达 SMIL/CSS 动画**——动画 SVG 只能在支持的渲染器（浏览器）里动。要做成到处能发的动图文件，必须走路线 B 把动效「烘焙」成多帧。

---

## 路线 A：写带动画的 SVG（嵌 HTML 播放）

### A1. SMIL（SVG 原生动画标签，零 CSS）

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <rect width="400" height="400" fill="#0f172a"/>
  <circle cx="200" cy="200" r="40" fill="#06b6d4">
    <!-- 半径脉动 -->
    <animate attributeName="r" values="40;80;40" dur="2s" repeatCount="indefinite"/>
    <!-- 透明度呼吸 -->
    <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <!-- 旋转：animateTransform -->
  <rect x="170" y="170" width="60" height="60" fill="#6366f1">
    <animateTransform attributeName="transform" type="rotate"
      from="0 200 200" to="360 200 200" dur="3s" repeatCount="indefinite"/>
  </rect>
  <!-- 路径描边动画（线条生长）：配合 stroke-dasharray -->
  <path d="M50 350 Q200 50 350 350" fill="none" stroke="#f59e0b" stroke-width="4"
        stroke-dasharray="500" stroke-dashoffset="500">
    <animate attributeName="stroke-dashoffset" from="500" to="0" dur="2s"
             fill="freeze" repeatCount="indefinite"/>
  </path>
</svg>
```

SMIL 常用：`<animate>`(数值属性) `<animateTransform>`(平移/旋转/缩放) `<animateMotion>`(沿路径运动)。
关键属性：`attributeName` `values`(分号分隔关键帧) 或 `from/to` `dur` `repeatCount="indefinite"` `fill="freeze"`(停在末态) `begin`(延迟/链式 `begin="a.end"`).

### A2. CSS @keyframes（内嵌 `<style>`）

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <style>
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes fade { 0%,100%{opacity:.3} 50%{opacity:1} }
    .ring { transform-origin: 200px 200px; animation: spin 2s linear infinite; }
    .dot  { animation: fade 1.5s ease-in-out infinite; }
  </style>
  <rect width="400" height="400" fill="#0f172a"/>
  <circle class="ring" cx="200" cy="200" r="100" fill="none"
          stroke="#06b6d4" stroke-width="6" stroke-dasharray="120 480"/>
  <circle class="dot" cx="200" cy="200" r="20" fill="#6366f1"/>
</svg>
```

注意：CSS `transform` 的 `transform-origin` 在 SVG 里要写**用户坐标**（如 `200px 200px`），否则绕左上角转。

### 嵌入 HTML

直接把 `<svg>...</svg>` 放进 HTML body，或 `<img src="anim.svg">`（`<img>` 方式 CSS 动画仍生效，但内部脚本不执行）。用 `preview_url` 预览。

---

## 路线 B：导出动图文件（animate.py）

把动效拆成 N 帧静态 SVG，逐帧渲染 PNG，再合成 GIF/WebP/APNG/MP4。

### B1. 模板模式（推荐）

在 SVG 里用 `__T__` 当进度占位符（脚本会替换成 0→1 的浮点）。哪里要变就把 `__T__` 写进哪里：

```svg
<!-- progress-bar.svg：进度条 + 数值 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200">
  <rect width="600" height="200" fill="#0f172a"/>
  <rect x="50" y="90" width="500" height="20" rx="10" fill="#1e293b"/>
  <!-- 宽度 = 500 * __T__ ；但脚本只做字符串替换，所以预先把可计算量摊开 -->
  <rect x="50" y="90" width="__T__" height="20" rx="10" fill="#06b6d4"/>
</svg>
```

⚠️ `__T__` 是**纯字符串替换**（0..1 的小数），脚本不做数学运算。如果需要 `width = 500*t` 这类，有两种办法：
1. 直接让占位符代表最终值范围——用「帧目录模式」自己算（最灵活）。
2. 用 SVG 自身能力放大：例如把元素放进 `<g transform="scale(500,1)">`，再用 `width="__T__"`，由 transform 把 0..1 放大到 0..500。

旋转淡入等「天然 0..1 友好」的属性（`opacity`、`scale` 比例、`offset` 渐变位置）最适合模板模式。

```bash
PY=$HOME/.workbuddy/binaries/python/versions/3.13.12/bin/python3
$PY scripts/animate.py --template anim.svg --frames 30 -o out.gif --fps 15 --bg "#0f172a"
```

### B2. 帧目录模式（精确，适合复杂动画）

自己用代码/循环生成每一帧 SVG（可在 SVG 里做任意数学），命名带递增数字：

```
frames/frame-000.svg
frames/frame-001.svg
...
frames/frame-029.svg
```

```bash
$PY scripts/animate.py --frames-dir ./frames -o out.webp --fps 24 --loop 0 --scale 1
```

脚本按文件名里的数字自然排序合成。这是表达任意复杂逐帧动画的终极方式——每帧就是一张完整 SVG，想画什么画什么。

### 参数

- `--fps` 帧率（默认 12）
- `--loop` 循环次数，0=无限（默认 0）
- `--scale` / `--width` 每帧 PNG 的清晰度（动图建议 scale=1~1.5，控制体积）
- `--bg` 帧背景；**GIF 不支持半透明**，务必给实底色
- `--quality` WebP 质量（默认 90）
- 输出 `.mp4` 需本机有 `ffmpeg`

### 格式选择

| 格式 | 优点 | 缺点 | 适用 |
|---|---|---|---|
| GIF | 兼容性最强，到处能发 | 256 色、文件大、无半透明 | 表情包、简单 loading |
| WebP | 体积小、全彩、支持 alpha | 老平台不支持 | 网页、现代 IM |
| APNG | 无损、全 alpha | 体积大 | 高质量 UI 动效 |
| MP4 | 体积最小、长动画 | 不能透明、需播放器 | 长演示、录屏式 |

## 性能与坑

- 帧数 × 清晰度 = 渲染耗时。预览用 12fps×20 帧足够；正式再加。
- Chrome 并发拉起偶发 mach port 冲突，脚本已内置 3 次重试。
- 模板模式记住：`__T__` 只是替换字符串，复杂运动用帧目录模式。
- GIF 发虚/有杂边：通常是背景没给实底（用了 transparent），改 `--bg` 实色。
