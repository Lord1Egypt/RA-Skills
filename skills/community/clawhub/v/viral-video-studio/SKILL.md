---
name: viral-video-studio
description: "Full short-form video content creation workflow for TikTok, Instagram Reels, and YouTube Shorts: analyze a reference viral video URL, reverse-engineer its viral structure using the 7 psychological triggers framework, generate AI image prompts for each scene, create a detailed shooting script with text overlays, build a posting schedule, and produce a monetization roadmap. Use when: (1) user provides a TikTok/Reels/Shorts link and wants to create similar content, (2) user wants to build a viral short video channel from scratch, (3) user needs a content calendar for channel growth, (4) user wants AI-generated image prompts for short videos, (5) user asks about making viral videos, content strategy, or growing a TikTok channel."
---

# Viral Video Studio

End-to-end workflow for cloning viral TikTok content structure and building a monetizable channel.

## Workflow Overview

```
Step 0: Define Character (once) — create character bible, fill character sheet
Step 1: Analyze reference video — download, extract frame, decode content type
Step 2: Deep Viral Analysis — 7 triggers, frame breakdown, share mechanic
Step 3: Reverse-Engineer Viral Structure — hook/setup/conflict/peak/twist/CTA
Step 4: Generate New Video Concept — same structure, new character/scenario
Step 5: Scene-by-Scene AI Image Prompts — 6 frames, Midjourney/DALL-E
Step 6: Full Script with Text Overlays — per-frame spec with sound cues
Step 7: Algorithm Optimization — completion rate, hook formulas, length strategy
Step 8: CapCut Assembly Instructions — import, timing, effects, export
Step 9: 30-Day Posting Calendar + Monetization Roadmap
```

---

## Step 0: Define Character (Do This Once)

**Before making any video**, create a Character Bible. Read `references/character-bible.md`.

Key decisions:
1. Pick archetype: Overconfident Underdog / Dignified Aristocrat / Innocent Explorer / Unlikely Professional
2. Define: species, color, signature outfit, personality, fatal flaw, motivation
3. Write a "consistency prompt prefix" — prepend to EVERY AI image prompt
4. Choose series format: single gags OR running series (series = faster follower growth)

**Output:** A completed character sheet saved to `assets/character-sheet.md`
See `assets/character-sheet-template.md` for the fill-in-the-blank template.

---

## Step 1: Analyze Reference Video

When user provides a TikTok URL:

```bash
# Download video
yt-dlp -o "/tmp/tiktok-ref.%(ext)s" "<URL>"

# Extract first frame for visual analysis
ffmpeg -i /tmp/tiktok-ref.mp4 -ss 00:00:01 -frames:v 1 /tmp/tiktok-thumb.jpg -update 1

# Try to get subtitles (may not be available)
yt-dlp --write-auto-sub --sub-lang "vi,en,zh" --skip-download -o "/tmp/tiktok-sub" "<URL>"
```

Then use the `image` tool to analyze `/tmp/tiktok-thumb.jpg` and describe:
- **Content type**: Comedy / Educational / Story / Trend
- **Format**: AI-generated images / Live action / Screen recording / Animation
- **Hook style**: Text hook / Visual hook / Sound hook
- **Pacing**: Fast cuts / Slow / Building
- **Emotion trigger**: Humor / Surprise / Curiosity / Relatability

---

## Step 2: Deep Viral Analysis

This is the most important step. Read `references/viral-analysis.md` for full protocol.

**Quick analysis (run for every reference video):**

1. **7 Triggers check** — which psychological triggers fire? (surprise, relatability, curiosity, social currency, empathy, awe, identity)
2. **Frame-by-frame breakdown** — what emotion does each moment create?
3. **The Real Why** — what universal human experience is at the core?
4. **Share mechanic** — who sends this to whom, and why?
5. **Red flags check** — does the reference video have any fail patterns to avoid?

Output a **Viral Analysis Report** (template in viral-analysis.md) before writing any script.

---

## Step 3: Reverse-Engineer Viral Structure

Decode the video into this framework:

```
HOOK (0-3s):     What stops the scroll?
SETUP (3-10s):   What's the premise?
CONFLICT (10-25s): What's the tension/challenge?
PEAK (25-35s):   What's the climax?
TWIST (35-45s):  Surprise or punchline
CTA (45-55s):    What action does it ask for?
```

Identify:
- **Character archetype**: Small vs Big / Underdog / Relatable everyman
- **Emotion arc**: Anticipation → Tension → Release → Satisfaction
- **Loop factor**: Does it make viewers rewatch? How?

---

## Step 4: Generate New Video Concept

Create a new video using the SAME structure but DIFFERENT content:

