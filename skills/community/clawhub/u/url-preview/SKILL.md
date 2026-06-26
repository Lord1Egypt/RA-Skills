---
name: url-preview
description: Extract and display URL previews with title, description, and favicon. Use when user shares any HTTP/HTTPS link and wants to see what the page is about without visiting it. Triggers on: (1) User sends a URL/link, (2) User asks "这个链接是什么", "看看这个网页", "what's this link"
---

# URL Preview Skill

When a user shares a URL, automatically extract and display a preview card.

## How It Works

1. User sends any HTTP/HTTPS URL
2. Use `extract_content_from_websites` tool to fetch the page
3. Parse and display: title, description, favicon, and a brief summary

## Output Format

```
🔗 [Page Title](URL)
📝 Description: ...
🌐 Site: favicon + domain
```

## Example

User sends: `https://github.com/openclaw/openclaw`

Output:
```
🔗 OpenClaw/OpenClaw
📝 An open-source AI assistant platform...
🌐 github.com
```

## Notes

- Only works on public HTTP/HTTPS URLs
- Respects rate limits - don't extract more than 5 URLs per minute
- Use `maxChars: 200` in extract_content to limit description length
