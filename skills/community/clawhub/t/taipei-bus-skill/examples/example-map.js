/**
 * example-map.js — 公車動態地圖範例
 *
 * 說明：生成一張互動地圖 HTML，疊加所有在線公車位置
 *
 * ⚠️  本 API（TstBusEvent.json）只有 StopID，沒有經緯度座標
 *     此範例需要搭配「臺北市公車站牌 API」取得座標後才能正常渲染地圖
 *
 * 站牌 API：https://data.taipei/dataset/detail?id=4e1014b8-ead7-4bc4-b32c-d427ea784cfe
 *
 * 如只需要以 StopID 顯示，目前建議：
 * 1. 先用 fetchAll() 取得所有公車 StopID
 * 2. 額外串站牌 API 取得 StopID → 經緯度對照表
 * 3. 再渲染騰訊地圖
 *
 * 本範例為框架參考，實作時請替換 STATION_COORDS 為真實座標查詢結果
 */

const { fetchAll, routeSummary } = require('../lib/bus-api.js');

// ============================================================
// 騰訊地圖 JSAPI HTML 範本（已含公車疊加層邏輯）
// ============================================================
function generateMapHTML(busesWithCoords, routeFilter = null) {
  const busMarkers = busesWithCoords
    .filter(b => !routeFilter || b.RouteID === routeFilter)
    .map(b => `{
      id: '${b.BusID}',
      lat: ${b.lat},
      lng: ${b.lng},
      route: '${b.RouteID}',
      status: '${b.CarOnStop === '1' ? '停站' : '行駛中'}',
      direction: '${b.GoBack === '1' ? '去程' : '返程'}',
      updated: '${b.DataTime}'
    }`)
    .join(',\n');

  return `<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>臺北市公車動態地圖</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
    #map { width: 100vw; height: 100vh; }
    #panel {
      position: absolute; top: 16px; left: 16px; z-index: 1000;
      background: rgba(255,255,255,0.95); border-radius: 12px;
      padding: 16px; width: 280px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    #panel h2 { font-size: 16px; margin-bottom: 12px; color: #1a1a2e; }
    #panel select, #panel button {
      width: 100%; padding: 8px 12px; margin-bottom: 8px;
      border: 1px solid #ddd; border-radius: 8px; font-size: 14px;
    }
    #panel button {
      background: #4a90d9; color: white; border: none; cursor: pointer;
    }
    #panel button:hover { background: #3a7fc9; }
    #stats { font-size: 13px; color: #555; margin-top: 8px; }
    .legend {
      display: flex; gap: 12px; margin-top: 10px; font-size: 12px;
    }
    .legend span { display: flex; align-items: center; gap: 4px; }
    .dot { width: 10px; height: 10px; border-radius: 50%; }
    .dot-moving { background: #4a90d9; }
    .dot-stopped { background: #e74c3c; }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="panel">
    <h2>🚌 臺北市公車動態</h2>
    <select id="routeFilter">
      <option value="">全部路線</option>
    </select>
    <button onclick="refreshMap()">🔄 重新整理</button>
    <div id="stats">載入中...</div>
    <div class="legend">
      <span><div class="dot dot-moving"></div>行駛中</span>
      <span><div class="dot dot-stopped"></div>停站中</span>
    </div>
  </div>

  <!-- 騰訊地圖 JSAPI (請替換 YOUR_API_KEY) -->
  <script src="https://map.qq.com/api/gljs?v=2.exp&key=YOUR_TENCENT_MAP_API_KEY"></script>
  <script>
    const busData = [${busMarkers}];

    // 初始化地圖（預設中心：臺北市政府）
    const center = new TMap.LatLng(25.0376, 121.5637);
    const map = new TMap.Map(document.getElementById('map'), {
      center, zoom: 13, pitch: 0, mapStyle: 'night'
    });

    // 公車標記層
    const markerLayer = new TMap.MultiMarker({
      map,
      geometries: busData.map(b => ({
        id: b.id,
        position: new TQLatLng(b.lat, b.lng),
        properties: b,
        icon: new TMap.Symbol({
          style: b.status === '停站' ? 'circle' : 'circle',
          color: b.status === '停站' ? 'rgba(231,76,60,0.8)' : 'rgba(74,144,217,0.8)',
          size: 14
        })
      }))
    });

    // 填充路線篩選下拉選單
    const routes = [...new Set(busData.map(b => b.route))];
    const sel = document.getElementById('routeFilter');
    routes.forEach(r => sel.add(new Option(r, r)));
    sel.addEventListener('change', () => refreshMap(sel.value));

    // 更新統計
    document.getElementById('stats').innerHTML =
      \`📊 共 \${busData.length} 台公車\` +
      \`<br>🛣 \${routes.length} 條路線\`;

    function refreshMap(route) {
      // 重新過濾標記（實際專案可配合站牌 API 即時更新座標）
      document.getElementById('stats').innerHTML = \`已篩選：\${route || '全部'}\`;
    }
  </script>
</body>
</html>`;
}

// ============================================================
// 使用範例
// ============================================================
async function main() {
  console.log('⚠️  注意：本範例需要站牌 API 提供座標資料才能完整運作');
  console.log('    站牌 API：https://data.taipei/dataset/detail?id=4e1014b8-ead7-4bc4-b32c-d427ea784cfe\n');

  const summary = await routeSummary();
  const routes = Object.keys(summary);
  console.log(`📊 目前系統共 ${routes.length} 條路線有公車在線\n`);

  // 示範如何對應座標（需額外串站牌 API）
  // const all = await fetchAll();
  // const stopIds = [...new Set(all.map(b => b.StopID))];
  // console.log(`共 ${stopIds.length} 個站點有公車經過`);

  console.log('✅ 地圖框架已就緒，請串接站牌座標 API 後即可使用 generateMapHTML()');
}

main().catch(console.error);
