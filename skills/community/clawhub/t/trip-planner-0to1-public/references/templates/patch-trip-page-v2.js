#!/usr/bin/env node
/**
 * 行程单页增强注入器 v2（trip-planner skill）
 *
 * v2 相对 v1 的增量：
 *   1) marker 上的文字标号统一改成「按 waypoints 索引递增的数字 1/2/3...」
 *      - 原页面里随便写的 A/B/K/T 等字母标号会被自动替换成数字
 *      - 即使 L.marker 的定义顺序和行程先后不符，也会按 waypoints 数组顺序重排
 *   2) 注入「自驾里程汇总」表格（地图正下方）：
 *      - 每段一行：# / 方式（飞机 🛩️ / 汽车 🚗）/ 路段 / 距离 / 耗时 / 导航/航班
 *      - 实测 km/hr 从 OSRM 结果取；飞行段走 haversine 直线估算
 *      - drawSegment 带 catch 兜底：哪怕 OSRM 请求抛异常，也会用 haversine 先 addRow，保证不丢段
 *      - addRow 严格按 idx 有序插入，重复写入会用 outerHTML 原位替换（不会叠行）
 *   3) 总里程徽章：加载过程中显示「加载 n/m」，完成后变成大字「自驾 X km · 飞行 Y km」
 *   4) 并发限流（3 路并发）调 OSRM，不会打爆公共节点
 *
 * 飞行段识别规则（按优先级）：
 *   a. HTML 里有注释 <!-- FLIGHT_SEGMENTS: [0,7,8] -->（注释值是 0-based segment index）
 *   b. fallback：waypoints 两点直线距离 > 800 km 自动判定为飞行段
 *
 * 用法：
 *   node patch-trip-page-v2.js <page-name>
 *   输入：/tmp/<page-name>.html
 *   输出：/tmp/<page-name>_patched.html
 */

const fs = require('fs');

const pageName = process.argv[2];
if (!pageName) {
  console.error('Usage: node patch-trip-page-v2.js <page-name>');
  process.exit(1);
}

const src = `/tmp/${pageName}.html`;
const dst = `/tmp/${pageName}_patched.html`;

let html = fs.readFileSync(src, 'utf8');

