# Output Format

Return a structured JSON result. Parse `choices[0].message.content` from the
API response and extract the JSON object below.

```json
{
  "summary": "brief explanation of image",
  "objects": ["detected items"],
  "text_detected": ["extracted text"],
  "ui_structure": "layout description if applicable",
  "inferred_elements": ["guessed parts"],
  "uncertainty_notes": ["what is unclear"]
}
```

| Key | Description |
|-----|-------------|
| `summary` | Brief explanation of the image |
| `objects` | Detected items / UI elements |
| `text_detected` | Extracted text strings |
| `ui_structure` | Layout description if applicable |
| `inferred_elements` | Parts guessed/inferred (must be clearly marked) |
| `uncertainty_notes` | Anything that remains unclear |
