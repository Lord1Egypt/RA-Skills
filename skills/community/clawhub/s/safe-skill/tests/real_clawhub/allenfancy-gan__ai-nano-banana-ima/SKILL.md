---
name: IMA Nano Banana
version: 1.0.0
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, nano banana, gemini image, text to image, image to image
argument-hint: "[text prompt or image URL]"
description: >
  Image generation with IMA Open API using only Nano Banana series: Nano Banana,
  Nano Banana Pro, Nano Banana 2. Budget (Nano Banana2 512px), balanced (Nano Banana2/Pro),
  premium (Nano Banana Pro 4K). Native aspect_ratio (1:1, 16:9, 9:16, 4:3, 3:4).
  Requires ima_* API key. Bundled script: scripts/ima_image_create.py.
---

# IMA Nano Banana (Image Generation)

## Overview

This skill calls the IMA Open API for **image generation** using **only the Nano Banana series**: **Nano Banana**, **Nano Banana Pro**, **Nano Banana 2**. No other models (e.g. SeeDream, Midjourney) are used or documented here.

**Supported task types:** `text_to_image`, `image_to_image`.

---

## 📥 User Input Parsing (Model & Parameter Recognition)

Normalize user wording (case-insensitive), then map to **task_type**, **model_id**, and **parameters**.

### 1. User phrasing → task_type

| User intent / phrasing | task_type | Notes |
|------------------------|-----------|--------|
| Only text, no input image | `text_to_image` | "画一张…" / "生成图片" / "text to image" |
| One input image + edit/transform | `image_to_image` | "把这张图…" / "参考这张图生成" / "图生图" / "风格迁移" |

If the user attaches or links one image and asks to change it or generate something "like this", use `image_to_image` with that image as input.

### 2. Model name / alias → model_id (Nano Banana only)

| User says (examples) | model_id | Notes |
|----------------------|----------|--------|
| Nano Banana / 香蕉 / Banana2 / NB2 / 最便宜 / budget | `gemini-3.1-flash-image` | Nano Banana2, 4–13 pts |
| Nano Banana Pro / Banana Pro / NB Pro / 最好 / premium | `gemini-3-pro-image` | 10–18 pts |
| 默认 / 不指定 | `gemini-3.1-flash-image` | Default: balanced, fast |

### 3. User phrasing → size / aspect_ratio

| User says (examples) | Parameter | Normalized value | Notes |
|----------------------|-----------|------------------|-------|
| 16:9 / 横图 / 9:16 / 竖图 / 4:3 / 3:4 / 1:1 | aspect_ratio | 16:9, 9:16, 4:3, 3:4, 1:1 | Native support |
| 4K / 2K / 1K / 512 | size | 4K, 2K, 1K, 512px | Via attribute_id |

Nano Banana 系列均**原生支持** aspect_ratio。**8K** 不支持，最高 4K；若用户要求 8K，告知并改用 4K。

---

## 💬 User Experience Protocol (IM / Feishu / Discord)

This skill runs inside IM platforms (Feishu, Discord via OpenClaw).  
**Never let users wait in silence.** Always follow all 6 steps below, every single time.

### 🚫 Never Say to Users

| ❌ Never say | ✅ What users care about |
|-------------|--------------------------|
| `ima_image_create.py` / 脚本 / script | — |
| 自动化脚本 / automation | — |
| 自动处理产品列表 / 查询接口 | — |
| attribute_id / model_version / form_config | — |
| API 调用 / HTTP 请求 / 任何技术参数名 | — |

Only tell users: **model name · estimated time · credits · result (image/media) · plain-language status**.

---

### Estimated Generation Time per Model

| Model | Estimated Time | Poll Every | Send Progress Every |
|-------|----------------|------------|---------------------|
| **Nano Banana2** 💚 | 20~40s | 5s | 15s |
| **Nano Banana Pro** | 60~120s | 5s | 30s |

`estimated_max_seconds` = the upper bound (e.g. 40 for Nano Banana2, 120 for Nano Banana Pro).

---

### Step 0 — Initial Acknowledgment Reply (Normal Reply)

**Before doing anything else**, reply to the user with a friendly acknowledgment using your **normal reply** (not `message` tool). This reply will appear FIRST in the conversation.

