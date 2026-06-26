# WhaleWatch 🐋

**巨鲸追踪 - 监控大户钱包动向，跟随聪明钱**

## 技能信息

- **名称**: WhaleWatch
- **版本**: 0.1.0
- **作者**: @gztanht
- **许可**: MIT
- **GitHub**: https://github.com/gztanht/whale-shark
- **ClawHub**: https://clawhub.com/skills/whale-shark

## 产品亮点

- 🐋 **巨鲸钱包监控** - 追踪大户持仓变化
- 💰 **大额转账提醒** - 实时监控链上大额转账
- 📊 **持仓变化分析** - 智能分析巨鲸操作
- 🎯 **聪明钱跟随** - 发现高胜率钱包
- 🔔 **实时通知** - 重要动向第一时间知道

## 快速开始

```bash
# 查看巨鲸列表
node scripts/whale.mjs

# 查看特定巨鲸持仓
node scripts/holdings.mjs 0x1234...5678

# 查看大额转账
node scripts/transfers.mjs --min 100000

# 设置转账提醒
node scripts/alert.mjs add --whale 0x1234 --min 50000
```

## 使用示例

### 巨鲸列表

```bash
$ node scripts/whale.mjs

🐋 WhaleWatch - 巨鲸钱包监控

排名  钱包地址          标签            总资产      24h 变化   胜率
─────────────────────────────────────────────────────────────────────────
1    0x47ac...5Df3   Unknown Whale   $125.8M    +2.3%     68%
2    0x8f3B...2Ae1   Smart Money     $89.2M     +5.1%     75%
3    0x2C91...9Bb4   VC Fund         $67.5M     -1.2%     62%
4    0x5E2a...7Cd8   Market Maker    $54.3M     +0.8%     55%
5    0x9D1f...4Ef2   DeFi Protocol   $43.7M     +12.4%    71%

💡 提示：node scripts/whale.mjs --limit 10
```

### 持仓分析

```bash
$ node scripts/holdings.mjs 0x8f3B...2Ae1

📊 WhaleWatch - 巨鲸持仓分析

钱包：0x8f3B...2Ae1
标签：Smart Money
胜率：75% (过去 30 天)

持仓分布:
  ETH       $45.2M    51%     🟢 +12%
  USDC      $18.5M    21%     🔴 -3%
  WBTC      $12.8M    14%     🟢 +5%
  UNI       $6.2M     7%      🟢 +28%
  LINK      $4.1M     5%      🟡 0%

24h 操作:
  ✅ 买入 $2.3M UNI @ $5.82
  ✅ 买入 $1.1M ETH @ $2,050
  ❌ 卖出 $800K USDC

💡 聪明钱指标：持续加仓 DeFi 蓝筹
```

### 大额转账

```bash
$ node scripts/transfers.mjs --min 100000

💸 WhaleWatch - 大额转账监控

时间      方向   金额        代币   从                    至
───────────────────────────────────────────────────────────────────────────────
2 分钟前   OUT    $2.5M      ETH    0x8f3B...2Ae1      0x742d...9Aa3
5 分钟前   IN     $1.8M      USDC   0x1C4e...8Bb2   →  0x47ac...5Df3
10 分钟前  OUT    $950K      WBTC   0x2C91...9Bb4   →  Binance
15 分钟前  IN     $3.2M      ETH    Coinbase        →  0x9D1f...4Ef2

💡 提示：node scripts/transfers.mjs --min 500000
```

### 设置提醒

```bash
$ node scripts/alert.mjs add --whale 0x8f3B --min 50000

✅ 提醒已设置

巨鲸：0x8f3B...2Ae1 (Smart Money)
监控条件：转账金额 > $50,000
通知方式：Telegram

💡 查看提醒：node scripts/alert.mjs --list
```

## 命令参考

| 命令 | 功能 |
|------|------|
| `whale.mjs` | 查看巨鲸列表 |
| `whale.mjs --limit 10` | 限制显示数量 |
| `holdings.mjs <address>` | 查看持仓分析 |
| `transfers.mjs` | 查看大额转账 |
| `transfers.mjs --min 100000` | 最小金额筛选 |
| `alert.mjs add --whale <addr> --min 50000` | 设置提醒 |
| `smart.mjs` | 聪明钱排行 |

## 巨鲸分类

| 类型 | 描述 | 跟随价值 |
|------|------|---------|
| 🧠 Smart Money | 高胜率交易者 | ⭐⭐⭐⭐⭐ |
| 💼 VC Fund | 风投基金 | ⭐⭐⭐⭐ |
| 🏦 Market Maker | 做市商 | ⭐⭐⭐ |
| 🔧 DeFi Protocol | 协议金库 | ⭐⭐ |
| ❓ Unknown | 未知巨鲸 | ⭐⭐⭐ |

## 聪明钱评分

| 胜率 | 等级 | 跟随建议 |
|------|------|---------|
| 70%+ | 🧠 聪明钱 | 重点关注 |
| 60-69% | 📈 优秀 | 参考操作 |
| 50-59% | 📊 普通 | 谨慎参考 |
| <50% | 📉 反面教材 | 反向指标 |

## 定价

**免费使用**: 5 次查询/天

**赞助解锁**: 0.5 USDT/USDC → 无限查询

**赞助地址**:
- USDT (ERC20): `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`
- USDC (ERC20): `0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`

## 数据源

- Etherscan API
- Arkham Intelligence
- Nansen (付费)
- 链上数据分析

## 安全提示

⚠️ **重要提醒**:
- 巨鲸也可能亏损，不要盲目跟随
- 注意区分转移和真实交易
- 小额测试后再跟随
- 做好自己的研究 (DYOR)

## 支持渠道

- **GitHub Issues**: https://github.com/gztanht/whale-shark/issues
- **Telegram**: @gztanht
- **ClawHub**: https://clawhub.com/skills/whale-shark

---

**🐋 WhaleWatch v0.1.0 - Follow The Whales**
