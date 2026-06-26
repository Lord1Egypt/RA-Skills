---
name: feishu-image-send
description: Send inline images via Feishu Bot messages. Use when the `message` tool's `filePath`/`file_path` parameters fail to render images (shows JSON text instead). Works by generating a temporary Node.js script that calls the Feishu Open API directly (upload image → get image_key → send image message). Trigger: sending images to Feishu chat, image rendering fails, or user asks to send a picture via Feishu bot.
---

# Feishu Image Send

Send images that render inline in Feishu chat (not as file links).

## Problem

The `message` tool's `filePath`/`file_path` parameters often fail for Feishu:
- API returns `ok:true` but the recipient sees raw JSON text instead of rendered image
- Caused by path restrictions (`mediaLocalRoots`) and outbound handling bugs
- This skill bypasses the issue by calling the Feishu Open API directly

## Workflow

When asked to send an image to a Feishu chat:

1. Get the image path and target user/chat
2. Generate a temporary Node.js script with values filled in (see Template below)
3. Write it to `/tmp/feishu-send-{timestamp}.js` using `write`
4. Run: `node /tmp/feishu-send-{timestamp}.js`
5. Confirm `✅ Image sent` in output, then clean up: `rm /tmp/feishu-send-{timestamp}.js`

### Script Template

Copy this template and fill in the values:

```javascript
const https = require('https');
const fs = require('fs');

// === Config: update these values ===
const APP_ID = '<app_id>';             // e.g. cli_a931e5b57ff89cc0
const APP_SECRET = '<app_secret>';     // from openclaw.json
const IMAGE_PATH = '/absolute/path/to/image.jpg';  // must be absolute
const RECEIVE_ID = '<open_id_or_chat_id>';           // e.g. ou_71c53ff7589f8527a27c2a057b96b6d7
const RECEIVE_ID_TYPE = 'open_id';     // or 'chat_id', 'user_id'
// ===================================

function req(url, opts, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const r = https.request({
      hostname: u.hostname,
      path: u.pathname + u.search,
      method: opts.method || 'GET',
      headers: opts.headers || {}
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)) } catch (e) { resolve(d) } });
    });
    r.on('error', reject);
    if (body) r.write(typeof body === 'string' ? body : JSON.stringify(body));
    r.end();
  });
}

(async () => {
  // 1. Get tenant access token
  const t = await req('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }, { app_id: APP_ID, app_secret: APP_SECRET });
  if (t.code !== 0) { console.error('Token error:', t); process.exit(1); }
  const token = t.tenant_access_token;
  console.log('Token acquired');

  // 2. Upload image via multipart/form-data
  const boundary = '----Boundary' + Date.now().toString(36);
  const CRLF = '\r\n';
  const img = fs.readFileSync(IMAGE_PATH);
  const fn = IMAGE_PATH.split('/').pop();
  const body = Buffer.concat([
    Buffer.from(`--${boundary}${CRLF}`),
    Buffer.from(`Content-Disposition: form-data; name="image_type"${CRLF}${CRLF}message${CRLF}`),
    Buffer.from(`--${boundary}${CRLF}`),
    Buffer.from(`Content-Disposition: form-data; name="image"; filename="${fn}"${CRLF}`),
    Buffer.from(`Content-Type: image/jpeg${CRLF}${CRLF}`),
    img,
    Buffer.from(`${CRLF}--${boundary}--${CRLF}`),
  ]);
  const uploaded = await new Promise((resolve, reject) => {
    const r = https.request({
      hostname: 'open.feishu.cn',
      path: '/open-apis/im/v1/images',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length
      }
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)) } catch (e) { reject(e) } });
    });
    r.on('error', reject); r.write(body); r.end();
  });
  if (uploaded.code !== 0) { console.error('Upload error:', uploaded); process.exit(1); }
  const imageKey = uploaded.data.image_key;
  console.log('Image uploaded, key:', imageKey);

  // 3. Send image message
  // ⚠️ RECEIVE_ID_TYPE must be in URL query string, NOT in JSON body
  const content = JSON.stringify({ image_key: imageKey });
  const sent = await req(
    `https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${encodeURIComponent(RECEIVE_ID_TYPE)}`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json; charset=utf-8'
      }
    },
    { receive_id: RECEIVE_ID, msg_type: 'image', content }
  );
  if (sent.code !== 0) { console.error('Send error:', sent); process.exit(1); }
  console.log('✅ Image sent. message_id:', sent.data.message_id);
})();
```

## Critical Rules

| Rule | Detail |
|------|--------|
| `receive_id_type` | **Must** be a URL query parameter (`?receive_id_type=open_id`), not in the JSON body |
| `image_type` in upload | Use `"message"` for chat images, not `"avatar"` |
| `content` field in send | Must be a JSON **string** (double-escaped), not an object |
| `IMAGE_PATH` | Must be an absolute path to a readable image file |

## Getting Credentials

Read `openclaw.json` → `channels.feishu.accounts.<accountId>` for `appId` and `appSecret`.

For the CTO agent, these are already known:
- `accountId`: `cto`
- `appId`: `cli_a931e5b57ff89cc0`
- `appSecret`: `Q3c78ab1ORB7xOj0JtRz2d1GwQtzZcZH`

For the target user, use the current conversation's sender `open_id` from the inbound context.

## Supported Formats

JPEG, PNG, GIF, WEBP, TIFF, BMP, ICO — max 30MB.

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `99992402 field validation failed` for `receive_id_type` | Parameter placed in JSON body instead of URL | Move `receive_id_type=open_id` to the URL query string |
| `234011 Can't recognize image format` | Corrupted, missing, or unsupported file | Ensure valid JPEG/PNG and file exists at the given path |
| Image uploads but not displayed in chat | Used `image_type=avatar` instead of `message` | Change `image_type` to `"message"` for chat images |
| `message` tool returns `ok` but no image renders | `filePath` not in `mediaLocalRoots` or outbound bug | Use this skill's direct API method instead |

## Integration with Cron Jobs

In automated reports (daily/weekly), generate and run the script programmatically:

```javascript
const { writeFileSync, unlinkSync } = require('fs');
const { execSync } = require('child_process');
const path = '/tmp/feishu-send-' + Date.now() + '.js';

const script = `/* filled template */`;
writeFileSync(path, script);
execSync(`node ${path}`);
unlinkSync(path);
```

## API Reference

- **Upload Image**: `POST /open-apis/im/v1/images` (multipart/form-data)
- **Send Message**: `POST /open-apis/im/v1/messages?receive_id_type={type}` (JSON body)

Official docs:
- [Upload Image](https://open.feishu.cn/document/ukTMukTMukTM/ukTM5UjL5ETO14COxkTN/1images-1upload)
- [Send Message](https://open.feishu.cn/document/ukTMukTMukTM/ukTM5UjL5ETO14COxkTN/1messages-1create)
