# Command Examples

## Local Headed Launch

```bash
PLAYWRIGHT_HEADLESS=0 uvx t0cksn1per run taneda \
  --size 3 \
  --release-at 11:00 \
  --newly-released-only \
  --dates 2026-05-27,2026-05-28,2026-05-29,2026-05-30,2026-05-31 \
  --exact-times "5:15 PM,7:45 PM"
```

## Node Headless Launch

```bash
PLAYWRIGHT_HEADLESS=1 uvx t0cksn1per run taneda \
  --size 1 \
  --release-at 11:00 \
  --newly-released-only \
  --dates 2026-05-27,2026-05-28,2026-05-29,2026-05-30,2026-05-31
```

## Local Headed CDP

```bash
PLAYWRIGHT_HEADLESS=0 uvx t0cksn1per run taneda \
  --size 3 \
  --release-at 11:00 \
  --newly-released-only \
  --dates 2026-05-27,2026-05-28,2026-05-29,2026-05-30,2026-05-31 \
  --exact-times "5:15 PM,7:45 PM" \
  --cdp-url http://127.0.0.1:9222
```
