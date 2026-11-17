# telegram-formatting

Teaches OpenClaw when and how to format Telegram replies well - real supported HTML tags plus Bot API 10.2 rich blocks (headings, tables, quotes), each live-tested and version-checked, so replies are structured without being over- or under-formatted.

## What's inside

| | |
|---|---|
| **Standard mode** | bold, italic, code, blockquote, spoiler - the tags that always work |
| **Rich mode** | headings, tables, blockquotes as native blocks - gated behind `richMessages: true`, live-tested not guessed |
| **Judgment rules** | when a message needs formatting at all, overuse/underuse tells |
| **Version safety** | test results tagged to an OpenClaw version, self-checks config before assuming what's available |

## Verified results (OpenClaw 2026.7.1-2)

| Block | Status |
|---|---|
| Heading / Table / Blockquote | Works (image-free messages only) |
| Collapsible / Checklist / Pull quote | Broken - renderer doesn't implement them |
| Slideshow / Collage | Not usable - no outbound media-group support yet |

## Use it

Drop in `~/.openclaw/workspace/skills/telegram-formatting/`, then:

```bash
openclaw skills list
```

Full rules, syntax, and reasoning: see [`SKILL.md`](./SKILL.md).
