/**
 * YahooClaw 快速测试脚本
 * 测试技能是否正常工作
 */

import yahooclaw from './src/index.js';

console.log('🦞 YahooClaw 技能测试开始...\n');

// 测试查询股价
console.log('📈 测试查询 AAPL 股价...');
const aapl = await yahooclaw.getQuote('AAPL');
if (aapl.success) {
  console.log(`✅ AAPL: $${aapl.data.price} (${aapl.data.change > 0 ? '+' : ''}${aapl.data.changePercent}%)`);
} else {
  console.log(`⚠️  ${aapl.message}`);
}

console.log('\n📊 测试查询 TSLA 历史数据...');
const tsla = await yahooclaw.getHistory('TSLA', '5d');
if (tsla.success) {
  console.log(`✅ TSLA: ${tsla.data.quotes.length} 条历史记录`);
} else {
  console.log(`⚠️  ${tsla.message}`);
}

console.log('\n📉 测试 NVDA 技术指标...');
const nvda = await yahooclaw.getTechnicalIndicators('NVDA', '1mo', ['MA', 'RSI', 'MACD']);
if (nvda.success) {
  console.log(`✅ NVDA 信号：${nvda.data.analysis.signal} (${nvda.data.analysis.confidence}%)`);
  console.log(`   建议：${nvda.data.analysis.recommendation}`);
} else {
  console.log(`⚠️  ${nvda.message}`);
}

console.log('\n📰 测试 MSFT 新闻...');
const msft = await yahooclaw.getNews('MSFT', { limit: 3, sentiment: true });
if (msft.success) {
  console.log(`✅ MSFT: ${msft.data.news.length} 条新闻`);
  console.log(`   整体情感：${msft.data.overallSentiment}`);
} else {
  console.log(`⚠️  ${msft.message}`);
}

console.log('\n✅ 测试完成！');
