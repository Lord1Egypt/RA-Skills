---
name: gold-price-query
description: This skill retrieves real-time precious metal prices (gold, silver, platinum, palladium, etc.) from https://i.jzj9999.com/quoteh5. It provides bid/ask prices, daily high/low prices, and price trends for 20+ metal types.
---

# 金价查询 Skill

从 https://i.jzj9999.com/quoteh5 页面获取实时的贵金属价格信息，包括黄金、白银等贵金属的回购价格、销售价格以及高低价。

## 功能描述

- 查询实时黄金、白银等贵金属价格
- 获取贵金属的回购和销售价格对比
- 了解当日贵金属价格波动范围（高/低价）
- 投资参考和价格监控

## 使用场景

- **投资者**: 实时监控贵金属价格，把握投资时机
- **珠宝行业**: 获取实时金价，优化采购定价策略
- **收藏家**: 了解贵金属市场行情，辅助收藏决策
- **企业用户**: 价格趋势分析，制定采购计划

## 数据来源

- **网站**: 融通金 (https://i.jzj9999.com/quoteh5)
- **数据类型**: 实时贵金属行情
- **更新频率**: 实时

## 支持的贵金属品种

### 黄金类
- 黄金9999
- 黄金T+D
- 黄金现货
- 美黄金
- 伦敦金

### 白银类
- 白银现货
- 白银T+D
- 美白银
- 伦敦银

### 铂金类
- 铂金现货
- 铂金9995
- 美铂金
- 伦敦铂

### 钯金类
- 钯金现货
- 美钯金
- 伦敦钯

### 稀有金属
- 铑金
- 铱
- 钌

### 其他
- 美元汇率

## 数据格式说明

每个贵金属品种返回以下数据：

```json
{
  "name": "品种名称",
  "bidPrice": "回购价格",
  "askPrice": "销售价格",
  "high": "当日最高价",
  "low": "当日最低价",
  "bidTrend": "回购价涨跌趋势 (up/down/flat)",
  "askTrend": "销售价涨跌趋势 (up/down/flat)",
  "updateTime": "更新时间"
}
```

## 使用方法

### 方式一：直接运行脚本

```bash
# 安装依赖
npm install

# 运行脚本
npm start
```

### 方式二：作为模块使用

```javascript
const { getGoldPrices, formatPrices } = require('./index');

async function main() {
  const prices = await getGoldPrices();
  console.log(formatPrices(prices));
}

main();
```

### 方式三：使用 Playwright MCP Tool

如果在支持Playwright MCP的环境中使用，可以直接使用：

```javascript
// 获取页面快照并解析
state.page = context.pages().find((p) => p.url() === 'about:blank') ?? (await context.newPage())
await state.page.goto('https://i.jzj9999.com/quoteh5', { waitUntil: 'domcontentloaded' })
await waitForPageLoad({ page: state.page, timeout: 5000 })

// 等待价格数据加载
await state.page.waitForSelector('.price-table-row', { timeout: 10000 })

// 提取价格数据
const prices = await state.page.evaluate(() => {
  const rows = document.querySelectorAll('.price-table-row');
  const result = [];

  rows.forEach(row => {
    const name = row.querySelector('.symbol-name')?.textContent?.trim();
    const bidPrice = row.querySelector('.el-col:nth-child(2) .symbole-price span')?.textContent?.trim();
    const askPrice = row.querySelector('.el-col:nth-child(3) .symbole-price span')?.textContent?.trim();
    const high = row.querySelector('.el-col:nth-child(4) .symbol-price-rise')?.textContent?.trim();
    const low = row.querySelector('.el-col:nth-child(4) .symbol-price-fall')?.textContent?.trim();

    if (name) {
      result.push({
        name,
        bidPrice: bidPrice || '--',
        askPrice: askPrice || '--',
        high: high || '--',
        low: low || '--',
        updateTime: new Date().toLocaleString('zh-CN')
      });
    }
  });

  return result;
});

console.log('贵金属价格:', JSON.stringify(prices, null, 2));
```

## 输出示例

```
================================================================================
贵金属实时价格
更新时间: 2026/03/05 14:30:25
================================================================================

品种: 黄金9999
  回购价: 1144.10 ↓
  销售价: 1144.95 ↓
  高/低: 1158.00 / 1140.38

品种: 黄金T+D
  回购价: 1143.96 ↓
  销售价: 1144.06 ↓
  高/低: 1159.59 / 1140.00

品种: 白银
  回购价: 20.645 ↓
  销售价: 20.745 ↓
  高/低: 21.644 / 20.437

品种: 铂金
  回购价: 491.80 ↓
  销售价: 493.30 ↓
  高/低: 508.30 / 491.50

================================================================================
说明: 以上行情仅供参考，价格仅适用于融通金公司自身贵金属业务
================================================================================
```

## 使用示例

### 基本查询

```javascript
const prices = await getGoldPrices();
prices.forEach(item => {
  console.log(`${item.name}: 回购 ${item.bidPrice}, 销售 ${item.askPrice}`);
});
```

### 筛选特定品种

```javascript
const prices = await getGoldPrices();
const goldPrices = prices.filter(p => p.name.includes('黄金'));
console.log('黄金品种价格:', goldPrices);
```

### 价格对比

```javascript
const prices = await getGoldPrices();
prices.forEach(item => {
  const spread = parseFloat(item.askPrice) - parseFloat(item.bidPrice);
  console.log(`${item.name}: 买卖价差 ${spread.toFixed(2)}`);
});
```

### 价格提醒

```javascript
async function checkPriceAlert(targetPrice) {
  const prices = await getGoldPrices();
  const gold = prices.find(p => p.name === '黄金9999');

  if (gold && parseFloat(gold.bidPrice) >= targetPrice) {
    console.log(`价格提醒: 黄金9999回购价达到 ${gold.bidPrice}`);
  }
}
```

## 错误处理

```javascript
try {
  const prices = await getGoldPrices();
  if (prices && prices.length > 0) {
    console.log('获取成功:', prices);
  } else {
    console.log('未获取到价格数据');
  }
} catch (error) {
  console.error('获取金价失败:', error.message);
  // 可以添加重试逻辑
}
```

## 注意事项

1. **数据仅供参考**: 网站明确声明"以上行情仅供参考"
2. **实时性**: 价格会实时变动，建议多次获取以确认
3. **免责声明**: 该价格仅适用于融通金公司自身贵金属实物销售及回收业务
4. **反爬虫**: 网站可能有反爬虫机制，建议：
   - 设置合理的请求间隔
   - 使用真实的User-Agent
   - 避免频繁请求
   - 考虑使用代理
5. **网络要求**: 需要能够访问外网
6. **浏览器资源**: 运行Playwright需要一定的系统资源

## 技术实现

### 技术栈

- **语言**: JavaScript / Node.js
- **浏览器自动化**: Playwright
- **浏览器**: Chromium
- **依赖包**: playwright

### 实现原理

1. 使用Playwright启动无头浏览器
2. 访问融通金行情页面
3. 等待页面JavaScript渲染完成
4. 通过CSS选择器提取价格数据
5. 解析并格式化数据输出
6. 支持导出为JSON格式

### 性能优化

- 使用无头模式减少资源占用
- 设置合理的超时时间
- 一次性提取所有数据
- 支持缓存机制

## 依赖安装

```bash
# 安装 Playwright
npm install playwright

# 安装浏览器驱动
npx playwright install chromium
```

## 扩展功能

### 定时查询

```javascript
setInterval(async () => {
  const prices = await getGoldPrices();
  console.log('更新时间:', new Date().toLocaleString());
  console.log('价格:', prices);
}, 60000); // 每分钟查询一次
```

### 数据持久化

```javascript
const { exportToJSON } = require('./index');

async function savePrices() {
  const prices = await getGoldPrices();
  exportToJSON(prices, 'prices-2026-03-05.json');
}
```

### 价格趋势分析

```javascript
function analyzeTrend(prices) {
  return prices.map(item => ({
    name: item.name,
    trend: item.bidTrend === 'up' ? '上涨' : (item.bidTrend === 'down' ? '下跌' : '持平'),
    spread: parseFloat(item.askPrice) - parseFloat(item.bidPrice)
  }));
}
```

## 相关链接

- 融通金官网: https://i.jzj9999.com
- 贵金属行情页面: https://i.jzj9999.com/quoteh5
- Playwright文档: https://playwright.dev/

---

## 👨‍💻 开发者信息

**开发者昵称**: lfq

**联系方式**:
- 📧 邮箱: [108518@qq.com](mailto:108518@qq.com)
- 💬 微信: lfq108518

**定制服务**:

如需定制开发专属 Skill，欢迎联系！

### 通用定制服务
- ✅ 数据爬取与分析类 Skill
- ✅ 自动化脚本与工具开发
- ✅ API 集成与数据处理
- ✅ Web 自动化解决方案
- ✅ 其他定制化需求

### 💎 珠宝行业 AI 定制开发服务

专注为珠宝行业提供智能化解决方案，助力企业数字化转型。

#### 🎯 服务内容

**1. 智能价格监控与分析**
- 实时金价/贵金属价格监控
- 多平台价格对比分析
- 价格趋势预测与预警
- 自动生成价格报告

**技术实现路径**:
```
数据采集层 → 数据清洗 → AI分析引擎 → 可视化展示 → 智能预警
```

**预期交付成果**:
- ✅ 实时价格监控系统
- ✅ 价格分析报告生成工具
- ✅ 智能预警推送服务

---

**2. 智能库存管理**
- 基于销售预测的智能补货
- 库存周转率优化
- 滞销商品智能识别
- 库存成本优化建议

**技术实现路径**:
```
销售数据分析 → 需求预测模型 → 库存优化算法 → 补货决策 → 自动化执行
```

**预期交付成果**:
- ✅ 智能库存管理仪表板
- ✅ 补货建议系统
- ✅ 库存优化分析报告

---

**3. AI 辅助设计**
- 珠宝款式智能推荐
- 设计趋势分析与预测
- 个性化定制方案生成
- 设计稿智能评估

**技术实现路径**:
```
图像识别 → 风格分析 → 趋势挖掘 → AI生成 → 专家评估 → 方案输出
```

**预期交付成果**:
- ✅ 款式推荐引擎
- ✅ 趋势分析报告
- ✅ 定制方案生成器

---

**4. 智能客服与销售助手**
- 7×24小时智能客服
- 产品知识库问答
- 销售话术智能生成
- 客户需求智能分析

**技术实现路径**:
```
知识库构建 → NLP理解 → 意图识别 → 对话管理 → 答案生成 → 多渠道输出
```

**预期交付成果**:
- ✅ 智能客服系统
- ✅ 销售助手工具
- ✅ 客户洞察分析平台

---

**5. 市场趋势分析**
- 珠宝市场大数据分析
- 消费者行为画像
- 竞品分析系统
- 营销策略优化建议

**技术实现路径**:
```
数据采集 → 清洗整合 → 机器学习分析 → 趋势挖掘 → 报告生成 → 决策支持
```

**预期交付成果**:
- ✅ 市场分析仪表板
- ✅ 竞品监控系统
- ✅ 营销策略优化工具

---

**6. 智能鉴定与评估**
- 珠宝图像识别与分类
- 品质智能评估
- 价格智能估算
- 鉴定报告自动生成

**技术实现路径**:
```
图像采集 → 深度学习识别 → 特征提取 → 品质评估 → 价格计算 → 报告输出
```

**预期交付成果**:
- ✅ 智能鉴定系统
- ✅ 价格评估工具
- ✅ 自动报告生成器

---

#### 📊 行业应用场景

| 应用场景 | 解决问题 | 业务价值 |
|---------|---------|---------|
| **零售门店** | 价格更新慢、库存管理混乱 | 提升效率30%+，降低成本15%+ |
| **批发商** | 价格波动风险、需求预测不准 | 降低库存风险，提升资金周转 |
| **品牌商** | 设计创新难、市场反应慢 | 加速产品迭代，提升竞争力 |
| **电商** | 客服成本高、转化率低 | 降低人工成本，提升转化率 |
| **鉴定机构** | 鉴定效率低、成本高 | 提升效率50%+，标准化输出 |

#### 🛠️ 技术栈

**AI/机器学习**:
- Python / TensorFlow / PyTorch
- OpenCV / YOLO / ResNet
- NLP / LLM / RAG

**数据处理**:
- Pandas / NumPy
- ETL Pipeline
- 时序数据库

**开发框架**:
- React / Vue / Node.js
- 微服务架构
- 云原生部署

**数据分析**:
- Power BI / Tableau
- 自研可视化引擎
- 实时数据大屏

#### 📈 服务流程

```
需求调研 → 方案设计 → 原型开发 → 测试验证 → 部署上线 → 培训支持 → 持续优化
```

**服务周期**: 2-8周（根据项目复杂度）

---

**服务承诺**:
- 🔒 代码安全可靠
- ⚡ 响应及时高效
- 🎯 需求精准对接
- 💡 技术方案专业

期待与您的合作！

---

**版本**: v1.0.0 | **更新日期**: 2026-03-05
