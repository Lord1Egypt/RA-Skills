---
name: vue3-echarts-dashboard
description: "Vue3 + TypeScript + ECharts 的一体化技能，两种模式共用同一份图表资产。模式一 scaffold：一键生成可视化大屏项目（Vite + ECharts + Axios + Pinia + Naive UI，scale 等比缩放适配 1920x1080，主题可切换，初始化 JSON 放 public/data 由 Axios 拉取，数字翻牌用 vue3-digital-flop）；模式二 chart：往已有 Vue3 项目注入单个图表，产出 builder + hook + vue 三件套。触发词：大屏、可视化大屏、数据看板、dashboard scaffold、ECharts 大屏、数字翻牌、生成图表组件、封装 ECharts、做个折线图/柱状图/饼图/漏斗/热力图/桑基图/旭日图/地图/词云/水球组件。"
slug: vue3-echarts-dashboard
displayName: Vue3 ECharts 大屏与图表一体化
version: "1.0.0"
summary: 一个技能两种用法——一键生成 4x4 可视化大屏项目，或往已有 Vue3 项目注入单个 ECharts 图表；18 类图表共用同一份 builder 资产，主题可切换，数据自洽。
tags: [vue3, echarts, typescript, dashboard, 大屏, 数据可视化, vite, pinia]
license: MIT
agent_created: true
---

# Vue3 + TS ECharts 一体化技能（大屏脚手架 + 单图表注入）

## Overview

一个技能、两种用法，**共用同一份图表资产** `assets/builders/`——不存在第二份图表模板：

| 模式 | 用途 | 命令要点 |
|------|------|----------|
| `scaffold`（默认） | 从零起一个完整可视化大屏项目 | `node generate.mjs <dir> --theme tech-green` |
| `chart` | 往已有 Vue3 项目注入单个图表 | `node generate.mjs <项目根> --mode chart --name sales-trend --type line` |

两种模式产出的图表都是**同一套三件套**，结构、命名、生命周期完全一致：

```
src/hooks/charts/builders/<kebab>.ts      # 选项构造器：纯函数 buildOption(data, config)
src/hooks/charts/use<Pascal>Chart.ts      # 业务 hook：托管 init / setOption / resize / dispose
src/components/charts/<Pascal>Chart.vue   # UI 组件：props 接 data/config/height/theme
```

自包含、弱耦合：每个图表只依赖自己的 hook + builder，放进任意 Vue3 项目即可用，不注入/不覆盖任何共享 `useECharts.ts`（可选共享件见 `assets/use-echarts.ts`）。

## 决策：用哪个模式

- 用户要「一个页面 / 一个项目 / 大屏 / 看板」→ `scaffold`
- 用户要「加一个图表 / 封装个折线图 / 做个饼图组件」→ `chart`
- 判不出来就问，别猜。

---

## 模式 A：scaffold（一键起大屏）

```bash
node "<skill>/scripts/generate.mjs" ./my-screen
node "<skill>/scripts/generate.mjs" ./my-screen --theme tech-green --install
node "<skill>/scripts/generate.mjs" ./my-screen --charts trend:line,device:pie,region:map --no-kpi
node "<skill>/scripts/generate.mjs" ./my-screen --dry-run     # 只看计划不落盘
```

`<skill>` 即本技能目录 `C:/Users/李玉明/.workbuddy/skills/vue3-echarts-dashboard`。

| 参数 | 说明 | 缺省 |
|------|------|------|
| `--mode` | `scaffold` / `chart` | `scaffold` |
| `--theme` | `tech-blue` / `tech-green` / `tech-purple` | `tech-blue` |
| `--charts` | `name:type[:title],...`，自定义要哪些图表 | 内置 15 类 |
| `--no-kpi` | 不生成数字翻牌 KPI 格 | 含 KPI |
| `--install` | 生成后自动 `npm install` | 不装 |
| `--force` | 目标已存在时覆盖 | 否 |
| `--dry-run` | 只打印计划 | 否 |

### 产出结构

```
my-screen/
├── public/
│   ├── data/*.json        # 页面初始化数据（Axios 拉取，16 份）
│   └── geo/china.json     # 中国省级边界（离线渲染，合规）
└── src/
    ├── main.ts            # 注册 pinia / naive-ui / vue3-digital-flop / 应用主题
    ├── App.vue            # scale 等比缩放容器
    ├── theme/index.ts     # 主题（CSS 变量 + echarts.registerTheme('dashboard')）
    ├── api/               # axios 实例 + 接口 + 类型
    ├── stores/dashboard.ts# Pinia 数据中心（并发拉全部 JSON）
    ├── composables/useScreenScale.ts
    ├── components/        # ScreenHeader / PanelBox / DigitalFlop / Ranking
    ├── hooks/charts/      # builders/ + use<Name>Chart.ts
    └── views/Dashboard.vue
```

### 布局与默认图表

4 列网格，行数按图表数推导（`ceil((图表数 + KPI) / 4)`）。默认 **4×4 = 16 格**：第 1 格 KPI 数字翻牌，其余 15 格图表。

