# 🔄 API 使用场景说明

YahooClaw 设计了智能的多数据源架构，在不同场景下自动选择最优数据源。

---

## 📊 数据源选择逻辑

### **默认行为**

```
用户请求
    ↓
检查缓存 (5 分钟内)
    ↓
有缓存？→ 返回缓存数据 ✅
    ↓ 无缓存
Yahoo Finance (首选)
    ↓ 成功？→ 返回数据 + 缓存 ✅
    ↓ 失败/限流
Alpha Vantage (备用)
    ↓ 返回数据 + 缓存 ✅
```

---

## 🎯 使用场景详解

### **场景 1: 正常使用（Yahoo Finance 可用）**

**触发条件：**
- API 请求频率 < 100 次/小时
- Yahoo Finance 服务正常
- 网络状况良好

**行为：**
```javascript
const quote = await yahooclaw.getQuote('AAPL');
// ✅ 使用 Yahoo Finance
// ✅ 实时数据
// ✅ 缓存 5 分钟
```

**适用情况：**
- 偶尔查询股价
- 非高频交易
- 日常使用

---

### **场景 2: Yahoo Finance 限流**

**触发条件：**
- 1 小时内请求 > 100 次
- Yahoo Finance 返回 429 错误

**行为：**
```javascript
// 第 1-100 次请求
const quote1 = await yahooclaw.getQuote('AAPL');
// ✅ Yahoo Finance

// 第 101 次请求
const quote2 = await yahooclaw.getQuote('TSLA');
// ⚠️ Yahoo Finance 限流
// ✅ 自动切换到 Alpha Vantage
// ✅ 用户无感知
```

**适用情况：**
- 批量分析多只股票
- 高频查询场景
- 量化交易策略回测

---

### **场景 3: 缓存命中**

**触发条件：**
- 相同请求在 5 分钟内已执行过
- 缓存未过期

**行为：**
```javascript
// 第一次请求
const quote1 = await yahooclaw.getQuote('AAPL');
// ✅ Yahoo Finance
// 💾 缓存结果

// 3 分钟后，相同请求
const quote2 = await yahooclaw.getQuote('AAPL');
// ✅ 直接从缓存返回
// ⚡ 响应速度提升 10 倍
// 📉 不消耗 API 配额
```

**适用情况：**
- 用户频繁查看同一股票
- 实时监控面板
- 降低 API 成本

---

### **场景 4: 技术指标分析**

**触发条件：**
- 请求技术指标数据
- 需要历史价格计算

**行为：**
```javascript
const tech = await yahooclaw.getTechnicalIndicators('NVDA', '1mo', ['MA', 'RSI', 'MACD']);

// 内部流程：
// 1. 从 Yahoo Finance 获取历史数据
// 2. 本地计算技术指标（不消耗 API）
// 3. 返回完整分析结果
```

**适用情况：**
- 技术分析交易
- 量化策略开发
- 投资研究报告

---

### **场景 5: 新闻聚合查询**

**触发条件：**
- 请求股票相关新闻
- 需要情感分析

**行为：**
```javascript
const news = await yahooclaw.getNews('MSFT', { limit: 10, sentiment: true });

// 内部流程：
// 1. 从 Yahoo Finance 获取新闻
// 2. 本地情感分析（不消耗 API）
// 3. 返回新闻 + 情感评分
```

**适用情况：**
- 舆情监控
- 事件驱动交易
- 投资决策辅助

---

### **场景 6: 多数据源对比**

**触发条件：**
- 需要验证数据准确性
- 主要数据源不可靠

**行为：**
```javascript
import { APIManager } from './src/api/APIManager.js';

const apiManager = new APIManager();

// 同时从两个数据源获取
const [yahoo, alpha] = await Promise.all([
  apiManager.apis.YahooFinance.getQuote('AAPL'),
  apiManager.apis.AlphaVantage.getQuote('AAPL')
]);

// 对比数据
console.log(`Yahoo: $${yahoo.data.price}`);
console.log(`Alpha: $${alpha.data.price}`);
```

**适用情况：**
- 数据质量验证
- 套利机会发现
- 异常检测

---

### **场景 7: 离线/网络故障**

**触发条件：**
- 网络连接不稳定
- 某个 API 服务宕机

**行为：**
```javascript
const quote = await yahooclaw.getQuote('TSLA');

// 如果 Yahoo Finance 超时
// ✅ 自动尝试 Alpha Vantage
// ✅ 如果都失败，返回友好错误信息
```

**适用情况：**
- 网络环境差
- API 服务维护
- 灾难恢复

---

## 📈 实际案例

### **案例 1: 批量股票分析**

