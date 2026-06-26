# Default Layout System

The visual system when the user picks "default" in Step 1 (or doesn't tell you — this is the implicit default). Co-designed with Monica on the DeltaStream campaign and validated as the production-ready output of this skill.

**This is one of two modes** the skill operates in:
- **Default** (this file) — clean, restrained, every screen the same composition skeleton. **This is what the skill produces well.**
- **Replicate a reference** (whatever the user supplies) — extract the reference's compositional rules, adapt to the user's brand. See `references/layout-archetypes.md` for examples of patterns the user might point at.

If the user supplies a reference, study that instead and extract its rules. This file is the default fallback.

---

## The composition (one template, varied per screen)

Each of the 6 screens uses the same skeleton — vary the color, the headline, and the device content. Variety comes from the brand palette rotation and the natural difference between app screens, not from layout gymnastics.

```
1290 × 2796 canvas
┌────────────────────────────────┐
│                                │  ← top padding ~140px
│   [optional brand mark]        │
│                                │
│   Headline goes here.          │  ← 120-140px Funnel Display 800
│   Sub line if needed.          │  ← 36-40px Hanken Grotesk 500
│                                │
│      ┌──────────────────┐      │
│      │                  │      │
│      │                  │      │  ← Device: 1000px wide
│      │   App screen     │      │      (~78% of canvas)
│      │   from Figma     │      │      Anti-aliased rounded corners
│      │                  │      │      Soft drop shadow
│      │                  │      │
│      │                  │      │
│      └──────────────────┘      │
│                                │  ← bottom padding ~80-120px
└────────────────────────────────┘
```

## Exact specs

### Stage
- `1290 × 2796` px, `overflow: hidden`, single solid-color background

### Top zone (y ≈ 110 to 600)
- Optional small brand mark at y ≈ 110, ink or brand color, ~44-56px tall, paired with brand wordmark in tracked caps (20-22px, letter-spacing 0.28-0.32em, opacity 0.55)
- Headline starts y ≈ 200, centered. Funnel-Display-class (or whatever the brand's display face is) at weight 800
  - Size: 120-144px (don't push past 150; that's where it starts competing with the device)
  - Line-height: 0.88-0.92
  - Letter-spacing: -0.04 to -0.045em
  - Color: ink (#1C1A18 in DeltaStream) on light bg; cream (#FAF5EC) on dark bg
- Subhead 24-32px below headline. Body sans at weight 500
  - Size: 36-40px
  - Line-height: 1.3
  - Opacity: 0.7-0.75 of the headline color
  - Letter-spacing: -0.005 to -0.01em

### Device zone (y = 580 to 2748)
- Width: **1000px** (~78% of canvas).
- Height: derived from aspect — for iPhone 15/16 Pro source (393×852), `width × 852/393 = 2168px`.
- Position: `top: 580px; left: 50%; transform: translateX(-50%);` — bottom lands at y=2748, leaving 48px breathing room at the canvas edge.
- **Pick one: bleed OR full-frame. Never mid-crop the bottom curve.** The default is full-frame (top: 580): rounded bottom corners fully visible inside the canvas. If you want a bleed-off-bottom variant for drama (e.g. the hook screen), push `top` to ≥ 819 so the bottom curve is entirely past y=2796 (since the bottom curve is ~191px tall at radius=75 source / width=1000 display). Anything in between produces an ugly half-cut curve where the canvas slices through the rounded corner mid-arc.
- Drop shadow: `filter: drop-shadow(0 80px 100px rgba(28,26,24, 0.18))` on light bg; bump alpha to 0.28-0.40 on darker bg.
- **No CSS `border-radius` needed if the source has been cleaned** (see `render-pipeline.md` → "Cleaning Figma source PNGs"). The cleaned PNG's anti-aliased mask carries the corners.
- Optional slight tilt: `transform: translateX(-50%) rotate(-3deg)`. Use sparingly — at most one screen per campaign.

### Color rotation across 6 screens

Don't repeat the same background on adjacent screens unless deliberate. A good DeltaStream sequence: `butter / cream / butter / cream / plum / butter`. The plum break in position 5 gives one tonal moment of drama without overusing depth color.

For any brand:
- Primary brand color = dominant (3-4 screens)
- Secondary/cream/neutral = supporting (2-3 screens)
- Accent/depth color = once, usually positions 4-5 (the "wow" or "proof" moment)
- Never invent a color not in the brand palette

## Variation knobs (use sparingly)

The default is **same template, different color + content per screen**. If a campaign needs more variation, add ONE of these per screen — never more than one:

1. **Slight device tilt** (-3 to -5deg). Best on the WOW screen or the close.
2. **Small brand mark above headline.** Best on the HOOK screen (sets the brand stamp).
3. **Wordmark at the bottom.** Best on the close (signs off).
4. **Tracked-caps tagline** below the device. Best on connections/feature screens that need a one-line claim ("— CONTEXT, KEPT CURRENT").

Anything more — generated lifestyle photos, parallax shapes, quote cards — should only enter the campaign if the user explicitly wants more drama or supplies a reference that demands it.

## What this system is NOT

- **Not parallax.** Big shapes floating behind devices look great in mockups, terrible at App Store thumbnail scale. Skip.
- **Not full-bleed UI.** Showing the screenshot at canvas size without a device frame works on paper but reads as "a poster" not "an app." Skip unless you have the source app's UI designed to bleed.
- **Not side-by-side device + photo.** Tried it, devices get small (≤ 560px wide), violates the "device is the hero" rule.
- **Not quote cards.** No fabricated press quotes by default. If the user has real proof to feature, add it as a tracked-caps tagline on a feature screen, not a dedicated screen.
- **Not SVG iPhone bezels.** See `render-pipeline.md`.

## The squint test (apply before delivering)

1. **Contact sheet at 25%.** Each screen still readable? Headlines legible? Devices distinct? If any screen disappears at thumbnail size — the focal element is wrong.
2. **Cover the device.** Does the surrounding design still feel like the brand (color, type, voice in copy)? If not, the screen is generic.
3. **Cover the headline.** Can you tell what the app does just from the device + color choice? If not, the visual hierarchy is wrong (device should carry the story; copy supports).
