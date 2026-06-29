# 图表系统参考

> 18种图型 + 三轴决策树 + 拦截规则 + 三画幅系统 + HTML骨架
> 版本: 2.0 | 画布: 宽幅 640×400 / 标准 640×480 / 方版 640×640

---

## 1. 三轴决策树

```
数据关系是什么？（轴1: 变量类型）
│
├─ 类别比较（1分类 + 1连续）
│   ├─ 少类别 (2-6) → bar-chart
│   ├─ 多类别 (7+) → horizontal-bar-chart
│   └─ 分组对比 → grouped-bar
│
├─ 时间变化（1时间 + 1连续）
│   ├─ 少数据点 (2-8) → bar-chart
│   ├─ 多数据点 (8+) → line-chart
│   └─ 趋势+总量 → area-chart
│
├─ 占比关系（1分类看构成）
│   ├─ 少分段 (2-5) → donut-chart
│   ├─ 多分段 (6+) → treemap
│   └─ 分组占比 → stacked-bar
│
├─ 相关性（2+连续变量）
│   ├─ 2变量 → scatter-plot
│   ├─ 2变量+阈值 → quadrant-chart
│   └─ 3+变量 → bubble-chart
│
├─ 流程（顺序/并行步骤）
│   ├─ 顺序步骤 → flow-chart
│   ├─ 并行泳道 → swimlane-chart
│   └─ 状态转换 → state-machine
│
├─ 层级（嵌套/分类结构）
│   ├─ 树结构 → tree-chart
│   └─ 分层架构 → layered-diagram
│
├─ 集合重叠
│   └─ 2-3集合 → venn-diagram
│
├─ 累积变化
│   └─ 正负贡献 → waterfall-chart
│
└─ 多维度对比
    └─ 行列结构 → comparison-table
```

### 同一数据不同论点 → 不同图

| 数据 | 论点"比较" | 论点"趋势" | 论点"占比" |
|------|-----------|-----------|-----------|
| 2020-2024年收入 | bar-chart（4组对比） | line-chart（增长趋势） | — |
| 3产品市场份额 | bar-chart（谁最大） | — | donut-chart（各占多少） |
| 用户画像标签 | h-bar-chart（排名） | — | treemap（层级占比） |

---

## 2. 18种图型

| # | Type | When | Data Shape | 画幅 |
|---|------|------|-----------|------|
| 1 | **bar-chart** | 2-6类别比较 | `[{label, value, color?}]` | 标准 |
| 2 | **horizontal-bar-chart** | 7+类别或长标签 | `[{label, value, color?}]` | 标准 |
| 3 | **line-chart** | 8+时间点趋势 | `{labels, series:[{name,values,color?}]}` | 宽幅 |
| 4 | **donut-chart** | 2-5段占比 | `[{label, value, color}]` | 方版 |
| 5 | **quadrant-chart** | 2轴+阈值线 | `{xLabel, yLabel, items:[{name,x,y}]}` | 方版 |
| 6 | **flow-chart** | 3-8步顺序流程 | `{steps:[{id,label,type?}], connections:[{from,to}]}` | 宽幅 |
| 7 | **swimlane-chart** | 2-4角色并行流程 | `{lanes:[{name,steps}]}` | 宽幅 |
| 8 | **state-machine** | 状态转换+条件 | `{states, transitions}` | 方版 |
| 9 | **tree-chart** | 层级结构 | `{root:{label,children}}` | 标准 |
| 10 | **layered-diagram** | 分层架构 | `{layers:[{name,items,color?}]}` | 标准 |
| 11 | **venn-diagram** | 2-3集合重叠 | `{sets, overlap}` | 方版 |
| 12 | **waterfall-chart** | 累积正负贡献 | `[{label,value,type}]` | 标准 |
| 13 | **treemap** | 多类别层级占比 | `[{label,value,color?,children?}]` | 标准 |
| 14 | **scatter-plot** | 2连续变量关系 | `{xLabel, yLabel, items:[{name,x,y}]}` | 方版 |
| 15 | **grouped-bar** | 分组类别对比 | `{labels, groups:[{name,values,color?}]}` | 宽幅 |
| 16 | **stacked-bar** | 分组占比对比 | `{labels, segments:[{name,values,color?}]}` | 标准 |
| 17 | **area-chart** | 趋势+总量 | `{labels, series:[{name,values,color?}]}` | 宽幅 |
| 18 | **comparison-table** | 多维度行列对比 | `{headers, rows:[{label, values}]}` | 标准 |

