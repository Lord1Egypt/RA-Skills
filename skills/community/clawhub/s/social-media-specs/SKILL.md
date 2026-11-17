---
name: social-media-specs
description: The real limits for posting on every major social and ad platform. Caption and post lengths counted the way each platform counts (X weighting, Bluesky graphemes plus bytes, Threads emoji bytes, TikTok video vs photo), image and video sizes and aspect ratios per placement, file and duration caps, and the safe zones where app buttons cover a vertical video. Use before writing a caption, exporting a creative or scheduling a post.
license: MIT
---

# Social media specs

Use this before you write a caption, export an image or video, or schedule a post. Every number here comes from the
platform's own documentation; the full dataset with a source link per row, a counting library and a CLI is
[social-media-specs](https://github.com/hermoso-ai/social-media-specs).

If Node is available, check instead of counting by eye:

```bash
npx social-media-specs fit "<caption>"                              # every channel at once
npx social-media-specs media instagram-reel 1080x1920 --video --seconds 40
npx social-media-specs ad meta.primary-text "<ad text>"
```

## Post text

| Channel | Limit | How it counts |
|---|---:|---|
| X | 280 (25,000 with X Premium) | Links count 23; CJK characters and every emoji count 2 |
| Threads | 500, max 5 links | Each emoji counts as its UTF-8 bytes (about 4) |
| Instagram caption | 2,200, max 30 hashtags, 20 @mentions | |
| Facebook post | 63,206 | |
| LinkedIn post | 3,000 | Over-length is refused, not cut |
| Pinterest | title 100, description 800 | |
| YouTube | title 100, description 5,000 bytes, tags 500 combined | A tag with a space costs 2 extra |
| TikTok | video caption 2,200; photo post title 90, caption 4,000 | Swapping photo for video can break the caption |
| Bluesky | 300 graphemes **and** 3,000 bytes | Both apply |
| Telegram | 4,096; 1,024 once media is attached | |
| Google Business Profile | 1,500 | |

What matters more than the cap: the feed shows only the first one to three lines. **Put the point in the first line.**

## Image and video sizes

| Placement | Export at | Shape | Notes |
|---|---|---|---|
| Instagram post (app) | 1080 x 1440 | 3:4 (accepts 3:4 to 1.91:1) | Grid tiles are 3:4 |
| Instagram post (API or scheduler) | 1080 x 1350 | 4:5 to 1.91:1 | 3:4 is refused; JPEG, 8 MB |
| Instagram Story / Reel | 1080 x 1920 | 9:16 | Reels: 720 px minimum, 30 fps |
| Meta feed ad | 1440 x 1800 | 4:5 | 30 MB image, 4 GB video |
| Meta Story / Reels ad | 1440 x 2560 | 9:16 | Keep 14% top, 35% bottom, 6% sides clear |
| TikTok video | 1080 x 1920 | 9:16 | |
| TikTok In-Feed ad | 1080 x 1920 | 9:16, 16:9 or 1:1 | 540 x 960 minimum, 500 MB, 10 min |
| YouTube video | 1920 x 1080 or 3840 x 2160 | 16:9 | |
| YouTube Short | 1080 x 1920 | 9:16 or square | Up to 3 minutes |
| YouTube thumbnail | 3840 x 2160 | 16:9 | 640 wide minimum; 2 MB from a phone |
| YouTube banner | 2560 x 1440 | 16:9 | Text inside the centre 1235 x 338 (at 2048 x 1152) |
| LinkedIn image | 1080 x 1350 | 4:5 to 3:1 | 552 x 276 minimum, 5 MB |
| X image | 1080 x 1080 | 1:1, 4:5, 2:3, 16:9, 9:16, 1.91:1 | 5 MB, GIF 15 MB |
| Pinterest Pin | 1000 x 1500 | 2:3 | Taller may be cut off |

## Safe zones on vertical video

On a 9:16 frame, the apps cover roughly the top 8 to 9%, the bottom 9 to 14%, a column of buttons on the right 18 to 22%
(from about 40% down), and the caption block above the bottom bar. Keep text, faces, logos and the product in the
centre-left area. For Meta Story and Reels ads, Meta's own guidance is 14% top, 35% bottom and 6% on each side.

## Before you post

- [ ] Caption fits the strictest channel you are posting to (check X and Bluesky first; they are the tightest)
- [ ] The first line carries the point
- [ ] Media is exported at the placement's size and shape, not cropped by the platform
- [ ] Nothing important sits in a safe-zone band
- [ ] Video is within the duration and file limits
