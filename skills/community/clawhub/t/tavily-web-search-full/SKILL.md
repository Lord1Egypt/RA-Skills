---
name: tavily-web-search
description: Complete Tavily toolkit: Search, Extract, Usage, Crawl, Map, Research. All official APIs with safety controls.
homepage: https://tavily.com
version: 2.0.3
metadata: {
  "clawdbot": {
    "emoji": "🔍",
    "requires": {
      "bins": ["python3"],
      "env": ["TAVILY_API_KEY"]
    },
    "primaryEnv": "TAVILY_API_KEY"
  }
}
---

# Tavily Web Search

完整功能的 Tavily 网络搜索工具，基于官方 API 文档实现。专为 AI Agent 和 RAG 工作流设计。

## ✨ 功能特性

### 核心功能
- 🔄 **自动重试** - 3 次重试 + 指数退避
- 💾 **查询缓存** - 1 小时 TTL，节省 API 额度
- 📝 **详细日志** - `~/.openclaw/logs/tavily.log`
- 🎯 **多种输出** - JSON / Brave 兼容 / Markdown

### 官方 API 完整支持
| 功能 | 参数 | 说明 |
|------|------|------|
| **搜索深度** | `--search-depth` | `basic` / `advanced` / `fast` / `ultra-fast` |
| **主题分类** | `--topic` | `general` / `news` / `finance` |
| **时间过滤** | `--time-range` | `day` / `week` / `month` / `year` |
| **日期范围** | `--start-date` / `--end-date` | YYYY-MM-DD 格式 |
| **域名过滤** | `--include-domains` / `--exclude-domains` | 逗号分隔 |
| **国家定向** | `--country` | `united states` / `china` 等 |
| **AI 答案** | `--include-answer` / `--answer-type` | `basic` / `advanced` |
| **完整内容** | `--include-raw-content` | `markdown` / `text` |
| **图片搜索** | `--include-images` | 包含图片结果 |
| **自动参数** | `--auto-parameters` | AI 自动配置 |
| **精确匹配** | `--exact-match` | 精确短语匹配 |

## 📦 安装

### 从 ClawHub 安装（推荐）
```bash
clawhub install tavily-web-search-full
```

### 本地使用
Skill 已放置在：`~/.openclaw/workspace/skills/tavily-web-search/`

### 配置 API Key

```bash
# 方法 1: 添加到 ~/.openclaw/.env
echo "TAVILY_API_KEY=tvly-your-key-here" >> ~/.openclaw/.env

# 方法 2: 环境变量
export TAVILY_API_KEY="tvly-your-key-here"
```

获取 API Key: https://app.tavily.com/home (每月 1000 免费信用)

## 🚀 使用示例

### 🔍 Search API（搜索）

```bash
# 简单搜索（默认 compact Markdown 输出）
python3 {baseDir}/scripts/search.py --query "Python tutorial"

# 指定结果数量
python3 {baseDir}/scripts/search.py --query "Docker compose" --max-results 10

# 新闻搜索
python3 {baseDir}/scripts/search.py --query "AI breakthrough" --topic news --time-range day

# 深度研究
python3 {baseDir}/scripts/search.py --query "LLM architecture" --search-depth advanced

# 域名过滤
python3 {baseDir}/scripts/search.py --query "React" --include-domains "github.com,dev.to"
```

### 📄 Extract API（URL 内容提取）

```bash
# 提取单个 URL
python3 {baseDir}/scripts/extract.py --urls "https://example.com/article"

# 提取多个 URL
python3 {baseDir}/scripts/extract.py --urls "https://a.com,https://b.com,https://c.com"

# 带查询提取（按相关性重排内容）
python3 {baseDir}/scripts/extract.py --urls "https://example.com" --query "find pricing information"

# 高级提取（更详细，2 信用/5 URL）
python3 {baseDir}/scripts/extract.py --urls "https://example.com" --extract-depth advanced

# 包含图片
python3 {baseDir}/scripts/extract.py --urls "https://example.com" --include-images

# 输出为纯文本
python3 {baseDir}/scripts/extract.py --urls "https://example.com" --format text
```

### 📊 Usage API（使用量查询）

