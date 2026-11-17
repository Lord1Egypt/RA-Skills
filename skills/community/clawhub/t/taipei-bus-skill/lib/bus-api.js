/**
 * bus-api.js — 臺北市公車定點車機 OD API 核心模組（整合 PTX 座標版）
 *
 * 整合兩個資料來源：
 * 1. 定點車機即時 API（TstBusEvent.json） — 即時車位
 * 2. PTX Bus Stop API — 站牌座標（已本地快取）
 */

const { getStopCoords, getStationCoords, batchGetStopCoords, searchStops } = require('./stop-coords.js');
const routeApi = require('./route-api.js');

// ─── 定點車機即時 API ────────────────────────────────────────────
const VEHICLE_API_URL = 'https://tcgbusfs.blob.core.windows.net/blobbus/TstBusEvent.json';

/**
 * 抓取全量即時公車資料（車機 OD）
 * @returns {Promise<BusRecord[]>}
 */
async function fetchAll() {
  const res = await fetch(VEHICLE_API_URL);
  if (!res.ok) throw new Error(`API 回應錯誤: ${res.status}`);
  const raw = await res.json();
  return raw.sort((a, b) => new Date(b.DataTime) - new Date(a.DataTime));
}

/**
 * 依路線代碼查詢所有在線公車
 */
async function findByRoute(routeId) {
  const buses = await fetchAll();
  return buses.filter(b => b.RouteID === routeId);
}

/**
 * 依車牌查單台公車狀態
 */
async function findByBus(busId) {
  const buses = await fetchAll();
  return buses.find(b => b.BusID === busId) || null;
}

/**
 * 查某站目前停在站位的公車
 */
async function findAtStation(stopId) {
  const buses = await fetchAll();
  return buses.filter(b => b.StopID === stopId && b.CarOnStop === '1');
}

// ─── PTX 座標整合 ────────────────────────────────────────────────

/**
 * 估算公車到站時間（含座標版 ETA，距離更精確）
 * @param {string} routeId
 * @param {string} targetStopId
 * @param {number} avgSpeedKmh — 平均時速（預設市區 25km/h）
 * @returns {Promise<EtaResult>}
 */
async function etaEstimate(routeId, targetStopId, avgSpeedKmh = 25) {
  const buses = await findByRoute(routeId);
  if (!buses.length) return { minutes: null, bus: null, note: '目前無此路線公車在線' };

  // 取最新一筆
  const bus = buses[0];
  const coords = getStopCoords(bus.StopID);
  const targetCoords = getStopCoords(targetStopId);

  let minutes;
  let note;

  if (coords && targetCoords) {
    // 有座標 → Haversine 距離估算
    const distKm = haversineDistance(
      coords.lat, coords.lon,
      targetCoords.lat, targetCoords.lon
    );
    minutes = Math.max(1, Math.round((distKm / avgSpeedKmh) * 60));
    note = `依直線距離約 ${distKm.toFixed(2)} km（${avgSpeedKmh}km/h）估算`;
  } else {
    // 無座標 → 固定站距估算
    const stationDistanceKm = 0.5;
    minutes = Math.max(1, Math.round((stationDistanceKm / avgSpeedKmh) * 60));
    note = `⚠️ 無座標，依平均站距 ${stationDistanceKm * 1000}m 估算`;
  }

  return { minutes, bus, note, coords: targetCoords };
}

/**
 * Haversine 公式：計算兩點間球面距離（km）
 */
function haversineDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // 地球半徑 km
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}
function toRad(deg) { return deg * Math.PI / 180; }

/**
 * 偵測脫班/異常公車
 */
async function detectAnomalies() {
  const buses = await fetchAll();
  return buses.filter(b => b.DutyStatus !== '1' || b.BusStatus !== '0');
}

/**
 * 全系統路線概況摘要
 */
async function routeSummary() {
  const buses = await fetchAll();
  const summary = {};
  for (const bus of buses) {
    if (!summary[bus.RouteID]) summary[bus.RouteID] = { count: 0, buses: [] };
    summary[bus.RouteID].count++;
    summary[bus.RouteID].buses.push(bus);
  }
  return summary;
}

// ─── 增強版：含座標的公車資料 ──────────────────────────────────────

/**
 * 取得所有公車，並附加站牌座標
 * @returns {Promise<EnrichedBusRecord[]>}
 */
async function fetchAllWithCoords() {
  const buses = await fetchAll();
  const stopIds = [...new Set(buses.map(b => b.StopID))];
  const coordsMap = batchGetStopCoords(stopIds);

  return buses.map(bus => ({
    ...bus,
    _stopCoords: coordsMap[bus.StopID] || null
  }));
}

