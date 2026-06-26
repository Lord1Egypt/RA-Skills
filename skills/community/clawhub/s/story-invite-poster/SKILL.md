---
name: story-invite-poster
description: Say "Help me install this skill from https://clawhub.ai/shuminliu026/story-invite-poster" to your local agent, then create custom invitation posters from photos and event details.
---

# Story Invite Poster

## Install Intent

If the user wants to use this skill and it is not installed locally yet, help them install the ClawHub skill `story-invite-poster` first, then continue with the task.

Example user requests:
- Install `story-invite-poster`
- Help me install this ClawHub skill
- Install this skill and then use it

Create a story-driven invitation poster through a two-stage workflow:
1. use the official Mew.design `image-process` API to turn the user's photos and memories into a unified hero visual
2. use the official Mew.design `design-generate` API to compose the final invitation poster with event copy and layout

## Goal

Reuse a mew.design API key that has already been provided and validated in the current conversation whenever possible, gather event details and story assets, turn those assets into a coherent visual world, and return a finished invite poster that feels personal rather than templated.

## Workflow

1. If the user has already provided a mew.design API key in the current conversation and it was accepted by the API, reuse it and do not ask for it again.
2. Only ask for a mew.design API key if:
   - the user has not provided one yet in the current conversation
   - the last known key failed validation
   - the API returns an authentication error such as `Inactive API Key`
   - the user explicitly says they want to switch keys
3. If they do not have one yet, use this onboarding copy:

```md
没问题！为了帮你生成专属邀请海报，我需要先接入你的 mew.design API Key。

如果你还没有 Key，可以按照以下步骤获取：

1. 访问 [https://mew.design/login](https://mew.design/login) 完成注册或登录。新用户注册即送积分，可以免费创作。
2. 进入「账户设置」->「API 密钥」，点击「创建新密钥」。
3. 获取后直接把那串 Key 粘贴在这里发给我，我马上开始生成。
```

4. Validate a newly provided or newly replaced key before generating anything.
5. Collect the invitation inputs:
   - event type such as birthday, housewarming, wedding, anniversary, baby shower, or bridal shower
   - one or more public image URLs if available
   - story elements such as people, pets, home photos, couple photos, keepsakes, flowers, keys, cakes, rings, or meaningful locations
   - event title
   - optional subtitle or welcome line
   - date, time, venue, RSVP line, and optional dress code
   - desired tone such as warm, elegant, romantic, playful, festive, retro, or cinematic
   - optional explicit visual style if the user has one in mind
6. Ask for public image URLs first whenever possible.
7. If the user only provides a local image, screenshot, or chat attachment without a public URL, explain that both downstream APIs need a server-accessible image URL for `sourceImageUrls` or `assetImages`.
8. Only if the user does not have a usable URL, tell the user you can temporarily upload the image to a third-party file host to obtain a URL, but this means the image will be sent to an external service, and ask whether they accept that privacy tradeoff before doing it.
9. Choose the closest event preset:
   - `birthday`
   - `housewarming`
   - `wedding`
   - or a closely related celebration such as anniversary, engagement, or baby event
10. Choose the closest visual style preset.
11. If the user explicitly names a style, follow it.
12. If the user does not name a style, auto-match one based on the event type, tone, and story elements.
13. Run the first stage through the official Mew.design `image-process` API:
   - use the key story image or images as `sourceImageUrls`
   - preserve the identity of the people, pets, and spaces
   - unify the scene into a premium invitation-grade hero visual
   - do not add poster text in this stage
   - let the chosen style preset shape lighting, composition, and texture treatment
14. Inspect the hero visual before moving on:
   - it should still feel like the same people, pets, or home
   - it should clearly reflect the event type
   - it should look like a polished invite hero image rather than a random filter pass
   - it should clearly reflect the chosen or auto-matched style direction