### 补充: data-billboard（非独立图型，用于单一数值高亮）

| Type | When | Data Shape | 画幅 |
|------|------|-----------|------|
| **data-billboard** | 单一关键数值 | `{value, label, context?, stats:[{value,label}]}` | 标准 |

---

## 3. 拦截规则详解

| # | 触发条件 | 问题 | 替代方案 | 话术模板 |
|---|---------|------|---------|---------|
| I1 | 2个数据点画折线 | 2点折线无趋势意义 | bar-chart | "2个数据点画折线图看不出趋势，改用柱状图更直观" |
| I2 | 7+类别画donut | 角度比较超过5段人眼难分 | horizontal-bar-chart | "7+类别画环形图角度难区分，横向柱状图长度比较更清晰" |
| I3 | 单一数值做数据图 | 1个数字不需要图 | data-billboard | "单个数值不需要复杂图表，用数字高亮卡更有冲击力" |
| I4 | 一图>2论点 | 信息过载 | 拆图 | "一张图承载多个论点会稀释每个论点的传达力，建议拆分" |
| I5 | 类别变量用折线 | 暗示不存在的连续关系 | bar-chart | "类别变量之间没有连续关系，折线会误导读者，改用柱状图" |
| I6 | Y轴不从0起 | 误导小差异看起来很大 | 加断裂标记或从0起 | "Y轴不从0起会夸大差异，建议从0起或加明显的轴断裂标记" |
| I7 | rainbow/jet色图 | 感知不均匀 | 主题色板+冗余编码 | "彩虹色图感知不均匀会造假峰，改用色盲安全色板" |
| I8 | 图例压数据 | 遮挡关键信息 | 调整图例位置 | "图例遮挡了数据，建议移到空白区域" |

---

## 4. 色盲安全色板

### Okabe-Ito 8色（默认）

```css
:root {
  --chart-1: #E69F00; /* 橙 */
  --chart-2: #56B4E9; /* 天蓝 */
  --chart-3: #009E73; /* 青绿 */
  --chart-4: #D55E00; /* 朱红 */
  --chart-5: #CC79A7; /* 粉紫 */
  --chart-6: #F0E442; /* 黄 */
  --chart-7: #0072B2; /* 深蓝 */
  --chart-8: #000000; /* 黑 */
}
```

### 使用规则

1. **单图不超4色** — 超过4类时合并小类为"其他"
2. **冗余编码** — 不同类别加不同形状(marker)或线型(dashed/solid/dotted)
3. **灰度可分** — 出图前想象灰度版，颜色仍可区分
4. **强调色** — 需要高亮某一类时用 `--accent`，其余用 `--chart-*`

### 冗余编码参考

| 类别 | 颜色 | 形状 | 线型 |
|------|------|------|------|
| A | --chart-1 | circle ● | solid |
| B | --chart-2 | square ■ | dashed |
| C | --chart-3 | triangle ▲ | dotted |
| D | --chart-4 | diamond ◆ | dash-dot |

---

## 5. Chart Styling Rules

- **Typography**: 标题 `--font-body` 18-24px/500; 轴标 12px/400 `--muted`; 数据标 13px/500 `.num`; 来源 10-11px `--muted`
- **Data Font**: 数值用 `.num` class → `--font-data` (Inter) + `tnum` 等宽对齐
- **Spacing**: 内边距 36-48px; 图例间距 16px; KPI卡片间距 8-12px
- **Surface**: 卡片用 `--surface`; 次级表面用 `--surface-2`; 强调块用 `--accent` + 白字
- **Semantic Colors**: 涨 `--good`; 跌 `--bad`; 警告 `--warn`
- **SVG**: 用 `viewBox` + `width:100%` + `height:auto`
- **A11y**: `role="img"` + `aria-label`; 不纯靠颜色区分
- **Source**: 每张图底部必须标注数据来源
- **Accent Block**: 强调色块必须用 `--accent` 品牌色，禁止近黑色

