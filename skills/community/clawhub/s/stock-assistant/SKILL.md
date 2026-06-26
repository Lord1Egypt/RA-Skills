---
name: stock-assistant
description: |
  A股交易辅助工具，集行情查询、交易记录管理、盈亏分析于一体。
  用于：(1) 查询A股实时行情 (2) 管理交易记录 (3) 计算持仓和盈亏 (4) 导入/导出CSV
  代码目录：D:\aicode\stock-assistant（跨平台：代码会自动适配路径）
  调用方式：from fetcher import get_quote 或 python main.py quote <股票代码>
---

# 炒股助手

A股交易辅助工具，提供行情查询、交易管理、盈亏分析功能。

## 代码位置

**项目目录**：`D:\aicode\stock-assistant`（Linux/Mac 路径相同）

```
D:\aicode\stock-assistant/
├── main.py          # CLI 入口
├── fetcher.py       # A股行情获取
├── trader.py        # 交易管理
├── models.py        # 数据模型
├── db.py            # SQLite 操作
├── requirements.txt # 依赖
└── data/            # 数据库目录
```

## 跨平台说明

代码已适配 Windows/Linux/Mac：
- Windows：`D:\aicode\stock-assistant\data\trades.db`
- Linux/Mac：自动使用脚本所在目录的 `data/trades.db`

Python import 时路径自动适配，无需手动指定。

## 快速命令

| 命令 | 说明 |
|------|------|
| `python main.py quote 600016` | 查询股票行情（完整数据） |
| `python main.py positions` | 查看当前持仓 |
| `python main.py pnl 600016` | 查看盈亏(自动获取实时价) |
| `python main.py pnl 600016 --price 4.15` | 查看盈亏(指定价格) |
| `python main.py list` | 列出所有交易记录 |
| `python main.py list --code 600016` | 列出指定股票交易记录 |
| `python main.py import trades.csv` | 从CSV导入交易记录 |
| `python main.py export --output trades.csv` | 导出交易记录到CSV |
| `python main.py add --code 600016 --type buy --quantity 1000 --price 3.90` | 添加买入记录 |
| `python main.py add --code 600016 --type sell --quantity 500 --price 4.20` | 添加卖出记录 |
| `python main.py delete <id>` | 删除指定ID的交易记录 |
| `python main.py notify 600016` | 查询并输出行情(飞书卡片格式) |
| `python main.py notify --codes 600016,000001` | 查询多只股票 |
| `python main.py notify --codes 600016 --webhook https://xxx` | 推送到飞书群机器人 |
| `python main.py notify --codes 600016 --app-id xxx --app-secret xxx --receive-id xxx` | 推送到飞书私聊 |

## 行情查询 API

### Python 调用方式

```python
import sys
import os

# 自动适配路径（Windows/Linux/Mac）
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from fetcher import get_quote
from trader import StockTrader

# 查询行情 - 返回完整字典数据
quote = get_quote('600016')

# 交易管理（无需指定路径，自动使用脚本所在目录）
trader = StockTrader()

# 返回字段说明：
# {
#     '股票代码': '600016',
#     '股票名称': '民生银行',
#     '当前价格': '3.97',
#     '涨跌额': '0.03',
#     '涨跌幅(%)': '0.76',
#     '今开价': '3.93',
#     '昨收价': '3.94',
#     '最高价': '4.05',
#     '最低价': '3.90',
#     '成交量(手)': '1552322',
#     '成交额(元)': '547876',
#     '换手率(%)': '2.35',
#     '市盈率(动态)': '6.52',
#     '市净率': '0.65',
#     '总市值(亿元)': '1825.63',
#     '流通市值(亿元)': '1523.85',
#     '涨停价': '4.35',
#     '跌停价': '3.55',
#     '买一价': '3.97', '买一量(手)': '10000',
#     '卖一价': '3.98', '卖一量(手)': '20000',
#     ... (买二~买五, 卖二~卖五),
#     '日期时间': '2026-03-14 14:30:00',
#     '_股票代码': 'sh600016',
#     '_市场': 'A股'
# }
```

