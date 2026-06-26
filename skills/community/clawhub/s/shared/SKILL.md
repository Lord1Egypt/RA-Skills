---
name: stock-cache-utils
description: 股票技能通用缓存工具模块。支持交易时间检测、自动缓存、有效期管理。
---

# 股票技能缓存工具模块

为所有股票交易 skill 提供统一的缓存机制。

## 功能

- ✅ 交易时间自动检测（A 股交易时段）
- ✅ 缓存读取/保存
- ✅ 缓存有效期管理（24 小时）
- ✅ 自动降级处理

## 使用方法

```python
from cache_utils import StockDataCache, check_trading_status

# 初始化缓存
cache = StockDataCache(cache_dir='./.cache', cache_max_age_hours=24)

# 检查交易状态
status = check_trading_status()
if status['is_trading_time']:
    # 交易时间：获取实时数据
    data = fetch_realtime_data()
    cache.save(data)
else:
    # 非交易时间：使用缓存
    if cache.should_use_cache():
        data = cache.load()
    else:
        data = fetch_realtime_data()
```

## API

### StockDataCache

```python
cache = StockDataCache(cache_dir, cache_max_age_hours=24)

# 判断是否使用缓存
cache.should_use_cache()

# 加载缓存
data = cache.load()

# 保存缓存
cache.save(data)

# 清除缓存
cache.clear()

# 获取缓存信息
info = cache.get_cache_info()
```

### check_trading_status

```python
status = check_trading_status()
# 返回：
# {
#   'current_time': '2026-03-21 00:07:49',
#   'weekday': 'Saturday',
#   'is_trading_day': False,
#   'is_trading_time': False,
#   'next_trading_time': '2026-03-23 09:30:00'
# }
```

## 缓存策略

| 时段 | 行为 |
|------|------|
| 交易日 9:30-15:30 | 获取实时数据 |
| 其他时间 | 使用缓存（24 小时有效） |

## 依赖

- Python 3.10+
- 无额外依赖

## 许可证

MIT