---

## 6. HTML骨架（每种图型）

### 通用头部（所有骨架共享）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a; --paper: #fafaf8; --accent: #002FA7;
  --muted: #737373; --rule: #d4d4d2;
  --surface: #ffffff; --surface-2: #f2f2f0;
  --good: #1aaf6c; --bad: #e0445a; --warn: #f5a524;
  --font-body: 'Noto Sans SC', sans-serif;
  --font-data: 'Inter', 'Noto Sans SC', sans-serif;
  --chart-1: #E69F00; --chart-2: #56B4E9; --chart-3: #009E73; --chart-4: #D55E00;
}
* { margin:0; padding:0; box-sizing:border-box; }
.num { font-family:var(--font-data); font-feature-settings:'tnum' on; letter-spacing:-0.02em; }
</style>
```

### KPI卡片+Sparkline组件（可嵌入任何图型头部）

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
  <div class="kpi-card">
    <div class="kpi-label">付费率</div>
    <div class="kpi-value num">8.7%</div>
    <div class="kpi-delta down">-0.3%</div>
    <svg class="sparkline" viewBox="0 0 80 24" preserveAspectRatio="none">
      <polyline fill="none" stroke="var(--chart-2)" stroke-width="1.5"
        points="0,8 10,10 20,9 30,12 40,11 50,14 60,13 70,16 80,15"/>
    </svg>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">ARPU</div>
    <div class="kpi-value num">¥42</div>
    <div class="kpi-delta up">+5.1%</div>
    <svg class="sparkline" viewBox="0 0 80 24" preserveAspectRatio="none">
      <polyline fill="none" stroke="var(--chart-3)" stroke-width="1.5"
        points="0,20 10,18 20,16 30,14 40,12 50,10 60,8 70,6 80,4"/>
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

### bar-chart (标准 640×480)

```html
<!-- 通用头部 + 以下 -->
<style>
html, body { width:640px; overflow:hidden; font-family:var(--font-body); background:var(--paper); color:var(--ink); }
.page { width:640px; padding:40px 48px; }
.kicker { font-size:11px; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); margin-bottom:6px; }
.title { font-size:22px; font-weight:500; line-height:1.3; margin:0 0 24px; }
.chart-area { display:flex; flex-direction:column; gap:12px; }
.bar-row { display:flex; align-items:center; gap:12px; }
.bar-label { width:80px; font-size:13px; text-align:right; flex-shrink:0; }
.bar-track { flex:1; height:32px; background:var(--surface-2); border-radius:2px; position:relative; }
.bar-fill { height:100%; border-radius:2px; display:flex; align-items:center; justify-content:flex-end; padding-right:10px; }
.bar-value { font-size:12px; font-weight:500; color:var(--paper); }
.source { font-size:11px; color:var(--muted); margin-top:20px; }
</style>
<body>
<div class="page">
  <div class="kicker">数据对比</div>
  <h2 class="title">标题</h2>
  <div class="chart-area">
    <div class="bar-row">
      <span class="bar-label">类别A</span>
      <div class="bar-track"><div class="bar-fill" style="width:85%;background:var(--chart-1)"><span class="bar-value num">85%</span></div></div>
    </div>
    <div class="bar-row">
      <span class="bar-label">类别B</span>
      <div class="bar-track"><div class="bar-fill" style="width:62%;background:var(--chart-2)"><span class="bar-value num">62%</span></div></div>
    </div>
  </div>
  <div class="source">数据来源：XXX</div>
