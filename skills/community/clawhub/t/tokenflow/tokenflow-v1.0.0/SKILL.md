---
name: tokenflow
version: 2.0.0
description: "Convert files and URLs to structured text using the TokenFlow API — agent-agnostic with per-filetype configuration"
author: Iron Lion International
license: MIT
triggers: "tokenflow", "convert file", "flow this", "make it flow"
env:
  TOKENFLOW_API_KEY: "Your TokenFlow API key (from dashboard)"
---

# TokenFlow

**Name:** `tokenflow`  
**Version:** 2.0.0  
**Description:** Convert files and URLs to structured text using the TokenFlow API  
**Author:** Iron Lion International  
**License:** MIT

---

## Overview

This skill enables agents to automatically convert supported file types and URLs to structured text using the TokenFlow API. Configuration happens agent-side — edit `config.json` to set per-filetype behavior.

**Supported Platforms:** OpenClaw, Hermes

---

## Requirements

- `TOKENFLOW_API_KEY` — Your TokenFlow API key (required)
- Internet access to reach `https://tokenflow.fly.dev`

---

## Installation

### OpenClaw

```bash
openclaw skills install tokenflow
```

Or manually copy this skill directory to `~/.openclaw/skills/`.

### Hermes

Copy the `tokenflow/` skill directory to `~/.hermes/skills/`.

---

## Configuration

Edit `config.json` in the skill directory:

```json
{
  "apiKey": "your-api-key-here",
  "apiUrl": "https://tokenflow.fly.dev",
  "filetypeBehavior": {
    "docx":   { "action": "convert", "askEachTime": false },
    "xlsx":   { "action": "convert", "askEachTime": true },
    "pdf":    { "action": "convert", "askEachTime": false },
    "audio":  { "action": "convert", "askEachTime": false }
  },
  "outputFormat": "markdown",
  "maxRetries": 1,
  "fallbackBehavior": "use_file"
}
```

### Filetype Behavior

| Filetype | Extensions | `action` | `askEachTime` |
|----------|-----------|----------|---------------|
| `docx` | `.docx`, `.pptx` | `"convert"` or `"skip"` | `true` = prompt user each time |
| `xlsx` | `.xlsx`, `.xls`, `.csv` | `"convert"` or `"skip"` | `true` = prompt user each time |
| `pdf` | `.pdf` | `"convert"` or `"skip"` | `true` = prompt user each time |

| `audio` | `.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a` | `"convert"` or `"skip"` | `true` = prompt user each time |

### Options

- `outputFormat`: `"markdown"` (default) or `"html"`. Agents should use `"markdown"`.
- `maxRetries`: `0`–`3`. Retry count on failure.
- `fallbackBehavior`: `"use_file"` (use original file on failure) or `"fail"` (report error)

---

## Supported File Types

- **Documents:** `.pdf`, `.docx`, `.pptx`, `.html`, `.htm`
- **Spreadsheets:** `.xlsx`, `.xls`, `.csv`
- **Data:** `.json`, `.xml`, `.txt`, `.md`
- **Audio:** `.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a` → transcription
- **Archives:** `.zip`

---

## Agent Behavior

### On File Attachment

```
1. Check if extension is supported
   └─ No → Skip, use file as-is

2. Look up filetypeBehavior in config
   ├─ action = "skip" → Skip
   ├─ askEachTime = true and not explicit → Return shouldAsk signal
   └─ action = "convert" → Proceed

3. For XLSX: call /convert/preview to get sheet names
   └─ If multiple sheets, pass sheets="all"

4. Call TokenFlow API: POST /convert
   Headers: Authorization: Bearer {apiKey}
   Body: multipart/form-data with file + output_format=markdown

5. If success (200):
   └─ Return structured text to agent

6. If failure or empty result:
   ├─ Retries < maxRetries → Retry (step 4)
   ├─ Fallback = use_file → Use original file, log warning
   └─ Fallback = fail → Report error to user
```

### On URL Paste

1. Detect URL in user message
2. Call `POST /convert/url` with `{url: "..."}`
3. Return structured text from the webpage

---

## API Integration

### POST /convert

```bash
curl -X POST "https://tokenflow.fly.dev/convert" \
  -H "Authorization: Bearer ${TOKENFLOW_API_KEY}" \
  -F "file=@document.pdf" \
  -F "output_format=markdown"
```

**Response:** JSON with `markdown` or `html` field.

### POST /convert/preview (XLSX only)

```bash
curl -X POST "https://tokenflow.fly.dev/convert/preview" \
  -H "Authorization: Bearer ${TOKENFLOW_API_KEY}" \
  -F "file=@data.xlsx"
```

**Response:** `{"sheets": ["Sheet1", "Sheet2"]}`

### GET /health

```bash
curl "https://tokenflow.fly.dev/health"
```

### GET /usage

```bash
curl -H "Authorization: Bearer ${TOKENFLOW_API_KEY}" \
  "https://tokenflow.fly.dev/usage"
```

### POST /convert/url

```bash
curl -X POST "https://tokenflow.fly.dev/convert/url" \
  -H "Authorization: Bearer ${TOKENFLOW_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| API key invalid | Log error, use original file (if fallback=use_file) |
| Quota exceeded (429) | Report to user: "TokenFlow quota exceeded" |
| Rate limited (429) | Wait 1s, retry once if retries > 0 |
| File too large (413) | Skip conversion, use original file |
| Unsupported format (400) | Skip conversion, use original file |
| API timeout (5s) | Fail fast, use original file |
| Empty result | Treat as failure, apply fallback |

---

## Changelog

**v2.0.0** (2026-05-13)
- Agent-agnostic: supports OpenClaw and Hermes
- Configuration moved agent-side (`config.json`)
- Per-filetype behavior with `askEachTime` option
- PDFs return markdown with base64-embedded images when `outputFormat=markdown`
- Standalone image conversion removed (base64 always inflates tokens)

**v1.2.0** (2026-05-05)
- Added persistent config file
- Added automatic first-run onboarding
- Added AGENTS.md sync protocol

**v1.0.0** (2026-04-27)
- Initial release

---

## Support

- TokenFlow: https://tokenflow.ironlion.cc
- Issues: https://github.com/iron-lion-international/tokenflow/issues
