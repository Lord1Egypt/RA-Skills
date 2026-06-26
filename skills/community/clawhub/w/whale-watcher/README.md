# 🐋 Whale Watcher - 巨鲸钱包监控

**Version:** 1.0.0  
**Author:** 宝宝 (BaoBao)  
**License:** MIT

---

## 🎯 功能介绍

实时监控加密货币巨鲸钱包，追踪大额交易动向。

### 核心功能

- 🔍 **钱包监控** - 追踪特定巨鲸地址
- 💰 **阈值告警** - 设置最低交易金额提醒
- ⛓️ **多链支持** - Ethereum, BSC 等
- 📊 **交易分析** - 自动识别大额转账
- 📱 **实时推送** - Telegram 告警通知

---

## 💡 使用场景

1. **跟巨鲸操作** - 发现大佬建仓/出货
2. **项目监控** - 监控项目方钱包动向
3. **风险预警** - 大额转账可能是砸盘信号
4. **投资机会** - 早期发现聪明钱动向

---

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub
clawhub install whale-watcher

# 或手动安装
git clone https://github.com/your-repo/whale-watcher.git
cp -r whale-watcher ~/.openclaw/skills/
```

### 配置

```bash
# 环境变量（可选）
export ETHERSCAN_API_KEY="your_etherscan_key"
export BSCSCAN_API_KEY="your_bscscan_key"
export TELEGRAM_BOT_TOKEN="your_telegram_bot"
```

### 使用示例

```bash
# 监控 V 神钱包
/whale-watcher monitor 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045

# 设置阈值 100 万美元
/whale-watcher alert --min 1000000

# 查看最近交易
/whale-watcher txs 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --chain ETH
```

---

## 📊 输出示例

```
🐋 监控钱包：0xd8dA6BF2... (ETH)
💰 阈值：$50,000
============================================================

✅ 发现 3 笔大额交易:

1. 2026-03-06 12:30:45
   💰 500.00 ETH ($1,750,000.00)
   📤 0x742d35Cc6... → 0xd8dA6BF26...
   🔗 https://etherscan.io/tx/0xabc123...

2. 2026-03-06 10:15:22
   💰 200.00 ETH ($700,000.00)
   📤 0xd8dA6BF26... → 0x28C6c0629...
   🔗 https://etherscan.io/tx/0xdef456...
```

---

## 💰 付费版本 (Pro)

**免费版：**
- 监控 1 个钱包
- 阈值最低 $50,000
- 手动查询

**Pro 版 ($9.99/月)：**
- 监控 10 个钱包
- 阈值最低 $10,000
- 实时 Telegram 推送
- 历史数据分析
- 多链支持 (ETH, BSC, ARB, OP)

---

## 🔧 技术细节

- **数据源：** Etherscan API, BscScan API
- **更新频率：** 每 5 分钟
- **延迟：** < 30 秒
- **准确率：** 99%+

---

## 📞 支持

- **Telegram:** @baobao_support
- **Email:** support@baobao.ai
- **GitHub:** Issues

---

## ⚠️ 免责声明

本工具仅供参考，不构成投资建议。加密货币投资风险极高，请自行研究 (DYOR)。

---

**Made with ❤️ by 宝宝 (BaoBao)**
