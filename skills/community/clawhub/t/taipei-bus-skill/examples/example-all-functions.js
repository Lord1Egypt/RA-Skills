/**
 * example-all-functions.js
 * 展示 taipei-bus 所有函式（含 PTX 座標版）
 * 執行：node example-all-functions.js
 */

const {
  fetchAll,
  findByRoute,
  findByBus,
  findAtStation,
  etaEstimate,
  detectAnomalies,
  routeSummary,
  fetchAllWithCoords,
  getHotspots,
  getStopCoords,
  searchStops,
  formatBus
} = require('../lib/bus-api.js');

async function main() {
  console.log('=== 臺北市公車定點車機 OD（含 PTX 座標版）示範 ===\n');

  // 1. 抓全量資料
  console.log('1️⃣ fetchAll() — 全量即時資料（只顯示前5筆）');
  const all = await fetchAll();
  console.log(`   共 ${all.length} 台公車在線`);
  all.slice(0, 3).forEach(b => console.log('   ' + formatBus(b).split('\n')[0]));
  console.log('');

  // 2. 含座標版本
  console.log('2️⃣ fetchAllWithCoords() — 公車 + 站牌座標');
  const enriched = await fetchAllWithCoords();
  enriched.slice(0, 3).forEach(b => {
    const coord = b._stopCoords;
    const coordStr = coord ? `📍 ${coord.name}(${coord.lat?.toFixed(4)},${coord.lon?.toFixed(4)})` : '❓無座標';
    console.log(`   🚌 ${b.BusID} → ${coordStr}`);
  });
  console.log('');

  // 3. 依路線查
  console.log('3️⃣ findByRoute() — 查特定路線');
  if (all.length > 0) {
    const sampleRoute = all[0].RouteID;
    const routeBuses = await findByRoute(sampleRoute);
    console.log(`   路線 ${sampleRoute} 目前有 ${routeBuses.length} 台車在線`);
  }
  console.log('');

  // 4. 依車牌查
  console.log('4️⃣ findByBus() — 以車牌查單台公車');
  if (all.length > 0) {
    const sampleBus = all[0].BusID;
    const bus = await findByBus(sampleBus);
    if (bus) console.log(formatBus(bus, true));
  }
  console.log('');

  // 5. 站點查停靠公車
  console.log('5️⃣ findAtStation() — 查某站停靠公車');
  if (all.length > 0) {
    const sampleStop = all[0].StopID;
    const atStation = await findAtStation(sampleStop);
    console.log(`   站點 ${sampleStop} 共有 ${atStation.length} 台車停靠`);
  }
  console.log('');

  // 6. 站名搜尋（PTX 座標查詢）
  console.log('6️⃣ searchStops() — 站名搜尋');
  const found = searchStops('捷運', 5);
  found.forEach(s => console.log(`   🔍 StopID=${s.stopId} ${s.name} (${s.lat?.toFixed(4)},${s.lon?.toFixed(4)})`));
  console.log('');

  // 7. 座標查詢
  console.log('7️⃣ getStopCoords() — 依 StopID 查座標');
  const coords = getStopCoords('33210');
  if (coords) console.log(`   ✅ StopID=33210: ${coords.name} (${coords.lat}, ${coords.lon})`);
  console.log('');

  // 8. 到站時間估算（含座標）
  console.log('8️⃣ etaEstimate() — 到站時間估算（含實際距離）');
  if (all.length > 0) {
    const sampleRoute = all[0].RouteID;
    const sampleStop = all[0].StopID;
    const eta = await etaEstimate(sampleRoute, sampleStop);
    if (eta.bus) {
      console.log(`   路線 ${sampleRoute} → 站點 ${sampleStop}`);
      console.log(`   ${eta.note}`);
      console.log(`   預估 ${eta.minutes} 分鐘，車牌: ${eta.bus.BusID}`);
    }
  }
  console.log('');

  // 9. 熱點站位
  console.log('9️⃣ getHotspots() — 公車密度最高的站點');
  const hotspots = await getHotspots(5);
  hotspots.forEach((h, i) => {
    console.log(`   ${i + 1}. ${h.stopName} (${h.lat?.toFixed(4)},${h.lon?.toFixed(4)}) — ${h.count} 台公車`);
  });
  console.log('');

  // 10. 異常偵測
  console.log('🔟 detectAnomalies() — 偵測異常公車');
  const anomalies = await detectAnomalies();
  console.log(`   發現 ${anomalies.length} 台異常公車`);
  console.log('');
}

main().catch(console.error);
