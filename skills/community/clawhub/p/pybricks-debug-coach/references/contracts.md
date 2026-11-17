# Structured contract

When structured output is requested, return exactly one JSON object and no Markdown fence:

```json
{
  "schema": "debug.coach.response.v0",
  "headline": "short coach judgment",
  "evidence": ["specific evidence from the request"],
  "likelyCause": "one most likely hypothesis with uncertainty",
  "experiment": {
    "changeOneVariable": "the only variable to change",
    "howToTest": "small repeatable test procedure",
    "passCheck": "observable pass condition",
    "failCheck": "observable fail condition"
  },
  "evidenceGaps": ["smallest missing evidence to collect"]
}
```

If the caller's contract requires a `source` field, set it only to a caller-supported value. Do not claim a runtime or source that was not supplied.