</div>
</body>
```

### line-chart (宽幅 640×400)

```html
<!-- 通用头部 + 以下 -->
<style>
html, body { width:640px; overflow:hidden; font-family:var(--font-body); background:var(--paper); color:var(--ink); }
.page { width:640px; padding:36px 48px; }
.kicker { font-size:11px; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); margin-bottom:6px; }
.title { font-size:22px; font-weight:500; line-height:1.3; margin:0 0 20px; }
.chart-container { width:544px; }
.legend { display:flex; gap:20px; margin-bottom:12px; }
.legend-item { display:flex; align-items:center; gap:6px; font-size:12px; }
.legend-dot { width:10px; height:10px; border-radius:50%; }
svg { width:100%; height:auto; }
.axis-label { font-size:11px; fill:var(--muted); }
.source { font-size:11px; color:var(--muted); margin-top:16px; }
</style>
<body>
<div class="page">
  <div class="kicker">趋势</div>
  <h2 class="title">标题</h2>
  <div class="chart-container">
    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:var(--chart-1)"></div>系列A</div>
      <div class="legend-item"><div class="legend-dot" style="background:var(--chart-2)"></div>系列B</div>
    </div>
    <svg viewBox="0 0 544 280" xmlns="http://www.w3.org/2000/svg">
      <line x1="50" y1="20" x2="530" y2="20" stroke="var(--rule)" stroke-width="0.5"/>
      <line x1="50" y1="80" x2="530" y2="80" stroke="var(--rule)" stroke-width="0.5"/>
      <line x1="50" y1="140" x2="530" y2="140" stroke="var(--rule)" stroke-width="0.5"/>
      <line x1="50" y1="200" x2="530" y2="200" stroke="var(--rule)" stroke-width="0.5"/>
      <line x1="50" y1="260" x2="530" y2="260" stroke="var(--rule)" stroke-width="0.5"/>
      <polyline points="50,200 150,160 250,120 350,80 450,60 530,40" fill="none" stroke="var(--chart-1)" stroke-width="2"/>
      <polyline points="50,220 150,200 250,180 350,160 450,140 530,120" fill="none" stroke="var(--chart-2)" stroke-width="2" stroke-dasharray="6,3"/>
      <text x="50" y="280" class="axis-label" text-anchor="middle">2020</text>
      <text x="150" y="280" class="axis-label" text-anchor="middle">2021</text>
      <text x="250" y="280" class="axis-label" text-anchor="middle">2022</text>
      <text x="350" y="280" class="axis-label" text-anchor="middle">2023</text>
      <text x="450" y="280" class="axis-label" text-anchor="middle">2024</text>
      <text x="530" y="280" class="axis-label" text-anchor="middle">2025</text>
    </svg>
  </div>
  <div class="source">数据来源：XXX</div>
</div>
</body>
```

### donut-chart (方版 640×640)

```html
<!-- 通用头部 + 以下 -->
<style>
html, body { width:640px; height:640px; overflow:hidden; font-family:var(--font-body); background:var(--paper); color:var(--ink); }
.page { width:640px; height:640px; padding:48px; display:flex; flex-direction:column; }
.kicker { font-size:11px; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); margin-bottom:6px; }
.title { font-size:22px; font-weight:500; line-height:1.3; margin:0 0 24px; }
.chart-center { flex:1; display:flex; align-items:center; justify-content:center; }
svg { width:320px; height:320px; }
.legend { display:flex; flex-wrap:wrap; gap:16px; justify-content:center; margin-top:24px; }
.legend-item { display:flex; align-items:center; gap:6px; font-size:13px; }
.legend-dot { width:12px; height:12px; border-radius:2px; }
.source { font-size:11px; color:var(--muted); margin-top:auto; }
</style>
<body>
<div class="page">
  <div class="kicker">占比</div>
  <h2 class="title">标题</h2>
  <div class="chart-center">
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <circle cx="100" cy="100" r="70" fill="none" stroke="var(--chart-1)" stroke-width="30"
              stroke-dasharray="132 308" stroke-dashoffset="0" transform="rotate(-90 100 100)"/>
      <circle cx="100" cy="100" r="70" fill="none" stroke="var(--chart-2)" stroke-width="30"
              stroke-dasharray="110 330" stroke-dashoffset="-132" transform="rotate(-90 100 100)"/>
      <circle cx="100" cy="100" r="70" fill="none" stroke="var(--chart-3)" stroke-width="30"
              stroke-dasharray="88 352" stroke-dashoffset="-242" transform="rotate(-90 100 100)"/>
      <text x="100" y="96" text-anchor="middle" font-size="28" font-weight="200" fill="var(--ink)" class="num">100%</text>
      <text x="100" y="116" text-anchor="middle" font-size="11" fill="var(--muted)">总计</text>
    </svg>
  </div>
  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:var(--chart-1)"></div>A 30%</div>
    <div class="legend-item"><div class="legend-dot" style="background:var(--chart-2)"></div>B 25%</div>
    <div class="legend-item"><div class="legend-dot" style="background:var(--chart-3)"></div>C 20%</div>
  </div>
  <div class="source">数据来源：XXX</div>
