/**
 * example-eta.js — 到站時間預估範例
 * 說明：傳入路線代碼 + 目標站點代碼，估算到站時間
 */

const { etaEstimate, findByRoute } = require('../lib/bus-api.js');

async function main() {
  // 示範：可替換為你想查詢的路線與站點
  const DEMO_ROUTE = '158701'; // 替換為實際路線代碼
  const DEMO_STOP = '185365';  // 替換為實際站點代碼

  console.log(`🔍 查詢路線 ${DEMO_ROUTE} → 站點 ${DEMO_STOP} 的到站時間\n`);

  // 先確認該路線有車在線
  const buses = await findByRoute(DEMO_ROUTE);
  if (buses.length === 0) {
    console.log('⚠️ 目前無此路線公車在線');
    return;
  }

  // 估算到站時間
  const eta = await etaEstimate(DEMO_ROUTE, DEMO_STOP);
  if (eta.bus) {
    console.log(`✅ 估算到站時間：約 ${eta.minutes} 分鐘`);
    console.log(`📌 最近一台：${eta.bus.BusID}`);
    console.log(`   目前所在站：${eta.bus.StopID}`);
    console.log(`   行駛方向：${eta.bus.GoBack === '1' ? '去程' : '返程'}`);
    console.log(`   資料更新：${eta.bus.DataTime}`);
    console.log(`\n💡 ${eta.note}`);
  } else {
    console.log(eta.note);
  }
}

main().catch(console.error);
