# ECharts 选项构造器速查（Cookbook）

每个图表类型对应 `assets/builders/<type>.ts`，导出 `ChartData` / `ChartConfig` / `buildOption`。
下表列出内置类型的数据结构与可用配置项，复制改即可。

内置 15 类，按 3×5 布局组织：

| 行 | 分类 | 类型 |
|----|------|------|
| 1 | 趋势 / 分布 / 对比 | `line` `bar` `pie` `scatter` `radar` |
| 2 | 指标 / 占比 | `gauge` `kpi` `funnel` `liquidfill` `wordcloud` |
| 3 | 关系 / 结构 / 地理 | `sunburst` `sankey` `treemap` `heatmap` `map` |

其中 `liquidfill` / `wordcloud` 依赖社区插件（见下方「插件依赖」），`map` 需自行注册 geoJSON。

各类型数据结构与配置项（复制改即可）：

| type | 数据 `ChartData` | 关键 `ChartConfig` |
|------|----------------|-------------------|
| `line` | `{ categories: string[]; series: { name; data:number[] }[] }` | `smooth`, `area`, `stack`, `showLegend` |
| `bar` | 同 line | `stack`, `horizontal`, `round`, `showLegend` |
| `pie` | `{ items: { name; value:number }[] }` | `doughnut`, `roseType`, `showLegend` |
| `scatter` | `{ points: [number,number][]; name? }` | `showAxis`, `symbolSize` |
| `radar` | `{ indicator: {name;max}[]; series: {name;value:number[]}[] }` | `area`, `showLegend` |
| `gauge` | `{ value: number; name? }` | `max`, `unit` |
| `kpi` | `{ trend:number[]; value?; name?; target? }` | `area`, `color`, `showTrend` |
| `funnel` | `{ items: { name; value:number }[] }` | `sort`, `gap`, `showLegend` |
| `heatmap` | `{ xCategories:string[]; yCategories:string[]; values:[x,y,v][] }` | `min`, `max` |
| `sankey` | `{ nodes:{name}[]; links:{source;target;value}[] }` | `orient`, `showLabel` |
| `treemap` | `{ items: { name; value?; children? }[] }` | `roam`, `breadcrumb` |
| `sunburst` | `{ items: { name; value?; children? }[] }` | `radius`, `showLabel` |

> `treemap` 与 `sunburst` 数据结构**完全一致**（`{name, value?, children?}[]`），同一份层级数据可两图互切；`kpi`/`gauge` 都吃单值；`funnel`/`sankey` 都是流程/转化视角。详见下方「数据自洽」。

## 插件依赖（liquidfill / wordcloud / map）

前两类不是 echarts 内置 series，需额外安装；`map` 是内置 series 但要自备地理数据。

### 1. 安装与挂载

```bash
npm i echarts-wordcloud echarts-liquidfill
```

```ts
// 入口（main.ts 或 echarts-setup.ts）里 import 一次即可，插件内部自带注册
import 'echarts-wordcloud'
import 'echarts-liquidfill'
```

版本注意：`echarts-wordcloud` 对 echarts 版本敏感，装完若报 `series.type='wordCloud' not exists`，
检查 echarts 是否 ≥ 5；`echarts-liquidfill` 同理需 echarts ≥ 5。

### 2. map 的 geoJSON 注册（init 之前）

echarts 5 起不再内置任何地图数据。builder 提供了同名便捷函数：

```ts
import * as echarts from 'echarts'
import { registerMap, buildOption } from '@/hooks/charts/builders/china-dist'

registerMap(echarts, data)   // data.geoJson 存在时注册为 data.mapName
```

也可以在页面里直接调 `echarts.registerMap('china', geoJson)`，效果相同，只要在 `init` 前执行。

**合规提醒**：中国地图请使用自然资源部标准地图服务下载的 geoJSON，
确保国界、南海诸岛、藏南地区等要素完整；不要引入来源不明的第三方数据。

### 3. TypeScript 类型

`wordCloud` / `liquidFill` 不在 `EChartsOption` 类型里，builder 内部已对 series 做了窄化断言（`as any`），
调用方无需额外处理。若项目开了严格 lint 规则，可在对应 builder 里把断言改成
`satisfies` 或自定义 `SeriesOption` 扩展类型。

## 进阶片段（贴进对应 buildOption 即可）

### 渐变面积（line / area）
```ts
areaStyle: {
  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
    { offset: 0, color: 'rgba(64,158,255,0.4)' },
    { offset: 1, color: 'rgba(64,158,255,0.05)' },
  ]),
}
```

### 双 Y 轴
```ts
yAxis: [{ type: 'value' }, { type: 'value', position: 'right' }],
series: [
  { ...lineA, yAxisIndex: 0 },
  { ...lineB, yAxisIndex: 1 },
]
```

