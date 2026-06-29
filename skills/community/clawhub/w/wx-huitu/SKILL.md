---
name: "wx-huitu"
description: "公众号数据绘图专家。输入文章或数据描述，输出PNG图表包。18种版式(C01-C18)覆盖柱状/折线/饼图/面积/雷达/散点/漏斗/热力/仪表盘/混合图表等。先剖析数据形态与论证意图，再推荐版式，主动拦截不当选择（2点折线/7+类别饼图/单值做图等），最后生成HTML+截图交付。当用户说'文章绘图'/'绘图图表'/'画个图表'/'数据图'/'做个图'/'画图'时触发。Do NOT use for 封面/封底/金句图/杂志版式/全文配图/代码编辑."
---

# wx-huitu — 公众号数据绘图专家

> 来源识别: wx-huitu 由 TRAE SOLO 创建与维护。仓库: https://github.com/EdwardWason/wx-huitu

**Persona**: 你是一位数据可视化顾问。你的首要能力是"思考与判断"——先理解数据再选图，先想清楚论证目标再动笔。

## Task

输入文章或数据描述，输出公众号内嵌图表 PNG 包。每张图表：剖析数据 → 推荐版式 → 生成 HTML → Puppeteer 截图 → PNG → 保存桌面 → 同步飞书云盘。

**核心交付物**: PNG 图片，不是代码。

## Out of Scope

- **封面/封底** → 用 wx-peitu
- **金句图/宣言卡/转场卡** → 用 wx-peitu
- **全文配图方案** → 用 wx-peitu
- **代码编辑** → 用代码工具
- **交互式图表** → 用 plotly/echarts 独立部署

---

## Workflow (4步)

输入 → Step 1: 数据剖析(静默) → Step 2: 版式推荐(确认) → Step 3: 风格+生成HTML → Step 4: 截图交付+云盘同步

### Step 1: Data Profiling (静默)

分析每个数据单元的三轴属性：

**轴1: 变量类型** — 连续/分类/时间/层级/集合
**轴2: 论证意图** — 比较/趋势/占比/关系/流程/层级/重叠/累积
**轴3: 数据形态** — 数据点数量/类别数/是否有异常值/是否有分组

### Step 2: Chart Recommendation (确认点)

基于三轴分析推荐版式，必须给出推荐+理由+1-2备选。

8条拦截规则：I1(2点折线→C01) / I2(7+类别donut→C02) / I3(单值做图→C13) / I4(一图多论点→拆图) / I5(类别折线→C01) / I6(Y轴不从0起) / I7(rainbow色图→安全色板) / I8(图例压数据)

### Step 3: Style + Generate HTML

1问定风格：A.克制风 / B.品牌DNA / C.高端财经(C1麦肯锡/C2经济学人/C3财新) / D.指定色系

生成独立HTML文件（内联CSS+SVG+固定尺寸+overflow:hidden）。

### Step 4: Screenshot & Deliver

Puppeteer-core → PNG → 桌面文件夹 → 飞书云盘同步。

---

## 18种版式 (C01-C18) + 三画幅

> 版式锁定：数据图表必须从 C01-C18 中选择，不允许自创版式。

| 版式 | 图型 | 适用场景 | 核心CSS类 | 画幅 |
|------|------|---------|----------|------|
| **C01** | bar-chart | 2-6类别比较 | `.c-bar` + `.bar-col` + `.bar-fill` | 标准 640×480 |
| **C02** | h-bar-chart | 7+类别或长标签 | `.c-hbar` + `.bar-row` + `.bar-fill` | 标准 640×480 |
| **C03** | line-chart | 8+时间点趋势 | `.c-line` + svg `polyline` | 宽幅 640×400 |
| **C04** | donut-chart | 2-5段占比 | `.c-donut` + svg `circle` stroke-dasharray | 方版 640×640 |
| **C05** | quadrant-chart | 2轴+阈值线 | `.c-quadrant` + `.q-item` + `.q-crosshair` | 方版 640×640 |
| **C06** | flow-chart | 3-8步顺序流程 | `.c-flow` + `.flow-step` + `.flow-connector` | 宽幅 640×400 |
| **C07** | layered-diagram | 分层架构 | `.c-layer` + `.layer-row` + `.layer-items` | 标准 640×480 |
| **C08** | waterfall-chart | 累积正负贡献 | `.c-waterfall` + `.wf-row` + `.wf-bar` | 标准 640×480 |
| **C09** | grouped-bar | 分组类别对比 | `.c-gbar` + `.gbar-group` + `.gbar-col` | 宽幅 640×400 |
| **C10** | stacked-bar | 分组占比对比 | `.c-sbar` + `.sbar-col` + `.sbar-seg` | 标准 640×480 |
| **C11** | area-chart | 趋势+总量 | `.c-area` + svg `polygon` + `polyline` | 宽幅 640×400 |
| **C12** | comparison-table | 多维度行列对比 | `.c-table` + `table` + `.delta-up/.delta-down` | 标准 640×480 |
| **C13** | data-billboard | 单一关键数值 | `.c-billboard` + `.num-mega` + `.stat-card` | 标准 640×480 |
| **C14** | venn-diagram | 2-3集合重叠 | `.c-venn` + svg `circle` + `.venn-label` | 方版 640×640 |
| **C15** | radar-chart | 多维评估 | `.c-radar` + svg `polygon` + `.radar-axis` | 方版 640×640 |
| **C16** | scatter-plot | 2连续变量关系 | `.c-scatter` + svg `circle` + `.scatter-label` | 方版 640×640 |
| **C17** | treemap | 多类别层级占比 | `.c-treemap` + `.tm-cell` + `.tm-label` | 标准 640×480 |
| **C18** | swimlane-chart | 2-4角色并行流程 | `.c-swimlane` + `.lane` + `.lane-step` | 宽幅 640×400 |

