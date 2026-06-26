#!/usr/bin/env node
/**
 * 给 trip 单页补两件事：
 *   1) leaflet 地图上按 marker 顺序画折线（优先走 OSRM 真实路由，失败回退直线）
 *   2) 页面底部插入"各路段一键 Google Maps 导航"表格
 *
 * 用法：
 *   node patch-trip-page.js <page-name>
 *   其中 <page-name> 会映射到 /var/www/trip/<page-name>/index.html
 *   本脚本假设已经用 scp 拉到 /tmp/<page-name>.html 做本地处理，处理完输出 /tmp/<page-name>_patched.html
 *
 * 设计原则：
 *   - 不改动已有 marker / 内容，只追加 <style>、<script>、一段表格 HTML
 *   - 路线段按 marker 在源码中出现的顺序串接，天然就是行程顺序（各页 marker 本来就是按天排的）
 *   - 无坐标编造：全部 lat/lng 从原页面已有 L.marker 提取
 */

const fs = require('fs');
const path = require('path');

const pageName = process.argv[2];
if (!pageName) {
  console.error('Usage: node patch-trip-page.js <page-name>');
  process.exit(1);
}

const src = `/tmp/${pageName}.html`;
const dst = `/tmp/${pageName}_patched.html`;

let html = fs.readFileSync(src, 'utf8');

// ========== 1. 提取所有 marker：坐标 + popup 主标题 ==========
const markerRe = /L\.marker\(\[\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\][\s\S]*?\.bindPopup\((['"])([\s\S]*?)\3\s*\)/g;
const titleRe = /<strong>([^<]+)<\/strong>/;

const markers = [];
let m;
while ((m = markerRe.exec(html)) !== null) {
  const lat = parseFloat(m[1]);
  const lng = parseFloat(m[2]);
  const popup = m[4];
  const titleMatch = popup.match(titleRe);
  const fullTitle = titleMatch ? titleMatch[1].trim() : `点${markers.length + 1}`;
  markers.push({ lat, lng, title: fullTitle });
}

if (markers.length < 2) {
  console.error(`[${pageName}] 解析到 marker 数量 ${markers.length} < 2，无法构建路线`);
  process.exit(2);
}

console.log(`[${pageName}] 提取 ${markers.length} 个 marker：`);
markers.forEach((p, i) => console.log(`  ${i + 1}. (${p.lat}, ${p.lng}) ${p.title}`));

// ========== 2. 构造 polyline 注入脚本 ==========
const waypointsJSON = JSON.stringify(markers.map(p => [p.lat, p.lng]));
const titlesJSON = JSON.stringify(markers.map(p => p.title));

const scriptInject = `

// ===== AUTO-PATCH: 路线渲染（OSRM 真实路由 + 本地缓存，失败回退直线）=====
(function() {
  if (typeof map === 'undefined' || !map) return;

  const waypoints = ${waypointsJSON};
  const titles = ${titlesJSON};
  const OSRM_ENDPOINTS = [
    'https://router.project-osrm.org/route/v1/driving',
    'https://routing.openstreetmap.de/routed-car/route/v1/driving'
  ];
  const routeColors = ['#4fc3f7', '#81c784', '#ffb74d', '#ba68c8', '#f06292', '#4dd0e1', '#ff8a65', '#aed581'];

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
        const timer = setTimeout(() => ctrl.abort(), 10000);
        const res = await fetch(ep + '/' + coordStr + '?overview=full&geometries=geojson', { signal: ctrl.signal });
        clearTimeout(timer);
        if (!res.ok) continue;
        const data = await res.json();
        if (data.routes && data.routes[0] && data.routes[0].geometry) {
          const coords = data.routes[0].geometry.coordinates.map(c => [c[1], c[0]]);
          const km = (data.routes[0].distance / 1000).toFixed(1);
          const hr = (data.routes[0].duration / 3600).toFixed(2);
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

  function drawSegment(idx) {
    const from = waypoints[idx];
    const to = waypoints[idx + 1];
    const color = routeColors[idx % routeColors.length];
    const style = { color, weight: 4, opacity: 0.85 };
    const fallback = L.polyline([from, to], { ...style, dashArray: '6,6', opacity: 0.5 }).addTo(map);
    const label = '<strong>' + (idx + 1) + '. ' + titles[idx] + ' → ' + titles[idx + 1] + '</strong>';
    fallback.bindPopup(label + '<br><small>正在加载真实路径…</small>');

    fetchSegment(from, to).then(result => {
      if (result && result.coords && result.coords.length > 2) {
        map.removeLayer(fallback);
        const real = L.polyline(result.coords, style).addTo(map);
        real.bindPopup(label + '<br><small>实测 ' + result.km + ' km · ' + result.hr + ' 小时</small>');
      } else {
        fallback.setPopupContent(label + '<br><small>路由服务不可达，显示直线估算</small>');
      }
    });
  }

  for (let i = 0; i < waypoints.length - 1; i++) drawSegment(i);
})();
`;

// 注入到 </script> 之前（找最后一个 </script>）
const lastScriptIdx = html.lastIndexOf('</script>');
if (lastScriptIdx === -1) {
  console.error(`[${pageName}] 找不到 </script>，无法注入`);
  process.exit(3);
}
html = html.slice(0, lastScriptIdx) + scriptInject + '\n' + html.slice(lastScriptIdx);

// ========== 3. 构造 Google Maps 导航表格 ==========
const gmapsRows = [];
for (let i = 0; i < markers.length - 1; i++) {
  const a = markers[i];
  const b = markers[i + 1];
  const url = `https://www.google.com/maps/dir/?api=1&origin=${a.lat},${a.lng}&destination=${b.lat},${b.lng}&travelmode=driving`;
  gmapsRows.push(`
        <tr>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); font-size:13px; white-space:nowrap; color:#90caf9;">${i + 1}</td>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); font-size:13px;">${a.title}</td>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); font-size:13px; color:#ffb74d;">→</td>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); font-size:13px;">${b.title}</td>
          <td style="padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.08); white-space:nowrap;">
            <a href="${url}" target="_blank" rel="noopener" style="color:#4fc3f7; font-size:12px; text-decoration:none; display:inline-flex; align-items:center; gap:4px;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
              打开导航
            </a>
          </td>
        </tr>`);
}

const gmapsSection = `

<!-- AUTO-PATCH: Google Maps 导航表格 -->
<section style="max-width:1100px; margin:24px auto; padding:0 16px;">
  <h2 style="color:#fff; font-size:18px; font-weight:600; margin:0 0 12px; display:flex; align-items:center; gap:8px;">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4fc3f7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 7-8 13-8 13s-8-6-8-13a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
    各路段 Google Maps 一键导航
  </h2>
  <p style="color:#90caf9; font-size:12px; margin:0 0 12px; opacity:.75;">点击"打开导航"会在 Google Maps 用真实坐标打开该段驾车路线，可继续优化或发到手机继续导航。</p>
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

// 插到 <footer 之前（找不到就插到 </body> 前）
let insertAnchor = html.indexOf('<footer');
if (insertAnchor === -1) insertAnchor = html.lastIndexOf('</body>');
if (insertAnchor === -1) {
  console.error(`[${pageName}] 找不到 <footer 或 </body>，无法插入导航表格`);
  process.exit(4);
}
html = html.slice(0, insertAnchor) + gmapsSection + html.slice(insertAnchor);

fs.writeFileSync(dst, html, 'utf8');
console.log(`[${pageName}] ✓ 已生成 ${dst}  (segments: ${markers.length - 1})`);
