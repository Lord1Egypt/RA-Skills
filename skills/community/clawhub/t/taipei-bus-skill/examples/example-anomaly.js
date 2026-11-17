/**
 * example-anomaly.js — 公車脫班 / 異常偵測範例
 * 偵測：DutyStatus !== '1' 或 BusStatus !== '0' 的公車
 */

const { detectAnomalies, formatBus, fetchAll } = require('../lib/bus-api.js');

async function main() {
  console.log('🔎 全系統公車異常偵測\n');

  const anomalies = await detectAnomalies();

  if (anomalies.length === 0) {
    console.log('✅ 目前無偵測到異常公車（全數正常行駛）');
    return;
  }

  console.log(`⚠️  共偵測到 ${anomalies.length} 台異常公車：\n`);
  anomalies.forEach(bus => {
    const reason = [];
    if (bus.DutyStatus !== '1') reason.push(`勤務異常(${bus.DutyStatus})`);
    if (bus.BusStatus !== '0') reason.push(`狀態異常(${bus.BusStatus})`);
    console.log(`--- ${bus.BusID} ---`);
    console.log(`   路線: ${bus.RouteID} | 站點: ${bus.StopID}`);
    console.log(`   🚨 ${reason.join('、')}`);
    console.log(`   更新: ${bus.DataTime}\n`);
  });
}

main().catch(console.error);
