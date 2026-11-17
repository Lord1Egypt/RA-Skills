/**
 * route-api.js — PTX 公車路線整合模組
 *
 * 資料來源：
 *   - Route API:      https://ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei
 *   - StopOfRoute API: https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei
 *   - 本地快取:        data/route-full-cache.json
 *
 * 功能：
 *   - 路名搜尋 → RouteID
 *   - 站序查詢 → 某站是第幾站、離終點還剩幾站
 *   - 精確 ETA → 依剩餘站數估算（比 Haversine 更精準）
 *   - 路線完整資訊 → 起訖站、首末班、業者
 */

const path = require('path');
const fs = require('fs');

const CACHE_PATH = path.join(__dirname, '..', 'data', 'route-full-cache.json');

let _cache = null;
function _loadCache() {
  if (_cache) return _cache;
  if (!fs.existsSync(CACHE_PATH)) return null;
  try {
    _cache = JSON.parse(fs.readFileSync(CACHE_PATH, 'utf-8'));
    return _cache;
  } catch (e) {
    console.warn('[route-api] 快取讀取失敗:', e.message);
    return null;
  }
}

// ════════════════════════════════════════════════════════════════════
//  1. 路名 / RouteID 查詢
// ════════════════════════════════════════════════════════════════════

/**
 * 以路名（數字/幹線/顏色）查詢路線
 * @param {string} name — 如 "234"、"南京"、"藍10"
 * @returns {RouteInfo|null}
 */
function findRouteByName(name) {
  const cache = _loadCache();
  if (!cache) return null;

  // 精確 match
  if (cache.name_to_routes[name]) return cache.name_to_routes[name];

  // 模糊 match（包含）
  const fuzzy = Object.entries(cache.name_to_routes)
    .filter(([k]) => k.includes(name) || name.includes(k))
    .map(([, v]) => v);
  return fuzzy.length > 0 ? fuzzy[0] : null;
}

/**
 * 以 RouteID 查路線資訊
 * @param {string} routeId
 * @returns {RouteInfo|null}
 */
function getRoute(routeId) {
  const cache = _loadCache();
  if (!cache) return null;
  return cache.route_map[routeId] || null;
}

/**
 * 搜尋所有匹配路線（模糊）
 * @param {string} keyword
 * @param {number} limit
 * @returns {RouteInfo[]}
 */
function searchRoutes(keyword, limit = 10) {
  const cache = _loadCache();
  if (!cache) return [];
  const k = keyword.toLowerCase();
  const results = Object.entries(cache.name_to_routes)
    .filter(([name]) => name.toLowerCase().includes(k) || k.includes(name.toLowerCase()))
    .map(([, v]) => v);
  return results.slice(0, limit);
}

/**
 * 取得所有路線代碼列表
 * @returns {string[]}
 */
function listRouteIds() {
  const cache = _loadCache();
  if (!cache) return [];
  return Object.keys(cache.route_map || {});
}

// ════════════════════════════════════════════════════════════════════
//  2. 站序查詢
// ════════════════════════════════════════════════════════════════════

/**
 * 取得某路線的全部站序
 * @param {string} routeId
 * @param {number} direction — 0=去程, 1=返程
 * @returns {StopEntry[]}
 */
function getRouteStops(routeId, direction = 0) {
  const cache = _loadCache();
  if (!cache) return [];
  const seq = cache.route_seq[routeId];
  return seq ? (seq[direction] || []) : [];
}

/**
 * 查某站點在特定路線的站序資訊
 * @param {string} routeId
 * @param {string} stopId
 * @param {number} direction
 * @returns {{ stop: StopEntry, index: number, remaining: number, total: number } | null}
 */
function getStopSequence(routeId, stopId, direction = 0) {
  const stops = getRouteStops(routeId, direction);
  const index = stops.findIndex(s => s.stopId === stopId || s.stopId === String(stopId));
  if (index === -1) return null;
  return {
    stop: stops[index],
    index: index + 1,       // 1-based
    remaining: stops.length - index - 1,
    total: stops.length,
  };
}

/**
 * 查某站點在所有路線的經過情形
 * @param {string} stopId
 * @returns {StopEntry[]}
 */
function getStopRoutes(stopId) {
  const cache = _loadCache();
  if (!cache) return [];

  // stopId → name → cache entry
  // 需要反向：所有 route_seq 中找 stopId
  const results = [];
  for (const routeId in cache.route_seq || {}) {
    for (const dir in cache.route_seq[routeId]) {
      const idx = cache.route_seq[routeId][dir].findIndex(s => s.stopId === stopId);
      if (idx !== -1) {
        const s = cache.route_seq[routeId][dir][idx];
        results.push({ ...s, routeId, direction: parseInt(dir), index: idx + 1 });
      }
    }
  }
  return results;
}

