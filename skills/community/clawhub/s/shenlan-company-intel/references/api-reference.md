# 深蓝企业情报 API 参考文档

## 端点总览

| 端点 | 方法 | 说明 | 认证 |
|------|------|------|------|
| `/api/v2/companies` | GET | 企业列表 | 否 |
| `/api/v2/companies/{id}` | GET | 企业详情 | 否 |
| `/api/v2/companies/slug/{slug}` | GET | 按Slug查企业 | 否 |
| `/api/v2/companies/stock/{code}` | GET | 按股票代码查企业 | 否 |
| `/api/v2/companies/{id}/contents` | GET | 企业关联内容 | 否 |
| `/api/v2/companies/{id}/mentions` | GET | 企业舆情追踪 | 否 |
| `/api/v2/companies/{id}/followers` | GET | 企业关注者 | 否 |
| `/api/v2/trending/companies` | GET | 热门企业排行 | 否 |
| `/api/v2/stocks/{code}/announcements` | GET | 按股票代码查公告 | 否 |
| `/api/v2/announcements/search` | GET | 搜索公告 | 否 |
| `/api/v2/announcements/important` | GET | 重要公告 | 否 |
| `/api/v2/announcements/{id}` | GET | 公告详情 | 否 |
| `/api/v2/announcements/{id}/download` | GET | 下载公告PDF | 否 |

## 通用响应格式

```json
{
  "data": [...],
  "meta": {
    "current_page": 1,
    "per_page": 20,
    "total": 1000
  }
}
```

## 企业数据字段

```json
{
  "id": 1,
  "name": "贵州茅台酒股份有限公司",
  "short_name": "贵州茅台",
  "slug": "guizhou-maotai",
  "stock_code": "600519",
  "stock_market": "SH",
  "industry": "白酒",
  "description": "...",
  "logo": "https://img.shenlannews.com/...",
  "follower_count": 1234,
  "content_count": 567,
  "mention_count": 890
}
```