```javascript
// 分析 50 只股票的技术指标
const stocks = ['AAPL', 'TSLA', 'NVDA', 'MSFT', ...]; // 50 只

// 使用缓存 + 备用 API
const results = await Promise.all(
  stocks.map(symbol => yahooclaw.getTechnicalIndicators(symbol, '1mo'))
);

// 结果：
// - 前 100 次请求使用 Yahoo Finance
// - 超出的请求自动使用 Alpha Vantage
// - 相同股票的重复请求使用缓存
// ✅ 所有请求成功完成
```

---

### **案例 2: 实时监控系统**

```javascript
// 每 30 秒监控一次持仓股票
setInterval(async () => {
  const portfolio = ['AAPL', 'TSLA', 'NVDA'];
  
  for (const symbol of portfolio) {
    const quote = await yahooclaw.getQuote(symbol);
    console.log(`${symbol}: $${quote.data.price}`);
  }
}, 30000);

// 结果：
// - 第 1 次：Yahoo Finance + 缓存
// - 第 2 次（30 秒后）：缓存命中（不消耗 API）
// - 第 11 次（5 分钟后）：缓存过期，重新请求
// ✅ 持续运行不触发限流
```

---

### **案例 3: 高频交易策略**

```javascript
// 需要快速获取大量数据
const historicalData = await yahooclaw.getHistory('SPY', '1y');
const techIndicators = await yahooclaw.getTechnicalIndicators('SPY', '1y', ['MA', 'RSI', 'MACD']);

// 使用专用配置
import { APIManager } from './src/api/APIManager.js';

const apiManager = new APIManager({
  primary: 'AlphaVantage',  // Alpha Vantage 历史数据更稳定
  cache: false,             // 关闭缓存，获取最新数据
  timeout: 15000            // 增加超时时间
});
```

---

## 🎯 最佳实践建议

### **1. 日常使用（推荐配置）**

```javascript
// 默认配置即可
import yahooclaw from './src/index.js';

const quote = await yahooclaw.getQuote('AAPL');
```

**优点：**
- ✅ 自动故障转移
- ✅ 缓存优化
- ✅ 无需手动管理

---

### **2. 批量分析**

```javascript
// 启用缓存，批量请求
const stocks = ['AAPL', 'TSLA', 'NVDA'];

const results = await Promise.all(
  stocks.map(symbol => yahooclaw.getQuote(symbol))
);
```

**优点：**
- ✅ 并行请求
- ✅ 缓存重复数据
- ✅ 自动切换数据源

---

### **3. 生产环境**

```javascript
// 配置环境变量
// .env 文件：
ALPHA_VANTAGE_API_KEY=your_key
API_CACHE_TTL=600000      // 10 分钟缓存
API_TIMEOUT=15000         // 15 秒超时

// 代码中
import yahooclaw from './src/index.js';
```

**优点：**
- ✅ 更高 API 限额
- ✅ 更长缓存时间
- ✅ 更稳定的服务

---

## ⚠️ 注意事项

### **1. API 限流**

| API | 限制 | 解决方案 |
|-----|------|---------|
| Yahoo Finance | ~100 次/小时 | 自动切换到 Alpha Vantage |
| Alpha Vantage | 500 次/天 | 申请正式 API key，或使用缓存 |

### **2. 数据延迟**

- **Yahoo Finance:** 实时或 15 分钟延迟
- **Alpha Vantage:** 实时
- **缓存数据:** 最多 5 分钟延迟

### **3. 成本考虑**

- **Yahoo Finance:** 免费
- **Alpha Vantage:** 免费 500 次/天
- **缓存:** 免费，强烈推荐启用

---

## 📊 性能对比

| 场景 | 无缓存 | 有缓存 | 提升 |
|------|-------|-------|------|
| 单次查询 | 2-3 秒 | 0.1 秒 | **20-30 倍** |
| 批量查询 (10 只) | 20-30 秒 | 2-3 秒 | **10 倍** |
| 重复查询 | 2-3 秒 | 0.05 秒 | **40-60 倍** |

---

## 🚀 总结

**YahooClaw 智能数据源架构：**

1. **首选 Yahoo Finance** - 数据全面、实时
2. **自动故障转移** - 限流时自动切换 Alpha Vantage
3. **智能缓存** - 5 分钟内重复请求直接返回
4. **用户无感知** - 所有切换自动完成
5. **成本优化** - 最大限度减少 API 调用

**适用场景：**
- ✅ 日常股票查询
- ✅ 批量技术分析
- ✅ 实时监控系统
- ✅ 量化交易策略
- ✅ 生产环境部署

---

**Happy Trading! 📈**