/**
 * 取得全系統熱點站位（公車密度最高的站點）
 * @param {number} topN
 * @returns {Promise<Array<{stopId, stopName, lat, lon, count}>>}
 */
async function getHotspots(topN = 10) {
  const enriched = await fetchAllWithCoords();
  const counter = {};
  for (const bus of enriched) {
    if (!bus._stopCoords) continue;
    const key = bus.StopID;
    if (!counter[key]) {
      counter[key] = { stopId: key, stopName: bus._stopCoords.name, lat: bus._stopCoords.lat, lon: bus._stopCoords.lon, count: 0 };
    }
    counter[key].count++;
  }
  return Object.values(counter).sort((a, b) => b.count - a.count).slice(0, topN);
}

// ─── 格式化輸出 ────────────────────────────────────────────────────

/**
 * 人類可讀格式化（含站牌名稱）
 * @param {BusRecord} bus
 */
function formatBus(bus, showCoords = false) {
  const time = new Date(bus.DataTime).toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' });
  const status = bus.CarOnStop === '1' ? '🟢 停在站位' : '🚌 行駛中';
  const duty = bus.DutyStatus === '1' ? '上班' : '非上班';
  const goBack = bus.GoBack === '1' ? '去程' : '返程';

  const stopInfo = getStopCoords(bus.StopID);
  const stopName = stopInfo ? stopInfo.name : `站點 ${bus.StopID}`;

  let extra = showCoords && stopInfo
    ? `\n   📍 座標: (${stopInfo.lat?.toFixed(5)}, ${stopInfo.lon?.toFixed(5)})`
    : '';

  return [
    `🚌 ${bus.BusID}（${bus.CarType === '0' ? '一般' : '類型' + bus.CarType}）`,
    `   路線: ${bus.RouteID}（${goBack}）`,
    `   站點: ${stopName} ${status}`,
    `   勤務: ${duty} | 狀態: ${bus.BusStatus === '0' ? '正常' : '異常'}`,
    `   更新: ${time}${extra}`
  ].join('\n');
}

// ─── PTX 路名 / 站序整合 ───────────────────────────────────────

/**
 * 以路名搜尋公車路線（模糊匹配）
 * @param {string} keyword — 如 "234"、"南京"、"藍10"
 * @returns {RouteInfo|null}
 */
function searchRouteByName(keyword) {
  return routeApi.findRouteByName(keyword);
}

/**
 * 以 RouteID 查完整路線資訊
 */
function getRouteInfo(routeId) {
  return routeApi.getRoute(routeId);
}

/**
 * 模糊搜尋所有匹配路線
 * @param {string} keyword
 * @param {number} limit
 */
function searchRoutes(keyword, limit = 10) {
  return routeApi.searchRoutes(keyword, limit);
}

/**
 * 取得某路線的全部站序
 * @param {string} routeId
 * @param {number} direction — 0=去程, 1=返程
 */
function getRouteStopSequence(routeId, direction = 0) {
  return routeApi.getRouteStops(routeId, direction);
}

/**
 * 依站序估算到站時間（最精確版本）
 * @param {string} routeId — PTX RouteID（如 "10132"）
 * @param {string} targetStopId
 * @param {number} direction
 * @param {number} avgSecPerStop — 平均每站秒數（預設 90s）
 */
function etaBySequence(routeId, targetStopId, direction = 0, avgSecPerStop = 90) {
  return routeApi.estimateArrivalBySequence(routeId, targetStopId, direction, avgSecPerStop);
}

/**
 * 查某站點有哪些路線經過
 * @param {string} stopId
 */
function getRoutesByStop(stopId) {
  return routeApi.getStopRoutes(stopId);
}

// ─── 匯出 ─────────────────────────────────────────────────────────
module.exports = {
  // 即時車機
  fetchAll,
  findByRoute,
  findByBus,
  findAtStation,
  etaEstimate,
  detectAnomalies,
  routeSummary,
  // 座標增強版
  fetchAllWithCoords,
  getHotspots,
  // 路線整合
  searchRouteByName,
  getRouteInfo,
  searchRoutes,
  getRouteStopSequence,
  etaBySequence,
  getRoutesByStop,
  // 工具
  getStopCoords,
  getStationCoords,
  searchStops,
  batchGetStopCoords,
  // 格式化
  formatBus,
  haversineDistance,
  // 直接暴露 route-api（高階用）
  routeApi,
  VEHICLE_API_URL
};
