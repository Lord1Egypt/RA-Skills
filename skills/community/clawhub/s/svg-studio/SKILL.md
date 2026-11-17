---
name: SVG绘图工作台-智能生图
slug: svg-studio
displayName: SVG绘图工作台-智能生图
version: 1.3.0
description: |
  用「编写 SVG」的方式生成图片——让没有多模态生图能力的模型也能产出任意宽高比、任意复杂度的矢量图，并导出为 SVG / PNG / 动图(GIF/APNG/WebP/MP4)，或内嵌进 HTML。
  适用场景：用户要「生成一张图 / 画个图 / 做张配图 / 做海报 / 信息图 / 图表 / 流程图 / 架构图 / 图标 / 封面 / OG 图」，要求指定宽高比(16:9 / 1:1 / 9:16 等)或导出 PNG；也包括「做个动图 / GIF / 加载动画 / loading 动效」。
  能力：① 按指令编写复杂 SVG（图表/插画/流程图/海报）；② SVG→PNG 高清渲染(Chrome 优先，cairosvg/resvg 兜底)；③ 多帧/模板 SVG→GIF/APNG/WebP/MP4 动图；④ 任意宽高比与 DPR。
  关键词：生图、画图、SVG、矢量图、配图、海报、信息图、图表、流程图、架构图、图标、封面、OG image、转 PNG、动图、GIF、动画、loading。
description_zh: 用 SVG 生成任意宽高比/复杂度的图，支持 PNG 与动图导出
description_en: Generate images by authoring SVG; export PNG and animated GIF/APNG/WebP/MP4
disable: false
agent_created: true
---

# SVG绘图工作台-智能生图

让模型「写代码画图」：用 SVG 表达任意复杂的图形，按需渲染成 PNG / 动图，或内嵌 HTML。
**核心理念**：SVG 是纯文本，模型完全可控；**交付默认到 `.svg` 为止**——PNG/动图是「导出格式」，用户点名才做。

## 何时用

- 用户要生成/绘制一张图：海报、封面、信息图、图表、流程图、架构图、思维导图、图标、插画、示意图。
- 指定宽高比（16:9 / 1:1 / 9:16 / OG 1.91:1 ...）或要求导出 PNG。
- 要做动图 / GIF / loading 动画 / 动效演示。
- 没有多模态生图工具，或需要文字/数据 100% 精确（生图模型常画错字、错数字）。

> 需要照片级真实感、写实人物/风景时，SVG 不擅长——那种场景请用多模态生图工具。SVG 强在：矢量、精确、可编辑、文字数字零误差、无限缩放。

## 工作流总览

```
用户指令 → ① 选宽高比(viewBox) → ② 编写 SVG → ③ 存 .svg
        → ④ 用户点名要位图? render.py 转 PNG（默认跳过，到 .svg 为止）
        → ⑤ 用户要动图? 多帧/模板 SVG + animate.py 合成
        → ⑥ 自检（含肉眼检查）→ ⑦ 交付
```

## Step 1 — 选宽高比，定 viewBox

读 `references/svg-techniques.md` 的「宽高比预设」表。常用：
- 方图 `0 0 1000 1000`、16:9 `0 0 1280 720`、9:16 `0 0 720 1280`、OG `0 0 1200 630`、公众号封面 `0 0 900 383`。
- 像素清晰度不靠 viewBox，靠渲染时的 `--scale`（DPR）或 `--width`。

## Step 2 — 编写 SVG

**动手前先读 `references/svg-techniques.md`**（文档骨架、文本换行、渐变滤镜、图表数学公式、配色、塌方点）。要点速记：
- 起手：`<svg xmlns=... viewBox="0 0 W H" font-family="-apple-system,'PingFang SC',sans-serif">`
- 除非要透明，**第一件事画满背景 rect**，否则渲染位图时背景透明。
- `<text>` 不自动换行，多行用多个 `<tspan x=同值 dy=行高>`。
- 渐变/滤镜放 `<defs>`，用 `url(#id)` 引用。
- 图表把数据空间映射到像素空间（公式见参考文档）；注意 y 轴向下。
- 大数字+单位（如「50 万台」）单位用 `<tspan dx="N">` 内联，**不要嵌套 `<text>`**（Chrome headless 不渲染）；排版红线见参考文档 §10。
- 财经涨红跌绿（中国习惯），货币 `¥`。

