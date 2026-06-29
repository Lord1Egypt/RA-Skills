---
theme: default
title: 城市运营监控大屏
info: Slidev × DataV (datav-vue3) large-screen dashboard example
canvasWidth: 1920          # design at 1920px wide …
aspectRatio: '16/9'        # … → 1080px tall; Slidev fits this to any screen
fonts:
  sans: Noto Sans SC       # CJK-capable; Rajdhani/Orbitron loaded via dashboard.css for numbers
  weights: '400,600,700'
class: text-left
---

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

// DataV draws to canvas/SVG and can't read CSS vars — mirror the palette here as literal colors.
const palette = {
  primary: '#00baff', secondary: '#3de7c9', accent: '#f7b500',
  success: '#2ed47a', warning: '#ffb02e', danger: '#ff5b5b',
  text: '#c9e0ff', dim: '#7fa6cc',
  series: ['#00baff', '#3de7c9', '#f7b500', '#fb7293', '#9b8bff', '#2ed47a'],
}

// SSR-safe gate: render DataV only after mount (keeps `slidev build`/`export` from blanking).
const mounted = ref(false)
const now = ref('')
const thousands = (n: number) => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')

// ---- KPI digital flops (top row) ----
const kpis = reactive([
  { label: '今日客流(人次)', config: { number: [128430], content: '{nt}', formatter: thousands, style: { fontSize: 40, fill: palette.primary } } },
  { label: '在线设备',       config: { number: [1864],   content: '{nt}', style: { fontSize: 40, fill: palette.secondary } } },
  { label: '告警事件',       config: { number: [37],     content: '{nt}', style: { fontSize: 40, fill: palette.danger } } },
  { label: '能耗(kWh)',      config: { number: [95620],  content: '{nt}', formatter: thousands, style: { fontSize: 40, fill: palette.accent } } },
  { label: '满意度(%)',      config: { number: [96.4],   content: '{nt}', toFixed: 1, style: { fontSize: 40, fill: palette.success } } },
])

// ---- Left: ranking + capsule ----
const ranking = reactive({
  data: [
    { name: '城东片区', value: 167 }, { name: '高新区', value: 142 }, { name: '老城中心', value: 121 },
    { name: '滨江新城', value: 98 }, { name: '空港物流', value: 86 }, { name: '大学城', value: 72 },
    { name: '工业园', value: 65 },
  ],
  unit: '万人次', color: palette.primary, textColor: palette.text,
})
const capsule = reactive({
  data: [
    { name: '公交', value: 167 }, { name: '地铁', value: 233 }, { name: '出租', value: 98 },
    { name: '共享单车', value: 145 }, { name: '步行', value: 75 },
  ],
  colors: palette.series, unit: '万', showValue: true, textColor: palette.dim,
})

// ---- Center: trend (line+bar) + conical ranking ----
const trend = reactive({
  legend: { data: ['进城', '出城'], textStyle: { fill: palette.text } },
  xAxis: {
    name: '时', data: ['00', '03', '06', '09', '12', '15', '18', '21'],
    axisLine: { style: { stroke: '#2b4a6b' } }, axisLabel: { style: { fill: palette.dim } },
  },
  yAxis: {
    name: '车流(千)', data: 'value',
    axisLine: { style: { stroke: '#2b4a6b' } }, axisLabel: { style: { fill: palette.dim } },
    splitLine: { show: true, style: { stroke: '#16314e' } },
  },
  series: [
    { name: '进城', type: 'line', data: [12, 8, 26, 64, 48, 52, 78, 40], smooth: true,
      lineArea: { show: true, gradient: ['rgba(0,186,255,.45)', 'rgba(0,186,255,0)'] },
      lineStyle: { stroke: palette.primary } },
    { name: '出城', type: 'bar', data: [6, 5, 14, 30, 52, 38, 70, 55],
      gradient: { color: ['#3de7c9', '#1d9c87'] } },
  ],
})
const conical = reactive({
  data: [
    { name: '城东', value: 167 }, { name: '高新', value: 142 }, { name: '滨江', value: 121 },
    { name: '空港', value: 98 }, { name: '老城', value: 86 }, { name: '大学城', value: 72 },
  ],
  columnColor: 'rgba(0,194,255,0.45)', textColor: palette.text, showValue: true,
})

// ---- Right: ring + water + percent + scroll board ----
const ring = reactive({
  lineWidth: 22,
  data: [
    { name: '运行', value: 1680 }, { name: '待机', value: 120 },
    { name: '离线', value: 64 },
  ],
  color: [palette.primary, palette.secondary, palette.dim],
  digitalFlopStyle: { fontSize: 22, fill: palette.secondary },
  digitalFlopUnit: '台',
})
const water = reactive({ data: [68], shape: 'roundRect', colors: [palette.primary, palette.secondary] })
const percent = reactive({ value: 82, colors: [palette.secondary, palette.primary] })
const board = reactive({
  header: ['时间', '区域', '事件', '级别'],
  data: [] as string[][],
  index: true, columnWidth: [40, 88, 150], align: ['center', 'center', 'left', 'center'],
  headerBGC: 'rgba(0,186,255,.25)', oddRowBGC: 'rgba(12,30,60,.5)', evenRowBGC: 'rgba(12,30,60,.2)',
})

