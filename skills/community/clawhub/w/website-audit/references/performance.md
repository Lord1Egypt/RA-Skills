# Performance checks

**Scripts:** `check_html.py` reports static indicators only (compression, render-blocking scripts, image dimensions, third-party hosts, HTML size); `check_headers.py` reports Cache-Control and Content-Encoding. `check_rendered.py` (Tier C) measures Core Web Vitals in the lab via Lighthouse. Without Tier C or field data, write "Not measured".

## Core Web Vitals (C, or external data)
Targets at the 75th percentile: **LCP 2.5s or less, INP 200ms or less, CLS 0.1 or less**.
- Prefer field data (Chrome UX Report, PageSpeed Insights) over lab data. Lab data (Lighthouse) is a useful proxy but varies by run and device profile.
- If you cannot measure, write **Not measured**. Do not estimate Core Web Vitals from HTML.

## Lab measurements via check_rendered.py (C)
One Lighthouse run, emulated device (mobile by default, `--preset desktop` for desktop), categories performance + accessibility. Numbers are copied from the Lighthouse report; the script never estimates.
- **LCP**: issue `cwv.lcp_slow` — medium over 2.5s, high over 4.0s.
- **CLS**: issue `cwv.cls_high` — medium over 0.1, high over 0.25.
- **INP**: issue `cwv.inp_slow` when Lighthouse returns a value (medium over 200ms, high over 500ms). Lab runs usually return none; the output then carries `inp_note` saying INP was **not measured**, and Total Blocking Time is reported instead as a labelled proxy (`cwv.tbt_high`, low over 200ms, medium over 600ms). Never present TBT as INP.
- All rendered findings carry confidence `likely`: one lab run is evidence, not a verdict. If the report matters, run twice and say both numbers.
- A failed run (no Chrome, interstitial, timeout) comes back as `not_checked` with Lighthouse's own error quoted — list it under "What was not checked", never as a pass.
- Behind a proxy, the script passes the environment's proxy to Chrome (value never printed) and `--ignore-cert-errors` is available as an explicit opt-in; when used, the output says so, and TLS findings still belong to `check_headers.py`.
- **Credentialled proxies:** Chrome rejects any `--proxy-server` value that embeds credentials (`net::ERR_NO_SUPPORTED_PROXIES`), and a credential-free value gets a 407. If the environment's proxy needs embedded auth, run a tiny local relay that injects the `Proxy-Authorization` header toward the upstream proxy and listens on loopback without auth, then pass `--proxy-server http://127.0.0.1:<port>`. A TLS-intercepting proxy additionally needs `--ignore-cert-errors` (labelled, see above). A reference relay implementation pattern: read the upstream proxy URL from the environment at runtime, keep the credential in memory only, bind 127.0.0.1 only.

## Static indicators (A or B)
These are signals, not metrics. Label them as indicators.
- **Compression** (B): HTML/CSS/JS served with gzip or brotli.
- **Caching** (B): long `Cache-Control` on fingerprinted static assets; sensible policy on HTML.
- **Render-blocking resources** (A): scripts in `<head>` without `async`/`defer`; large CSS loaded synchronously.
- **Images**: oversized files, legacy formats where WebP/AVIF would fit, missing `width`/`height` (layout shift risk), missing `loading="lazy"` below the fold, hero image wrongly lazy-loaded.
- **Fonts**: `font-display` set; number of font files; preconnect for font hosts.
- **Third parties**: count and weight of tags, analytics, chat widgets, embeds. Name the heaviest.
- **Page weight and request count** (B): report the numbers you measured, with the page and conditions.

## Reporting
Say what was measured, where, and how (tool, device profile, lab vs field). One slow lab run is not a conclusion; mention variance.
