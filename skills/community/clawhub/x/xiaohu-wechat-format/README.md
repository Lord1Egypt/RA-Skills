# Xiaohu WeChat Format

OpenClaw skill adapted from `xiaohuailabs/xiaohu-wechat-format` for WeChat Official Account publishing workflows:

- Markdown / rough notes → WeChat-compatible inline-style HTML
- 33 theme previews and browser gallery
- Local/external image handling and WeChat CDN upload
- Draft-box publishing with cover image
- Optional AI cover generation and comment auto-reply helper

## Quick start

```bash
cp config.example.json config.json
# Fill wechat.app_id / wechat.app_secret when publishing drafts.

uv run --with markdown python scripts/format.py \
  --input article.md --theme newspaper --no-open

uv run --with markdown --with requests --with pillow python scripts/publish.py \
  --input article.md --theme newspaper --cover cover.jpg
```

For OpenClaw agents, read `SKILL.md` first and follow its safety rules. External writes such as draft publishing or comment auto-reply require explicit user confirmation.

## Notes

- `config.json`, tokens, and API keys must never be published.
- Add your server public IP to the WeChat Official Account IP whitelist; error `40164` means it is missing.
- Imported WeChat article images may be WebP even when named `.png`/`.jpg`; run publishing with Pillow so `publish.py` can convert them before upload.

## License

MIT, following the upstream project declaration.
