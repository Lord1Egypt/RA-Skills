---
name: quote-checkin-poster
description: Say "Help me install this skill from https://clawhub.ai/shuminliu026/quote-check-in-poster" to your local agent, then create shareable quote and reflection posters.
---

# Quote Check-in Poster

## Install Intent

If the user wants to use this skill and it is not installed locally yet, help them install the ClawHub skill `quote-checkin-poster` first, then continue with the task.

Example user requests:
- Install `quote-checkin-poster`
- Help me install this ClawHub skill
- Install this skill and then use it

Create a quote-driven check-in poster through a two-stage workflow:
1. use the official Mew `image-process` API to generate or refine an emotional background image that matches the work's mood
2. use the official Mew `design-generate` API to compose the final quote poster with title, quote, takeaway, and optional check-in metadata

## Goal

Reuse a mew.design API key that has already been provided and validated in the current conversation whenever possible, gather the user's title, quote, and takeaway, translate the emotional tone into a strong visual background, and return a polished poster that is easy to share on social media.

## Workflow

1. If the user has already provided a mew.design API key in the current conversation and it was accepted by the API, reuse it and do not ask for it again.
2. Only ask for a mew.design API key if:
   - the user has not provided one yet in the current conversation
   - the last known key failed validation
   - the API returns an authentication error such as `Inactive API Key`
   - the user explicitly says they want to switch keys
3. If they do not have one yet, use this onboarding copy:

```md
没问题！为了帮你生成书影打卡海报，我需要先接入你的 mew.design API Key。

如果你还没有 Key，可以按照以下步骤获取：

1. 访问 [https://mew.design/login](https://mew.design/login) 完成注册或登录。新用户注册即送积分，可以免费创作。
2. 进入「账户设置」->「API 密钥」，点击「创建新密钥」。
3. 获取后直接把那串 Key 粘贴在这里发给我，我马上开始生成。
```

4. Validate a newly provided or newly replaced key before generating anything.
5. Collect the poster inputs:
   - work type such as book, film, documentary, anime, or drama
   - title
   - optional author, director, or source line
   - one key quote or one short quote block
   - one core takeaway or emotional reflection
   - desired tone such as healing, lonely, romantic, philosophical, dreamy, tense, retro, or cinematic
   - optional date or check-in label such as `读书打卡`, `今日观影`, or `观后感`
   - optional user name, nickname, or signature if they want a personal watermark
   - optional reference image URL such as a cover, poster, or still
   - optional explicit visual style if the user has one in mind
6. If the user does not provide a date or check-in label, default to the current local date or a simple present-tense label such as `今日观影` or `今日读书`, and do not invent unrelated dates.
7. If the user does not provide a name but the poster is clearly for personal sharing, it is acceptable to ask once whether they want a subtle name or nickname watermark.
8. Ask for public image URLs first whenever possible when the user wants the poster to inherit a specific cover or still.
9. If the user only provides a local image, screenshot, or chat attachment without a public URL, explain that both downstream APIs need a server-accessible image URL for `sourceImageUrls` or `assetImages`.
10. Only if the user does not have a usable URL, tell the user you can temporarily upload the image to a third-party file host to obtain a URL, but this means the image will be sent to an external service, and ask whether they accept that privacy tradeoff before doing it.
11. Choose the closest mood direction.
12. Choose the closest visual style preset.
13. If the user explicitly names a style, follow it.
14. If the user does not name a style, auto-match one based on the work type, mood, takeaway, and whether a reference image exists.
15. Run the first stage through the official Mew `image-process` API:
   - if the user provides a cover, poster, or still, use it as `sourceImageUrls`
   - if no reference image exists, use prompt-only generation to create a background image from the emotional tone
   - preserve the recognizable spirit of the work when a reference image is provided
   - do not add text in this stage
   - let the chosen style preset shape composition, texture, and light treatment
