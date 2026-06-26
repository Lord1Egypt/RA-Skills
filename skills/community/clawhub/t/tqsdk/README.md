# TqSdk 天勤期货 Skill

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/shinnytech/tqsdk-python)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

天勤量化SDK，开源期货/期权交易，提供实时行情、回测和实盘。

## ✨ 特性

- 🆓 **开源免费** - Apache 2.0 开源，基础功能免费使用
- 📈 **期货期权专用** - 专注期货和期权市场，深度支持
- ⚡ **实时行情** - 提供实时 tick 和 K 线行情数据
- 🔄 **回测与实盘统一代码** - 同一套代码无缝切换回测和实盘
- 🔀 **异步API** - 基于异步架构，高效处理实时数据

## 📥 安装

```bash
pip install tqsdk
```

## ⚙️ 配置

需要注册天勤账号：

1. 访问 [天勤官网](https://www.shinnytech.com/) 注册账号
2. 在代码中传入账号或设置环境变量 `TQ_USERNAME` / `TQ_PASSWORD`

## 🚀 快速开始

```python
from tqsdk import TqApi, TqAuth

# 创建API实例
api = TqApi(auth=TqAuth("your_username", "your_password"))

# 获取实时行情
quote = api.get_quote("SHFE.rb2501")
print(f"最新价: {quote.last_price}, 涨跌: {quote.pre_settlement - quote.last_price}")

# 获取K线
klines = api.get_kline_serial("SHFE.rb2501", duration_seconds=60)
print(klines.tail())

# 下单
order = api.insert_order("SHFE.rb2501", direction="BUY", offset="OPEN", volume=1, limit_price=3800)

api.close()
```

## 📊 核心功能

| 类别 | 说明 | 示例接口 |
|------|------|----------|
| 行情 | 实时行情 | `api.get_quote()` |
| K线 | K线数据 | `api.get_kline_serial()` |
| 交易 | 下单/撤单 | `api.insert_order()` |
| 持仓 | 持仓查询 | `api.get_position()` |
| 账户 | 账户信息 | `api.get_account()` |
| 回测 | 回测模式 | `TqBacktest()` |

## 📖 更多示例

```python
from tqsdk import TqApi, TqAuth, TqBacktest
from datetime import date

# 回测模式
api = TqApi(
    backtest=TqBacktest(start_dt=date(2023, 1, 1), end_dt=date(2024, 1, 1)),
    auth=TqAuth("username", "password")
)

quote = api.get_quote("SHFE.rb2501")
position = api.get_position("SHFE.rb2501")
account = api.get_account()

while True:
    api.wait_update()
    if position.pos_long == 0:
        api.insert_order("SHFE.rb2501", direction="BUY", offset="OPEN", volume=1)
    print(f"账户权益: {account.balance}")
```

## 📄 许可证

Apache License 2.0

## 📊 更新日志

### v1.2.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接


### v1.1.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持期货期权实时行情与交易

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：https://github.com/shinnytech/tqsdk-python
- **ClawHub**：https://clawhub.com
