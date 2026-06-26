# Tavily Web Search Skill - v2.0.0

完整功能的 Tavily 工具包，包含所有 6 个官方 API。基于官方 API 文档实现。

## 📦 ClawHub 发布

- **Slug**: `tavily-web-search-full`
- **版本**: 2.0.0
- **发布**: ✅ 已发布到 ClawHub
- **APIs**: Search + Extract + Usage + Crawl + Map + Research

## 🚀 快速开始

### ✅ 日常 API（默认启用）

```bash
# Search - 网络搜索
python3 scripts/search.py --query "你的问题"

# Extract - URL 内容提取
python3 scripts/extract.py --urls "https://example.com/article"

# Usage - 查看使用量
python3 scripts/usage.py
```

### ⚠️ 高级 API（默认禁用 - 需 `--enable`）

```bash
# Crawl - 网站爬取（3-5 信用/10 页）
python3 scripts/crawl.py --url "https://example.com" --enable

# Map - 网站地图（1-2 信用/10 页）
python3 scripts/map.py --url "https://example.com" --enable
```

### ⚠️⚠️ 研究 API（极度昂贵 - 需 `--enable --confirm`）

```bash
# Research - 深度研究（4-250 信用/次）
python3 scripts/research.py --query "AI impact" --enable --confirm
```

## 📊 API 对比

| API | 默认 | 成本 | 启用方式 |
|-----|------|------|---------|
| **Search** | ✅ | 1-2 信用/次 | 直接使用 |
| **Extract** | ✅ | 1-2 信用/5 URL | 直接使用 |
| **Usage** | ✅ | 免费 | 直接使用 |
| **Crawl** | ❌ | 3-5 信用/10 页 | `--enable` |
| **Map** | ❌ | 1-2 信用/10 页 | `--enable` |
| **Research** | ❌ | 4-250 信用/次 | `--enable --confirm` |

## 💰 成本说明

### 免费额度（1000 信用/月）可做：

- **Search (basic)**: 1,000 次
- **Extract (basic)**: 5,000 个 URL
- **Map**: 5,000-10,000 页
- **Crawl**: 2,000-3,300 页
- **Research (mini)**: 9-250 次
- **Research (pro)**: 4-66 次

### 建议

- ✅ **日常使用**: Search + Extract + Usage
- ⚠️ **偶尔使用**: Crawl + Map（需要时加 `--enable`）
- ❌ **谨慎使用**: Research（太贵，除非必要）

## 📁 文件结构

```
tavily-web-search/
├── SKILL.md              # 完整文档
├── README.md             # 本文件
├── CHANGELOG.md          # 更新日志
├── _meta.json            # v2.0.0
└── scripts/
    ├── search.py         # Search API ✅
    ├── extract.py        # Extract API ✅
    ├── usage.py          # Usage API ✅
    ├── crawl.py          # Crawl API ❌ (--enable)
    ├── map.py            # Map API ❌ (--enable)
    ├── research.py       # Research API ❌ (--enable --confirm)
    ├── update.py         # 自动更新
    └── test_all.py       # 测试套件
```

## 🔧 配置

需要 API Key，添加到 `~/.openclaw/.env`:
```
TAVILY_API_KEY=tvly-your-key-here
```

获取 Key: https://app.tavily.com/home（1000 免费信用/月）

## 📚 文档

详细文档见 `SKILL.md` 或运行：
```bash
python3 scripts/search.py --help
python3 scripts/extract.py --help
python3 scripts/crawl.py --help
python3 scripts/map.py --help
python3 scripts/research.py --help
```

## 🔗 链接

- ClawHub: https://clawhub.com/skills/tavily-web-search-full
- Tavily 官方：https://tavily.com
- API 文档：https://docs.tavily.com
