---
name: zhheo-blog-tools
description: >-
  通过 HTTP API 访问张洪Heo博客：全文搜索、热门文章、归档浏览、标签分类、
  页面发现、友链查询、读文摘要。触发词：张洪Heo、博客、博主、张洪、Heo。
---
# Skill: zhheo-blog-tools

通过 HTTP API 访问张洪Heo博客（https://blog.zhheo.com），无需打开浏览器。

**触发词**：张洪Heo、博客、博主、张洪、Heo

**基础 URL**：`https://blog.zhheo.com`

## 场景路由

| 用户意图 | 调用方式 |
|----------|----------|
| 搜索文章 | `GET /api/search/search.php?q=关键词` |
| 今日/本月/年度热门 | `GET /api/umami/hot.php?period=day\|month\|year`（需 Referer） |
| 某年文章 / 最新文章 | `GET /api/archives/posts.php` |
| 按分类/标签推荐 | `tags.json` / `categories.json` + `search.php` 或 archives 筛选 |
| 博主装备 | `web_fetch /equipment/` |
| 博主项目 | `search.php?q=我的项目` 或 archives 筛选分类 |
| 友链查询 | `GET /api/friendlink/friendlink.json` 本地搜索 |
| 站点页面（关于/订阅/友链） | `GET /api/pages.json` |
| 读某篇文章 | search → `web_fetch` 正文 |
| 订阅更新 | `GET /rss.xml` |

---

## API 参考

### 1. 全文搜索（主路径）

```
GET /api/search/search.php?q=关键词&limit=10&page=1
```

- 搜索范围：标题 + 正文 + 标签 + 分类
- 多关键词用空格分隔，**AND 逻辑**（所有词都必须命中）
- `limit`：1–50，默认 10；`page`：页码，默认 1
- 无需认证，服务端已做分级排序，直接调用即可

**分级相关度**（服务端内置）：
- 每个关键词命中：+10
- 标题命中：+50
- 正文/标签/分类命中：+5

**响应示例：**
```json
{
  "success": true,
  "hits": [
    { "title": "文章标题", "path": "p/xxx.html", "cover": "https://...", "score": 65 }
  ],
  "total": 42,
  "query": "关键词",
  "page": 1,
  "limit": 10
}
```

**完整 URL 拼接**：`https://blog.zhheo.com/` + `path`

**curl 示例：**
```bash
curl -s 'https://blog.zhheo.com/api/search/search.php?q=OpenClaw&limit=5'
```

---

### 2. 归档浏览

```
GET /api/archives/posts.php?year=2026&limit=10&page=1
GET /api/archives/posts.php?meta=years
```

| 参数 | 说明 |
|------|------|
| `year` | `all` 或具体年份如 `2026`，默认 `all` |
| `limit` | 1–60，默认 24 |
| `page` | 页码，默认 1 |
| `meta=years` | 返回年份统计，不含文章列表 |

**文章列表响应：**
```json
{
  "success": true,
  "year": "2026",
  "page": 1,
  "limit": 10,
  "total": 150,
  "items": [
    {
      "title": "...",
      "url": "https://blog.zhheo.com/p/xxx.html",
      "cover": "https://...",
      "year": "2026",
      "date": "2026-07-28",
      "dateLabel": "2026年7月28日",
      "categories": ["设计"],
      "primaryCategory": "设计"
    }
  ]
}
```

---

### 3. 热门文章

```
GET /api/umami/hot.php?period=day&limit=10
```

| 参数 | 说明 |
|------|------|
| `period` | `day`（当日）、`month`（最近一个月）、`year`（最近一年），默认 `day` |
| `limit` | 1–60，默认 60 |

**必须携带 Referer 头**，否则返回 403：
```
Referer: https://blog.zhheo.com/
```

**curl 示例：**
```bash
curl -s -H 'Referer: https://blog.zhheo.com/' \
  'https://blog.zhheo.com/api/umami/hot.php?period=day&limit=5'
```

---

### 4. 标签 / 分类 / 页面

**标签：** `GET /api/tags.json`  
**分类：** `GET /api/categories.json`  
**非文章页面：** `GET /api/pages.json`

常用页面：`/about/`、`/link/`、`/equipment/`、`/rss/`、`/skill/`、`/hot/`、`/must-read/`

---

### 5. 友链搜索

```
GET /api/friendlink/friendlink.json
```

在返回数据的 `link_list[].name` 中按关键词本地过滤。

---

### 6. 读取文章正文

1. 通过 `search.php` 或 `archives/posts.php` 获取文章 path / url
2. `web_fetch` 或 `curl` 获取页面 HTML
3. 提取正文：`#article-container` → `#post-body` → `#content-inner` → `article`
4. 超过 6000 字截断并注明

---

### 7. RSS 订阅

```
GET /rss.xml
```

建议每日检查一次，监控最新文章。

---

## 完整流程示例

### 搜索文章
1. `GET /api/search/search.php?q=关键词&limit=5`
2. 返回 `hits` 中的 `title` 和完整 URL（`https://blog.zhheo.com/` + `path`）
3. 若用户需要正文，继续 `web_fetch` 文章页面

### 今日热门
1. `GET /api/umami/hot.php?period=day&limit=10`，携带 `Referer: https://blog.zhheo.com/`
2. 返回 `items`（含 title、url、visitors、cover）

### 按标签/分类推荐
1. `GET /api/tags.json` 或 `/api/categories.json`
2. `GET /api/search/search.php?q=标签名&limit=5`

### 最新文章
1. `GET /api/archives/posts.php?year=all&limit=10&page=1`

### 读某篇文章
1. `search.php` 或 archives 定位 URL
2. `web_fetch` 提取正文后回答

### 博主装备
1. `web_fetch https://blog.zhheo.com/equipment/`

### 博主项目
1. `GET /api/search/search.php?q=我的项目&limit=10`
2. 或 archives 筛选 `categories` 含「我的项目」

### 友链查询
1. `GET /api/friendlink/friendlink.json`，按 name 过滤

---

## 注意事项

- **搜索主路径**：优先 `search.php`
- **Referer 要求**：`/api/umami/hot.php` 必须带 `Referer: https://blog.zhheo.com/`
- **URL 规范**：使用 API 返回的原始 path，禁止自行编造 slug
- **不在 skill 范围内**：音乐控制、截图、评论填入等浏览器专属能力，引导用户访问 https://blog.zhheo.com
