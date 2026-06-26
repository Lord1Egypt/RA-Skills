# 算法计算口径库

本文档沉淀常用的数据计算口径，便于理解和复用。

---

## 1. 目标L值计算（满意度加权公式（集团口径））

### 中文名称

**满意度加权公式（集团口径）**

### 计算公式

```
目标L值 = (Z-1)/9*25 + (AA-1)/9*25 + (AB-1)/9*50
```

**规则**：
- 如果任一值 < 1，则该项贡献为0
- 结果保留4位小数

### 代码实现

```python
def calc_target_l(z_val: float, aa_val: float, ab_val: float) -> float:
    """
    计算目标L值：(Z-1)/9*25 + (AA-1)/9*25 + (AB-1)/9*50
    如果任一值 < 1，则该项贡献为0
    """
    result = 0.0
    if z_val >= 1:
        result += (z_val - 1) / 9 * 25
    if aa_val >= 1:
        result += (aa_val - 1) / 9 * 25
    if ab_val >= 1:
        result += (ab_val - 1) / 9 * 50
    return result
```

### 业务含义

| 字段 | 贡献占比 | 说明 |
|------|----------|------|
| Z列 | 25% | 第一类指标 |
| AA列 | 25% | 第二类指标 |
| AB列 | 50% | 第三类指标（权重最高）|

---

## 2. 同比计算

### 计算公式

```
同比 = (本期值 - 去年同期值) / 去年同期值 * 100%
```

### 代码实现

```python
def calc_yoy(current_val: float, last_year_val: float, decimal_places: int = 2) -> float:
    """
    计算同比增长率
    
    Args:
        current_val: 本期值
        last_year_val: 去年同期值
        decimal_places: 保留小数位数
    
    Returns:
        同比增长率（百分比），如 15.23 表示 15.23%
    """
    if last_year_val == 0:
        return 0.0 if current_val == 0 else float('inf')
    
    yoy = (current_val - last_year_val) / last_year_val * 100
    return round(yoy, decimal_places)

def format_yoy(yoy_val: float) -> str:
    """格式化同比为带箭头的字符串"""
    if yoy_val == float('inf'):
        return "新增"
    elif yoy_val > 0:
        return f"↑{yoy_val:.2f}%"
    elif yoy_val < 0:
        return f"↓{abs(yoy_val):.2f}%"
    else:
        return "持平"
```

### 使用示例

```python
# 示例
this_month = 1500
last_year_month = 1200

yoy = calc_yoy(this_month, last_year_month)
print(f"同比增长: {format_yoy(yoy)}")  # 输出: 同比增长: ↑25.00%
```

---

## 3. 环比计算

### 计算公式

```
环比 = (本期值 - 上期值) / 上期值 * 100%
```

### 代码实现

```python
def calc_qoq(current_val: float, last_period_val: float, decimal_places: int = 2) -> float:
    """
    计算环比增长率
    
    Args:
        current_val: 本期值
        last_period_val: 上期值（如上月、上周）
        decimal_places: 保留小数位数
    
    Returns:
        环比增长率（百分比）
    """
    if last_period_val == 0:
        return 0.0 if current_val == 0 else float('inf')
    
    qoq = (current_val - last_period_val) / last_period_val * 100
    return round(qoq, decimal_places)

def format_qoq(qoq_val: float) -> str:
    """格式化环比为带箭头的字符串"""
    if qoq_val == float('inf'):
        return "新增"
    elif qoq_val > 0:
        return f"↑{qoq_val:.2f}%"
    elif qoq_val < 0:
        return f"↓{abs(qoq_val):.2f}%"
    else:
        return "持平"
```

### 使用示例

```python
# 示例：本周与上周对比
this_week = 500
last_week = 480

qoq = calc_qoq(this_week, last_week)
print(f"环比增长: {format_qoq(qoq)}")  # 输出: 环比增长: ↑4.17%
```

---

## 4. 转化率计算

### 计算公式

```
转化率 = 转化数 / 访问数 * 100%
```

### 代码实现

```python
def calc_conversion_rate(converted: int, visitors: int, decimal_places: int = 2) -> float:
    """
    计算转化率
    
    Args:
        converted: 转化数（下单数、点击数等）
        visitors: 访问数（浏览数、进店数等）
        decimal_places: 保留小数位数
    
    Returns:
        转化率（百分比），如 3.45 表示 3.45%
    """
    if visitors == 0:
        return 0.0
    
    rate = converted / visitors * 100
    return round(rate, decimal_places)

def calc_funnel_rate(stage_n: int, stage_n_minus_1: int, decimal_places: int = 2) -> float:
    """
    计算漏斗各阶段转化率
    
    Args:
        stage_n: 当前阶段人数
        stage_n_minus_1: 上一阶段人数
    
    Returns:
        阶段转化率
    """
    if stage_n_minus_1 == 0:
        return 0.0
    
    return round(stage_n / stage_n_minus_1 * 100, decimal_places)

def calc_drop_rate(stage_n_minus_1: int, stage_n: int, decimal_places: int = 2) -> float:
    """
    计算流失率
    
    Args:
        stage_n_minus_1: 上一阶段人数
        stage_n: 当前阶段人数
    
    Returns:
        流失率
    """
    if stage_n_minus_1 == 0:
        return 0.0
    
    drop = stage_n_minus_1 - stage_n
    return round(drop / stage_n_minus_1 * 100, decimal_places)
```

