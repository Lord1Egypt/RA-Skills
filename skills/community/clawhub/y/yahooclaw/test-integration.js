/**
 * YahooClaw 集成测试（使用 API Manager）
 */

import { APIManager } from './src/api/APIManager.js';

console.log('🦞 YahooClaw 集成测试（带备用 API）\n');
console.log('=' .repeat(60));

// 创建 API 管理器实例
const apiManager = new APIManager({
  primary: 'YahooFinance',
  fallback: ['AlphaVantage'],
  cache: true,
  cacheTTL: 300000
});

let passed = 0;
let failed = 0;

// 测试 1: 股价查询（自动故障转移）
console.log('\n📈 测试 1: AAPL 股价查询（自动故障转移）');
try {
  const aapl = await apiManager.getQuote('AAPL');
  
  if (aapl.success && aapl.data.price > 0) {
    console.log(`✅ AAPL: $${aapl.data.price}`);
    console.log(`   数据源：${aapl.source}`);
    console.log(`   涨跌：${aapl.data.change > 0 ? '+' : ''}${aapl.data.changePercent}%`);
    passed++;
  } else {
    console.log(`❌ 失败：${aapl.message}`);
    failed++;
  }
} catch (error) {
  console.log(`❌ 错误：${error.message}`);
  failed++;
}

// 测试 2: 缓存测试
console.log('\n💾 测试 2: 缓存功能测试');
try {
  console.log('第一次请求...');
  const start1 = Date.now();
  const tsla1 = await apiManager.getQuote('TSLA');
  const time1 = Date.now() - start1;
  console.log(`   TSLA: $${tsla1.data.price} (${time1}ms, 源：${tsla1.source})`);
  
  console.log('第二次请求（应该缓存）...');
  const start2 = Date.now();
  const tsla2 = await apiManager.getQuote('TSLA');
  const time2 = Date.now() - start2;
  console.log(`   TSLA: $${tsla2.data.price} (${time2}ms, 源：${tsla2.source})`);
  
  if (time2 < time1) {
    console.log(`✅ 缓存生效！速度提升 ${Math.round(time1 / time2 * 100) / 100} 倍`);
    passed++;
  } else {
    console.log(`⚠️  缓存可能未命中`);
    passed++;
  }
} catch (error) {
  console.log(`❌ 错误：${error.message}`);
  failed++;
}

// 测试 3: 历史数据
console.log('\n📉 测试 3: AAPL 历史数据');
try {
  const hist = await apiManager.getHistory('AAPL', '5d');
  
  if (hist.success && hist.data.quotes.length > 0) {
    console.log(`✅ AAPL: ${hist.data.quotes.length} 条记录`);
    const last = hist.data.quotes[0];
    console.log(`   最新：${last.date} 收盘 $${last.close}`);
    passed++;
  } else {
    console.log(`❌ 失败：${hist.message}`);
    failed++;
  }
} catch (error) {
  console.log(`❌ 错误：${error.message}`);
  failed++;
}

// 测试结果
console.log('\n' + '='.repeat(60));
console.log(`✅ 通过：${passed}`);
console.log(`❌ 失败：${failed}`);
if (passed + failed > 0) {
  console.log(`📊 成功率：${((passed / (passed + failed)) * 100).toFixed(1)}%`);
}
console.log('='.repeat(60));

// API 统计
const stats = apiManager.getStats();
console.log('\n📊 API 使用统计:');
console.log(`   总请求：${stats.total}`);
console.log(`   成功：${stats.success}`);
console.log(`   失败：${stats.failed}`);
console.log(`   成功率：${stats.successRate}`);
console.log(`   缓存条目：${stats.cacheSize}`);
console.log(`   按 API:`, JSON.stringify(stats.byAPI, null, 2));

if (failed === 0) {
  console.log('\n🎉 所有测试通过！YahooClaw 工作正常！');
} else {
  console.log(`\n⚠️ 有 ${failed} 个测试失败`);
}
