# WeChat Official Account API Reference

## Authentication

**Endpoint:** `POST https://api.weixin.qq.com/cgi-bin/stable_token`

```json
{
  "grant_type": "client_credential",
  "appid": "YOUR_APPID",
  "secret": "YOUR_APPSECRET",
  "force_refresh": false
}
```

Response: `{ "access_token": "...", "expires_in": 7200 }`

Token expires in 7200s. Use `get_token.py` which auto-caches and refreshes.

---

## Image Upload (Article Body Images)

**Endpoint:** `POST https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=TOKEN`

- Method: multipart/form-data
- Field name: `media`
- Supported: jpg, png, gif, webp
- Max size: 10MB
- Response: `{ "url": "http://mmbiz.qpic.cn/..." }`

The returned `url` is a permanent WeChat CDN URL — use directly in article HTML.

---

## Cover Image Upload (thumb_media_id)

**Endpoint:** `POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=TOKEN&type=thumb`

- Method: multipart/form-data, field name: `media`
- Supported: jpg, png
- Max size: 1MB (64×64 to 900×500 pixels recommended)
- Response: `{ "media_id": "...", "url": "..." }`

The `media_id` is used as `thumb_media_id` in the draft upload.

---

## Upload Draft

**Endpoint:** `POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=TOKEN`

```json
{
  "articles": [{
    "title": "文章标题",
    "author": "作者",
    "digest": "摘要（不超过120字）",
    "content": "<p>HTML正文...</p>",
    "thumb_media_id": "COVER_MEDIA_ID",
    "need_open_comment": 0,
    "only_fans_can_comment": 0
  }]
}
```

Response: `{ "media_id": "DRAFT_MEDIA_ID" }`

Multiple articles can be included in one draft (multi-page article).

---

## Publish Draft (Optional)

**Endpoint:** `POST https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=TOKEN`

```json
{ "media_id": "DRAFT_MEDIA_ID" }
```

Response: `{ "publish_id": "...", "msg_data_id": "..." }`

Use `GET /cgi-bin/freepublish/get?access_token=TOKEN&publish_id=ID` to check publish status.

---

## Error Codes

| errcode | Meaning |
|---------|---------|
| 40001 | Invalid access_token (expired or wrong) |
| 40013 | Invalid AppID |
| 45009 | API call frequency limit |
| 48001 | API permission denied (check account type) |
| 40007 | Invalid media_id |

---

## WeChat HTML Constraints

- **No `<style>` blocks** — all CSS must be inline
- **No `<script>` tags**
- **Images must use WeChat CDN URLs** — external URLs may be blocked
- **Supported tags:** `p`, `h1-h4`, `strong`, `em`, `ul`, `ol`, `li`, `blockquote`, `img`, `br`, `a`, `hr`, `span`, `section`
- **Recommended article width:** ≤ 677px
- **Font size:** min 14px for readability on mobile

---

## Config File Format (`config.json`)

```json
{
  "appid": "wx1234567890abcdef",
  "appsecret": "your_appsecret_here"
}
```

Or set environment variables: `WX_APPID`, `WX_APPSECRET`
