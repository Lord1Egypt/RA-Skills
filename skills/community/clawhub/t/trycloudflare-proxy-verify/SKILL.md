---
name: trycloudflare-proxy-verify
description: Expose a local file, local folder, screenshot, or local HTTP service through a temporary trycloudflare.com tunnel and verify the public URL before sharing it. Use when a user asks for a downloadable URL to local resources, local web pages, local screenshots, local generated artifacts, or any machine-local content that should be shared externally. Always verify the final public URL yourself before returning it.
---

# TryCloudflare Proxy Verify

Use this skill whenever local content needs to be shared via a public URL.

## Rule

Never hand back a trycloudflare URL without verifying it first.

Minimum verification:

1. start the local file server or local web service
2. start the trycloudflare tunnel
3. wait until cloudflared reports a public URL
4. request the final public URL yourself
5. confirm expected HTTP status and, when practical, content type or content length
6. only then return the URL

If verification fails, do not share the URL. Retry or tell the user it is not reachable yet.

## Preferred flow

### For a single file

1. Put the file in a dedicated temp/export directory.
2. Serve that directory locally, for example with `python3 -m http.server`.
3. Start `cloudflared tunnel --url http://127.0.0.1:<port> --no-autoupdate --protocol http2`.
4. Poll logs until a `https://*.trycloudflare.com` URL appears and the tunnel registers successfully.
5. Verify with `curl -I <public-url>/<filename>`.
6. Return that verified file URL.

### For an existing local web app/service

1. Confirm the local service is reachable on localhost.
2. Start cloudflared against that localhost URL.
3. Verify the externally visible URL with `curl` before sharing.

## Important notes

- Prefer `--protocol http2` if QUIC stalls or times out.
- Keep the tunnel process alive after sharing the URL.
- If the first tunnel cannot connect, kill it and create a new one.
- For downloads, verify the exact file path, not just the site root.
- Mention that trycloudflare links are temporary.

## Resources

### scripts/
- `share_local_path.sh`: start local server, start tunnel, verify public URL

### references/
- `verification-checklist.md`: checklist for reliable URL validation
