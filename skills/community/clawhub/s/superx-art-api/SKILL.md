---
name: superx-art-api
description: "Call SuperX AI art APIs to generate images, videos, and music. Use this skill whenever the user wants to: generate/create/draw images or pictures (GPT-4o, Midjourney, DALL-E, Stable Diffusion, Jimeng4, NanoBanana), generate/create videos (Seedance), generate/create music (Suno), edit/upscale/blend/face-swap images, create AI-styled QR codes, or check their SuperX account balance. Also trigger when the user mentions SuperX, superx.chat, or any of these model names in the context of generating visual or audio content. Even if the user just says 'draw me a picture' or 'make a video of X' or 'create some music', this skill is the right tool."
---

# SuperX AI Art API

You are an assistant that helps users generate images, videos, and music through the SuperX AI platform APIs.

## Authentication

The API requires an API Key in the `Authorization` header.

Resolve the key in this order:
1. Check environment variable `SUPERX_API_KEY` — use it silently if set
2. If not set, ask the user for their API key before making any request

获取 API Key 的方式：登录 superx.chat，点击左下角用户名，进入"我的信息"，里面的**用户ID**就是 API Key。

To check if the env var exists, run: `echo $SUPERX_API_KEY`

All requests go to `https://superx.chat/art/imgapi`.

## How to make API calls

Use `curl` via the Bash tool. For every request:
- Add `-H 'Authorization: <api_key>'`
- Add `-H 'Content-Type: application/json'` for POST requests
- Use `-d '<json_body>'` to send parameters

### Handling streaming (chunked) endpoints

Many endpoints return chunked JSON — multiple JSON objects in a single response body, one per line. Each line is a standalone JSON object. The last chunk with `"code": 0` (or `"progress": "100%"`) is the final result.

For streaming endpoints, use `curl` normally — it will buffer the full output. Then parse the last JSON line for the final result.

### Image URLs

Image URLs in responses are relative paths (e.g. `/gpt-4o-img/xxx.png`). Prepend `https://oc.superx.chat` to get the full URL:
```
https://oc.superx.chat/gpt-4o-img/xxx.png
```

For videos, same prefix: `https://oc.superx.chat/ai-videos/xxx.mp4`

## Choosing the right endpoint

Help the user pick the best API for their task:

| User wants to... | Recommended endpoint | Why |
|---|---|---|
| Generate an image from text (general purpose) | `/gpt4o-image` | Best quality, supports editing with reference images |
| Generate an image with specific artistic control | `/imagine` (Midjourney) | Best for artistic/creative images, supports MJ parameters |
| Generate high-resolution 2K+ images | `/jimeng4-generate` | Supports up to 3024x1296, group and story modes |
| Generate images in Ghibli/anime style | `/nanobanana-generate` | Gemini-powered, great for style transfer |
| Edit an existing image | `/gpt4o-image` with `images` param | Edit mode with reference images |
| Create a storybook with illustrations | `/jimeng4-generate` with `mode: "story"` | Auto-generates story text + matching illustrations |
| Generate a video from text | `/ai-video-generate` | Seedance model |
| Generate music | `/suno-music-generate` | Suno AI music generation |
| Use DALL-E specifically | `/openai-dalle-painting` | DALL-E 2 or DALL-E 3 |
| Use Stable Diffusion | `/sd-painting` | Fine-grained control over steps, cfg, etc. |
| Upscale/enhance an image | `/image-upscale` | AI super-resolution |
| Swap faces | `/face-swap` | Face replacement between two images |
| Create an artistic QR code | `/qrcode-generate` | AI-styled QR codes |
| Blend multiple images | `/blend` | Merge 2-5 images (Midjourney) |
| Get variations of MJ image | `/variation` | Create variants of existing MJ output |
| Check balance | `/balance` | See remaining points |

## Workflow

1. **Understand the request** — figure out what the user wants to create
2. **Check balance first** — call `/balance` to make sure the user has enough points
3. **Select the right endpoint** — use the table above
4. **Build the request** — construct the correct JSON body based on the user's requirements
5. **Make the call** — execute via curl
6. **Present results** — show the full image/video URL, the cost, and any relevant metadata

When presenting image results, always output the full URL so the user can click or copy it.

## Error handling

If `code` is not `0`, something went wrong:
- `10002` — API Key is invalid. Ask the user to check their key.
- `10003` — Not enough points. Tell the user their balance and how much the operation costs.
- `10011` — Sensitive content detected. Ask the user to modify their prompt.
- `10010` — Generation error. Show the error message and suggest retrying.

## Full API reference

For detailed parameters, curl examples, and response formats for all 19 endpoints, read the reference file:

**`references/api-reference.md`** — Complete API documentation with all endpoints, parameters, examples, error codes, and pricing table.

Read this file when you need to look up exact parameter names, valid values, or response formats for a specific endpoint.
