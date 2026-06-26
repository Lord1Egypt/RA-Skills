# 固收 + 产品数据查询脚本

此脚本用于批量查询 87 只固收 + 产品的 Wind 数据。

## 使用方法

### 1. 查询当日涨跌幅
```python
from wind_client import run_function

codes = [
    "010029.OF", "004534.OF", "018737.OF", "018846.OF", "012951.OF",
    "018597.OF", "163806.OF", "010942.OF", "011091.OF", "010940.OF",
    # ... 完整 87 只代码
]

date = "2026-03-24"
data = run_function("f_nav_adjustedreturn1", codes, date)
```

### 2. 查询近 1 年收益
```python
data = run_function("f_return_1y", codes, date)
```

### 3. 查询最大回撤
```python
start_date = "2024-03-24"
end_date = "2026-03-24"
data = run_function("f_risk_maxdownside", codes, start_date, end_date)
```

### 4. 查询最大回撤区间
```python
data = run_function("f_risk_maxdownside_date", codes, start_date, end_date)
```

## 分批查询策略

由于 Wind API 限制，建议分批查询:
- 低波赛道：30 只 (分 2 批，每批 15 只)
- 90 天赛道：5 只 (1 批)
- 中波赛道：22 只 (分 2 批，每批 11 只)
- 高波赛道：30 只 (分 2 批，每批 15 只)

## 输出格式

```json
{
  "010029.OF": {
    "当日涨跌幅": 0.85,
    "近 1 年收益": 11.38,
    "近 2 年最大回撤": -1.79,
    "最大回撤区间": "2024-08-08 至 2024-10-09"
  },
  ...
}
```
