---
name: url-shortener-mobile
description: "Guide for shortening any URL via public web services. Use whenever the user asks to shorten, abbreviate, or create a shareable link from a long URL. This skill does NOT execute HTTP itself — it instructs the agent to invoke the existing http_fetch tool, which has a different network fingerprint that bypasses the anti-bot filters that block the on-device QuickJS fetch."
triggers:
  - shorten
  - "short url"
  - "줄여"
  - "단축 url"
  - "링크 단축"
metadata:
  openclaw:
    emoji: "🔗"
---

# URL Shortener (guide)

This skill is **instructions-only**. It does not run any code on the device.
When the user asks to shorten a URL, the agent should use the existing
`http_fetch` tool to call one of the public shortener APIs below and then
return the response body as the short URL.

## Preferred backend: da.gd

**GET** `https://da.gd/s?url=<URL-encoded original URL>`

Exactly one call. Response body is the short URL as plain text (no JSON).

### Agent procedure

1. Extract the original URL from the user's message.
   - It must start with `http://` or `https://`. If not, ask the user to
     provide one.
2. URL-encode the original URL (apply `encodeURIComponent` to it).
3. Call `http_fetch` with these parameters:
   - `url`: `https://da.gd/s?url=<encoded original>`
   - `method`: `GET`
4. Take the raw response body, strip surrounding whitespace, and verify it
   starts with `https://da.gd/`. If so, return that as the short URL.
5. If the body doesn't match, or the status is not 2xx, fall back to one of
   the alternate backends below.

### Example

Original:
```
https://github.com/anthropics/claude-code/tree/main/docs/very/long/path
```

Encoded:
```
https%3A%2F%2Fgithub.com%2Fanthropics%2Fclaude-code%2Ftree%2Fmain%2Fdocs%2Fvery%2Flong%2Fpath
```

Fetch:
```
http_fetch({ url: "https://da.gd/s?url=https%3A%2F%2Fgithub.com%2Fanthropics%2Fclaude-code%2Ftree%2Fmain%2Fdocs%2Fvery%2Flong%2Fpath", method: "GET" })
```

Expected response body: `https://da.gd/XXXXXX`

## Fallback 1: cleanuri.com

**POST** `https://cleanuri.com/api/v1/shorten`

- `method`: `POST`
- `content_type`: `application/x-www-form-urlencoded`
- `body`: `url=<URL-encoded original URL>`

Response is JSON: `{"result_url": "https://cleanuri.com/XXXXXX"}`. Parse and
return `result_url`.

## Fallback 2: tinyurl.com (unreliable)

**GET** `https://tinyurl.com/api-create.php?url=<URL-encoded original URL>`

Response body is plain text like `https://tinyurl.com/XXXXXX`. Some clients
get bot-detected and receive a "deprecated preview" placeholder — if the
response body lies outside the `https://tinyurl.com/` domain or redirects
to `tinyurl.com/preview/deprecated`, treat it as a failure and move on.

## Notes for the agent

- Always verify the final short URL's domain matches the backend's own
  domain before returning it.
- If all three backends fail, tell the user honestly — do not fabricate a
  short URL.
- The user cares about reaching the original URL through the short link.
  Do not silently substitute a different destination.
