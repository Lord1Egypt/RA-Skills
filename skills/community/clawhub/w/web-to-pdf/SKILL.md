---
name: Web to PDF
description: "Convert any webpage to a clean, high-quality PDF file and send it directly. Use when the user asks to view a website, screenshot a webpage, or see a page's content. Exports the webpage using browser PDF functionality for crystal-clear results."
---

## When to Use

Use this skill when:
- User asks "let me see this website" or "show me this page"
- User requests a screenshot of a webpage
- User wants to view or save webpage content
- You need to send a webpage as a file to the user

This approach is **better than screenshots** because:
- ✅ Maximum clarity and legibility (PDF preserves all formatting)
- ✅ Preserves text, links, and structure
- ✅ Compact file format
- ✅ Professional appearance
- ✅ Easy to save, print, or share

## Workflow

### Step 1: Navigate to the URL

Use the `browser` tool to open the webpage:

```
browser action=navigate url=https://example.com
```

Wait for the page to fully load.

### Step 2: Export to PDF

Use the `browser` tool's PDF export:

```
browser action=pdf
```

This returns a file path like: `FILE:/home/user/.openclaw/media/browser/uuid.pdf`

### Step 3: Send the PDF File

Use the `message` tool to send the file directly to the user:

```
message action=send filePath=/path/to/file.pdf message="Here's the webpage as a PDF!"
```

### Step 4: Clean Up (Important!)

Delete the local PDF file immediately after sending to save space:

```
exec command=rm /path/to/file.pdf
```

Or in one line:
```
exec command=rm /path/to/file.pdf && echo "✅ PDF cleaned up"
```

## Why This Workflow

| Aspect | Why |
|--------|-----|
| PDF format | Preserves layout, fonts, colors, and links perfectly |
| Browser tool | Native PDF export ensures compatibility |
| Direct file send | User gets the file immediately, no compression artifacts |
| Cleanup step | Respects workspace storage and keeps things tidy |

## Common Patterns

### Pattern 1: User says "show me this website"

```
1. browser navigate <URL>
2. browser pdf
3. message send filePath=<result> message="Here's the website as PDF"
4. exec rm <result>
```

### Pattern 2: User asks for a screenshot

```
1. browser navigate <URL>
2. browser pdf (better than screenshot!)
3. message send filePath=<result> message="PDF view of the webpage"
4. exec rm <result>
```

### Pattern 3: Multiple pages/links

If the user wants multiple webpages:
- Repeat steps 1-4 for each URL
- Or export all to PDF in a batch script (see `scripts/batch-export.sh`)

## Error Handling

### Page fails to load

```
browser wait --url "**/expected-path" --timeout-ms 10000
```

### PDF export fails

The browser might be in headless mode or network issue. Try:
```
browser status
browser start (if not running)
browser navigate <URL>
```

### File not accessible

Check the path returned by `browser pdf`. If it's a relative path, convert to absolute:
```
exec command=realpath <path>
```

## Tips

- **For long pages**: PDF preserves entire page length, so large documents are still readable
- **For dynamic content**: Wait for dynamic content to load before exporting
- **For mobile view**: Use `browser resize 375 812` before PDF export if mobile view is needed
- **For specific sections**: Export full PDF, user can crop or extract what they need

## Related Skills

- `browser` — OpenClaw's native browser automation
- `screenshot` — Fallback if PDF export isn't suitable (rarely needed)

## Feedback & Updates

- Star this skill: `clawhub star web-to-pdf`
- Check for updates: `clawhub sync web-to-pdf`