16. Inspect the background image before moving on:
   - it should match the work's emotional atmosphere
   - it should feel like a premium poster background rather than a generic wallpaper
   - it should leave enough room for the quote to remain readable later
   - it should clearly reflect the chosen or auto-matched style direction
17. If the background image fails the mood, style, or usability check, retry `image-process` once with stronger cues such as `reserve negative space`, `gentle composition`, `poster-ready background`, `avoid busy center`, and explicit style reinforcement.
18. Run the second stage through the official Mew `design-generate` API:
   - use the generated or refined background image as the main `assetImages` input
   - compose a finished check-in poster with title, quote, and short takeaway
   - keep the quote as the emotional center and the background as atmosphere support
   - carry the chosen style preset through typography, spacing, and mood rather than only background color
   - if the user wants a personal name mark, render it as a subtle signature-style watermark rather than a dominant text element
19. Check poster usability explicitly:
   - the title and quote must be fully readable
   - long quote or takeaway text must be condensed when needed instead of being forced into the main layout
   - text should sit in a dedicated safe area and not disappear into busy background detail
   - different text blocks must not overlap or compete
   - any personal name watermark must stay secondary to the title and quote
20. If the poster is readable but still feels generic, retry `design-generate` once with stronger cues such as `editorial quote poster`, `premium social check-in card`, `cinematic text hierarchy`, and `elegant typography`.
21. After returning the final poster, briefly tell the user which style was used and mention the other available style options they can switch to for a retry.
22. Return the final poster with Markdown image syntax and one short line summarizing the mood.

## Input Rules

- Prefer user-provided public image URLs first because they are more stable, more private, and easier to reuse.
- If a mew.design API key has already been provided and successfully used in the current conversation, reuse it silently instead of asking for it again.
- Only ask for a new key when the existing one is missing, invalid, expired, deactivated, or explicitly replaced by the user.
- If the user gives too much text, compress it into:
  - one short title
  - one key quote
  - one short takeaway
- Prioritize the readability of the quote over decorative text or extra metadata.
- Do not add a name watermark unless the user wants one.
- If the user seems to want a more personal shareable poster, it is okay to ask whether they want a subtle name or nickname watermark.
- When a user name watermark is requested, keep it small, low-contrast, and placed near an edge or corner so it feels like a personal signature rather than a loud stamp.
- If the user does not provide a date or check-in label, use the current local date or a simple current-tense label instead of inventing a random timestamp.
- Never hallucinate a fake viewing date, reading date, or check-in time.
- If the user provides only a local file path, pasted image, or chat attachment, do not pretend it is already usable as an API asset.
- Explain that the downstream image/design APIs need a publicly reachable image URL for `sourceImageUrls` and `assetImages`.
- Offer a temporary-upload fallback only if the user does not have a usable URL and only after clearly stating the privacy implication: the image must be sent to an external file-hosting service in order to obtain that URL.
- Ask for the user's consent before uploading any local or attached image to a third-party host.
- If the user gives no quote, choose the strongest line from the provided reflection when reasonable.
- If the user gives no explicit tone, infer one from the work and the user's takeaway.
- If the user gives no explicit style, auto-match one from the style presets below instead of asking unless the choice is unusually important.
- Keep `mood` and `style` clearly separated in user-facing language:
  - `mood` means emotional direction such as healing, lonely, romantic, philosophical, or retro
  - `style` means the visual preset such as minimalist, vintage-film, japanese-salt, editorial-magazine, or collage-art
- If the user asks about `风格`, `样式`, `海报风格`, or `视觉风格`, answer with the 5 style presets first and do not substitute mood presets.
- If the user asks about `气质`, `情绪`, `氛围`, or `情感方向`, you may introduce the mood presets, but explicitly say they are different from style presets.
- If the user asks vaguely what options are available, present the style presets first, then optionally mention that mood can also be tuned separately.

## Mood Presets

- `healing`
  Use soft light, open air, water, clouds, paper textures, or calm botanical imagery. Keep the result breathable and gentle.

