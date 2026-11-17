<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import 'echarts-wordcloud'
import 'echarts-liquidfill'
import KpiCard from '@/components/KpiCard.vue'
import ChartPanel from '@/components/ChartPanel.vue'
import FullscreenBtn from '@/components/FullscreenBtn.vue'
import DataPanel from '@/components/DataPanel.vue'
import { useDashboardStore } from '@/stores/dashboard'
import { alpha, theme } from '@/theme'

const store = useDashboardStore()
const {
  kpis, trend, product, channel, profit, region,
  funnel, gauge, scatter, sunburst, sankey, tree, heatmap, map, wordcloud,
  loading, error,
} = storeToRefs(store)

const stageRef = ref<HTMLElement | null>(null)

/** 1920×1080 设计画布等比缩放居中 */
function fit() {
  const el = stageRef.value
  if (!el) return
  const s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080)
  el.style.transform = `scale(${s})`
  el.style.marginLeft = `${Math.round((window.innerWidth - 1920 * s) / 2)}px`
  el.style.marginTop = `${Math.round((window.innerHeight - 1080 * s) / 2)}px`
}

// ---- 中国地图 geoJSON：本地 public/data/china.json，加载后注册 ----
const geoReady = ref(false)
const geoError = ref('')
async function loadGeo() {
  try {
    const geo = await fetch('/data/china.json').then((r) => r.json())
    echarts.registerMap('china', geo as never)
    geoReady.value = true
  } catch {
    geoError.value = '地图数据加载失败'
  }
}

onMounted(() => {
  store.loadAll()
  void loadGeo()
  fit()
  window.addEventListener('resize', fit)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', fit)
})

// ---- 主题驱动的通用样式（坐标轴 / 分割线 / 文本） ----
const AXIS = {
  axisLine: { lineStyle: { color: theme.panel.border } },
  axisLabel: { color: theme.text.secondary },
  nameTextStyle: { color: theme.text.secondary },
  splitLine: { lineStyle: { color: alpha(theme.panel.border, 0.55) } },
} as const

// ---- 各图表 option：由 store 数据推导（纯 ECharts option） ----

const trendOption = computed<EChartsOption>(() => {
  const d = trend.value
  return {
    tooltip: {
      trigger: 'axis',
      valueFormatter: (v: unknown) => `${String(v)} ${d?.unit ?? ''}`,
    },
    grid: { left: 64, right: 24, top: 32, bottom: 40 },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: d?.categories ?? [],
      axisLine: AXIS.axisLine,
      axisLabel: AXIS.axisLabel,
    },
    yAxis: {
      type: 'value',
      name: d?.unit ?? '',
      nameTextStyle: AXIS.nameTextStyle,
      axisLabel: AXIS.axisLabel,
      splitLine: AXIS.splitLine,
    },
    series: [
      {
        type: 'line',
        name: d?.name ?? '',
        smooth: true,
        symbolSize: 8,
        lineStyle: { width: 3, color: theme.accent },
        itemStyle: { color: theme.accent },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: alpha(theme.accent, 0.35) },
              { offset: 1, color: alpha(theme.accent, 0.02) },
            ],
          },
        },
        label: { show: true, position: 'top', color: theme.text.primary, formatter: '{c}' },
        data: d?.values ?? [],
      },
    ],
  }
})

const productOption = computed<EChartsOption>(() => {
  const d = product.value
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ' + (d?.unit ?? '') + ' ({d}%)',
    },
    legend: { bottom: 0, type: 'scroll', textStyle: { color: theme.text.secondary, fontSize: 11 } },
    series: [
      {
        type: 'pie',
        radius: ['32%', '52%'],
        center: ['50%', '47%'],
        avoidLabelOverlap: true,
        minAngle: 5,
        itemStyle: { borderColor: theme.background.mid, borderWidth: 2 },
        label: { color: theme.text.primary, fontSize: 11, formatter: '{b} {d}%' },
        labelLine: { lineStyle: { color: alpha(theme.text.secondary, 0.6) } },
        data: d?.items ?? [],
      },
    ],
    color: theme.chartPalette,
  }
})

