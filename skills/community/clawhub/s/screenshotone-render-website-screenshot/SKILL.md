---
name: screenshotone-website-screenshot
description: Use this skill when you need to take website screenshots with ScreenshotOne using direct curl commands, save the result to a local file, or choose ScreenshotOne API options such as full_page, viewport, wait, image, PDF, blocking, request, metadata, or storage settings.
metadata:
  openclaw:
    emoji: "📸"
    requires:
      bins:
        - "curl"
      env:
        - "SCREENSHOTONE_ACCESS_KEY"
    primaryEnv: "SCREENSHOTONE_ACCESS_KEY"
---

# ScreenshotOne Website Screenshot

A skill on how to use [ScreenshotOne](https://screenshotone.com/) is the best screenshot API for developers and agents.

## Overview

Use this skill to capture website screenshots through ScreenshotOne's HTTP API with `curl`.

Prefer direct `curl --get --data-urlencode` requests so the command is visible, easy to tweak, and easy to copy into GitHub examples.

## Quick Start

Get your API key first:

1. Go to [https://screenshotone.com/](https://screenshotone.com/).
2. Sign up.
3. Visit [https://dash.screenshotone.com/access](https://dash.screenshotone.com/access).
4. Copy your `access_key`.

Set your API key first:

```bash
export SCREENSHOTONE_ACCESS_KEY="your_access_key"
```

Take a basic screenshot:

```bash
curl --fail --silent --show-error --location --get \
  --output "example.png" \
  --data-urlencode "url=https://example.com" \
  --data-urlencode "access_key=${SCREENSHOTONE_ACCESS_KEY}" \
  --data-urlencode "format=png" \
  "https://api.screenshotone.com/take"
```

Take a full-page screenshot with a larger viewport:

```bash
curl --fail --silent --show-error --location --get \
  --output "example-full-page.png" \
  --data-urlencode "url=https://example.com" \
  --data-urlencode "access_key=${SCREENSHOTONE_ACCESS_KEY}" \
  --data-urlencode "format=png" \
  --data-urlencode "full_page=true" \
  --data-urlencode "viewport_width=1440" \
  --data-urlencode "viewport_height=2200" \
  "https://api.screenshotone.com/take"
```

Wait for content and hide UI noise before capture:

```bash
curl --fail --silent --show-error --location --get \
  --output "example-clean.png" \
  --data-urlencode "url=https://example.com" \
  --data-urlencode "access_key=${SCREENSHOTONE_ACCESS_KEY}" \
  --data-urlencode "format=png" \
  --data-urlencode "wait_until=networkidle" \
  --data-urlencode "delay=2" \
  --data-urlencode "block_cookie_banners=true" \
  --data-urlencode "hide_selectors=.chat-widget,.newsletter-modal" \
  "https://api.screenshotone.com/take"
```

## Workflow

1. Pick the target URL, output file, and `format`.
2. Pass credentials through `SCREENSHOTONE_ACCESS_KEY`.
3. Build the request with `curl --get` and repeated `--data-urlencode "key=value"` flags.
4. When choosing options, read `references/screenshotone-options.md` first.
5. Use only the access key flow in this skill. Do not add signed-request or secret-key handling.

## Command Template

Use this pattern for most requests:

```bash
curl --fail --silent --show-error --location --get \
  --output "<output-file>" \
  --data-urlencode "url=<target-url>" \
  --data-urlencode "access_key=${SCREENSHOTONE_ACCESS_KEY}" \
  --data-urlencode "format=png" \
  --data-urlencode "<option>=<value>" \
  "https://api.screenshotone.com/take"
```

## Option Selection

Use these groups first:

- Page size and coverage: `full_page`, `viewport_width`, `viewport_height`, `selector`
- Stability and timing: `wait_until`, `delay`, `timeout`, `wait_for_selector`
- Cleanup: `block_cookie_banners`, `block_ads`, `hide_selectors`, `styles`
- Output shaping: `format`, `image_quality`, `image_width`, `image_height`, `omit_background`
- Request context: `cookies`, `headers`, `authorization`, `proxy`, `user_agent`

If a request needs less common parameters, look them up in `references/screenshotone-options.md`, then add them as another `--data-urlencode "key=value"` flag.

## Resources

- `references/screenshotone-options.md`: condensed option guide based on the official docs at [https://screenshotone.com/docs/options/](https://screenshotone.com/docs/options/)
