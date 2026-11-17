import { defineStore } from 'pinia'
import {
  fetchChannel,
  fetchFunnel,
  fetchGauge,
  fetchHeatmap,
  fetchKpi,
  fetchMap,
  fetchProduct,
  fetchProfit,
  fetchRegion,
  fetchSankey,
  fetchScatter,
  fetchSunburst,
  fetchTree,
  fetchTrend,
  fetchWordcloud,
} from '@/api'
import type {
  CategorySeries,
  FunnelData,
  GaugeData,
  HeatmapData,
  KpiItem,
  MapData,
  PieData,
  RegionData,
  SankeyData,
  ScatterData,
  SunburstData,
  TreeData,
  WordcloudData,
} from '@/types'

interface DashboardState {
  loading: boolean
  error: string
  kpis: KpiItem[]
  trend: CategorySeries | null
  product: PieData | null
  channel: CategorySeries | null
  profit: CategorySeries | null
  region: RegionData | null
  funnel: FunnelData | null
  gauge: GaugeData | null
  scatter: ScatterData | null
  sunburst: SunburstData | null
  sankey: SankeyData | null
  tree: TreeData | null
  heatmap: HeatmapData | null
  map: MapData | null
  wordcloud: WordcloudData | null
}

/** 大屏数据仓库：初始化时并发加载 public/data/*.json */
export const useDashboardStore = defineStore('dashboard', {
  state: (): DashboardState => ({
    loading: true,
    error: '',
    kpis: [],
    trend: null,
    product: null,
    channel: null,
    profit: null,
    region: null,
    funnel: null,
    gauge: null,
    scatter: null,
    sunburst: null,
    sankey: null,
    tree: null,
    heatmap: null,
    map: null,
    wordcloud: null,
  }),
  getters: {
    ready: (state) =>
      !!state.trend &&
      !!state.product &&
      !!state.channel &&
      !!state.profit &&
      !!state.region &&
      !!state.funnel &&
      !!state.gauge &&
      !!state.scatter &&
      !!state.sunburst &&
      !!state.sankey &&
      !!state.tree &&
      !!state.heatmap &&
      !!state.map &&
      !!state.wordcloud,
  },
  actions: {
    async loadAll() {
      this.loading = true
      this.error = ''
      try {
        const [
          kpis,
          trend,
          product,
          channel,
          profit,
          region,
          funnel,
          gauge,
          scatter,
          sunburst,
          sankey,
          tree,
          heatmap,
          map,
          wordcloud,
        ] = await Promise.all([
          fetchKpi(),
          fetchTrend(),
          fetchProduct(),
          fetchChannel(),
          fetchProfit(),
          fetchRegion(),
          fetchFunnel(),
          fetchGauge(),
          fetchScatter(),
          fetchSunburst(),
          fetchSankey(),
          fetchTree(),
          fetchHeatmap(),
          fetchMap(),
          fetchWordcloud(),
        ])
        this.kpis = kpis
        this.trend = trend
        this.product = product
        this.channel = channel
        this.profit = profit
        this.region = region
        this.funnel = funnel
        this.gauge = gauge
        this.scatter = scatter
        this.sunburst = sunburst
        this.sankey = sankey
        this.tree = tree
        this.heatmap = heatmap
        this.map = map
        this.wordcloud = wordcloud
      } catch (e) {
        this.error = e instanceof Error ? e.message : String(e)
      } finally {
        this.loading = false
      }
    },
  },
})
