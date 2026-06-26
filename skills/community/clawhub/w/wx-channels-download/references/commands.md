# Share Link Download Commands

Load this reference for less-common commands or when the user asks for exact
CLI syntax.

# Direct Share Link Download

This skill is scoped to no-install, no-local-proxy WeChat Channels downloads.

```bash
bash scripts/download_sph.sh "https://weixin.qq.com/sph/..."
bash scripts/download_sph.sh "https://weixin.qq.com/sph/..." "video.mp4"
WX_CHANNELS_QUALITY=h265 bash scripts/download_sph.sh "https://weixin.qq.com/sph/..." "video_h265.mp4"
```

The script:

1. POSTs the share link to `https://sph.litao.workers.dev/api/fetch_video_profile`.
2. Extracts h264 by default, or h265 when `WX_CHANNELS_QUALITY=h265`.
3. Downloads the returned media URL with `curl`.
4. Writes the file to `~/Downloads`.

## Direct Media URL

Use only when the user already has a direct `finder.video.qq.com/...` URL:

```bash
curl -fL -o "$HOME/Downloads/video.mp4" "VIDEO_URL"
```

## Out Of Scope

Do not use this skill for local proxy startup, WeChat PC button injection,
certificate installation, system proxy changes, `sudo`, Cloudflare deploy, or
remote API/RSS operations.

The older upstream CLI supports those flows, but this OpenClaw skill deliberately
does not expose them as the default path.