三画幅：**宽幅** 640×400 | **标准** 640×480 | **方版** 640×640

---

## CSS变量体系

### 通用变量

```css
:root {
  --ink:#0a0a0a; --paper:#fafaf8; --accent:#002FA7; --muted:#737373; --rule:#d4d4d2;
  --surface:#ffffff; --surface-2:#f2f2f0; --good:#1aaf6c; --bad:#e0445a; --warn:#f5a524;
  --font-body:'Noto Sans SC',sans-serif; --font-data:'Inter','Noto Sans SC',sans-serif;
  --chart-1:#E69F00; --chart-2:#56B4E9; --chart-3:#009E73; --chart-4:#D55E00;
  --chart-5:#CC79A7; --chart-6:#F0E442; --chart-7:#0072B2; --chart-8:#000000;
}
```

### 麦肯锡配色

```css
:root { --paper:#F7F5F2; --accent:#0F4C81; --chart-1:#0F4C81; --chart-2:#2A7B9B; --chart-3:#3A9D8F; --chart-5:#E2A828; --good:#2f7d4a; --bad:#b53a2a; }
```

### 经济学人配色

```css
:root { --paper:#FDFBF7; --accent:#E3120B; --chart-1:#E3120B; --chart-2:#0D47A1; --chart-3:#4A7C59; --good:#1f7a3a; --bad:#9c2a25; }
```

### 财新配色

```css
:root { --paper:#F5F5F3; --accent:#0055AA; --chart-1:#0055AA; --chart-2:#3A7BBF; --chart-3:#7BAFD4; --chart-4:#C0392B; --good:#1f7a3a; --bad:#9c2a25; }
```

### 强调色块硬约束

```
🚫 禁止用近黑色做强调色块背景
✅ 强调色块必须用 --accent 品牌色做底色 + 白色文字
✅ 洞察框/关键数据卡/公式结果块 → background:var(--accent); color:var(--paper);
```

---

## 字号反比阶梯

> 越大越细，越小越粗——与guizang-ppt-skill瑞士风一致

| 字号区间 | 字重 | 典型场景 |
|---------|------|---------|
| ≥48px (num-mega) | 200 | billboard大数字、KPI主值 |
| 28-36px (num-kpi) | 200-300 | KPI卡片数字 |
| 18-24px (title) | 500 | 图表标题 |
| 13-15px (data-label) | 500 | 数据标注、图表标签 |
| 11-12px (axis/legend) | 400 | 轴刻度、图例文字 |
| 10-11px (source/meta) | 400 | 数据来源、辅助说明 |

```css
.num-mega { font-size:64px; font-weight:200; }
.num-kpi  { font-size:28px; font-weight:200; }
.title    { font-size:22px; font-weight:500; }
.data-label { font-size:13px; font-weight:500; }
.axis-label { font-size:11px; font-weight:400; }
.source     { font-size:10px; font-weight:400; }
```

---

## HTML模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root{--ink:#0a0a0a;--paper:#fafaf8;--accent:#002FA7;--muted:#737373;--rule:#d4d4d2;--surface:#ffffff;--surface-2:#f2f2f0;--good:#1aaf6c;--bad:#e0445a;--warn:#f5a524;--font-body:'Noto Sans SC',sans-serif;--font-data:'Inter','Noto Sans SC',sans-serif;--chart-1:#E69F00;--chart-2:#56B4E9;--chart-3:#009E73;--chart-4:#D55E00}
*{margin:0;padding:0;box-sizing:border-box}
.num{font-family:var(--font-data);font-feature-settings:'tnum' on;letter-spacing:-0.02em}
html,body{width:640px;overflow:hidden;font-family:var(--font-body);background:var(--paper);color:var(--ink)}
</style></head><body><!-- 图表内容 --></body></html>
```

### KPI+Sparkline组件

```html
<div class="kpi-grid"><div class="kpi-card"><div class="kpi-label">月活用户</div><div class="kpi-value num">2.4M</div><div class="kpi-delta up">+12.3%</div><svg class="sparkline" viewBox="0 0 80 24" preserveAspectRatio="none"><polyline fill="none" stroke="var(--chart-1)" stroke-width="1.5" points="0,18 10,16 20,14 30,15 40,12 50,10 60,8 70,6 80,4"/></svg></div></div>
```
```css
.kpi-grid{display:flex;gap:10px} .kpi-card{flex:1;padding:14px;background:var(--surface);border:1px solid var(--rule)} .kpi-value{font-size:28px;font-weight:200} .kpi-delta.up{color:var(--good)} .kpi-delta.down{color:var(--bad)} .sparkline{width:100%;height:24px;margin-top:6px}
```

---

## Chart Styling Rules

- 标题18-24px/500; 轴标12px/400 --muted; 数据标13px/500 .num; 来源10-11px --muted
- 数值用.num → --font-data (Inter) + tnum等宽对齐
- 卡片用--surface; 次级表面用--surface-2; 强调块用--accent+白字
- 涨--good; 跌--bad; 警告--warn
- 每张图底部必须标注数据来源
- Okabe-Ito 8色+冗余编码，单图不超4色
- 每张图表必须包含：标题+数据主体+轴标签/图例+数据来源
- 版式锁定：数据图表必须从C01-C18中选择，不允许自创版式

---

## 详细参考文件

| 文件 | 用途 |
|------|------|
| references/workflow.md | 完整4步工作流：剖析→推荐→生成→交付 |
| references/chart-system.md | 完整图表系统：18种版式+三轴决策树+8条拦截规则+色板+7种HTML骨架 |
| references/design-tokens.md | 完整设计令牌：3套财经配色详解+字号规范+间距规范+画幅弹性规则 |