**Concept generation prompt:**
```
Based on this viral structure: [DECODED STRUCTURE]
Generate 5 new video concepts using the same emotional arc but different characters/scenarios.
Each concept: Title + Character + Scenario + Twist
Format: AI-generated image series (6 frames)
```

Pick the best concept and proceed.

---

## Step 5: Scene-by-Scene AI Image Prompts

For each of the 6 frames, write Midjourney/DALL-E prompts following this formula:

```
[Subject] [Action] [Setting] [Emotion] [Style: photorealistic/cartoon/cinematic] [Aspect ratio: 9:16 vertical]
```

**Quality modifiers to always include:**
- `photorealistic, ultra detailed, professional photography`
- `9:16 vertical format` (TikTok native)
- `dramatic lighting` or `soft natural lighting`
- `funny expression` / `shocked expression` / `confident pose`

**Consistency tip:** Start each prompt with "Same [character description]" to maintain visual consistency across frames.

> **🎀 Cute Factor:** Cute characters — chubby body, round shape, big eyes — create instant emotional investment. The cuter the character, the faster viewers bond and the harder they laugh at failures. Lean into exaggerated cuteness. See `references/character-bible.md` for the Cute Factor framework.

**Video generation options (choose by budget):**
- **Budget**: DALL-E images → CapCut slideshow (~$0.50/video)
- **Mid**: Hailuo AI video clips → CapCut (~$0.75/video)
- **Best quality**: Kling AI with character reference image (~$1-3/video)
- See `references/video-generation-tools.md` for full comparison, pricing, and all 15 Kling AI prompts for Hammy video.

See `references/prompt-templates.md` for 10 ready-to-use prompt templates.
See `references/script-templates.md` for 4 full script templates + 30 content ideas.
See `references/character-bible.md` for character archetypes, quality checklist, and emotional arc framework.
See `references/viral-analysis.md` for the 7 viral triggers, deep analysis protocol, and red flags checklist.

---

## Step 6: Full Scene-by-Scene Script

For EVERY scene (frame), specify ALL of the following in detail:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CẢNH [N] — [TIMESTAMP, e.g. 0:00-0:03]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👁️ HÌNH ẢNH (Visual):
  - Nhân vật: [Ai? Đang làm gì? Biểu cảm gì? Tư thế?]
  - Bối cảnh: [Địa điểm, ánh sáng, góc máy]
  - Chuyển động: [Static / Ken Burns zoom in / Ken Burns zoom out / Pan]
  - Chi tiết quan trọng: [Vật thể nào nổi bật? Màu sắc chủ đạo?]

🎨 DALL-E / MIDJOURNEY PROMPT:
  "[Character description], [action], [setting], [emotion], [lighting], photorealistic, 9:16 vertical"
  Negative prompt: "blurry, deformed, text, watermark"

📝 TEXT OVERLAY:
  Nội dung: "[Tối đa 6 từ + emoji]"
  Vị trí: [Top / Bottom / Center]
  Font style: [Bold white + black stroke]

🔊 ÂM THANH:
  Nhạc nền: [Tên loại nhạc / mood: sneaky / dramatic / happy / sad...]
  SFX: [Tên sound effect cụ thể: "record scratch" / "vine boom" / "sad trombone" / không có]
  Volume nhạc: [100% / 70% / 50%]

⏱️ THỜI LƯỢNG: [X giây]
🎭 CẢM XÚC MỤC TIÊU: [Người xem cảm thấy gì ở cảnh này?]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Ví dụ cảnh chi tiết:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CẢNH 1 — 0:00-0:03 (HOOK)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👁️ HÌNH ẢNH:
  - Nhân vật: Hammy (hamster béo màu cam) đứng thẳng, hai tay chống hông
    Biểu cảm: Tự tin, mắt ánh lên quyết tâm
    Tư thế: Nhìn thẳng vào camera, ngực ưỡn ra
  - Bối cảnh: Trước cổng ngân hàng khổng lồ, góc máy thấp nhìn lên
    Ngân hàng cao như tòa nhà chọc trời so với Hammy
  - Chuyển động: Ken Burns zoom out chậm để lộ kích thước ngân hàng
  - Chi tiết: Ánh nắng buổi sáng, bóng Hammy dài trên mặt đường

🎨 DALL-E PROMPT:
  "Hammy, a tiny chubby round orange hamster with big black eyes,
  wearing yellow cherry-print shorts, standing confidently arms akimbo
  in front of a massive marble bank building that towers above him,
  dramatic low angle shot, morning golden light, photorealistic, 9:16 vertical"
  Negative: "blurry, deformed, text, watermark, multiple characters"

📝 TEXT OVERLAY:
  Nội dung: "Hammy có kế hoạch 😤"
  Vị trí: Bottom 1/3
  Font: Bold white + black stroke, size lớn

