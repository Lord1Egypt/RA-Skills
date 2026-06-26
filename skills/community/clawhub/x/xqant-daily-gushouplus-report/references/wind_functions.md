# Wind 数据查询函数参考

本文件详细说明固收 + 产品监控所需的所有 Wind 数据查询函数。

---

## 1. 当日涨跌幅查询

### 函数
```
f_nav_adjustedreturn1(代码，日期)
```

### 参数
- `代码`: 6 位数字+.OF 格式 (如 010029.OF)
- `日期`: YYYY-MM-DD 格式 (如 2026-03-24)

### 返回值
- 当日涨跌幅 (%)，浮点数

### 示例
```python
data = run_function("f_nav_adjustedreturn1", "010029.OF", "2026-03-24")
# 返回：0.85
```

### 注意事项
- 必须使用精确日期，不能使用"当日"等模糊表述
- 非交易日会返回空值
- 周末/节假日需查询最近交易日数据

---

## 2. 近 1 年收益查询

### 函数
```
f_return_1y(代码，日期)
```

### 参数
- `代码`: 6 位数字+.OF 格式
- `日期`: YYYY-MM-DD 格式

### 返回值
- 近 1 年复权单位净值增长率 (%)，浮点数

### 示例
```python
data = run_function("f_return_1y", "010029.OF", "2026-03-24")
# 返回：11.38
```

### 注意事项
- 返回值为近 1 年区间收益率
- 对于成立不满 1 年的产品，返回成立以来收益率

---

## 3. 近 2 年最大回撤查询

### 函数
```
f_risk_maxdownside(代码，起始日期，结束日期)
```

### 参数
- `代码`: 6 位数字+.OF 格式
- `起始日期`: YYYY-MM-DD 格式 (如 2024-03-24)
- `结束日期`: YYYY-MM-DD 格式 (如 2026-03-24)

### 返回值
- 最大回撤幅度 (%)，负数表示 (如 -1.79)

### 示例
```python
data = run_function("f_risk_maxdownside", "010029.OF", "2024-03-24", "2026-03-24")
# 返回：-1.79
```

### 注意事项
- 窗口期必须为近 2 年 (730 天)
- 若产品成立时间不足 2 年，返回成立以来最大回撤

---

## 4. 最大回撤区间查询

### 函数
```
f_risk_maxdownside_date(代码，起始日期，结束日期)
```

### 参数
- 同 `f_risk_maxdownside`

### 返回值
- 字符串格式："YYYY/MM/DD 至 YYYY/MM/DD" (如 "2024/08/08 至 2024/10/09")
- 或 "YYYY-MM-DD 至 YYYY-MM-DD" 格式

### 示例
```python
data = run_function("f_risk_maxdownside_date", "010029.OF", "2024-03-24", "2026-03-24")
# 返回："2024/08/08 至 2024/10/09"
```

### 注意事项
- **优先使用 API 返回的日期**，即使与净值曲线不符
- 该日期用于归因分析的关键事件定位
- 若返回日期与产品历史重大事件不匹配，需人工复核

---

## 5. 基金基本信息查询

### 函数
```
f_myfund_basic(代码)
```

### 返回值
- 基金名称、基金代码、基金公司、成立日期、基金类型等

### 示例
```python
data = run_function("f_myfund_basic", "010029.OF")
# 返回：{"基金名称": "富国稳进回报 12 个月持有 A", "基金公司": "富国基金", ...}
```

### 用途
- 获取产品名称用于报告展示 (隐藏代码列)
- 获取基金类型用于分类验证

---

## 6. 赛道排名计算

### 计算方法
```python
# 假设已有 87 只产品的近 1 年收益数据
return_1y_data = {
    "010029.OF": 11.38,
    "004534.OF": 6.61,
    ...
}

# 按赛道分组
low_wave_codes = ["010029.OF", "004534.OF", ...]  # 30 只
nine_day_codes = ["016644.OF", "015479.OF", ...]  # 5 只
mid_wave_codes = ["014847.OF", "011096.OF", ...]  # 22 只
high_wave_codes = ["014767.OF", "011803.OF", ...] # 30 只

# 赛道内排名 (基于近 1 年收益)
def calculate_rank(codes, return_data):
    sorted_codes = sorted(codes, key=lambda c: return_data[c], reverse=True)
    rank_dict = {code: rank+1 for rank, code in enumerate(sorted_codes)}
    return rank_dict
```

### 注意事项
- **赛道独立性**: 每个赛道的排名仅基于该赛道内产品
- 低波赛道排名池：30 只
- 90 天赛道排名池：5 只
- 中波赛道排名池：22 只
- 高波赛道排名池：30 只

---

## 7. 批量查询优化

### 分批策略
由于 Wind API 限制，建议按以下策略分批查询:

```python
# 策略 1: 按赛道分批次
batches = {
    "低波": low_wave_codes,        # 30 只 → 分 2 批
    "90 天": nine_day_codes,       # 5 只 → 1 批
    "中波": mid_wave_codes,        # 22 只 → 分 2 批
    "高波": high_wave_codes,       # 30 只 → 分 2 批
}

# 策略 2: 按数据类型分批次
# 第 1 批：查询所有 87 只产品的当日涨跌幅
# 第 2 批：查询所有 87 只产品的近 1 年收益
# 第 3 批：查询所有 87 只产品的最大回撤
# 第 4 批：查询所有 87 只产品的最大回撤区间
```

### 超时处理
- 单次查询超时阈值：300 秒
- 超时后记录已查询部分
- 后续任务补全剩余数据

---

## 8. 数据验证规则

### 8.1 日期验证
```python
def validate_maxdownside_date(date_string, nav_curve):
    """
    验证最大回撤日期是否与净值曲线匹配
    若不匹配，优先以 API 返回为准
    """
    api_start, api_end = parse_date_range(date_string)
    
    # 检查 API 返回日期区间内是否存在明显净值下跌
    min_nav = min(nav_curve[api_start:api_end])
    max_nav = max(nav_curve[api_start:api_end])
    
    if (max_nav - min_nav) / max_nav < 0.01:  # 跌幅不足 1%
        log_warning(f"API 返回的回撤区间{date_string}与净值曲线不匹配")
    
    # 始终返回 API 数据
    return date_string
```

### 8.2 代码验证
```python
import re

def validate_code(code):
    """
    验证基金代码格式：6 位数字+.OF
    """
    pattern = r'^\d{6}\.OF$'
    if not re.match(pattern, code):
        raise ValueError(f"无效代码格式：{code}")
    return True
```

---

## 9. 错误处理

### 常见错误

| 错误代码 | 原因 | 处理方法 |
|----------|------|----------|
| 空值 | 非交易日/产品未成立 | 跳过或标记"N/A" |
| API_FAIL | Wind API 响应超时 | 重试 1 次，仍失败则标记 |
| CODE_INVALID | 代码格式错误 | 重新验证代码 |
| DATE_INVALID | 日期格式错误 | 检查日期格式 |

### 重试策略
```python
def query_with_retry(func, *args, max_retries=2):
    for attempt in range(max_retries):
        try:
            return func(*args)
        except TimeoutError:
            if attempt == max_retries - 1:
                return None  # 返回 None 表示查询失败
            time.sleep(5)  # 重试前等待 5 秒
```
