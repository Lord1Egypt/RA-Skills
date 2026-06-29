# 设计令牌参考

> CSS变量体系 + 三套财经配色 + 三画幅系统 + 字号规范
> 版本: 2.0 | 画布: 宽幅 640×400 / 标准 640×480 / 方版 640×640

---

## 1. CSS变量体系

### 通用变量（所有图表共享）

```css
:root {
  /* 基础色 */
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;

  /* 表面层级 */
  --surface: #ffffff;          /* 卡片白 */
  --surface-2: #f2f2f0;        /* 次级表面（浅灰） */

  /* 语义色 — 涨跌/状态 */
  --good: #1aaf6c;             /* 正向-绿（涨/达标/好） */
  --bad: #e0445a;              /* 负向-红（跌/未达标/差） */
  --warn: #f5a524;             /* 警告-琥珀（注意/中性偏负） */

  /* 字体 */
  --font-body: 'Noto Sans SC', sans-serif;
  --font-data: 'Inter', 'Noto Sans SC', sans-serif;  /* 数据专用，等宽数字 */

  /* 图表色板 (Okabe-Ito 色盲安全) */
  --chart-1: #E69F00;
  --chart-2: #56B4E9;
  --chart-3: #009E73;
  --chart-4: #D55E00;
  --chart-5: #CC79A7;
  --chart-6: #F0E442;
  --chart-7: #0072B2;
  --chart-8: #000000;
}
```

### 数据字体对齐

```css
.num {
  font-family: var(--font-data);
  font-feature-settings: 'tnum' on;
  letter-spacing: -0.02em;
}
```

> Inter 的 `tnum` 特性确保数字等宽对齐，表格和KPI卡片中数值列不会参差不齐。

### 主题切换

只替换 `:root` 变量即可切换主题：

**克制风（默认）**
```css
:root { --accent: #002FA7; }
```

**品牌DNA — 微信绿**
```css
:root { --accent: #07C160; }
```

**品牌DNA — 经济学人红**
```css
:root { --accent: #E3120B; }
```

**品牌DNA — 知乎蓝**
```css
:root { --accent: #0066FF; }
```

**暖色系**
```css
:root { --accent: #C0392B; --paper: #f8f6f1; }
```

---

## 2. 高端财经媒体配色方案

> 三套方案分别对标麦肯锡、经济学人、财新杂志的图表视觉风格。
> 核心原则：低饱和度、高灰度占比、单色系为主+1个强调色、大面积留白。

### 方案A：麦肯锡 McKinsey

**视觉特征**：深蓝主色+青绿辅助+暖灰底色，克制严谨，数据密度高但视觉噪音低。

```css
:root {
  --ink: #1B1B1B;
  --paper: #F7F5F2;        /* 暖灰白，非纯白 */
  --accent: #0F4C81;       /* 麦肯锡深蓝 — 强调色块必须用品牌色 */
  --muted: #6B6B6B;
  --rule: #D9D5CF;         /* 暖灰分割线 */
  --surface: #ffffff;
  --surface-2: #efeee9;    /* 暖灰次级表面 */
  --good: #2f7d4a;         /* 麦肯锡绿 */
  --bad: #b53a2a;          /* 麦肯锡红 */
  --warn: #c47b25;         /* 麦肯锡琥珀 */
  --font-body: 'Noto Sans SC', sans-serif;
  --font-data: 'Inter', 'Noto Sans SC', sans-serif;

  /* 麦肯锡图表色板：低饱和度、蓝-青-绿-琥珀渐进 */
  --chart-1: #0F4C81;      /* 深蓝 Steel Blue */
  --chart-2: #2A7B9B;      /* 青蓝 Teal Blue */
  --chart-3: #3A9D8F;      /* 青绿 Sage Teal */
  --chart-4: #A8B820;      /* 橄榄绿 Olive */
  --chart-5: #E2A828;      /* 琥珀 Amber */
  --chart-6: #C76D5E;      /* 赤陶 Terracotta */
  --chart-7: #7B6B8D;      /* 灰紫 Mauve */
  --chart-8: #4A4A4A;      /* 深灰 Charcoal */
}
```