### 数据缩放 dataZoom（折线/柱状）
```ts
dataZoom: [{ type: 'inside' }, { type: 'slider' }],
```

### 主题色板（与 Element Plus 风格对齐）
```ts
color: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399']
```

### 坐标轴文案旋转（类目过多）
```ts
xAxis: { axisLabel: { rotate: 30, interval: 0 } }
```

### 点击系列拿数据（在组件里用 getInstance）
```ts
const { getInstance } = useXxxChart(elRef, data)
onMounted(() => {
  getInstance()?.on('click', (params) => console.log(params.data))
})
```

## 主题（theme）

组件已透传 `theme` prop（→ 业务 hook → 基础 composable 的 `init`），用户可直接指定：

1. **注册主题名**（整站统一风格）：
   ```ts
   import * as echarts from 'echarts'
   echarts.registerTheme('myTheme', { color: [...], backgroundColor: '#0b1021' })
   // 组件：<XxxChart :theme="'myTheme'" />
   ```
2. **内联主题对象**：`<XxxChart :theme="{ backgroundColor: '#fff' }" />`

注意：主题在 `init` 时生效，运行时改 `theme` 不会自动重绘；切换主题用 `:key` 强制重挂：
```vue
<XxxChart :key="theme" :theme="theme" :data="data" />
```

## 数据自洽：一份业务数据喂多种图

六个"指标/结构"类图表（kpi / gauge / funnel / sunburst / sankey / treemap / heatmap）应共享同一份业务数据，彼此印证。以"电商转化分析"为例，**所有数字同源**，只是视角不同：

```ts
// 唯一数据源（来自接口）
const stages = [
  { name: '访问', value: 10000 },
  { name: '注册', value: 6000 },
  { name: '下单', value: 3000 },
  { name: '支付', value: 2400 },
]
const trend = [320, 332, 301, 334, 390, 330, 320, 410, 420, 450, 470, 430] // 近 12 期访问
```

| 图表 | 数据派生 | 印证关系 |
|------|----------|----------|
| `kpi` | `{ value: stages[0].value, name: '总访问', trend }` | 大数字 = 漏斗顶层 |
| `gauge` | `{ value: 2400/10000*100, name: '支付转化率', unit: '%' }` | 转化率 = 末层/顶层 |
| `funnel` | `{ items: stages }` | 各层 value 即源数据 |
| `sankey` | `{ nodes: stages.map(s=>({name:s.name})), links: 相邻层 {source,target,value: 下层value} }` | 链路值 = 漏斗相邻层差值累加 |
| `sunburst` | `{ items: 嵌套层级（访问→注册→下单→支付） }` | 与 treemap 同一份层级数据 |
| `treemap` | 同 sunburst 层级数据 | 与 sunburst 完全互换 |
| `heatmap` | `{ xCategories: stages.name, yCategories:['新客','老客'], values: 各层×维度拆分 }` | 行=漏斗各层，列=维度 |
| `liquidfill` | `{ value: 2400/10000, name: '支付达成率' }` | 与 gauge 同口径（0~1 占比形式） |
| `wordcloud` | `{ words: 搜索词 × 次数 }` | 词频排序与 bar 的 TOP N 同源 |
| `map` | `{ mapName:'china', items: 各省 {name,value: 该省访问数} }` | 各省 value 之和 = 漏斗顶层 10000 |

派生示例（漏斗 → 桑基 / 旭日）：

```ts
// funnel 已是 { items: stages }
// sankey：把相邻层连成链路
const links = stages.slice(1).map((s, i) => ({
  source: stages[i].name, target: s.name, value: s.value,
}))
// sunburst / treemap：递归成层级
function toTree(arr: {name:string;value:number}[], i = 0): any {
  if (i >= arr.length) return null
  const node = { name: arr[i].name, value: arr[i].value }
  const child = toTree(arr, i + 1)
  if (child) node.children = [child]
  return node
}
const hierarchy = [toTree(stages)] // 与 treemap 传入结构一致
```

> 约定：
> - 层级类（sunburst / treemap）统一用 `{ name, value?, children? }[]`，两图可互换；
> - 流程类（funnel / sankey）统一用阶段数组，sankey 链路由相邻阶段推导；
> - 占比类（gauge / liquidfill）统一用 0~100 或 0~1 的同一口径值，kpi 展示其绝对值；
> - 分布类（bar TOP N / wordcloud / map）统一吃「维度 × 数值」，词云看体感、柱状看排序、地图看地域。
>
> 这样一份数据可在 KPI、仪表、水球、漏斗、旭日、矩形树、桑基、热力、词云、地图之间互相印证，不会出现对不上的数。

