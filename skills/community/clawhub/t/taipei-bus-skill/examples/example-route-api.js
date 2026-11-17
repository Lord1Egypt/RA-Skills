/**
 * example-route-api.js
 * 展示 PTX 公車路線 API（站序 + 精確 ETA）
 * 執行：node example-route-api.js
 */

const {
  searchRouteByName,
  searchRoutes,
  getRouteInfo,
  getRouteStopSequence,
  etaBySequence,
  getRoutesByStop,
  routeApi
} = require('../lib/bus-api.js');

function demo() {
  console.log('=== PTX 公車路線 API 示範 ===\n');

  // 1. 路名搜尋
  console.log('1️⃣ searchRouteByName() — 以路名查詢');
  for (const name of ['234', '棕1', '南京']) {
    const r = searchRouteByName(name);
    if (r) console.log(`   ✅ "${name}" → RouteID=${r.routeId} ${r.routeName} (${r.departure} → ${r.terminal})`);
  }
  console.log('');

  // 2. 模糊搜尋
  console.log('2️⃣ searchRoutes() — 模糊搜尋（"藍"）');
  const blues = searchRoutes('藍', 5);
  blues.forEach(r => console.log(`   🟦 ${r.routeName} (${r.routeId})`));
  console.log('');

  // 3. 路線完整資訊
  console.log('3️⃣ getRouteInfo() — 路線完整資訊');
  const route = searchRouteByName('234');
  if (route) {
    console.log(routeApi.formatRoute(route));
  }
  console.log('');

  // 4. 站序查詢
  console.log('4️⃣ getRouteStopSequence() — 站序查詢（路線 234 去程）');
  if (route) {
    const stops = getRouteStopSequence(route.routeId, 0);
    console.log(`   共 ${stops.length} 站，前5站:`);
    stops.slice(0, 5).forEach((s, i) =>
      console.log(`   ${i + 1}. ${s.stopName} (StopID=${s.stopId})`)
    );
    console.log('   ...');
    console.log(`   後3站:`);
    stops.slice(-3).forEach((s, i) =>
      console.log(`   ${stops.length - 3 + i + 1}. ${s.stopName} (StopID=${s.stopId})`)
    );
  }
  console.log('');

  // 5. 精確 ETA 估算（站序版）
  console.log('5️⃣ etaBySequence() — 依站序估算到站時間');
  if (route) {
    // 找第 10 站的 StopID
    const stops = getRouteStopSequence(route.routeId, 0);
    if (stops.length >= 10) {
      const midStop = stops[9]; // 第10站
      const eta = etaBySequence(route.routeId, midStop.stopId, 0);
      console.log(`   路線 ${route.routeName} → 目標站：${midStop.stopName}（StopID=${midStop.stopId}）`);
      console.log(`   ${eta.note}`);
      console.log(`   ⏱️  預估 ${eta.minutes} 分鐘`);
      console.log(`   📍 座標：(${midStop.lat?.toFixed(5)}, ${midStop.lon?.toFixed(5)})`);
    }
  }
  console.log('');

  // 6. 站點查經過路線
  console.log('6️⃣ getRoutesByStop() — 查某站有哪些路線經過');
  const stopId = '33210'; // 歡仔園
  const passingRoutes = getRoutesByStop(stopId);
  console.log(`   StopID=${stopId} (歡仔園) 有 ${passingRoutes.length} 條路線經過:`);
  passingRoutes.forEach(r =>
    console.log(`   🚌 ${r.routeName} 方向=${r.direction === 0 ? '去程' : '返程'} 第${r.index}站`)
  );
  console.log('');

  // 7. 格式化輸出
  console.log('7️⃣ formatStopSequence() — 格式化站序');
  if (route) {
    const stops = getRouteStopSequence(route.routeId, 0);
    if (stops.length >= 5) {
      const seq = routeApi.getStopSequence(route.routeId, stops[4].stopId, 0);
      console.log(routeApi.formatStopSequence(seq, route.routeId, 0));
    }
  }
}

demo();
