/**
 * YahooClaw TSLA 测试脚本
 */

import yahooclaw from './src/yahoo-finance.js';

console.log('🦞 YahooClaw TSLA 测试开始...\n');

// 1. 测试实时股价
console.log('📈 测试 1: 获取 TSLA 实时股价');
const quote = await yahooclaw.getQuote('TSLA');
if (quote.success) {
  console.log(`✅ TSLA 股价：$${quote.data.price}`);
  console.log(`   涨跌：${quote.data.change} (${quote.data.changePercent}%)`);
  console.log(`   市值：$${(quote.data.marketCap / 1e9).toFixed(2)}B\n`);
} else {
  console.log(`❌ 失败：${quote.message}\n`);
}

// 2. 测试技术指标
console.log('📊 测试 2: 获取 TSLA 技术指标');
const tech = await yahooclaw.getTechnicalIndicators('TSLA', '1mo', ['MA', 'RSI', 'MACD']);
if (tech.success) {
  console.log(`✅ 信号：${tech.data.analysis.signal}`);
  console.log(`   置信度：${tech.data.analysis.confidence}%`);
  console.log(`   建议：${tech.data.analysis.recommendation}\n`);
} else {
  console.log(`❌ 失败：${tech.message}\n`);
}

// 3. 测试新闻
console.log('📰 测试 3: 获取 TSLA 新闻');
const news = await yahooclaw.getNews('TSLA', { limit: 5, sentiment: true });
if (news.success) {
  console.log(`✅ 获取 ${news.data.count} 条新闻`);
  console.log(`   整体情感：${news.data.overallSentiment}`);
  console.log(`   利好：${news.data.sentimentStats.positive}`);
  console.log(`   利空：${news.data.sentimentStats.negative}\n`);
} else {
  console.log(`❌ 失败：${news.message}\n`);
}

console.log('✅ TSLA 测试完成！');