**Example acknowledgment messages:**
```
好的!来帮你画一只萌萌的猫咪 🐱
```
```
收到！马上为你生成一张 16:9 的风景照 🏔️
```
```
OK! Starting image generation with Nano Banana2 🎨
```

**Rules:** Short and warm (< 15 words), match user language (Chinese/English), include relevant emoji. This is your ONLY normal reply — all subsequent updates use `message` tool.

---

### Step 1 — Pre-Generation Notification (Push via message tool)

**After Step 0 reply**, use the `message` tool to push a notification:

**User-facing message template:**
```
🎨 开始生成图片，请稍候…
• 模型：[Model Name]
• 预计耗时：[X ~ Y 秒]
• 消耗积分：[N pts]
```

**Cost transparency examples (Nano Banana only):**
- Balanced/default: "使用 Nano Banana2（4–13 积分，可选 512px/1K/2K/4K）"
- Premium: "使用 Nano Banana Pro（10–18 积分，最高质量，1K/2K/4K）"
- Budget: "使用 Nano Banana2 512px（4 积分，最便宜最快）"

---

### Step 2 — Progress Updates (Push via message tool)

1. Start the generation script in background or use polling loop  
2. Track elapsed time since start  
3. Every `[Send Progress Every]` seconds (see table above), push a progress update via `message` tool  
4. Stop when task completes (success/failure)

**Progress message template:**
```
⏳ 正在生成中… [P]%
已等待 [elapsed]s，预计最长 [max]s
```

**Progress formula:** `P = min(95, floor(elapsed_seconds / estimated_max_seconds * 100))`. Cap at 95% until API returns `success`. If `elapsed > estimated_max`: keep P at 95% and append `「稍等，即将完成…」`.

**When to send progress:** Short tasks (<20s) skip Step 2; medium (20–60s) send 1–2 updates; long (>60s) every 20–30s.

---

### Step 3 — Success Notification (Push image via message tool)

When task status = `success`, use the `message` tool to **send the generated image** (not plain text URL):

**Caption template:**
```
✅ 图片生成成功！
• 模型：[Model Name]
• 耗时：预计 [X~Y]s，实际 [actual]s
• 消耗积分：[N pts]

🔗 原始链接：{image_url}
```

**Platform:** Feishu/Discord — `message(action=send, media=url, caption="...")`. Do NOT send only a text URL; users expect to see the image rendered.

---

### Step 4 — Failure Notification (Push via message tool)

When task status = `failed` or any API/network error, push a failure message with alternative suggestions (Nano Banana only):

**Message template:**
```
❌ 图片生成失败
• 原因：[natural_language_error_message]
• 建议改用：
  - [Alt Model 1]（[特点]，[N pts]）
  - [Alt Model 2]（[特点]，[N pts]）

需要我帮你用其他模型重试吗？
```

**Error Message Translation (user-facing only)**

Never show technical errors. API key & credits: imaclaw.ai (same IMA platform as imastudio.com).

| Technical Error | ❌ Never Say | ✅ Say Instead (Chinese) | ✅ Say Instead (English) |
|-----------------|-------------|--------------------------|---------------------------|
| `401 Unauthorized` | Invalid API key / 401 | ❌ API密钥无效或未授权<br>💡 **生成新密钥**: https://www.imaclaw.ai/imaclaw/apikey | ❌ API key is invalid or unauthorized<br>💡 **Generate API Key**: https://www.imaclaw.ai/imaclaw/apikey |
| `4008 Insufficient points` | Insufficient points / 4008 | ❌ 积分不足，无法创建任务<br>💡 **购买积分**: https://www.imaclaw.ai/imaclaw/subscription | ❌ Insufficient points to create this task<br>💡 **Buy Credits**: https://www.imaclaw.ai/imaclaw/subscription |
| `"Invalid product attribute"` / `"Insufficient points"` | Invalid product attribute | 生成参数配置异常，请稍后重试 | Configuration error, please try again later |
| Error 6006 (credit mismatch) | Error 6006 | 积分计算异常，系统正在修复 | Points calculation error, system is fixing |
| Error 6010 (attribute_id mismatch) | Attribute ID does not match | 模型参数不匹配，请尝试其他模型 | Model parameters incompatible, try another model |
| error 400 (bad request) | error 400 / Bad request | 图片参数设置有误，请调整尺寸或比例 | Image parameter error, adjust size or aspect ratio |
| `resource_status == 2` | Resource status 2 | 图片生成遇到问题，建议换个模型试试 | Image generation failed, try another model |
| `status == "failed"` | Task failed | 这次生成没成功，要不换个模型试试？ | Generation unsuccessful, try a different model? |
| timeout | Task timed out | 生成时间过长已超时，建议用更快的模型 | Generation took too long, try a faster model |
| Network error | Connection refused / Network error | 网络连接不稳定，请检查网络后重试 | Network connection unstable, check network and retry |
| Rate limit exceeded | 429 / Rate limit | 请求过于频繁，请稍等片刻再试 | Too many requests, please wait a moment |
| Unsupported aspect ratio | Parameter not supported | 请使用支持的比例：1:1、16:9、9:16、4:3、3:4 | Use supported ratios: 1:1, 16:9, 9:16, 4:3, 3:4 |

