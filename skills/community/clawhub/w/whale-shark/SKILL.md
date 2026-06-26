# WhaleWatch Skill - SKILL.md

**🐋 巨鲸追踪 - 监控大户钱包动向，跟随聪明钱**

## 基本信息

```json
{
  "name": "whale-shark",
  "version": "0.1.0",
  "description": "巨鲸追踪 - 监控大户钱包动向，跟随聪明钱",
  "author": "@gztanht",
  "license": "MIT"
}
```

## 命令系统

| 命令 | 描述 | 参数 |
|------|------|------|
| `whale` | 查看巨鲸列表 | `--limit`, `--type` |
| `holdings` | 持仓分析 | `<address>` |
| `transfers` | 大额转账 | `--min` |
| `smart` | 聪明钱排行 | `--limit` |
| `alert` | 提醒管理 | `add`, `list`, `remove` |

## 功能说明

### 1. 巨鲸列表 (`whale.mjs`)

显示追踪的巨鲸钱包：
- 钱包地址
- 标签分类
- 总资产
- 24h 变化
- 交易胜率

### 2. 持仓分析 (`holdings.mjs`)

详细分析巨鲸持仓：
- 持仓分布
- 24h 操作记录
- 聪明钱指标

### 3. 大额转账 (`transfers.mjs`)

监控链上大额转账：
- 转账方向
- 金额和代币
- 发送/接收方

### 4. 聪明钱排行 (`smart.mjs`)

按胜率排序的钱包列表

### 5. 提醒管理 (`alert.mjs`)

设置转账提醒

## 巨鲸分类

| 类型 | 描述 | 权重 |
|------|------|------|
| smart_money | 高胜率交易者 | 5 |
| vc_fund | 风投基金 | 4 |
| market_maker | 做市商 | 3 |
| defi_protocol | 协议金库 | 2 |
| unknown | 未知 | 3 |

## 输出格式

### 巨鲸列表
```
🐋 WhaleWatch - 巨鲸钱包监控

排名  钱包地址          标签            总资产      24h 变化   胜率
─────────────────────────────────────────────────────────────────────────
1    0x47ac...5Df3   Unknown Whale   $125.8M    +2.3%     68%
```

### 持仓分析
```
📊 WhaleWatch - 巨鲸持仓分析

钱包：0x8f3B...2Ae1
持仓分布:
  ETH  $45.2M  51%  🟢 +12%
```

## 定价策略

- **免费版**: 5 次查询/天
- **赞助版**: 0.5 USDT/USDC → 无限查询

## 未来规划

- v0.2.0 - 实时推送通知
- v0.3.0 - 自动跟随交易
- v1.0.0 - AI 预测巨鲸操作

---

**🐋 WhaleWatch v0.1.0 - Follow The Whales**
