# Rendshot API & CLI Reference

Use this when MCP tools are not available.

## REST API

Base URL: `https://api.rendshot.com` (or self-hosted)

Authentication: `Authorization: Bearer rs_live_xxx`

### POST /v1/image — Render image

```bash
curl -X POST https://api.rendshot.com/v1/image \
  -H "Authorization: Bearer $RENDSHOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<div style=\"...\">Hello</div>",
    "width": 1080,
    "height": 1080,
    "format": "png"
  }'
```

Supports same params as MCP `generate_image`: `html`, `template_id`, `variables`, `prompt`, `platform`, etc.

### POST /v1/screenshot — Screenshot URL

```bash
curl -X POST https://api.rendshot.com/v1/screenshot \
  -H "Authorization: Bearer $RENDSHOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "url": "https://example.com", "fullPage": true }'
```

### POST /v1/ai-render — AI generate (streaming)

```bash
curl -X POST https://api.rendshot.com/v1/ai-render \
  -H "Authorization: Bearer $RENDSHOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "prompt": "Coffee shop card", "platform": "xiaohongshu" }'
```

Returns streaming response with tool calls for template updates.

### GET /v1/templates — List templates

```bash
curl "https://api.rendshot.com/v1/templates?platform=xiaohongshu&limit=10" \
  -H "Authorization: Bearer $RENDSHOT_API_KEY"
```

### GET /v1/templates/:id — Get template

### POST /v1/templates — Create template

### GET /v1/usage — Check quota

---

## CLI

Install: `npm install -g rendshot`

Auth: `rendshot auth` (interactive) or `RENDSHOT_API_KEY` env var.

```bash
# AI prompt → image
rendshot generate -p "Coffee shop card" --platform xiaohongshu --save cover.png

# Template → image
rendshot generate --template tpl_abc123 --var title="Hello" --var bg_image="https://..." --save out.png

# HTML → image
rendshot generate --html "<div>Hello</div>" -w 1080 -h 1080 --save out.png

# Screenshot
rendshot screenshot --url https://example.com --full-page --save screenshot.png

# Browse templates
rendshot template list --platform xiaohongshu
rendshot template info tpl_abc123

# Check usage
rendshot usage
```

---

## SDK (Node.js)

Install: `npm install @rendshot/sdk`

```typescript
import { RendshotClient } from '@rendshot/sdk'

const client = new RendshotClient({ apiKey: process.env.RENDSHOT_API_KEY })

// AI generate
const result = await client.aiRender({
  prompt: "Coffee shop card",
  platform: "xiaohongshu"
})
console.log(result.url, result.html)

// Template render
const img = await client.renderImage({
  templateId: "tpl_abc123",
  variables: { title: "Hello" }
})

// Screenshot
const shot = await client.screenshotUrl({ url: "https://example.com" })
```

---

## Python SDK

Install: `pip install rendshot`

```python
from rendshot import RendshotClient

client = RendshotClient(api_key="rs_live_xxx")

# AI generate
result = client.ai_render(prompt="Coffee shop card", platform="xiaohongshu")

# Template render
img = client.render_image(template_id="tpl_abc123", variables={"title": "Hello"})

# Screenshot
shot = client.screenshot_url(url="https://example.com")
```
