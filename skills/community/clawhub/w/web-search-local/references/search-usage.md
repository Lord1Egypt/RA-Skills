# Web Search Local - 详细用法指南

本文档提供 web-search-local 技能的详细用法说明和示例。

## 基本用法

### 安装依赖

```bash
pip install requests beautifulsoup4
```

### 基本搜索命令

```bash
# 基本搜索（默认 Bing 引擎）
python3 scripts/search.py -q "关键词"

# 限制结果数量
python3 scripts/search.py -q "关键词" -l 5

# 指定搜索引擎
python3 scripts/search.py -q "关键词" -e bing       # 必应（默认，推荐）
python3 scripts/search.py -q "关键词" -e webfetch   # urllib 备用（无需 requests）
python3 scripts/search.py -q "关键词" -e ddg        # DuckDuckGo
python3 scripts/search.py -q "关键词" -e yandex     # Yandex
python3 scripts/search.py -q "关键词" -e auto       # 自动故障转移（带详细日志）

# 跳过缓存（强制重新搜索）
python3 scripts/search.py -q "关键词" --no-cache

# 快速模式（跳过 Cookie 获取，减少延迟）
python3 scripts/search.py -q "关键词" --fast
```

### 输出选项

```bash
# 输出到文件
python3 scripts/search.py -q "关键词" -o results.json

# 人类可读文本格式输出
python3 scripts/search.py -q "关键词" -f text

# 组合使用：快速 + 文本格式 + 输出到文件
python3 scripts/search.py -q "关键词" --fast -f text -o results.txt

# 调试模式（显示详细日志 + 完成总结）
python3 scripts/search.py -q "关键词" -v
```

## 输出格式

### JSON 格式（默认）

```bash
python3 scripts/search.py -q "关键词" -f json
```

```json
{
  "query": "搜索关键词",
  "engine": "bing",
  "count": 3,
  "results": [
    {
      "title": "页面标题",
      "url": "https://...",
      "snippet": "摘要描述"
    }
  ],
  "elapsed_seconds": 0.58,
  "metadata": {
    "cookie_seconds": 0.0,
    "search_seconds": 0.519,
    "parse_seconds": 0.001
  }
}
```

`metadata` 包含各阶段耗时：

| 字段 | 说明 |
|------|------|
| `cookie_seconds` | Cookie 预获取耗时（fast 模式为 0） |
| `search_seconds` | 搜索请求耗时 |
| `parse_seconds` | 结果解析耗时 |
| `cache_hit` | 缓存命中时为 `true`，新搜索时不含此字段 |

**缓存命中示例：**
```json
"metadata": {
  "cookie_seconds": 0.0,
  "search_seconds": 0.0,
  "parse_seconds": 0.0,
  "cache_hit": true
}
```

**新搜索示例：**
```json
"metadata": {
  "cookie_seconds": 0.52,
  "search_seconds": 0.519,
  "parse_seconds": 0.001
}
```

### Text 格式（人类可读）

```bash
python3 scripts/search.py -q "关键词" -f text
```

```
搜索: python programming
引擎: bing
结果数: 2
============================================================

1. Python.org - Official Site
   https://python.org
   The official home of Python

2. PyPI - Python Package Index
   https://pypi.org
   Repository of Python software

搜索耗时: 0.58s
  [search 0.581s, parse 0.001s]
```

## 高级参数

### 语言设置

```bash
# 指定搜索语言
python3 scripts/search.py -q "python tutorial" --lang en      # 英文
python3 scripts/search.py -q "Python教程" --lang zh-Hans     # 中文简体
```

### 超时与颜色

```bash
# 自定义请求超时时间（秒）
python3 scripts/search.py -q "关键词" --timeout 5   # 5秒超时
python3 scripts/search.py -q "关键词" -t 3          # 3秒超时（缩写）

# 禁用 ANSI 颜色码（便于管道处理）
python3 scripts/search.py -q "关键词" -f text --no-color

# 组合：快速搜索 + 纯文本输出
python3 scripts/search.py -q "关键词" --fast -f text --no-color
```

### 重定向与排序

