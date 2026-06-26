# API Fallback - Tapo Camera

Use this file only when the maintained local path is not enough.

## When API Fallback Is Justified

Use an unofficial local API path only if all of these are true:
- `python-kasa` can reach the device but cannot yield a usable capture path
- RTSP or ONVIF is unsupported, disabled, or broken for the exact model
- the user still needs a local still capture
- the user approves a narrower fallback with model-specific behavior

## Why This Is A Fallback

The preferred stack is:
1. `kasa` for discovery and auth validation
2. RTSP or ONVIF on the local camera
3. `ffmpeg` or another local media tool for one-frame capture

An unofficial API is a fallback because:
- it is less stable across firmware revisions
- it may be model-specific
- it can blur the line between supported local features and reverse-engineered behavior

## Fallback Rules

- Keep the fallback on the local camera host only.
- Do not route frames through a cloud relay just to make the fallback work.
- Keep the dependency explicit and local to the user environment.
- Treat any API session token or credential blob as a secret.

## Decision Notes To Record

If the fallback is used, save:
- the exact model
- why RTSP or ONVIF failed
- what local API surface worked
- what image quality or latency trade-off the user accepted

Do not save the actual secrets or full authenticated URLs.
