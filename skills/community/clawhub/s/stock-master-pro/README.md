# Stock Master Pro

A 股智能盯盘与选股系统，基于 QVeris AI 数据源。

## 功能特性

- 📊 **持仓监控**：10 分钟自动检查，实时盈亏计算
- ⚠️ **预警系统**：目标价、止损价、涨跌幅、放量预警
- 📰 **事件监控**：财报、公告、龙虎榜、新闻舆情
- 📈 **趋势选股**：右侧交易策略，智能评分推荐
- 📝 **复盘报告**：午盘/尾盘/收盘自动复盘

## 依赖要求

### 必须安装

1. **QVeris AI Skill**
   - 提供股票数据源
   - 安装指南：https://qveris.ai/?ref=y9d7PKgdPcPC-A

2. **Node.js** >= 18.0.0
   - 运行脚本环境

### 检查依赖

```bash
node scripts/check_dependency.mjs
```

## 快速开始

### 1. 创建持仓配置

```bash
cp stocks/holdings.example.json stocks/holdings.json
```

编辑 `stocks/holdings.json`，添加你的持仓：

```json
{
  "holdings": [
    {
      "code": "000531.SZ",
      "name": "穗恒运 A",
      "cost": 7.2572,
      "shares": 700,
      "alerts": {
        "target_price": 8.20,
        "stop_loss": 7.00,
        "change_pct": 5
      }
    }
  ]
}
```

### 2. 开始盯盘

```bash
node scripts/check_holdings.mjs
```

### 3. 选股

```bash
node scripts/stock_screener.mjs
```

## 脚本说明

| 脚本 | 功能 | 执行频率 |
|------|------|----------|
| `check_dependency.mjs` | 依赖检查 | 首次运行 |
| `check_holdings.mjs` | 持仓检查 | 每 10 分钟 |
| `stock_screener.mjs` | 选股器 | 按需 |
| `market_review.mjs` | 复盘报告 | 午盘/尾盘 |
| `alert_checker.mjs` | 预警检测 | 每 10 分钟 |
| `announcement_monitor.mjs` | 公告监控 | 每日 |
| `dragon_tiger.mjs` | 龙虎榜 | 每日收盘后 |
| `earnings_calendar.mjs` | 财报日历 | 每周 |

## 配置说明

### holdings.json

```json
{
  "holdings": [
    {
      "code": "股票代码（带后缀）",
      "name": "股票名称",
      "cost": 成本价，
      "shares": 股数，
      "buy_date": "买入日期",
      "notes": "备注",
      "alerts": {
        "target_price": 目标价，
        "stop_loss": 止损价，
        "change_pct": 涨跌幅阈值（百分比）
      }
    }
  ],
  "watchlist": [
    {
      "code": "股票代码",
      "name": "股票名称",
      "reason": "关注理由"
    }
  ],
  "settings": {
    "check_interval_minutes": 10,
    "review_times": ["12:30", "15:30", "16:00"],
    "exclude_st": true,
    "exclude_kcb": true
  }
}
```

## 选股策略

### 核心条件

1. **趋势向上**（25 分）
   - 均线多头排列：ma5 > ma10 > ma20 > ma60
   - 股价在 60 日线上方

2. **温和放量**（20 分）
   - 量比 1.2-2.5
   - 避免天量

3. **筹码集中**（15 分）
   - 获利比例 30%-80%
   - 筹码集中度 > 0.6

4. **MACD 金叉**（15 分）
   - DIF > DEA
   - 红柱放大

5. **基本面**（20 分）
   - 业绩增长
   - 机构持仓
   - 市值适中

### 评分标准

- ⭐⭐⭐⭐⭐ 80+ 分：强烈推荐
- ⭐⭐⭐⭐ 70-79 分：推荐
- ⭐⭐⭐ 60-69 分：关注
- < 60 分：观望

## 预警类型

| 类型 | 触发条件 | 等级 |
|------|----------|------|
| 目标价 | 现价 >= 目标价 | ℹ️ 提示 |
| 止损价 | 现价 <= 止损价 | 🚨 紧急 |
| 涨跌幅 | 绝对值 >= 阈值 | ⚠️ 警告 |
| 放量 | 量比 >= 3 | ⚠️ 警告 |

## 事件监控（仅持仓股）

- 📊 **财报发布**：提前 5 天提醒
- 📢 **公司公告**：增减持、合同、处罚
- 🐉 **龙虎榜**：机构/游资动向
- 📰 **新闻舆情**：利好/利空分析

## 故障排查

### QVeris API 调用失败

```bash
# 检查 API Key
echo $QVERIS_API_KEY

# 检查 Skill 安装
ls ~/.openclaw/skills/qveris-official/SKILL.md

# 测试 CLI
node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs --help
```

### 脚本执行失败

```bash
# 检查 Node.js 版本
node -v

# 检查依赖
node scripts/check_dependency.mjs
```

## 免责声明

⚠️ **本技能提供的分析仅供参考，不构成投资建议。**

- 股市有风险，投资需谨慎
- 历史表现不代表未来
- 请结合个人风险承受能力决策
- 本技能不保证数据完全准确

## 版本

v1.0.0 (2026-03-24)

## 许可证

MIT
