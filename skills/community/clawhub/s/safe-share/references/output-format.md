# Output Format

Return JSON with this shape:

```json
{
  "sanitized_text": "string",
  "findings_summary": [
    {
      "type": "openai_api_key",
      "count": 1
    }
  ],
  "review_notes": [
    "Sanitization reduces risk but may miss custom identifiers."
  ]
}
```

## Field Rules

- `sanitized_text`: the shareable version of the input
- `findings_summary`: each item contains a normalized `type` and a `count`
- `review_notes`: short warnings about residual risk or ambiguous items

## Response Rules

- Do not include raw matched values in any field.
- Keep `type` values stable and machine-readable.
- Add a review note when the text looks partially sanitized already or when ambiguous identifiers remain.