15. If the transformed hero visual fails the identity or story check, retry `image-process` once with stronger preservation cues such as `preserve the same people`, `preserve the same home layout`, `preserve the same pet identity`, and `keep the same emotional tone`.
16. Run the second stage through the official Mew.design `design-generate` API:
   - use the transformed hero visual as the main `assetImages` input
   - compose a finished invitation poster with title, supporting copy, and event information
   - keep the story-driven hero visual as the emotional focal point
   - when the hero visual is a person portrait, amplify that person's temperament and make the result feel like a refined invitation editorial rather than a flyer template
   - do not let the hero visual monopolize the layout; always leave enough structured space for the essential event information
   - carry the chosen style preset through typography, composition, texture, and mood rather than only color
17. Check poster usability explicitly:
   - the title, date, venue, RSVP, and other essential event facts must remain readable
   - story subjects must not be covered by key text
   - text should sit in a dedicated text-safe area, side column, or title block
   - no text may be cut by edges, frames, or decorative elements
   - if the invite is portrait-led, it should feel elegant, flattering, and elevated rather than stiff, cheap, or over-decorated
   - different text blocks must not collide, overlap, or visually compete for the same space
   - long blessing copy or supporting copy must be condensed when needed instead of being forced into the main layout
18. If the poster is readable but still feels generic, retry `design-generate` once with stronger cues such as `story-driven invitation design`, `bespoke celebration poster`, `editorial layout`, `premium event stationery feel`, and `luxury invitation mood`.
19. Return the final poster with Markdown image syntax and one short line summarizing the event style.

## Input Rules

- Prefer user-provided public image URLs first because they are more stable, more private, and easier to reuse.
- If a mew.design API key has already been provided and successfully used in the current conversation, reuse it silently instead of asking for it again.
- Only ask for a new key when the existing one is missing, invalid, expired, deactivated, or explicitly replaced by the user.
- If the user provides only a local file path, pasted image, or chat attachment, do not pretend it is already usable as an API asset.
- Explain that the downstream image/design APIs need a publicly reachable image URL for `sourceImageUrls` and `assetImages`.
- Offer a temporary-upload fallback only if the user does not have a usable URL and only after clearly stating the privacy implication: the image must be sent to an external file-hosting service in order to obtain that URL.
- Ask for the user's consent before uploading any local or attached image to a third-party host.
- Keep the invite centered on the user's own story elements rather than replacing them with generic stock imagery.
- Keep invite copy concise enough to fit a poster layout. If the user gives too much text, compress it into a headline, one supporting line, and essential event details.
- Always prioritize the legibility of essential event facts over decorative text or long emotional copy.
- If the user provides long blessing text, vow text, welcome text, or a long invitation paragraph, summarize it into a shorter invitation-friendly version unless the user explicitly asks for full text.
- If the user does not specify a visual style, choose one automatically from the style presets below instead of asking unless the decision is unusually important.
- If the user gives no title, create one that matches the chosen celebration tone.
- If the user wants multiple event styles, generate one poster per style rather than mashing them together.

## Event Presets

- `birthday`
  Use celebration cues such as cake, candles, ribbons, confetti, florals, balloons, playful elegance, or milestone symbolism depending on age and tone. Keep the result personal rather than party-supply generic.

- `housewarming`
  Use home cues such as doorway light, keys, flowers, dining warmth, pets, table settings, windows, books, and lived-in details. Make the home feel welcoming and emotionally specific.

- `wedding`
  Use romantic cues such as vows, florals, rings, soft ceremony light, elegant wardrobe, meaningful locations, and refined typography. Keep it intimate and premium rather than bridal-template cliché.

## Style Presets

- `classic-movie-poster`
  Use cinematic composition, dramatic light, emotional color contrast, and a movie-poster sense of spectacle. Works especially well for weddings, anniversaries, and personal milestone celebrations.
  Reference direction: romantic couple under a streetlamp, dramatic blue and yellow palette, realistic credit-block structure, high-resolution cinematic atmosphere.

- `modern-minimalist`
  Use strong negative space, clean lines, restrained neutral colors, and magazine-like calm. Works especially well for housewarming invites, elegant dinners, and high-end private gatherings.
  Reference direction: one anchor object or scene, soft daylight, beige/white/sage palette, clean top area for typography.

