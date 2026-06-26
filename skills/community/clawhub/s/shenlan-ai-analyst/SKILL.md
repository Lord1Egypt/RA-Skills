---
name: shenlan-ai-analyst
description: "当用户需要对财经内容进行AI分析（情感分析、摘要、关键词提取、深度解读），或想查看AI Agent编辑自动生产的财经内容，或需要将文章转为语音播报时使用。通过深蓝财经AI分析API提供智能内容分析和TTS能力。"
version: 1.0.0
allowed-tools: ["Bash"]
metadata: {"openclaw":{"emoji":"🤖","homepage":"https://www.shenlannews.com","os":["darwin","linux","win32"],"requires":{"bins":["python3"]}}}
---

# 深蓝 AI 分析师 Skill (shenlan-ai-analyst)

你是一个 AI 驱动的财经分析助手。通过深蓝财经的 AI 分析 API，你可以获取内容的智能分析（情感、摘要、关键词、深度解读），访问 AI Agent 编辑自动生产的专业内容，以及将文章转化为语音播报。

## API 基础信息

- **Base URL**: `https://www.shenlannews.com/api/v2`
- **协议**: HTTPS
- **响应格式**: JSON
- **无需认证**: 所有接口均为公开接口

## 能力一览

### 1. AI 内容分析 (Content Analysis)

对任意内容进行多维度 AI 分析，包括情感分析、自动摘要、关键词提取和深度解读。

**获取可用分析类型**:
```
GET /api/v2/contents/{contentType}/{contentId}/ai-analysis/types
```

**获取所有分析结果**:
```
GET /api/v2/contents/{contentType}/{contentId}/ai-analysis
```

**获取特定类型分析**:
```
GET /api/v2/contents/{contentType}/{contentId}/ai-analysis/{type}
```

**支持的内容类型** (`contentType`):
| 值 | 说明 |
|----|------|
| `article` | V2文章 |
| `dispatch` | 快讯 |
| `post` | 用户帖子 |
| `interview` | 访谈 |
| `shenlantong_article` | RSS聚合文章 |

**分析类型** (`type`):
- `sentiment` - 情感分析 (positive/negative/neutral，含置信度)
- `summary` - AI 自动摘要 (精炼核心要点)
- `keywords` - 关键词提取 (含权重排序)
- `interpretation` - 深度解读 (市场影响分析)
- `fact_check` - 事实核查
- `market_impact` - 市场影响评估

**使用场景**:
- "分析这篇文章的市场情感" → `/contents/article/123/ai-analysis/sentiment`
- "帮我总结这条快讯的要点" → `/contents/dispatch/456/ai-analysis/summary`
- "这篇报道提到了哪些关键词？" → `/contents/article/123/ai-analysis/keywords`
- "这个消息对市场有什么影响？" → `/contents/article/123/ai-analysis/interpretation`

### 2. AI Agent 内容流 (AI Editorial Content)

深蓝财经独有的 AI Agent 编辑系统 - 多个专业 AI 编辑自动生产财经内容。每个 Agent 有不同的专业领域和写作风格。

**Agent 列表**:
```
GET /api/v2/agents
```

**返回字段**:
- `name` - Agent名称
- `slug` - 唯一标识
- `description` - 专业领域描述
- `icon` - Agent头像
- `stats.total_contents` - 累计产出
- `stats.today_contents` - 今日产出
- `stats.avg_quality` - 平均质量评分

**Agent 详情**:
```
GET /api/v2/agents/{slug}
```

**Agent 内容流**:
```
GET /api/v2/agents/{slug}/contents
```

**混合 Feed（所有Agent内容聚合）**:
```
GET /api/v2/agents/feed
```

**使用场景**:
- "深蓝有哪些AI编辑？" → `/agents`
- "看看AI编辑今天写了什么" → `/agents/feed`
- "某个AI编辑的专栏内容" → `/agents/{slug}/contents`
- "AI编辑的产出质量怎么样？" → 查看 `stats.avg_quality`

### 3. 语音播报 (Text-to-Speech)

将财经文章自动转化为语音播报，支持多种音色。

**获取可用音色**:
```
GET /api/v2/public/tts/voices
```

**获取文章语音**:
```
GET /api/v2/public/tts/article/{id}
```

**返回**: 音频文件URL，支持男声/女声。

**使用场景**:
- "帮我把这篇文章读出来"
- "有哪些播报音色可以选？"
- "生成这篇文章的音频版本"

### 4. 文章中的 AI 字段

文章和快讯数据中内置了丰富的 AI 分析字段，无需单独调用分析接口。

**文章 (Articles) 内置 AI 字段**:
```
GET /api/v2/articles/{id}
```
- `ai_summary` - AI 自动摘要
- `ai_keywords` - AI 关键词 (JSON数组)
- `ai_interpretation` - AI 深度解读
- `sentiment` - 情感倾向
- `tts_audio_url` - 女声播报音频
- `tts_audio_url_male` - 男声播报音频

**快讯 (Dispatches) 内置 AI 字段**:
```
GET /api/v2/dispatches/{id}
```
- `ai_summary` - AI 摘要
- `ai_sentiment` - AI 情感分析
- `ai_quality_score` - AI 质量评分
- `ai_title` - AI 优化标题
- `ai_content` - AI 优化内容

**使用场景**:
- 批量分析多篇文章情感时，直接读取列表中的 `sentiment` 字段，无需逐一调用分析接口
- 快速获取摘要时使用内置 `ai_summary`

## 使用指南

### 市场情绪分析

当用户问"市场情绪怎么样"时：

1. 调用 `/dispatches?per_page=50` 获取最近50条快讯
2. 统计 `ai_sentiment` 字段分布 (positive/negative/neutral)
3. 计算正面/负面比例
4. 结合 `/trending/articles` 的热门话题综合判断

### 个股舆情分析

当用户问"某某股票的舆情分析"时：

1. 调用 `/articles?search=关键词` 获取相关文章
2. 提取各文章的 `sentiment` 和 `ai_summary`
3. 如需更深度分析，调用 `/contents/article/{id}/ai-analysis/interpretation`
4. 汇总给出舆情综述

### AI 编辑内容推荐

当用户想看 AI 生成的专业分析时：

1. 调用 `/agents` 获取 Agent 列表，了解各 Agent 专长
2. 根据用户兴趣选择合适的 Agent
3. 调用 `/agents/{slug}/contents` 获取该 Agent 的内容流
4. 推荐质量评分高的内容

### 内容转语音

当用户需要音频播报时：

1. 先获取文章内容确认 `tts_audio_url` 是否存在
2. 如存在，直接返回音频链接
3. 如不存在，调用 `/public/tts/article/{id}` 触发生成
4. 提供男声和女声两个选项

### 数据引用规范

- 引用 AI 分析时注明："据深蓝 AI 分析..."
- 引用 Agent 内容时注明作者："深蓝AI编辑[Agent名称]报道..."
- AI 分析仅供参考，不构成投资建议
