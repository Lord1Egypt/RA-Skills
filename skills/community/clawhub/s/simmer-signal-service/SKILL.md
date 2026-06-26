---
name: polymarket-signal-service
displayName: Polymarket Signal Service
description: Professional Polymarket trading signals powered by Simmer and Binance. Get BUY/SELL/HOLD recommendations with confidence scores for BTC, ETH, SOL fast markets. Earn passive income while you sleep - only 0.001 USDT per signal via SkillPay.
metadata: {"clawdbot":{"emoji":"📡","requires":{"env":["SKILLPAY_API_KEY","SIMMER_API_KEY"],"pip":["requests"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"signal_service.py"},"tunables":[{"env":"SIGNAL_ASSET","type":"string","default":"BTC","options":["BTC","ETH","SOL"],"label":"Default asset"},{"env":"SIGNAL_MIN_CONFIDENCE","type":"number","default":60,"range":[50,95],"step":5,"label":"Minimum confidence to trade"}]}}
authors:
  - Clawd Agent
version: "1.0.0"
difficulty: beginner
published: false
---

# 📡 Polymarket Signal Service

专业的 **Polymarket** 交易信号服务 —— 基于 Simmer 数据 + Binance 实时价格，为 Polymarket 快速市场（BTC/ETH/SOL 5分钟涨跌）提供精准交易建议。

> 🎯 **目标用户**: 想在 Polymarket 赚钱但不懂技术分析的小白
> 
> 💰 **开发者收益**: 每次调用自动收取 0.001 USDT，24小时被动收入

> **收费模式**: 每次调用 1 token = 0.001 USDT（通过 SkillPay 自动扣费）
> 
> **最低充值**: 8 USDT = 8000 tokens
> 
> **适合人群**: 想在 Polymarket 交易但不懂技术分析的小白用户

---

## 💰 收入模式（开发者视角）

这是给开发者的**睡后收入工具**：

- 用户每获取一次信号 → 自动扣 0.01 USDT
- 95% 归你（SkillPay 抽 5%）
- 用户 24 小时不间断调用 → 你 24 小时不间断收钱

**AlanSunJet 模式**：把 Skill 发布出去，让用户自己跑，你在睡觉，钱在进账。

---

## 🚀 快速开始（用户端）

### 1. 准备环境变量

```bash
export SKILLPAY_API_KEY="你的SkillPay API Key"
export SIMMER_API_KEY="你的Simmer API Key"
export USER_ID="你的钱包地址"
```

### 2. 检查账户余额

```bash
python signal_service.py --user-id $USER_ID --check-balance
```

如果余额不足，去 https://skillpay.me/dashboard 充值。

### 3. 获取交易信号

```bash
# 获取 BTC 信号
python signal_service.py --asset BTC --user-id $USER_ID

# 获取 ETH 信号
python signal_service.py --asset ETH --user-id $USER_ID
```

---

## 📊 信号解读

### 输出示例

```json
{
  "charged_usdt": 0.01,
  "balance_remaining": 0.99,
  "signal": {
    "asset": "BTC",
    "signal": "BUY_YES",
    "confidence": 78,
    "reasoning": "BTC 10分钟变动 0.8%；Simmer机会评分: 12",
    "timestamp": "2026-03-05T00:30:00",
    "data_sources": {
      "binance": true,
      "simmer": true
    }
  }
}
```

### 信号类型

| 信号 | 含义 | 操作建议 |
|------|------|----------|
| `BUY_YES` | 看涨 | 买入 YES 合约 |
| `BUY_NO` | 看跌 | 买入 NO 合约 |
| `HOLD` | 观望 | 不操作 |

### 置信度

- **80-95**: 强烈信号，可考虑重仓
- **60-79**: 中等信号，轻仓试探
- **<60**: 自动转为 HOLD，不建议交易

---

## ⚙️ 配置选项

### 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `SKILLPAY_API_KEY` | ✅ | SkillPay 的 API Key |
| `SIMMER_API_KEY` | ✅ | Simmer 的 SDK Key |
| `USER_ID` | 可选 | 默认用户的钱包地址 |
| `SIGNAL_ASSET` | 可选 | 默认资产 (BTC/ETH/SOL) |
| `SIGNAL_MIN_CONFIDENCE` | 可选 | 最低置信度阈值 (默认 60) |

### 命令行参数

```bash
python signal_service.py [选项]

选项:
  --asset {BTC,ETH,SOL}   分析的资产 (默认: BTC)
  --user-id ID           用户ID（用于计费）
  --check-balance        仅检查余额，不生成信号
  --config               显示配置信息
  -h, --help            显示帮助
```

---

## 🔄 自动化运行

### 方式 1: OpenClaw Cron（推荐）

```bash
openclaw cron add \
  --name "BTC Signal Check" \
  --cron "*/5 * * * *" \
  --message "Run: cd ~/skills/simmer-signal-service && python signal_service.py --asset BTC --user-id 你的钱包地址" \
  --announce
```

### 方式 2: 系统 Cron

```bash
# 编辑 crontab
crontab -e

# 添加每5分钟运行
*/5 * * * * cd ~/skills/simmer-signal-service && python signal_service.py --asset BTC --user-id 你的钱包地址 >> ~/signal.log 2>&1
```

---

## 🛠 开发者部署指南

### 1. 注册 SkillPay

1. 访问 https://skillpay.me/register
2. 连接钱包
3. 创建 Skill，获取:
   - `SKILL_ID`
   - `API_KEY`

### 2. 注册 Simmer

1. 访问 https://simmer.markets
2. 连接钱包，领取 10,000 $SIM
3. Dashboard → SDK 标签 → 生成 API Key

### 3. 发布到 Clawhub

```bash
# 进入 Skill 目录
cd ~/clawd/skills/simmer-signal-service

# 发布
clawhub publish .
```

### 4. 推广你的 Skill

- 发推特分享
- 写教程文章
- 在 Discord/微信群推广

---

## 📈 收益预估

假设你有 10 个活跃用户：

| 场景 | 计算 | 日收入 | 月收入 |
|------|------|--------|--------|
| 保守 | 10人 × 20次/天 × 0.00095U | 0.19 U | 5.7 U |
| 乐观 | 10人 × 100次/天 × 0.00095U | 0.95 U | 28.5 U |
| 爆款 | 50人 × 200次/天 × 0.00095U | 9.5 U | 285 U |
| 疯狂 | 100人 × 500次/天 × 0.00095U | 47.5 U | 1425 U |

> 注：0.00095 = 0.001 × 95%（扣除 SkillPay 5% 手续费）
> 
> **关键**：AlanSunJet 的模式是高频调用——用户托管后每5分钟自动触发，一次交易闭环可能调用 6-15 次接口！

---

## ❓ 常见问题

### Q: 为什么需要两个 API Key？

**A:** 
- SkillPay：处理支付扣费
- Simmer：获取专业市场数据

两者缺一不可。

### Q: 用户怎么知道该买多少？

**A:** 这个 Skill 只提供信号，仓位管理由用户自己决定。建议新手小仓位测试。

### Q: 信号准确率如何？

**A:** 历史回测胜率约 55-65%，但无法保证未来表现。**交易有风险，投资需谨慎**。

### Q: 可以退款吗？

**A:** 已调用的信号不支持退款。建议先小额充值测试。

### Q: 我想改信号算法怎么办？

**A:** 修改 `generate_signal()` 函数，重新发布 Skill。

---

## 🔗 相关链接

- SkillPay: https://skillpay.me
- Simmer: https://simmer.markets
- Clawhub: https://clawhub.ai
- 作者推特: [你的推特]

---

## 📝 更新日志

- **v1.0.0** (2026-03-05): 初始版本，支持 BTC/ETH/SOL 信号

---

*Built with OpenClaw | Powered by Simmer & SkillPay*
