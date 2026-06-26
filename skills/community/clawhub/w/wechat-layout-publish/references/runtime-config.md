# Runtime Config

The standalone scripts in this skill accept configuration from either:

- command-line arguments
- a JSON config file
- environment variables

## Environment Variables

- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`
- `WECHAT_PROXY_ORIGIN`
- `WECHAT_AUTHOR`

## Example Config JSON

```json
{
  "appId": "wx1234567890",
  "appSecret": "your-secret",
  "proxyOrigin": "https://your-proxy.example.com",
  "author": "OpenClaw"
}
```

## Standalone Command Flow

1. normalize source content:

```bash
python3 scripts/normalize_to_markdown.py --url 'https://example.com/article' --output article.md --meta-output article.meta.json
```

2. list themes:

```bash
python3 scripts/list_themes.py
```

3. render themed HTML:

```bash
python3 scripts/render_wechat_html.py --theme w022 --input article.md --title '文章标题' --output article.wechat.html
```

4. dry-run publish payload:

```bash
python3 scripts/publish_wechat.py --html article.wechat.html --mode draft --dry-run
```

5. real publish:

```bash
python3 scripts/publish_wechat.py --html article.wechat.html --config wechat.json --mode draft
```
