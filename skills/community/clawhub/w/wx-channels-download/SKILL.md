---
name: wx-channels-download
description: >
  Resolve and download WeChat Channels / 微信视频号 share links directly, using the
  online sph resolver and curl. Use when the user wants no local install and no
  local proxy startup.
---

# wx_channels_download

Use this skill only for direct `https://weixin.qq.com/sph/...` share-link
resolution and download. It is intentionally scoped to the no-install,
no-local-proxy path.

Upstream: https://github.com/ltaoo/wx_channels_download

## Boundaries

- Only use this for content the user is allowed to access and download.
- Do not bypass paywalls, private access controls, account restrictions, or platform security.
- Do not start the local proxy, install certificates, change system proxy, run `sudo`, deploy Cloudflare, or use WeChat PC injection flows for this skill.
- If the user asks for WeChat PC download-button injection, say this skill does not cover that path.

## Direct Download

For a WeChat Channels share link, run:

```bash
SKILL_DIR="$(dirname "$(openclaw skills info wx-channels-download | awk -F'Path: ' '/Path:/ {print $2}' | sed 's#^~#'"$HOME"'#')")"
bash "$SKILL_DIR/scripts/download_sph.sh" "https://weixin.qq.com/sph/..."
```

Optional filename:

```bash
bash "$SKILL_DIR/scripts/download_sph.sh" "https://weixin.qq.com/sph/..." "video.mp4"
```

Use h265 when requested:

```bash
WX_CHANNELS_QUALITY=h265 bash "$SKILL_DIR/scripts/download_sph.sh" "https://weixin.qq.com/sph/..." "video_h265.mp4"
```

The script calls the online resolver at `https://sph.litao.workers.dev/api/fetch_video_profile`,
extracts `h264VideoInfo.videoUrl` by default, then downloads the returned media
URL with `curl`. Output goes to `~/Downloads`.

## Direct Media URL

If the user already gives a direct `finder.video.qq.com/...` media URL:

```bash
curl -fL -o "$HOME/Downloads/video.mp4" "<video-url>"
```

## Source Notes

Core facts are derived from upstream README, docs, and CLI source at commit
`6fc6cfec01f6ee38c40c9534ff89680fba50ca53` checked on 2026-06-08. This skill
uses the upstream online resolver endpoint and does not bundle or start the
desktop proxy binary.