const channelOption = computed<EChartsOption>(() => {
  const d = channel.value
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      valueFormatter: (v: unknown) => `${String(v)} ${d?.unit ?? ''}`,
    },
    grid: { left: 70, right: 36, top: 16, bottom: 26 },
    xAxis: {
      type: 'value',
      name: d?.unit ?? '',
      nameTextStyle: AXIS.nameTextStyle,
      axisLabel: AXIS.axisLabel,
      splitLine: AXIS.splitLine,
    },
    yAxis: {
      type: 'category',
      data: d?.categories ?? [],
      axisLabel: AXIS.axisLabel,
      axisLine: AXIS.axisLine,
    },
    series: [
      {
        type: 'bar',
        name: d?.name ?? '',
        barWidth: 11,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 1,
            y2: 0,
            colorStops: [
              { offset: 0, color: theme.chartPalette[1] ?? theme.accent },
              { offset: 1, color: theme.chartPalette[0] ?? theme.accent },
            ],
          },
          borderRadius: [0, 4, 4, 0],
        },
        label: { show: true, position: 'right', color: theme.text.primary, fontSize: 11 },
        data: d?.values ?? [],
      },
    ],
  }
})

const profitOption = computed<EChartsOption>(() => {
  const d = profit.value
  const green = theme.chartPalette[3] ?? '#34c77b'
  return {
    tooltip: {
      trigger: 'axis',
      valueFormatter: (v: unknown) => `${String(v)} ${d?.unit ?? ''}`,
    },
    grid: { left: 56, right: 16, top: 22, bottom: 28 },
    xAxis: {
      type: 'category',
      data: d?.categories ?? [],
      axisLabel: AXIS.axisLabel,
      axisLine: AXIS.axisLine,
    },
    yAxis: {
      type: 'value',
      name: d?.unit ?? '',
      nameTextStyle: AXIS.nameTextStyle,
      axisLabel: AXIS.axisLabel,
      splitLine: AXIS.splitLine,
    },
    series: [
      {
        type: 'bar',
        name: d?.name ?? '',
        barWidth: 12,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: green },
              { offset: 1, color: alpha(green, 0.25) },
            ],
          },
          borderRadius: [4, 4, 0, 0],
        },
        label: { show: true, position: 'top', color: theme.text.primary, fontSize: 11 },
        data: d?.values ?? [],
      },
    ],
  }
})

const regionOption = computed<EChartsOption>(() => {
  const d = region.value
  const orange = theme.chartPalette[2] ?? '#ff9f43'
  return {
    tooltip: { trigger: 'item' },
    radar: {
      indicator: d?.indicators ?? [],
      radius: '52%',
      axisName: { color: theme.text.secondary, fontSize: 11 },
      axisLine: { lineStyle: { color: alpha(theme.panel.border, 0.6) } },
      splitLine: { lineStyle: { color: alpha(theme.panel.border, 0.6) } },
      splitArea: {
        areaStyle: {
          color: [alpha(theme.panel.border, 0.15), alpha(theme.panel.border, 0.05)],
        },
      },
    },
    series: [
      {
        type: 'radar',
        symbolSize: 4,
        lineStyle: { color: orange, width: 2 },
        itemStyle: { color: orange },
        areaStyle: { color: alpha(orange, 0.25) },
        data: [{ value: d?.values ?? [], name: d?.name ?? '' }],
      },
    ],
  }
})

