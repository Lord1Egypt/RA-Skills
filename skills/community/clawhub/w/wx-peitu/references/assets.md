# Assets Reference (资源参考)

> 图库、截图美化、图表系统、Layout Recipe 布局配方的统一参考文件
> 版本: 2.0 | 画布: 正文 640px · 封面 900×383

---

## 1. Image Sources (免费图库接入)

### Three Built-In Libraries

| Library | Strength | Best For | License |
|---------|----------|----------|---------|
| **Pexels** | 中文搜索，覆盖广 | 通用背景、生活、职场、美食、自然 | 免费商用，无需署名 |
| **Unsplash** | 最高画质，艺术感 | 人像、空间/建筑、抽象纹理、氛围 | 免费商用 (Unsplash License) |
| **Wallhaven** | 游戏美术、电影级 | 科幻、游戏、暗色/情绪背景 | 混合许可，需逐张检查 |

Search URLs: `pexels.com/search/{keyword}/` · `unsplash.com/s/photos/{keyword}` · `wallhaven.cc/search?q={keyword}`

### Mode-Based Priority

| Mode | Primary | Secondary | Rationale |
|------|---------|-----------|-----------|
| **Editorial Magazine** | Unsplash | Pexels | 画质匹配杂志美学 |
| **Swiss International** | Pexels | Wallhaven | Pexels 干净产品图；Wallhaven 暗色科技背景 |
| **Dark/Tech** | Wallhaven | Unsplash | 电影级暗色影像 |

### Content Type → Image Type Mapping

| Content Type | Image Role | Source | Search Keywords |
|-------------|-----------|--------|-----------------|
| Cover/Hero | 氛围 + 标题背景 | Unsplash > Pexels | `{topic} abstract`, `{topic} minimal` |
| Data chart | 无图 (CSS/SVG) | N/A | — |
| Quote card | 微妙纹理背景 | Pexels | `paper texture`, `minimal background` |
| Comparison | 证据照片 | Pexels > Unsplash | `{subject} photo`, `{product} closeup` |
| Cases card | 产品/人物照片 | Unsplash > Pexels | `{company} office`, `{person} portrait` |

### Image Quality Requirements

- **Minimum**: 1600px 宽（避免 Retina 模糊）
- **Format**: JPG 照片，PNG 透明 UI 元素
- **Size**: 单张 < 5MB
- **No watermarks**: 拒绝带水印图片
- **Crop**: 每张图设置 `object-position` 定位主体

### Search Strategy

1. 英文关键词优先（三个图库英文索引更好）
2. Pexels 可加中文关键词
3. 背景用抽象词：`minimal dark`, `abstract gradient`, `paper texture`
4. 证据照用具体词：`rocket launch`, `satellite orbit`
5. 按方向筛选：封面 landscape (21:9)，3:4 卡片 portrait，1:1 square

### User Image Priority

**用户自有图片始终优先于图库。**

- 用户提供图片 → 优先使用，仅不足时补充图库
- 无图片时问一次："需要配图吗？A.你自己有照片/截图（推荐）B.我去图库帮你找 C.纯CSS/SVG无图方案"
- 不重复追问

### Attribution

- Pexels/Unsplash：无需署名，建议图注标注
- Wallhaven：检查单张许可，需要时添加署名
- 用户图片：标注"图片来源：用户提供"

---

## 2. Screenshot Styling (截图美化)

### Device Frame Components

| Frame | Use Case | CSS Approach |
|-------|----------|-------------|
| **macOS window** | 桌面应用截图 | 顶栏红黄绿圆点 + 居中标题 + 8px圆角 |
| **iOS device** | 移动端截图 | 圆角矩形 + 灵动岛 + Home指示条 |
| **Browser chrome** | Web应用截图 | 标签栏 + 地址栏 + 书签栏 |

### Material Backgrounds (材质背景)

截图不应浮在白底上，必须放在材质背景上：

| Background | CSS | Best For |
|-----------|-----|----------|
| **格纸** | `background-image: linear-gradient(#e8e5de 1px, transparent 1px), linear-gradient(90deg, #e8e5de 1px, transparent 1px); background-size: 20px 20px;` | Editorial, 教程卡片 |
| **点阵** | `background-image: radial-gradient(circle, #d4d4d2 1px, transparent 1px); background-size: 16px 16px;` | Swiss, 科技产品 |
| **暖白** | `background: #f5f4ed;` | 两种模式，极简风格 |
| **深色** | `background: #1a1a1e;` | Swiss, 暗色主题 |

### Shadow & Radius Rules

| Mode | Shadow | Border Radius |
|------|--------|--------------|
| **Editorial** | `0 4px 24px rgba(0,0,0,0.12)` | 8px (window), 16px (device) |
| **Swiss** | `0 2px 12px rgba(0,0,0,0.08)` | 4px (window), 12px (device) |

### Screenshot Priority

1. 用户截图 → 加设备框 + 材质背景
2. 无截图 → 图库照片
3. 都没有 → 纯 CSS/SVG 布局

---

## 3. Chart System (图表系统)

纯 CSS + 内联 SVG 实现，不依赖外部库。

### Chart Type Decision Tree

```
数据关系是什么？
│
├─ 类别比较
│   ├─ 少类别 (2-6) → bar-chart
│   └─ 多类别 (7+) → horizontal-bar-chart
│
├─ 时间变化
│   ├─ 少数据点 (2-8) → bar-chart
│   ├─ 多数据点 (8+) → line-chart
│   └─ 金融/股票 → candlestick-chart
│
├─ 占比关系
│   ├─ 少分段 (2-5) → donut-chart
│   └─ 多分段 (6+) → treemap
│
├─ 相关性
│   ├─ 2变量 → scatter-plot (有阈值线用 quadrant-chart)
│   └─ 3+变量 → bubble-chart
│
├─ 流程
│   ├─ 顺序步骤 → flow-chart
│   ├─ 并行泳道 → swimlane-chart
│   └─ 状态转换 → state-machine
│
├─ 层级
│   ├─ 树结构 → tree-chart
│   ├─ 分层/嵌套 → layered-diagram
│   └─ 组织架构 → tree-chart (horizontal)
│
├─ 集合重叠
│   └─ 2-3集合 → venn-diagram
│
└─ 累积变化
    └─ 正负贡献 → waterfall-chart
```

### 14 Chart Types (精简)

| # | Type | When | Data Shape | Notes |
|---|------|------|-----------|-------|
| 1 | **bar-chart** | 2-6类别比较 | `[{label, value, color?}]` | CSS flexbox，最多8条 |
| 2 | **horizontal-bar-chart** | 7+类别或长标签 | `[{label, value, color?}]` | CSS grid行，最多15条 |
| 3 | **line-chart** | 8+时间点趋势 | `{labels, series:[{name,values,color?}]}` | SVG polyline，最多3条线 |
| 4 | **donut-chart** | 2-5段占比 | `[{label, value, color}]` | SVG stroke-dasharray，最多5段 |
| 5 | **quadrant-chart** | 2轴+阈值线 | `{xLabel, yLabel, items:[{name,x,y}]}` | SVG四象限+十字线 |
| 6 | **flow-chart** | 3-8步顺序流程 | `{steps:[{id,label,type?}], connections:[{from,to}]}` | CSS grid + SVG箭头 |
| 7 | **swimlane-chart** | 2-4角色并行流程 | `{lanes:[{name,steps}]}` | CSS grid行 + SVG跨道箭头 |
| 8 | **state-machine** | 状态转换+条件 | `{states, transitions}` | SVG圆+路径，最多6状态 |
| 9 | **tree-chart** | 层级结构 | `{root:{label,children}}` | CSS flexbox+连接线，最深3层 |
| 10 | **layered-diagram** | 分层架构 | `{layers:[{name,items,color?}]}` | CSS堆叠矩形，最多6层 |
| 11 | **venn-diagram** | 2-3集合重叠 | `{sets, overlap}` | SVG圆 + mix-blend-mode |
| 12 | **candlestick-chart** | 金融OHLC | `[{date,open,high,low,close}]` | SVG rect+line，最多30点 |
| 13 | **waterfall-chart** | 累积正负贡献 | `[{label,value,type:'positive'\|'negative'\|'total'}]` | CSS flexbox堆叠，最多10项 |
| 14 | **treemap** | 多类别层级占比 | `[{label,value,color?,children?}]` | CSS grid-area，最多12项 |

