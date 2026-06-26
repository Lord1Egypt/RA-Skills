# QMT 迅投量化 Skill

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](http://dict.thinktrader.net/freshman/rookie.html)
[![License](https://img.shields.io/badge/license-Proprietary-orange.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

QMT迅投量化交易终端，内置Python策略开发、回测引擎和实盘交易。

## ✨ 特性

- 🖥️ **完整桌面客户端** - 集成行情、策略编辑、回测、实盘于一体
- 📈 **内置回测引擎** - 支持历史数据回测与绩效分析
- 🌐 **全品种支持** - 股票、基金、债券、期货、期权
- 📊 **Level2数据** - 支持逐笔成交、十档行情等深度数据

## 📥 安装

QMT 客户端模式需要从券商获取安装包。miniQMT 模式可通过 pip 安装：

```bash
pip install xtquant
```

> ⚠️ 需券商开通 QMT 权限，仅支持 Windows 系统。

## 🚀 快速开始

```python
# QMT 客户端策略模式
def init(ContextInfo):
    """策略初始化"""
    ContextInfo.set_universe(['600519.SH', '000858.SZ'])
    ContextInfo.run_time('market_open', '9:31:00', 'SH')

def handlebar(ContextInfo):
    """每个bar执行"""
    data = ContextInfo.get_market_data(['close'], stock_code=['600519.SH'], period='1d', count=10)
    print(f"最新收盘价: {data['close'].iloc[-1]}")

def market_open(ContextInfo):
    """定时任务"""
    order_shares('600519.SH', 100, 'fix', 0, ContextInfo, '市价委托')
```

## 📊 核心功能

| 类别 | 说明 | 示例接口 |
|------|------|----------|
| 行情 | 实时/历史行情 | `ContextInfo.get_market_data()` |
| 历史 | 历史数据查询 | `ContextInfo.get_history_data()` |
| 交易 | 下单/撤单 | `order_shares()` |
| 持仓 | 持仓/委托查询 | `get_trade_detail_data()` |
| 股票池 | 设置股票池 | `ContextInfo.set_universe()` |
| 板块 | 板块成分股 | `get_stock_list_in_sector()` |

## 📖 更多示例

```python
def init(ContextInfo):
    ContextInfo.set_universe(['600519.SH'])
    ContextInfo.accountid = 'your_account'

def handlebar(ContextInfo):
    # 获取历史数据
    history = ContextInfo.get_history_data(10, '1d', 'close')
    
    # 查询持仓
    positions = get_trade_detail_data('your_account', 'stock', 'position')
    for pos in positions:
        print(f"{pos.m_strInstrumentID}: {pos.m_nVolume}股")
    
    # 获取板块成分
    stocks = get_stock_list_in_sector('沪深300')
```

## 📄 许可证

Proprietary - 券商授权使用

## 📊 更新日志

### v1.3.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接


### v1.2.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持QMT客户端策略开发与交易

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：http://dict.thinktrader.net/freshman/rookie.html
- **ClawHub**：https://clawhub.com
