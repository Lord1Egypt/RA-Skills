# Social Ad Templates

Short-form video templates optimized for social media platforms. All clips designed for 4-8 seconds (ideal for feeds and stories).

## Instagram/TikTok Story Ad (4s, 720x1280)
Vertical format for stories and reels.

```
Use case: social ad
Primary request: [PRODUCT/SERVICE] eye-catching vertical reveal
Scene/background: vibrant gradient or lifestyle setting
Subject: [PRODUCT] or [brand visual element] centered
Action: fast zoom-in or pop-up reveal, hold final frame 1s
Camera: vertical 9:16, dynamic motion, snappy
Lighting/mood: bright, energetic, attention-grabbing
Color palette: [BRAND COLORS], high contrast
Constraints: vertical 720x1280; max 4 seconds; no text (add in post)
Avoid: slow pacing; muted colors; horizontal framing
```

### CLI command:
```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt "Eye-catching product reveal of [PRODUCT]" \
  --use-case "social ad" \
  --scene "vibrant gradient background" \
  --camera "dynamic zoom-in, snappy" \
  --lighting "bright, energetic" \
  --size 720x1280 \
  --seconds 4
```

## LinkedIn Professional (8s, 1280x720)
Polished horizontal format for professional feeds.

```
Use case: social ad
Primary request: [PRODUCT/SERVICE] professional showcase
Scene/background: clean office or studio setting, soft bokeh
Subject: [PRODUCT] or [concept visualization]
Action: beat 1 (0-4s) product/concept enters frame; beat 2 (4-8s) settle and subtle motion
Camera: horizontal 16:9, 50mm, steady, slight push
Lighting/mood: professional, warm, trustworthy
Color palette: [BRAND COLORS], muted professional tones
Constraints: horizontal 1280x720; 8 seconds; no text overlay
Avoid: consumer-feel aesthetics; flashy effects; hand-held shake
```

## Feed Scroll-Stopper (4s, 1280x720)
Designed to stop the scroll — high impact first frame.

```
Use case: social ad
Primary request: dramatic [PRODUCT] moment that demands attention
Scene/background: high contrast, clean backdrop
Subject: [PRODUCT] in motion — falling, spinning, catching light
Action: single dramatic motion over 4 seconds, smooth slow-motion feel
Camera: 1280x720, 85mm, locked off, clean composition
Lighting/mood: dramatic, single strong light source, bold shadows
Color palette: [2-3 COLORS] high contrast
Constraints: 4 seconds; first frame must be visually striking; no text
Avoid: busy backgrounds; gentle motion; subtle effects
```

## Carousel Element (4s each, 1280x720)
Individual clips for a multi-slide carousel ad.

```
Use case: social carousel
Primary request: [FEATURE N] of [PRODUCT] — clean isolated showcase
Scene/background: consistent [COLOR] backdrop across all clips
Subject: [PRODUCT] highlighting [SPECIFIC FEATURE]
Action: simple, consistent motion (same style across all carousel clips)
Camera: same lens, same angle, same distance across all clips
Lighting/mood: consistent across all clips — match exactly
Color palette: [SAME PALETTE for all clips]
Constraints: 4 seconds each; visually consistent set; no text
Avoid: varying styles between clips; different backgrounds; inconsistent lighting
```

**Tip:** Generate all carousel clips in one session to maintain consistency. Use the same `--scene`, `--camera`, and `--lighting` flags across all clips.

## Usage Notes
- Always shoot 720x1280 for stories, 1280x720 for feeds
- 4 seconds is the sweet spot for social — shorter is better
- Generate 3-5 variants and A/B test
- Use `sora-2` for rapid iteration, `sora-2-pro` for final picks
- Add text/CTAs in your design tool, not in the video prompt
- Download immediately — URLs expire after ~1 hour