### Chart Styling Rules

- **Color**: 默认 `--color-accent-1` ~ `--color-accent-4`，单图不超4色
- **Typography**: 轴标 `--text-caption`/`--color-text-muted`；数据标 `--text-small` + `tabular-nums`；标题 `--text-h3`/`--font-display`
- **Spacing**: 内边距 `--sp-4`，图例间距 `--sp-3`，图例项间距 `--sp-2`
- **SVG**: 用 `viewBox` + `width:100%` + `height:auto`，最小宽度320px
- **A11y**: `role="img"` + `aria-label`，不纯靠颜色区分

### Auto-Selection Integration

内容解析后自动建议：
1. 数值比较 → bar-chart / horizontal-bar-chart
2. 时间序列 → line-chart
3. 占比 → donut-chart
4. 流程 → flow-chart
5. 层级 → tree-chart / layered-diagram
6. 跨角色比较 → swimlane-chart

---

## 4. Layout Recipes (布局配方系统)

24 套布局配方，分为 **Editorial (E01-E14)** 和 **Swiss (S01-S10)** 两大系列。

每套配方包含：
- **Name + ID** — 唯一标识
- **Best for** — 适用内容类型
- **Structure** — 组件分解
- **Minimum density** — 填充画布的最小内容集
- **Hard limits** — 数量/尺寸硬约束
- **HTML skeleton** — 完整可运行的 HTML 文件

### 通用规则

- 所有 HTML 文件完全自包含（内联 CSS，无外部依赖）
- Google Fonts `@import` 放在 `<style>` 顶部
- 图片用 `<img>` 标签 + `crossorigin="anonymous"`（禁止 CSS background-image）
- 颜色通过 CSS 变量引用：`var(--ink)`, `var(--paper)`, `var(--accent)` 等
- 画布固定宽高 + `overflow: hidden`
- 标题长度自适应字号规则：≤6字 56-72px / 7-14字 40-52px / 15-24字 28-36px / 25+字 22-28px

---

### E01 Cover: Magazine Issue Cover (900×383)

**Best for:** 文章封面，杂志期号风格，适合有明确主题分类和多个要点的长文

**Structure:**
- 顶部 kicker 行（分类 + 日期）
- 大号衬线标题，2-4 行
- 一张大照片占据页面 35-55%
- 底部 issue-strip，3-5 个要点

**Minimum density:** 标题 + 照片 + 3 个 issue-strip 条目

**Hard limits:** issue-strip 3-5 条；标题 ≤4 行；照片占比 35-55%

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 900px; height: 383px; }
body { width: 900px; height: 383px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.cover { display: flex; width: 900px; height: 383px; }
.cover-left { flex: 1; display: flex; flex-direction: column; padding: 32px 28px 24px 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
.date { font-size: 11px; color: var(--muted); letter-spacing: 0.05em; }
.title { font-family: var(--font-display); font-size: 42px; font-weight: 700; line-height: 1.15; margin: 16px 0 auto; }
.issue-strip { display: flex; gap: 20px; padding-top: 16px; border-top: 1px solid var(--rule); margin-top: 20px; }
.issue-item { font-size: 12px; line-height: 1.4; color: var(--ink); }
.issue-item span { display: block; font-size: 10px; color: var(--muted); margin-top: 2px; }
.cover-right { width: 380px; position: relative; overflow: hidden; flex-shrink: 0; }
.cover-right img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 30%; }
</style>
</head>
<body>
<div class="cover">
  <div class="cover-left">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span class="kicker">深度研究</span>
      <span class="date">2026年6月</span>
    </div>
    <h1 class="title">当算法开始<br/>替我们做决定</h1>
    <div class="issue-strip">
      <div class="issue-item">算法偏见<span>三个真实案例</span></div>
      <div class="issue-item">监管困局<span>全球立法竞赛</span></div>
      <div class="issue-item">人的选择<span>最后的防线</span></div>
    </div>
  </div>
  <div class="cover-right">
    <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80" crossorigin="anonymous" />
  </div>
</div>
</body>
</html>
```

---

### E02 Field Note Photo (640×auto)

**Best for:** 纪实照片配文，田野笔记，产品实拍展示

**Structure:**
- 大幅纪实照片
- 窄栏说明文字或底部说明条带
- 一行大字 takeaway

**Minimum density:** 照片 + 说明 + takeaway

**Hard limits:** 照片占垂直空间 50-70%；takeaway ≤1 行

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 0; }
.photo { width: 640px; height: 360px; position: relative; overflow: hidden; }
.photo img { width: 100%; height: 100%; object-fit: cover; object-position: center; }
.caption-band { padding: 20px 48px 8px; display: flex; gap: 24px; }
.caption { font-size: 13px; line-height: 1.5; color: var(--muted); flex: 1; }
.takeaway { padding: 12px 48px 28px; }
.takeaway-text { font-family: var(--font-display); font-size: 28px; font-weight: 700; line-height: 1.3; color: var(--ink); }
</style>
</head>
<body>
<div class="page">
  <div class="photo">
    <img src="https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&q=80" crossorigin="anonymous" />
  </div>
  <div class="caption-band">
    <p class="caption">深圳南山科技园，凌晨两点依然灯火通明的写字楼群。这里是全球硬件创新的心脏地带。</p>
  </div>
  <div class="takeaway">
    <div class="takeaway-text">真正的创新从不按时下班</div>
  </div>
</div>
</body>
</html>
```

---

### E03 Editorial Essay Split (640×auto)

**Best for:** 观点文章，社论，深度分析，左右对照式阅读

**Structure:**
- 左栏：大标题或 pull quote
- 右栏：2-3 段短文
- 两栏间细线分隔

**Minimum density:** 标题 + 3 段短文 OR 标题 + 2 段 + 底部列表

**Hard limits:** 左栏 ≤40% 宽度；右栏段落 ≤3 段

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; display: flex; gap: 32px; }
.col-left { width: 36%; flex-shrink: 0; display: flex; flex-direction: column; justify-content: flex-start; padding-top: 8px; }
.col-rule { width: 1px; background: var(--rule); flex-shrink: 0; }
.col-right { flex: 1; }
.title { font-family: var(--font-display); font-size: 32px; font-weight: 700; line-height: 1.2; margin: 0; }
.paragraph { font-size: 15px; line-height: 1.7; color: var(--ink); margin: 0 0 16px; }
.footnote { font-size: 12px; color: var(--muted); line-height: 1.5; margin-top: 8px; }
</style>
</head>
<body>
<div class="page">
  <div class="col-left">
    <h2 class="title">效率的悖论</h2>
  </div>
  <div class="col-rule"></div>
  <div class="col-right">
    <p class="paragraph">我们追求效率的每一步，都在制造新的复杂性。自动化省下的时间，被用来管理自动化本身。</p>
    <p class="paragraph">工具越智能，操作它的认知负担越重。这不是技术的问题，而是系统的必然——任何简化都在别处产生复杂。</p>
    <p class="paragraph">真正的效率不是做得更快，而是决定不做什么。</p>
    <div class="footnote">摘自《减法思维》第三章</div>
  </div>
