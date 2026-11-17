# 手绘 / 手账 / 便签信息图风格手册

复刻「牛皮纸做旧 + 手绘抖动 + 便签卡片 + 荧光笔高亮 + 胶带贴纸」这类风格信息图（常见于小红书 / 公众号 / 团队科普长图）。
本手册是**配方表**：照着抄滤镜和版式，就能稳定出效果，不用每次现场试错。

> 这类图的灵魂是 **版面 + 信息层级 + 配色 + 装饰细节**，不是照片级真实感——正是 SVG 的强项。
> 干净产品/SaaS 风 ≈95% 还原；手账做旧风 ≈90% 还原。
> **写实/拟物插画（水彩晕染、铅笔颗粒、真实人物）做不到**——那部分交给多模态生图，SVG 负责排版和简笔元素。

---

## 0. 风格分两档，先认清目标

| 档位 | 长相 | 关键手法 |
|---|---|---|
| **A. 手账做旧风** | 牛皮纸/米黄底、撕纸边、胶带、手写感、卡片微倾斜、毛糙描边 | 纸张滤镜 + 手绘抖动 + rotate + 荧光笔 |
| **B. 干净产品风** | 白底、圆角卡片、柔和阴影、扁平图标、整齐网格 | 柔和阴影 + 规整布局 + 扁平配色（**不要**抖动滤镜） |

两档**配色和装饰策略不同**，下面分别给。先判断用户参考图是哪一档。

---

## 1. 核心滤镜配方（A 档手账风的灵魂）

全部放进 `<defs>`。这三个滤镜是「毛毛糙糙」效果的来源。

### 1.1 纸张做旧底纹（二选一）

**配方 A — 凹凸光照纸（更厚重，推荐做牛皮纸）**
```svg
<filter id="paper" x="0%" y="0%" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="5" result="noise"/>
  <feDiffuseLighting in="noise" lighting-color="#f5f0e8" surfaceScale="2">
    <feDistantLight azimuth="45" elevation="55"/>
  </feDiffuseLighting>
</filter>
<!-- 用法：单独画一个 rect 铺满，fill 无所谓（被滤镜覆盖） -->
<rect width="W" height="H" filter="url(#paper)"/>
```
- `lighting-color` 决定纸的基色：牛皮纸 `#d9c4a3`，米黄便签纸 `#f5f0e8`，旧报纸 `#ece5d3`。
- `baseFrequency` 越大颗粒越细；`surfaceScale` 越大凹凸越明显。

**配方 B — 轻噪叠加（更轻，纸色自己控制）**
```svg
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.012 0.014" numOctaves="3" seed="7" result="n"/>
  <feColorMatrix in="n" type="saturate" values="0.1"/>
  <feComponentTransfer><feFuncA type="linear" slope="0.06"/></feComponentTransfer>
  <feComposite operator="over" in2="SourceGraphic"/>
</filter>
<!-- 用法：先画实色底，再叠一层带此滤镜的同色 rect -->
<rect width="W" height="H" fill="#d9c4a3"/>
<rect width="W" height="H" fill="#d9c4a3" filter="url(#grain)"/>
```
- `slope` 控噪点强度（0.04~0.08 自然）。颗粒细腻，不抢内容。

**可叠加：方格纸网格**（手账常见）
```svg
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
  <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#e8e0d0" stroke-width="0.5" opacity="0.6"/>
</pattern>
<rect width="W" height="H" fill="url(#grid)"/>
```

### 1.2 手绘抖动（让直线/边框变「毛糙」——最关键）
```svg
<filter id="sketch" x="-3%" y="-3%" width="106%" height="106%">
  <feTurbulence type="turbulence" baseFrequency="0.05" numOctaves="2" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="2.5"
       xChannelSelector="R" yChannelSelector="G"/>
</filter>
<!-- 用法：给卡片边框、图标线条套 -->
<g filter="url(#sketch)">
  <rect x="90" y="55" width="620" height="130" rx="12"
        fill="#fff9e6" stroke="#c8a060" stroke-width="3"/>
</g>
```
- `scale` 是抖动幅度：边框 `2~3`，小图标 `2~4`。太大（>5）会糊。
- **关键坑**：filter 区域要给 `-3%/106%` 余量，否则抖出边界被裁。
- **关键坑**：被套滤镜的 `<text>` 会变模糊——**文字不要套 sketch**，只套形状/边框/图标。