### 返回字段完整列表

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| **基础信息** ||||
| 股票代码 | string | A股代码 | 600016 |
| 股票名称 | string | 上市公司名称 | 民生银行 |
| _市场 | string | 市场标识 | A股 |
| 日期时间 | string | 数据时间 | 2026-03-14 14:30:00 |
| **价格数据** ||||
| 当前价格 | string | 最新成交价 | 3.97 |
| 涨跌额 | string | 涨跌金额 | +0.03 |
| 涨跌幅(%) | string | 涨跌幅比例 | +0.76% |
| 今开价 | string | 今日开盘价 | 3.93 |
| 昨收价 | string | 昨日收盘价 | 3.94 |
| 最高价 | string | 今日最高价 | 4.05 |
| 最低价 | string | 今日最低价 | 3.90 |
| **成交数据** ||||
| 成交量(手) | string | 成交数量(手) | 1552322 |
| 成交额(元) | string | 成交金额 | 547876 |
| 换手率(%) | string | 日换手率 | 2.35% |
| **财务指标** ||||
| 市盈率(动态) | string | PE TTM | 6.52 |
| 市净率 | string | PB | 0.65 |
| 总市值(亿元) | string | 总市值 | 1825.63 |
| 流通市值(亿元) | string | 流通市值 | 1523.85 |
| **涨跌停** ||||
| 涨停价 | string | 当日涨停价 | 4.35 |
| 跌停价 | string | 当日跌停价 | 3.55 |
| **盘口数据（5档）** ||||
| 买一价~买五价 | string | 买入价位 | 3.97 |
| 买一量~买五量(手) | string | 买入挂单量 | 10000 |
| 卖一价~卖五价 | string | 卖出价位 | 3.98 |
| 卖一量~卖五量(手) | string | 卖出挂单量 | 20000 |

### CLI 输出格式

```bash
$ python main.py quote 600016

【A股行情】
==================================================
股票: 民生银行 (600016)
市场: A股

【价格】
当前价: 3.97
涨跌额: 0.03
涨跌幅: 0.76%

【开盘收盘】
今开: 3.93
昨收: 3.94
最高: 4.05
最低: 3.90

【成交】
成交量: 1552322 手
成交额: 547876 元
换手率: 2.35%

【财务指标】
市盈率(动态): 6.52
市净率: 0.65
总市值: 1825.63 亿元
流通市值: 1523.85 亿元

【涨跌停】
涨停价: 4.35
跌停价: 3.55

【盘口】
买一: 3.97 (10000) → 卖一: 3.98 (20000)
买二: 3.96 (15000) → 卖二: 3.99 (18000)
...

更新时间: 2026-03-14 14:30:00
```

## 交易管理 API

```python
import sys
sys.path.insert(0, 'D:\\aicode\\stock-assistant')
from trader import StockTrader

trader = StockTrader('D:\\aicode\\stock-assistant\\data\\trades.db')

# 导入CSV
trader.import_csv('trades.csv')

# 获取持仓
positions = trader.get_positions()

# 计算盈亏
pnl = trader.get_pnl_with_live_price('600016')
print(f"盈亏: {pnl.profit:.2f} ({pnl.profit_pct:.2f}%)")
```

## 数据格式

### CSV 导入/导出格式

```csv
日期,时间,股票代码,股票名称,买卖方向,成交数量,成交均价,成交金额,佣金,其他费用,印花税,过户费
2026-03-14,10:30:00,600016,民生银行,买入,1000,3.90,3900.00,2.73,0.30,0.00,0.04
2026-03-14,14:30:00,600016,民生银行,卖出,500,4.10,2050.00,1.44,0.20,2.05,0.02
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| 日期 | 是 | 交易日期，格式 YYYY-MM-DD |
| 时间 | 否 | 交易时间，格式 HH:MM:SS |
| 股票代码 | 是 | A股代码，如 600016 |
| 股票名称 | 否 | 股票名称，如 民生银行 |
| 买卖方向 | 是 | 买入/卖出 |
| 成交数量 | 是 | 股数 |
| 成交均价 | 是 | 价格 |
| 成交金额 | 是 | 数量 × 价格 |
| 佣金 | 否 | 手续费，默认0 |
| 其他费用 | 否 | 其他费用，默认0 |
| 印花税 | 否 | 印花税（卖出收），默认0 |
| 过户费 | 否 | 过户费，默认0 |

## 注意事项

1. **只支持A股** - 不支持港股、美股
2. **数据来源** - 腾讯财经（免费接口）
3. **存储** - SQLite 本地数据库 `data/trades.db`
4. **路径** - 所有路径使用 Windows 格式，如 `D:\aicode\stock-assistant`

## 后续更新

项目代码更新后，同步更新此 skill 文档。

---

## 更新规则

Skill 文件位置：`D:\aicode\stock-assistant\SKILL.md`

更新时同步修改：
- 项目代码更新后
- 新增功能后
- 参数变化后

直接编辑这个文件即可，格式是 Markdown。