### 使用示例

```python
# 漏斗分析
pv = 10000       # 页面浏览
uv = 5000        # 访客数
click = 1000     # 点击数
order = 200      # 下单数

print(f"点击率: {calc_conversion_rate(click, pv)}%")      # 10.0%
print(f"下单转化率: {calc_conversion_rate(order, uv)}%")   # 4.0%

# 漏斗转化
stage1 = 10000   # 浏览
stage2 = 5000    # 加购
stage3 = 1000    # 下单

print(f"加购转化率: {calc_funnel_rate(stage2, stage1)}%")  # 50.0%
print(f"下单转化率: {calc_funnel_rate(stage3, stage2)}%")   # 20.0%
print(f"整体转化率: {calc_funnel_rate(stage3, stage1)}%")   # 10.0%
```

---

## 5. 占比计算

### 计算公式

```
占比 = 部分值 / 总体值 * 100%
```

### 代码实现

```python
def calc_percentage(part: float, total: float, decimal_places: int = 2) -> float:
    """
    计算占比
    
    Args:
        part: 部分值
        total: 总体值
        decimal_places: 保留小数位数
    
    Returns:
        占比（百分比）
    """
    if total == 0:
        return 0.0
    
    return round(part / total * 100, decimal_places)

def calc_percentage_with_total_dict(data_dict: dict, decimal_places: int = 2) -> dict:
    """
    计算多个数据的占比
    
    Args:
        data_dict: {name: value} 格式的数据
        decimal_places: 保留小数位数
    
    Returns:
        {name: {'value': 原值, 'percentage': 占比}}
    """
    total = sum(data_dict.values())
    result = {}
    
    for name, value in data_dict.items():
        result[name] = {
            'value': value,
            'percentage': calc_percentage(value, total, decimal_places)
        }
    
    return result

def calc_contribution_ratio(part: float, total: float, decimal_places: int = 2) -> float:
    """
    计算贡献度（某部分对整体的贡献）
    
    Args:
        part: 部分增量
        total: 总体增量
    
    Returns:
        贡献度（百分比）
    """
    if total == 0:
        return 0.0
    
    return round(part / total * 100, decimal_places)
```

### 使用示例

```python
# 渠道占比
channels = {'线上': 8000, '线下': 5000, '代理': 3000}
total_sales = sum(channels.values())  # 16000

for name, value in channels.items():
    pct = calc_percentage(value, total_sales)
    print(f"{name}: {pct}%")

# 贡献度计算
overall_increase = 2000  # 整体增长
online_increase = 1200   # 线上增长

contribution = calc_contribution_ratio(online_increase, overall_increase)
print(f"线上渠道贡献度: {contribution}%")  # 60.0%
```

---

## 6. 排名计算

### 计算公式

```
排名 = 数据按降序排列后的序号
```

### 代码实现

```python
from typing import List, Dict, Tuple

def calc_rank(data: List[Dict], value_key: str, descending: bool = True) -> List[Dict]:
    """
    计算排名
    
    Args:
        data: 数据列表 [{name: 'A', value: 100}, ...]
        value_key: 值字段名
        descending: 是否降序（True=从大到小）
    
    Returns:
        带排名字段的数据列表
    """
    sorted_data = sorted(data, key=lambda x: x.get(value_key, 0), reverse=descending)
    
    for i, item in enumerate(sorted_data, 1):
        item['rank'] = i
    
    return sorted_data

def get_top_n(data: List[Dict], value_key: str, n: int = 10, descending: bool = True) -> List[Dict]:
    """
    获取Top N
    
    Args:
        data: 数据列表
        value_key: 值字段名
        n: 获取前几名
        descending: 是否降序
    
    Returns:
        Top N 数据列表
    """
    ranked = calc_rank(data, value_key, descending)
    return ranked[:n]

def calc_percentile_rank(value: float, all_values: List[float]) -> float:
    """
    计算百分位排名
    
    Args:
        value: 当前值
        all_values: 所有值列表
    
    Returns:
        百分位排名（0-100），如 85 表示超过了85%的数据
    """
    if not all_values:
        return 0.0
    
    count_below = sum(1 for v in all_values if v < value)
    return round(count_below / len(all_values) * 100, 2)
```

### 使用示例

