import axios from 'axios'
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

/** axios 实例：数据 JSON 放在 public/data/，通过 /data/*.json 访问 */
export const http = axios.create({
  baseURL: '/',
  timeout: 10000,
})

export const fetchKpi = () => http.get<KpiItem[]>('/data/kpi.json').then((r) => r.data)
export const fetchTrend = () => http.get<CategorySeries>('/data/trend.json').then((r) => r.data)
export const fetchProduct = () => http.get<PieData>('/data/product.json').then((r) => r.data)
export const fetchChannel = () => http.get<CategorySeries>('/data/channel.json').then((r) => r.data)
export const fetchProfit = () => http.get<CategorySeries>('/data/profit.json').then((r) => r.data)
export const fetchRegion = () => http.get<RegionData>('/data/region.json').then((r) => r.data)
export const fetchFunnel = () => http.get<FunnelData>('/data/funnel.json').then((r) => r.data)
export const fetchGauge = () => http.get<GaugeData>('/data/gauge.json').then((r) => r.data)
export const fetchScatter = () => http.get<ScatterData>('/data/scatter.json').then((r) => r.data)
export const fetchSunburst = () => http.get<SunburstData>('/data/sunburst.json').then((r) => r.data)
export const fetchSankey = () => http.get<SankeyData>('/data/sankey.json').then((r) => r.data)
export const fetchTree = () => http.get<TreeData>('/data/tree.json').then((r) => r.data)
export const fetchHeatmap = () => http.get<HeatmapData>('/data/heatmap.json').then((r) => r.data)
export const fetchMap = () => http.get<MapData>('/data/map.json').then((r) => r.data)
export const fetchWordcloud = () => http.get<WordcloudData>('/data/wordcloud.json').then((r) => r.data)