const funnelOption = computed<EChartsOption>(() => {
  const d = funnel.value
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ' + (d?.unit ?? '') + ' ({d}%)',
    },
    series: [
      {
        type: 'funnel',
        sort: 'descending',
        gap: 2,
        left: 8,
        right: 26,
        top: 8,
        bottom: 8,
        label: {
          show: true,
          position: 'inside',
          color: theme.text.primary,
          fontSize: 11,
          formatter: '{b} {c}',
        },
        labelLine: { show: false },
        itemStyle: { borderColor: theme.background.mid, borderWidth: 1 },
        data: d?.items ?? [],
      },
    ],
    color: theme.chartPalette,
  }
})

const gaugeOption = computed<EChartsOption>(() => {
  const d = gauge.value
  return {
    series: [
      {
        type: 'gauge',
        startAngle: 210,
        endAngle: -30,
        min: 0,
        max: d?.max ?? 100,
        progress: { show: true, width: 11, itemStyle: { color: theme.accent } },
        axisLine: {
          lineStyle: { width: 11, color: [[1, alpha(theme.panel.border, 0.5)]] },
        },
        axisTick: { show: false },
        splitLine: { length: 6, lineStyle: { color: alpha(theme.text.secondary, 0.4) } },
        axisLabel: { color: theme.text.secondary, distance: 9, fontSize: 9 },
        pointer: { width: 3, itemStyle: { color: theme.accent } },
        anchor: { show: true, size: 8, itemStyle: { color: theme.accent } },
        title: { color: theme.text.secondary, offsetCenter: [0, '58%'], fontSize: 11 },
        detail: {
          valueAnimation: true,
          color: theme.text.primary,
          fontSize: 20,
          offsetCenter: [0, '32%'],
          formatter: '{value}' + (d?.unit ?? ''),
        },
        data: [{ value: d?.value ?? 0, name: d?.name ?? '' }],
      },
    ],
  }
})

const scatterOption = computed<EChartsOption>(() => {
  const d = scatter.value
  return {
    tooltip: {
      trigger: 'item',
      formatter: (p: unknown) => {
        const v = (p as { value: number[] }).value ?? []
        return `${d?.xName ?? 'x'}: ${v[0]}<br/>${d?.yName ?? 'y'}: ${v[1]}`
      },
    },
    grid: { left: 64, right: 30, top: 22, bottom: 30 },
    xAxis: {
      type: 'value',
      name: d?.xName ?? '',
      nameGap: 6,
      nameTextStyle: AXIS.nameTextStyle,
      axisLabel: AXIS.axisLabel,
      splitLine: AXIS.splitLine,
    },
    yAxis: {
      type: 'value',
      name: d?.yName ?? '',
      nameTextStyle: AXIS.nameTextStyle,
      axisLabel: AXIS.axisLabel,
      splitLine: AXIS.splitLine,
    },
    series: [
      {
        type: 'scatter',
        name: d?.name ?? '',
        symbolSize: 9,
        itemStyle: { color: theme.chartPalette[0] ?? theme.accent },
        data: (d?.points ?? []).map((p) => [p.x, p.y]),
      },
    ],
  }
})

const sunburstOption = computed<EChartsOption>(() => {
  const d = sunburst.value
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ' + (d?.unit ?? '') + ' ({d}%)',
    },
    series: [
      {
        type: 'sunburst',
        radius: ['10%', '80%'],
        data: d?.items ?? [],
        itemStyle: { borderColor: theme.background.mid, borderWidth: 2 },
        label: { color: theme.text.primary, fontSize: 10 },
        emphasis: { focus: 'ancestor' },
      },
    ],
    color: theme.chartPalette,
  }
})

const sankeyOption = computed<EChartsOption>(() => {
  const d = sankey.value
  return {
    tooltip: { trigger: 'item', triggerOn: 'mousemove' },
    series: [
      {
        type: 'sankey',
        data: d?.nodes ?? [],
        links: d?.links ?? [],
        left: 8,
        right: 60,
        top: 8,
        bottom: 8,
        nodeWidth: 9,
        nodeGap: 9,
        label: { color: theme.text.secondary, fontSize: 11 },
        lineStyle: { color: 'gradient', curveness: 0.5, opacity: 0.35 },
        itemStyle: { borderColor: theme.background.mid, borderWidth: 1 },
        emphasis: { focus: 'adjacency' },
      },
    ],
    color: theme.chartPalette,
  }
})

