# 微信公众号 API 参考

## 认证

所有接口都需要 `access_token`，有效期 **7200秒（约2小时）**，脚本自动缓存并刷新。

```
GET https://api.weixin.qq.com/cgi-bin/token
  ?grant_type=client_credential
  &appid={appid}
  &secret={appsecret}
```

返回：
```json
{
  "access_token": "xxx",
  "expires_in": 7200
}
```

---

## 上传封面图（永久素材）

```
POST https://api.weixin.qq.com/cgi-bin/material/add_material
  ?access_token={token}&type=image
Content-Type: multipart/form-data
```

参数：`media` = 图片文件（建议 900x383，JPEG/PNG，< 2MB）

返回：
```json
{
  "media_id": "xxx",
  "url": "https://mmbiz.qpic.cn/..."
}
```

> ⚠️ 需微信认证后才有永久素材权限。临时素材（有效期3天）无需认证，但草稿接口不支持临时 thumb_media_id。

---

## 创建草稿

```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}
Content-Type: application/json; charset=utf-8
```

请求体：
```json
{
  "articles": [
    {
      "title": "文章标题（不超过32个字）",
      "author": "作者名（不超过16个字）",
      "digest": "摘要（不超过128个字）",
      "content": "<!DOCTYPE html><html>...</html>",
      "thumb_media_id": "封面图 media_id",
      "content_source_url": "",
      "need_open_comment": 0,
      "only_fans_can_comment": 0
    }
  ]
}
```

返回：
```json
{ "media_id": "草稿media_id", "errcode": 0 }
```

常见错误：
- `45004` — digest 超过 128 个字（size out of limit）
- `40007` — 无效的 `thumb_media_id`（必须先上传封面图）
- `41006` — 缺少 `thumb_media_id`
- `40001` — access_token 无效或已过期

---

## 查询草稿

```
POST https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}
Content-Type: application/json
```

```json
{ "offset": 0, "count": 10, "no_content": 1 }
```

`no_content=1`：不返回正文内容（节省流量）

---

## 删除草稿

```
POST https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}
Content-Type: application/json
```

```json
{ "media_id": "草稿media_id" }
```

---

## 权限要求

| 接口 | 权限 |
|------|------|
| 获取 access_token | 无特殊要求 |
| 上传永久素材 | 需微信认证 |
| 创建草稿 | 需微信认证 |
| 查询/删除草稿 | 需微信认证 |

---

## 正文图片处理

草稿接口的 `content` 字段中的图片处理：

1. 上传图片到微信素材库：`POST /cgi-bin/media/upload?type=image`
2. 获取返回的 `url`
3. 在 HTML 中使用：`<img src="https://mmbiz.qpic.cn/..." />`

微信编辑器会自动处理图片 CDN 加速。