</div>
</body>
```

### data-billboard (标准 640×480)

```html
<!-- 通用头部 + 以下 -->
<style>
html, body { width:640px; overflow:hidden; font-family:var(--font-body); background:var(--paper); color:var(--ink); }
.page { width:640px; padding:48px; display:flex; flex-direction:column; min-height:480px; }
.kicker { font-size:11px; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); margin-bottom:6px; }
.num-mega { font-size:64px; font-weight:200; line-height:1; color:var(--ink); margin:auto 0 0; }
.num-label { font-size:16px; font-weight:500; color:var(--accent); margin-top:12px; letter-spacing:0.05em; }
.num-context { font-size:14px; color:var(--muted); line-height:1.6; margin-top:8px; max-width:400px; }
.stats { display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-top:auto; }
.stat-card { background:var(--accent); color:var(--paper); padding:16px; border-radius:4px; }
.stat-card .num { font-size:22px; font-weight:200; }
.stat-card .label { font-size:11px; color:rgba(255,255,255,0.7); margin-top:4px; }
.source { font-size:11px; color:var(--muted); margin-top:16px; }
</style>
<body>
<div class="page">
  <div class="kicker">关键数据</div>
  <p class="num-mega num">2.4 亿</p>
  <div class="num-label">中国灵活就业人口</div>
  <p class="num-context">占全国就业人口的近三分之一</p>
  <div class="stats">
    <div class="stat-card"><div class="num">+12%</div><div class="label">年增长率</div></div>
    <div class="stat-card"><div class="num">68%</div><div class="label">90后占比</div></div>
    <div class="stat-card"><div class="num">3.2万</div><div class="label">年均收入</div></div>
  </div>
  <div class="source">数据来源：XXX</div>
</div>
</body>
```

### flow-chart (宽幅 640×400)

```html
<!-- 通用头部 + 以下 -->
<style>
html, body { width:640px; overflow:hidden; font-family:var(--font-body); background:var(--paper); color:var(--ink); }
.page { width:640px; padding:36px 48px; }
.kicker { font-size:11px; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); margin-bottom:6px; }
.title { font-size:22px; font-weight:500; line-height:1.3; margin:0 0 28px; }
.flow { display:flex; flex-direction:column; gap:0; }
.step { display:flex; align-items:flex-start; gap:16px; padding:14px 0; }
.step + .step { border-top:1px solid var(--rule); }
.step-num { font-size:13px; font-weight:500; color:var(--accent); width:28px; flex-shrink:0; padding-top:2px; }
.step-title { font-size:16px; font-weight:500; line-height:1.3; }
.step-desc { font-size:13px; color:var(--muted); line-height:1.4; margin-top:4px; }
.source { font-size:11px; color:var(--muted); margin-top:20px; }
</style>
<body>
<div class="page">
  <div class="kicker">流程</div>
  <h2 class="title">标题</h2>
  <div class="flow">
    <div class="step"><span class="step-num">01</span><div><div class="step-title">步骤一</div><div class="step-desc">描述</div></div></div>
    <div class="step"><span class="step-num">02</span><div><div class="step-title">步骤二</div><div class="step-desc">描述</div></div></div>
    <div class="step"><span class="step-num">03</span><div><div class="step-title">步骤三</div><div class="step-desc">描述</div></div></div>
  </div>
  <div class="source">数据来源：XXX</div>
