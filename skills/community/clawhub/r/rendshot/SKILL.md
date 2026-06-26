---
name: rendshot
description: "Image generation and screenshot tool using Rendshot. Use when the user asks to generate images from HTML/CSS, take website screenshots, render templates to images, create social media graphics, OG images, or any visual content programmatically. Also triggers on: 'render HTML', 'html to image', 'screenshot this page', 'create a card image', 'generate thumbnail'."
---

# Rendshot — Image Generation & Screenshot

Rendshot renders HTML/CSS to images, takes URL screenshots, and supports AI-powered template generation with platform presets.

## Tool Selection

**MCP tools available?** Use them directly (preferred path):

| Tool | Use when |
|------|----------|
| `generate_image` | Render HTML, fill a template, or AI-generate from prompt |
| `screenshot_url` | Capture a webpage |
| `list_templates` | Browse community templates by platform/category |
| `get_template` | Get variable schema before filling a template |
| `create_template` | Save a design for reuse |

**No MCP tools?** Fall back to CLI or API. See [references/api-endpoints.md](references/api-endpoints.md).

## Core Workflows

### 1. AI Prompt to Image (fastest)

```
generate_image({
  prompt: "Coffee shop promotion card, warm brown tones, large title",
  platform: "xiaohongshu",    // auto-sets 1080x1440 + style guide
  locale: "zh"                // response language
})
```

Combine with `template_id` to reference an existing template's visual style:
```
generate_image({
  prompt: "Same layout but for a bakery",
  template_id: "tpl_abc123",  // style reference
  platform: "instagram_post"
})
```

### 2. Template to Image (deterministic)

```
// Step 1: Find a template
list_templates({ platform: "xiaohongshu", q: "product showcase" })

// Step 2: Check its variables
get_template({ template_id: "tpl_abc123" })
// Returns: title(text), subtitle(text), bg_image(image), accent_color(color)

// Step 3: Render with custom values
generate_image({
  template_id: "tpl_abc123",
  variables: {
    title: "Today's Special",
    subtitle: "Hand-roasted beans",
    bg_image: "https://example.com/beans.jpg",
    accent_color: "#8B4513"
  }
})
```

### 3. Raw HTML to Image

```
generate_image({
  html: "<div style='...'>Hello World</div>",
  width: 1080,
  height: 1080,
  format: "png",
  deviceScale: 2        // 2x for retina
})
```

### 4. Screenshot

```
screenshot_url({
  url: "https://example.com",
  width: 1280,
  height: 800,
  fullPage: true,
  format: "png"
})
```

### 5. Save and Reuse

After AI generates a design, save it as a template:
```
create_template({
  name: "Coffee Promo Card",
  html: "<returned html from AI>",
  variables: [
    { key: "title", type: "text", label: "Title", default: "Special Offer" },
    { key: "bg_image", type: "image", label: "Background", default: "https://..." }
  ],
  platform: "xiaohongshu",
  tags: ["coffee", "promotion"],
  visibility: "private"
})
```

## Platform Presets

| Platform | Default size | Typical use |
|----------|-------------|-------------|
| `xiaohongshu` | 1080x1440 | Notes, product cards |
| `xiaohongshu_wide` | 1080x810 | Wide format notes |
| `instagram_post` | 1080x1080 | Feed posts |
| `instagram_story` | 1080x1920 | Stories, reels covers |
| `twitter_card` | 1200x628 | Link preview cards |
| `twitter_post` | 1200x675 | Image posts |
| `linkedin_post` | 1200x627 | Professional posts |
| `youtube_thumb` | 1280x720 | Video thumbnails |
| `wechat_cover` | 900x383 | Article covers |
| `wechat_thumb` | 200x200 | Article thumbnails |
| `og_image` | 1200x630 | Open Graph images |
| `custom` | 1080x1080 | Any custom size |

## Variable Types

| Type | Example | Constraints |
|------|---------|------------|
| `text` | Title, subtitle | `maxLength` |
| `image` | Background, avatar | URL format |
| `color` | Accent, background | Hex format |
| `number` | Font size, opacity | `min`, `max` |
| `select` | Style variant | `options: ["A","B"]` |

## Key Rules

- `html`, `template_id`, and `prompt` are mutually exclusive (except `prompt` + `template_id` for style reference)
- Always call `get_template` before using a template to check its variable schema
- Use `deviceScale: 2` for retina/high-DPI output
- Default format is `png`; use `jpg` + `quality: 85` for smaller file size
- AI prompt mode returns HTML + variables; save good results with `create_template`
- For detailed tool parameters, see [references/mcp-tools.md](references/mcp-tools.md)
- For API/CLI/SDK usage, see [references/api-endpoints.md](references/api-endpoints.md)
