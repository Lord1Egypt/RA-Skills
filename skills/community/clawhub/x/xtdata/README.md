# XtData 行情数据模块 Skill

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](http://dict.thinktrader.net/nativeApi/xtdata.html)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

XtQuant行情数据模块，提供实时行情、K线、Tick、Level2和财务数据。

## ✨ 特性

- 📡 **实时行情** - 全市场实时行情推送和快照
- 📊 **多周期K线** - 1分钟到日线多周期K线数据
- 📈 **Level2数据** - 逐笔成交、逐笔委托、十档行情
- 💰 **财务数据** - 完整的上市公司财务报表数据
- 🗂️ **板块管理** - 板块成分股查询和自定义板块

## 📥 安装

```bash
pip install xtquant
```

## ⚙️ 配置

需 miniQMT 客户端运行：

```python
from xtquant import xtdata

# 连接行情服务（需miniQMT运行）
xtdata.connect()
```

## 🚀 快速开始

```python
from xtquant import xtdata

# 连接行情服务
xtdata.connect()

# 下载历史数据
xtdata.download_history_data('000001.SZ', '1d', start_time='20240101')

# 获取K线数据
data = xtdata.get_market_data_ex([], ['000001.SZ'], period='1d', start_time='20240101')
print(data['000001.SZ'].head())
```

## 📊 支持的数据类型

| 类别 | 说明 | 示例接口 |
|------|------|----------|
| K线数据 | 多周期K线 | `get_market_data_ex()` |
| 实时行情 | 订阅推送 | `subscribe_quote()` |
| 全市场快照 | Tick快照 | `get_full_tick()` |
| 历史下载 | 批量下载 | `download_history_data()` |
| 财务数据 | 财务报表 | `get_financial_data()` |
| 板块成分 | 板块查询 | `get_stock_list_in_sector()` |

## 📖 更多示例

```python
from xtquant import xtdata

# 订阅实时行情
xtdata.subscribe_quote('000001.SZ', period='1d', callback=on_data)

# 全市场快照
snapshot = xtdata.get_full_tick(['SH', 'SZ'])

# 财务数据
fin_data = xtdata.get_financial_data(['000001.SZ'], table_list=['Balance', 'Income'])

# 板块成分股
stocks = xtdata.get_stock_list_in_sector('沪深A股')
```

## 📄 许可证

Apache License 2.0

## 📊 更新日志

### v1.3.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接


### v1.2.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持实时行情、K线、Tick、Level2和财务数据

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：http://dict.thinktrader.net/nativeApi/xtdata.html
- **ClawHub**：https://clawhub.com