```bash
# 查看使用量（简洁模式）
python3 {baseDir}/scripts/usage.py

# 详细 Markdown 输出
python3 {baseDir}/scripts/usage.py --md

# JSON 输出
python3 {baseDir}/scripts/usage.py --json

# 查询特定项目
python3 {baseDir}/scripts/usage.py --project-id "my-project-123"
```

### 🕷️ Crawl API（网站爬取）⚠️ 默认禁用

**成本**: 3-5 信用/10 页 | **必须使用 `--enable`**

```bash
# 爬取网站（必须使用 --enable）
python3 {baseDir}/scripts/crawl.py --url "https://example.com" --enable

# 带指令爬取
python3 {baseDir}/scripts/crawl.py --url "https://example.com" --enable --instructions "find all pricing pages"

# 限制页数
python3 {baseDir}/scripts/crawl.py --url "https://example.com" --enable --limit 20
```

### 🗺️ Map API（网站地图）⚠️ 默认禁用

**成本**: 1-2 信用/10 页 | **必须使用 `--enable`**

```bash
# 生成网站地图
python3 {baseDir}/scripts/map.py --url "https://example.com" --enable

# 带指令
python3 {baseDir}/scripts/map.py --url "https://example.com" --enable --instructions "find all blog posts"

# 输出 URL 列表
python3 {baseDir}/scripts/map.py --url "https://example.com" --enable --output urls
```

### 📚 Research API（深度研究）⚠️⚠️ 强烈建议默认禁用

**成本**: 4-250 信用/次 | **必须使用 `--enable --confirm`**

```bash
# 深度研究（必须使用 --enable AND --confirm）
python3 {baseDir}/scripts/research.py --query "AI impact on healthcare" --enable --confirm

# Pro 模型（更贵但质量更高）
python3 {baseDir}/scripts/research.py --query "market analysis" --model pro --enable --confirm
```

### 新闻搜索
```bash
# 今日新闻
python3 {baseDir}/scripts/search.py --query "AI breakthrough" --topic news --time-range day

# 本周财经
python3 {baseDir}/scripts/search.py --query "stock market" --topic finance --time-range week

# 指定日期范围
python3 {baseDir}/scripts/search.py --query "election results" --start-date 2025-01-01 --end-date 2025-01-31
```

### 深度研究
```bash
# 高级模式（最高相关性，2 信用/次）
python3 {baseDir}/scripts/search.py --query "LLM architecture" --search-depth advanced

# 包含完整页面内容
python3 {baseDir}/scripts/search.py --query "React best practices" --include-raw-content markdown

# 详细 AI 答案
python3 {baseDir}/scripts/search.py --query "climate change impact" --answer-type advanced
```

### 域名过滤
```bash
# 只搜索特定网站
python3 {baseDir}/scripts/search.py --query "JavaScript tips" --include-domains "github.com,dev.to,medium.com"

# 排除某些网站
python3 {baseDir}/scripts/search.py --query "Python tutorial" --exclude-domains "w3schools.com"

# 组合使用
python3 {baseDir}/scripts/search.py --query "Rust programming" --include-domains "rust-lang.org,docs.rs" --exclude-domains "reddit.com"
```

### 国家/地区定向
```bash
# 美国科技新闻
python3 {baseDir}/scripts/search.py --query "tech startups" --country "united states" --topic news

# 中国财经
python3 {baseDir}/scripts/search.py --query "stock market" --country "china" --topic finance
```

### 图片搜索
```bash
# 搜索图片
python3 {baseDir}/scripts/search.py --query "sunset photography" --include-images

# 带描述
python3 {baseDir}/scripts/search.py --query "machine learning" --include-images --include-image-descriptions
```

### 快速搜索（低延迟）
```bash
# 快速模式（1 信用，低延迟）
python3 {baseDir}/scripts/search.py --query "weather today" --search-depth fast

# 超快速（1 信用，最低延迟）
python3 {baseDir}/scripts/search.py --query "stock price" --search-depth ultra-fast
```

### 自动参数
```bash
# 让 Tavily 自动配置（可能使用 advanced=2 信用）
python3 {baseDir}/scripts/search.py --query "comprehensive analysis of AI trends" --auto-parameters

# 自动参数但手动控制深度（控制成本）
python3 {baseDir}/scripts/search.py --query "research query" --auto-parameters --search-depth basic
```

