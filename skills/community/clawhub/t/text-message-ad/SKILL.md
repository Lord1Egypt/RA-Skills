---
name: text-message-ad
description: Create animated iMessage-style conversation ads (HTML + 1080x1920 MP4 with synthesized message sounds) for marketing and product demos. Use this skill whenever the user asks for a "text message ad", "iMessage ad", "fake text conversation" ad, a chat-style promo video, or a short vertical video ad where someone texts a friend about a product — including when they only say "make an ad for my product" or "another version for X". Also use it for the social captions that accompany these videos.
---

# Text-Message Ad Maker

Builds a short (~15s) vertical video ad styled as an iMessage conversation:
someone texts a friend about a problem, the friend recommends the product with
a link card, and the video ends on a branded end card with a CTA. Output is a
self-contained animated HTML file plus a 1080×1920 MP4 with synthesized
send/receive sounds.

**Intended use:** marketing creative and product demos only. The conversations
are fictional dramatizations between invented characters — a recognizable ad
format, not an attempt to pass off a real conversation. Never use real,
identifiable people as the characters, never present the exchange as a genuine
testimonial, and add a "Dramatization" line to the end card if a platform
requires disclosure. Do not use this skill to fabricate conversations meant to
deceive (fake evidence, impersonation, etc.).

## Workflow

### 1. Collect the brand inputs
Read `references/brand-checklist.md` and gather what it lists from the user:
logo, product name/price/domain, the customer pain point, one proof point, the
expensive alternative for the price anchor, and an accent color. It also
contains the color-theming pattern, copy voice rules, and caption formulas.

### 2. Write the conversation
7 visible messages is the sweet spot for ~15s. The canonical beat structure
(matching the template):

| Row | Type | Beat |
|---|---|---|
| 0 | out (blue) | Hook — customer states the pain |
| 1 | typing | |
| 2 | in | Friend reframes / names what's actually needed |
| 3 | in | Friend names product + price + one proof point |
| 4 | in, link card | Product link preview |
| 5 | out | Surprise / objection beat ("Wait, I can do that??") |
| 6 | typing | |
| 7 | in | Friend closes with speed/ease proof ("Took me 10 minutes 🙌") |
| 8 | out | Action beat ("Doing it now 🙏") |

Keep each bubble under ~90 characters. Follow the positive-framing rules in
`references/brand-checklist.md`.

### 3. Create the HTML
Copy `assets/template.html` (blue theme, placeholder copy in [brackets]) and
string-replace: contact name + avatar letter, timestamp, all bubble texts,
link-card preview text + meta title + domain, end-card brand name / tagline /
price anchor / CTA text, and the theme colors per
`references/brand-checklist.md`. Replace the `.logoimg` base64 data URI with
the user's logo (trimmed, on white, base64-embedded). The HTML autoplays with
a replay button — deliver it alongside the MP4 so the user can edit and
re-record later.

### 4. Render the MP4
Requirements: Playwright + Chromium, ffmpeg, Python with numpy (all present in
the Claude environment).

Write a timeline config JSON:

```json
{
  "html": "/abs/path/to/ad.html",
  "framesDir": "/home/claude/frames_myad",
  "durationMs": 15000,
  "ts": 400,
  "shows": [900, 2000, 3500, 4700, 5900, 7200, 8100, 9600, 10900],
  "hides": {"1": 3500, "6": 9600},
  "endcard": 12700,
  "rowKinds": ["send", "typ", "recv", "recv", "recv", "send", "typ", "recv", "send"]
}
```

- `shows[i]` = ms when row *i* appears (rows in DOM order). `hides` = when
  typing rows disappear (usually the moment the next bubble appears).
- These default timings work for the canonical 9-row structure; scale them if
  the conversation is longer/shorter. `endcard` ≈ last message + 1800ms;
  `durationMs` ≈ `endcard` + 2300ms.
- `rowKinds` drives the audio: `send` = outgoing swoosh, `recv` = incoming ding
  (bubbles and link cards), `typ` = soft pop, `none` = silent.

Then:

```bash
node scripts/render.js config.json          # deterministic frame stepping (audio-sync exact)
python3 scripts/make_audio.py config.json   # writes <framesDir>.wav
ffmpeg -y -framerate 30 -i <framesDir>/%04d.png -i <framesDir>.wav \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 128k \
  -shortest -movflags +faststart output.mp4
```

Why frame-stepping instead of screen recording: the renderer pauses each CSS
animation at an exact negative delay per frame, so the video timeline matches
the config exactly and the audio lands sample-accurate on every bubble.

### 5. Verify before delivering
View 2–3 frames (an early bubble, the link card, the end card) or check pixel
stats (accent-color and white-plate pixel counts) to confirm the theme and logo
rendered. Confirm MP4 specs with ffprobe (1080-wide, ~15s, h264 + aac). Deliver
both the MP4 and the HTML.

### 6. Captions (if asked, or offer)
Use the caption formulas in `references/brand.md` for YouTube (title +
description + hashtags) and Instagram (hook-beat caption + lowercase hashtags).