**风格判断**：如果用户要的是「手账风 / 手绘风 / 便签风 / 小红书风 / 牛皮纸做旧 / 毛糙描边」信息图，或「干净产品/SaaS 风信息图」（圆角卡片+柔和阴影+扁平图标，如功能介绍长图），**先读 `references/handdrawn-infographic.md`**——里面有现成的纸张做旧滤镜、手绘抖动滤镜、便签卡片、胶带/荧光笔/手绘箭头等装饰配方，照抄即可稳定复刻，不用临场试错。注意：写实/拟物插画（水彩、铅笔颗粒、真实人物）SVG 做不到，该部分交给生图模型。

把 SVG 写入工作目录的 `.svg` 文件（用 Write 工具）。

## Step 3 — 渲染 PNG（仅用户要求位图时）

**默认跳过这一步：交付到 `.svg` 为止。** 用户没提 PNG/位图就别转，多产出的 PNG 是噪音。

`scripts/render.py`：Chrome headless 优先（渐变/滤镜/中文字体全保真），自动降级 resvg→cairosvg（无浏览器环境的兜底；resvg 对手绘滤镜 feTurbulence/feDisplacementMap 有损，重滤镜图务必 Chrome）。
输出尺寸自动从 viewBox 按比例推导。

```bash
PY=$HOME/.workbuddy/binaries/python/versions/3.13.12/bin/python3
# 默认 2x DPR，自动同名 .png，透明背景
$PY scripts/render.py poster.svg
# 指定输出/缩放/实底背景
$PY scripts/render.py poster.svg -o poster.png --scale 2 --bg "#0f172a"
# 强制输出宽度（高度按比例）
$PY scripts/render.py chart.svg --width 1600
# 顺带产出可嵌入的独立 HTML
$PY scripts/render.py chart.svg --html chart.html
```

