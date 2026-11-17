# Platform specs and system requirements

Checked 2026-11-02.

## What the renderer outputs

1080x1920, 30 fps, H.264, yuv420p, BT.709, AAC 48 kHz (a silent track when there's no music).
A 30-second text short is usually 3 to 10 MB. That is accepted by all three:

| | TikTok (Content Posting API) | Instagram Reels (Graph API) | YouTube Shorts |
|---|---|---|---|
| Format | MP4 recommended, H.264 | MP4/MOV, H.264, 4:2:0, AAC up to 48 kHz | Vertical or square |
| Frame rate | 23 to 60 | 23 to 60 | Any |
| Length | Up to 10 min by API, but check the account's limit | 3 s to 15 min | Up to 3 min counts as a Short |
| File size | 4 GB | 300 MB | Large |

Sources: [TikTok media transfer guide](https://developers.tiktok.com/doc/content-posting-api-media-transfer-guide),
[Instagram media reference](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media),
[YouTube Shorts length](https://support.google.com/youtube/answer/15424877).

TikTok accounts can have a shorter limit: read `maxVideoPostDurationSec` from WoopSocial's
`social_accounts_get_platform_inputs` before posting.

## Safe zones

The apps cover the top (search, tabs), the bottom (caption, username, music, progress bar) and
the right (like, comment, share). Only Meta publishes numbers: keep the top 14%, bottom 35% and
6% on each side clear
([Meta Reels ads guide](https://www.facebook.com/business/ads-guide/update/video/instagram-reels)).
TikTok publishes overlay files, not numbers, and YouTube shows its safe area only as an image;
the YouTube edges below are read from that image.

The templates use the strictest edge of the three on a 1080x1920 frame:

| Edge | px | From |
|---|---|---|
| Top | 288 | YouTube Shorts |
| Bottom | 672 | Meta and YouTube |
| Left | 96 | Meta's 65, rounded up for breathing room |
| Right | 192 | YouTube Shorts action buttons |

That leaves a text area of 792x960. Centred text uses 192 px on both sides (696 px wide), so
it sits on the frame's centre line; left-aligned scenes use the full 792. Vertically, text is
centred in the visible band between the top bar and the caption area, which is above the
frame's middle on purpose: the bottom third is covered on every app. Backgrounds and photos still fill the whole frame; only
text stays inside. The review sheet marks the safe area with a thin dashed line so you can check.

## Remotion system requirements

From [remotion.dev/docs](https://www.remotion.dev/docs/):

- Node 20 or newer (the skill's setup checks).
- macOS 15 or newer; Windows x64 (no native Windows on ARM build); Linux with glibc 2.35 or newer
  (Ubuntu 22.04+, Debian 12+). Alpine and NixOS aren't supported.
- FFmpeg is bundled. Chrome Headless Shell is downloaded on setup: 100 to 150 MB depending on the
  platform.

Linux libraries ([Remotion docs](https://www.remotion.dev/docs/miscellaneous/linux-dependencies)):

```bash
# Ubuntu 24.04 (on 22.04 use libasound2 instead of libasound2t64)
sudo apt install -y libnss3 libdbus-1-3 libatk1.0-0 libasound2t64 libxrandr2 libxkbcommon-dev libxfixes3 libxcomposite1 libxdamage1 libgbm-dev libcups2 libcairo2 libpango-1.0-0 libatk-bridge2.0-0

# Debian 12
sudo apt install -y libnss3 libdbus-1-3 libatk1.0-0 libgbm-dev libasound2 libxrandr2 libxkbcommon-dev libxfixes3 libxcomposite1 libxdamage1 libpango-1.0-0 libcairo2 libcups2 libatk-bridge2.0-0
```

## Remotion licence

Remotion isn't MIT. It's free for individuals, non-profits and companies of up to 3 people.
Companies of 4 or more need a company licence; rendering from scripts (what this skill does)
counts as automation, priced per render with a monthly minimum. Current terms:
[remotion.pro/license](https://www.remotion.pro/license). This skill's own code is MIT.
