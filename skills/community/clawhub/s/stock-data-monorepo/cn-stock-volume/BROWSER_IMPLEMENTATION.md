# cn-stock-volume 浏览器调用实现方案

## 问题分析

当前 `fetch_data.py` 中的浏览器调用是 TODO 状态，返回占位符数据。

## 解决方案

由于 OpenClaw 的 browser 工具无法通过 subprocess 直接调用，我们需要采用以下方案：

### 方案 A：使用 sessions_spawn（推荐）⭐

创建一个 wrapper 脚本，通过 `openclaw sessions_spawn` 调用 browser 工具：

```python
# 伪代码
import subprocess

# 创建 task
task = """
1. browser navigate https://www.iwencai.com/unifiedwap/result?w=上证指数
2. browser snapshot refs="aria"
3. 解析 snapshot 提取指数数据
4. 返回 JSON
"""

# 执行
result = subprocess.run(
    ['openclaw', 'sessions', 'spawn', '--task', task, '--runtime', 'subagent'],
    capture_output=True, text=True
)
```

### 方案 B：使用 web_fetch 工具

```bash
openclaw web-fetch "https://www.iwencai.com/unifiedwap/result?w=上证指数" --extractMode text
```

### 方案 C：直接修改 generate_report.py

在 stock-daily-report 的 generate_report.py 中，直接使用 browser 工具 API（需要该脚本在 OpenClaw session 中执行）。

## 实现决策

**选择方案 C**：因为 stock-daily-report 的 generate_report.py 已经在 OpenClaw session 中执行，可以直接使用 browser 工具。

## 实现步骤

1. 修改 `generate_report.py` 的 `step1_fetch_index_data()` 方法
2. 直接使用 `browser.navigate()` 和 `browser.snapshot()`
3. 解析 snapshot 提取数据

## 数据源 URL

| 数据 | URL |
|------|-----|
| 上证指数 | https://www.iwencai.com/unifiedwap/result?w=上证指数 |
| 深证成指 | https://www.iwencai.com/unifiedwap/result?w=深证成指 |
| 创业板指 | https://www.iwencai.com/unifiedwap/result?w=创业板指 |
| 上涨家数 | https://www.iwencai.com/unifiedwap/result?w=A 股上涨家数 |
| 下跌家数 | https://www.iwencai.com/unifiedwap/result?w=A 股下跌家数 |

## 解析规则

### 指数数据
期望 snapshot 格式：
```
heading "上证指数 (000001)" [level=4]
generic [ref=e116]: 3367.95-20.50/-0.61%
```

提取：
- 点位：`3367.95`
- 涨跌幅：`-0.61`

### 涨跌家数
期望 snapshot 格式：
```
上涨家数为 1234 家
下跌家数为 4786 家
```

## 代码实现

见 `scripts/fetch_iwencai_index.py` - 提供解析函数和 browser 工具集成。

## 测试命令

```bash
# 测试解析逻辑
python3 scripts/fetch_iwencai_index.py

# 完整流程测试（需要 browser 工具）
python3 scripts/generate_report.py --verbose
```

## 注意事项

1. browser 工具需要在 OpenClaw session 中才能使用
2. 需要处理非交易日情况（自动往前推）
3. 需要添加缓存机制（避免重复请求）
4. 需要处理错误情况（单个数据失败不影响其他数据）
