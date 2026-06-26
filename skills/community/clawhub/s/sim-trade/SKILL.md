---
name: sim-trade
description: "A 股模拟交易盘 - 支持真实行情、多平台模拟盘连接、持仓管理、盈亏计算"
---

# Sim Trade - 模拟股票交易盘 🎮📈

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| ✅ **真实行情** | 东方财富实时行情 API |
| ✅ **多平台模拟盘** | 同花顺/东方财富/蚂蚁财富（需登录） |
| ✅ **本地模拟** | 虚拟资金练习（无需外部账户） |
| ✅ **持仓管理** | 成本、数量、浮动盈亏 |
| ✅ **交易记录** | 完整成交日志 |

---

## 🚀 快速开始

### 1️⃣ 初始化（本地模拟模式）

```bash
cd ~/.openclaw/workspace/skills/sim-trade/scripts
python3 init_account.py
```

### 2️⃣ 行情查询

```bash
# 查询单只股票
python3 quote.py 600900

# 批量查询持仓股票行情
python3 quote.py
```

---

## 🌐 连接真实模拟盘

### 方式一：东方财富模拟盘（需要 Cookie）

1. 在浏览器登录东方财富模拟交易
2. 获取 Cookie（开发者工具 → Network → 复制请求头中的 Cookie）
3. 配置文件：`~/.openclaw/sim_trade/config.json`

```json
{
  "mode": "eastmoney",
  "cookie": "your_cookie_here"
}
```

### 方式二：同花顺模拟盘（需要 Cookie）

同上，获取同花顺账号的 Cookie

### 方式三：券商 API（如华泰、银河）

```json
{
  "mode": "broker",
  "broker": "htf",
  "token": "your_api_token"
}
```

---

## 📁 文件结构

```
sim-trade/
├── SKILL.md
├── README.md
└── scripts/
    ├── config.py
    ├── account.py
    ├── positions.py
    ├── quote.py          # 行情查询
    ├── trade.py          # 交易执行
    ├── sync.py           # 同步真实账户
    ├── show_account.py
    ├── show_positions.py
    ├── list_trades.py
    └── init_account.py
```

---

## ⚙️ 配置说明

### config.py

```python
# 交易模式
# - "local": 本地模拟（默认）
# - "eastmoney": 东方财富模拟盘
# - "tonghuashun": 同花顺模拟盘
# - "broker": 券商 API
TRADE_MODE = "local"

# 东方财富 Cookie（获取模拟盘数据用）
EASTMONEY_COOKIE = ""

# 券商配置
BROKER = "htf"  # 华泰
BROKER_TOKEN = ""
```

---

## 💡 使用示例

### 本地模拟交易

```bash
# 初始化
python3 init_account.py

# 买入（市价）
python3 trade.py buy 600900 100

# 买入（限价）
python3 trade.py buy 600900 100 --price 27.00

# 卖出
python3 trade.py sell 600900 50

# 查看账户
python3 show_account.py
```

### 查询实时行情

```bash
python3 quote.py 600900
python3 quote.py 600900 600025 600919
```

---

## ⚠️ 风险提示

- 本系统仅供学习参考，不构成投资建议
- 模拟盘交易不代表真实交易结果
- 真实账户连接需要妥善保管账号信息

---

<div align="center">
<strong>Sim Trade ✨</strong><br>
连接真实行情，练习实盘操作 📈🎮
</div>