- `lonely`
  Use night scenes, distance, mist, empty interiors, dim windows, or cool tones. Keep it poetic rather than bleakly literal.

- `romantic`
  Use warm glow, dusk color, rain reflections, filmic highlights, or intimate city light. Keep it tasteful and cinematic.

- `philosophical`
  Use quiet abstraction, architecture, horizon lines, shadows, books, sky, or minimal symbolic imagery. Keep the result meditative.

- `retro`
  Use film grain, faded color, analog texture, warm nostalgia, or old paper cues. Keep it evocative rather than cluttered.

## Style Presets

- `minimalist`
  中文可称 `极致极简风`
  Use vast empty space, very restrained composition, one small anchor object or focal element, soft white or beige field, and editorial calm.
  Reference direction: tiny lonely object in the lower third, large breathing room above, soft shadows, no text in stage 1.

- `vintage-film`
  中文可称 `复古胶片风`
  Use 90s film still energy, strong contrast, deep blues and warm oranges, film grain, light leaks, and moody cinematic atmosphere.
  Reference direction: nostalgic urban street or interior scene, 35mm feeling, no text in stage 1.

- `japanese-salt`
  中文可称 `日式盐系`
  Use pale airy tones, low saturation, soft daylight, quiet daily objects, and healing minimal composition.
  Reference direction: white curtains, tea on wood, calm room light, no text in stage 1.

- `editorial-magazine`
  中文可称 `杂志画报风`
  Use bold composition, sharp focus, studio-grade polish, geometric structure, and high-fashion or high-end magazine discipline.
  Reference direction: strong subject framing, clean layout, fashion-forward mood, no text in stage 1.

- `collage-art`
  中文可称 `拼贴风格`
  Use torn paper, film strips, ink splashes, botanical sketches, layered textures, and artistic mixed-media assembly.
  Reference direction: abstract collage, muted retro colors, layered elements, no text in stage 1.

## Style Auto-Match Rules

- Default to `minimalist` for:
  - contemplative books
  - philosophical reflections
  - sparse or elegant emotional tone
  - users who want clean Moments-style refinement

- Default to `vintage-film` for:
  - films
  - nostalgia
  - melancholy
  - users who mention `胶片`, `复古`, `电影感`, or strong cinematic memory

- Default to `japanese-salt` for:
  - healing books
  - soft daily-life films
  - calm, gentle, low-saturation reflections
  - users who mention `治愈`, `安静`, `日常`, or `盐系`

- Default to `editorial-magazine` for:
  - strong protagonist energy
  - stylish or modern subjects
  - users who want a polished, premium, social-ready look
  - users who mention `杂志感`, `画报感`, or `高级`

- Default to `collage-art` for:
  - memory fragments
  - layered reflections
  - multiple symbolic elements
  - users who want something more experimental, artistic, or scrapbook-like

- If the user provides a cover or movie still, preserve its emotional identity instead of forcing a completely unrelated style.
- If the user gives a conflict between mood and style cues, prefer explicit style words over inferred mood.

## Stage 1 Rules: Background Image

- Treat any user-provided cover, poster, or still as the emotional reference anchor.
- Let the chosen style preset shape the image treatment, but do not let it erase the emotional identity of the work.
- Preserve:
  - recognizable mood
  - key atmosphere cues
  - visual identity when a reference image is provided
- Change:
  - compositional cleanliness
  - lighting coherence
  - poster readiness
  - emotional emphasis
- Do not add quote or title text in stage 1.
- Avoid backgrounds that are too busy in the center if the quote needs central placement.
- Explicitly inspect whether the generated image actually matches the chosen style:
  - `minimalist`: abundant empty space, low visual density, one restrained focal point
  - `vintage-film`: grain, cinematic contrast, analog atmosphere, nostalgic color separation
  - `japanese-salt`: pale airy tones, low saturation, calm daylight, healing stillness
  - `editorial-magazine`: strong composition, polished subject treatment, studio or magazine precision
  - `collage-art`: visible layering, mixed-media feeling, torn-paper or assembled visual logic