```bash
# 禁止 HTTP 重定向跟随（检测搜索引擎跳转链接）
python3 scripts/search.py -q "关键词" --no-redirect

# 结果排序方式（默认 relevance）
python3 scripts/search.py -q "关键词" --sort relevance   # 按相关性（默认）
python3 scripts/search.py -q "关键词" --sort date        # 按日期（RSS pubDate 有效时生效）
```

### 代理

```bash
# HTTP 代理
python3 scripts/search.py -q "关键词" --proxy "http://proxy:8080"

# SOCKS5 代理（需 pip install requests[socks]）
python3 scripts/search.py -q "关键词" --proxy "socks5://127.0.0.1:1080"
```

## 性能优化

### Fast 模式

`--fast` 参数跳过必应首页 Cookie 预获取步骤，可减少 2-5 秒延迟：

```bash
python3 scripts/search.py -q "关键词" --fast
```

**适用场景：**
- 脚本批量调用，需要速度
- 不需要 Cookie 验证的简单查询

**不适用场景：**
- 遇到反爬检测时（Cookie 有助于通过验证）

## 引擎选择建议

| 引擎 | 推荐度 | 说明 |
|------|--------|------|
| `bing` | ⭐⭐⭐ | 默认首选，支持 RSS 和 HTML 双模式 |
| `auto` | ⭐⭐⭐ | 自动故障转移，Bing → Yandex → DDG → WebFetch |
| `webfetch` | ⭐⭐ | 使用标准库 urllib，不依赖 requests 包 |
| `ddg` | ⭐ | DuckDuckGo，部分服务器可能被 SSL 封锁 |
| `yandex` | ⭐ | Yandex，部分 IP 可能触发 CAPTCHA |

**建议：** 默认使用 `bing`，如果失败则用 `auto`。

## 搜索策略

1. **RSS 优先** — Bing `format=rss` 端点，结构化输出，无广告
2. **HTML 回退** — RSS 失败时解析 HTML 搜索结果页
3. **多引擎故障转移** — `auto` 模式依次尝试 Bing → Yandex → DDG → WebFetch
4. **缓存加速** — 默认 1 小时本地缓存，相同查询秒回
5. **反爬策略** — Cookie 预获取、随机 UA、2-5 秒延迟、指数退避重试

## 缓存管理

### 缓存命令

```bash
# 自定义缓存过期时间（秒）
python3 scripts/search.py -q "关键词" --cache-ttl 300    # 5 分钟

# 查看缓存统计
python3 scripts/search.py --cache-stats
# 输出: {"total": 5, "valid": 3, "expired": 2, "total_size_kb": 3.2, "cache_dir": "..."}

# 清空所有缓存
python3 scripts/search.py --cache-clear
# 输出: {"action": "clear", "removed": 5}
```

### 缓存说明

- **位置：** `~/.cache/web-search-local/`
- **过期时间：** 1 小时（3600 秒，可自定义）
- **跳过：** 使用 `--no-cache` 参数
- **键：** 基于 `engine:query` 的 MD5 哈希

## 错误处理

脚本内置以下错误处理：

- **CAPTCHA 检测** — 自动识别验证码页面，指数退避重试
- **HTTP 错误** — 处理 403/429/503 状态码
- **超时** — 10 秒请求超时，自动重试
- **SSL 错误** — DDG 引擎可能被封，自动跳过
- **编码问题** — UTF-8 解码，错误字符替换

## 注意事项

- 中文搜索效果好，已针对 cn.bing.com 优化
- 每次搜索有 2-5 秒延迟（反爬策略）
- 缓存命中时无延迟
- 不支持需要登录才能查看的内容
- 结果取决于搜索引擎索引，可能有地域差异
- 需要 `requests` 包（`webfetch` 引擎除外，使用标准库 urllib）

### 并发安全

脚本使用模块级全局变量（`REQUEST_TIMEOUT`、`PROXY`、`NO_REDIRECT`、`USE_COLOR`）控制运行时配置，**不是线程安全的**。

- ✅ **安全：** 单进程串行调用（如 OpenClaw agent 单线程使用）
- ✅ **安全：** 多进程并行调用（每个进程独立的全局变量副本）
- ⚠️ **不安全：** 多线程并发调用且共享同一模块实例

**多线程场景建议：** 使用 `subprocess` 调用 CLI 而非直接 import 模块函数，或确保每次调用前后自行管理全局状态。