### 精确匹配
```bash
# 精确搜索人名/公司名
python3 {baseDir}/scripts/search.py --query '"John Smith" CEO Acme Corp' --exact-match
```

## 📋 完整参数说明

```bash
python3 {baseDir}/scripts/search.py --help
```

### 必需参数
| 参数 | 说明 |
|------|------|
| `--query` | 搜索关键词（建议 <400 字符） |

### 搜索深度
| 参数值 | 延迟 | 相关性 | 内容类型 | 信用 |
|--------|------|--------|----------|------|
| `ultra-fast` | 最低 | 较低 | NLP 摘要 | 1 |
| `fast` | 低 | 良好 | 相关片段 | 1 |
| `basic` | 中等 | 高 | NLP 摘要 | 1 |
| `advanced` | 较高 | 最高 | 相关片段 | 2 |

## 💡 最佳实践

### 查询优化
- ✅ **保持查询简洁** - 建议 <400 字符
- ✅ **复杂查询拆分** - 分成多个小查询
- ✅ **使用精确匹配** - 人名/公司名用 `--exact-match`
- ✅ **合理设置 max-results** - 3-5 个足够（默认 5）

### 搜索深度选择
- `basic` - 日常搜索（推荐）
- `advanced` - 深度研究（特定问题）
- `fast` / `ultra-fast` - 实时应用

### 结果过滤
```bash
# 按相关性分数过滤
python3 scripts/search.py --query "Python" --min-score 0.7

# 只搜索特定域名
python3 scripts/search.py --query "React" --include-domains "github.com,dev.to"

# 排除低质量站点
python3 scripts/search.py --query "AI" --exclude-domains "content-farm.com"
```

### 成本优化
- ⚠️ **auto_parameters 可能使用 advanced**（2 信用）
- ✅ 手动设置 `--search-depth basic` 控制成本
- ✅ 使用缓存（默认开启）
- ✅ 批量提取 URL（5 个 URL = 1 信用）

## 💰 API 信用说明

### 日常 API（推荐）

| API | 操作 | 信用消耗 | 免费额度可用次数 |
|-----|------|----------|----------------|
| **Search** | basic/fast/ultra-fast | 1/次 | 1,000 次 |
| **Search** | advanced | 2/次 | 500 次 |
| **Extract** | basic | 1/5 URL | 5,000 URL |
| **Extract** | advanced | 2/5 URL | 2,500 URL |
| **Usage** | 查询 | 免费 | 无限 |

### 高级 API（默认禁用 ⚠️）

| API | 操作 | 信用消耗 | 免费额度可用次数 |
|-----|------|----------|----------------|
| **Map** | 标准 | 1/10 页 | ~10,000 页 |
| **Map** | 带指令 | 2/10 页 | ~5,000 页 |
| **Crawl** | basic | ~3/10 页 | ~3,300 页 |
| **Crawl** | advanced | ~5/10 页 | ~2,000 页 |

### 研究 API（极度昂贵 ⚠️⚠️）

| API | 模型 | 信用消耗 | 免费额度可用次数 |
|-----|------|----------|----------------|
| **Research** | mini | 4-110/次 | 9-250 次 |
| **Research** | pro | 15-250/次 | 4-66 次 |

**免费额度**: 1000 信用/月

### 安全控制

| API | 默认状态 | 启用方式 |
|-----|---------|---------|
| Search | ✅ 启用 | 直接使用 |
| Extract | ✅ 启用 | 直接使用 |
| Usage | ✅ 启用 | 直接使用 |
| Map | ❌ 禁用 | `--enable` |
| Crawl | ❌ 禁用 | `--enable` |
| Research | ❌ 禁用 | `--enable --confirm` |

### 节省信用技巧
1. 日常使用 Search/Extract/Usage
2. 启用缓存（默认开启）
3. 设置合理的 `max-results`（3-5 足够）
4. 避免不必要的 `include_raw_content`
5. 批量提取 URL（5 个 URL = 1 信用）
6. **谨慎使用 Crawl/Map/Research**

### 主题分类
- `general` - 通用搜索（默认）
- `news` - 新闻（包含 `published_date`）
- `finance` - 财经

### 时间过滤
- `--time-range`: `day` / `week` / `month` / `year`
- `--start-date`: YYYY-MM-DD
- `--end-date`: YYYY-MM-DD

