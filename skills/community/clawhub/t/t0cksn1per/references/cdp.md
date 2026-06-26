# CDP Mode

Use CDP only when the user explicitly wants to run against an existing Chrome on their Mac.

## Start Chrome With Remote Debugging

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/tocksn1per-cdp
```

## Run The CLI Through CDP

```bash
PLAYWRIGHT_HEADLESS=0 uvx t0cksn1per run taneda \
  --size 3 \
  --release-at 11:00 \
  --newly-released-only \
  --dates 2026-05-27,2026-05-28,2026-05-29,2026-05-30,2026-05-31 \
  --exact-times "5:15 PM,7:45 PM" \
  --cdp-url http://127.0.0.1:9222
```

## Notes

- CDP is for local browser reuse, not the default path
- if Chrome is not started with remote debugging enabled, the attach will fail
- keep Playwright-managed browser launch as the fallback and default