### 1.3 柔和投影（卡片浮起感，A/B 档都用）
```svg
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#5b4a2e" flood-opacity="0.25"/>
</filter>
```
- A 档阴影色用暖棕 `#5b4a2e`；B 档用冷灰 `#1e293b` 或纯黑低透明。
- **必须 Chrome 引擎渲染**，cairosvg 对 feDropShadow 支持差。

---

## 2. 便签卡片（信息分区的基本单元）

每块内容 = 一张「便签纸」。要点：**整体轻微 rotate（±1~2.5°）打破死板**，顶部一条深色标题带。

```svg
<g transform="translate(65, 215) rotate(-1.5)">
  <!-- 卡片本体（可选套 sketch 让边毛糙） -->
  <rect x="0" y="0" width="310" height="185" rx="6" fill="#fff5cc" stroke="#e8c860" stroke-width="2"/>
  <!-- 顶部标题带：同宽，深色，上圆角 -->
  <rect x="0" y="0" width="310" height="38" rx="6" fill="#f4a460" opacity="0.9"/>
  <text x="155" y="28" text-anchor="middle" font-size="20" fill="#fff" font-weight="bold">💡 核心思想</text>
  <!-- 正文：逐行，行距 25~28 -->
  <text x="25" y="68" font-size="15" fill="#5d4037">第一条要点</text>
  <text x="25" y="95" font-size="15" fill="#5d4037">第二条要点</text>
</g>
```
- 倾斜角交替正负（-1.5° / +1 / -1 / +2），像随手贴上去。
- 标题带颜色 = 卡片主题色加深；正文用深棕 `#5d4037` 不用纯黑，更柔。
- 流程类卡片并排时，等宽等高 + 各自小角度旋转。

---

## 3. 装饰元素配方（点睛，缺了就「太规整不像手账」）

### 3.1 胶带（贴角）
```svg
<g transform="translate(60, 15) rotate(-8)">
  <rect width="110" height="28" rx="2" fill="#a8d8ea" opacity="0.85"/>
  <rect width="110" height="28" rx="2" fill="none" stroke="#7ab8d5" stroke-width="0.5"/>
  <!-- 几条竖线模拟胶带纹理 -->
  <line x1="10" y1="0" x2="10" y2="28" stroke="#7ab8d5" stroke-width="0.3" opacity="0.5"/>
  <line x1="55" y1="0" x2="55" y2="28" stroke="#7ab8d5" stroke-width="0.3" opacity="0.5"/>
</g>
```
半透明（0.7~0.85）才像胶带；常用蓝/粉/黄，分布在四角。

### 3.2 荧光笔高亮（压在文字下面）
```svg
<!-- 先画高亮块，再画文字（文字在上） -->
<rect x="150" y="118" width="190" height="38" fill="#ffe14d" opacity="0.75" transform="rotate(-1 245 137)"/>
<text x="450" y="152" text-anchor="middle" font-size="40" font-weight="bold">被高亮的标题</text>
```
- 半透明黄 `#ffe14d` / 粉 `#ffb3c1` / 青 `#a8e6cf`；轻微旋转更像手涂。
- 高度略大于字号，左右略宽出文字。

### 3.3 手绘下划线 / 波浪线（用抖动的 path，别用直 line）
```svg
<path d="M 180 108 Q 300 112, 400 108 Q 500 104, 620 110"
      fill="none" stroke="#c8a060" stroke-width="2.5" stroke-linecap="round"/>
```
用 `Q` 二次贝塞尔做轻微起伏，比直线有手感。虚线下划线加 `stroke-dasharray="8 4"`。

### 3.4 手绘箭头（流程连接）
```svg
<g stroke="#8b6914" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path d="M 220 545 Q 228 540, 235 545"/>      <!-- 箭杆，微弯 -->
  <path d="M 232 540 L 235 545 L 232 550"/>     <!-- 箭头 -->
</g>
```
或用 marker（见 svg-techniques.md）。手账风优先手画微弯的。

### 3.5 编号气泡
```svg
<circle cx="490" cy="372" r="13" fill="#e0533d"/>
<text x="490" y="379" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold">1</text>
```