**Generic fallback:** Chinese: `图片生成遇到问题，请稍后重试或换个模型试试` / English: `Image generation encountered an issue, please try again or use another model`

**Failure fallback (Nano Banana only):**

| Failed Model | First Alt | Second Alt |
|--------------|-----------|------------|
| **Nano Banana2** | **Nano Banana Pro**（高质量，10–18 pts） | 同款换 size/attribute_id |
| **Nano Banana Pro** | **Nano Banana2**（更快更省，4 pts 起） | 同款换 size |

---

### Step 5 — Done (No Further Action)

After Steps 0–4: no further reply or `NO_REPLY`. Do not send duplicate confirmations or the same content twice via `message` tool.

**Flow summary:** Step 0 normal reply (first) → Step 1 start notification → Step 2 progress (if >20s) → Step 3 success image + caption → Step 5 done.

---

## ⚙️ How This Skill Works

This skill uses a bundled Python script (`scripts/ima_image_create.py`) to call the IMA Open API. The script:

- Sends your prompt to IMA's servers (two domains, see below)
- Uses `--user-id` **only locally** as a key for storing model preferences
- Returns an image URL when generation is complete

### 🌐 Network Endpoints Used

| Domain | Purpose | What's Sent | Authentication |
|--------|---------|-------------|-----------------|
| `api.imastudio.com` | Main API (task create, status poll) | Prompts, model params, task IDs | Bearer token (IMA API key) |
| `imapi.liveme.com` | Image upload (OSS token) | Image files (i2i only), IMA API key | IMA API key + APP_KEY signature |

Both domains are owned and operated by IMA Studio. For text_to_image, only `api.imastudio.com` is contacted.

### ⚠️ Credential Security Notice

Your IMA API key is sent to **both** domains when using image_to_image. Best practices: use a test/scoped key first; do not share or commit the key. Get key at https://imastudio.com.

**What gets sent:** prompt, model selection, image params, image files (i2i), IMA API key. **Not sent:** user_id (local prefs only).

**Stored locally:** `~/.openclaw/memory/ima_prefs.json` (preferences), `~/.openclaw/logs/ima_skills/` (logs, auto-deleted after 7 days).

### Agent Execution (Bundled Script)

Use the script in **this skill** to ensure correct parameter construction:

```bash
# List available models (Nano Banana series in product list)
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY --task-type text_to_image --list-models

# text_to_image — default Nano Banana2
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY --task-type text_to_image \
  --model-id gemini-3.1-flash-image --prompt "a cute puppy on grass" \
  --user-id {user_id} --output-json

# text_to_image — Nano Banana Pro 4K
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY --task-type text_to_image \
  --model-id gemini-3-pro-image --prompt "sunset landscape" \
  --size 4K --user-id {user_id} --output-json

# image_to_image
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY --task-type image_to_image \
  --model-id gemini-3.1-flash-image --prompt "turn into oil painting" \
  --input-images https://example.com/photo.jpg --user-id {user_id} --output-json
```

The script outputs JSON; parse it for the result URL and pass to the user via the UX protocol above.

---

## 🔒 Security & Transparency Policy

