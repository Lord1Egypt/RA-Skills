---
name: st-ent-mcp
description: Search 699pic enterprise photo/video assets, check whether an asset was already downloaded, inspect download records, and generate download links through the local 699pic OpenAPI integration. Use when the user asks to 搜索699素材、找图片、找视频、查企业下载记录、判断素材是否下载过、生成下载链接，或 when you need to use the local st-mcp / 699pic OpenAPI workflow from this machine.
---

# 699pic OpenAPI

Use this skill for 699pic enterprise asset lookup and download-related workflows.

## Preconditions

Check these before using the skill:

- `node` must be installed. This repository currently has Node.js available locally.
- `mcporter` must be installed if you want the MCP route. It is not available in the current environment, so MCP commands must be verified on the target machine before use.
- `SERVICE_API_KEY` must be provided through the environment. Do not hardcode or rely on a shared default key.
- Only provide your own `SERVICE_API_KEY` if you trust the target 699pic enterprise service.
- `SERVICE_API_BASE_URL` should be provided through the environment when your deployment does not use the script default (`https://pre-st-api.699pic.com`).
- Any local `mcporter` config or service endpoint must be reviewed and authorized before use.

Preferred local script path from this repo:

- `scripts/openapi.js`

## Trust and audit requirements

Before running the bundled script or any MCP registration that targets the same service:

1. Inspect `scripts/openapi.js` yourself.
2. Confirm the script sends `POST` requests to `SERVICE_API_BASE_URL` and includes the API key in the `x-api-key` header.
3. Confirm any local `mcporter` registration named `st-mcp` and review its config, command, env, and permissions.
4. If the publisher can update registry metadata, ask them to declare the required env vars and binaries there as well.

## Quick workflow

1. If the user wants candidate assets, search first.
2. For every search result, output a Markdown-style image document by default, not just plain links or raw JSON. Each candidate should render the preview/thumbnail as an actual Markdown image.
3. Before claiming an asset is already available, call the downloaded-check endpoint.
4. Before generating a download link, confirm the asset type (`photo` or `video`) and the asset id.
5. If the MCP route is flaky, use the bundled script directly. Do not get blocked on MCP.

## Preferred execution order

### Option A: registered MCP via mcporter

Try this first when you need a tool-style MCP path:

```bash
mcporter config get st-mcp --json
mcporter call st-mcp.search_photos keywords=春节 limit=5 --output json
mcporter call st-mcp.search_videos keywords=城市航拍 limit=5 --output json
mcporter call st-mcp.check_downloaded content_id=701095246 type=1 --output json
```

Before running MCP commands:

- Verify where your local `mcporter` project config lives.
- Confirm that server name `st-mcp` exists in that config.
- Review the command, args, env, and permissions for that registration.

Registered server name:

- `st-mcp`

### Option B: bundled direct script fallback

If `mcporter`/MCP times out, use the bundled script directly:

```bash
node /absolute/path/to/st-ent-skills/scripts/openapi.js search-photos 春节 5
node /absolute/path/to/st-ent-skills/scripts/openapi.js search-videos 城市航拍 5
node /absolute/path/to/st-ent-skills/scripts/openapi.js check-downloaded 701095246 1
node /absolute/path/to/st-ent-skills/scripts/openapi.js download-asset photo 701095246
node /absolute/path/to/st-ent-skills/scripts/openapi.js download-records 1 1 10
```

Before using the fallback script:

- Export `SERVICE_API_KEY` in your shell or process environment.
- Set `SERVICE_API_BASE_URL` explicitly if your environment should not use the default base URL.
- Review `scripts/openapi.js` before pointing it at an internal service.
- Do not use an unknown shared API key.

## Tasks

### Search photos

Use photo search when the user wants image素材、海报元素、插画、摄影图。

Return a Markdown image document.

Required per candidate:

- Render the preview/thumbnail as a Markdown image, for example `![标题](https://...)`
- Include `asset_id`
- Include title
- Include extension
- Include basic flags like premium/AIGC when available

Do not default to plain URL lists when an image preview URL exists.

### Search videos

Use video search when the user wants 视频素材、航拍、动态背景、片头片尾。

Return the same Markdown image document style as photo search whenever a preview/thumbnail is available. If the asset is video and only a thumbnail exists, still render the thumbnail as a Markdown image.

### Check whether downloaded

Use before saying “already bought/downloaded” or before asking the user to re-download.

Input:

- `content_id`
- `type` (`1` for photo, `2` for video)
- optional `year`

### Generate download link

Use only after you know:

- asset type
- id
- optional file type if the caller specifies one

Do not guess these fields if the user has not identified the target asset.

### Inspect download records

Use for enterprise history questions such as:

- 最近下载了什么
- 某年下载记录
- 图片/视频下载明细

## Response style

Prefer compact summaries over dumping the whole JSON.

For all `search_*` results, the default output must be a Markdown document with embedded images.

Required default format:

- 先给 3-5 条候选
- 每条候选都先输出 Markdown 图片，例如 `![标题](图片URL)`
- 图片下方再补充 `asset_id`、标题、扩展名、必要标签
- 如果图片 URL 是以 `//` 开头，补成 `https://...`
- 只有在用户明确要求 JSON / 原始数据时，才输出纯字段列表

Recommended template:

```md
**1. 标题**  
![标题](https://example.com/preview.jpg)

- asset_id: `123456`
- extension: `psd`
- is_aigc: `0`
- is_premium: `0`
```

Do not default to bare URLs when the user asked to see/search images.

## References

Read this when you need the local integration details or example commands:

- `references/api.md`