</div>
</body>
```

### grouped-bar (宽幅 640×400)

```html
<!-- 通用头部 + 以下 -->
<style>
html, body { width:640px; overflow:hidden; font-family:var(--font-body); background:var(--paper); color:var(--ink); }
.page { width:640px; padding:36px 48px; }
.kicker { font-size:11px; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); margin-bottom:6px; }
.title { font-size:22px; font-weight:500; line-height:1.3; margin:0 0 16px; }
.legend { display:flex; gap:20px; margin-bottom:16px; }
.legend-item { display:flex; align-items:center; gap:6px; font-size:12px; }
.legend-dot { width:10px; height:10px; border-radius:2px; }
.chart-area { display:flex; align-items:flex-end; gap:24px; height:200px; padding-bottom:28px; border-bottom:1px solid var(--rule); }
.group { display:flex; flex-direction:column; align-items:center; flex:1; }
.bars { display:flex; gap:4px; align-items:flex-end; height:200px; }
.bar { width:28px; border-radius:2px 2px 0 0; transition:height 0.3s; }
.group-label { font-size:11px; color:var(--muted); margin-top:8px; }
.source { font-size:11px; color:var(--muted); margin-top:16px; }
</style>
<body>
<div class="page">
  <div class="kicker">分组对比</div>
  <h2 class="title">标题</h2>
  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:var(--chart-1)"></div>系列A</div>
    <div class="legend-item"><div class="legend-dot" style="background:var(--chart-2)"></div>系列B</div>
  </div>
  <div class="chart-area">
    <div class="group"><div class="bars"><div class="bar" style="height:80%;background:var(--chart-1)"></div><div class="bar" style="height:60%;background:var(--chart-2)"></div></div><span class="group-label">Q1</span></div>
    <div class="group"><div class="bars"><div class="bar" style="height:90%;background:var(--chart-1)"></div><div class="bar" style="height:70%;background:var(--chart-2)"></div></div><span class="group-label">Q2</span></div>
    <div class="group"><div class="bars"><div class="bar" style="height:75%;background:var(--chart-1)"></div><div class="bar" style="height:85%;background:var(--chart-2)"></div></div><span class="group-label">Q3</span></div>
  </div>
  <div class="source">数据来源：XXX</div>
</div>
</body>
```

### comparison-table (标准 640×480)

```html
<!-- 通用头部 + 以下 -->
<style>
html, body { width:640px; overflow:hidden; font-family:var(--font-body); background:var(--paper); color:var(--ink); }
.page { width:640px; padding:40px 48px; }
.kicker { font-size:11px; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); margin-bottom:6px; }
.title { font-size:22px; font-weight:500; line-height:1.3; margin:0 0 20px; }
table { width:100%; border-collapse:collapse; font-size:13px; }
thead th { text-align:left; padding:10px 12px; background:var(--surface-2); color:var(--muted); font-weight:500; font-size:11px; letter-spacing:0.05em; }
tbody td { padding:10px 12px; border-bottom:1px solid var(--rule); }
tbody tr:hover { background:var(--surface-2); }
.delta-up { color:var(--good); font-weight:500; }
.delta-down { color:var(--bad); font-weight:500; }
.source { font-size:11px; color:var(--muted); margin-top:16px; }
</style>
<body>
<div class="page">
  <div class="kicker">对比</div>
  <h2 class="title">标题</h2>
  <table>
    <thead><tr><th>指标</th><th>2023</th><th>2024</th><th>变化</th></tr></thead>
    <tbody>
      <tr><td>收入</td><td class="num">1.2M</td><td class="num">1.5M</td><td class="delta-up num">+25%</td></tr>
      <tr><td>成本</td><td class="num">800K</td><td class="num">950K</td><td class="delta-down num">+19%</td></tr>
    </tbody>
  </table>
  <div class="source">数据来源：XXX</div>
</div>
</body>
```

---

## 7. 自动选图集成

内容解析后自动建议：

| 数据信号 | 推荐图型 | 画幅 |
|---------|---------|------|
| "A占X%，B占Y%" | bar-chart / h-bar-chart | 标准 |
| "逐年/逐月增长" | line-chart | 宽幅 |
| "分为三部分/占比" | donut-chart | 方版 |
| "A→B→C步骤" | flow-chart | 宽幅 |
| "包含/下属/层级" | tree-chart / layered-diagram | 标准 |
| "正相关/负相关" | scatter-plot | 方版 |
| "同时属于/交集" | venn-diagram | 方版 |
| "贡献了/减少了" | waterfall-chart | 标准 |
| "A和B各多少，按季度" | grouped-bar | 宽幅 |
| "趋势+总量" | area-chart | 宽幅 |
| "多维度对比" | comparison-table | 标准 |
