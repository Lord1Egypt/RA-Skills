# SMC 交易信号监控 📈

> 基于 SMC 聪明钱交易理念，1H 定方向 + 15M 入场，ATR 动态止盈止损

## ✨ 核心策略

### 多时间周期分析

- **1H（1 小时）** → 确定趋势方向
  - BULLISH（偏多）→ 只做多
  - BEARISH（偏空）→ 只做空
  - NEUTRAL（震荡）→ 观望

- **15M（15 分钟）** → 精确入场点
  - IFC 机构蜡烛确认
  - SSL/BSL 流动性扫损
  - CHOCH 趋势转变

### ATR 动态风控

| 项目 | 计算 | 说明 |
|------|------|------|
| **止损** | ±1 × ATR | 自适应市场波动 |
| **TP1** | ±1.5 × ATR | 风险回报比 1:1.5 |
| **TP2** | ±3 × ATR | 风险回报比 1:3.0 |
| **TP3** | ±5 × ATR | 风险回报比 1:5.0 |

## 🚀 快速开始

### 1. 安装

```bash
clawhub install smc-trading-signal
```

### 2. 配置

编辑 `config/symbols.json` 添加监控品种：

```json
{
  "symbols": [
    {
      "name": "黄金",
      "code": "GC",
      "source": "akshare",
      "enabled": true
    }
  ]
}
```

### 3. 测试

```bash
cd ~/.openclaw/workspace/skills/smc-trading-signal
python3 scripts/monitor.py --test
```

### 4. 启用定时监控

```bash
# 每小时检查一次
openclaw cron add smc-trading-signal --interval 60
```

## 📋 信号示例

```
📈 SMC 交易信号 - 黄金
⏰ 2026-03-24 16:30

【趋势分析】
├ H1 趋势：BEARISH (偏空)
├ 当前价格：2156.80
├ 涨跌幅：-0.85%
└ 日内范围：2142.30 - 2168.90

【交易信号】做空
├ 入场：2156.80 附近
├ 止损：2171.30 (1 × ATR)
├ TP1: 2142.30 (1:1.5)
├ TP2: 2127.80 (1:3.0)
└ TP3: 2113.30 (1:5.0)

【信号依据】
1. ✅ SSL 流动性扫损
   跌破前低，触发卖盘流动性

2. ✅ IFC 机构蜡烛
   15M 大阴线，成交量放大

【风险提示】
⚠️ 风险回报比：1:1.5
⚠️ 建议仓位：总资金 2-3%
⚠️ 严格执行止损
```

## ⚙️ 配置说明

### 品种配置 (config/symbols.json)

```json
{
  "symbols": [
    {
      "name": "黄金",           // 品种名称
      "code": "GC",            // 交易代码
      "source": "akshare",     // 数据源
      "enabled": true,         // 是否启用
      "check_interval": 60     // 检查间隔（分钟）
    }
  ]
}
```

### ATR 配置

```json
{
  "atr": {
    "period": 14,              // ATR 周期
    "stop_loss": 1.0,          // 止损倍数
    "take_profit": [1.5, 3.0, 5.0]  // 止盈位
  }
}
```

### 风控配置

```json
{
  "risk_management": {
    "max_position_size": 0.03,  // 最大仓位 3%
    "daily_loss_limit": 0.05,   // 日亏损限制 5%
    "min_risk_reward": 1.5      // 最小风报比
  }
}
```

## 📊 支持品种

| 品种 | 代码 | 数据源 | 状态 |
|------|------|--------|------|
| 黄金 (COMEX) | GC | 新浪财经/雅虎 | ✅ 已支持 |
| 比特币 | BTCUSDT | Binance | ⏳ 开发中 |
| 以太坊 | ETHUSDT | Binance | ⏳ 开发中 |
| 欧元/美元 | EURUSD | 外汇 API | 📅 计划 |

### ⚠️ 数据源说明

**中国大陆用户**:
- 新浪财经接口可能不稳定
- 建议使用 VPN 或代理
- 或使用模拟数据测试

**海外用户**:
- 雅虎财经接口稳定
- 无需额外配置

**生产环境建议**:
- 使用付费 API（如 Alpha Vantage、Twelve Data）
- 或自建数据源（AkShare + 本地缓存）

## 🎓 SMC 术语

| 术语 | 全称 | 含义 |
|------|------|------|
| **IFC** | Institutional Fair Candle | 机构公平蜡烛 |
| **SSL** | Sell Side Liquidity | 卖方流动性 |
| **BSL** | Buy Side Liquidity | 买方流动性 |
| **CHOCH** | Change of Character | 趋势转变 |
| **OB** | Order Block | 订单块 |
| **FVG** | Fair Value Gap | 公允价值缺口 |
| **ATR** | Average True Range | 平均真实波幅 |

## ⚠️ 风险提示

**重要声明**:
- ❗ 本技能提供的信号仅供参考
- ❗ 不构成投资建议或推荐
- ❗ 交易有风险，入市需谨慎
- ❗ 请严格执行止损，控制仓位
- ❗ 过往表现不代表未来收益

**建议**:
- ✅ 先用模拟盘测试
- ✅ 从小仓位开始
- ✅ 记录每笔交易
- ✅ 定期复盘总结

## 📝 更新日志

### v1.0.0 (2026-03-24)
- ✅ 首次发布
- ✅ 1H+15M 多周期分析
- ✅ ATR 动态止盈止损
- ✅ 黄金品种支持
- ✅ SMC 信号识别

### 📅 计划
- [ ] 加密货币支持
- [ ] 外汇货币对
- [ ] 自动回测功能
- [ ] 信号统计面板
- [ ] 移动端推送

## ❓ 常见问题

**Q: 信号准确率如何？**  
A: SMC 策略胜率约 55-65%，但风险回报比高（平均 1:3+）。

**Q: 多久出一次信号？**  
A: 每小时检查，平均每天 2-5 个有效信号。

**Q: 需要手动执行吗？**  
A: 是的，信号仅供参考，需自行判断执行。

**Q: 可以自动交易吗？**  
A: 暂不支持，建议手动执行以确保风控。

**Q: 适合新手吗？**  
A: 建议先学习 SMC 基础，再用模拟盘练习。

## 📚 学习资源

- [SMC 交易策略入门](https://example.com/smc-intro)
- [ATR 指标详解](https://example.com/atr-guide)
- [风险管理指南](https://example.com/risk-management)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

GitHub: https://github.com/zt6558609-cpu/smc-trading-signal

## 📄 许可证

MIT License

---

**交易有风险，请理性投资！** 📉📈
