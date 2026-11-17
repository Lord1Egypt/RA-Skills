# Vue3 可视化大屏脚手架

技术栈：**Vue 3 + TypeScript + Vite + ECharts + Axios + Pinia + Element Plus + vue3-digital-flop**

## 快速开始

```bash
npm install
npm run dev        # 开发预览 http://localhost:5173
npm run build      # 类型检查 + 生产构建
npm run preview    # 预览构建产物
```

## 目录结构

```
├── public/
│   └── data/                  # 页面初始化 JSON 数据（data 文件夹）
│       ├── kpi.json           # KPI 数字翻牌卡
│       ├── trend.json         # 季度营收趋势（折线/面积图）
│       ├── product.json       # 产品线占比（环形图）
│       ├── channel.json       # 渠道贡献（条形图）
│       ├── profit.json        # 月度利润（柱状图）
│       ├── region.json        # 区域销售指数（雷达图）
│       ├── funnel.json        # 销售漏斗（漏斗图）
│       ├── gauge.json         # 经营健康度（仪表盘）
│       ├── scatter.json       # 月度营收-利润分布（散点图）
│       ├── sunburst.json      # 产品结构（旭日图）
│       ├── sankey.json        # 产品流向（桑基图）
│       ├── tree.json          # 产品结构树（树图）
│       ├── heatmap.json       # 产品季度营收（热力图）
│       ├── map.json           # 区域营收分布（中国地图）
│       ├── wordcloud.json     # 品牌关键词热度（词云）
│       └── china.json         # 中国地图 geoJSON（DataV 数据）
└── src/
    ├── api/index.ts           # axios 实例 + 数据请求（/data/*.json）
    ├── stores/dashboard.ts    # Pinia store：并发加载全部初始化数据
    ├── types/index.ts         # 数据契约类型
    ├── theme/
    │   ├── theme.ts           # 主题配置：改这里即可全局换肤
    │   └── index.ts           # 主题导出
    ├── components/
    │   ├── KpiCard.vue        # 数字翻牌卡（vue3-digital-flop）
    │   ├── ChartPanel.vue     # ECharts 图表容器（自动 init/resize/dispose）
    │   ├── DataPanel.vue      # 数据面板（更新时间 + 刷新）
    │   └── FullscreenBtn.vue  # 全屏按钮（Element Plus）
    └── views/BigScreen.vue    # 大屏页面（1920×1080 等比缩放 + 4×4 布局）
```

## 内置图表（15 类）

| 图表 | 类型 | 数据文件 |
| --- | --- | --- |
| 季度营收趋势 | 折线/面积 | trend.json |
| 产品线营收占比 | 环形图 | product.json |
| 渠道贡献 | 条形图（横向） | channel.json |
| 月度利润 | 柱状图 | profit.json |
| 区域销售指数 | 雷达图 | region.json |
| 销售漏斗 | 漏斗图 | funnel.json |
| 经营健康度 | 仪表盘 | gauge.json |
| 月度营收-利润分布 | 散点图 | scatter.json |
| 产品结构 | 旭日图 | sunburst.json |
| 产品流向 | 桑基图 | sankey.json |
| 产品结构树 | 树图 | tree.json |
| 产品季度营收 | 热力图 | heatmap.json |
| 区域营收分布 | 地图 | map.json + china.json |
| 品牌关键词热度 | 词云（echarts-wordcloud） | wordcloud.json |
| 目标达成率 | 水球图（echarts-liquidfill） | gauge.json |

> 插件型图表依赖 npm 包：`echarts-wordcloud`、`echarts-liquidfill`（已在 package.json）。

## 自定义

1. **换数据**：直接改 `public/data/*.json`（页面经 axios 加载，改完刷新即生效）。
2. **换主题**：改 `src/theme/theme.ts`（背景/面板/强调色/图表色板），整屏配色自动跟随。
3. **换图表**：在 `src/views/BigScreen.vue` 中调整各 `computed` 的 ECharts option，或复用 `ChartPanel` 增加面板；新增 JSON 需同步 `src/types/index.ts` 契约与 `stores/dashboard.ts`。
4. **换组件库**：Element Plus 可替换为 Naive UI，在 `main.ts` 改注册即可。

## 说明

- 设计画布固定 1920×1080，页面按窗口等比缩放居中；全屏按钮调用浏览器全屏 API。
- 示例数据均为演示值，生产使用请替换为真实数据。
