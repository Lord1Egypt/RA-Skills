---
name: tavily-search
description: "使用 Tavily AI 进行网络搜索、深度研究、内容提取。支持 search、research、extract 三个功能。"
---

# Tavily Search Skill

使用 Tavily 的 LLM 优化 API 进行网络搜索、深度研究和内容提取。

## 配置

API Key 保存在 `.env` 文件中（与 SKILL.md 同目录）:

```
TAVILY_API_KEY=tvly-your-key-here
```

获取免费 API Key: [https://tavily.com](https://tavily.com)

## 三个功能

### 1. Search - 网络搜索

快速搜索，返回相关结果。

```bash
python scripts/tavily_client.py "搜索内容"
```

**参数:**
| 参数 | 简写 | 默认 | 说明 |
|------|------|------|------|
| `--max-results` | `-n` | 10 | 结果数量 (1-20) |
| `--search-depth` | `-d` | advanced | 搜索深度: ultra-fast, fast, basic, advanced |
| `--time-range` | `-t` | null | 时间: day, week, month, year |
| `--json` | `-j` | false | 输出 JSON |

### 2. Research - 深度研究

对主题进行深入研究，返回完整答案和引用来源。（耗时 30-120 秒）

```bash
python scripts/tavily_research.py "量子计算发展趋势"
```

**参数:**
| 参数 | 简写 | 默认 | 说明 |
|------|------|------|------|
| `--model` | `-m` | mini | 模型: mini, pro, auto |
| `--max-results` | `-n` | null | 最大来源数 |
| `--output` | `-o` | null | 保存到文件 |
| `--json` | `-j` | false | 输出 JSON |

### 3. Extract - URL 内容提取

从指定 URL 提取干净的内容。

```bash
python scripts/tavily_extract.py "https://example.com"
```

**参数:**
| 参数 | 简写 | 默认 | 说明 |
|------|------|------|------|
| `--extract-depth` | `-d` | basic | 深度: basic, deep |
| `--output` | `-o` | null | 保存到文件 |
| `--json` | `-j` | false | 输出 JSON |

## 示例

```bash
# 搜索
python scripts/tavily_client.py "AI 新闻" --max-results 5 --time-range week

# 研究（需等待）
python scripts/tavily_research.py "Python vs JavaScript" --model pro --output report.md

# 提取
python scripts/tavily_extract.py "https://github.com" --output content.md
```