### 3.6 简笔画图标（机器人 / 灯泡 / 放大镜 / 纸飞机）
用基本图形 + 套 `sketch` 滤镜加手感。范例（机器人头）：
```svg
<g filter="url(#sketch)">
  <rect x="0" y="14" width="48" height="40" rx="10" fill="#cfe8f2" stroke="#2b3a45" stroke-width="2.5"/>
  <circle cx="14" cy="32" r="5" fill="#2b3a45"/><circle cx="34" cy="32" r="5" fill="#2b3a45"/>
  <path d="M16 44 Q24 49 32 44" stroke="#2b3a45" stroke-width="2.5" fill="none"/>
  <line x1="24" y1="2" x2="24" y2="14" stroke="#2b3a45" stroke-width="2.5"/>
  <circle cx="24" cy="2" r="3.5" fill="#e0533d"/>
</g>
```
灯泡 = circle + 底部两横线；放大镜 = circle + 斜 line；纸飞机 = 两个 polygon。
emoji（💡🎯🔍✅⚠️📋★）也能直接当图标用，省事且渲染稳定。

---

## 4. 字体（手感来源之一）

```
font-family="'STKaiti','Kaiti SC','PingFang SC',sans-serif"          <!-- 楷体，中文手写感 -->
font-family="'Comic Sans MS','Segoe Print','PingFang SC',cursive"    <!-- 英文手写感 -->
```
- 标题楷体 + 正文黑体（PingFang）对比更清晰。
- 纯手写体全文会降低可读性，**标题/点睛用手写，正文用黑体**最稳。
- 关键文字别套 sketch 滤镜（会糊）。

---

## 5. 配色板（直接抄）

**A 档手账做旧**
- 底：牛皮纸 `#d9c4a3` / 米黄 `#f5f0e8` / 旧报 `#ece5d3`
- 卡片：`#fff9e6 #fff5cc #fbf6ea`（暖白系）
- 正文：深棕 `#5d4037`，次要 `#8b6914`
- 主题色（标题带/边框）：橙 `#f4a460` 红 `#e57373` 蓝 `#42a5f5` 绿 `#66bb6a` 粉 `#ec407a` 黄棕 `#c8a060`
- 强调红 `#c0392b` / `#e0533d`，强调绿 `#1e7d4f`

**B 档干净产品**（参考 SaaS 信息图）
- 底：白 `#ffffff` / 极浅灰 `#f7f8fa`
- 卡片：白 + 柔和阴影；分区用浅色块 `#eef2ff #ecfdf5 #fef3c7 #fee2e2`
- 文本：`#1f2937` 主 / `#6b7280` 次
- 强调：靛 `#6366f1` 青 `#06b6d4` 琥珀 `#f59e0b` 绿 `#10b981` 红 `#ef4444`
- **不加**纸张/抖动滤镜，改用规整圆角 + 等距网格 + 扁平描边图标。

---

## 6. 整体版式套路（长图信息图）

竖版长图常用 `viewBox="0 0 900 1200"`（3:4）或更长 `0 0 800 1100`。自上而下：

```
┌ 顶部胶带（贴角装饰）
├ 标题卡（大标题 + 荧光笔高亮关键词 + 手绘下划线 + 副标题）
├ 两栏并列卡（如「核心思想」｜「痛点/结论」）
├ N 栏流程卡（等宽，微旋转，手绘箭头连接）
├ 通栏「核心洞察」卡（点睛，灯泡图标 + 高亮金句）
└ 底部签名 / 胶带
```
- 留白：卡片间距 15~25px，别塞满。
- 信息密度：每卡 3~5 条要点，多了换卡。

---

## 7. 渲染与验收

```bash
PY=$HOME/.workbuddy/binaries/python/versions/3.13.12/bin/python3
$PY scripts/render.py infographic.svg --scale 2 --bg "#d9c4a3"   # bg 给纸色，别透明
```
- **必须 Chrome 引擎**（滤镜全保真）；cairosvg/resvg 对 feDiffuseLighting/feDropShadow 支持差，会丢纸张质感和阴影。
- 用 Read 工具肉眼检查：纸纹在不在、边框毛糙度对不对、文字没被滤镜糊、没截断。

---

## 8. 塌方点速查

- 文字套了 `sketch` 滤镜 → 糊成一团。**只给形状/边框/图标套，文字裸放。**
- 滤镜抖出边界被裁 → filter 给 `-3%/106%` 余量。
- 用 cairosvg/resvg 渲染 → 纸张光照、阴影丢失，变成平面色块。**指定 `--engine chrome`。**
- 卡片全部正放不旋转 → 太规整，不像手账。给 ±1~2.5° rotate。
- 用纯直 line 做下划线/箭头 → 太机械。用 Q 贝塞尔微弯。
- 牛皮纸渲染出来透明/发黑 → `--bg` 没给纸色，或忘了铺底 rect。
- 全文手写体 → 可读性差。标题手写、正文黑体。
- B 档（干净产品风）误加纸张+抖动 → 显脏。B 档保持干净。
