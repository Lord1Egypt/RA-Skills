# TokenSniper 🎯

**代币狙击手 - 新代币上线监控，第一时间发现机会**

## 技能信息

- **名称**: TokenSniper
- **版本**: 0.1.0
- **作者**: @gztanht
- **许可**: MIT
- **GitHub**: https://github.com/gztanht/token-shark
- **ClawHub**: https://clawhub.com/skills/token-shark

## 产品亮点

- 🎯 **新代币监控** - DEX 新上线代币实时追踪
- 🔍 **风险评估** - 多维度风险评分系统
- 💰 **流动性追踪** - 流动性池变化监控
- 🚨 **快速提醒** - 第一时间发现机会
- 📊 **市场分析** - 交易量/持有者/价格趋势

## 快速开始

```bash
# 查看新代币列表
node scripts/monitor.mjs

# 查看代币详情
node scripts/analyze.mjs 0x1234...5678

# 查看风险评分
node scripts/risk.mjs 0x1234...5678

# 设置价格提醒
node scripts/alert.mjs add --token 0x1234 --price 0.01
```

## 使用示例

### 新代币监控

```bash
$ node scripts/monitor.mjs

🎯 TokenSniper - 新代币监控

时间        代币名称        链        价格        流动性    风险    24h 交易
────────────────────────────────────────────────────────────────────────────────
10 分钟前   PEPE2.0       Ethereum  $0.00012   $50K     🟡 中    $12K
15 分钟前   SafeMoon V3   BSC       $0.000001  $25K     🔴 高    $5K
20 分钟前   CatCoin       Base      $0.0023    $100K    🟢 低    $45K
30 分钟前   AI_Token      Arbitrum  $0.15      $200K    🟢 低    $89K

💡 提示：node scripts/monitor.mjs --chain ethereum
```

### 代币分析

```bash
$ node scripts/analyze.mjs 0x1234...5678

📊 TokenSniper - 代币分析

代币：PepeAI (PEPEAI)
合约：0x1234...5678
链：Ethereum

价格信息:
- 当前价格：$0.00012
- 24h 涨跌：+245%
- 市值：$1.2M
- 流动性：$50K

持有者分析:
- 总持有者：1,234
- Top10 持仓：35%
- 合约持仓：5%

风险评估:
- 整体评分：🟡 中等风险 (65/100)
- 合约审计：❌ 未审计
- 流动性锁定：✅ 已锁定 (90 天)
- 持有者分布：✅ 健康

💡 建议：小额参与，设置止损
```

### 风险评分

```bash
$ node scripts/risk.mjs 0x1234...5678

🔍 TokenSniper - 风险评估

代币：PepeAI (PEPEAI)

风险维度              评分      状态
─────────────────────────────────────────────────────
合约安全              70/100    🟡 中等
流动性风险            60/100    🟡 中等
持有者集中度          80/100    🟢 健康
开发团队              40/100    🔴 匿名
社区活跃度            75/100    🟢 活跃
整体评分              65/100    🟡 中等风险

⚠️ 风险提示:
- 开发团队匿名
- 合约未经审计
- 流动性锁定期较短

💡 建议：投资不超过总仓位 2%
```

### 价格提醒

```bash
$ node scripts/alert.mjs add --token 0x1234 --price 0.01

✅ 提醒已设置

代币：0x1234...5678
目标价格：$0.01
当前价格：$0.00012
提醒条件：价格上涨至 $0.01

💡 查看提醒：node scripts/alert.mjs --list
```

## 命令参考

| 命令 | 功能 |
|------|------|
| `monitor.mjs` | 查看新代币列表 |
| `monitor.mjs --chain ethereum` | 按链筛选 |
| `analyze.mjs <address>` | 代币详情分析 |
| `risk.mjs <address>` | 风险评估 |
| `alert.mjs add --token <addr> --price <price>` | 设置提醒 |
| `alert.mjs --list` | 查看所有提醒 |
| `alert.mjs remove <id>` | 删除提醒 |

## 风险评分标准

| 分数 | 等级 | 建议 |
|------|------|------|
| 80-100 | 🟢 低风险 | 可正常参与 |
| 60-79 | 🟡 中等风险 | 小额参与 |
| 40-59 | 🟠 较高风险 | 谨慎参与 |
| 0-39 | 🔴 高风险 | 建议观望 |

## 监控的DEX

| 交易所 | 链 | 状态 |
|--------|-----|------|
| Uniswap V2 | Ethereum | ✅ |
| Uniswap V3 | Ethereum | ✅ |
| PancakeSwap | BSC | ✅ |
| SushiSwap | 多链 | ✅ |
| Camelot | Arbitrum | ✅ |
| Aerodrome | Base | ✅ |

## 定价

**免费使用**: 5 次查询/天

**赞助解锁**: 0.5 USDT/USDC → 无限查询

**赞助地址**:
- USDT (ERC20): `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`
- USDC (ERC20): `0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`

## 安全提示

⚠️ **重要提醒**:
- 新代币风险极高，可能归零
- 永远不要投资超过能承受损失的金额
- 警惕"rug pull"骗局
- 检查合约是否放弃所有权
- 检查流动性是否锁定
- 小额测试后再考虑大额

## 支持渠道

- **GitHub Issues**: https://github.com/gztanht/token-shark/issues
- **Telegram**: @gztanht
- **ClawHub**: https://clawhub.com/skills/token-shark

---

**🎯 TokenSniper v0.1.0 - Snipe Before Moon**
