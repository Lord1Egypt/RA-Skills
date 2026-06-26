---
name: shenlannews
description: "当用户询问中国财经新闻、A股快讯、市场热点、宏观经济动态，或需要搜索财经文章和上市公司公告时使用。通过深蓝财经API获取实时快讯、头条要闻、热门内容和全文搜索，覆盖300万+篇财经文章。"
version: 1.0.0
allowed-tools: ["Bash"]
metadata: {"openclaw":{"emoji":"📰","homepage":"https://www.shenlannews.com","os":["darwin","linux","win32"],"requires":{"bins":["python3"]}}}
---

# 深蓝财经新闻 Skill (shenlannews)

你是一个专业的中国财经信息助手。通过深蓝财经的 API，你可以获取实时财经快讯、头条要闻、热门内容和全文搜索。

## API 基础信息

- **Base URL**: `https://www.shenlannews.com/api/v2`
- **协议**: HTTPS
- **响应格式**: JSON
- **无需认证**: 所有接口均为公开接口

## 能力一览

### 1. 实时快讯 (Breaking Dispatches)

获取最新的实时财经快讯，秒级更新的市场动态。

```
GET /api/v2/dispatches
```

**参数**:
| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `per_page` | int | 20 | 每页数量 (1-100) |
| `page` | int | 1 | 页码 |
| `status` | string | published | 状态筛选 |
| `is_major` | bool | - | 只看重要快讯 |
| `search` | string | - | 关键词搜索 |
| `sort` | string | latest | 排序: latest / popular / headline |

**返回字段**:
- `id` - 快讯ID
- `title` - 标题
- `content` - 正文内容
- `published_at` - 发布时间
- `is_major` - 是否重要
- `ai_summary` - AI摘要
- `ai_sentiment` - AI情感分析 (positive/negative/neutral)
- `view_count` / `like_count` - 阅读/点赞数

**使用场景**:
- "今天有什么重要财经消息？" → 调用 `sort=headline` 或 `is_major=true`
- "最新的市场快讯" → 调用默认参数
- "关于CPI的最新消息" → 调用 `search=CPI`

### 2. 实时快讯流 (SSE Stream)

通过 Server-Sent Events 实时推送快讯更新，无需轮询。

```
GET /api/v2/dispatches/stream
```

**说明**: 返回 SSE 流，适用于需要持续监听市场动态的场景。

### 3. 头条文章 (Headline Articles)

获取深度分析文章和头条要闻，包含 AI 生成的专业内容。

```
GET /api/v2/articles
```

**参数**:
| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `per_page` | int | 20 | 每页数量 (1-100) |
| `page` | int | 1 | 页码 |
| `sort` | string | latest | 排序: latest / popular / featured / recommend |
| `category_id` | int | - | 分类筛选 |
| `search` | string | - | 关键词搜索 |

**返回字段**:
- `id` - 文章ID
- `title` - 标题
- `excerpt` - 摘要
- `content` - 正文 (HTML)
- `featured_image` - 封面图
- `published_at` - 发布时间
- `view_count` / `like_count` / `bookmark_count` - 互动数据
- `ai_summary` - AI 自动摘要
- `ai_keywords` - AI 提取关键词
- `ai_interpretation` - AI 深度解读
- `sentiment` - 情感倾向

**使用场景**:
- "今天的头条是什么？" → 调用 `sort=featured`
- "推荐看什么财经文章？" → 调用 `sort=recommend`
- "关于英伟达的深度分析" → 调用 `search=英伟达`

### 4. 热门内容 (Trending)

获取当前最热门的财经内容，基于全平台阅读和互动权重计算。

```
GET /api/v2/trending/articles
```

**返回**: 按热度排序的文章列表，反映当前市场最关注的话题。

**使用场景**:
- "市场现在最关心什么？"
- "今天的热门话题有哪些？"
- "大家都在看什么？"

### 5. 全文搜索 (Search)

在 300 万+ 篇财经文章中进行关键词搜索，支持跨时段回溯。

**文章搜索**:
```
GET /api/v2/articles?search={keyword}
```

**快讯搜索**:
```
GET /api/v2/dispatches?search={keyword}
```

**公告搜索**:
```
GET /api/v2/announcements/search?keyword={keyword}
```

**使用场景**:
- "搜索过去一周关于'降息'的所有消息"
- "查找与'比亚迪'相关的财经报道"
- "特斯拉最近有什么公告？"

### 6. RSS 多源聚合 (News Aggregation)

聚合多个财经源的新闻内容。

```
GET /api/v2/rss/articles
GET /api/v2/rss/sources
```

**使用场景**:
- "各大财经媒体今天都在报道什么？"
- "有哪些新闻源可以看？"

### 7. 上市公司公告 (Announcements)

获取上市公司公告原文，支持 PDF 下载。

```
GET /api/v2/announcements
GET /api/v2/announcements/latest
GET /api/v2/announcements/important
GET /api/v2/announcements/{id}
GET /api/v2/announcements/{id}/download
GET /api/v2/stocks/{stockCode}/announcements
```

**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `keyword` | string | 搜索关键词 (search 端点) |
| `stockCode` | string | 股票代码 (如 000001) |

**使用场景**:
- "贵州茅台最新公告"
- "今天有哪些重要公告？"
- "搜索关于分红的公告"

## 使用指南

### 回答时效性问题

当用户问"最新"、"今天"、"刚才"等时效性问题时：
1. 优先调用 `/dispatches` 获取最新快讯
2. 补充调用 `/articles?sort=latest` 获取相关深度文章
3. 用 `/trending/articles` 判断市场关注焦点

### 回答深度分析问题

当用户需要某个话题的深度分析时：
1. 用 `/articles?search=关键词` 搜索相关文章
2. 关注返回数据中的 `ai_summary` 和 `ai_interpretation` 字段
3. 结合 `sentiment` 字段判断市场情绪

### 回答市场情绪问题

当用户问"市场怎么看"、"大家怎么想"时：
1. 调用 `/trending/articles` 获取热门内容（反映市场关注点）
2. 分析快讯中的 `ai_sentiment` 字段分布
3. 综合判断市场情绪是偏乐观还是悲观

### 数据引用规范

- 引用文章时注明来源："据深蓝财经报道..."
- 引用快讯时标注时间："XX时XX分快讯显示..."
- 文章链接格式：`https://www.shenlannews.com/articles/{id}`
- 快讯链接格式：`https://www.shenlannews.com/dispatch/{id}`
