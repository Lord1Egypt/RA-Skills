---
name: solana-analytics-pro
description: 专业级 Solana 综合分析工具。提供技术面分析、链上数据洞察、市场情绪监控、投资组合管理和交易信号生成。当用户需要深度分析 Solana 项目、生成交易信号、管理加密投资组合、进行风险评估或获取专业级市场报告时触发此 Skill。
---

# Solana Analytics Pro - 专业级综合分析工具

全方位 Solana 生态分析平台，整合技术分析、链上数据、情绪监控和智能策略。

## 核心模块

### 1. 技术分析 (TA)
- 价格行为分析
- 技术指标计算 (RSI, MACD, MA, Bollinger Bands)
- 支撑阻力位识别
- 趋势判断与预测

### 2. 链上分析 (On-Chain)
- 巨鲸钱包追踪
- 资金流向监控
- 持有者行为分析
- 智能合约审计检查

### 3. 情绪分析 (Sentiment)
- 社交媒体情绪监控
- KOL 言论追踪
- 社区热度指数
- 恐惧贪婪指数

### 4. 投资组合管理 (Portfolio)
- 多币种持仓追踪
- 收益/风险分析
- 再平衡建议
- 税务报告生成

### 5. 交易信号 (Signals)
- 买入/卖出信号生成
- 止损止盈建议
- 仓位管理策略
- 回测验证

## 快速开始

### 基础分析
- "分析 SOL 的技术面"
- "生成 BONK 的交易信号"
- "评估我的 Solana 投资组合"

### 深度研究
- "对 WIF 进行全面的基本面+技术面分析"
- "分析 Pump.fun 发射的某个新币"
- "生成 Solana 生态周报"

### 实时监控
- "设置巨鲸警报"
- "监控某个钱包的动态"
- "追踪市场情绪变化"

## 分析框架

### 五维分析模型 (PENTA)
1. **P**rice Action - 价格行为
2. **E**cosystem - 生态健康度
3. **N**etwork - 链上数据
4. **T**iming - 时机选择
5. **A**ttitude - 市场情绪

### 交易评分系统 (0-100)
| 分数 | 评级 | 建议 |
|------|------|------|
| 80-100 | A+ | 强烈推荐 |
| 60-79 | B | 可以考虑 |
| 40-59 | C | 观望 |
| 20-39 | D | 不推荐 |
| 0-19 | F | 避免 |

## 参考资源

### 技术分析参考
查看 [references/technical-analysis.md](references/technical-analysis.md):
- 常用技术指标详解
- 图表模式识别
- 支撑阻力计算方法
- 趋势判断规则

### 链上数据参考
查看 [references/on-chain-metrics.md](references/on-chain-metrics.md):
- 巨鲸钱包数据库
- 资金流动模式
- 持有者分布分析
- 合约安全检查清单

### 情绪分析参考
查看 [references/sentiment-guide.md](references/sentiment-guide.md):
- 情绪指标计算方法
- KOL 影响力评估
- 社交媒体监控工具
- 恐慌贪婪指数解读

### 投资组合参考
查看 [references/portfolio-management.md](references/portfolio-management.md):
- 资产配置策略
- 风险管理框架
- 再平衡规则
- 税务优化建议

## 分析脚本

### 全能分析仪
`scripts/comprehensive_analyzer.py` - 五维综合分析:
```bash
python3 scripts/comprehensive_analyzer.py --token BONK --depth full
```

### 交易信号生成器
`scripts/signal_generator.py` - 生成买卖信号:
```bash
python3 scripts/signal_generator.py --token WIF --timeframe 4h
```

### 投资组合分析器
`scripts/portfolio_analyzer.py` - 分析持仓组合:
```bash
python3 scripts/portfolio_analyzer.py --input portfolio.json
```

### 巨鲸监控器
`scripts/whale_tracker.py` - 追踪巨鲸动态:
```bash
python3 scripts/whale_tracker.py --wallet WALLET_ADDRESS --alert
```

### 报告生成器
`scripts/report_generator.py` - 生成专业报告:
```bash
python3 scripts/report_generator.py --type weekly --format markdown
```

## 使用场景详解

### 场景1: 交易决策支持
**用户需求**: 想买入某个 Solana 代币，需要全面分析

**Skill 执行**:
1. 技术分析 - 识别趋势和关键价位
2. 链上分析 - 检查资金流入流出
3. 情绪分析 - 评估市场热度
4. 生成交易信号 - 买入/观望/避免建议
5. 提供入场点、止损点、目标价位

### 场景2: 投资组合优化
**用户需求**: 管理多个 Solana 代币持仓

**Skill 执行**:
1. 导入持仓数据
2. 分析每个持仓的风险收益比
3. 计算组合相关性
4. 识别过度集中风险
5. 生成再平衡建议

### 场景3: 新币评估
**用户需求**: 评估 Pump.fun 上新发射的代币

**Skill 执行**:
1. 合约安全检查
2. 代币经济学分析
3. 早期持有者分布
4. 社交媒体热度
5. 风险评估报告

### 场景4: 市场监控
**用户需求**: 持续监控 Solana 生态动态

**Skill 执行**:
1. 设置巨鲸钱包警报
2. 监控关键指标变化
3. 追踪重要事件
4. 生成日报/周报

## 数据整合

### 市场数据
- CoinGecko / CoinMarketCap - 价格和市值
- TradingView - 图表数据
- Birdeye / DexScreener - DEX 实时数据

### 链上数据
- Helius - RPC 和索引
- Solscan / SolanaFM - 区块浏览器
- DefiLlama - TVL 数据
- Dune Analytics - 自定义查询

### 情绪数据
- Twitter/X API - 社交热度
- LunarCrush - 社交指标
- Santiment - 链上情绪

## 风险管理体系

### 三层风险控制
1. **仓位控制** - 单笔交易不超过总资金 5%
2. **止损管理** - 硬止损 7%，移动止损 10%
3. **相关性控制** - 同类资产不超过 30%

### 风险评级
```
🔴 极高风险 - 新币、无流动性、合约未验证
🟠 高风险 - 高波动、集中持仓、监管不确定
🟡 中等风险 - 成熟项目但波动较大
🟢 低风险 - 蓝筹代币、深度流动性
🔵 极低风险 - 稳定币、主流资产
```

## 报告模板

### 每日简报
- 市场概况 (3-5 句话)
- 关键数据 (TVL、交易量、活跃地址)
- 重要事件
- 明日关注

### 深度研究报告
- 执行摘要
- 技术分析
- 链上分析
- 情绪分析
- 风险评估
- 投资建议
- 附录 (数据来源、方法论)

## 与其他 Skill 的协作

- `solana-intelligence` - 基础生态数据
- `dex-price-monitor` - DEX 价格监控
- `whale-alert-monitor` - 鲸鱼警报
- `social-sentiment-monitor` - 深度情绪分析
- `crypto-trend-analyzer` - 宏观趋势分析

## 更新日志

- v1.0.0 - 初始版本
  - 五维分析模型 (PENTA)
  - 技术分析模块
  - 链上分析模块
  - 情绪分析模块
  - 投资组合管理
  - 交易信号生成
  - 自动化报告

## 免责声明

⚠️ **风险提示**:
- 本 Skill 提供的分析和建议仅供参考，不构成投资建议
- 加密货币市场具有极高风险，可能导致本金全部损失
- 过往表现不代表未来收益
- 请根据自身风险承受能力做出投资决策
- 建议咨询专业金融顾问
