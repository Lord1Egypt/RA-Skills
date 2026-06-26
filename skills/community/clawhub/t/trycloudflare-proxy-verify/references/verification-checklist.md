# Verification Checklist

Before sharing a trycloudflare URL, check all of these:

1. Local origin responds successfully.
   - Example: `curl -I http://127.0.0.1:8765/file.zip`
2. `cloudflared` logs show a generated `https://*.trycloudflare.com` URL.
3. `cloudflared` logs show the tunnel actually registered successfully.
   - Example: `Registered tunnel connection ... protocol=http2`
4. The exact public URL responds successfully.
   - Example: `curl -I https://example.trycloudflare.com/file.zip`
5. Response matches expectation.
   - Correct status code
   - Expected content type if relevant
   - Expected content length if relevant

If any step fails, do not send the URL yet.

## Common failure pattern

A quick tunnel URL may be printed before the edge connection is healthy. That URL is not ready to share until you have verified it yourself.

## Reliable flags

When QUIC is flaky, use:

```bash
cloudflared tunnel --url http://127.0.0.1:PORT --no-autoupdate --protocol http2
```
