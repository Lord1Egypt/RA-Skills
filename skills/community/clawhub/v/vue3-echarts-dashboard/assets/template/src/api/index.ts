import axios from 'axios'
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
} from './types'

// 统一请求实例。baseURL 留空即走同源，dev 下由 Vite 直接读取 public/data 下的静态 json。
// 真实接口只需把 baseURL 改成网关地址，并把下方路径改为后端路由即可。
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 10000,
})

export const getOverview = () =>
  http.get<OverviewResp>('/data/overview.json').then((r) => r.data)

export const getTrend = () =>
  http.get<TrendResp>('/data/trend.json').then((r) => r.data)

export const getCategory = () =>
  http.get<CategoryResp>('/data/category.json').then((r) => r.data)

export const getPie = () =>
  http.get<PieResp>('/data/pie.json').then((r) => r.data)

export const getRanking = () =>
  http.get<RankingResp>('/data/ranking.json').then((r) => r.data)

export const getGauge = () =>
  http.get<GaugeResp>('/data/gauge.json').then((r) => r.data)

export const getRadar = () =>
  http.get<RadarResp>('/data/radar.json').then((r) => r.data)

export const getFunnel = () =>
  http.get<FunnelResp>('/data/funnel.json').then((r) => r.data)

export const getBar = () =>
  http.get<BarResp>('/data/bar.json').then((r) => r.data)

export const getHeatmap = () =>
  http.get<HeatmapResp>('/data/heatmap.json').then((r) => r.data)

export const getSankey = () =>
  http.get<SankeyResp>('/data/sankey.json').then((r) => r.data)

export const getTree = () =>
  http.get<TreeResp>('/data/tree.json').then((r) => r.data)

export const getSunburst = () =>
  http.get<SunburstResp>('/data/sunburst.json').then((r) => r.data)

export const getMap = () =>
  http.get<MapResp>('/data/map.json').then((r) => r.data)

export const getWordCloud = () =>
  http.get<WordCloudResp>('/data/wordcloud.json').then((r) => r.data)

export const getLiquidFill = () =>
  http.get<LiquidFillResp>('/data/liquidfill.json').then((r) => r.data)

// 地图底图：本地 geoJSON（放在 public/geo/ 下），由组件调用 echarts.registerMap 注册
export const getGeo = (mapName = 'china') =>
  http.get<unknown>(`/geo/${mapName}.json`).then((r) => r.data)
