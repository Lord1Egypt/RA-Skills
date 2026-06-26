# tt-download troubleshooting

Load this file only when an invocation fails or the user reports a problem.
The matrix below covers every known failure mode with a one-line fix.

## Failure matrix

| Symptom (stderr message) | Likely cause | Fix |
|---|---|---|
| `未找到 <video src=...>` | Token expired, or SPA structure changed | Have the user refresh the source page and copy a fresh `video_player?token=...` URL. Tokens live ~5 minutes. |
| `Chrome 输出为空，无法解析 DOM` | Chrome crashed, page never loaded, sandbox issue | Check that Chrome runs interactively. On Linux, may need `--no-sandbox` (already set). Verify network egress to `ad.oceanengine.com`. |
| `未找到 Chrome / Chromium / Edge` | No supported browser at any default install path | Install Google Chrome or Microsoft Edge. To point at a non-default location, edit `CHROME_CANDIDATES` in `scripts/tt_download.py` (see `references/chrome-paths.json`). |
| `cc URL 返回 HTTP <code> 但没有 Location 头` | cc.oceanengine.com changed behavior, or anti-bot challenged the request | Most often: User-Agent / Referer header stripped by a proxy. The script sets both; ensure nothing in between removes them. If the response is HTML, the SPA gate may have flipped — raise a skill bug. |
| `HTTP Error 403: Forbidden` on download | vck_* cookie wasn't carried from the 302 to the GET | Shouldn't happen — `download()` accepts `cookie_str` and `resolve_video_url()` returns it. If it does, file a skill bug with the cc URL hostname and CDN error code (e.g. `X-Moat-Code`). |
| `HTTP Error 404` on download | Signed URL already expired by the time the GET went out | Re-run. If reproducible: the system clock is skewing >1 minute, fix NTP. |
| `subprocess.TimeoutExpired` | Chrome hung mid-render | Re-run; if persistent, lower `--virtual-time-budget` in `scripts/tt_download.py` or check the page for a JS infinite loop. |
| Exit code `2` | Bad CLI usage (missing/empty URL, wrong flags) | Show `--help`; ensure URL is the first positional arg. |
| `UnicodeDecodeError` in `decode("utf-8", "replace")` | Should be impossible — `replace` fallback. If seen, file a bug. | — |

## Token lifecycle

The `token=` query parameter on the input URL is a base64-encoded encrypted blob
that the SPA's JS exchanges for an `cc.oceanengine.com` short-lived permit.
Each permit:

1. Decodes the original token
2. Issues a `cc.oceanengine.com/anm/...` URL with a fresh `material_center_random` nonce
3. That URL 302s to a `video-cn.oceanengine.com` signed URL containing:
   - `dy_q=<unix-seconds>` — issue timestamp
   - `policy=<base64-json>{"vm":2,"ck":"vck_<id>"}` — which cookie must be present
   - `ft=J9ThAGkHH_Myq8Z~...` — CDN-side signature

TTL on the final URL is **300 seconds** (5 minutes) per the `vck_*` cookie's
`max-age=300`. If you save the URL and try again 6 minutes later, you'll get
`403 X-Moat-Code 4119`.

## Why headless Chrome is required

The page at `video_player?token=...`:

1. Loads `index.<hash>.js` (~56KB loader).
2. Lazy-loads chunks `42, 541, 465, 618, 110` and module `93110` (the `R` component).
3. That module makes an authenticated API call (the SPA's own session, not
   your request) to materialize the video src.
4. Renders `<video src="https://cc.oceanengine.com/anm/...">`.

No single one of those API calls can be reverse-engineered from outside
without re-implementing the SPA's session/auth/CSRF stack. Headless Chrome
sidesteps all of it by running the JS as the user's browser would.

## When yt-dlp is the right answer instead

- The URL is a regular public video page (YouTube, Bilibili, Twitter, TikTok, etc.)
- The URL is an Oceanengine **public** creative preview (not the material center)
- The user wants format selection / audio-only / subtitles

For our specific token-signed `material_center/outer/video_player` URL,
yt-dlp returns "Unable to extract video data" because there's no `<video>`
in the static HTML.
