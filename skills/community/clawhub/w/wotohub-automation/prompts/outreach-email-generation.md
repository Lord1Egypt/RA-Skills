# Outreach Email Generation Prompt

Use this prompt when generating creator outreach emails with model-first behavior.

## Goal
Generate natural, low-AI-scent outreach emails for selected creators only.

## Rules
- Default language: English (`en`) unless user explicitly specifies another language.
- Match tone to creator style and signals.
- Avoid robotic phrases like "I hope this email finds you well" or overly generic praise.
- Keep subject lines short, natural, and realistic.
- Output HTML body using lightweight tags only: `p`, `br`, `strong`, `em`, `ul`, `li`, `a`.
- Do not output Markdown.
- Do not invent product facts, compensation, or deliverables.
- If a field is missing, stay conservative instead of hallucinating.

## Output JSON schema

```json
{
  "writeBackMetadata": {
    "selectedCreatorCount": 10,
    "generatedDraftCount": 10,
    "uniqueBloggerIdCount": 10,
    "missingBloggerIds": [],
    "duplicateBloggerIds": [],
    "unexpectedBloggerIds": []
  },
  "items": [
    {
      "bloggerId": "string",
      "nickname": "string",
      "language": "en",
      "style": "creator-friendly-natural",
      "subject": "string",
      "htmlBody": "<p>...</p>",
      "plainTextBody": "string",
      "styleReason": "string"
    }
  ]
}
```

## Hard constraints

- Return exactly one personalized draft per selected creator when information is sufficient.
- `bloggerId` must map to the current creator only, do not copy another creator's id.
- Do not duplicate the same full email body across multiple creators.
- `writeBackMetadata` must honestly describe the batch, not the intended batch.
