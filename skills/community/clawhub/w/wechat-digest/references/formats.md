# WeChat Digest — Output Formats Reference

## One-Line Summary

Ultra-concise single line with title and key data.

```
AI 时代的写作革命 | Key: 2024 年中国 AI 写作市场规模达到 50 亿元
```

## 3-Paragraph Summary

Structured executive summary.

```
**{Title}** — Presents N key data points and N notable quotes.

Key findings include: ...

Quotes: ...
```

## Knowledge Card (JSON)

Structured data for integration with knowledge bases.

```json
{
  "title": "...",
  "type": "knowledge_card",
  "key_data": [...],
  "quotes": [...],
  "outline": [...]
}
```

## Cross-Article Synthesis

Merges multiple articles on the same topic.

```json
{
  "source_count": 3,
  "common_themes": ["theme1", "theme2"],
  "key_quotes": ["..."],
  "synthesis": "..."
}
```

## Noise Removal Patterns

The denoiser strips these common WeChat elements:

| Pattern | Description |
|---------|-------------|
| 点击.*关注 | Click-to-follow prompts |
| 长按.*二维码 | QR code scan prompts |
| 阅读原文 | "Read original" links |
| 推荐阅读 | Related reading sections |
| 版权声明 | Copyright notices |
| 底部菜单 | Bottom menu bars |
| 设为星标 | Star/favorite prompts |
