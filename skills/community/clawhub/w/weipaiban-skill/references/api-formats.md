# API 端点与响应格式参考

所有 API 请求都需要在 Header 中携带认证信息：

```
Authorization: Bearer $WEIPAIBAN_API_KEY
```

API 基础地址：`${WEIPAIBAN_API_BASE:-https://weipaiban.cn}`

---

## 模板搜索响应

`GET /api/v1/templates`

```json
{
  "data": {
    "items": [
      {
        "id": "模板ID",
        "title": "模板标题",
        "description": "模板描述",
        "tags": ["标签1", "标签2"],
        "thumbnail": "缩略图URL",
        "publishedAt": "2026-01-01T00:00:00.000Z"
      }
    ],
    "total": 10,
    "page": 1,
    "perPage": 5
  }
}
```

## 默认模板响应

`GET /api/v1/templates/default`

```json
{
  "data": {
    "id": "模板ID",
    "title": "模板标题",
    "description": "模板描述",
    "tags": ["标签1", "标签2"],
    "thumbnail": "缩略图URL",
    "publishedAt": "2026-01-01T00:00:00.000Z"
  }
}
```

## 克隆模板响应

`POST /api/v1/templates/{模板ID}/clone`

请求体：`{"title": "作品标题"}`

```json
{
  "data": {
    "id": "新作品ID",
    "title": "作品标题",
    "createdAt": "2026-01-01T00:00:00.000Z",
    "updatedAt": "2026-01-01T00:00:00.000Z"
  }
}
```

## Parser 获取响应

`GET /api/v1/vectors/{作品ID}/parser`

```json
{
  "data": {
    "id": "作品ID",
    "title": "作品标题",
    "elements": [
      {
        "id": "元素ID",
        "name": "标题文本",
        "type": "text",
        "text": "原始文本内容",
        "charCount": 7,
        "fill": "#333333"
      },
      {
        "id": "元素ID",
        "name": "背景色块",
        "type": "rect",
        "fill": "#d9d9d9",
        "width": 750,
        "height": 1200
      },
      {
        "id": "元素ID",
        "name": "背景图",
        "type": "image",
        "image": {
          "src": "https://原始图片地址",
          "width": 800,
          "height": 600,
          "ratio": "4:3"
        }
      },
      {
        "id": "元素ID",
        "name": "轮播图",
        "type": "slideshow",
        "assets": [
          {
            "id": "asset1",
            "title": "高山.jpg",
            "src": "https://图片地址1",
            "width": 1170,
            "height": 1800,
            "ratio": "13:20"
          },
          {
            "id": "asset2",
            "title": "草地.jpg",
            "src": "https://图片地址2",
            "width": 1170,
            "height": 1800,
            "ratio": "13:20"
          }
        ]
      }
    ]
  }
}
```

## Parser 更新响应

`POST /api/v1/vectors/{作品ID}/parser`

```json
{
  "data": {
    "id": "作品ID",
    "title": "作品标题",
    "updatedAt": "2026-01-01T00:00:00.000Z"
  }
}
```

## CDN 上传响应

`POST /api/v1/assets/fetch`

请求体：`{"url": "图片URL"}`

该接口基于文件内容 SHA1 哈希自动去重：相同图片重复上传返回 HTTP 200（已有记录），新图片上传返回 HTTP 201。

成功响应：

```json
{
  "data": {
    "id": "资源ID",
    "type": "image",
    "name": "存储路径",
    "title": "文件名",
    "src": "https://svg-cdn.creatby.com/...",
    "width": 800,
    "height": 600,
    "size": 123456,
    "createdAt": "2026-01-01T00:00:00.000Z"
  }
}
```

错误响应（400/413/415/502/504）：

```json
{
  "error": {
    "message": "错误描述",
    "code": 400
  }
}
```

## CDN 文件上传

`POST /api/v1/assets/upload`

请求格式：`multipart/form-data`，字段 `file` 为图片文件。

```bash
curl -s --max-time 30 -X POST \
  -H "Authorization: Bearer $WEIPAIBAN_API_KEY" \
  -F "file=@本地文件路径" \
  "${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/assets/upload"
```

响应格式与 `/api/v1/assets/fetch` 相同（同样支持 SHA1 去重）。