// ========== 1. 提取所有 marker：坐标 + popup 主标题 + marker 片段（用于改写 label） ==========
// 捕获整段 L.marker(...).addTo(map).bindPopup('...')，便于 in-place 修改里面的数字 label
const markerBlockRe = /L\.marker\(\s*\[\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\][\s\S]*?\.bindPopup\(\s*(['"])([\s\S]*?)\3\s*\)\s*;?/g;
const titleRe = /<strong>([^<]+)<\/strong>/;

const markers = [];
const matches = [];
let m;
while ((m = markerBlockRe.exec(html)) !== null) {
  const lat = parseFloat(m[1]);
  const lng = parseFloat(m[2]);
  const popup = m[4];
  const titleMatch = popup.match(titleRe);
  const fullTitle = titleMatch ? titleMatch[1].trim() : `点${markers.length + 1}`;
  markers.push({ lat, lng, title: fullTitle, blockStart: m.index, blockEnd: m.index + m[0].length, raw: m[0] });
  matches.push(m[0]);
}

if (markers.length < 2) {
  console.error(`[${pageName}] 解析到 marker 数量 ${markers.length} < 2，无法构建路线`);
  process.exit(2);
}

console.log(`[${pageName}] 提取 ${markers.length} 个 marker：`);
markers.forEach((p, i) => console.log(`  ${i + 1}. (${p.lat}, ${p.lng}) ${p.title}`));

// ========== 2. 把每个 marker 块里的「文字 label」统一改成 数字（index + 1） ==========
// 只替换 divIcon html 里的标号，不碰其他字段
// 倒序替换，避免 offset 漂移
const rewriteLabel = (block, label) => {
  // 匹配 divIcon html 中居中放置的单字符/数字标号：字段通常是 ">X</div>"（X 是一个字符或数字）
  // 更宽松：找 ...font-weight:700;">标号</div> 这样的结构
  const labelRe = /(font-weight\s*:\s*7\d{2}\s*;?\s*['"]?\s*>)([^<]{1,3})(<\/div>)/;
  if (labelRe.test(block)) {
    return block.replace(labelRe, `$1${label}$3`);
  }
  // fallback：找 divIcon 的 html 里最内层的 >X</div>
  const fallbackRe = /(>)([A-Za-z0-9]{1,3})(<\/div>\s*,?\s*iconSize)/;
  if (fallbackRe.test(block)) {
    return block.replace(fallbackRe, `$1${label}$3`);
  }
  return block;
};

// 倒序替换
for (let i = markers.length - 1; i >= 0; i--) {
  const mk = markers[i];
  const newBlock = rewriteLabel(mk.raw, String(i + 1));
  if (newBlock !== mk.raw) {
    html = html.slice(0, mk.blockStart) + newBlock + html.slice(mk.blockEnd);
  }
}

// ========== 3. 从 HTML 注释里读飞行段 ==========
const flightRe = /<!--\s*FLIGHT_SEGMENTS\s*:\s*(\[[^\]]*\])\s*-->/i;
let flightSegments = [];
const flightMatch = html.match(flightRe);
if (flightMatch) {
  try {
    flightSegments = JSON.parse(flightMatch[1]);
    console.log(`[${pageName}] 飞行段（来自 HTML 注释）：`, flightSegments);
  } catch (e) {
    console.warn(`[${pageName}] FLIGHT_SEGMENTS 解析失败：`, e.message);
  }
}

// fallback：直线距离 > 800km 自动判定飞行段
if (flightSegments.length === 0) {
  const toRad = d => d * Math.PI / 180;
  const hv = (a, b) => {
    const R = 6371;
    const dLat = toRad(b.lat - a.lat);
    const dLng = toRad(b.lng - a.lng);
    const lat1 = toRad(a.lat), lat2 = toRad(b.lat);
    const x = Math.sin(dLat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLng / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(x));
  };
  for (let i = 0; i < markers.length - 1; i++) {
    if (hv(markers[i], markers[i + 1]) > 800) flightSegments.push(i);
  }
  if (flightSegments.length) console.log(`[${pageName}] 飞行段（自动推断 >800km）：`, flightSegments);
}

// ========== 4. 构造注入脚本 ==========
const waypointsJSON = JSON.stringify(markers.map(p => [p.lat, p.lng]));
const titlesJSON = JSON.stringify(markers.map(p => p.title));
const flightSegJSON = JSON.stringify(flightSegments);

const scriptInject = `

// ===== AUTO-PATCH v2: 路线渲染（OSRM 真实路由 + 飞行段虚线 + 分段里程表 + 总里程） =====
(function() {
  if (typeof map === 'undefined' || !map) return;

  const waypoints = ${waypointsJSON};
  const titles = ${titlesJSON};
  const flightSegments = ${flightSegJSON};

  const flightSet = new Set(flightSegments || []);

  const OSRM_ENDPOINTS = [
    'https://router.project-osrm.org/route/v1/driving',
    'https://routing.openstreetmap.de/routed-car/route/v1/driving'
  ];
  const routeColors = ['#4fc3f7', '#81c784', '#ffb74d', '#ba68c8', '#f06292', '#4dd0e1', '#ff8a65', '#aed581', '#7986cb', '#ff7043'];

  function haversine(a, b) {
    const R = 6371;
    const toRad = d => d * Math.PI / 180;
    const dLat = toRad(b[0] - a[0]);
    const dLng = toRad(b[1] - a[1]);
    const lat1 = toRad(a[0]);
    const lat2 = toRad(b[0]);
    const x = Math.sin(dLat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLng / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(x));
  }

  function cacheKey(a, b) {
    return 'trip_osrm_' + a.map(n => n.toFixed(4)).join(',') + '|' + b.map(n => n.toFixed(4)).join(',');
  }

  async function fetchSegment(from, to) {
    const key = cacheKey(from, to);
    try {
      const cached = localStorage.getItem(key);
      if (cached) {
        const obj = JSON.parse(cached);
        if (obj && obj.coords && obj.coords.length > 2) return obj;
      }
    } catch (e) {}
    const coordStr = from[1] + ',' + from[0] + ';' + to[1] + ',' + to[0];
    for (const ep of OSRM_ENDPOINTS) {
      try {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), 12000);
        const res = await fetch(ep + '/' + coordStr + '?overview=full&geometries=geojson', { signal: ctrl.signal });
        clearTimeout(timer);
        if (!res.ok) continue;
        const data = await res.json();
        if (data.routes && data.routes[0] && data.routes[0].geometry) {
          const coords = data.routes[0].geometry.coordinates.map(c => [c[1], c[0]]);
          const km = data.routes[0].distance / 1000;
          const hr = data.routes[0].duration / 3600;
          const result = { coords, km, hr };
          try { localStorage.setItem(key, JSON.stringify(result)); } catch (e) {}
          return result;
        }
      } catch (e) {
        console.warn('[OSRM]', ep, 'failed:', e.message);
      }
    }
    return null;
  }

  // 总里程汇总容器
  function ensureSummaryUI() {
    let box = document.getElementById('trip-route-summary');
    if (box) return box;
    const mapEl = document.getElementById('map');
    if (!mapEl) return null;
    box = document.createElement('div');
    box.id = 'trip-route-summary';
    box.style.cssText = 'margin: 12px 0 18px; padding: 14px 16px; background: linear-gradient(135deg, #132a4f 0%, #1a3561 100%); border-radius: 10px; color: #e0e7ef; font-size: 13.5px; line-height: 1.7;';
    box.innerHTML = '<div style="display:flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">' +
      '<div><strong style="font-size:16px; color:#fff;">自驾里程汇总</strong> <span style="color:#90caf9;">Google/OSRM 真实路由</span></div>' +
      '<div id="trip-route-total" style="font-size: 16px; font-weight: 600; color: #90caf9;"><span id="trip-route-progress">加载 0/0</span></div>' +
      '</div>' +
      '<table style="width:100%; margin-top:10px; border-collapse: collapse; font-size:12.5px;"><thead><tr>' +
      '<th style="text-align:left; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.1); color:#90caf9; width:50px;">#</th>' +
      '<th style="text-align:center; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.1); color:#90caf9; width:55px;">方式</th>' +
      '<th style="text-align:left; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.1); color:#90caf9;">路段</th>' +
      '<th style="text-align:right; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.1); color:#90caf9; width:90px;">距离</th>' +
      '<th style="text-align:right; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.1); color:#90caf9; width:90px;">耗时</th>' +
      '<th style="text-align:right; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.1); color:#90caf9; width:70px;">导航</th>' +
      '</tr></thead><tbody id="trip-route-rows"></tbody></table>';
    mapEl.parentNode.insertBefore(box, mapEl.nextSibling);
    return box;
  }

  function addRow(idx, from, to, fromTitle, toTitle, km, hr, mode) {
    const rows = document.getElementById('trip-route-rows');
    if (!rows) return;
    const isFlight = mode === 'flight';
    const navUrl = isFlight
      ? 'https://www.google.com/flights?q=' + encodeURIComponent(fromTitle + ' to ' + toTitle)
      : 'https://www.google.com/maps/dir/?api=1&origin=' + from[0] + ',' + from[1] + '&destination=' + to[0] + ',' + to[1] + '&travelmode=driving';
    const navLabel = isFlight ? '航班' : '导航';
    const planeIcon = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ffb74d" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:middle;"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>';
    const carIcon = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#81c784" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:middle;"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>';
    const modeIcon = isFlight ? planeIcon : carIcon;
    const kmText = km != null ? (mode === 'drive-estimate' ? '≈ ' + km.toFixed(0) + ' km' : km.toFixed(1) + ' km') : '—';
    const hrText = hr != null ? (hr < 1 ? (hr * 60).toFixed(0) + ' min' : hr.toFixed(1) + ' h') : '—';
    const rowHtml = '<tr data-idx="' + idx + '"><td style="padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05); color:#90caf9;">' + (idx + 1) + '</td>' +
      '<td style="padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05); text-align:center;">' + modeIcon + '</td>' +
      '<td style="padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05);">' + fromTitle + ' → ' + toTitle + '</td>' +
      '<td style="padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05); text-align:right; font-weight:600;">' + kmText + '</td>' +
      '<td style="padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05); text-align:right;">' + hrText + '</td>' +
      '<td style="padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05); text-align:right;"><a href="' + navUrl + '" target="_blank" style="color:#4fc3f7;">' + navLabel + '</a></td></tr>';
    // 已存在同 idx 则替换，否则按 idx 顺序插入
    const existing = rows.querySelector('tr[data-idx="' + idx + '"]');
    if (existing) { existing.outerHTML = rowHtml; return; }
    const all = rows.querySelectorAll('tr[data-idx]');
    let inserted = false;
    for (const tr of all) {
      if (parseInt(tr.getAttribute('data-idx'), 10) > idx) {
        tr.insertAdjacentHTML('beforebegin', rowHtml);
        inserted = true;
        break;
      }
    }
    if (!inserted) rows.insertAdjacentHTML('beforeend', rowHtml);
  }

  function drawFlightSegment(idx) {
    const from = waypoints[idx];
    const to = waypoints[idx + 1];
    const style = { color: '#ffb74d', weight: 3, opacity: 0.85, dashArray: '10,8' };
    const line = L.polyline([from, to], style).addTo(map);
    const km = haversine(from, to);
    const label = '<strong>' + (idx + 1) + '. ' + titles[idx] + ' → ' + titles[idx + 1] + '（飞行）</strong>';
    line.bindPopup(label + '<br><small>飞行段 · 直线距离 ' + km.toFixed(0) + ' km</small>');
    // 航线中点放一个小飞机 SVG 标识
    const mid = [(from[0] + to[0]) / 2, (from[1] + to[1]) / 2];
    const planeSvg = '<svg width="22" height="22" viewBox="0 0 24 24" fill="#ffb74d" stroke="#fff" stroke-width="1" style="filter: drop-shadow(0 1px 2px rgba(0,0,0,0.6));"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>';
    L.marker(mid, {
      icon: L.divIcon({
        className: 'flight-marker',
        html: planeSvg,
        iconSize: [22, 22],
        iconAnchor: [11, 11]
      })
    }).addTo(map);
    addRow(idx, from, to, titles[idx], titles[idx + 1], km, null, 'flight');
    return Promise.resolve({ km, isFlight: true });
  }

  function drawSegment(idx) {
    if (flightSet.has(idx)) {
      return drawFlightSegment(idx);
    }
    const from = waypoints[idx];
    const to = waypoints[idx + 1];
    const color = routeColors[idx % routeColors.length];
    const style = { color, weight: 4, opacity: 0.85 };
    const fallback = L.polyline([from, to], { ...style, dashArray: '6,6', opacity: 0.5 }).addTo(map);
    const label = '<strong>' + (idx + 1) + '. ' + titles[idx] + ' → ' + titles[idx + 1] + '</strong>';
    fallback.bindPopup(label + '<br><small>正在加载真实路径…</small>');

    return fetchSegment(from, to).then(result => {
      if (result && result.coords && result.coords.length > 2) {
        map.removeLayer(fallback);
        const real = L.polyline(result.coords, style).addTo(map);
        real.bindPopup(label + '<br><small>实测 ' + result.km.toFixed(1) + ' km · ' + (result.hr < 1 ? (result.hr * 60).toFixed(0) + ' min' : result.hr.toFixed(2) + ' h') + '</small>');
        addRow(idx, from, to, titles[idx], titles[idx + 1], result.km, result.hr, 'drive');
        return { km: result.km, isFlight: false };
      } else {
        const hvKm = haversine(from, to);
        fallback.setPopupContent(label + '<br><small>路由不可达 · 直线估算 ' + hvKm.toFixed(0) + ' km</small>');
        addRow(idx, from, to, titles[idx], titles[idx + 1], hvKm, null, 'drive-estimate');
        return { km: hvKm, isFlight: false };
      }
    }).catch(err => {
      console.warn('[drawSegment]', idx, err);
      const hvKm = haversine(from, to);
      fallback.setPopupContent(label + '<br><small>加载异常 · 直线估算 ' + hvKm.toFixed(0) + ' km</small>');
      addRow(idx, from, to, titles[idx], titles[idx + 1], hvKm, null, 'drive-estimate');
      return { km: hvKm, isFlight: false };
    });
  }

  ensureSummaryUI();
  const total = waypoints.length - 1;
  let done = 0;
  let driveKm = 0, flyKm = 0;
  const progressEl = document.getElementById('trip-route-progress');
  const totalEl = document.getElementById('trip-route-total');
  const updateProgress = () => {
    const parts = [];
    if (driveKm > 0) parts.push('自驾 <span style="color:#81c784;">' + driveKm.toFixed(0) + ' km</span>');
    if (flyKm > 0) parts.push('飞行 <span style="color:#ffb74d;">' + flyKm.toFixed(0) + ' km</span>');
    if (done < total) {
      if (progressEl) progressEl.textContent = '加载 ' + done + '/' + total + ' · 路线获取中…';
      if (parts.length && totalEl) totalEl.innerHTML = '<span style="font-size:13px;color:#90caf9;">加载 ' + done + '/' + total + '</span>&nbsp;&nbsp;' + parts.join('  ·  ');
    } else {
      if (totalEl) {
        totalEl.style.fontSize = '20px';
        totalEl.style.fontWeight = '700';
        totalEl.style.color = '#4fc3f7';
        totalEl.innerHTML = parts.join('  ·  ') || '—';
      }
    }
  };
  updateProgress();

  // 并发限流：同时最多 3 个请求（OSRM 公共节点别压太狠）
  const CONCURRENCY = 3;
  let cursor = 0;
  async function worker() {
    while (cursor < total) {
      const i = cursor++;
      try {
        const r = await drawSegment(i);
        if (r) {
          if (r.isFlight) flyKm += (r.km || 0);
          else driveKm += (r.km || 0);
        }
      } catch (e) {
        console.warn('[segment]', i, e);
      }
      done++;
      updateProgress();
    }
  }
  const workers = [];
  for (let w = 0; w < Math.min(CONCURRENCY, total); w++) workers.push(worker());
  Promise.all(workers).then(updateProgress);
})();
`;

// 注入到最后一个 </script> 之前
const lastScriptIdx = html.lastIndexOf('</script>');
if (lastScriptIdx === -1) {
  console.error(`[${pageName}] 找不到 </script>，无法注入`);
  process.exit(3);
}
html = html.slice(0, lastScriptIdx) + scriptInject + '\n' + html.slice(lastScriptIdx);

// ========== 5. 底部 Google Maps 一键导航表格（保留 v1 行为） ==========
const gmapsRows = [];
for (let i = 0; i < markers.length - 1; i++) {
  const a = markers[i];
  const b = markers[i + 1];
  const isFlight = flightSegments.includes(i);
  const url = isFlight
    ? `https://www.google.com/flights?q=${encodeURIComponent(a.title + ' to ' + b.title)}`
    : `https://www.google.com/maps/dir/?api=1&origin=${a.lat},${a.lng}&destination=${b.lat},${b.lng}&travelmode=driving`;
  const label = isFlight ? '查航班' : '打开导航';
  gmapsRows.push(`
        <tr>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); font-size:13px; white-space:nowrap; color:#90caf9;">${i + 1}</td>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); font-size:13px;">${a.title}</td>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); font-size:13px; color:${isFlight ? '#ffb74d' : '#ffb74d'};">${isFlight ? '✈' : '→'}</td>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); font-size:13px;">${b.title}</td>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); white-space:nowrap;">
            <a href="${url}" target="_blank" rel="noopener" style="color:#4fc3f7; font-size:12px; text-decoration:none;">${label}</a>
          </td>
        </tr>`);
}

const gmapsSection = `

<!-- AUTO-PATCH v2: Google Maps / Flights 一键导航表格 -->
<section style="max-width:1100px; margin:24px auto; padding:0 16px;">
  <h2 style="color:#fff; font-size:18px; font-weight:600; margin:0 0 12px;">各路段一键导航</h2>
  <p style="color:#90caf9; font-size:12px; margin:0 0 12px; opacity:.75;">自驾段走 Google Maps 驾车路线，飞行段跳转 Google Flights 查航班。</p>
  <div style="overflow-x:auto; background:rgba(10,25,47,0.6); border:1px solid #1e4976; border-radius:8px;">
    <table style="width:100%; border-collapse:collapse;">
      <thead>
        <tr style="background:rgba(30,73,118,.45);">
          <th style="padding:10px; text-align:left; color:#e0e7ef; font-size:12px; font-weight:600;">#</th>
          <th style="padding:10px; text-align:left; color:#e0e7ef; font-size:12px; font-weight:600;">出发</th>
          <th style="padding:10px;"></th>
          <th style="padding:10px; text-align:left; color:#e0e7ef; font-size:12px; font-weight:600;">到达</th>
          <th style="padding:10px; text-align:left; color:#e0e7ef; font-size:12px; font-weight:600;">操作</th>
        </tr>
      </thead>
      <tbody>${gmapsRows.join('')}
      </tbody>
    </table>
  </div>
</section>
`;

let insertAnchor = html.indexOf('<footer');
if (insertAnchor === -1) insertAnchor = html.lastIndexOf('</body>');
if (insertAnchor === -1) {
  console.error(`[${pageName}] 找不到 <footer 或 </body>，无法插入导航表格`);
  process.exit(4);
}
html = html.slice(0, insertAnchor) + gmapsSection + html.slice(insertAnchor);

fs.writeFileSync(dst, html, 'utf8');
console.log(`[${pageName}] ✓ 已生成 ${dst}  (segments: ${markers.length - 1}, flights: ${flightSegments.length})`);
