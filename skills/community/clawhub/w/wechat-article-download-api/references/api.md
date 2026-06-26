# API Reference

## Endpoint

- URL: `https://down.mptext.top/api/public/v1/download`
- Method: `GET`
- API key: not required

## Query Parameters

- `url` (required): WeChat article URL, URL-encoded.
- `format` (optional, default `html`): one of `html`, `markdown`, `text`, `json`.

## Typical Call

```bash
curl -G "https://down.mptext.top/api/public/v1/download" \
  --data-urlencode "url=https://mp.weixin.qq.com/s/EXAMPLE" \
  --data-urlencode "format=json"
```

## Response Notes

- Success usually returns HTTP `200`.
- `Content-Type` varies by format:
  - `html` -> `text/html`
  - `markdown` -> `text/markdown`
  - `text` -> `text/plain`
  - `json` -> `application/json`