const treeOption = computed<EChartsOption>(() => {
  const d = tree.value
  return {
    tooltip: { trigger: 'item', triggerOn: 'mousemove' },
    series: [
      {
        type: 'tree',
        data: d?.items ? [d.items] : [],
        orient: 'horizontal',
        left: 8,
        right: 84,
        top: 10,
        bottom: 10,
        symbol: 'circle',
        symbolSize: 6,
        initialTreeDepth: 2,
        label: {
          position: 'left',
          verticalAlign: 'middle',
          align: 'right',
          color: theme.text.secondary,
          fontSize: 11,
        },
        leaves: {
          label: { position: 'right', verticalAlign: 'middle', align: 'left', color: theme.text.primary },
        },
        lineStyle: { color: theme.panel.border, width: 1 },
        itemStyle: { color: theme.accent },
        emphasis: { focus: 'descendant' },
        expandAndCollapse: true,
      },
    ],
  }
})

const heatmapOption = computed<EChartsOption>(() => {
  const d = heatmap.value
  const vals = (d?.values ?? []).map((v) => v.value)
  const hmin = vals.length ? Math.min(...vals) : 0
  const hmax = vals.length ? Math.max(...vals) : 1
  return {
    tooltip: { position: 'top', formatter: '{b}: {c} ' + (d?.unit ?? '') },
    grid: { left: 56, right: 20, top: 22, bottom: 40 },
    xAxis: {
      type: 'category',
      data: d?.categories ?? [],
      splitArea: { show: true },
      axisLine: AXIS.axisLine,
      axisLabel: AXIS.axisLabel,
    },
    yAxis: {
      type: 'category',
      data: d?.series ?? [],
      splitArea: { show: true },
      axisLine: AXIS.axisLine,
      axisLabel: AXIS.axisLabel,
    },
    visualMap: {
      min: hmin,
      max: hmax,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      itemWidth: 10,
      itemHeight: 60,
      textStyle: { color: theme.text.secondary, fontSize: 10 },
      inRange: { color: [alpha(theme.background.mid, 0.75), theme.accent] },
    },
    series: [
      {
        type: 'heatmap',
        data: (d?.values ?? []).map((v) => [v.x, v.y, v.value]),
        label: { show: true, color: theme.text.primary, fontSize: 10 },
        itemStyle: { borderColor: theme.background.mid, borderWidth: 1 },
        emphasis: { itemStyle: { shadowBlur: 6, shadowColor: 'rgba(0,0,0,0.4)' } },
      },
    ],
  }
})

const mapOption = computed<EChartsOption>(() => {
  if (!geoReady.value) {
    return {
      title: {
        text: geoError.value || '地图加载中…',
        left: 'center',
        top: 'middle',
        textStyle: { color: theme.text.secondary, fontSize: 12, fontWeight: 'normal' },
      },
    }
  }
  const d = map.value
  const vals = (d?.items ?? []).map((i) => i.value)
  const vmin = vals.length ? Math.min(...vals) : 0
  const vmax = vals.length ? Math.max(...vals) : 1
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c} ' + (d?.unit ?? '') },
    visualMap: {
      min: vmin,
      max: vmax,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      itemWidth: 10,
      itemHeight: 60,
      textStyle: { color: theme.text.secondary, fontSize: 10 },
      inRange: { color: [alpha(theme.background.mid, 0.6), theme.accent] },
    },
    series: [
      {
        type: 'map',
        map: 'china',
        roam: false,
        zoom: 1.15,
        label: { show: false },
        itemStyle: { borderColor: alpha(theme.background.mid, 0.9), borderWidth: 1 },
        emphasis: {
          label: { show: true, color: theme.text.primary, fontSize: 10 },
          itemStyle: { areaColor: theme.chartPalette[2] ?? theme.accent },
        },
        data: d?.items ?? [],
      },
    ],
  }
})