// ════════════════════════════════════════════════════════════════════
//  3. 精確 ETA 估算（依站序）
// ════════════════════════════════════════════════════════════════════

/**
 * 估算公車到站時間（依站序版本）
 *
 * @param {string} routeId
 * @param {string} targetStopId
 * @param {number} direction — 0=去程, 1=返程
 * @param {number} avgSecPerStop — 平均每站秒數（預設 90s = 1.5min 市區）
 * @returns {{ minutes: number|null, remaining: number, total: number, stop: object, note: string }}
 */
function estimateArrivalBySequence(routeId, targetStopId, direction = 0, avgSecPerStop = 90) {
  const seq = getStopSequence(routeId, targetStopId, direction);

  if (!seq) {
    return {
      minutes: null,
      remaining: null,
      total: null,
      stop: null,
      note: `路線 ${routeId} 中找不到站點 ${targetStopId}，請確認 StopID 是否正確`
    };
  }

  const minutes = Math.max(1, Math.round((seq.remaining * avgSecPerStop) / 60));
  const directionLabel = direction === 0 ? '去程' : '返程';
  return {
    minutes,
    remaining: seq.remaining,
    total: seq.total,
    stop: seq.stop,
    note: `依站序（第 ${seq.index}/${seq.total} 站），離目標站尚有 ${seq.remaining} 站（${directionLabel}）`,
  };
}

// ════════════════════════════════════════════════════════════════════
//  4. 路線完整資訊格式化
// ════════════════════════════════════════════════════════════════════

/**
 * 格式化路線資訊（人類可讀）
 * @param {RouteInfo} route
 */
function formatRoute(route) {
  if (!route) return '❌ 查無此路線';
  const subs = route.subRoutes || [];
  const go = subs.find(s => s.direction === 0);
  const back = subs.find(s => s.direction === 1);

  const lines = [
    `🚌 路線：${route.routeName}（${route.routeNameEn || route.routeName}）`,
    `   代碼：${route.routeId}`,
    `   起點：${route.departure || '—'} → 訖點：${route.terminal || '—'}`,
    `   業者：${route.operators.join('、') || '—'}`,
  ];

  if (go) {
    lines.push(`   去程首班：${go.firstBus || '—'} / 末班：${go.lastBus || '—'}`);
  }
  if (back) {
    lines.push(`   返程首班：${back.firstBus || '—'} / 末班：${back.lastBus || '—'}`);
  }

  return lines.join('\n');
}

/**
 * 格式化站序資訊（人類可讀）
 * @param {object} seq
 * @param {string} routeId
 * @param {number} direction
 */
function formatStopSequence(seq, routeId, direction) {
  if (!seq) return '❌ 查無站序資料';
  const route = getRoute(routeId);
  const routeName = route ? route.routeName : routeId;
  const directionLabel = direction === 0 ? '去程' : '返程';
  const stops = getRouteStops(routeId, direction);
  const nearby = stops.slice(Math.max(0, seq.index - 2), seq.index + 3);

  let lines = [
    `🚏 站點：${seq.stop.stopName}（StopID: ${seq.stop.stopId}）`,
    `   路線：${routeName}（${directionLabel}）`,
    `   站序：第 ${seq.index}/${seq.total} 站，離終點尚有 ${seq.remaining} 站`,
    `   📍 座標：(${seq.stop.lat?.toFixed(5)}, ${seq.stop.lon?.toFixed(5)})`,
  ];

  if (nearby.length > 1) {
    const currentIdx = seq.index - 1;
    lines.push('   周邊站：');
    nearby.forEach((s, i) => {
      const actualIdx = Math.max(0, currentIdx - 1) + i;
      const marker = actualIdx === currentIdx ? '👉' : '  ';
      lines.push(`     ${marker} ${actualIdx + 1}. ${s.stopName}`);
    });
  }

  return lines.join('\n');
}

// ════════════════════════════════════════════════════════════════════
//  匯出
// ════════════════════════════════════════════════════════════════════

module.exports = {
  findRouteByName,
  getRoute,
  searchRoutes,
  listRouteIds,
  getRouteStops,
  getStopSequence,
  getStopRoutes,
  estimateArrivalBySequence,
  formatRoute,
  formatStopSequence,
  CACHE_PATH
};
