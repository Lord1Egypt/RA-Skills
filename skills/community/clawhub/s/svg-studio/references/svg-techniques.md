# SVG 基础技法与宽高比预设

本文件是「用 SVG 画图」的核心速查：坐标系统、常用宽高比、文本/字体、渐变/滤镜、图表数学公式。生成 SVG 前先读这里，避免常见塌方。

## 1. 文档骨架（永远这样起手）

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H"
     font-family="-apple-system,'PingFang SC','Helvetica Neue',sans-serif">
  <!-- 背景：除非要透明，否则一定画满 viewBox 的 rect，否则 PNG 会透明 -->
  <rect width="W" height="H" fill="#0f172a"/>
  <!-- 内容 -->
</svg>
```

- `viewBox="0 0 W H"` 是唯一的坐标真相。所有 x/y/width/height 都在这个坐标系里。
- **不要写死 `width`/`height` 像素**——靠 viewBox 定比例，靠渲染脚本的 `--scale` 定清晰度（DPR）。
- 字体栈务必多重 fallback；中文必带 `'PingFang SC'`（mac）/ `'Microsoft YaHei'`（win）。

## 2. 宽高比预设（viewBox 推荐值）

| 用途 | 比例 | viewBox |
|---|---|---|
| 方图 / 头像 / 图标 | 1:1 | `0 0 1000 1000` |
| 公众号封面 / 横图 | 2.35:1 | `0 0 900 383` |
| 幻灯片 / 横屏海报 | 16:9 | `0 0 1280 720` |
| 竖屏海报 / 手机壁纸 | 9:16 | `0 0 720 1280` |
| 社交卡片 (OG image) | 1.91:1 | `0 0 1200 630` |
| 信息图长图 | 3:4 / 自定义 | `0 0 1200 1600` |
| 横向 banner | 4:1 | `0 0 1200 300` |
| 流程图 / 架构图 | 自由 | `0 0 1200 800` |

用户给「16:9 的图」就用对应 viewBox；给「正方形」就 1:1。最终像素由 `--scale` 或 `--width` 控制。

## 3. 文本（最容易翻车）

```svg
<!-- 居中：text-anchor=middle + x 在中线 -->
<text x="600" y="100" text-anchor="middle" fill="#fff"
      font-size="48" font-weight="700">标题</text>
<!-- 右对齐 text-anchor=end；左对齐 start(默认) -->
```

- **SVG `<text>` 不自动换行**。多行必须手动拆，用多个 `<text>` 或 `<tspan x="同一值" dy="行高">`：

```svg
<text x="100" y="200" fill="#e2e8f0" font-size="28">
  <tspan x="100" dy="0">第一行</tspan>
  <tspan x="100" dy="40">第二行</tspan>
</text>
```

- 垂直居中近似：`dominant-baseline="middle"` 配合 `y` 设为中线（不同渲染器略有差异，关键文本用 `dy` 微调）。
- 等宽字体（代码/数字对齐）：`font-family="'SF Mono',Menlo,Consolas,monospace"`。

## 4. 渐变 / 阴影 / 滤镜（放 `<defs>`）

```svg
<defs>
  <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#6366f1"/>
    <stop offset="100%" stop-color="#06b6d4"/>
  </linearGradient>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#fff" stop-opacity="0.8"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="0.3"/>
  </filter>