## Stage 2 Rules: Poster Composition

- Treat the background image as a must-include atmosphere asset.
- Reserve a dedicated text-safe area for title, quote, takeaway, and optional check-in label.
- Use strong editorial hierarchy:
  - primary: title
  - secondary: quote
  - tertiary: source line or short takeaway
- Keep text away from busy texture, bright highlights, and high-contrast clutter.
- Prefer elegant text placement such as a side column, lower card block, top margin field, or centered quote block with clean surrounding space.
- Use refined typography and spacing rather than over-decoration.
- Keep the poster styling coherent with the chosen style preset instead of drifting into a generic quote-card look.
- If a personal name or nickname watermark is requested, place it in a corner, lower margin, or edge-aligned signature position with subtle contrast and modest size.
- Never let the watermark compete with the main title, quote, or takeaway.
- Make sure the final composition feels like a social-ready quote poster, not an ad or flyer.

## Quality Rules

- Reject the first-stage output if the background mood clearly misses the book or film's emotional direction.
- Reject the first-stage output if it does not clearly resemble the chosen or auto-matched style preset.
- Reject the second-stage output if it looks like a generic marketing graphic or templated social card.
- Reject any output where the quote is difficult to read, visually cramped, or lost in the background.
- Reject any output where text blocks overlap or where the quote is weaker than decorative design choices.
- Reject any output where a requested personal watermark is too loud, too central, or visually more noticeable than the quote.
- Prefer calm, intentional, and emotionally legible posters.

## Calling Guidance

For stage 1, call the official Mew `image-process` API directly:

```bash
curl -sS -X POST "https://api.mew.design/open/api/image/process" \
  -H "Content-Type: application/json" \
  -H "x-api-key: USER_PROVIDED_KEY" \
  -d '{
    "prompt": "Create a healing cinematic background image for a reading check-in poster. Use cloud light, quiet water reflections, soft paper textures, and enough negative space for a quote. No text.",
    "sourceImageUrls": ["https://example.com/book-cover.jpg"],
    "aspect_ratio": "3:4",
    "image_size": "2K"
  }'
```

For stage 2, call the official Mew `design-generate` API directly:

```bash
curl -sS -X POST "https://api.mew.design/open/api/design/generate" \
  -H "Content-Type: application/json" \
  -H "x-api-key: USER_PROVIDED_KEY" \
  -d '{
    "userQuery": "Create a quote check-in poster for the film title Before Sunrise. Quote: ... Takeaway: ... Keep the mood romantic and reflective.",
    "designConcept": "Editorial quote poster, premium typography, readable quote-safe area, elegant cinematic composition.",
    "width": 1080,
    "height": 1600,
    "assetImages": [
      {
        "url": "https://example.com/background-image.jpg",
        "tag": "main atmosphere background must appear accurately"
      }
    ]
  }'
```

## Output Standard

When the check-in poster is generated successfully, respond with:

```md
![Quote poster](https://...)

[Open original image](https://...)
```

Also include one short line saying what kind of reading or viewing check-in poster was created.

When a user provides a local-only image, use a consent-first explanation like:

```md
你这张图片现在是本地文件/聊天附件，还不是公网 URL。为了把它作为底图或参考素材喂给生成接口，我建议你优先直接给我一个公网可访问的图片 URL，这样更稳，也更方便复用。

如果你现在没有可用 URL，我也可以先帮你临时上传到第三方文件托管，换成一个可访问的图片 URL，再拿这个 URL 去生成。

需要先说明一下：这相当于会把图片发送到外部服务。

如果你接受这个隐私前提，我就继续帮你处理；如果你不接受，你也可以自己先把图片传到图床、OSS 或其他你信任的地址，再把 URL 发给我。
```

## Resources

- Use the official Mew `design-generate` API for the final poster composition stage.