</div>
</body>
</html>
```

---

### E04 Pull Quote / Thesis (640×640)

**Best for:** 金句，核心论点，文章中最值得传播的一句话

**Structure:**
- 顶部可选 kicker
- 大号引文横跨页面
- 底部来源/上下文行
- 底部细线

**Minimum density:** 引文 + 来源行 + kicker（此配方允许 ≤60% 画布填充，但必须有 3 个锚点：顶部 kicker、来源行、底部细线）

**Hard limits:** 引文 ≤4 行；画布 640×640

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; height: 640px; }
body { width: 640px; height: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; height: 640px; display: flex; flex-direction: column; padding: 56px 64px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: auto; }
.quote { font-family: var(--font-display); font-size: 36px; font-weight: 700; line-height: 1.4; margin: 0; flex: 1; display: flex; align-items: center; }
.source-row { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.source { font-size: 13px; color: var(--muted); }
.bottom-rule { width: 48px; height: 1px; background: var(--ink); }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">核心论点</div>
  <p class="quote">最好的界面<br/>是没有界面</p>
  <div class="source-row">
    <span class="source">— Golden Krishna，《The Best Interface Is No Interface》</span>
  </div>
  <div class="bottom-rule"></div>
</div>
</body>
</html>
```

---

### E05 Checklist / Buying Guide (640×auto)

**Best for:** 选购指南，检查清单，步骤清单，产品对比

**Structure:**
- 标题行
- 4-6 行，每行含序号、项目名、后果/说明
- 可选小照片裁切

**Minimum density:** 标题 + 4 行含后果说明

