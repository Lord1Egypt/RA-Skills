---
name: qstar-video-ecom
version: 1.3.1
author: qstar
emoji: "🎬"
homepage: https://guanma.top
tags:
  - video
  - ecommerce
  - ai-video
  - chinese
  - product-video
  - tiktok
  - douyin
  - xiaohongshu
  - short-video
  - marketing
  - sora
  - chinese-ecommerce
  - video-generation
  - ai-marketing
description: >
  One-click AI product video generator for Chinese e-commerce, upgraded with
  advanced creation modes. Use it for classic one-click product videos, single-image
  fast starts, batch video variants, and natural-language revision requests for
  short-form commerce videos.
---

# Qstar Video Ecom

Use this skill when the user wants to make a Chinese e-commerce short video quickly, especially for Douyin, Xiaohongshu, Taobao, Pinduoduo, JD, or WeChat Video.

Default value: keep the old one-click product video flow as the stable path, then layer newer video-factory style modes on top.

## What this skill supports

This skill now has 4 modes:

1. `classic`
Classic one-click product video.
Best when the user says "做个产品视频", "生成电商视频", "帮我出一条带解说的视频".

2. `single-image`
Single-image fast start.
Best when the user already has one product image, poster, hero shot, or reference visual and wants to start from it.

3. `batch-variants`
Batch multiple short-video variants from one product brief.
Best when the user wants several hooks, tones, or platform versions in one go.

4. `revise`
Natural-language revision mode.
Best when the user already has a generated video and says things like "把背景换掉", "节奏快一点", "换成男声", "再来 3 个版本".

If the user does not specify a mode, use `classic`.

## Important boundary

Do not pretend the backend already has magical edit APIs if it does not.

For newer modes:
- If the current `bot.guanma.top/sora-api` endpoints can support the request with the existing generate flow, use them.
- If the request exceeds current API capability, convert the user intent into a structured generation brief and explain that you are using the nearest supported workflow.
- Prefer a truthful fallback over a fake "done".

## Step 0 — Extract USER_ID

Extract platform and sender_id from the current session key and convert to `{platform}:{sender_id}`.

Examples:
- `agent:main:telegram:direct:5239705501` -> `tg:5239705501`
- `agent:main:wechat:direct:oh8CU6xxx` -> `wx:oh8CU6xxx`
- `agent:main:wecom:direct:zhangsan` -> `wecom:zhangsan`
- `agent:main:feishu:direct:ou_xxx` -> `feishu:ou_xxx`
- `agent:main:slack:direct:U12345` -> `slack:U12345`

Always inline the real value into commands. Do not rely on shell variables.

## Step 1 — Detect mode

Route by user intent:

- `classic`
User wants one finished e-commerce short video and has no advanced request.

- `single-image`
User gives or mentions a specific product image / hero image / visual reference and wants to start from that one image.

- `batch-variants`
User asks for multiple versions, multiple hooks, multiple platforms, multiple tones, or "批量跑素材".

- `revise`
User already has an existing video and wants changes in plain language.

If mixed, prefer:
`revise` > `batch-variants` > `single-image` > `classic`

## Step 2 — Check profile

```bash
curl -s https://bot.guanma.top/sora-api/user/profile/{USER_ID}
```

If `onboarded: false`, run the onboarding flow before generation.

Opening message:

```text
🎬 欢迎使用 AI 电商视频生成！

📌 使用须知：
• 免费版：每天 1 次，仅支持通用商品视频
• 付费版：不限次数，支持上传产品实拍图，生成更贴近真实商品的视频

如果你想做“基于真实产品图”的视频，建议使用付费版。
```

Ask:
1. `你主要在哪个平台经营？（淘宝/小红书/抖音/其他）`
2. `你的主营产品类目是？（服装/数码/美妆/食品/其他）`
3. `售后联系方式（选填，可跳过）`

Then:

