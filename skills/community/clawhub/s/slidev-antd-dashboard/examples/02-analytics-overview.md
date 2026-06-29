---
layout: full
---

<script setup>
import { ref } from 'vue'

const range = ref('Week')

const revenueOption = {
  tooltip: { trigger: 'axis' },
  grid: { left: 40, right: 12, top: 16, bottom: 28 },
  xAxis: { type: 'category', boundaryGap: false, data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] },
  yAxis: { type: 'value' },
  series: [{
    name: 'Revenue', type: 'line', smooth: true,
    areaStyle: { opacity: 0.15 }, lineStyle: { width: 3 },
    data: [3200, 3320, 3010, 4340, 4900, 5300, 4810],
  }],
}

const channelOption = {
  tooltip: { trigger: 'item' },
  legend: { bottom: 0, icon: 'circle' },
  series: [{
    type: 'pie', radius: ['48%', '72%'], avoidLabelOverlap: false,
    itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
    label: { show: false },
    data: [
      { value: 5400, name: 'Direct' },
      { value: 3100, name: 'Organic' },
      { value: 2300, name: 'Referral' },
      { value: 1200, name: 'Social' },
    ],
  }],
}

const productCols = [
  { title: 'Product', dataIndex: 'name', key: 'name' },
  { title: 'Category', key: 'cat' },
  { title: 'Units', dataIndex: 'units', key: 'units', align: 'right' },
  { title: 'Revenue', dataIndex: 'rev', key: 'rev', align: 'right' },
  { title: 'Trend', key: 'trend', align: 'right' },
]
const products = [
  { key: 1, name: 'Pro subscription', cat: 'Plans', units: 412, rev: '$16,480', up: true, delta: '+9%' },
  { key: 2, name: 'Team seats', cat: 'Plans', units: 318, rev: '$9,540', up: true, delta: '+4%' },
  { key: 3, name: 'API credits', cat: 'Usage', units: 1290, rev: '$6,450', up: false, delta: '-2%' },
  { key: 4, name: 'Onboarding', cat: 'Services', units: 36, rev: '$5,400', up: true, delta: '+12%' },
]
</script>

<DashboardShell selected-key="analytics" open-key="insights-g" :crumbs="['Home', 'Analytics']" title="Analytics overview">
  <template #actions>
    <a-space>
      <a-segmented v-model:value="range" :options="['Day', 'Week', 'Month']" />
      <a-range-picker />
      <a-button type="primary"><download-outlined /> Export</a-button>
    </a-space>
  </template>

  <!-- KPI row -->
  <a-row :gutter="[16, 16]">
    <a-col :span="6">
      <a-card :bordered="false">
        <a-statistic title="Revenue" :value="48230" prefix="$" :precision="0" />
        <a-typography-text type="success"><arrow-up-outlined /> 12% </a-typography-text>
        <a-typography-text type="secondary">vs last week</a-typography-text>
      </a-card>
    </a-col>
    <a-col :span="6">
      <a-card :bordered="false">
        <a-statistic title="Orders" :value="1429" />
        <a-typography-text type="success"><arrow-up-outlined /> 8% </a-typography-text>
        <a-typography-text type="secondary">vs last week</a-typography-text>
      </a-card>
    </a-col>
    <a-col :span="6">
      <a-card :bordered="false">
        <a-statistic title="Conversion" :value="3.4" suffix="%" :precision="1" />
        <a-typography-text type="danger"><arrow-down-outlined /> 0.3pp </a-typography-text>
        <a-typography-text type="secondary">vs last week</a-typography-text>
      </a-card>
    </a-col>
    <a-col :span="6">
      <a-card :bordered="false">
        <a-statistic title="Avg. order value" :value="34" prefix="$" />
        <a-typography-text type="success"><arrow-up-outlined /> 2% </a-typography-text>
        <a-typography-text type="secondary">vs last week</a-typography-text>
      </a-card>
    </a-col>
  </a-row>

  <!-- charts row -->
  <a-row :gutter="[16, 16]" style="margin-top: 16px">
    <a-col :span="16">
      <a-card title="Revenue trend" :bordered="false">
        <v-chart :option="revenueOption" style="height: 240px" autoresize />
      </a-card>
    </a-col>
    <a-col :span="8">
      <a-card title="Revenue by channel" :bordered="false">
        <v-chart :option="channelOption" style="height: 240px" autoresize />
      </a-card>
    </a-col>
  </a-row>

  <!-- table row -->
  <a-row :gutter="[16, 16]" style="margin-top: 16px">
    <a-col :span="24">
      <a-card title="Top products" :bordered="false">
        <a-table :columns="productCols" :data-source="products" size="small" :pagination="false">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'cat'">
              <a-tag>{{ record.cat }}</a-tag>
            </template>
            <template v-else-if="column.key === 'trend'">
              <a-typography-text :type="record.up ? 'success' : 'danger'">
                <arrow-up-outlined v-if="record.up" /><arrow-down-outlined v-else /> {{ record.delta }}
              </a-typography-text>
            </template>
          </template>
        </a-table>
      </a-card>
    </a-col>
  </a-row>
</DashboardShell>
