#!/usr/bin/env node
/**
 * 验证所有25个公开API
 */
const { call } = require('./call-node.js');

const tests = [
  // 1. 主题分析 (7个)
  { name: 'themes', params: { pageNum: 1, pageSize: 3 } },
  { name: 'theme_indices', params: { themeId: '3' } },
  { name: 'theme_etfs', params: { themeId: '3' } },
  { name: 'theme_diagnose', params: { themeId: '1477062244' } },
  { name: 'theme_subs_diagnose', params: { themeId: '3' } },
  { name: 'theme_narratives', params: { themeId: '5900', startDate: '2026-08-01', endDate: '2026-08-13' } },
  { name: 'theme_contents', params: { themeId: 8, pageSize: 3, pageNum: 1, startDate: '2026-08-17', endDate: '2026-08-17', newsCategory: '事件' } },
  
  // 2. 榜单 (4个)
  { name: 'board_hotspots', params: { pageNum: '1', pageSize: '3' } },
  { name: 'board_hotspots_detail', params: { startTime: '2026-08-24', endTime: '2026-08-24' } },
  { name: 'board_hotspots_latest_detail', params: {} },
  { name: 'board_indices', params: { startDate: '2026-08-03', endDate: '2026-08-03' } },
  
  // 3. 热点 (10个)
  { name: 'hotspot_heats', params: { keywords: ['英伟达'], startTime: '2026-08-03 00:00:00', endTime: '2026-08-12 12:34:32' } },
  { name: 'hotspot_emotions', params: { keywords: ['AI'], startTime: '2026-08-13 00:00:00', endTime: '2026-08-17 13:34:32' } },
  { name: 'hotspot_news', params: { startTime: '2026-08-01', endTime: '2026-08-24', keywords: '英伟达' } },
  { name: 'hotspot_viewpoints', params: { startTime: '2026-07-09', endTime: '2026-07-14', keywords: '石油' } },
  { name: 'hotspot_securities', params: { startTime: '2026-08-17', endTime: '2026-08-17', keywords: 'AI', start: '0', end: '5' } },
  { name: 'hotspot_indices', params: { startTime: '2026-07-17', endTime: '2026-07-23', keywords: '标普石油' } },
  { name: 'hotspot_themes', params: { startTime: '2025-05-09', endTime: '2025-05-21', keywords: '华为' } },
  { name: 'hotspot_etfs', params: { startTime: '2026-08-19', endTime: '2026-08-19', keywords: '眼镜' } },
  { name: 'hotspot_policies', params: { startTime: '2026-01-17', endTime: '2026-01-21', keywords: 'AI' } },
  { name: 'hotspot_funds', params: { startTime: '2026-08-17', endTime: '2026-08-17', keywords: '智能机器人' } },
  
  // 4. 基金 (1个)
  { name: 'fund_narratives', params: { fundTicker: '516090' } },
  
  // 5. 指数 (2个)
  { name: 'index_detail', params: { indexTicker: 'HSTECH.HK' } },
  { name: 'index_daily', params: { indexTickers: '000001.SH,000300.SH', startDate: '2026-06-01', endDate: '2026-06-05' } },
  
  // 6. ETF (1个)
  { name: 'etf_narratives', params: { etfTicker: '159994' } },
];

async function runTest(test) {
  try {
    const result = await call(test.name, test.params);
    if (result.statusCode === 200) {
      const data = result.data;
      if (data.errCode === 0 || data.code === 0 || data.data) {
        return { success: true, name: test.name };
      } else {
        return { success: false, name: test.name, error: `errCode=${data.errCode}, code=${data.code}, msg=${data.errMsg || data.msg}` };
      }
    } else {
      return { success: false, name: test.name, error: `HTTP ${result.statusCode}` };
    }
  } catch (e) {
    return { success: false, name: test.name, error: e.message };
  }
}

async function main() {
  console.log('开始验证 25 个公开API...\n');
  console.log('='.repeat(60));
  
  let pass = 0, fail = 0;
  const failures = [];
  
  for (const test of tests) {
    process.stdout.write(`测试 ${test.name}... `);
    const result = await runTest(test);
    if (result.success) {
      console.log('✅');
      pass++;
    } else {
      console.log(`❌ ${result.error}`);
      fail++;
      failures.push(result);
    }
  }
  
  console.log('='.repeat(60));
  console.log(`\n验证完成: ✅ ${pass} 通过, ❌ ${fail} 失败`);
  
  if (failures.length > 0) {
    console.log('\n失败详情:');
    failures.forEach(f => {
      console.log(`  - ${f.name}: ${f.error}`);
    });
  }
}

main().catch(console.error);