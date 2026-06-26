# Data formats | 数据格式

## Input for `merge_batches.py` | `merge_batches.py` 输入格式

Each input file may be one of the following forms:  
每个输入文件可以是下面两种结构之一：

### Structure A | 结构 A

```json
{
  "results": [
    {
      "combo_name": "雪球抄作业A股",
      "combo_symbol": "ZH3537653",
      "best_record_at": "2/28/2026, 4:03:47 PM",
      "holdings": [
        {"stock_name": "紫金矿业", "stock_symbol": "SH601899", "weight": 13}
      ]
    }
  ],
  "failures": []
}
```

### Structure B | 结构 B

```json
{
  "comboHoldings": [...],
  "failures": [...]
}
```

## Patch JSON | 修补用 patch JSON

Pass a list and let the script overwrite combos by `combo_symbol`:  
传入一个列表，脚本会按 `combo_symbol` 覆盖对应组合：

```json
[
  {
    "combo_name": "目标三年三倍",
    "combo_symbol": "ZH3583033",
    "best_record_at": "2/2/2026, 10:22:36 PM",
    "holdings": [
      {"stock_name": "华夏银行", "stock_symbol": "SH600015", "weight": 100}
    ]
  }
]
```