🔊 ÂM THANH:
  Nhạc nền: Spy/sneaky piano theme (bắt đầu nhẹ)
  SFX: Dramatic single piano chord khi text hiện ra
  Volume nhạc: 60%

⏱️ THỜI LƯỢNG: 3 giây
🎭 CẢM XÚC: Tò mò + hào hứng — "Cái gì đây?!"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Quy tắc âm thanh theo từng loại cảnh:

| Loại cảnh | Nhạc nền | SFX gợi ý |
|---|---|---|
| HOOK | Dramatic sting / Silence → bang | Single piano chord |
| SETUP | Sneaky/spy theme | Footsteps, paper rustle |
| CONFLICT | Tension buildup | Machine hum, creaking |
| PEAK | Music STOPS → chaos | Explosion, scream |
| TWIST | Sad trombone / Magic sparkle | Record scratch, fail horn |
| CTA | Upbeat happy | Victory fanfare (mini) |

### Quy tắc hình ảnh đa frame → video:

Mỗi video = **6-15 frames ảnh AI** ghép thành video trong CapCut:
- Frame 1-2: HOOK (3-6 giây)
- Frame 3-5: SETUP + CONFLICT (10-15 giây)
- Frame 6-8: PEAK (8-10 giây)
- Frame 9-10: TWIST (5-7 giây)
- Frame 11-12: RESOLUTION + CTA (5-7 giây)

**Ken Burns effect** trên mỗi frame tạo cảm giác chuyển động dù ảnh tĩnh:
- Zoom in: tạo tension, dramatic
- Zoom out: reveal surprise
- Pan left/right: following character movement

---

## Step 7: Algorithm Optimization

TikTok ranks videos by priority order:
1. **Completion rate** — watch to the end? (most important)
2. **Rewatch rate** — watch again?
3. **Shares** — send to someone?
4. **Comments** — feel compelled to respond?
5. **Follows** — earn new followers?

**Every creative decision must serve one of these metrics.**

### Hook Formulas (First 3 Seconds — Most Critical)
```
"Stop scrolling if you [situation]"
"POV: [character] just discovered [thing]"
"Watch until the end — [teaser of twist]"
"[Bold statement]. Let me explain."
"[Number] things about [topic] nobody talks about:"
```

### Video Length Strategy
- **7-15s**: Memes, single-gag AI images → highest completion rate
- **15-30s**: Story arc (6 frames) → best balance of value + retention  
- **30-60s**: Extended story, series episode → loyal audience
- **1-3 min**: Deep dives → lower reach but higher-quality followers

### Engagement Tactics
- Reply to **every comment** in first hour → algorithm boost
- Pin the funniest comment on each video
- Create follow-up videos responding to comments
- Ask a specific question in CTA (not generic "comment below")
- Use "Part 2?" as CTA to tease continuation

---

## Step 8: CapCut Assembly Instructions

```
1. Import all AI images in order
2. Set each image duration: 3-5 seconds
3. Add Ken Burns effect (slow zoom) on each image
4. Add transition: Fade or Whip Pan between frames
5. Add text overlay per frame (match script)
6. Add background music: search "sneaky/funny/dramatic" in CapCut sounds
7. Add sound effects at TWIST frame (e.g., "record scratch", "dramatic chipmunk")
8. Export: 1080x1920, 30fps, MP4
```

---

## Step 9: 30-Day Posting Calendar + Monetization Roadmap

### Posting Calendar

See `references/posting-calendar.md` for the full template.

**Quick schedule:**
- **Week 1-2:** Post 2x/day, test 4 different content styles
- **Week 3-4:** Double down on best-performing style, post 3x/day
- **Best times (Vietnam timezone GMT+7):** 7-9 AM, 12-1 PM, 8-10 PM

**Content mix per week:**
```
3x Comedy/Story (core content)
2x Trend-riding (attach to current TikTok sounds)
1x Behind-the-scenes (how you make the AI images)
1x Engagement bait (poll, question, "guess what happens next")
```

See `references/trend-riding.md` for the full trend-riding playbook.
See `references/channel-setup.md` for new channel setup guide.

### Monetization Roadmap

See `references/monetization.md` for full details.

**Quick milestones:**
```
1K followers  → Enable TikTok Creator Fund
10K followers → Brand deals (AI tools, pet products, apps)
50K followers → Affiliate marketing ($500-2000/month)
100K+         → Sponsored content ($1000-5000/video)
```

**Fastest monetization paths for AI comedy content:**
1. **Midjourney affiliate**: 20% recurring commission — promote in bio
2. **CapCut Pro affiliate**: Promote editing workflow
3. **Merchandise**: Print-on-demand with your character designs
4. **Course**: "How I make viral AI videos" — sell for $29-99