**Hard limits:** 4-6 行；超过 6 行则拆分为两页

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-family: var(--font-display); font-size: 28px; font-weight: 700; line-height: 1.2; margin: 0 0 28px; }
.checklist { display: flex; flex-direction: column; gap: 0; }
.check-row { display: flex; align-items: flex-start; gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--rule); }
.check-num { font-size: 13px; font-weight: 500; color: var(--accent); width: 24px; flex-shrink: 0; text-align: right; padding-top: 2px; }
.check-body { flex: 1; }
.check-item { font-size: 16px; font-weight: 500; line-height: 1.3; }
.check-consequence { font-size: 13px; color: var(--muted); line-height: 1.4; margin-top: 4px; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">选购指南</div>
  <h2 class="title">远程办公摄像头清单</h2>
  <div class="checklist">
    <div class="check-row">
      <span class="check-num">01</span>
      <div class="check-body">
        <div class="check-item">4K 分辨率</div>
        <div class="check-consequence">低于 1080p 在大屏会议中会明显模糊</div>
      </div>
    </div>
    <div class="check-row">
      <span class="check-num">02</span>
      <div class="check-body">
        <div class="check-item">自动对焦</div>
        <div class="check-consequence">固定焦距在移动后需要手动调整</div>
      </div>
    </div>
    <div class="check-row">
      <span class="check-num">03</span>
      <div class="check-body">
        <div class="check-item">内置降噪麦克风</div>
        <div class="check-consequence">无降噪在开放空间中回声严重</div>
      </div>
    </div>
    <div class="check-row">
      <span class="check-num">04</span>
      <div class="check-body">
        <div class="check-item">USB-C 直连</div>
        <div class="check-consequence">USB-A 适配器增加故障点</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### E06 Evidence Wall (640×auto)

**Best for:** 证据展示，案例集，多图并置对比

**Structure:**
- 2×2 或 3 列图片网格
- 每张图附短说明
- 一个大标题锚定解读

**Minimum density:** 标题 + 4 张图含说明

**Hard limits:** 4-9 张图；每张说明 ≤20 字

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.title { font-family: var(--font-display); font-size: 28px; font-weight: 700; line-height: 1.2; margin: 0 0 24px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.cell { position: relative; overflow: hidden; border-radius: 4px; }
.cell img { width: 100%; height: 180px; object-fit: cover; display: block; }
.cell-caption { padding: 8px 0; font-size: 12px; color: var(--muted); line-height: 1.4; }
</style>
</head>
<body>
<div class="page">
  <h2 class="title">四种城市通勤方式</h2>
  <div class="grid">
    <div class="cell">
      <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&q=80" crossorigin="anonymous" />
      <div class="cell-caption">地铁 · 准时但拥挤</div>
    </div>
    <div class="cell">
      <img src="https://images.unsplash.com/photo-1449965408869-ebd13bc9e5a8?w=400&q=80" crossorigin="anonymous" />
      <div class="cell-caption">骑行 · 灵活但受天气限制</div>
    </div>
    <div class="cell">
      <img src="https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=400&q=80" crossorigin="anonymous" />
      <div class="cell-caption">自驾 · 舒适但停车难</div>
    </div>
    <div class="cell">
      <img src="https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=400&q=80" crossorigin="anonymous" />
      <div class="cell-caption">步行 · 最慢但最健康</div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### E07 Closing Note / Field Ledger (640×auto)

**Best for:** 文章收尾，要点总结，行动清单，结尾寄语

**Structure:**
- 大号 takeaway 标题（≤2 行）
- 4-6 条 ledger 条目，每条含标题 + 副行
- 收尾块：pull-quote 或签名行或 CTA

**Minimum density:** 标题 + 4 条 ledger 含副行 + 收尾块

**Hard limits:** ledger 条目 4-6 条；takeaway ≤2 行

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.takeaway { font-family: var(--font-display); font-size: 32px; font-weight: 700; line-height: 1.2; margin: 0 0 28px; }
.ledger { display: flex; flex-direction: column; gap: 0; }
.ledger-row { display: flex; align-items: baseline; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--rule); }
.ledger-title { font-size: 15px; font-weight: 500; }
.ledger-sub { font-size: 13px; color: var(--muted); margin-left: auto; flex-shrink: 0; }
.closing { margin-top: 28px; padding: 20px 0 0; border-top: 2px solid var(--ink); }
.closing-quote { font-family: var(--font-display); font-size: 18px; font-style: italic; line-height: 1.5; color: var(--ink); }
.closing-sig { font-size: 12px; color: var(--muted); margin-top: 8px; }
</style>
</head>
<body>
<div class="page">
  <h2 class="takeaway">记住这四件事</h2>
  <div class="ledger">
    <div class="ledger-row">
      <span class="ledger-title">数据不是答案</span>
      <span class="ledger-sub">问题比答案重要</span>
    </div>
    <div class="ledger-row">
      <span class="ledger-title">简单永远赢</span>
      <span class="ledger-sub">复杂是脆弱的伪装</span>
    </div>
    <div class="ledger-row">
      <span class="ledger-title">先动手再完美</span>
      <span class="ledger-sub">迭代优于规划</span>
    </div>
    <div class="ledger-row">
      <span class="ledger-title">用户不关心技术</span>
      <span class="ledger-sub">只关心结果</span>
    </div>
  </div>
  <div class="closing">
    <div class="closing-quote">"完美是完成的敌人。"</div>
    <div class="closing-sig">— Voltaire</div>
  </div>
</div>
</body>
</html>
```

---

### E08 Tall Ledger (640×auto)

**Best for:** 排行榜，详细对比表，条目化信息展示

**Structure:**
- 标题行
- 4-6 个全宽行，每行 80-120px 高
- 左侧索引列，右侧标题 + 后果说明
- 可选竖向强调条

**Minimum density:** 标题 + 4 个 ledger 行

**Hard limits:** 4-6 行；行高 80-120px

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-family: var(--font-display); font-size: 28px; font-weight: 700; line-height: 1.2; margin: 0 0 24px; }
.ledger { display: flex; flex-direction: column; }
.ledger-row { display: flex; align-items: center; min-height: 90px; border-bottom: 1px solid var(--rule); gap: 20px; }
.ledger-index { width: 48px; font-family: var(--font-display); font-size: 28px; font-weight: 700; color: var(--accent); flex-shrink: 0; text-align: center; }
.ledger-body { flex: 1; padding: 12px 0; }
.ledger-name { font-size: 17px; font-weight: 500; line-height: 1.3; }
.ledger-desc { font-size: 13px; color: var(--muted); line-height: 1.4; margin-top: 4px; }
.accent-strip { width: 3px; height: 100%; background: var(--accent); flex-shrink: 0; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">排行榜</div>
  <h2 class="title">2026 最值得学的编程语言</h2>
  <div class="ledger">
    <div class="ledger-row">
      <span class="ledger-index">1</span>
      <div class="accent-strip"></div>
      <div class="ledger-body">
        <div class="ledger-name">Rust</div>
        <div class="ledger-desc">系统级安全，性能与表达力的最佳平衡</div>
      </div>
    </div>
    <div class="ledger-row">
      <span class="ledger-index">2</span>
      <div class="ledger-body">
        <div class="ledger-name">TypeScript</div>
        <div class="ledger-desc">前端标配，类型安全带来的工程红利</div>
      </div>
    </div>
    <div class="ledger-row">
      <span class="ledger-index">3</span>
      <div class="ledger-body">
        <div class="ledger-name">Go</div>
        <div class="ledger-desc">云原生基础设施的首选语言</div>
      </div>
    </div>
    <div class="ledger-row">
      <span class="ledger-index">4</span>
      <div class="ledger-body">
        <div class="ledger-name">Python</div>
        <div class="ledger-desc">AI/ML 领域无可替代的生态位</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### E09 Atmospheric Thesis (640×640)

**Best for:** 核心观点陈述，氛围感强的论点展示，文章的灵魂句

**Structure:**
- 颗粒/渐变/水洗背景铺满页面
- 一个超大论点或引文
- 1-2 条支撑注释
- 小号元数据条 + 底部细线

**Minimum density:** 论点 + 1 条注释 + 元数据条

**Hard limits:** 论点 ≤3 行；画布 640×640

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; height: 640px; }
body { width: 640px; height: 640px; font-family: var(--font-body); color: var(--ink); }
.page {
  width: 640px; height: 640px; position: relative;
  background: linear-gradient(160deg, #f5f0e8 0%, #e8e2d6 40%, #d9d0c0 100%);
  display: flex; flex-direction: column; padding: 56px 64px; box-sizing: border-box;
}
.thesis { font-family: var(--font-display); font-size: 40px; font-weight: 700; line-height: 1.25; margin: auto 0; max-width: 480px; }
.note { font-size: 14px; line-height: 1.6; color: var(--muted); margin-top: 24px; }
.meta-strip { display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 16px; border-top: 1px solid var(--rule); }
.meta { font-size: 11px; color: var(--muted); letter-spacing: 0.05em; }
</style>
</head>
<body>
<div class="page">
  <p class="thesis">复杂系统<br/>不需要复杂的设计</p>
  <p class="note">所有持久的系统都遵循同一个原则：用最少的规则产生最丰富的行为。</p>
  <div class="meta-strip">
    <span class="meta">系统思维 · 第三章</span>
    <span class="meta">03 / 24</span>
  </div>
</div>
</body>
</html>
```

---

### E10 Evidence Feature (640×auto)

**Best for:** 产品截图展示，功能演示，证据型内容

**Structure:**
- 大截图/照片占垂直画布 45-65%
- 标题和导语在上方或侧方
- 底部说明条带含 2-3 条 takeaway

**Minimum density:** 标题 + 照片 + 2 条 takeaway 说明

**Hard limits:** 照片占比 45-65%；takeaway 2-3 条

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 40px 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-family: var(--font-display); font-size: 24px; font-weight: 700; line-height: 1.2; margin: 0 0 6px; }
.lead { font-size: 14px; color: var(--muted); line-height: 1.5; margin: 0 0 20px; }
.screenshot { width: 544px; height: 320px; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.12); margin: 0 auto 20px; }
.screenshot img { width: 100%; height: 100%; object-fit: cover; }
.caption-band { display: flex; gap: 24px; padding-top: 16px; border-top: 1px solid var(--rule); }
.caption-item { flex: 1; }
.caption-label { font-size: 12px; font-weight: 500; color: var(--accent); margin-bottom: 4px; }
.caption-text { font-size: 13px; color: var(--muted); line-height: 1.4; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">产品观察</div>
  <h2 class="title">新版编辑器的三个突破</h2>
  <p class="lead">我们花了两周时间深度体验了最新版本。</p>
  <div class="screenshot">
    <img src="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&q=80" crossorigin="anonymous" />
  </div>
  <div class="caption-band">
    <div class="caption-item">
      <div class="caption-label">实时协作</div>
      <div class="caption-text">多人同时编辑零延迟</div>
    </div>
    <div class="caption-item">
      <div class="caption-label">AI 补全</div>
      <div class="caption-text">上下文感知的代码建议</div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### E11 Marginalia Essay (640×auto)

**Best for:** 长文配注，学术风格，正文+旁注双栏阅读

**Structure:**
- 宽编辑标题
- 主栏 2-3 段
- 窄旁注栏含关键词、引文碎片
- 两栏间竖向细线

**Minimum density:** 标题 + 2 段 + 3 条旁注

**Hard limits:** 主栏占 68-72%；旁注栏 ≤3 条

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.title { font-family: var(--font-display); font-size: 28px; font-weight: 700; line-height: 1.2; margin: 0 0 24px; }
.columns { display: flex; gap: 24px; }
.col-main { flex: 1; max-width: 70%; }
.col-margin { width: 1px; background: var(--rule); flex-shrink: 0; }
.col-side { width: 26%; flex-shrink: 0; padding-top: 4px; }
.paragraph { font-size: 15px; line-height: 1.7; margin: 0 0 16px; }
.margin-item { font-size: 12px; color: var(--muted); line-height: 1.5; margin-bottom: 16px; padding-left: 8px; border-left: 2px solid var(--accent); }
</style>
</head>
<body>
<div class="page">
  <h2 class="title">知识的边界</h2>
  <div class="columns">
    <div class="col-main">
      <p class="paragraph">我们总以为知识是累积的——每一代人都站在前人的肩膀上。但真正的知识进步往往来自推翻，而非堆叠。</p>
      <p class="paragraph">范式转移不是知识的增加，而是看世界方式的根本改变。旧框架不是被补充，而是被替代。</p>
    </div>
    <div class="col-margin"></div>
    <div class="col-side">
      <div class="margin-item">范式转移</div>
      <div class="margin-item">库恩 · 1962</div>
      <div class="margin-item">"看见不同于看"</div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### E12 Section Divider (640×200)

**Best for:** 文章章节分隔，节奏调节，视觉呼吸

**Structure:**
- 一个 kicker 如"第二幕"
- 一个大号衬线章节名（3-6 字）
- 一行短副标题
- 可选底部 issue-strip

**Minimum density:** kicker + 章节名

**Hard limits:** 画布 640×200；章节名 3-6 字

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; height: 200px; }
body { width: 640px; height: 200px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: var(--accent); margin-bottom: 12px; }
.section-name { font-family: var(--font-display); font-size: 56px; font-weight: 700; line-height: 1; }
.subtitle { font-size: 14px; color: var(--muted); margin-top: 12px; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">Act II</div>
  <div class="section-name">实践</div>
  <div class="subtitle">从理论到产品的三步跨越</div>
</div>
</body>
</html>
```

---

### E13 Hero Question (640×640)

**Best for:** 开篇提问，引发思考的问题展示，文章引子

**Structure:**
- 颗粒/渐变背景
- 安静的 kicker
- 大号衬线问句，2-3 行
- 一行短提示
- 底部元数据条

**Minimum density:** kicker + 问句 + 提示 + 元数据条

**Hard limits:** 问句 ≤3 行；画布 640×640

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; height: 640px; }
body { width: 640px; height: 640px; font-family: var(--font-body); color: var(--ink); }
.page {
  width: 640px; height: 640px; position: relative;
  background: linear-gradient(180deg, #e8e5de 0%, #d4cfc4 100%);
  display: flex; flex-direction: column; padding: 56px 64px; box-sizing: border-box;
}
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); }
.question { font-family: var(--font-display); font-size: 44px; font-weight: 700; line-height: 1.25; margin: auto 0; max-width: 480px; }
.prompt { font-size: 15px; color: var(--muted); margin-top: 16px; }
.meta-strip { display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 16px; border-top: 1px solid var(--rule); }
.meta { font-size: 11px; color: var(--muted); letter-spacing: 0.05em; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">开篇</div>
  <p class="question">如果 AI 能写代码，<br/>程序员还剩什么？</p>
  <p class="prompt">思考三分钟再往下读</p>
  <div class="meta-strip">
    <span class="meta">AI 与创造力</span>
    <span class="meta">01 / 12</span>
  </div>
</div>
</body>
</html>
```

---

### E14 Vertical Pipeline (640×auto)

**Best for:** 流程步骤，方法论展示，线性过程说明

**Structure:**
- Kicker + 页面标题
- 3-5 个步骤行：步骤号（等宽）、步骤标题（衬线）、一行描述（无衬线）
- 步骤间细线，24-28px 间距

**Minimum density:** 标题 + 3 个步骤

**Hard limits:** 3-5 步；6+ 步则拆分为两页或改用 E05

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
:root {
  --ink: #1a1a1a;
  --paper: #FAFAF8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', monospace;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-family: var(--font-display); font-size: 28px; font-weight: 700; line-height: 1.2; margin: 0 0 28px; }
.pipeline { display: flex; flex-direction: column; }
.step { display: flex; align-items: flex-start; gap: 16px; padding: 16px 0; }
.step + .step { border-top: 1px solid var(--rule); }
.step-num { font-family: var(--font-mono); font-size: 14px; font-weight: 500; color: var(--accent); width: 32px; flex-shrink: 0; padding-top: 3px; }
.step-title { font-family: var(--font-display); font-size: 18px; font-weight: 700; line-height: 1.3; }
.step-desc { font-size: 13px; color: var(--muted); line-height: 1.4; margin-top: 4px; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">方法论</div>
  <h2 class="title">设计冲刺五步法</h2>
  <div class="pipeline">
    <div class="step">
      <span class="step-num">01</span>
      <div>
        <div class="step-title">理解</div>
        <div class="step-desc">用一天时间对齐团队对问题的认知</div>
      </div>
    </div>
    <div class="step">
      <span class="step-num">02</span>
      <div>
        <div class="step-title">定义</div>
        <div class="step-desc">选择一个焦点问题和一个目标用户</div>
      </div>
    </div>
    <div class="step">
      <span class="step-num">03</span>
      <div>
        <div class="step-title">发散</div>
        <div class="step-desc">每个人独立画出解决方案草图</div>
      </div>
    </div>
    <div class="step">
      <span class="step-num">04</span>
      <div>
        <div class="step-title">决定</div>
        <div class="step-desc">投票选出最有潜力的方案</div>
      </div>
    </div>
    <div class="step">
      <span class="step-num">05</span>
      <div>
        <div class="step-title">验证</div>
        <div class="step-desc">用原型测试真实用户的反应</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### S01 Cover: Swiss Hero (900×383)

**Best for:** 瑞士风格封面，全出血照片背景，大字标题叠加

**Structure:**
- 全出血照片背景
- 大号无衬线标题，weight 200-300
- 一个强调色 kicker
- 底部元数据条

**Minimum density:** 标题 + kicker + 元数据条

**Hard limits:** 标题 weight 200-300；画布 900×383

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 900px; height: 383px; }
body { width: 900px; height: 383px; font-family: var(--font-body); }
.cover { position: relative; width: 900px; height: 383px; overflow: hidden; }
.cover img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 30%; }
.cover-gradient { position: absolute; inset: 0; background: linear-gradient(to top, rgba(0,0,0,0.6), transparent 55%); }
.cover-content { position: relative; z-index: 2; padding: 32px 48px; display: flex; flex-direction: column; justify-content: flex-end; height: 100%; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 12px; }
.title { font-size: 52px; font-weight: 200; line-height: 1.1; color: #ffffff; margin: 0; }
.meta-strip { display: flex; gap: 20px; margin-top: 16px; }
.meta { font-size: 11px; color: rgba(255,255,255,0.6); letter-spacing: 0.05em; }
</style>
</head>
<body>
<div class="cover">
  <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&q=80" crossorigin="anonymous" />
  <div class="cover-gradient"></div>
  <div class="cover-content">
    <div class="kicker">年度专题</div>
    <h1 class="title">数据的形状</h1>
    <div class="meta-strip">
      <span class="meta">2026.06</span>
      <span class="meta">Vol.03</span>
      <span class="meta">深度报道</span>
    </div>
  </div>
</div>
</body>
</html>
```

---

### S02 Data Billboard (640×auto)

**Best for:** 单一数据高亮，关键指标展示，数字冲击力

**Structure:**
- 一个超大数字（`.num-mega`，40-48px，weight 200）
- 支撑标签和上下文
- 可选 2-3 个支撑统计在 `.card-fill` 网格中

**Minimum density:** 超大数字 + 标签 + 1 个支撑统计

**Hard limits:** 超大数字 ≤8 字符；支撑统计 2-3 个

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.num-mega { font-size: 48px; font-weight: 200; line-height: 1; color: var(--ink); margin: 0; }
.num-label { font-size: 14px; font-weight: 500; color: var(--accent); margin-top: 8px; letter-spacing: 0.05em; }
.num-context { font-size: 13px; color: var(--muted); line-height: 1.5; margin-top: 6px; max-width: 360px; }
.card-fill-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-top: 24px; }
.card-fill { background: var(--ink); color: var(--paper); padding: 16px; border-radius: 4px; }
.card-fill .num { font-size: 24px; font-weight: 200; }
.card-fill .label { font-size: 11px; color: rgba(255,255,255,0.6); margin-top: 4px; }
</style>
</head>
<body>
<div class="page">
  <p class="num-mega">2.4 亿</p>
  <div class="num-label">中国灵活就业人口</div>
  <p class="num-context">占全国就业人口的近三分之一，且仍在以每年 12% 的速度增长。</p>
  <div class="card-fill-grid">
    <div class="card-fill">
      <div class="num">+12%</div>
      <div class="label">年增长率</div>
    </div>
    <div class="card-fill">
      <div class="num">68%</div>
      <div class="label">90后占比</div>
    </div>
    <div class="card-fill">
      <div class="num">3.2万</div>
      <div class="label">年均收入</div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### S03 Feature Matrix (640×auto)

**Best for:** 功能对比，特性矩阵，多维度评估

**Structure:**
- Kicker + 标题
- 2×2 或 2×3 的 `.card-fill` 单元格网格
- 每个单元格：图标/数字 + 标题 + 一行描述

**Minimum density:** 标题 + 4 个单元格

**Hard limits:** 4-6 个单元格；8+ 则改用 S04 H-Bar Chart

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-size: 28px; font-weight: 400; line-height: 1.2; margin: 0 0 24px; }
.matrix { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.card-fill { background: var(--ink); color: var(--paper); padding: 20px; border-radius: 4px; }
.card-fill .num { font-size: 28px; font-weight: 200; color: var(--accent); }
.card-fill .card-title { font-size: 15px; font-weight: 500; margin-top: 8px; }
.card-fill .card-desc { font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 4px; line-height: 1.4; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">能力矩阵</div>
  <h2 class="title">四大核心能力</h2>
  <div class="matrix">
    <div class="card-fill">
      <div class="num">01</div>
      <div class="card-title">感知</div>
      <div class="card-desc">实时数据采集与环境理解</div>
    </div>
    <div class="card-fill">
      <div class="num">02</div>
      <div class="card-title">推理</div>
      <div class="card-desc">基于规则的逻辑决策引擎</div>
    </div>
    <div class="card-fill">
      <div class="num">03</div>
      <div class="card-title">学习</div>
      <div class="card-desc">从反馈中持续优化策略</div>
    </div>
    <div class="card-fill">
      <div class="num">04</div>
      <div class="card-title">行动</div>
      <div class="card-desc">毫秒级响应的执行系统</div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### S04 H-Bar Chart (640×auto)

**Best for:** 横向柱状图，多类别排名，数据比较

**Structure:**
- Kicker + 标题
- 4-8 条横向柱，含标签和数值
- 一条强调色柱高亮

**Minimum density:** 标题 + 4 条柱

**Hard limits:** 4-8 条柱；最多 15 条

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-size: 28px; font-weight: 400; line-height: 1.2; margin: 0 0 24px; }
.chart { display: flex; flex-direction: column; gap: 10px; }
.bar-row { display: flex; align-items: center; gap: 12px; }
.bar-label { width: 80px; font-size: 13px; font-weight: 400; text-align: right; flex-shrink: 0; }
.bar-track { flex: 1; height: 28px; background: var(--rule); border-radius: 2px; position: relative; }
.bar-fill { height: 100%; border-radius: 2px; background: var(--ink); display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; }
.bar-fill.accent { background: var(--accent); }
.bar-value { font-size: 12px; font-weight: 500; color: var(--paper); }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">市场数据</div>
  <h2 class="title">编程语言流行度</h2>
  <div class="chart">
    <div class="bar-row">
      <span class="bar-label">Python</span>
      <div class="bar-track"><div class="bar-fill accent" style="width:88%"><span class="bar-value">88%</span></div></div>
    </div>
    <div class="bar-row">
      <span class="bar-label">JavaScript</span>
      <div class="bar-track"><div class="bar-fill" style="width:76%"><span class="bar-value">76%</span></div></div>
    </div>
    <div class="bar-row">
      <span class="bar-label">TypeScript</span>
      <div class="bar-track"><div class="bar-fill" style="width:62%"><span class="bar-value">62%</span></div></div>
    </div>
    <div class="bar-row">
      <span class="bar-label">Rust</span>
      <div class="bar-track"><div class="bar-fill" style="width:41%"><span class="bar-value">41%</span></div></div>
    </div>
    <div class="bar-row">
      <span class="bar-label">Go</span>
      <div class="bar-track"><div class="bar-fill" style="width:38%"><span class="bar-value">38%</span></div></div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### S05 Before/After (640×auto)

**Best for:** 改造前后对比，优化效果展示，转型故事

**Structure:**
- Kicker + 标题
- 两个 `.ba-block` 行堆叠：before（dimmed .68 opacity）和 after
- 每个块：kicker + 中号标题 + 3-4 条短 bullet

**Minimum density:** 标题 + 2 个块各含 3 条 bullet

**Hard limits:** 2 个块；每块 3-4 条 bullet

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-size: 28px; font-weight: 400; line-height: 1.2; margin: 0 0 24px; }
.ba-block { padding: 20px 24px; border-radius: 4px; margin-bottom: 12px; }
.ba-before { background: var(--rule); opacity: 0.68; }
.ba-after { background: var(--ink); color: var(--paper); }
.ba-kicker { font-size: 10px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 8px; }
.ba-before .ba-kicker { color: var(--muted); }
.ba-after .ba-kicker { color: var(--accent); }
.ba-title { font-size: 17px; font-weight: 500; margin-bottom: 10px; }
.ba-after .ba-title { color: #ffffff; }
.ba-list { list-style: none; padding: 0; margin: 0; }
.ba-list li { font-size: 13px; line-height: 1.5; padding: 3px 0; }
.ba-list li::before { content: '·'; margin-right: 8px; }
.ba-before .ba-list li { color: var(--muted); }
.ba-after .ba-list li { color: rgba(255,255,255,0.8); }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">转型案例</div>
  <h2 class="title">从瀑布到敏捷</h2>
  <div class="ba-block ba-before">
    <div class="ba-kicker">Before</div>
    <div class="ba-title">季度发布，反馈滞后</div>
    <ul class="ba-list">
      <li>需求冻结后无法调整</li>
      <li>测试集中在最后两周</li>
      <li>上线即发现重大缺陷</li>
    </ul>
  </div>
  <div class="ba-block ba-after">
    <div class="ba-kicker">After</div>
    <div class="ba-title">双周迭代，持续交付</div>
    <ul class="ba-list">
      <li>每两周可验证的增量</li>
      <li>自动化测试覆盖 85%</li>
      <li>缺陷发现时间缩短 70%</li>
    </ul>
  </div>
</div>
</body>
</html>
```

---

### S06 Stat Tower (640×auto)

**Best for:** 多指标展示，关键数据堆叠，统计摘要

**Structure:**
- Kicker + 标题
- 3-4 个堆叠统计行，每行含 `.num-xl` + 标签 + 描述
- 一行使用 `.card-accent` 高亮

**Minimum density:** 标题 + 3 个统计行

**Hard limits:** 3-4 个统计行

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-size: 28px; font-weight: 400; line-height: 1.2; margin: 0 0 24px; }
.stat-tower { display: flex; flex-direction: column; gap: 0; }
.stat-row { display: flex; align-items: baseline; gap: 16px; padding: 16px 0; border-bottom: 1px solid var(--rule); }
.stat-row.card-accent { background: var(--accent); color: #ffffff; padding: 16px 20px; border-radius: 4px; border-bottom: none; margin: 4px -20px; }
.num-xl { font-size: 32px; font-weight: 200; line-height: 1; flex-shrink: 0; min-width: 100px; }
.stat-row.card-accent .num-xl { color: #ffffff; }
.stat-label { font-size: 14px; font-weight: 500; }
.stat-desc { font-size: 12px; color: var(--muted); margin-top: 2px; }
.stat-row.card-accent .stat-label { color: #ffffff; }
.stat-row.card-accent .stat-desc { color: rgba(255,255,255,0.7); }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">年度数据</div>
  <h2 class="title">平台增长指标</h2>
  <div class="stat-tower">
    <div class="stat-row">
      <span class="num-xl">1.2M</span>
      <div>
        <div class="stat-label">月活用户</div>
        <div class="stat-desc">同比增长 340%</div>
      </div>
    </div>
    <div class="stat-row card-accent">
      <span class="num-xl">94%</span>
      <div>
        <div class="stat-label">7日留存率</div>
        <div class="stat-desc">行业平均 62%</div>
      </div>
    </div>
    <div class="stat-row">
      <span class="num-xl">8.6</span>
      <div>
        <div class="stat-label">NPS 评分</div>
        <div class="stat-desc">用户推荐意愿极强</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### S07 Image Hero (640×auto)

**Best for:** 产品展示，视觉主导内容，照片+文字组合

**Structure:**
- 大照片在 `.r-16x9` 或 `.r-3x2` 比例框中
- 标题和导语在上方
- 底部说明条带

**Minimum density:** 标题 + 照片 + 说明

**Hard limits:** 照片比例 16:9 或 3:2

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-size: 28px; font-weight: 400; line-height: 1.2; margin: 0 0 6px; }
.lead { font-size: 14px; color: var(--muted); line-height: 1.5; margin: 0 0 20px; }
.r-3x2 { width: 544px; aspect-ratio: 3/2; border-radius: 4px; overflow: hidden; margin: 0 auto; }
.r-3x2 img { width: 100%; height: 100%; object-fit: cover; }
.caption { font-size: 12px; color: var(--muted); margin-top: 12px; text-align: center; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">产品</div>
  <h2 class="title">新一代工作站</h2>
  <p class="lead">为创意工作者打造的沉浸式体验</p>
  <div class="r-3x2">
    <img src="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80" crossorigin="anonymous" />
  </div>
  <div class="caption">M4 芯片驱动 · 统一内存架构 · 全天续航</div>
</div>
</body>
</html>
```

---

### S08 Quote Card (640×640)

**Best for:** 瑞士风格金句，深色背景引言，极简引文

**Structure:**
- 纯 `var(--ink)` 背景
- 大号无衬线引文，weight 200-300
- 等宽字体署名

**Minimum density:** 引文 + 署名

**Hard limits:** 引文 weight 200-300；画布 640×640

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', monospace;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; height: 640px; }
body { width: 640px; height: 640px; font-family: var(--font-body); background: var(--ink); color: var(--paper); }
.page { width: 640px; height: 640px; display: flex; flex-direction: column; justify-content: center; padding: 64px 72px; box-sizing: border-box; }
.quote { font-size: 36px; font-weight: 200; line-height: 1.4; margin: 0; max-width: 480px; }
.attribution { font-family: var(--font-mono); font-size: 13px; color: var(--accent); margin-top: 32px; letter-spacing: 0.02em; }
</style>
</head>
<body>
<div class="page">
  <p class="quote">少即是多，<br/>但少必须精。</p>
  <div class="attribution">— Mies van der Rohe</div>
</div>
</body>
</html>
```

---

### S09 Pipeline (640×auto)

**Best for:** 瑞士风格流程，步骤说明，线性过程

**Structure:**
- Kicker + 标题
- 3-5 个步骤行：步骤号、步骤标题（无衬线）、描述（无衬线）
- 步骤间细线

**Minimum density:** 标题 + 3 个步骤

**Hard limits:** 3-5 步

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-size: 28px; font-weight: 400; line-height: 1.2; margin: 0 0 24px; }
.pipeline { display: flex; flex-direction: column; }
.step { display: flex; align-items: flex-start; gap: 16px; padding: 14px 0; }
.step + .step { border-top: 1px solid var(--rule); }
.step-num { font-size: 13px; font-weight: 500; color: var(--accent); width: 28px; flex-shrink: 0; padding-top: 2px; }
.step-title { font-size: 16px; font-weight: 500; line-height: 1.3; }
.step-desc { font-size: 13px; color: var(--muted); line-height: 1.4; margin-top: 4px; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">工作流</div>
  <h2 class="title">持续部署四步法</h2>
  <div class="pipeline">
    <div class="step">
      <span class="step-num">01</span>
      <div>
        <div class="step-title">提交代码</div>
        <div class="step-desc">Push 触发 CI 流水线</div>
      </div>
    </div>
    <div class="step">
      <span class="step-num">02</span>
      <div>
        <div class="step-title">自动测试</div>
        <div class="step-desc">单元测试 + 集成测试 + E2E</div>
      </div>
    </div>
    <div class="step">
      <span class="step-num">03</span>
      <div>
        <div class="step-title">灰度发布</div>
        <div class="step-desc">5% → 25% → 100% 逐步放量</div>
      </div>
    </div>
    <div class="step">
      <span class="step-num">04</span>
      <div>
        <div class="step-title">监控验证</div>
        <div class="step-desc">错误率 + 延迟 + 业务指标</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```

---

### S10 Closing Summary (640×auto)

**Best for:** 文章收尾总结，要点回顾，行动号召

**Structure:**
- Kicker + 标题
- 3-5 条关键 takeaway 行在 `.card-fill` 中
- 底部一条 `.card-accent` CTA 行

**Minimum density:** 标题 + 3 条 takeaway 行 + CTA

**Hard limits:** takeaway 3-5 条；CTA 1 条

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --font-body: 'Noto Sans SC', sans-serif;
}
html, body { margin: 0; padding: 0; overflow: hidden; }
html { width: 640px; }
body { width: 640px; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
.page { width: 640px; padding: 48px; box-sizing: border-box; }
.kicker { font-size: 11px; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.title { font-size: 28px; font-weight: 400; line-height: 1.2; margin: 0 0 24px; }
.summary { display: flex; flex-direction: column; gap: 8px; }
.card-fill { background: var(--ink); color: var(--paper); padding: 16px 20px; border-radius: 4px; display: flex; align-items: center; gap: 12px; }
.card-fill .num { font-size: 18px; font-weight: 200; color: var(--accent); flex-shrink: 0; }
.card-fill .text { font-size: 14px; font-weight: 400; }
.card-accent { background: var(--accent); color: #ffffff; padding: 20px 24px; border-radius: 4px; margin-top: 12px; text-align: center; }
.card-accent .cta-text { font-size: 18px; font-weight: 300; }
.card-accent .cta-sub { font-size: 12px; color: rgba(255,255,255,0.7); margin-top: 4px; }
</style>
</head>
<body>
<div class="page">
  <div class="kicker">要点回顾</div>
  <h2 class="title">记住这三件事</h2>
  <div class="summary">
    <div class="card-fill">
      <span class="num">01</span>
      <span class="text">数据驱动不是数据替代决策</span>
    </div>
    <div class="card-fill">
      <span class="num">02</span>
      <span class="text">简单方案先跑起来再迭代</span>
    </div>
    <div class="card-fill">
      <span class="num">03</span>
      <span class="text">用户反馈比假设更可靠</span>
    </div>
  </div>
  <div class="card-accent">
    <div class="cta-text">开始你的第一次实验</div>
    <div class="cta-sub">关注公众号回复「实验」获取模板</div>
  </div>
</div>
</body>
</html>
```

---

## 5. Cover Title Placement Modes (封面标题放置模式)

当封面/封底使用照片背景时，根据照片主体位置选择标题放置模式。

### 四种放置模式

| Mode | 主体位置 | 标题位置 | 适用场景 |
|------|---------|---------|---------|
| **A · 顶压底沉** | 主体在中段，上下留白 | 顶：kicker 0-12% y；底：标题 72-92% y | 大多数照片的默认选择 |
| **B · 侧栏立柱** | 主体占据一侧纵列，对侧干净 | 对侧列（约 36-40% 宽）：kicker → 标题 → 副标题 | 照片有明确纵向分割 |
| **C · 角落徽章** | 主体充满大部分画面，一角空白 | 空角小块（≤35% w × ≤25% h） | 只有一个角落可用 |
| **D · 下沉条带** | 宽幅风景，底部大量负空间 | 底部条带 78-92% y：标题 + 元数据条，左对齐 | 风景/氛围照片 |

### Mode A · 顶压底沉 — HTML 示例

```html
<div style="position:relative;width:900px;height:383px;overflow:hidden">
  <img src="PHOTO_URL" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" crossorigin="anonymous" />
  <div style="position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,0.65),transparent 55%)"></div>
  <!-- 顶部 kicker -->
  <div style="position:absolute;top:0;left:48px;right:48px;padding-top:28px;z-index:2">
    <span style="font-size:11px;font-weight:500;letter-spacing:0.15em;text-transform:uppercase;color:#002FA7">深度研究</span>
  </div>
  <!-- 底部标题 -->
  <div style="position:absolute;bottom:0;left:48px;right:48px;padding-bottom:32px;z-index:2">
    <h1 style="font-size:48px;font-weight:700;color:#fff;line-height:1.15;margin:0">标题文字</h1>
    <div style="display:flex;gap:20px;margin-top:12px">
      <span style="font-size:11px;color:rgba(255,255,255,0.6)">2026.06</span>
      <span style="font-size:11px;color:rgba(255,255,255,0.6)">Vol.03</span>
    </div>
  </div>
</div>
```

### Mode B · 侧栏立柱 — HTML 示例

```html
<div style="position:relative;width:900px;height:383px;overflow:hidden">
  <img src="PHOTO_URL" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:right center" crossorigin="anonymous" />
  <div style="position:absolute;left:0;top:0;width:40%;height:100%;background:linear-gradient(to right,rgba(0,0,0,0.7),transparent)"></div>
  <!-- 左侧标题列 -->
  <div style="position:absolute;left:48px;top:50%;transform:translateY(-50%);width:300px;z-index:2">
    <span style="font-size:11px;font-weight:500;letter-spacing:0.15em;text-transform:uppercase;color:#002FA7">年度专题</span>
    <h1 style="font-size:40px;font-weight:700;color:#fff;line-height:1.15;margin:12px 0 8px">标题文字</h1>
    <p style="font-size:14px;color:rgba(255,255,255,0.7);line-height:1.5">副标题说明</p>
  </div>
</div>
```

### Mode C · 角落徽章 — HTML 示例

```html
<div style="position:relative;width:900px;height:383px;overflow:hidden">
  <img src="PHOTO_URL" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" crossorigin="anonymous" />
  <!-- 右上角徽章 -->
  <div style="position:absolute;top:24px;right:32px;width:280px;padding:20px;background:rgba(0,0,0,0.75);border-radius:4px;z-index:2">
    <span style="font-size:10px;font-weight:500;letter-spacing:0.15em;text-transform:uppercase;color:#002FA7">专题</span>
    <h1 style="font-size:24px;font-weight:700;color:#fff;line-height:1.2;margin:8px 0 4px">标题文字</h1>
    <p style="font-size:12px;color:rgba(255,255,255,0.6)">副标题</p>
  </div>
</div>
```

### Mode D · 下沉条带 — HTML 示例

```html
<div style="position:relative;width:900px;height:383px;overflow:hidden">
  <img src="PHOTO_URL" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 30%" crossorigin="anonymous" />
  <div style="position:absolute;bottom:0;left:0;right:0;height:22%;background:rgba(0,0,0,0.7);z-index:1"></div>
  <!-- 底部条带内容 -->
  <div style="position:absolute;bottom:0;left:48px;right:48px;padding-bottom:24px;z-index:2;display:flex;align-items:flex-end;justify-content:space-between">
    <div>
      <h1 style="font-size:36px;font-weight:700;color:#fff;line-height:1.15;margin:0">标题文字</h1>
      <div style="display:flex;gap:16px;margin-top:8px">
        <span style="font-size:11px;color:rgba(255,255,255,0.6)">2026.06</span>
        <span style="font-size:11px;color:rgba(255,255,255,0.6)">深度报道</span>
      </div>
    </div>
  </div>
</div>
```

### 照片资格门控

选择放置模式前，照片必须通过以下测试：

1. **安静区测试**：照片必须有 ≥30% 画布面积的低细节/均匀区域用于标题放置
2. **光线测试**：照片必须具有氛围感/克制光线（阴天、黎明、黄金时刻、黄昏）。拒绝高饱和度正午照片。
3. **两项均未通过** → 使用 E01/S01 分栏布局替代全出血照片

---

## 6. Background Image Compatibility (背景图兼容性规则)

Puppeteer 截图必须用 `<img>` 标签，**禁止** CSS `background-image`。

**正确模式**：
```html
<div style="position:relative;width:900px;height:383px;overflow:hidden">
  <img src="https://images.unsplash.com/photo-xxx?w=1200&q=80"
       style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"
       crossorigin="anonymous" />
  <div style="position:absolute;inset:0;background:linear-gradient(to top, rgba(0,0,0,0.6), transparent 60%)"></div>
  <div style="position:relative;z-index:2;padding:40px">
    <!-- 文字内容 -->
  </div>
</div>
```

**错误模式**（截图可能白屏）：
```html
<div style="background-image:url('https://images.unsplash.com/...');background-size:cover">
  Content
</div>
```

**关键规则**：
- 外部图片 `<img>` 必须加 `crossorigin="anonymous"`
- 容器设固定 `width` 和 `height`（不用 auto）
- 用 `object-fit:cover` + `object-position` 对齐主体
- 渐变遮罩层用独立 `<div>`，夹在图片和文字之间

---

## 7. Adaptive Typography (自适应字号)

### 标题长度→字号映射

| 标题长度 | 中文字数 | 尺寸 (640px画布) | Weight | 行限制 |
|---------|---------|-----------------|--------|-------|
| Short | ≤6 | 56-72px | 200-400 | 1行 |
| Medium | 7-14 | 40-52px | 300-500 | 1-2行 |
| Long | 15-24 | 28-36px | 400-500 | 2行 |
| Extended | 25+ | 22-28px | 500 | 2-3行 |

### 纯JS实现

```javascript
function getTitleStyle(text, baseSize) {
  baseSize = baseSize || 56;
  var len = text.length;
  if (len <= 6) return { fontSize: baseSize + 'px', fontWeight: '300', lineHeight: '1.15' };
  if (len <= 14) return { fontSize: Math.round(baseSize * 0.72) + 'px', fontWeight: '400', lineHeight: '1.2' };
  if (len <= 24) return { fontSize: Math.round(baseSize * 0.52) + 'px', fontWeight: '500', lineHeight: '1.3' };
  return { fontSize: Math.round(baseSize * 0.4) + 'px', fontWeight: '500', lineHeight: '1.4',
           WebkitLineClamp: '3', display: '-webkit-box', WebkitBoxOrient: 'vertical', overflow: 'hidden' };
}
```

### 动态调整规则

1. **永不溢出**：文字溢出容器时，先降一级字号，再加 `line-clamp` 兜底
2. **最小可读**：640px画布上，正文最小14px，说明文字最小10px
3. **数字强调**：数据卡片中的数字始终用最大字号（如 "$186.74亿" 用48px）
4. **CJK换行**：中文任意字符处可换行，不依赖空格 word-break
5. **行高随字号**：Display 1.1-1.2，Body 1.5-1.6，Caption 1.3-1.4