| # | 组件 | 类型 | # | 组件 | 类型 |
|---|------|------|---|------|------|
| 1 | Trend | line | 9 | FlowSankey | sankey |
| 2 | Category | category-bar | 10 | SourceTree | tree |
| 3 | Monthly | bar | 11 | SourceSunburst | sunburst |
| 4 | Device | pie | 12 | Region | map |
| 5 | Ability | radar | 13 | HotWord | wordcloud |
| 6 | Conversion | funnel | 14 | Completion | liquidfill |
| 7 | Target | gauge | 15 | Ranking | ranking（非 ECharts） |
| 8 | ActiveHeat | heatmap | | | |

### 数据自洽

统一流量口径 **14000**，各图互相印证，改数据时别破坏这个关系：

- 渠道合计（category）= 桑基「访问」节点 = 漏斗「访问」= 树/旭日根值 = **地图省份合计**
- 漏斗 14000 → 10080 → 6020 → 3640 → **2772**，与桑基逐段流转及各流失边完全对齐
- 水球 `0.786` = 仪表盘 `78.6`（年度目标完成率）
- 词云与排行榜共用同一批热门页面数据

---

## 模式 B：chart（往已有项目注入单个图表）

```bash
python "<skill>/scripts/generate_chart.py" --target <项目根> --name sales-trend --type line
node    "<skill>/scripts/generate.mjs"      <项目根> --mode chart --name sales-trend --type line
node    "<skill>/scripts/generate.mjs"      <项目根> --mode chart --name my-pie --type pie --force
```

两条命令产出一致（`.mjs` 是主脚本，`.py` 是同逻辑的离线兜底）。名称接受 `sales-trend` / `SalesTrend` / `sales_trend`，脚本统一转 Pascal / kebab。

**参数**：`--name`（必填）、`--type`（默认 `line`）、`--dry-run`、`--force`。

产出 3 个文件后，在用到的地方：

```vue
<SalesTrendChart :data="chartData" :config="{ area: true }" height="360px" />
```

### 可用类型（18 类）

| 分组 | 类型 |
|------|------|
| 趋势 / 分布 | `line` `bar` `category-bar` `pie` `scatter` |
| 指标 / 占比 | `radar` `gauge` `kpi` `funnel` `liquidfill` |
| 关系 / 结构 | `sunburst` `sankey` `tree` `treemap` `heatmap` |
| 其他 | `map` `wordcloud` `ranking` `custom`（TODO 模板） |

每个类型的 `ChartData` 与 `public/data/*.json` 的结构**一一对应**（含 `title`），所以大屏数据可直接复用，无需适配层。

---

## 主题系统（两模式通用）

- **CSS 变量**：`applyTheme()` 写入 `--c-primary` / `--c-primary2` / `--c-text` / `--c-accent` / `--c-axis`，组件样式用 `color-mix(in srgb, var(--c-primary) N%, transparent)`。
- **ECharts 主题**：`echarts.registerTheme('dashboard', …)`，大屏模式下 hook 默认 `theme: 'dashboard'`。
- **builder 调色板**：hook 里的 `BASE_CONFIG` 由生成器按主题注入 `{ colors: [...], primary: '...' }`（热力/地图注入 5 色渐变带）。用户传入的 `config` 优先级更高。
- 扩展主题：在 `src/theme/index.ts` 的 `themes` 里加一条，并把调色板同步到 `scripts/generate.mjs` 的 `THEMES`。

## 常见定制

- **加图表**：`node generate.mjs <项目根> --mode chart --name <名> --type <类型>`，再在 `Dashboard.vue` 里放进一个 `.cell`。
- **换布局**：改 `views/Dashboard.vue` 里 `.dashboard__body` 的 `grid-template-columns` 与 `gridTemplateRows`。
- **接后端**：`src/api/index.ts` 里把 `/data/*.json` 换成真实接口，`ChartData` 结构保持不变即可。
- **去掉地图**：删 `public/geo/`、`RegionChart.vue`、`hooks/charts/useRegionChart.ts`、`builders/region.ts` 及 store/api 中 `map` 相关引用，省约 570KB。
- **体积优化**：参考 `assets/echarts-tree-shaking.ts` 改按需引入。

## 注意事项

- **插件型图表**必须装依赖，hook 已在顶部自动 `import`：`wordcloud` → `npm i echarts-wordcloud`；`liquidfill` → `npm i echarts-liquidfill`。
- **地图合规**：`map` 用 ECharts 内置 map + **本地 geoJSON**（DataV 中国省级边界，含台湾省、港澳及南海诸岛），不接在线瓦片服务、不含密钥；hook 内先 `registerMap` 再 `init`。替换 geoJSON 时必须用自然资源部标准地图。
- `vue3-digital-flop` 的 `start` 只在首次加载生效，本模板用 `end` 绑定指标值，初始化播放一次动画。
- `build` 脚本仅 `vite build`（不跑 `vue-tsc`），避免全局注册的组件触发模板类型报错；需要类型检查用 `npm run type-check`。
- 约定与 `plop-vue3-codegen` 对齐：kebab 目录、Pascal 组件、camel hook，`@` → `src`。
