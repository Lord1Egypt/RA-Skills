# 约定与集成说明（conventions）

## 目录与命名（与 plop-vue3-codegen 一致）

| 产物 | 路径 | 命名 |
|------|------|------|
| 选项构造器 | `src/hooks/charts/builders/<kebab>.ts` | 内部导出统一为 `ChartData/ChartConfig/buildOption` |
| 业务 hook | `src/hooks/charts/use<Pascal>Chart.ts` | `use<Pascal>Chart`，**自包含**（内置 ECharts 生命周期），导入时别名化避免冲突 |
| UI 组件 | `src/components/charts/<Pascal>Chart.vue` | Pascal + `Chart` 后缀 |

> 三者即一个图表所需的全部文件，**彼此弱耦合、不依赖任何共享 composable**。
> 可选共享件 `useECharts.ts` 默认【不】生成；如要集中治理生命周期，手动采用 `assets/use-echarts.ts`（见文末）。

- 名称同时接受 `sales-trend` / `SalesTrend` / `sales_trend`，脚本统一转换。
- 路径别名默认 `@` → `src/`。若项目用别的别名（如 `~`），改 `assets/` 与生成文件里的 `@/hooks/charts/...`。

## 项目集成

1. 安装依赖：`npm i echarts`（或 `pnpm add echarts`）。
2. 生成器只写该图表自己的 3 个文件，**绝不**注入/覆盖项目里已有的 `useECharts.ts` 或其它共享 composable。
3. 组件使用示例：
   ```vue
   <script setup lang="ts">
   import SalesTrendChart from '@/components/charts/SalesTrendChart.vue'
   const data = { categories: ['1月','2月'], series: [{ name: '销量', data: [120, 200] }] }
   </script>
   <template>
     <SalesTrendChart :data="data" :config="{ area: true }" height="320px" />
   </template>
   ```

## 体积优化（tree-shaking）

完整包约 1MB+。要瘦身：
- 用 `assets/echarts-tree-shaking.ts` 在入口注册用到的图表/组件。
- 生成的每个 `use<Pascal>Chart.ts` 顶部是 `import * as echarts from 'echarts'`，改为 `import { init } from 'echarts/core'`（并把 `echarts.init` 改成 `init`），类型用 `echarts/core` 的 `ECharts` / `ECOption`。
- builder 里 `EChartsOption` 换成 `ECOption`（从 `assets/echarts-tree-shaking.ts` 导出）。
- 新增图表类型必须同步在 `use([...])` 注册，否则图表空白。

## 想集中治理生命周期？（可选共享 composable）

默认每个图表自包含，互不干扰。若你偏好"全项目共用一份 init/resize/dispose"，可手动把 `assets/use-echarts.ts` 拷进 `src/hooks/charts/useECharts.ts`，再把对应 hook 的内联生命周期替换为：

```ts
import { useECharts } from '@/hooks/charts/useECharts'
// ...
const { setOption, resize, getInstance, isReady } = useECharts(elRef, { renderer, theme, autoResize })
function render(data) { setOption(buildOption(data, config)) }
return { render, resize, getInstance, isReady }
```

注意：这是**可选**的，且一旦采用就不要再让生成器覆盖你的 `useECharts.ts`（生成器本就不会动它）。

## 排错

- **图表空白 / 高度为 0**：容器必须有显式高度，组件 `height` 默认 `360px`，被父级 flex 压扁时给 `min-height` 或固定高。
- **切换 tab / v-show 后不显示**：`display:none` 时 init 拿到 0 尺寸，显示后调一次 `resize()`（组件已 `defineExpose({ resize })`，父组件 `ref` 拿到后调用）。
- **数据更新不生效**：`watch(props.data, ..., { deep: true })` 已内置；若数据是替换整体对象即可；大数组可改传 version 计数避免深监听开销。
- **"Component xxx is used but not imported"**：tree-shaking 模式下漏注册，见上。
- **dispose 报错**：组件卸载 `onBeforeUnmount` 已托管 dispose，不要在外部重复 dispose。
