/**
 * YahooClaw 重构后测试脚本
 * 测试所有模块功能是否正常
 */

import yahooclaw from '../src/index.js';
import { QuoteModule } from '../src/modules/Quote.js';
import { HistoryModule } from '../src/modules/History.js';
import { TechnicalModule } from '../src/modules/Technical.js';
import { NewsModule } from '../src/modules/News.js';

console.log('🦞 YahooClaw 重构测试开始...\n');

let passed = 0;
let failed = 0;

// 测试 1: Quote 模块
console.log('📈 测试 1: Quote 模块');
try {
  const quoteModule = new QuoteModule();
  const result = await quoteModule.getQuote('AAPL');
  
  if (result.success && result.data.price > 0) {
    console.log(`✅ AAPL 股价：$${result.data.price}`);
    passed++;
  } else {
    console.log(`❌ 失败：${result.message}`);
    failed++;
  }
} catch (error) {
  console.log(`❌ 错误：${error.message}`);
  failed++;
}
console.log('');

// 测试 2: History 模块
console.log('📊 测试 2: History 模块');
try {
  const historyModule = new HistoryModule();
  const result = await historyModule.getHistory('TSLA', '5d');
  
  if (result.success && result.data.quotes.length > 0) {
    console.log(`✅ TSLA 历史数据：${result.data.quotes.length} 条记录`);
    passed++;
  } else {
    console.log(`❌ 失败：${result.message}`);
    failed++;
  }
} catch (error) {
  console.log(`❌ 错误：${error.message}`);
  failed++;
}
console.log('');

// 测试 3: Technical 模块
console.log('📉 测试 3: Technical 模块');
try {
  const techModule = new TechnicalModule();
  
  // 模拟数据
  const closes = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 110];
  const highs = [101, 103, 102, 104, 106, 105, 107, 109, 108, 110, 111];
  const lows = [99, 101, 100, 102, 104, 103, 105, 107, 106, 108, 109];
  
  const result = techModule.calculate(closes, highs, lows, ['MA', 'RSI', 'MACD']);
  
  if (result.indicators.MA && result.indicators.RSI) {
    console.log(`✅ 技术指标计算成功`);
    console.log(`   MA5: ${result.indicators.MA.MA5?.value}`);
    console.log(`   RSI: ${result.indicators.RSI.RSI14}`);
    console.log(`   信号：${result.analysis.signal} (${result.analysis.confidence}%)`);
    passed++;
  } else {
    console.log(`❌ 失败：指标计算错误`);
    failed++;
  }
} catch (error) {
  console.log(`❌ 错误：${error.message}`);
  failed++;
}
console.log('');

// 测试 4: News 模块
console.log('📰 测试 4: News 模块');
try {
  const newsModule = new NewsModule();
  const result = await newsModule.getNews('NVDA', { limit: 3, sentiment: true });
  
  if (result.success) {
    console.log(`✅ NVDA 新闻：${result.data.count} 条`);
    console.log(`   整体情感：${result.data.overallSentiment}`);
    console.log(`   利好：${result.data.sentimentStats.positive}`);
    console.log(`   利空：${result.data.sentimentStats.negative}`);
    passed++;
  } else {
    console.log(`❌ 失败：${result.message}`);
    failed++;
  }
} catch (error) {
  console.log(`❌ 错误：${error.message}`);
  failed++;
}
console.log('');

// 测试 5: 主类兼容性
console.log('🔄 测试 5: 主类兼容性测试');
try {
  const result = await yahooclaw.getQuote('MSFT');
  
  if (result.success && result.data.price > 0) {
    console.log(`✅ MSFT 股价（旧 API）: $${result.data.price}`);
    passed++;
  } else {
    console.log(`❌ 失败：${result.message}`);
    failed++;
  }
} catch (error) {
  console.log(`❌ 错误：${error.message}`);
  failed++;
}
console.log('');

// 测试结果
console.log('='.repeat(50));
console.log(`✅ 通过：${passed}`);
console.log(`❌ 失败：${failed}`);
console.log(`📊 成功率：${((passed / (passed + failed)) * 100).toFixed(1)}%`);
console.log('='.repeat(50));

if (failed === 0) {
  console.log('\n🎉 所有测试通过！重构成功！');
} else {
  console.log(`\n⚠️ 有 ${failed} 个测试失败，请检查`);
}
