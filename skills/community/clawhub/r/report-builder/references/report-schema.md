# Report schema

Example:

```json
{
  "date": "2026-03-27",
  "summary": "7 scout signals, 4 archived cards, 7 generated ideas, 2 shortlisted ideas.",
  "reportUrl": "https://www.notion.so/example",
  "ideas": [
    {
      "id": "f1a2b3",
      "title": "Magnetic Desk Totem",
      "score": 82,
      "reason": "Strong wow moment, premium feel, and easy FDM manufacturability.",
      "notionUrl": "https://www.notion.so/example-idea"
    }
  ]
}
```

Blocked example:

```json
{
  "date": "2026-03-27",
  "summary": "Nightly report build blocked: missing OPENCLAW_NOTION_TOKEN",
  "reportUrl": null,
  "ideas": [],
  "blocker": {
    "code": "missing_env",
    "message": "Nightly report build blocked: missing OPENCLAW_NOTION_TOKEN",
    "missing": ["OPENCLAW_NOTION_TOKEN"]
  }
}
```
