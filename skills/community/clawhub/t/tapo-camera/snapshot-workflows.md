# Snapshot Workflows - Tapo Camera

Use this file when the user wants a real still image from a Tapo camera and the default local path should stay narrow, auditable, and reversible.

## Preferred Flow

1. Validate the camera first with `kasa`.
2. Capture one still to a local file.
3. Review the saved image locally.
4. Only then consider batch captures, retention, or downstream processing.

## Local Capture Helper

The included helper wraps the discovery and RTSP capture flow:

```bash
python3 tapo-capture.py \
  --host 192.168.1.50 \
  --output ~/tapo-camera/captures/front-door-2026-03-16T2350.jpg
```

Expected environment:
- `TAPO_CAMERA_USERNAME`
- `TAPO_CAMERA_PASSWORD`

Optional compatibility input:
- `KASA_CREDENTIALS_HASH`

The helper:
- connects through `python-kasa`
- verifies that the camera module is available
- derives the local RTSP and ONVIF surfaces
- captures one frame with `ffmpeg`
- prints a redacted summary by default

## Review Flow

After a successful capture:
- confirm the file exists
- inspect the still locally
- if the user wants agent vision on it, use the local image file rather than re-pulling the camera

Do not keep recapturing the same scene just to inspect it again.

## Safe Defaults

- Default to `stream1` for the highest-quality still unless bandwidth is a problem.
- Use a timestamped filename.
- Keep the output path explicit and local.
- Avoid printing the full RTSP URL unless the user explicitly wants it for another tool.

## When To Reveal The RTSP URL

Only reveal the full RTSP URL if the user explicitly asks for it because they want to:
- feed it into another local tool
- debug the stream with VLC or another player
- compare the derived URL against manual configuration

Even then, warn that the URL contains credentials and should not be pasted into shared logs.