### 输出格式
- `compact` - 简洁 Markdown（默认）
- `md` - 详细 Markdown（包含分数、完整内容）
- `brave` - JSON（兼容 web_search 格式）
- `raw` - 原始 JSON（包含所有字段）

## 💰 API 信用说明

| 操作 | 信用消耗 |
|------|----------|
| basic/fast/ultra-fast 搜索 | 1 |
| advanced 搜索 | 2 |
| include_answer (advanced) | +1 |
| include_raw_content | +1 |
| include_images | +1 |

**免费额度**: 1000 信用/月

### 节省信用技巧
1. 使用 `basic` 深度进行日常搜索
2. 启用缓存（默认开启）
3. 设置合理的 `max-results`（3-5 足够）
4. 避免不必要的 `include_raw_content`

## 🔄 自动更新

Tavily API 约每月更新 1-2 次。Skill 包含自动更新功能，定期检查官方 API 变更。

### 手动检查更新
```bash
# 检查是否有更新
python3 {baseDir}/scripts/update.py --check-only

# 应用更新
python3 {baseDir}/scripts/update.py

# 强制更新（即使无变更）
python3 {baseDir}/scripts/update.py --force

# 查看状态
python3 {baseDir}/scripts/update.py --status
```

### 自动更新（推荐）
添加每周检查的 cron 任务：
```bash
# 编辑 crontab
crontab -e

# 添加每周日 9:00 检查更新
0 9 * * 0 cd ~/.openclaw/workspace/skills/tavily-web-search && python3 scripts/update.py >> /tmp/tavily-update.log 2>&1
```

### 更新日志
- 更新记录：`{baseDir}/update.log`
- 最后检查：`{baseDir}/.last_check`
- 版本信息：`{baseDir}/_meta.json`

## 📁 文件位置

```
~/.openclaw/
├── .env                          # API key 配置
├── cache/tavily/                 # 缓存目录
│   ├── search/                   # Search 缓存
│   ├── extract/                  # Extract 缓存
│   ├── crawl/                    # Crawl 缓存
│   ├── map/                      # Map 缓存
│   └── research/                 # Research 缓存
├── logs/
│   ├── tavily.log                # Search 日志
│   ├── tavily_extract.log        # Extract 日志
│   ├── tavily_usage.log          # Usage 日志
│   ├── tavily_crawl.log          # Crawl 日志
│   ├── tavily_map.log            # Map 日志
│   └── tavily_research.log       # Research 日志
└── workspace/skills/tavily-web-search/
    ├── SKILL.md                  # 本文档
    ├── README.md                 # 快速开始
    ├── CHANGELOG.md              # 更新日志
    ├── _meta.json                # 版本信息
    ├── update.log                # 更新日志
    ├── .last_check               # 最后检查记录
    └── scripts/
        ├── search.py             # Search API（搜索）✅ 默认启用
        ├── extract.py            # Extract API（URL 提取）✅ 默认启用
        ├── usage.py              # Usage API（使用量查询）✅ 默认启用
        ├── crawl.py              # Crawl API（网站爬取）❌ 默认禁用
        ├── map.py                # Map API（网站地图）❌ 默认禁用
        ├── research.py           # Research API（深度研究）❌ 默认禁用
        ├── update.py             # 自动更新脚本
        └── test_all.py           # 测试套件
```

## 🔧 故障排除

### "Missing TAVILY_API_KEY"
```bash
# 检查配置
cat ~/.openclaw/.env | grep TAVILY

# 或设置环境变量
export TAVILY_API_KEY="tvly-xxx"
```

### "Search failed after 3 attempts"
- 检查网络连接
- 查看日志：`tail -f ~/.openclaw/logs/tavily.log`
- 验证 API key: https://app.tavily.com/home

### 清除缓存
```bash
rm -rf ~/.openclaw/cache/tavily/*
```

### 禁用缓存
```bash
python3 {baseDir}/scripts/search.py --query "test" --no-cache
```

## 📚 参考链接

- 官方文档：https://docs.tavily.com
- API 参考：https://docs.tavily.com/documentation/api-reference/endpoint/search
- 最佳实践：https://docs.tavily.com/documentation/best-practices/best-practices-search
- 管理平台：https://app.tavily.com
