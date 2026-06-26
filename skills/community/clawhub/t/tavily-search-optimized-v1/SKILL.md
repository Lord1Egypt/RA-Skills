---
name: tavily-search
version: 1.0.0
description: "Web search via Tavily API (alternative to Brave). Use when the user asks to search the web / look up sources / find links and Brave web_search is unavailable or undesired. Returns a small set of relevant results (title, url, snippet) and can optionally include short answer summaries. Optimized with better error handling, caching, and configuration options."
---

# Tavily Search 🔍

使用Tavily API进行Web搜索（Brave搜索的替代方案）。当用户需要搜索网络、查找资料或链接，而Brave web_search不可用或不希望使用时使用此技能。

## 🚀 快速开始

### 1. 获取API密钥

1. 访问 [Tavily官网](https://tavily.com) 注册账号
2. 获取API密钥
3. 配置密钥（任选一种方式）：

```bash
# 方式1：环境变量
export TAVILY_API_KEY="your_api_key_here"

# 方式2：添加到 ~/.openclaw/.env 文件
echo "TAVILY_API_KEY=your_api_key_here" >> ~/.openclaw/.env
```

### 2. 基本使用

```bash
# 基本搜索（JSON格式）
python3 /root/.openclaw/skills/tavily-search/scripts/tavily_search.py \
  --query "OpenClaw是什么" \
  --max-results 5

# 包含答案摘要
python3 /root/.openclaw/skills/tavily-search/scripts/tavily_search.py \
  --query "最新AI发展" \
  --max-results 3 \
  --include-answer

# Markdown格式输出
python3 /root/.openclaw/skills/tavily-search/scripts/tavily_search.py \
  --query "Python编程教程" \
  --max-results 5 \
  --format md

# Brave兼容格式
python3 /root/.openclaw/skills/tavily-search/scripts/tavily_search.py \
  --query "机器学习" \
  --max-results 5 \
  --format brave
```

## 📖 完整命令参考

### 必需参数
- `--query` 或 `-q`: 搜索查询字符串（必需）

### 可选参数
- `--max-results` 或 `-m`: 最大结果数量 (默认: 5, 范围: 1-10)
- `--include-answer`: 包含答案摘要
- `--search-depth`: 搜索深度 (basic | advanced, 默认: basic)
- `--format`: 输出格式 (raw | brave | md, 默认: raw)
- `--timeout`: 请求超时时间（秒）(默认: 30)
- `--cache-ttl`: 缓存时间（秒）(默认: 300)
- `--verbose` 或 `-v`: 详细输出模式

### 高级用法

```bash
# 使用高级搜索深度
python3 /root/.openclaw/skills/tavily-search/scripts/tavily_search.py \
  --query "复杂技术问题" \
  --search-depth advanced \
  --max-results 10

# 启用缓存（5分钟）
python3 /root/.openclaw/skills/tavily-search/scripts/tavily_search.py \
  --query "常见问题" \
  --cache-ttl 300

# 详细模式查看请求详情
python3 /root/.openclaw/skills/tavily-search/scripts/tavily_search.py \
  --query "测试" \
  --verbose
```

## 📊 输出格式

### 1. raw (默认)
JSON格式，包含原始Tavily响应：
```json
{
  "query": "搜索词",
  "answer": "答案摘要（如果启用）",
  "results": [
    {
      "title": "结果标题",
      "url": "https://example.com",
      "content": "内容摘要"
    }
  ]
}
```

### 2. brave
与Brave搜索兼容的JSON格式：
```json
{
  "query": "搜索词",
  "answer": "答案摘要（如果启用）",
  "results": [
    {
      "title": "结果标题",
      "url": "https://example.com",
      "snippet": "内容摘要"
    }
  ]
}
```

### 3. md
人类可读的Markdown格式：
```markdown
1. 结果标题
   https://example.com
   - 内容摘要

2. 另一个结果
   https://example2.com
   - 另一个内容摘要
```

## ⚙️ 配置选项

### 支持的环境变量
脚本支持以下环境变量，优先级：命令行参数 > 环境变量 > 配置文件 > 默认值

| 环境变量 | 描述 | 默认值 |
|----------|------|--------|
| `TAVILY_API_KEY` | Tavily API密钥（必需） | 无 |
| `TAVILY_KEY` | Tavily API密钥别名 | 无 |
| `TAVILY_CACHE_DIR` | 缓存目录 | `~/.openclaw/cache/tavily` |
| `TAVILY_DEFAULT_TIMEOUT` | 默认超时时间（秒） | `30` |
| `TAVILY_CACHE_TTL` | 默认缓存TTL（秒） | `300` |
| `TAVILY_MAX_RESULTS` | 默认最大结果数 | `5` |
| `TAVILY_SEARCH_DEPTH` | 默认搜索深度 | `basic` |

### 配置文件示例
在 `~/.openclaw/.env` 中添加（参考 `config.example.env`）：
```env
# 必需配置
TAVILY_API_KEY=your_api_key_here

# 可选配置
TAVILY_CACHE_DIR=~/.openclaw/cache/tavily
TAVILY_DEFAULT_TIMEOUT=30
TAVILY_CACHE_TTL=300
TAVILY_MAX_RESULTS=5
TAVILY_SEARCH_DEPTH=basic
```

### 配置优先级
1. **命令行参数** - 最高优先级（如 `--timeout 45`）
2. **环境变量** - 次高优先级（如 `export TAVILY_DEFAULT_TIMEOUT=45`）
3. **配置文件** - 较低优先级（`~/.openclaw/.env` 文件）
4. **默认值** - 最低优先级

## 🔧 错误处理

脚本包含完善的错误处理：
- API密钥缺失时提供清晰提示
- 网络超时自动重试
- 无效响应格式检测
- 速率限制处理

## 🎯 使用场景

### 何时使用
1. Brave搜索不可用时
2. 需要更精确的搜索结果时
3. 希望获得答案摘要时
4. 需要缓存搜索结果时

### 何时不使用
1. 简单的本地查询
2. 不需要网络搜索的场景
3. 对延迟要求极高的场景

## 📝 最佳实践

1. **保持结果数量适中**: 默认3-5个结果以减少token消耗
2. **合理使用缓存**: 对重复查询启用缓存
3. **选择适当搜索深度**: 简单查询用basic，复杂查询用advanced
4. **监控API使用**: 注意Tavily的速率限制

## 🔒 安全与隐私

- API密钥安全存储
- 搜索查询加密传输
- 本地缓存可配置
- 无持久化日志

## 🆘 故障排除

### 常见问题
1. **API密钥错误**: 检查环境变量或.env文件
2. **网络超时**: 增加--timeout参数
3. **无结果返回**: 尝试不同的搜索词
4. **缓存问题**: 清除缓存目录或禁用缓存

### 调试命令
```bash
# 检查API密钥
python3 -c "import os; print('TAVILY_API_KEY:', os.environ.get('TAVILY_API_KEY', '未设置'))"

# 测试网络连接
curl -I https://api.tavily.com
```

---

*版本: 1.0.0 | 最后更新: 2026-04-15*
