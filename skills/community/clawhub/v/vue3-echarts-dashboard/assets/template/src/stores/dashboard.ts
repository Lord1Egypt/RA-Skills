import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '@/api'
import type {
  OverviewResp,
  TrendResp,
  CategoryResp,
  PieResp,
  RankingResp,
  GaugeResp,
  RadarResp,
  FunnelResp,
  BarResp,
  HeatmapResp,
  SankeyResp,
  TreeResp,
  SunburstResp,
  MapResp,
  WordCloudResp,
  LiquidFillResp,
} from '@/api/types'

// 大屏数据中心：所有图表/指标统一从这里取数，组件只负责渲染。
export const useDashboardStore = defineStore('dashboard', () => {
  const overview = ref<OverviewResp>({ updatedAt: '', metrics: [] })
  const trend = ref<TrendResp | null>(null)
  const category = ref<CategoryResp | null>(null)
  const pie = ref<PieResp | null>(null)
  const ranking = ref<RankingResp | null>(null)
  const gauge = ref<GaugeResp | null>(null)
  const radar = ref<RadarResp | null>(null)
  const funnel = ref<FunnelResp | null>(null)
  const bar = ref<BarResp | null>(null)
  const heatmap = ref<HeatmapResp | null>(null)
  const sankey = ref<SankeyResp | null>(null)
  const tree = ref<TreeResp | null>(null)
  const sunburst = ref<SunburstResp | null>(null)
  const map = ref<MapResp | null>(null)
  const wordcloud = ref<WordCloudResp | null>(null)
  const liquidfill = ref<LiquidFillResp | null>(null)
  const loading = ref(false)
  const lastUpdated = ref('')

  async function fetchAll() {
    loading.value = true
    try {
      const [o, t, c, p, r, g, rd, f, b, h, s, tr, sb, m, w, l] = await Promise.all([
        api.getOverview(),
        api.getTrend(),
        api.getCategory(),
        api.getPie(),
        api.getRanking(),
        api.getGauge(),
        api.getRadar(),
        api.getFunnel(),
        api.getBar(),
        api.getHeatmap(),
        api.getSankey(),
        api.getTree(),
        api.getSunburst(),
        api.getMap(),
        api.getWordCloud(),
        api.getLiquidFill(),
      ])
      overview.value = o
      trend.value = t
      category.value = c
      pie.value = p
      ranking.value = r
      gauge.value = g
      radar.value = rd
      funnel.value = f
      bar.value = b
      heatmap.value = h
      sankey.value = s
      tree.value = tr
      sunburst.value = sb
      map.value = m
      wordcloud.value = w
      liquidfill.value = l
      lastUpdated.value = o.updatedAt
    } finally {
      loading.value = false
    }
  }

  return {
    overview,
    trend,
    category,
    pie,
    ranking,
    gauge,
    radar,
    funnel,
    bar,
    heatmap,
    sankey,
    tree,
    sunburst,
    map,
    wordcloud,
    liquidfill,
    loading,
    lastUpdated,
    fetchAll,
  }
})
