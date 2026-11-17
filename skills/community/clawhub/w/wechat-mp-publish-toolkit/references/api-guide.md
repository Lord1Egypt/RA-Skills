# WeChat MP API Guide

## API Endpoints

### 1. Get access_token
```
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=SECRET
```
- Returns: `{"access_token": "...", "expires_in": 7200}`
- Token expires in 2 hours. Get a fresh one for each session.

### 2. Upload Permanent Material (cover image)
```
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=TOKEN&type=image
```
- Body: multipart form, field `media=@/path/to/image.png`
- Returns: `{"media_id": "...", "url": "https://mmbiz.qpic.cn/..."}`
- The `media_id` is permanent (does not expire)
- The `url` can be used inside article HTML `<img>` tags

### 3. Create Draft
```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=TOKEN
```
Body:
```json
{
  "articles": [{
    "title": "Article Title",
    "author": "",
    "digest": "Summary text, max 120 chars",
    "content": "<html>...inline-styled HTML...</html>",
    "thumb_media_id": "MEDIA_ID_FROM_STEP_2",
    "need_open_comment": 1,
    "only_fans_can_comment": 0
  }]
}
```
- Returns: `{"media_id": "DRAFT_ID"}`

### 4. Publish Draft
```
POST https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=TOKEN
```
Body: `{"media_id": "DRAFT_ID"}`
- Returns: `{"errcode": 0, "errmsg": "ok", "publish_id": "..."}`
- **Irreversible** — article goes to all subscribers immediately

### 5. List Drafts
```
POST https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=TOKEN
```
Body: `{"offset": 0, "count": 20, "no_content": 1}`
- `no_content: 1` skips the HTML body (faster, just metadata)

### 6. Delete Draft
```
POST https://api.weixin.qq.com/cgi-bin/draft/delete?access_token=TOKEN
```
Body: `{"media_id": "DRAFT_ID"}`

---

## Error Codes

| errcode | Meaning | Solution |
|---------|---------|----------|
| 0 | Success | — |
| -1 | System error (transient) | Retry 2-3 times with fresh token; if persistent, publish manually |
| 40001 | Invalid credential | Check AppID/Secret; token may have expired |
| 40007 | Invalid media_id | Draft was already published, deleted, or media_id is wrong |
| 40164 | IP not whitelisted | Get server IP via `curl -s https://api.ipify.org`, add to MP backend |
| 45004 | Digest exceeds 120 chars | Shorten the summary |
| 45110 | Author exceeds 8 bytes | Leave author empty via API; set manually in editor |
| 48001 | API capability not enabled | Requires verified enterprise account; activates ~24h after verification |

---

## Critical Encoding Gotcha

### Problem
Python's `requests` library `json=` parameter and `json.dumps()` with default settings convert Chinese characters to `\uXXXX` escape sequences. WeChat's API does NOT correctly parse these — the draft content will appear as garbled text or literal `\uXXXX` strings in the editor.

### Solution
**Do NOT use:**
```python
# WRONG — garbles Chinese
requests.post(url, json=draft_data)
```

**DO use:**
```python
import json, subprocess

# 1. Write JSON with ensure_ascii=False
json_path = "/tmp/draft.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(draft_data, f, ensure_ascii=False, separators=(",", ":"))

# 2. Upload with curl --data-binary (preserves UTF-8 bytes)
subprocess.run([
    "curl", "-s", "-X", "POST", url,
    "-H", "Content-Type: application/json",
    "--data-binary", f"@{json_path}"
])
```

The `ensure_ascii=False` keeps Chinese characters as raw UTF-8 bytes, and `curl --data-binary` sends them without re-encoding.

---

## Field Limits

| Field | Limit | Notes |
|-------|-------|-------|
| title | 64 bytes | ~21 Chinese characters (3 bytes each) |
| digest | 120 characters | Counted in characters, not bytes |
| author | 8 bytes | ~2 Chinese characters; usually leave empty and set in editor |
| content | No hard limit | Practical: keep under 20000 chars for reliability |

---

## Article HTML Requirements

- Must use **inline styles** (`style="..."` on each tag)
- WeChat editor strips `<style>` blocks and CSS classes
- Images must use `mmbiz.qpic.cn` domain (upload to material library first, use the returned URL)
- External image URLs (`<img src="https://example.com/...">`) will NOT render
- No JavaScript
- No `<form>`, `<input>`, or interactive elements