**使用要点**：
- 主色用 `--chart-1` 深蓝，强调用 `--chart-5` 琥珀
- 背景 `--paper` 是暖灰白 #F7F5F2，不是纯白
- 分割线用暖灰 `--rule` #D9D5CF
- 数据标签用 `--ink` #1B1B1B，不用纯黑
- 卡片背景用 `--surface` 或 `rgba(15,76,129,0.04)`
- **强调色块用 `--accent` (#0F4C81) 深蓝底+白字，禁止用近黑色**

### 方案B：经济学人 The Economist

**视觉特征**：标志性红+深蓝灰+米白底，对比鲜明，标题粗重数据纤细，英式克制。

```css
:root {
  --ink: #1D1D1B;
  --paper: #FDFBF7;        /* 米白，微暖 */
  --accent: #E3120B;       /* 经济学人红 — 强调色块必须用品牌色 */
  --muted: #6C6C6C;
  --rule: #D5D0C8;         /* 米灰分割线 */
  --surface: #ffffff;
  --surface-2: #f0ede5;    /* 米灰次级表面 */
  --good: #1f7a3a;         /* 经济学人绿 */
  --bad: #9c2a25;          /* 经济学人红（深） */
  --warn: #c47b25;         /* 经济学人琥珀 */
  --font-body: 'Noto Sans SC', sans-serif;
  --font-data: 'Inter', 'Noto Sans SC', sans-serif;

  /* 经济学人图表色板：红-蓝-灰为主，低饱和辅助色 */
  --chart-1: #E3120B;      /* 经济学人红 */
  --chart-2: #0D47A1;      /* 深蓝 Navy */
  --chart-3: #4A7C59;      /* 橄榄绿 Olive Green */
  --chart-4: #D4A843;      /* 旧金 Gold */
  --chart-5: #7B5EA7;      /* 灰紫 Muted Purple */
  --chart-6: #C4784A;      /* 赤铜 Copper */
  --chart-7: #3B7D8C;      /* 灰青 Slate Teal */
  --chart-8: #4A4A4A;      /* 深灰 Charcoal */
}
```

**使用要点**：
- 强调用 `--chart-1` 红，主数据用 `--chart-2` 深蓝
- 标题字重500，数据数字字重200（粗细对比是经济学人标志）
- 来源行用小号斜体，底部细线分隔
- **强调色块用 `--accent` (#E3120B) 红底+白字，禁止用近黑色**
- 涨跌用 `--good` 绿 / `--bad` 红

### 方案C：财新 Caixin

**视觉特征**：财新蓝+深墨+冷灰底，中式财经克制，信息密度极高，留白精准。

```css
:root {
  --ink: #1A1A1A;
  --paper: #F5F5F3;        /* 冷灰白 */
  --accent: #0055AA;       /* 财新蓝 — 强调色块必须用品牌色 */
  --muted: #757575;
  --rule: #D4D4D4;         /* 冷灰分割线 */
  --surface: #ffffff;
  --surface-2: #eaeae8;    /* 冷灰次级表面 */
  --good: #1f7a3a;         /* 财新绿 */
  --bad: #9c2a25;          /* 财新红（深） */
  --warn: #c47b25;         /* 财新琥珀 */
  --font-body: 'Noto Sans SC', sans-serif;
  --font-data: 'Inter', 'Noto Sans SC', sans-serif;

  /* 财新图表色板：蓝-灰为主，暖色点缀 */
  --chart-1: #0055AA;      /* 财新蓝 */
  --chart-2: #3A7BBF;      /* 中蓝 */
  --chart-3: #7BAFD4;      /* 浅蓝 */
  --chart-4: #C0392B;      /* 警示红 */
  --chart-5: #D4883A;      /* 暖铜 Bronze */
  --chart-6: #5B8C5A;      /* 灰绿 Sage */
  --chart-7: #8E7CC3;      /* 灰紫 Lavender */
  --chart-8: #4A4A4A;      /* 深灰 Charcoal */
}
```

**使用要点**：
- 主色用 `--chart-1` 财新蓝，警示用 `--chart-4` 红
- 同色系渐变（蓝→中蓝→浅蓝）用于分组/层级对比
- 背景冷灰白 #F5F5F3，分割线冷灰
- **强调色块用 `--accent` (#0055AA) 蓝底+白字，禁止用近黑色**
- 数据来源标注严格，用「数据来源：」而非「Source:」

### 三方案速查对比

| 维度 | 麦肯锡 | 经济学人 | 财新 |
|------|--------|---------|------|
| 底色 | 暖灰白 #F7F5F2 | 米白 #FDFBF7 | 冷灰白 #F5F5F3 |
| 主色 | 深蓝 #0F4C81 | 红 #E3120B | 蓝 #0055AA |
| 强调色 | 琥珀 #E2A828 | 深蓝 #0D47A1 | 红 #C0392B |
| 强调色块底色 | 深蓝 #0F4C81 | 红 #E3120B | 蓝 #0055AA |
| 分割线 | 暖灰 #D9D5CF | 米灰 #D5D0C8 | 冷灰 #D4D4D4 |
| 涨色 | 绿 #2f7d4a | 绿 #1f7a3a | 绿 #1f7a3a |
| 跌色 | 红 #b53a2a | 红 #9c2a25 | 红 #9c2a25 |
| 风格气质 | 克制严谨 | 英式鲜明 | 中式精炼 |
| 适用场景 | 咨询报告/战略分析 | 全球财经/深度调查 | 国内财经/政策解读 |
| 色板特征 | 蓝→青→绿渐进 | 红+蓝对比为主 | 蓝色系渐变+红警示 |

### 强调色块硬约束

```
🚫 禁止用近黑色（#051C2C / #1D1D1B / #1A1A1A 等）做强调色块背景
✅ 强调色块必须用 --accent 品牌色做底色 + 白色/浅色文字
✅ 洞察框/关键数据卡/公式结果块 → background: var(--accent); color: var(--paper);
```

---

## 3. 字号规范

### 图表专用字号

| 元素 | 字号 | 字重 | 颜色 | 用途 |
|------|------|------|------|------|
| kicker | 10-11px | 500 | --accent | 分类标签 |
| title | 18-24px | 500 | --ink | 图表标题 |
| subtitle | 11px | 400 | --muted | 副标题/补充说明 |
| axis-label | 11-12px | 400 | --muted | 轴刻度标签 |
| data-label | 12-13px | 500 | --ink / --paper | 数据标注 |
| legend-text | 12-13px | 400 | --ink | 图例文字 |
| source | 10-11px | 400 | --muted | 数据来源 |
| num-mega | 48-64px | 200 | --ink | billboard大数字 |
| num-label | 14-16px | 500 | --accent | billboard标签 |
| num-kpi | 28-36px | 200 | --ink / --chart-* | KPI卡片数字 |
| sparkline-label | 9-10px | 400 | --muted | 迷你趋势线标签 |

### 标题长度→字号映射

| 标题长度 | 字号 | 字重 |
|---------|------|------|
| ≤6字 | 24px | 500 |
| 7-14字 | 22px | 500 |
| 15-24字 | 18px | 500 |
| 25+字 | 16px | 500 |

---

## 4. 间距规范

| 元素 | 间距 |
|------|------|
| 页面内边距 | 36-48px |
| 标题与图表间距 | 16-28px |
| 图表行间距 | 6-14px |
| KPI卡片间距 | 8-12px |
| 图例项间距 | 16-20px |
| 来源与图表间距 | 12-20px |

---

## 5. 三画幅系统

> 宽度固定640px，高度按内容自适应，每种画幅有基准高度和弹性区间。

### 画幅定义

| 画幅 | 基准尺寸 | 弹性区间 | 比例 | 设计逻辑 |
|------|---------|---------|------|---------|
| **宽幅** | 640×400 | 360-480px | 16:10 | 横向信息展开，移动端一屏可见 |
| **标准** | 640×480 | 420-600px | 4:3 | 信息密度与可读性平衡 |
| **方版** | 640×640 | 560-720px | 1:1 | 径向/对称结构，视觉重心居中 |

### 高度弹性规则

```
基准高度 = 画幅基准值（400/480/640）
实际高度 = 基准高度 + 内容溢出量
内容溢出量 ∈ [−40px, +80px]（向下取整到8的倍数）

判断逻辑：
- 数据行数 ≤4 → 用区间下限
- 数据行数 5-8 → 用基准值
- 数据行数 ≥9 或含洞察框 → 用区间上限
```

### 图型→画幅映射

| 图型 | 画幅 | 基准高度 | 说明 |
|------|------|---------|------|
| bar-chart | 标准 | 480 | 竖柱，4-8条 |
| h-bar-chart | 标准 | 480 | 横柱，5-10条 |
| line-chart | 宽幅 | 400 | 折线，横向展开 |
| donut-chart | 方版 | 640 | 环形，径向结构 |
| quadrant-chart | 方版 | 640 | 象限，2×2矩阵 |
| radar-chart | 方版 | 640 | 雷达，多轴对称 |
| venn-diagram | 方版 | 640 | 维恩，圆形交叠 |
| flow-chart | 宽幅 | 400 | 流程，横向步骤 |
| layered-diagram | 标准 | 480 | 层级，上下堆叠 |
| waterfall-chart | 标准 | 480 | 瀑布，增减对比 |
| scatter-plot | 方版 | 640 | 散点，自由分布 |
| bubble-chart | 方版 | 640 | 气泡，面积编码 |
| treemap | 标准 | 480 | 矩形树，面积占比 |
| data-billboard | 标准 | 480 | 大数字+标签 |
| grouped-bar | 宽幅 | 400 | 分组柱，横向展开 |
| stacked-bar | 标准 | 480 | 堆叠柱，纵向对比 |
| area-chart | 宽幅 | 400 | 面积，趋势填充 |
| comparison-table | 标准 | 480 | 对比表，行列结构 |

### KPI卡片+Sparkline组件

```html
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">月活用户</div>
    <div class="kpi-value num">2.4M</div>
    <div class="kpi-delta up">+12.3%</div>
    <svg class="sparkline" viewBox="0 0 80 24" preserveAspectRatio="none">
      <polyline fill="none" stroke="var(--chart-1)" stroke-width="1.5"
        points="0,18 10,16 20,14 30,15 40,12 50,10 60,8 70,6 80,4"/>
    </svg>
  </div>
</div>
```

```css
.kpi-grid { display:flex; gap:10px; margin-bottom:20px; }
.kpi-card { flex:1; padding:14px; background:var(--surface); border:1px solid var(--rule); border-radius:4px; }
.kpi-label { font-size:10px; color:var(--muted); margin-bottom:4px; }
.kpi-value { font-size:28px; font-weight:200; line-height:1; }
.kpi-delta { font-size:10px; font-weight:500; margin-top:2px; }
.kpi-delta.up { color:var(--good); }
.kpi-delta.down { color:var(--bad); }
.sparkline { width:100%; height:24px; margin-top:6px; }
```

### 字体加载

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
```