参数：`--scale`(DPR,默认2) `--width/--height`(强制尺寸) `--bg`(transparent 或 #色值，**全引擎生效**：Chrome/resvg/cairosvg 都吃) `--engine`(auto/chrome/cairosvg/resvg) `--html`。

## Step 4 — 生成动图（需要动效时）

**先判断目标**：
- 只在网页/HTML 里播 → 直接写**带动画的 SVG**（SMIL `<animate>` 或内嵌 `<style>` 的 CSS `@keyframes`），无需转换，把 .svg 嵌进 HTML 即可。见 `references/animation.md`。
- 要一个**动图文件**（GIF/APNG/WebP/MP4）→ 用 `scripts/animate.py`，走「多帧 SVG → 逐帧 PNG → 合成」。

两种喂帧方式：

**A. 模板模式**（推荐，省事）：一个 SVG 里放 `__T__` 占位符（代表进度 0→1），脚本自动替换生成 N 帧。
```bash
$PY scripts/animate.py --template anim.svg --frames 30 -o out.gif --fps 15 --bg "#0f172a"
```
例：`opacity="__T__"` 做淡入；`__T__` 也可放进 `transform`、坐标、颜色插值里（自己在多处写表达式）。

**B. 帧目录模式**（精确控制每一帧）：自己写好 `frame-000.svg ... frame-029.svg`，脚本按编号排序合成。
```bash
$PY scripts/animate.py --frames-dir ./frames -o out.webp --fps 24 --loop 0
```

输出格式由扩展名决定：`.gif`(256 色,通用) `.webp`(更小更清晰) `.apng/.png`(无损含 alpha) `.mp4`(需 ffmpeg)。
参数：`--fps` `--loop`(0=无限) `--scale/--width`(帧清晰度) `--bg`(GIF 的 matte 也用它，深色底不会再出白边) `--quality`(webp)。
帧渲染**自动并行**（首帧预热、其余多进程并发），30 帧从 ~30s 提到 ~5s 量级。

## Step 5 — 验证（必做，第 5 条闭环自检）

**用户要了位图**：
```bash
file out.png        # 确认 PNG image data, W x H
```
用 **Read 工具打开图片肉眼看**：文字没截断、背景对、中文字体没变 Times、动图帧确实在动。

**默认 SVG 交付**：渲染一张**临时 PNG 只做自检**（文字塌方/字体/溢出只有渲染了才看得见），Read 肉眼确认后**不作为交付物**——交付仍然只有 `.svg`，临时 PNG 交付前清掉。用户明确说「别生成任何 PNG 文件」时，跳过渲染，改用 Read 检查 SVG 源码（文本完整性、坐标/字号是否超出 viewBox）。不满意就回 Step 2 改 SVG。

## 交付

- 静态图：**默认只交付 `.svg`**（可编辑源，到 SVG 为止）。仅当用户明确要求 PNG/位图时才把 `.png` 一起交付；自检用的临时 PNG 不算交付物。
- 动图：交付 `.gif/.webp/.mp4`。
- 用 `deliver_attachments` 交付文件；HTML 内嵌用 `preview_url` 预览。

## 环境与坑

- **跨平台支持（macOS / Windows / Linux）**：
  - 浏览器路径：自动探测 Chrome/Edge/Brave/Chromium（Mac Applications 目录 + Windows Program Files + PATH which）。
  - venv 路径：自动按平台选 `bin/python`（Unix）或 `Scripts/python.exe`（Windows）。
  - Python 候选：优先 WorkBuddy managed python，fallback 到系统 python.org 安装、Homebrew、Windows 默认路径等。
  - Windows 上 Chrome headless 的 `--no-sandbox` 和 `--disable-gpu` 均正常工作，无需额外配置；MP4 合成在无符号链接权限时自动改用文件拷贝。
- **渲染引擎依赖**：Chrome 路径自动探测（Mac/Win 常见位置）；Chrome headless 每次渲染用独立临时 profile，**不会与你正开着的 Chrome 抢锁**，也支持多帧并行渲染。没有 Chrome 时自动用 Python 引擎，顺序 resvg→cairosvg。**resvg 是自带 wheel、零系统依赖**，优先；cairosvg 需要本机装了 libcairo（`brew install cairo` / `apt install libcairo2`），没装会报 `cannot load library 'libcairo-2'`，此时自动落到 resvg。
- **引擎实测（2026-09-17 同图对比）**：Chrome 2.9s / resvg 1.5s；resvg 对渐变、中文、tspan 排版、图表、feDropShadow 全部正确，**但对 feTurbulence+feDisplacementMap 手绘滤镜位移过猛，文字糊掉不可读**——手绘/重滤镜图必须 Chrome。ImageMagick 实测连字体渲染都失败；rsvg-convert 滤镜支持残缺、Inkscape 是完整编辑器启动慢。**非浏览器路线的天花板就是 resvg，别再找"更厉害的脚本引擎"**。
- **Python 原生库的隔离 venv 在 `.venv/`（skill 目录内）**，由脚本首次运行时自动用「系统 Python」创建并装 Pillow/cairosvg。**不要用 managed python 直接 import 这些库**——managed python 的 hardened runtime 会因 Team ID 不匹配拒绝加载第三方 .so（实测报 `code signature ... different Team IDs`）。脚本已自动处理：用系统 Python 建 venv 并 re-exec，调用方无感。**Windows 无此限制**（无 Team ID 签名机制），managed python 可直接用。
- `.venv/` 不要打包进 skill 分发；它是本机运行时缓存。
- 更多坑见 `references/svg-techniques.md` 和 `svg-to-png-chrome` skill（后者是纯 Chrome 转换路线，本 skill 的渲染思路与之兼容）。

## 参考文件

- `references/svg-techniques.md` — SVG 编写手册（骨架/比例/文本/渐变/图表数学/配色/塌方点）。
- `references/handdrawn-infographic.md` — 手绘/手账/便签风 & 干净产品风信息图配方（纸张做旧滤镜、手绘抖动、便签卡片、胶带/荧光笔/箭头装饰、两档配色、塌方点）。
- `references/animation.md` — 动画两条路线（HTML 内嵌 SMIL/CSS vs 导出动图文件）与模板写法。