```python
# 销售排名
sales_data = [
    {'name': '北京店', 'sales': 50000},
    {'name': '上海店', 'sales': 65000},
    {'name': '广州店', 'sales': 42000},
    {'name': '深圳店', 'sales': 58000},
]

ranked = calc_rank(sales_data, 'sales')
for item in ranked:
    print(f"第{item['rank']}名: {item['name']} - {item['sales']}")

# Top 3
top3 = get_top_n(sales_data, 'sales', 3)
print(f"Top 3: {[item['name'] for item in top3]}")
```

---

## 7. 列填充规则

### 业务降本推进项目规则

| 目标列 | 条件 | 计算方式 |
|--------|------|----------|
| E列 | `源L值 >= 1` 且 `T长度 >= 10` | 行数计数 |
| F列 | `源L值 >= 1` | 行数计数 |
| G列 | `源L值 >= 1` | 求和 |
| H列 | `源L值 >= 1` 且 `X="是"` | 行数计数（公式，禁止覆盖）|
| I列 | `X="是"` | 行数计数（无L限制）|
| K列 | `源L值 >= 1` 且 `源Z值 >= 1` | 平均值 = L/M |
| L列 | - | K列分子（sum_target_l）|
| M列 | - | K列分母（count_z_ge1）|

**验证公式**：当 M > 0 时，M/L = K

### 统计计数器结构

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MetricCounters:
    """指标计数器"""
    count_pos: int = 0           # 源L值>=1的行数
    sum_pos: float = 0.0         # 源L值之和
    count_pos_x_yes: int = 0     # L>=1且X="是"的计数
    count_pos_t_len: int = 0     # L>=1且T长度>=10的计数
    count_z_ge1: int = 0         # 源Z值>=1的计数
    sum_target_l: float = 0.0    # 目标L值之和

    def update(self, calc_val: float, x_yes: bool, t_len_ge10: bool, z_ge1: bool) -> None:
        """更新计数器"""
        self.count_pos += 1
        self.sum_pos += calc_val
        if x_yes:
            self.count_pos_x_yes += 1
        if t_len_ge10:
            self.count_pos_t_len += 1
        if z_ge1:
            self.count_z_ge1 += 1
            self.sum_target_l += calc_val
```

---

## 8. 日期处理

### 日期格式转换

```python
import re
from typing import Tuple
import datetime

def extract_month_day_from_yyyymmdd(v) -> Tuple[str, str]:
    """
    从日期值中提取月和日
    例如: 20260203 -> ("02", "03")
    支持格式：YYYYMMDD, YYYY-MM-DD, YYYY/MM/DD 等
    """
    s = safe_str(v)
    if not s:
        return ("", "")
    digits = re.sub(r"\D+", "", s)
    m = re.match(r"^(\d{4})(\d{2})(\d{2})$", digits)
    if not m:
        return ("", "")
    return m.group(2), m.group(3)

def convert_to_month_day(val) -> str:
    """将各种日期格式转换为X月X日格式"""
    if val is None:
        return ""
    
    # datetime对象
    if isinstance(val, datetime.datetime):
        return f"{val.month}月{val.day}日"
    if isinstance(val, datetime.date):
        return f"{val.month}月{val.day}日"
    
    # Excel日期序列号
    if isinstance(val, (int, float)):
        try:
            dt = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=val)
            return f"{dt.month}月{dt.day}日"
        except Exception:
            pass
    
    # 字符串解析
    digits = re.sub(r"\D+", "", safe_str(val))
    if len(digits) >= 8:
        m = re.match(r"^(\d{4})(\d{2})(\d{2})", digits)
        if m:
            month_int, day_int = int(m.group(2)), int(m.group(3))
            if 1 <= month_int <= 12 and 1 <= day_int <= 31:
                return f"{month_int}月{day_int}日"
    
    return ""
```

---

## 9. 数据验证

### 验证公式

```python
def validate_klm_relation(sum_target_l: float, count_z_ge1: int, k_avg: float) -> bool:
    """
    验证K/L/M列的关系：M/L = K（当M>0时）
    
    Args:
        sum_target_l: L列值（目标L值之和）
        count_z_ge1: M列值（Z>=1的计数）
        k_avg: K列值（平均值）
    
    Returns:
        验证是否通过
    """
    if count_z_ge1 <= 0:
        return k_avg == 0
    
    expected_k = round(sum_target_l / count_z_ge1, 4)
    return abs(expected_k - k_avg) < 0.0001
```

---

## 10. 新增算法模板

### 添加新算法的步骤

1. 在本文档中添加新的章节
2. 包含：公式、代码实现、业务含义
3. 提供使用示例
4. 添加到主索引（SKILL.md）

### 算法文档模板

```markdown
## N. 新算法名称

### 中文名称

**算法中文名称**

### 计算公式
```
公式描述
```

### 代码实现
```python
def algorithm_name(params):
    """算法说明"""
    pass
```

### 使用示例
```python
result = algorithm_name(data)
```

### 注意事项
- 注意点1
- 注意点2
```