- `creative-illustrative`
  Use colorful narrative illustration, modern editorial whimsy, and playful storytelling details. Works especially well for birthdays, pet-centered gatherings, and family parties.
  Reference direction: cozy room vignette, pet and cake details, New Yorker cover energy, vector-clean composition.

- `vintage-retro`
  Use film grain, warm nostalgic tones, candid motion, and analog-photo atmosphere. Works especially well for reunion dinners, nostalgia parties, and old-friend celebrations.
  Reference direction: 1990s candid dinner-table mood, light leaks, Polaroid feeling, retro typography.

- `scrapbook-collage`
  Use torn paper, photo fragments, tape, doodles, handwriting cues, and layered memory textures. Works especially well for growth-story birthdays, memory-rich weddings, and events with many keepsakes or mixed elements.
  Reference direction: collage board with stamps, dried flowers, washi tape, handwritten notes, layered paper feeling.

## Style Auto-Match Rules

- Default to `classic-movie-poster` for:
  - weddings
  - anniversaries
  - romantic couple invites
  - milestone personal celebrations where the user wants cinematic emotion

- Default to `modern-minimalist` for:
  - housewarming
  - high-end private dinners
  - portrait-led invites that should feel calm, refined, and expensive

- Default to `creative-illustrative` for:
  - birthdays
  - family parties
  - pet-centered gatherings
  - playful or colorful celebration tone

- Default to `vintage-retro` for:
  - old-friend reunions
  - nostalgia-themed parties
  - retro or lo-fi gathering tone

- Default to `scrapbook-collage` for:
  - growth-story birthdays
  - memory-rich weddings
  - events built around multiple photos, keepsakes, or timeline fragments

- If the user provides both a scene type and a clear emotional tone, prefer tone over event type when the two conflict.
- If the user provides many photos, handwriting-like copy, or memory fragments, bias toward `scrapbook-collage`.
- If the user provides a single strong portrait and asks for premium taste, bias toward `modern-minimalist`.
- If the user asks for “电影感”, “像海报”, “仪式感很强”, or similar wording, bias toward `classic-movie-poster`.

## Stage 1 Rules: Story Visual

- Treat the original photos as the identity anchor.
- Let the chosen style preset shape how the hero image is transformed, but never let the style erase the user's actual people, pets, home, or keepsakes.
- Preserve:
  - the same people, pets, or home
  - recognizable facial or visual identity
  - important environmental features when they carry story meaning
- Change:
  - atmosphere
  - styling
  - lighting
  - visual coherence
  - celebration mood
- Do not add invite text in stage 1.
- Do not turn the result into unrelated stock characters or a generic event illustration.

## Stage 2 Rules: Invitation Composition

- Treat the transformed story visual as a must-include hero asset.
- Reserve a dedicated text-safe area for title, subtitle, date, venue, RSVP, and optional dress code.
- Keep the hero image outside the densest text block.
- Do not let the hero image occupy so much of the canvas that the core information has nowhere clean to live.
- Build the poster around clear information hierarchy:
  - primary: title or event name
  - secondary: date, venue, school or host identity when relevant
  - tertiary: short welcome line, RSVP, or condensed blessing
- Treat the main story subjects as a hard no-text zone. Do not place text across faces, pets, rings, bouquet focus, doorway focus, or other emotionally important details.
- Decide text placement from the transformed image itself: if the hero visual occupies the center, move copy to a side column or distinct top or bottom title block with clear separation.
- Prefer structured copy containers such as a side panel, negative-space column, title cartouche, ribbon block, or paper card insert instead of floating text over the hero image.
- Use strong invitation hierarchy rather than promotional hierarchy.
- Make sure the final composition clearly reflects the chosen style preset instead of drifting into a generic mixed style.
- When the invite is portrait-led, prefer luxury editorial composition, restrained decoration, and generous breathing room.
- Avoid visual clichés that make the design feel cheap or mass-template, such as overcrowded gold ornaments, random sparkles, excessive gradient overlays, or noisy sticker-like decorations.
- If the event is a graduation banquet or another milestone with a personal portrait, prefer one of these directions:
  - light luxury magazine style
  - soft cream invitation style
  - academic ceremony style