- **Review source:** `scripts/ima_image_create.py`, `ima_logger.py`
- **Verify endpoints:** `api.imastudio.com`, `imapi.liveme.com` (see script)
- **Set API key:** `export IMA_API_KEY=ima_...` or in agent env
- **Data control:** Delete `~/.openclaw/memory/ima_prefs.json` to reset prefs; logs auto-cleanup in 7 days

**Avoid:** Sharing API keys, modifying endpoints to unknown servers, disabling SSL, logging sensitive data.

---

## 🧠 User Preference Memory

**Storage:** `~/.openclaw/memory/ima_prefs.json`

**Model selection:** 1) If user preference exists → use it. 2) Else → use recommended default (Nano Banana2 for balanced, Nano Banana Pro for premium).

**Save preference when:** User says "用XXX" / "以后都用XXX" / "默认用XXX" / "我喜欢XXX".

**Clear preference when:** User says "用最好的" / "推荐一个" / "用默认的" / "试试别的" (no specific model).

---

## ⭐ Model Selection Priority & Recommended Defaults

**Priority:** 1) User preference (if saved). 2) Fallback below (Nano Banana only).

| Task | Default Model | model_id | Cost | Why |
|------|---------------|----------|------|-----|
| text_to_image | **Nano Banana2** 💚 | `gemini-3.1-flash-image` | 4–13 pts | Balanced, fast, 512px/1K/2K/4K |
| text_to_image (budget) | **Nano Banana2** 512px | `gemini-3.1-flash-image` | 4 pts | Cheapest, fastest |
| text_to_image (premium) | **Nano Banana Pro** | `gemini-3-pro-image` | 10/10/18 pts | Best quality, 1K/2K/4K |
| image_to_image | **Nano Banana2** 💚 | `gemini-3.1-flash-image` | 4–13 pts | Same as text_to_image |
| image_to_image (premium) | **Nano Banana Pro** | `gemini-3-pro-image` | 10 pts | Best i2i quality |

---

## Supported Models (Nano Banana Only)

### text_to_image

| Name | model_id | version_id | Cost | attribute_id (参考) | Size |
|------|----------|------------|------|---------------------|------|
| **Nano Banana2** 💚 | `gemini-3.1-flash-image` | `gemini-3.1-flash-image-preview` | 4/6/10/13 pts | 4400/4401/4402/4403 | 512px / 1K / 2K / 4K |
| **Nano Banana Pro** | `gemini-3-pro-image` | `gemini-3-pro-image-preview` | 10/10/18 pts | 2399/2400/2401 | 1K / 2K / 4K |

### image_to_image

| Name | model_id | Cost | attribute_id (参考) |
|------|----------|------|---------------------|
| **Nano Banana2** 💚 | `gemini-3.1-flash-image` | 4/6/10/13 pts | 4404/4405/4406/4407 |
| **Nano Banana Pro** | `gemini-3-pro-image` | 10 pts | 2402/2403/2404 |

⚠️ **attribute_id** must be obtained at runtime from `GET /open/v1/product/list?category=text_to_image` or `image_to_image` (type=3 nodes, credit_rules[0]).

### Model Capabilities

| Model | aspect_ratio | Max Resolution | Size Options |
|-------|--------------|---------------|--------------|
| **Nano Banana2** | ✅ 1:1, 16:9, 9:16, 4:3, 3:4 | 4K | 512px(4) / 1K(6) / 2K(10) / 4K(13) pts |
| **Nano Banana Pro** | ✅ 1:1, 16:9, 9:16, 4:3, 3:4 | 4K | 1K(10) / 2K(10) / 4K(18) pts |

**8K:** Not supported. Max 4K. Inform user and use 4K if they ask for 8K.

---

## Environment

**Base URL:** `https://api.imastudio.com`

| Header | Required | Value |
|--------|----------|-------|
| `Authorization` | ✅ | `Bearer ima_your_api_key_here` |
| `x-app-source` | ✅ | `ima_skills` |
| `x_app_language` | recommended | `en` / `zh` |

---

## ⚠️ MANDATORY: Always Query Product List First

You **MUST** call `GET /open/v1/product/list?app=ima&platform=web&category=text_to_image` (or `image_to_image`) **before** creating any task. The `attribute_id` is required in the create request. If it is 0 or missing → "Invalid product attribute" / "Insufficient points" → task fails.

