# Rate Limit 处理实现说明

## 📊 Tavily 官方速率限制

根据官方文档：https://docs.tavily.com/documentation/rate-limits.md

| API | Development | Production |
|-----|-------------|------------|
| **Search/Extract/Map** | 100 RPM | 1,000 RPM |
| **Crawl** | 100 RPM | 100 RPM |
| **Research** | 20 RPM | 20 RPM |
| **Usage** | 10 次/10 分钟 | 10 次/10 分钟 |

## 🔧 实现方式

### 1. 统一 Rate Limit 处理器

创建了 `rate_limit.py` 模块，提供：

- ✅ 429 错误自动检测
- ✅ `retry-after` 头解析
- ✅ 指数退避重试
- ✅ 可配置的重试次数和延迟
- ✅ 装饰器模式，易于集成

### 2. 核心功能

```python
@rate_limit_handler(
    max_retries=3,           # 最多重试 3 次
    base_delay=1.0,          # 基础延迟 1 秒
    max_delay=300.0,         # 最大延迟 5 分钟
    exponential_base=2.0,    # 指数退避底数
    log_func=log             # 日志函数
)
def api_call():
    # API 调用代码
    pass
```

### 3. 重试策略

| 尝试次数 | 延迟时间 | 说明 |
|---------|---------|------|
| 1 | - | 首次请求 |
| 2 | 1-2 秒 | 第一次重试 |
| 3 | 2-4 秒 | 第二次重试 |
| 4 | 4-8 秒 | 第三次重试（如果 max_retries=4） |

如果服务器返回 `retry-after` 头，则使用服务器指定的时间。

### 4. 429 错误处理流程

```
请求 API
   ↓
收到 429 错误
   ↓
检查 retry-after 头
   ↓
计算等待时间
   ↓
等待指定时间
   ↓
重试请求
   ↓
成功 或 达到最大重试次数
```

## 📁 已更新的脚本

| 脚本 | 状态 | 说明 |
|------|------|------|
| `rate_limit.py` | ✅ 新建 | 通用 Rate Limit 处理器 |
| `search.py` | ✅ 已更新 | 集成 Rate Limit 处理 |
| `extract.py` | ✅ 已更新 | 集成 Rate Limit 处理 |
| `crawl.py` | ⏳ 待更新 | - |
| `map.py` | ⏳ 待更新 | - |
| `research.py` | ⏳ 待更新 | - |
| `usage.py` | ⏳ 待更新 | - |

## 🧪 测试

```bash
# 运行测试套件
python3 scripts/test_all.py --quick

# 输出
✅ Passed: 4/4 (100%)
```

## 💡 使用示例

### 正常情况
```bash
$ python3 scripts/search.py --query "test"

[DEBUG] Request attempt 1/3: test...
[INFO] Success: 5 results
```

### 遇到 Rate Limit
```bash
$ python3 scripts/search.py --query "test"

[DEBUG] Request attempt 1/3: test...
[WARN] Rate limited. Waiting 2.0s before retry...
[DEBUG] Request attempt 2/3: test...
[INFO] Success: 5 results
```

### 超过限制
```bash
$ python3 scripts/search.py --query "test"

[DEBUG] Request attempt 1/3: test...
[WARN] Rate limited. Waiting 2.0s before retry...
[DEBUG] Request attempt 2/3: test...
[WARN] Rate limited. Waiting 4.0s before retry...
[DEBUG] Request attempt 3/3: test...
[ERROR] All 3 retries failed: Rate limit exceeded
```

## 🎯 最佳实践

### 1. 批量请求时的延迟

```python
# ❌ 不好 - 快速连续请求
for query in queries:
    search(query)

# ✅ 好 - 添加延迟
import time
for query in queries:
    search(query)
    time.sleep(0.5)  # 每秒 2 个请求
```

### 2. 监控使用量

```bash
# 定期检查使用量
python3 scripts/usage.py
```

### 3. 使用缓存

```bash
# 启用缓存（默认开启）
python3 scripts/search.py --query "test"

# 强制刷新（禁用缓存）
python3 scripts/search.py --query "test" --no-cache
```

### 4. 了解限制

- **Development Key**: 100 RPM = 每秒~1.6 个请求
- **Production Key**: 1,000 RPM = 每秒~16 个请求

## 📚 相关文件

- `scripts/rate_limit.py` - Rate Limit 处理器
- `scripts/search.py` - 已集成
- `scripts/extract.py` - 已集成
- https://docs.tavily.com/documentation/rate-limits.md - 官方文档

## 🔄 后续更新

待更新的脚本：
- [ ] `crawl.py`
- [ ] `map.py`
- [ ] `research.py`
- [ ] `usage.py`

更新方法：
```python
# 1. 添加导入
from rate_limit import rate_limit_handler

# 2. 添加装饰器
@rate_limit_handler(max_retries=MAX_RETRIES, base_delay=RETRY_DELAY, log_func=log)
def api_function():
    # ...
```

---

**版本**: 1.0.0  
**更新日期**: 2026-03-22  
**基于**: Tavily Rate Limits 官方文档