```bash
curl -s -X POST https://bot.guanma.top/sora-api/user/onboard \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "{USER_ID}",
    "main_platform": "{用户回答1}",
    "category": "{用户回答2}",
    "contact": "{用户回答3}"
  }'
```

## Step 3 — Mode-specific intake

### Mode A: `classic`

Follow the stable old flow:

1. Ask target platform
2. Ask script style template
3. Ask product name + 2-3 core selling points
4. Ask voice choice
5. Check quota
6. If paid, allow product image upload
7. Generate one finished video

### Mode B: `single-image`

Ask for:

1. Target platform
2. Product name
3. One-sentence video goal
4. 2-3 selling points
5. Voice choice
6. One image upload or image URL

Then convert the brief into a structured `product` field like:

`[mode:single-image][platform:douyin] 产品名：{产品名}；目标：{视频目标}；卖点：{卖点列表}；要求：基于已上传图片生成，保留商品核心外观。`

If the image is available and the user has paid quota, prefer passing a direct public `image_url`.
Only use the documented upload endpoint if it is confirmed live in the current environment.
If image upload is unavailable, say you are falling back to the standard image-assisted generation path.

### Mode C: `batch-variants`

Ask for:

1. Target platform or platforms
2. Product name
3. Core selling points
4. Number of variants
5. Preferred dimensions of variation:
   - hook
   - tone
   - audience
   - CTA
   - voice

Then produce a variant plan first, for example:

- Variant 1: price-shock
- Variant 2: bestie recommendation
- Variant 3: curiosity bait

Run the current generation path once per variant if the backend only supports single-job generation.
Do not claim server-side batch execution unless it truly exists.

### Mode D: `revise`

Ask for:

1. Existing video link or generation context
2. What to change, in plain language
3. Whether the user wants:
   - overwrite-style replacement
   - one more revised version
   - several revised versions

Translate the user's request into a structured revision brief:

- scene/background change
- faster/slower rhythm
- stronger CTA
- female/male voice
- platform-specific format
- more dramatic / more everyday / more premium tone

If no true edit API exists, tell the user you are generating a revised new version instead of frame-accurate editing.

## Step 4 — Platform choice

Use this mapping:

```text
1 淘宝/天猫 -> taobao
2 拼多多 -> pinduoduo
3 小红书 -> xiaohongshu
4 抖音/TikTok -> douyin
5 京东 -> jingdong
6 视频号 -> shipinhao
```

Prompt:

```text
请选择视频发布平台：
1️⃣ 淘宝/天猫（16:9，8秒）
2️⃣ 拼多多（16:9，4秒）
3️⃣ 小红书（9:16，8秒）
4️⃣ 抖音/TikTok（9:16，8秒）
5️⃣ 京东（16:9，8秒）
6️⃣ 视频号（9:16，8秒）
```

## Step 5 — Script style template

For `classic` and most `batch-variants` cases, use the proven template system.
Template details live in [TEMPLATES.md](/Users/tiger/.codex/skills/qstar-video-ecom/TEMPLATES.md).

Prompt:

```text
请选择视频文案风格：
1️⃣ 痛点共鸣型
2️⃣ 价格冲击型
3️⃣ 闺蜜种草型
4️⃣ 专业测评型
5️⃣ 反常识悬念型
6️⃣ 自由描述
```

Map:
- `1 -> T1痛点共鸣`
- `2 -> T2价格冲击`
- `3 -> T3闺蜜种草`
- `4 -> T4专业测评`
- `5 -> T5反常识悬念`
- `6 -> free自由描述`

When the user chooses 1-5, auto-build the product brief using the template style plus platform.

## Step 6 — Voice choice

Prompt:

```text
请选择解说声音：
🎙️ 1. 晓晓（女声·温柔）
🎙️ 2. 云希（男声·稳重）
```

Map:
- `1 -> female`
- `2 -> male`

## Step 7 — Quota and image upload

Check quota:

```bash
curl -s https://bot.guanma.top/sora-api/quota/{USER_ID}
```

