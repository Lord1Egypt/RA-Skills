# cn-stock-volume 浏览器调用 - 最终实现方案

## 问题总结

经过多次尝试，发现以下方案都不可行：

1. ❌ `openclaw` CLI 命令不存在
2. ❌ Python 脚本中无法直接访问 `browser` 对象
3. ❌ `subprocess` 无法调用 OpenClaw 工具
4. ❌ `sessions_spawn` 需要 openclaw CLI

## 可行方案

### 方案 A：手动补充数据（当前使用）✅

**说明**：承认技术限制，使用占位符，让用户手动补充数据。

**实现**：
- `fetch_data.py` 返回占位符
- 用户通过 `补数据.py` 脚本补充成交量
- 指数数据通过其他方式获取（如手动查询）

**优点**：
- 简单可靠
- 不依赖外部工具
- 用户可以控制数据质量

**缺点**：
- 需要手动操作
- 无法自动化

### 方案 B：使用 web_fetch Python 模块

**说明**：如果 OpenClaw 提供 `web_fetch` Python 模块，可以直接调用。

**检查方法**：
```python
try:
    from openclaw import web_fetch
    result = web_fetch.fetch(url, extractMode='text')
except ImportError:
    print("web_fetch 模块不可用")
```

### 方案 C：创建 Skill 并通过 sessions_send 调用

**说明**：创建一个独立的 skill，通过 sessions_send 发送消息触发执行。

**流程**：
1. 创建 `cn-stock-volume-fetcher` skill
2. 该 skill 使用 browser 工具获取数据
3. 通过 sessions_send 发送消息触发
4. 结果保存到文件，generate_report.py 读取

**优点**：
- 可以正确使用 browser 工具
- 完全自动化

**缺点**：
- 需要额外的 skill
- 异步执行，需要等待结果

### 方案 D：使用 requests + BeautifulSoup（不推荐）

**说明**：直接使用 HTTP 请求获取网页内容。

**问题**：
- 同花顺问财使用 JavaScript 渲染
- 需要处理反爬虫机制
- 不稳定

## 推荐方案：方案 A + C 结合

### 短期（立即使用）

使用方案 A，接受占位符数据：
```python
# fetch_data.py 返回
{
  "indices": {
    "shanghai": {"point": None, "change": None, "note": "需手动补充"},
    ...
  }
}
```

### 中期（1-2 天）

实现方案 C：
1. 创建 `fetch-index-data` skill
2. 该 skill 使用 browser 工具
3. generate_report.py 通过 sessions_send 触发
4. 等待结果后继续

### 长期（优化）

与 OpenClaw 团队合作，提供 Python SDK：
```python
from openclaw.tools import browser, web_fetch

# 直接使用
browser.navigate(url)
snapshot = browser.snapshot()
```

## 当前状态

**generate_report.py 已修改为**：
- 使用 sessions_spawn 调用（方案 C 的简化版）
- 如果失败，使用占位符数据继续
- 报告中标注"暂缺"字段

**下一步**：
1. 测试 sessions_spawn 方案
2. 如果不可行，回退到占位符方案
3. 创建独立的 browser skill

## 代码位置

- `scripts/fetch_data.py` - 核心数据获取（当前返回占位符）
- `scripts/fetch_iwencai_index.py` - 解析逻辑（已实现）
- `scripts/generate_report.py` - 报告生成（已修改为 sessions_spawn）
- `BROWSER_IMPLEMENTATION.md` - 详细设计文档