const wordcloudOption = computed<EChartsOption>(() => {
  const d = wordcloud.value
  return {
    tooltip: { show: true, formatter: '{b}: {c}' },
    series: [
      {
        type: 'wordCloud',
        shape: 'circle',
        gridSize: 8,
        sizeRange: [12, 32],
        rotationRange: [0, 0],
        width: '100%',
        height: '100%',
        textStyle: { fontFamily: 'Microsoft YaHei' },
        data: (d?.items ?? []).map((i, idx) => ({
          name: i.name,
          value: i.value,
          itemStyle: {
            color: theme.chartPalette[idx % theme.chartPalette.length] ?? theme.accent,
          },
        })),
      },
    ],
  } as EChartsOption
})

const liquidOption = computed<EChartsOption>(() => {
  const d = gauge.value
  const ratio = d?.max ? d.value / d.max : 0
  return {
    series: [
      {
        type: 'liquidFill',
        data: [ratio],
        radius: '70%',
        center: ['50%', '54%'],
        color: [alpha(theme.accent, 0.7)],
        backgroundStyle: { color: alpha(theme.panel.border, 0.25) },
        outline: {
          show: true,
          borderDistance: 6,
          itemStyle: { borderColor: alpha(theme.accent, 0.7), borderWidth: 2 },
        },
        label: {
          show: true,
          color: theme.text.primary,
          fontSize: 22,
          formatter: `${(ratio * 100).toFixed(0)}%`,
        },
      },
    ],
  } as EChartsOption
})
</script>

<template>
  <div ref="stageRef" class="stage">
    <div class="header">
      <h1>经营数据可视化大屏</h1>
      <div class="sub">示例数据（演示用）· 2025 年度 · Vue3 + TS + ECharts + Pinia</div>
      <div class="accent"></div>
      <FullscreenBtn />
    </div>

    <div v-if="loading && !kpis.length" class="loading">数据加载中…</div>
    <div v-else-if="error" class="loading">加载失败：{{ error }}</div>

    <template v-else>
      <div class="kpi-row">
        <KpiCard v-for="k in kpis" :key="k.label" :item="k" />
      </div>

      <div class="grid">
        <div class="col">
          <ChartPanel title="产品线营收占比" :option="productOption" />
          <ChartPanel title="渠道贡献（万元）" :option="channelOption" />
          <ChartPanel title="销售漏斗（人）" :option="funnelOption" />
          <ChartPanel title="产品流向（人）" :option="sankeyOption" />
        </div>
        <div class="col">
          <ChartPanel title="2025 年季度营收趋势（万元）" :option="trendOption" />
          <ChartPanel title="经营健康度" :option="gaugeOption" />
          <ChartPanel title="月度利润（万元）" :option="profitOption" />
          <ChartPanel title="产品结构树（万元）" :option="treeOption" />
        </div>
        <div class="col">
          <ChartPanel title="区域销售指数" :option="regionOption" />
          <ChartPanel title="产品结构（万元）" :option="sunburstOption" />
          <ChartPanel title="月度营收-利润分布（万元）" :option="scatterOption" />
          <ChartPanel title="产品季度营收热力（万元）" :option="heatmapOption" />
        </div>
        <div class="col">
          <ChartPanel title="区域营收分布（万元）" :option="mapOption" />
          <ChartPanel title="品牌关键词热度" :option="wordcloudOption" />
          <ChartPanel title="目标达成率" :option="liquidOption" />
          <DataPanel />
        </div>
      </div>
    </template>

    <div class="footer">
      数据口径：单位 万元；初始化 JSON 位于 public/data/，通过 axios 加载进 Pinia。
    </div>
  </div>
</template>

<style scoped>
.loading {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 18px;
}
</style>
