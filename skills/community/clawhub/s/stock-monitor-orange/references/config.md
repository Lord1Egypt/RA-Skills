# 配置文件说明

## 概述

股票监控技能使用 JSON 格式的配置文件存储数据，存放在 `~/.openclaw/` 目录下。

---

## 股票池配置

**文件路径：** `~/.openclaw/stock-pool.json`

**说明：** 定义需要监控的股票列表

**结构：**
```json
{
  "stocks": {
    "600900": { "name": "长江电力", "type": "A" },
    "00992": { "name": "联想集团", "type": "HK" }
  },
  "updated": "2026-03-29T10:00:00.000000"
}
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| stocks | object | 股票字典，key为代码 |
| name | string | 股票名称 |
| type | string | 股票类型：`A`(A股)、`HK`(港股) |
| updated | string | 最后更新时间 |

**操作命令：**
```bash
python stock_monitor.py add 600900      # 添加
python stock_monitor.py remove 600900    # 移除
python stock_monitor.py list              # 列出全部
```

---

## 持仓记录

**文件路径：** `~/.openclaw/stock-positions.json`

**说明：** 记录当前持有的股票及成本

**结构：**
```json
{
  "positions": {
    "600900": {
      "quantity": 6000.0,
      "cost_price": 28.69,
      "updated": "2026-03-27T09:56:00.931391"
    },
    "00992": {
      "quantity": 4000.0,
      "cost_price": 9.41,
      "updated": "2026-03-27T09:56:11.939610"
    }
  },
  "updated": "2026-03-27T09:58:34.076944"
}
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| positions | object | 持仓字典，key为股票代码 |
| quantity | number | 持股数量 |
| cost_price | number | 成本价 |
| updated | string | 最后更新时间 |

**操作命令：**
```bash
python stock_monitor.py position add 600900 6000 28.69  # 添加/更新持仓
python stock_monitor.py position remove 600900           # 清除持仓
python stock_monitor.py position list                     # 查看持仓
python stock_monitor.py position 600900                   # 分析单只持仓
```

---

## 交易记录

**文件路径：** `~/.openclaw/stock-trades.json`

**说明：** 记录所有买卖交易历史

**结构：**
```json
{
  "trades": [
    {
      "id": "t_1701234567890",
      "code": "600900",
      "type": "buy",
      "quantity": 1000,
      "price": 28.50,
      "date": "2026-03-20T10:30:00.000000"
    },
    {
      "id": "t_1701245678901",
      "code": "600900",
      "type": "sell",
      "quantity": 500,
      "price": 29.00,
      "date": "2026-03-25T14:20:00.000000"
    }
  ],
  "updated": "2026-03-25T14:20:00.000000"
}
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| trades | array | 交易列表 |
| id | string | 交易ID（时间戳生成） |
| code | string | 股票代码 |
| type | string | 交易类型：`buy` 或 `sell` |
| quantity | number | 交易数量 |
| price | number | 成交价格 |
| date | string | 成交时间 |

**操作命令：**
```bash
python stock_monitor.py trade buy 600900 1000 28.50   # 记录买入
python stock_monitor.py trade sell 600900 500 29.00  # 记录卖出
python stock_monitor.py trades                        # 查看全部记录
python stock_monitor.py trades 600900                  # 查看特定股票记录
```

---

## 预警配置

**文件路径：** `~/.openclaw/stock-alerts.json`

**说明：** 定义各股票的预警规则

**结构：**
```json
{
  "alerts": {
    "600900": {
      "cost_pct_above": 15.0,
      "cost_pct_below": -12.0,
      "change_pct_above": 4.0,
      "change_pct_below": -4.0,
      "volume_surge": 2.0,
      "ma_monitor": true,
      "rsi_monitor": true,
      "gap_monitor": true,
      "trailing_stop": true
    }
  },
  "updated": "2026-03-29T10:00:00.000000"
}
```

**字段说明：**
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| cost_pct_above | number | 15.0 | 盈利达到此比例提醒（%） |
| cost_pct_below | number | -12.0 | 亏损达到此比例提醒（%） |
| change_pct_above | number | 4.0 | 日内涨幅超此比例提醒（%） |
| change_pct_below | number | -4.0 | 日内跌幅超此比例提醒（%） |
| volume_surge | number | 2.0 | 放量倍数阈值 |
| ma_monitor | boolean | true | 是否监控均线金叉/死叉 |
| rsi_monitor | boolean | true | 是否监控RSI超买超卖 |
| gap_monitor | boolean | true | 是否监控跳空缺口 |
| trailing_stop | boolean | true | 是否启用动态止盈 |

---

## 资金流向配置

**文件路径：** `~/.openclaw/stock-capital-config.json`

**说明：** 资金流向分析的配置参数

**结构：**
```json
{
  "config": {
    "threshold_large": 1000000,
    "threshold_huge": 5000000,
    "refresh_interval": 300
  }
}
```

---

## 快速操作汇总

| 任务 | 操作 | 文件 |
|------|------|------|
| 添加股票到监控 | `add <code>` | stock-pool.json |
| 查看监控列表 | `list` | stock-pool.json |
| 添加/更新持仓 | `position add <code> <qty> <cost>` | stock-positions.json |
| 查看持仓 | `position list` | stock-positions.json |
| 记录买入 | `trade buy <code> <qty> <price>` | stock-trades.json |
| 记录卖出 | `trade sell <code> <qty> <price>` | stock-trades.json |
| 查看交易记录 | `trades [code]` | stock-trades.json |

---

## 备份与恢复

配置文件均为 JSON 格式，可直接复制备份：

```powershell
# 备份
Copy-Item "$env:USERPROFILE\.openclaw\stock-pool.json" "stock-pool.json.bak"
Copy-Item "$env:USERPROFILE\.openclaw\stock-positions.json" "stock-positions.json.bak"

# 恢复
Copy-Item "stock-pool.json.bak" "$env:USERPROFILE\.openclaw\stock-pool.json"
Copy-Item "stock-positions.json.bak" "$env:USERPROFILE\.openclaw\stock-positions.json"
```
