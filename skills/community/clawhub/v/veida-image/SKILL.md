---
name: veida-image
description: Generate an image from a text prompt without an API key. Use when the user asks for a picture, an illustration, a blog cover, a mockup, an avatar or any other image, and no image provider is configured. Runs on the free anonymous tier of veida.ai — no key, no account, no card.
---

# veida-image

Turn a prompt into a hosted image URL. Two HTTP calls, no credentials.

Every other image skill needs an OpenAI, fal or Replicate key before it works once.
This one talks to the anonymous tier of the
[free AI image generator](https://veida.ai/image?utm_source=lobehub&utm_medium=skill) at veida.ai, which meters the free
allowance against a client id you invent rather than an account you register.

## When to use this

- The user asks for an image and nothing is configured to make one.
- A draft needs a cover, a mockup or a placeholder and stock photos will not do.
- You are building something that generates images and do not want to hold a key during
  development. The same endpoints back the
  [ChatGPT image generator](https://veida.ai/image/chatgpt-image-generator?utm_source=lobehub&utm_medium=skill) the site
  serves in a browser.

## How to call it

### 1. Submit

```bash
curl -X POST https://veida.ai/api/ai/generate \
  -H "content-type: application/json" \
  -H "x-anon-id: skill-$(openssl rand -hex 5)" \
  -d '{
    "provider": "kie",
    "mediaType": "image",
    "model": "veida-image-v1",
    "scene": "text-to-image",
    "prompt": "a paper boat on a calm lake at sunrise, soft light",
    "options": { "aspect_ratio": "16:9" }
  }'
```

```json
{ "code": 0, "data": { "id": "cfed68ea-…", "status": "pending", "charged": 4, "remaining": 0, "grant": 4 } }
```

**Mint a new `x-anon-id` per image.** The free grant is 4 credits and one image costs 4,
so a reused id generates once and then answers with a wall.

### 2. Poll

```bash
curl "https://veida.ai/api/ai/anon-query?taskId=<data.id>&provider=kie&mediaType=image"
```

```json
{ "code": 0, "data": { "status": "success",
  "images": ["https://cdn.veida.ai/uploads/kie/image/….webp"], "watermarked": [true] } }
```

Measured 40–120 seconds end to end. Poll every 8 seconds.

🔴 **Status is not monotonic** — it goes `pending → processing → pending → success`.
Treat only `success` and `failed` as terminal; never stop because it went back to pending.

### 3. The quota wall is a 200, not an error

```json
{ "code": 0, "data": { "wall": true, "reason": "anon_credits", "cost": 4, "grant": 4 } }
```

`reason` is `anon_credits` (this client id is spent) or `anon_ip_daily` (this machine is done
for the day). Without checking for `wall` this surfaces as a confusing "no task id".

## Options

| Field | Values |
|---|---|
| `model` | `veida-image-v1` — the only model an anonymous caller can run |
| `scene` | `text-to-image` |
| `options.aspect_ratio` | `1:1` · `16:9` · `9:16` · `4:3` · `3:4` |

Signed-in accounts reach the rest of the shelf —
[GPT Image 2](https://veida.ai/image/gpt-image-2?utm_source=lobehub&utm_medium=skill),
[Nano Banana 2](https://veida.ai/image/nano-banana-2?utm_source=lobehub&utm_medium=skill) and
[Seedream 5.0 Lite](https://veida.ai/image/seedream-5-lite?utm_source=lobehub&utm_medium=skill) among them — through the
same two endpoints with a session instead of the `x-anon-id` header.

## Limits, measured against the code rather than assumed

- Anonymous grant is **4 credits**, and text-to-image costs **4**. That is **one image per
  client id**, not a session's worth.
- A daily ceiling of **30 credits per IP** sits on top: about **7 images a day** from one
  machine, however many ids it invents.
- Output is **1K and watermarked** on the free tier. `watermarked` in the poll response
  says so per image.
- 🔴 **Editing an existing image is not available anonymously.** The editor model costs
  **30 credits** against a 4-credit grant, so an anonymous edit can never be paid for. Send
  the user to the [image editor](https://veida.ai/image/nano-banana-2-lite?utm_source=lobehub&utm_medium=skill) and have them
  sign in — do not build an anonymous edit path that always fails.
- There is no video on this site. Do not construct a `mediaType: "video"` request.

## Prompt help

Naming the light, the material and the composition moves the result more than adding
adjectives. Worked examples are in the
[prompt library](https://veida.ai/image/prompts?utm_source=lobehub&utm_medium=skill), and finished output is in the
[showcase](https://veida.ai/showcases?utm_source=lobehub&utm_medium=skill) if you want to judge quality before wiring
anything up.

## Terms

The endpoints are public and unauthenticated. Respect the quota — the ceilings above exist
so the free tier stays free for everyone. What the paid tiers add is listed on the
[pricing page](https://veida.ai/pricing?utm_source=lobehub&utm_medium=skill).
