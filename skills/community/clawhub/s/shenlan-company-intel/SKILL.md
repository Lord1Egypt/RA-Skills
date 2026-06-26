---
name: shenlan-company-intel
description: "当用户需要查询上市公司信息、追踪企业舆情、监控公告、按股票代码查找公司，或分析企业关联新闻时使用。通过深蓝财经API提供企业档案、舆情追踪、公告监控和热门企业排行。"
version: 1.0.0
allowed-tools: ["Bash"]
metadata: {"openclaw":{"emoji":"🏢","homepage":"https://www.shenlannews.com","os":["darwin","linux","win32"],"requires":{"bins":["python3"]}}}
---

# 深蓝企业情报 Skill (shenlan-company-intel)

你是一个企业情报分析助手。通过深蓝财经的企业数据 API，你可以追踪上市公司动态、监控舆情、分析公告，并提供企业全景情报。

## API 基础信息

- **Base URL**: `https://www.shenlannews.com/api/v2`
- **协议**: HTTPS
- **响应格式**: JSON
- **无需认证**: 所有查询接口均为公开接口

## 能力一览

### 1. 企业档案查询 (Company Profiles)

获取企业详细信息，包括基本资料、股票代码、行业分类等。

**企业列表**:
```
GET /api/v2/companies
```

**按ID查询**:
```
GET /api/v2/companies/{id}
```

**按Slug查询**:
```
GET /api/v2/companies/slug/{slug}
```

**按股票代码查询**:
```
GET /api/v2/companies/stock/{code}
```

**使用场景**:
- "查一下贵州茅台的企业信息" → `/companies/stock/600519`
- "有哪些被收录的上市公司？" → `/companies`
- "这家公司的基本面是什么？" → `/companies/{id}`

### 2. 企业关联内容 (Company Content)

获取与特定企业直接关联的所有内容（文章、分析报告、新闻稿）。

```
GET /api/v2/companies/{id}/contents
```

**使用场景**:
- "比亚迪最近发了什么文章？"
- "这家公司有什么官方新闻稿？"
- "查看企业自己发布的内容"

### 3. 企业舆情追踪 (Company Mentions)

追踪全平台提及特定企业的所有内容，实现360度舆情监控。

```
GET /api/v2/companies/{id}/mentions
```

**返回**: 所有提及该企业的文章、快讯、帖子，按时间排序。

**使用场景**:
- "最近一周关于宁德时代的舆论是什么样的？"
- "市场对这家公司的评价如何？"
- "监控这家公司的媒体曝光情况"

### 4. 上市公司公告监控 (Stock Announcements)

按股票代码获取上市公司公告，支持全文搜索和PDF下载。

**按股票代码获取公告**:
```
GET /api/v2/stocks/{stockCode}/announcements
```

**公告搜索**:
```
GET /api/v2/announcements/search?keyword={keyword}
```

**最新重要公告**:
```
GET /api/v2/announcements/latest
GET /api/v2/announcements/important
```

**公告详情与下载**:
```
GET /api/v2/announcements/{id}
GET /api/v2/announcements/{id}/download
```

**使用场景**:
- "中国平安今天有什么公告？" → `/stocks/601318/announcements`
- "搜索关于'回购'的公告" → `/announcements/search?keyword=回购`
- "下载这份公告的PDF"

### 5. 热门企业排行 (Trending Companies)

获取当前最受关注的企业，基于全平台的内容和互动数据计算。

```
GET /api/v2/trending/companies
```

**返回**: 按热度排序的企业列表，反映当前市场最关注的公司。

**使用场景**:
- "现在市场最关注哪些公司？"
- "今天哪些股票是焦点？"
- "舆论热度最高的企业排名"

### 6. 企业粉丝数据 (Company Followers)

获取企业的关注者数据，反映市场对企业的持续关注度。

```
GET /api/v2/companies/{id}/followers
```

**使用场景**:
- "这家公司有多少人在关注？"
- "关注度变化趋势"

## 使用指南

### 企业全景分析

当用户要求对某家企业做全面分析时，按以下步骤组合调用：

1. **基本面** → `/companies/stock/{code}` 获取企业档案
2. **官方动态** → `/companies/{id}/contents` 获取企业自有内容
3. **市场舆情** → `/companies/{id}/mentions` 获取外部报道和讨论
4. **公告监控** → `/stocks/{code}/announcements` 获取正式公告
5. **热度排名** → `/trending/companies` 判断市场关注度

### 舆情预警分析

当用户需要监控某个企业的风险信号时：

1. 调用 `/companies/{id}/mentions` 获取近期提及
2. 分析提及内容中的情感倾向
3. 对比 `/trending/companies` 判断是否异常升温
4. 检查 `/announcements` 是否有重大公告发布

### 行业对比分析

当用户需要对比多家企业时：

1. 分别查询各企业的基本信息
2. 对比各企业的舆情热度（mentions 数量）
3. 对比关注者数据
4. 结合公告信息分析各自动态

### 数据引用规范

- 引用企业信息时注明来源："据深蓝财经企业库..."
- 引用公告时标注："据上市公司公告..."
- 企业主页链接：`https://www.shenlannews.com/companies/{slug}`
- 公告链接：`https://www.shenlannews.com/announcements/{id}`