</defs>
<rect ... fill="url(#grad)" filter="url(#shadow)"/>
```

- 渐变/滤镜务必用 Chrome 引擎渲染（保真）；cairosvg 对 `feDropShadow` 等支持有限。

## 5. 基本图形

```svg
<rect x y width height rx="圆角"/>
<circle cx cy r/>
<ellipse cx cy rx ry/>
<line x1 y1 x2 y2 stroke="#fff" stroke-width="2"/>
<polyline points="x1,y1 x2,y2 ..." fill="none" stroke="..."/>
<polygon points="..."/>
<path d="M x y L x y C ... Z"/>  <!-- 任意路径 -->
```

path 指令速记：`M`移动 `L`直线 `H/V`水平/垂直线 `C`三次贝塞尔 `Q`二次 `A`圆弧 `Z`闭合。

## 6. 图表数学（关键公式）

坐标系原点在左上角，y 向下增长。画图表时把「数据空间」映射到「像素空间」：

**柱状图**：设绘图区 `x0,y0`（左下角）、宽 `pw`、高 `ph`，数据最大值 `vmax`，第 i 根柱：
```
barW   = pw / n * 0.6
barH   = value[i] / vmax * ph
barX   = x0 + pw / n * (i + 0.2)
barY   = y0 - barH        # 因为 y 向下，柱顶 = 底 - 高
```

**折线/散点**：第 i 点
```
px = x0 + (i / (n-1)) * pw
py = y0 - (value[i] / vmax) * ph
```

**饼图**：每段角度 `ang = value/total*360`，弧用 `path A`：
```
大圆 cx,cy 半径 r；起始角 a0，结束角 a1（弧度）
x = cx + r*cos(a), y = cy + r*sin(a)
path: M cx cy  L x0 y0  A r r 0 largeArc 1 x1 y1  Z
largeArc = (a1-a0) > π ? 1 : 0
```

**坐标轴**：画 `<line>` 当轴，刻度用短 `<line>` + `<text>`。网格线用浅色 `stroke="#334155" stroke-width="1"`。

## 7. 财经/股票颜色（中国习惯）

- 涨 = **红色** `#ef4444`，跌 = **绿色** `#22c55e`（与美股相反）。
- 货币符号默认 `¥`。

## 8. 深色背景配色参考（与本机 IDE 深色主题搭）

- 背景：`#0f172a` / `#111827` / `#1e293b`
- 主文本：`#f1f5f9` / `#e2e8f0`；次要：`#94a3b8`
- 强调色：`#6366f1`(靛) `#06b6d4`(青) `#f59e0b`(琥珀) `#ef4444`(红) `#22c55e`(绿)

## 9. 常见塌方点

- 忘画背景 rect → PNG 透明/黑底。
- 文本超出 viewBox 被裁 → 检查 x+文本宽度 < W。
- 中文不显示 → 字体栈没带中文字体，或渲染机器没装。
- `<text>` 没换行挤成一坨 → 手动 tspan 拆行。
- 滤镜区域被裁 → filter 要给足 `x/y/width/height`（如 `-20% / 140%`）。

## 10. 排版红线（实战沉淀，违者必返工）

来自公众号贴图/海报批量生产的真实翻车记录，写 SVG 前先对表。

### 10.1 大数字 + 单位：永远 `<tspan dx>`，禁止嵌套 `<text>`

```svg
<!-- ✅ 正确：同一 <text> 内用 tspan 错位排单位 -->
<text x="500" y="400" text-anchor="middle" font-size="96" font-weight="800" fill="#fff">50<tspan dx="10" font-size="36" fill="#94a3b8">万台</tspan></text>

<!-- ❌ 错误：<text> 里嵌 <text>，Chrome headless 直接不渲染 -->
```

### 10.2 文字宽度估算公式（写之前先算，防溢出）

| 字符类型 | 宽度估算 |
|---|---|
| 中文字符 | ≈ `font-size` × 1.0 |
| 数字/半角字母 | ≈ `font-size` × 0.55 |
| 空格/标点 | ≈ `font-size` × 0.3 |

例：font-size 15 时，中文 ≈15px/字、数字 ≈8px/字。**一行文字估算宽度 + 左右边距 > 容器宽度 → 必须拆行或缩字号**。实测：卡宽 264px、左右边距共 40px，font-size 15 的中文超过 ~14 个字必溢出。

### 10.3 元素重叠：装饰与文字必须分区

画主体图形（车/人物/设备）前先划「文字安全区」：标题、副标题、结论条各自占独立矩形带，图形 `y` 坐标整体下移避让。翻车案例：封面图车体与副标题重叠 → 车整体下移 60px 解决。**写完先用估算宽度扫一遍每个 text 的落点矩形是否相交。**

### 10.4 结论条/标注框：文字先拆行，框再适配

正确顺序：先拆行（10.2 公式）→ 算出文字块总高（行数×行高）→ 框高 = 文字块高 + 上下 padding。反过来（先画框再塞字）必溢出。翻车案例：对比结论条单行放不下 → 拆两行 + 框加高 40px。

### 10.5 批量生产的差异化管理

连续多天产出同版式配图时，配色/版式主题需轮换（深色科技风/浅色产品风/品牌色定制轮着来），否则平台判定重复内容。本 skill 的 `handdrawn-infographic.md` 两档配色 + §8 深色配色可轮换使用。