**How to get attribute_id:** Traverse response `data` → find `type=3` leaf where `model_id` matches target → use `credit_rules[0].attribute_id`, `credit_rules[0].points`, `id` (model_version), `name`, and `form_config` for defaults.

---

## Core Flow

1. **GET /open/v1/product/list** → get attribute_id, credit, model_version, form_config  
2. **[image_to_image only]** Upload input image → get public HTTPS URL (see Image Upload below)  
3. **POST /open/v1/tasks/create** → include attribute_id, model_name, model_version, credit, cast, prompt (nested in parameters.parameters)  
4. **POST /open/v1/tasks/detail** {task_id} → poll every 2–5s until medias[].resource_status == 1 → extract url

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| attribute_id 0 or missing | Always fetch product list first; use credit_rules[0] |
| prompt at outer level | prompt must be inside parameters[].parameters |
| Wrong credit | Must match credit_rules[].points (Error 6006) |
| image_to_image: missing src_img_url or input_images | Both required |
| Using non–Nano Banana model_id | This skill only uses gemini-3.1-flash-image, gemini-3-pro-image |

---

## Image Upload (Required for image_to_image)

The API does **not** accept raw bytes or base64. Input images must be public HTTPS URLs.

**Two-step flow:** 1) GET `/api/rest/oss/getuploadtoken` → { ful, fdl }. 2) PUT {ful} with raw image bytes → use **fdl** (CDN URL) as `input_images` value. The bundled script implements this; use script or same logic when calling API directly.

---

## Supported Task Types

| category | Capability | Input |
|----------|------------|-------|
| `text_to_image` | Text → Image | prompt |
| `image_to_image` | Image → Image | prompt + input image URL(s) |

---

## Detail API Status Values

| resource_status | status | Action |
|----------------|--------|--------|
| 0 or null | pending / processing | Keep polling |
| 1 | success | Stop; read url from medias |
| 1 | failed | Stop; handle error |
| 2 / 3 | any | Stop; handle error |

Treat `resource_status: null` as 0. Stop only when **all** medias have resource_status == 1.

---

## API 1: Product List

```
GET /open/v1/product/list?app=ima&platform=web&category=text_to_image
```

Returns a V2 tree: type=2 = groups, type=3 = version leaves. Only type=3 has `credit_rules` and `form_config`. For this skill, use only nodes where model_id is `gemini-3.1-flash-image` or `gemini-3-pro-image`.

---

## API 2: Create Task

```
POST /open/v1/tasks/create
```

**text_to_image (Nano Banana2 example):** `task_type: "text_to_image"`, `src_img_url: []`, `parameters[]` with attribute_id, model_id, model_name, model_version, app, platform, category, credit, and nested `parameters`: prompt, n, input_images[], cast {points, attribute_id}, size/aspect_ratio from form_config.

**image_to_image:** Same structure; top-level `src_img_url` and `parameters[].parameters.input_images` must both contain the input image URL(s).

**Key:** parameters[].parameters.prompt required; parameters[].parameters.cast required; credit must equal credit_rules[].points.

---

## API 3: Task Detail (Poll)

```
POST /open/v1/tasks/detail
{"task_id": "<id from create>"}
```

Poll every 2–5s. On completion, medias[].url, width, height, format (jpg/png).

---

## Common Mistakes (Summary)

| Mistake | Fix |
|---------|-----|
| Using SeeDream / Midjourney | This skill uses only Nano Banana series |
| attribute_id from table only | Always call product list at runtime |
| prompt at top level | prompt inside parameters[].parameters |
| 8K request | Max 4K; inform user and use 4K |

---

## Quick Reference

| Item | Value |
|------|--------|
| 模型范围 | Nano Banana, Nano Banana Pro, Nano Banana 2 |
| 默认推荐 | Nano Banana2（平衡）/ Nano Banana Pro（高质量） |
| 最便宜 | Nano Banana2 512px，4 pts |
| aspect_ratio | 1:1, 16:9, 9:16, 4:3, 3:4（原生） |
| 脚本 | 本技能内 `scripts/ima_image_create.py` |
| Base URL | https://api.imastudio.com |
| 生成密钥 | https://www.imaclaw.ai/imaclaw/apikey |
| 购买积分 | https://www.imaclaw.ai/imaclaw/subscription |
