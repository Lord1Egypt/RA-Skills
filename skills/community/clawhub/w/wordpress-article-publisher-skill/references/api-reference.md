# WordPress REST API 参考

## 基础信息

### API 端点

```
https://你的域名/wp-json/wp/v2/
```

### 认证方式

使用 HTTP Basic Authentication（应用程序密码）：

```
Authorization: Basic base64(用户名:应用程序密码)
```

### 请求头

```http
Content-Type: application/json; charset=utf-8
Authorization: Basic [Base64编码的认证信息]
```

## 文章操作

### 发布文章 (Create Post)

**请求：**
```http
POST /wp-json/wp/v2/posts
```

**请求体：**
```json
{
    "title": "文章标题",
    "content": "<p>文章内容（HTML格式）</p>",
    "status": "publish",
    "slug": "自定义-url-别名",
    "categories": [1, 2],
    "tags": [3, 4],
    "featured_media": 0,
    "date": "2024-01-01T12:00:00"
}
```

**参数说明：**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| title | string | 是 | 文章标题 |
| content | string | 是 | 文章内容（HTML格式） |
| status | string | 否 | publish/draft/pending/private（默认：draft） |
| slug | string | 否 | URL 别名 |
| categories | array | 否 | 分类 ID 数组 |
| tags | array | 否 | 标签 ID 数组 |
| featured_media | int | 否 | 特色图片媒体 ID |
| date | string | 否 | 发布日期（ISO 8601 格式） |

**成功响应 (201 Created)：**
```json
{
    "id": 3159,
    "date": "2026-05-22T17:57:00",
    "slug": "ai-文章的利弊",
    "status": "publish",
    "title": {
        "rendered": "AI文章的利弊"
    },
    "link": "https://example.com/ai-文章的利弊/",
    "author": 1
}
```

**错误响应：**
```json
{
    "code": "rest_invalid_param",
    "message": "Invalid parameter(s): title",
    "data": {
        "status": 400,
        "params": {
            "title": "文章标题不能为空"
        }
    }
}
```

### 获取文章列表 (Get Posts)

**请求：**
```http
GET /wp-json/wp/v2/posts
```

**查询参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码（默认：1） |
| per_page | int | 每页数量（默认：10，最大：100） |
| search | string | 搜索关键词 |
| status | string | post_status/pending/draft/private（默认：publish） |
| categories | int | 按分类 ID 筛选 |
| tags | int | 按标签 ID 筛选 |
| orderby | string | 排序字段：date/author/title/modified/slug/parent/relevance |
| order | string | asc/desc（默认：desc） |

**示例：**
```
GET /wp-json/wp/v2/posts?per_page=5&status=publish&orderby=date&order=desc
```

### 获取单篇文章 (Get Post)

**请求：**
```http
GET /wp-json/wp/v2/posts/{id}
```

**示例：**
```
GET /wp-json/wp/v2/posts/3159
```

### 更新文章 (Update Post)

**请求：**
```http
POST /wp-json/wp/v2/posts/{id}
```

**请求体：** 与创建文章相同

### 删除文章 (Delete Post)

**请求：**
```http
DELETE /wp-json/wp/v2/posts/{id}
```

**可选参数：**
- `force=true`：永久删除（默认移到回收站）

```http
DELETE /wp-json/wp/v2/posts/3159?force=true
```

## 分类操作

### 获取分类列表

**请求：**
```http
GET /wp-json/wp/v2/categories
```

**参数：**
- `per_page`：每页数量
- `search`：搜索名称

### 获取单分类

**请求：**
```http
GET /wp-json/wp/v2/categories/{id}
```

### 创建分类

**请求：**
```http
POST /wp-json/wp/v2/categories
```

**请求体：**
```json
{
    "name": "分类名称",
    "description": "分类描述",
    "slug": "分类别名"
}
```

## 标签操作

### 获取标签列表

**请求：**
```http
GET /wp-json/wp/v2/tags
```

### 创建标签

**请求：**
```http
POST /wp-json/wp/v2/tags
```

**请求体：**
```json
{
    "name": "标签名称"
}
```

## 用户操作

### 获取当前用户信息

**请求：**
```http
GET /wp-json/wp/v2/users/me
```

需要认证，返回当前认证用户的信息。

## 媒体操作

### 上传媒体

**请求：**
```http
POST /wp-json/wp/v2/media
```

**请求头：**
```
Content-Type: image/jpeg (或其他 MIME 类型)
```

**请求体：**
```
二进制文件数据
```

**返回：**
```json
{
    "id": 123,
    "source_url": "https://example.com/wp-content/uploads/2024/01/image.jpg"
}
```

## 错误代码

| 代码 | HTTP状态 | 说明 |
|------|----------|------|
| rest_bad_request | 400 | 请求格式错误 |
| rest_invalid_param | 400 | 参数无效 |
| rest_cannot_create | 401/403 | 无权创建 |
| rest_cannot_edit | 401/403 | 无权编辑 |
| rest_cannot_delete | 401/403 | 无权删除 |
| rest_invalid_json | 400 | JSON 解析错误 |
| rest_post_invalid_id | 404 | 文章不存在 |
| rest_no_route | 404 | 路由不存在 |

## 使用示例

### curl 发布文章

```bash
curl -X POST "https://example.com/wp-json/wp/v2/posts" \
  -H "Authorization: Basic $(echo -n 'user:app_password' | base64)" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "title": "文章标题",
    "content": "<p>文章内容</p>",
    "status": "publish"
  }'
```

### PowerShell 发布文章

```powershell
$body = @{
    title = "文章标题"
    content = "<p>文章内容</p>"
    status = "publish"
} | ConvertTo-Json -Compress

$headers = @{
    Authorization = "Basic $EncodedCredentials"
}

Invoke-RestMethod -Uri $apiUrl -Method Post -Body $body -Headers $headers -ContentType "application/json"
```

## 速率限制

WordPress REST API 没有固定的速率限制，但：
- 大量请求可能导致服务器响应变慢
- 某些托管服务商可能有自己的限制
- 建议添加适当延迟避免触发限制
