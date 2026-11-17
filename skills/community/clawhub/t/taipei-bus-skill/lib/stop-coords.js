/**
 * stop-coords.js — PTX 站牌座標對應模組
 * 資料來源：PTX API https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei
 * 快取：~/.qclaw/skills/taipei-bus/data/stop-coords.json（由 build-cache.py 產生）
 *
 * 使用方式：
 *   const { getStopCoords, getStationCoords } = require('./stop-coords.js');
 *   const coords = getStopCoords('33210');
 */

const path = require('path');
const fs = require('fs');

const CACHE_PATH = path.join(__dirname, '..', 'data', 'stop-coords.json');

// 延遲載入快取（避免啟動時就讀磁碟）
let _cache = null;
function _loadCache() {
  if (_cache) return _cache;
  if (!fs.existsSync(CACHE_PATH)) {
    return null;
  }
  try {
    _cache = JSON.parse(fs.readFileSync(CACHE_PATH, 'utf-8'));
    return _cache;
  } catch (e) {
    console.warn('[stop-coords] 快取讀取失敗:', e.message);
    return null;
  }
}

/**
 * 依 StopID 查站牌座標
 * @param {string} stopId
 * @returns {{ name, lat, lon, stationId } | null}
 */
function getStopCoords(stopId) {
  const cache = _loadCache();
  if (!cache) return null;
  return cache.stops[stopId] || null;
}

/**
 * 依 StationID 查站牌座標
 * @param {string} stationId
 * @returns {{ name, lat, lon, stopId } | null}
 */
function getStationCoords(stationId) {
  const cache = _loadCache();
  if (!cache) return null;
  return cache.stations[stationId] || null;
}

/**
 * 取得全部站牌數量
 */
function getTotalCount() {
  const cache = _loadCache();
  return cache ? cache.meta.total : 0;
}

/**
 * 批次查詢（適用於大量座標需求）
 * @param {string[]} stopIds
 * @returns {{[stopId: string]: coords}}
 */
function batchGetStopCoords(stopIds) {
  const cache = _loadCache();
  if (!cache) return {};
  const result = {};
  for (const id of stopIds) {
    if (cache.stops[id]) result[id] = cache.stops[id];
  }
  return result;
}

/**
 * 搜尋站名（模糊比對）
 * @param {string} keyword
 * @param {number} limit
 * @returns {Array}
 */
function searchStops(keyword, limit = 10) {
  const cache = _loadCache();
  if (!cache) return [];
  const k = keyword.toLowerCase();
  const results = [];
  for (const [id, info] of Object.entries(cache.stops)) {
    if (info.name.includes(keyword) || info.nameEn.toLowerCase().includes(k)) {
      results.push({ stopId: id, ...info });
      if (results.length >= limit) break;
    }
  }
  return results;
}

module.exports = {
  getStopCoords,
  getStationCoords,
  getTotalCount,
  batchGetStopCoords,
  searchStops,
  CACHE_PATH
};