// ---- Live mock data ----
const areas = ['城东片区', '高新区', '滨江新城', '空港物流', '老城中心', '大学城']
const events = ['设备离线', '客流激增', '温度异常', '门禁告警', '能耗超限', '网络抖动']
const levels = [`<span style="color:${palette.danger}">紧急</span>`, `<span style="color:${palette.warning}">警告</span>`, `<span style="color:${palette.success}">正常</span>`]
const rand = (a: any[]) => a[Math.floor(Math.random() * a.length)]
const makeRow = () => [new Date().toLocaleTimeString('zh-CN', { hour12: false }), rand(areas), rand(events), rand(levels)]

onMounted(() => {
  mounted.value = true
  // seed + tick the alarm board
  board.data = Array.from({ length: 8 }, makeRow)
  const clock = () => (now.value = new Date().toLocaleString('zh-CN', { hour12: false }))
  clock()
  setInterval(clock, 1000)
  setInterval(() => { board.data = [makeRow(), ...board.data].slice(0, 12) }, 3500)
  // nudge a KPI so the flop animates "live"
  setInterval(() => { kpis[0].config.number = [120000 + Math.floor(Math.random() * 20000)] }, 4000)
})
</script>

<!-- ============================= COVER ============================= -->

# 城市运营监控大屏

Slidev × DataV — 大屏示例 / a large-screen dashboard built with `@kjgl77/datav-vue3`

<div class="mt-6 op70 text-sm">
按 <kbd>空格</kbd> / <kbd>→</kbd> 进入大屏 · Press space to enter the dashboard
</div>

---
layout: dashboard
---

<DashGrid :cols="24" :rows="12" gap="14px">

  <!-- Header -->
  <div style="grid-column:1/25; grid-row:1/2">
    <div class="dv-header">
      <div class="dv-header__title">城市运营监控中心 · CITY OPS</div>
      <div class="dv-header__meta">系统状态 <b>正常</b> · 数据更新 <b>{{ now }}</b></div>
    </div>
    <DvDecoration10 style="width:100%;height:4px" />
  </div>

  <!-- KPI row -->
  <DashPanel box="DvBorderBox13" style="grid-column:1/25; grid-row:2/3">
    <div v-if="mounted" style="display:flex; height:100%; align-items:center; justify-content:space-around">
      <div v-for="k in kpis" :key="k.label" class="dv-kpi">
        <DvDigitalFlop :config="k.config" class="dv-num" style="width:200px;height:48px" />
        <div class="dv-kpi__label">{{ k.label }}</div>
      </div>
    </div>
  </DashPanel>

  <!-- Left column -->
  <DashPanel title="片区客流排名" box="DvBorderBox12" style="grid-column:1/8; grid-row:3/8">
    <DvScrollRankingBoard v-if="mounted" :config="ranking" style="width:100%;height:100%" />
  </DashPanel>

  <DashPanel title="出行方式构成" box="DvBorderBox12" style="grid-column:1/8; grid-row:8/13">
    <DvCapsuleChart v-if="mounted" :config="capsule" style="width:100%;height:100%" />
  </DashPanel>

  <!-- Center column -->
  <DashPanel title="实时车流趋势" box="DvBorderBox13" style="grid-column:8/18; grid-row:3/9">
    <DvCharts v-if="mounted" :option="trend" style="width:100%;height:100%" />
  </DashPanel>

  <DashPanel title="片区负荷锥形榜" box="DvBorderBox13" style="grid-column:8/18; grid-row:9/13">
    <DvConicalColumnChart v-if="mounted" :config="conical" style="width:100%;height:100%" />
  </DashPanel>

  <!-- Right column -->
  <DashPanel title="设备运行状态" box="DvBorderBox12" style="grid-column:18/25; grid-row:3/7">
    <DvActiveRingChart v-if="mounted" :config="ring" style="width:100%;height:100%" />
  </DashPanel>

  <DashPanel title="水位 / 在线率" box="DvBorderBox12" style="grid-column:18/25; grid-row:7/10">
    <div v-if="mounted" style="display:flex; height:100%; align-items:center; justify-content:space-around; gap:12px">
      <DvWaterLevelPond :config="water" style="width:110px;height:130px" />
      <div style="flex:1; display:flex; flex-direction:column; gap:10px">
        <div class="dv-text-dim" style="font-size:13px">系统在线率</div>
        <DvPercentPond :config="percent" style="width:100%;height:46px" />
      </div>
    </div>
  </DashPanel>

  <DashPanel title="实时告警" box="DvBorderBox12" style="grid-column:18/25; grid-row:10/13">
    <DvScrollBoard v-if="mounted" :config="board" style="width:100%;height:100%" />
  </DashPanel>

</DashGrid>

<!--
  Adapt this deck:
  - Swap palette: add `htmlAttrs: { class: 'theme-purple' }` to headmatter and update the `palette`
    object above to matching hex values.
  - Replace the center DvCharts with a DvFlylineChart map once you have a `bgImgUrl` map image.
  - Add more dashboard slides: copy from `---\nlayout: dashboard\n---` down, change the data.
  - Bind real data: replace the reactive objects / the onMounted intervals with your fetch + setInterval.
-->