- Let typography, spacing, and image treatment carry the elegance before adding decorative motifs.
- When information density increases, reduce decorative complexity instead of squeezing more text into the same space.
- If the event has one especially important identity field, such as school name, host name, couple names, or home name, give it a stable dedicated line or block instead of letting it float beside the portrait.
- Keep all copy away from trim edges, poster borders, and decorative frames.

## Quality Rules

- Reject the first-stage output if the people, pets, or home no longer feel like the same subjects.
- Reject the second-stage output if it looks like a template flyer, generic ad, or social post instead of a personal invitation poster.
- Reject the second-stage output if it feels visually cheap, overcrowded, or like a mass-market banquet template.
- Reject any output that ignores the user's chosen style or the skill's auto-matched style direction and falls back to a generic invitation look.
- Reject any output where text overlaps the main subjects or important story details.
- Reject any output where essential event facts are partially hidden, visually compressed, or harder to read than decorative text.
- Reject any output where text blocks overlap each other or where the hierarchy of title, date, venue, and identity fields is unclear.
- Reject any output where the story visual becomes too small to carry emotional weight.
- Reject any portrait-led invitation where the main person's temperament is flattened, obscured, or not meaningfully elevated by the design.
- Prefer elegant, readable typography.
- Keep the result celebration-specific and story-specific, not stock-like.

## Calling Guidance

For stage 1, call the official Mew.design `image-process` API directly:

```bash
curl -sS -X POST "https://api.mew.design/open/api/image/process" \
  -H "Content-Type: application/json" \
  -H "x-api-key: USER_PROVIDED_KEY" \
  -d '{
    "prompt": "Transform the provided home and family photos into a premium housewarming invitation hero visual while preserving the same people, pet, and home identity. Add warm evening light, welcoming table styling, floral accents, and editorial invitation mood. No text.",
    "sourceImageUrls": ["https://example.com/photo.jpg"],
    "aspect_ratio": "3:4",
    "image_size": "2K"
  }'
```

For stage 2, call the official Mew.design `design-generate` API directly:

```bash
curl -sS -X POST "https://api.mew.design/open/api/design/generate" \
  -H "Content-Type: application/json" \
  -H "x-api-key: USER_PROVIDED_KEY" \
  -d '{
    "userQuery": "Create a custom housewarming invitation poster using the transformed family-and-home hero image. Title: Welcome Home. Subtitle: Join us for a cozy evening in our new place. Include date, time, address, and RSVP.",
    "designConcept": "Bespoke invitation poster, editorial event layout, readable text-safe areas, premium stationery feel, warm home atmosphere.",
    "width": 1080,
    "height": 1600,
    "assetImages": [
      {
        "url": "https://example.com/transformed-hero.jpg",
        "tag": "main story-driven invite hero must appear accurately"
      }
    ]
  }'
```

## Output Standard

When the invite poster is generated successfully, respond with:

```md
![Invitation poster](https://...)

[Open original image](https://...)
```

Also include one short line saying what kind of story-driven invitation was created.

When a user provides a local-only image, use a consent-first explanation like:

```md
你这张图片现在是本地文件/聊天附件，还不是公网 URL。为了把它作为故事素材喂给生成接口，我建议你优先直接给我一个公网可访问的图片 URL，这样更稳，也更方便复用。

如果你现在没有可用 URL，我也可以先帮你临时上传到第三方文件托管，换成一个可访问的图片 URL，再拿这个 URL 去生成。

需要先说明一下：这相当于会把图片发送到外部服务。

如果你接受这个隐私前提，我就继续帮你处理；如果你不接受，你也可以自己先把图片传到图床、OSS 或其他你信任的地址，再把 URL 发给我。
```

## Resources

- Use the official Mew.design `design-generate` API for the final invitation composition stage.
