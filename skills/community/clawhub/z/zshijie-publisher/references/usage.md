# Usage

## Commands

The bundled CLI uses `references/zshijie-api.json` by default, so `--contract` is optional.

Login:

```bash
python3 scripts/publisher_cli.py login \
  --session .session.json \
  --html-output /tmp/zshijie-login.html \
  --png-output /tmp/zshijie-login.png
```

Publish article:

```bash
python3 scripts/publisher_cli.py publish-article \
  --session .session.json \
  --input-json article.json
```

Edit article:

```bash
python3 scripts/publisher_cli.py edit-article \
  --session .session.json \
  --input-json article-edit.json
```

Publish video:

```bash
python3 scripts/publisher_cli.py publish-video \
  --session .session.json \
  --input-json video.json
```

Edit video:

```bash
python3 scripts/publisher_cli.py edit-video \
  --session .session.json \
  --input-json video-edit.json
```

If the publish host for the four content APIs is not the bundled default, override it:

```bash
python3 scripts/publisher_cli.py publish-article \
  --session .session.json \
  --base-url http://your-host.example.com \
  --input-json article.json
```

## Session Behavior

- `login` fetches a fresh QR code from the Z视介创作者平台, writes a local HTML file, waits for the user to scan it, then stores the extracted `sessionId` in the session file.
- Publish and edit commands automatically send the `sessionId` request header, and also include `Cookie: sessionId=...` for compatibility.
- The CLI redacts request cookies and login cookies in console output.
- QR login uses the fixed creator-platform page `https://mp.cztv.com/#/login` and the bundled QR polling config from `references/zshijie-api.json`.
- The generated QR HTML defaults to `/tmp/openclaw-zshijie-login.html`; override it with `--html-output` if needed.
- The generated QR PNG defaults to `/tmp/openclaw-zshijie-login.png`; override it with `--png-output` if needed.
- `--wait-timeout` controls how long the CLI waits for the user to scan the code.
- Intermediate QR states such as `3030` and `3032` are treated as pending states and keep polling.
- If no `sessionId` is found after a success response, the CLI fails fast and asks for a real login response sample.

## Payload Strategy

- Put the exact request body from the API docs into `--input-json`.
- The CLI forwards that JSON body directly, but always normalizes `source` to `openclaw`.
- For quick tests, you can also use repeated `--value key=value` instead of `--input-json`.
- For edit operations, `article_id` must be present in the body.
- For article edits, prefer `cover_img` as the primary cover field. If you are updating the image, also send `content`; keeping `img_array` in the payload is optional compatibility padding, not the primary update field.

## Example Payloads

Article publish:

```json
{
  "source": "openclaw",
  "section": "demo-section",
  "title": "示例动态图文",
  "img_array": [
    {
      "pic": "https://cdn.example.com/1.jpg",
      "height": 1080,
      "wide": 1920
    }
  ],
  "topic": [],
  "activity_id": "",
  "position": "",
  "at_info": [],
  "tags": "演示标签",
  "description": "演示描述"
}
```

Video publish:

```json
{
  "source": "openclaw",
  "section": "demo-section",
  "uuid": "user-id",
  "title": "示例短视频",
  "cover_img": "https://cdn.example.com/cover.jpg",
  "width": 1080,
  "height": 1920,
  "video_url": "https://cdn.example.com/demo.mp4",
  "play_time": [
    "00",
    "00",
    "30"
  ],
  "type": 7,
  "topic": [],
  "activity_id": "",
  "position": "",
  "at_info": [],
  "tags": "演示标签",
  "description": "演示描述",
  "tribe_info": []
}
```

## ClawHub

Validate the skill and print the publish command with:

```bash
python3 scripts/release_to_clawhub.py .
```

Run the actual publish only when `clawhub` is installed and logged in:

```bash
python3 scripts/release_to_clawhub.py . --execute
```
