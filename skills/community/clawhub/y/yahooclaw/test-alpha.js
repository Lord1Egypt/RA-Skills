/**
 * 测试 Alpha Vantage 备用 API
 */

import { AlphaVantageAPI } from './src/api/AlphaVantage.js';

console.log('🧪 测试 Alpha Vantage 备用 API\n');

const alphaVantage = new AlphaVantageAPI({
  apiKey: '9Z6PTPL7AB5M5DN3'
});

// 测试 1: 查询股价
console.log('📈 测试：查询 AAPL 股价...');
const quote = await alphaVantage.getQuote('AAPL');

if (quote.success) {
  console.log(`✅ AAPL: $${quote.data.price}`);
  console.log(`   数据源：${quote.source}`);
  console.log(`   涨跌：${quote.data.change}`);
} else {
  console.log(`❌ 失败：${quote.message}`);
  console.log(`   错误：${quote.error}`);
}

// 测试 2: 查询历史数据
console.log('\n📊 测试：查询 TSLA 历史数据...');
const history = await alphaVantage.getHistory('TSLA', '1mo');

if (history.success) {
  console.log(`✅ TSLA: ${history.data.count} 条历史记录`);
  if (history.data.quotes.length > 0) {
    const last = history.data.quotes[0];
    console.log(`   最新：${last.date} 收盘价 $${last.close}`);
  }
} else {
  console.log(`❌ 失败：${history.message}`);
}

console.log('\n✅ Alpha Vantage API 测试完成！');
