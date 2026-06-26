# 🦎 XTrade Futu Paper Trade

> 让 AI 学会炒港股 - 实时行情 + 模拟交易

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

**一句话概括：给 AI 一个港股账户，让它能看行情、管仓位、下模拟单。**

---

## 🎯 核心能力

### 📊 实时行情（秒级响应）
- 港股主板/创业板全覆盖
- 现价、涨跌、成交量实时查询
- K线数据（日/周/月线）
- 财务报表（资产负债表、利润表）
- 财务指标（PE、PB、ROE、周转率）

### 💼 完整交易功能
- **账户管理**：资金查询、持仓查看、历史成交
- **下单**：市价买入/卖出、限价挂单
- **风控**：单票≤15%仓位提醒、纸面交易安全限制

### 🛡️ 安全设计
- 只支持**纸面交易**（Paper Trade）
- 检测到真实账户会拒绝执行
- 不涉及真实资金流动

---

## ⚡ 快速开始

```bash
# 1. 克隆或复制到 OpenClaw skills 目录
git clone https://github.com/XXXWANG/xtrade-futu-paper-trade.git
# 或复制到 ~/.openclaw/skills/xtrade-futu-paper-trade

# 2. 确保 FutuOpenD 正在运行
# 下载: https://www.futuhk.com/en/support/topic1_464

# 3. 查询行情
python xtrade_futu_skill.py quote --symbols HK.00700 HK.01810

# 4. 查看账户
python xtrade_futu_skill.py funds
python xtrade_futu_skill.py positions

# 5. 模拟买入
python xtrade_futu_skill.py buy --symbol HK.00700 --qty 100 --price 520
```

---

## 💡 常用命令速查

| 功能 | 命令 |
|------|------|
| 行情查询 | `quote --symbols HK.00700` |
| K线数据 | `kline --symbol HK.00700 --day 30` |
| 账户资金 | `funds` |
| 当前持仓 | `positions` |
| 今日盈亏 | `today-pnl` |
| 买入下单 | `buy --symbol HK.00700 --qty 100 --price 520` |
| 卖出下单 | `sell --symbol HK.00700 --qty 50 --price 530` |
| 财务指标 | `financial-indicators --code HK.00700` |
| 撤销订单 | `cancel --order_id 123456` |

---

## 🔗 黄金组合：+ XTrade Opportunity Screener

> **强烈推荐搭配 [xtrade-opportunity-screener](https://github.com/XXXWANG/xtrade-opportunity-screener) 使用！**

```
选股 → 验证 → 交易 = 完整 AI 量化工作流
```

### 为什么需要两个技能？

| 技能 | 职责 | 能力 |
|------|------|------|
| **xtrade-opportunity-screener** | 选股 | 多因子模型筛选上涨潜力股 |
| **xtrade-futu-paper-trade** | 交易 | 验证行情、执行下单 |

### 典型工作流

```
┌─────────────────────────────────────────────────────────┐
│  09:00 盘前                                            │
│  └─ xtrade-opportunity-screener → 筛选今日候选股票      │
│                                                         │
│  09:30-16:00 盘中监控                                   │
│  └─ xtrade-futu-paper-trade → 验证实时行情              │
│  └─ 发现满足条件的股票 → 买入                           │
│                                                         │
│  21:00 盘后复盘                                         │
│  └─ 分析当日交易 → 调整次日策略                         │
└─────────────────────────────────────────────────────────┘
```

### 30 天生存挑战示例

用这两个技能，你可以搭建一个**全自动 AI 交易系统**：

1. 每天 09:00 筛选候选股票
2. 每 30 分钟监控行情，发现机会则行动
3. 30 天后结算，目标 **+2% 收益**

---

## 📦 相关项目

| 项目 | 说明 |
|------|------|
| [xtrade-opportunity-screener](https://github.com/XXXWANG/xtrade-opportunity-screener) | 🧠 智能选股引擎 |
| [xtrade](https://github.com/XXXWANG/xtrade) | 🦎 技能箱主页 |

---

## 🤝 欢迎贡献

- 提交 Issue 报告问题
- 提交 PR 改进功能
- ⭐ Star 支持一下

---

**🦎 让 AI 成为你的港股交易助手**
