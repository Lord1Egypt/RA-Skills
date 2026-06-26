# Ptrade 恒生量化 Skill

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://ptradeapi.com)
[![License](https://img.shields.io/badge/license-Proprietary-orange.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

Ptrade恒生量化交易平台，策略运行在券商服务器，低延迟执行。

## ✨ 特性

- 🏢 **券商服务器运行** - 策略部署在券商机房，极低延迟
- ⚡ **低延迟执行** - 毫秒级下单响应，适合高频策略
- 📊 **Level2行情** - 支持逐笔成交、十档行情等深度数据
- 🔄 **事件驱动** - initialize() + handle_data() 经典事件驱动架构
- 💰 **融资融券/期货** - 支持两融交易和期货品种

## 📥 安装

无需 pip 安装，Ptrade 运行在券商服务器环境中，内置 Python 运行时。

> 需要联系券商开通 Ptrade 权限后，通过客户端上传策略。

## 🚀 快速开始

```python
def initialize(context):
    """初始化函数，策略启动时执行一次"""
    context.stock = '600519.SS'
    set_universe([context.stock])
    log.info("策略初始化完成")

def handle_data(context, data):
    """行情事件处理，每个交易bar执行"""
    price = data[context.stock]['close']
    position = get_position()
    
    if context.stock not in position:
        order(context.stock, 100)
        log.info(f"买入 {context.stock} 100股")
```

## 📊 核心功能

| 类别 | 说明 | 示例接口 |
|------|------|----------|
| 股票池 | 设置/获取股票池 | `set_universe()` |
| 行情 | 历史/实时行情 | `get_history()` / `get_snapshot()` |
| 交易 | 下单/撤单 | `order()` / `order_target()` |
| 持仓 | 查询持仓信息 | `get_position()` |
| 账户 | 账户资金信息 | `context.portfolio` |
| 定时 | 定时任务调度 | `run_daily()` / `run_interval()` |

## 📖 更多示例

```python
def initialize(context):
    set_universe(['600519.SS', '000858.SZ'])
    run_daily(context, market_open, time='09:31')

def market_open(context):
    """每日开盘后执行"""
    snapshot = get_snapshot('600519.SS')
    log.info(f"最新价: {snapshot['last_px']}")
    
    positions = get_position()
    portfolio = context.portfolio
    log.info(f"总资产: {portfolio.total_value}")
```

## 📄 许可证

Proprietary - 券商授权使用

## 📊 更新日志

### v1.3.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接


### v1.2.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持券商服务器策略开发与交易

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：https://ptradeapi.com
- **ClawHub**：https://clawhub.com