If `credits > 0`, allow image upload:

```text
📸 是否上传产品实拍图？上传后视频会更贴近你的真实商品。
直接发图即可，或回复“跳过”。
```

If the user sends an image, first obtain a public image URL through the host platform's image handling path, then:

```bash
curl -s -X POST "https://bot.guanma.top/sora-api/upload-image?user_id={USER_ID}" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "{用户图片的公网URL}"}'
```

Read `image_url` from the response.

If that endpoint returns `404` or equivalent unavailability, do not loop on the upload flow. Pass the original public image URL directly in the generate request instead.

The image URL must be reachable by the generation backend, not just by the local machine. Avoid internal-only hosts or asset domains that fail public DNS resolution.

If free user or skipped upload, keep `image_url` empty.

## Step 8 — Generate

Tell the user generation is running:

```text
正在生成，约需 3 分钟，请稍候...
```

Then:

```bash
curl -s -X POST https://bot.guanma.top/sora-api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "{USER_ID}",
    "platform": "{platform_key}",
    "product": "{结构化产品描述}",
    "voice": "{voice_key}",
    "image_url": "{产品图URL或空字符串}"
  }' \
  --max-time 400
```

## Step 9 — Response handling

If success:

- With uploaded image:
  `🎬 个性化视频已生成！基于你的产品图定制。`

- Free quota no image:
  `🎬 视频已生成！今日免费次数已用完，充值后可上传产品图生成更贴近真实商品的视频。`

- Paid quota no image:
  `🎬 视频已生成！如需更贴近真实商品的版本，可继续上传产品图重新生成。`

For `batch-variants`, summarize all successful outputs clearly by variant label.
For `revise`, explicitly say this is a revised version if you had to regenerate rather than edit in place.

If HTTP 402 or quota exceeded:
run the payment flow.

## Step 10 — Payment flow

Show:

```text
今日免费次数已用完 😅

升级付费版，解锁：
✅ 不限次数生成
✅ 上传产品实拍图，生成更贴近真实商品的视频

选择套餐：
1️⃣ 5次视频 · ¥39
2️⃣ 10次视频 · ¥69（最划算）
3️⃣ 20次视频 · ¥128
```

Then ask payment channel:

```text
请选择支付方式：
💚 1. 微信支付
💙 2. 支付宝
```

Create order:

```bash
curl -s -X POST "https://bot.guanma.top/sora-api/pay/create?user_id={USER_ID}&package={套餐价格}&channel={channel}"
```

Read `order_id`, `amount`, `qr_url`.
Send the QR image first, then:

```text
请扫码完成支付 👆
订单号：{order_id}
金额：¥{amount}

支付完成后系统会自动到账，无需截图。
```

Poll every 10 seconds, up to 18 times:

```bash
curl -s https://bot.guanma.top/sora-api/pay/status/{order_id}
```

If `status == "paid"`:

```text
✅ 支付成功！额度已到账，现在可以继续生成视频了。
```

Then return to Step 7.

If timeout:

```text
支付还未到账，可稍后发送“继续生成”重试。
```

## Operating rules

- Prefer the stable `classic` mode unless the user clearly wants a newer mode.
- Use `single-image` when the image is the center of the request, not just an optional add-on.
- Use `batch-variants` when the user cares about scale or testing multiple hooks.
- Use `revise` when the user wants changes to an existing output.
- Be explicit when a "revision" is actually a new regenerated version.
- Never hide quota/payment boundaries.

## Data and privacy

This skill is provided by **Q-star** via `https://guanma.top`.

- Transmitted data:
  - product description text
  - optional public product image URL
  - platform-linked user ID
  - optional contact info
- Transport:
  - HTTPS API calls to `bot.guanma.top`
- Storage:
  - generated videos are stored in Qiniu for delivery
- This skill does not read local files directly
- This skill does not access system credentials
- Payment QR codes are generated by the payment provider bound to Q-star services
