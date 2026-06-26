# 深蓝财经新闻 API 参考文档

## 端点总览

| 端点 | 方法 | 说明 | 认证 |
|------|------|------|------|
| `/api/v2/dispatches` | GET | 实时快讯列表 | 否 |
| `/api/v2/dispatches/stream` | GET | SSE 实时快讯流 | 否 |
| `/api/v2/dispatches/{id}` | GET | 快讯详情 | 否 |
| `/api/v2/articles` | GET | 文章列表 | 否 |
| `/api/v2/articles/{id}` | GET | 文章详情 | 否 |
| `/api/v2/trending/articles` | GET | 热门文章 | 否 |
| `/api/v2/announcements` | GET | 公告列表 | 否 |
| `/api/v2/announcements/latest` | GET | 最新公告 | 否 |
| `/api/v2/announcements/important` | GET | 重要公告 | 否 |
| `/api/v2/announcements/search` | GET | 搜索公告 | 否 |
| `/api/v2/announcements/{id}` | GET | 公告详情 | 否 |
| `/api/v2/announcements/{id}/download` | GET | 下载公告PDF | 否 |
| `/api/v2/stocks/{code}/announcements` | GET | 按股票代码查公告 | 否 |
| `/api/v2/rss/articles` | GET | RSS 聚合文章 | 否 |
| `/api/v2/rss/sources` | GET | RSS 来源列表 | 否 |
| `/api/v2/categories` | GET | 内容分类 | 否 |
| `/api/v2/tags/popular` | GET | 热门标签 | 否 |
| `/api/v2/tags/search` | GET | 搜索标签 | 否 |

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

## 错误码

| HTTP 状态码 | 说明 |
|------------|------|
| 200 | 成功 |
| 404 | 资源不存在 |
| 422 | 参数验证失败 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

## 频率限制

- 公开接口：60 次/分钟
- 搜索接口：30 次/分钟
