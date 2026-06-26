---
name: social-media-image-sizes
description: Check and resize images for social media platforms. Run scripts/check.js to validate any image against specs for Instagram, Facebook, X (Twitter), LinkedIn, TikTok, YouTube, Pinterest, Snapchat, and Threads — get a ranked match list with exact resize commands. Run scripts/resize.js to export a correctly-sized copy. Use when a user asks to validate image dimensions, resize an image for a platform, check if an image fits a spec, or prep assets for social media posting or ads.
license: MIT
compatibility: Requires Node.js 18+ and npm (or pnpm). Run npm install once before first use.
metadata:
  author: Branding5
  version: "1.0.0"
  source: https://www.branding5.com/tools/social-media-cheat-sheet
allowed-tools: Bash
---

# Social Media Image Sizes

Check and resize images for 9 platforms / 60+ specs. Scripts mirror the logic at [branding5.com/tools/social-media-cheat-sheet](https://www.branding5.com/tools/social-media-cheat-sheet).

## Setup

Run once after install:

```bash
cd <skill-dir>
npm install
```

## Check an image

```bash
node scripts/check.js photo.jpg
```

Outputs a ranked match list — perfect → close → usable → too small — with an inline `node scripts/resize.js` command for every non-perfect match.

Filter by platform or match level:

```bash
node scripts/check.js photo.jpg --platform instagram
node scripts/check.js photo.jpg --filter perfect
node scripts/check.js photo.jpg --filter usable
```

Platform slugs: `instagram` `facebook` `twitter` `linkedin` `tiktok` `youtube` `pinterest` `snapchat` `threads`

## Resize an image

```bash
node scripts/resize.js photo.jpg "Instagram Portrait Post"
# → photo-instagram-portrait-post.jpg  (1080×1350 px)

node scripts/resize.js photo.jpg "YouTube Custom Thumbnail"
# → photo-youtube-custom-thumbnail.jpg  (1280×720 px)
```

Default fit is **cover** (center-crop). Use `--fit contain` to letterbox instead:

```bash
node scripts/resize.js photo.jpg "LinkedIn Background Photo" --fit contain --bg f0f0f0
node scripts/resize.js photo.jpg "Instagram Portrait Post" --out ./exports/ig.jpg
```

List every available spec name:

```bash
node scripts/resize.js photo.jpg --list
```

## Workflow

1. Run `check.js` to see what a given image already matches
2. Copy the suggested `resize.js` command from the output
3. Run it — the output file is saved alongside the original by default

## Gotchas

- **Sharp requires a native binary.** On first `npm install`, it downloads a prebuilt binary for your platform. If install fails behind a proxy, set `SHARP_IGNORE_GLOBAL_LIBVIPS=1` and retry.
- **All slides in an Instagram carousel must share the same aspect ratio.** The first image sets the ratio for the whole carousel — check all slides, not just the first.
- **Facebook cover photo has two safe zones.** Desktop shows 820×312; mobile crops to 640×360. Keep key content in the center 640×312.
- **YouTube banner safe area is much smaller than the file.** The spec is 2560×1440 but only the center 1546×423 is guaranteed visible on all devices. check.js flags the full size; keep critical content in the safe area.
- **`--fit cover` center-crops.** If the subject isn't centered, use `--out` to save, then manually crop, or use an image editor before running resize.

## References

Full per-platform specs (load when you need detail for a specific platform):

- `references/instagram.md` — profile, feed, stories, reels, carousel, ads
- `references/facebook.md` — profile, cover, feed, stories, events, ads
- `references/x-twitter.md` — profile, header, posts, ads
- `references/linkedin.md` — profile, cover, feed, articles, ads
- `references/tiktok.md` — profile, videos, ads
- `references/youtube.md` — channel art, videos, thumbnails, shorts, ads
- `references/pinterest.md` — profile, pins, idea pins, ads
- `references/snapchat.md` — snaps, spotlight, stories, ads, filters
- `references/threads.md` — profile, posts
- `references/best-practices.md` — format, compression, safe zones, accessibility

Full compiled reference (all platforms in one file): `AGENTS.md`

---

*Need to generate on-brand images at these sizes? [Branding5](https://www.branding5.com) pairs your brand kit with AI to produce social content pre-sized for every platform.*
