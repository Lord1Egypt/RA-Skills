---
name: vue-bigscreen-scaffold
description: 当用户要求创建 Vue3 + TypeScript 的可视化数据大屏、Dashboard 项目脚手架，或要求一键生成大屏页面（含 ECharts 图表、vue3-digital-flop 数字翻牌 KPI、axios 加载初始化 JSON、pinia 状态管理、Element Plus/Naive UI 组件库）时使用。适用：大屏/数据可视化看板项目初始化、按数据 JSON 生成大屏页面、往大屏新增图表模块。不承接单页纯 HTML 大屏（走 echart-chart skill）。
---

# Vue3 大屏脚手架

一键生成 Vue3 + TS 可视化大屏项目：**Vite + Vue3 + TS + ECharts + Axios + Pinia + Element Plus + vue3-digital-flop**。页面初始化 JSON 数据放在 `public/data/`（data 文件夹），页面经 axios 请求 `/data/*.json` 加载进 pinia。

## 使用流程

1. 定位模板：`assets/vue-bigscreen-scaffold/`（完整可运行项目，不含 node_modules/dist）。
2. 复制模板到目标目录：复制整个文件夹，跳过 `node_modules` 与 `dist`。
3. 安装依赖并启动：`npm install` → `npm run dev`（默认 http://localhost:5173）。
4. 替换数据：编辑 `public/data/*.json`（kpi/trend/product/channel/profit/region/funnel/gauge/scatter/sunburst/sankey/tree/heatmap/map/wordcloud 十五类初始化数据 + china.json 地图）。
5. 验证：`npm run build` 通过（vue-tsc 类型检查 + vite 打包）；浏览器打开页面确认 KPI 翻牌与 15 个图表渲染、控制台无 error。
6. 交付：给出项目路径、启动命令、数据结构说明。

## 目录与职责

- `public/data/`：初始化 JSON（kpi/trend/product/channel/profit/region/funnel/gauge/scatter/sunburst/sankey/tree/heatmap/map/wordcloud.json 十五类 + china.json 地图，共 16 个文件），改数据即改这里。
- `src/api/index.ts`：axios 实例，统一请求 `/data/*.json`。
- `src/theme/theme.ts`：**主题配置唯一入口**——改 background/panel/accent/chartPalette/text 任一处，整屏配色（CSS 变量 + 图表色板）全局生效；`alpha()` 用于图表渐变/分割线。
- `src/stores/dashboard.ts`：pinia store，并发加载全部初始化数据。
- `src/types/index.ts`：数据契约类型；新增 JSON 必须补类型并同步。
- `src/components/KpiCard.vue`：vue3-digital-flop 数字翻牌卡（start/end/suffix/toFixedNum 等 props）。
- `src/components/ChartPanel.vue`：ECharts 容器，自动 init / resize / dispose，接收 `title` 与 `option`。
- `src/views/BigScreen.vue`：1920×1080 等比缩放 4×4 布局；全部图表 option 在此由 store 数据组装；中国地图 geoJSON 在挂载时加载并 `registerMap('china')`。
- `src/components/DataPanel.vue`：数据面板（更新时间 + 一键刷新 store）。
- `src/components/FullscreenBtn.vue`：全屏按钮（Element Plus 图标）。

## 内置图表（15 类）

| 图表 | ECharts 类型 | 数据文件 |
| --- | --- | --- |
| 季度营收趋势 | line（面积渐变） | trend.json |
| 产品线营收占比 | pie（环形） | product.json |
| 渠道贡献 | bar（横向） | channel.json |
| 月度利润 | bar（纵向渐变） | profit.json |
| 区域销售指数 | radar | region.json |
| 销售漏斗 | funnel | funnel.json |
| 经营健康度 | gauge（仪表盘） | gauge.json |
| 月度营收-利润分布 | scatter | scatter.json |
| 产品结构 | sunburst（旭日） | sunburst.json |
| 产品流向 | sankey（桑基） | sankey.json |
| 产品结构树 | tree（树图） | tree.json |
| 产品季度营收 | heatmap（热力） | heatmap.json |
| 区域营收分布 | map（中国地图） | map.json + china.json |
| 品牌关键词热度 | wordCloud（词云，echarts-wordcloud） | wordcloud.json |
| 目标达成率 | liquidFill（水球，echarts-liquidfill） | gauge.json |

> 词云/水球为 npm 插件系列（`echarts-wordcloud`、`echarts-liquidfill`），在 `src/views/BigScreen.vue` 顶部副作用导入，`src/env.d.ts` 有类型 shim。

## 质量门

- `npm run build` 必须零类型错误（vue-tsc --noEmit）。
- 真实渲染验证：KPI 翻牌数字、15 个 canvas 图表齐全；控制台无 error（favicon 404 已用 `data:,` 图标规避）。
- 数据契约：每个 JSON 与 `src/types/index.ts` 一一对应；改 JSON 必须同步类型。
- 新增图表：复用 ChartPanel，在 BigScreen.vue 组装 option；option 可用 echart-chart skill 的 `validate_option.py` 校验。
- 校验复制结果：运行 `scripts/verify_scaffold.py <项目目录>` 检查文件与依赖完整性。

## 定制要点

- **组件库**：默认 Element Plus（main.ts 全局注册 + dark 主题）；换 Naive UI 只改 `main.ts` 注册与按需样式。
- **布局**：BigScreen.vue 的 `.grid` 四列均分 × 四行；15 图 + 数据面板占满 16 格。
- **缩放**：设计画布 1920×1080，`fit()` 按窗口等比缩放居中；全屏走浏览器 Fullscreen API。
- **npm 组件扩展**：需要新 npm 组件（如翻牌器、滚动表格、ECharts 插件）直接 `npm install` 后在对应组件引入；ECharts 插件按副作用导入（如 `import 'echarts-wordcloud'`），无类型时在 `src/env.d.ts` 补 `declare module`。

## 不承接

- 单页纯 HTML 大屏 / ECharts 单图页（走 `echart-chart` skill）。
- 后端接口联调、真实数据源鉴权接入（脚手架提供 axios 实例与 mock JSON 路径，联调由使用者配置）。
