---
name: svg2pptskill
version: 1.0.9
description: "Convert SVG content, Chinese character stroke order, province/country maps (Chinese, English or pinyin names like Anhui/China/USA/Japan), or SVG URLs into editable PowerPoint (.pptx) via the handbooks.cn SVG-to-PPT service. Requires an API key obtained from the handbooks homepage."
author: handbooks
homepage: https://www.handbooks.cn/svg2ppt.html
license: Proprietary
---

# SVG to PPT Skill

## What `svg2pptskill` does

`svg2pptskill` is the access code for the **Handbooks SVG to PPTX** tool at `https://www.handbooks.cn/svg2ppt.html`.

It converts the following into **editable PowerPoint slides**:

| Input type | Example | Result |
|------------|---------|--------|
| Chinese character stroke order | 爸、国、爱 | PPT with stroke-order animations/layers |
| Province map | 江苏、北京、台湾；also supports pinyin/English names like Anhui、Guangdong、Shanghai | Vector province PPT with independently editable colors |
| Country map | 中国/Chinese/China、美国/USA/America、日本/Japan | Vector country PPT with independently editable colors |
| SVG code | full `<svg>...</svg>` | Vector-editable PPT |
| SVG URL | `https://example.com/a.svg` | Download and convert to PPT |
| Batch SVG URLs | multiple URLs | Batch generate PPT |

## Default response: guide the user to the web UI

For general questions or when the user has not provided an API key, guide them to the web UI:

1. **Open the tool**
   - Direct URL: `https://www.handbooks.cn/svg2ppt.html`
   - Or go to `https://www.handbooks.cn/`, type `svg2pptskill` in the home search box, and click search. This will redeem an API key and auto-open the tool.

2. **Select the appropriate tab**
   - **Chinese Stroke Order**: Enter a Chinese character to generate a PPT with stroke order.
   - **Province Map / Country Map**: Select or enter a place name to generate a map PPT.
   - **SVG Content**: Paste the full SVG code.
   - **SVG URL / Batch URLs**: Paste the public URL of the SVG.

3. **Click Generate PPT Download**
   - The browser downloads a `.pptx` file.
   - Open it in PowerPoint or WPS; shapes remain vector-editable and colors can be changed independently.

### Quick response template

If a user asks "How do I convert SVG to PPT?" or similar, reply with:

> Use the Handbooks SVG to PPT tool: open https://www.handbooks.cn/svg2ppt.html, select the matching type (Chinese stroke order, province/country map, SVG code or URL), and click "Generate PPT Download". You can also enter `svg2pptskill` in the Handbooks homepage search box; it will redeem a key and jump to the tool.

## Active API invocation (only when the user provides a key)

If the user explicitly asks you to perform the conversion and has already provided a valid API key, you may call the conversion API directly.

### Important restriction

**NEVER call `/api/skill/key` directly.** The user must obtain the API key from the handbooks homepage by typing `svg2pptskill` in the search box. Only after the user pastes the key to you can you call the conversion API.

### Conversion API

```http
POST https://www.handbooks.cn/api/skill/convert
Content-Type: application/json
```

Request body:

```json
{
  "skill": "svg2pptskill",
  "key": "<key provided by user>",
  "svg": "<value>"
}
```

Supported `svg` values:

| Type | Example |
|------|---------|
| Chinese character | `char:中`, `char:爸`, `char:爱` |
| Province map | `map:北京`/`map:Beijing`, `map:江苏`/`map:Jiangsu`, `map:台湾`/`map:Taiwan`, `map:安徽`/`map:Anhui` |
| Country map | `map:中国`/`map:Chinese`/`map:China`, `map:美国`/`map:USA`/`map:America`, `map:日本`/`map:Japan` |
| SVG code | `<svg xmlns="http://www.w3.org/2000/svg">...</svg>` |
| SVG URL | `https://example.com/image.svg` |

### Response handling

On success:

```json
{
  "success": true,
  "download_url": "https://www.handbooks.cn/downloads/svg2ppt-1783264040021-5e3b271e.pptx",
  "file_name": "svg2ppt-1783264040021-5e3b271e.pptx",
  "expires_in": 604800
}
```

Reply to the user with:

> Editable PPT generated:  
> [Click to download {{file_name}}]({{download_url}})  
> The link is valid for about 7 days; please download soon.

### Calling via the bundled script (recommended)

When invoking the bundled `scripts/convert.cjs` tool, pass the API key as the first argument and the `svg` value as the second argument.

OpenClaw invokes this tool via command-line arguments. Node.js on Windows preserves Unicode argv, so Chinese characters, full SVG code, and URLs can be passed directly without base64 encoding. The script also accepts input via stdin for manual piping.

Examples:

```bash
# Pass the svg value as the second argument (recommended for OpenClaw and CJK input)
node scripts/convert.cjs SVG2PPTSKILL-xxx map:安徽
node scripts/convert.cjs SVG2PPTSKILL-xxx char:中

# For manual CLI piping, stdin is also accepted
echo "map:安徽" | node scripts/convert.cjs SVG2PPTSKILL-xxx -
echo "char:中" | node scripts/convert.cjs SVG2PPTSKILL-xxx -
```

On error:
- `400`: Parameter error or SVG conversion failed. Read the `error` field and ask the user to check their input.
- `403`: API key invalid or quota used up. Ask the user to get a new key from the handbooks homepage and try again. If it still fails, guide them to the web UI at `https://www.handbooks.cn/svg2ppt.html`.

## When NOT to use this skill

- If the user only wants to read or summarize an existing `.pptx` file, use the `pptx` skill instead.
- If the user wants programmatic/server-side batch conversion, they should use the web UI or implement their own server-side key exchange. Never expose or call `/api/skill/key` on behalf of the user.
