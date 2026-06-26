# Prompt: Hallucination Check

## Purpose
Audit a drafted, cited answer to confirm that every factual claim is actually supported by the cited Tavily source. Flag unsupported, miscited, or fabricated claims before the answer is delivered.

## Reusable prompt template
```
Verify that every claim in the answer is supported by its cited source.

Answer to check:
{{cited_answer}}

Sources (full content):
{{sources_json}}   # array of {title, url, content, raw_content} keyed to [n]

For each factual claim, output JSON:
{
  "claim": "<the claim text>",
  "citation": "[n]",
  "status": "supported | partially_supported | unsupported | miscited",
  "evidence": "<quote or paraphrase from the cited source, or 'none found'>"
}

Then output:
{
  "verdict": "pass | revise",
  "issues": ["<claim that must be fixed or removed>", ...]
}

Rules:
- "supported" requires the cited source to directly back the claim.
- "miscited" = the claim is true in some source but not the one cited.
- "unsupported" = no provided source backs the claim -> must be removed or re-sourced.
- Numbers, dates, and names must match the source exactly.
- Verdict is "pass" ONLY if every claim is "supported".
```

## Variables
| Variable | Description |
|----------|-------------|
| `{{cited_answer}}` | The answer with inline `[n]` citations to verify. |
| `{{sources_json}}` | Full source content mapped to citation numbers. |

## Example use
Feed a cited answer plus the extracted source texts. The check returns per-claim status; if any claim is `unsupported`, verdict is `revise` and the synthesis step must remove or re-source it.

## Bad example
```
verdict: pass
(but claim "revenue grew 40%" cites [1], which never mentions revenue)
```
Passes despite a miscited/unsupported figure — exactly what this check must catch.

## Good example
```json
{
  "verdict": "revise",
  "issues": ["'revenue grew 40%' [1] is unsupported — source [1] does not mention revenue; remove or find a source."]
}
```
With the corrected answer, every claim returns `supported` and the verdict becomes `pass`.

> Verification needed: for borderline paraphrases, prefer conservative judgments and re-check against https://docs.tavily.com guidance on source fidelity.
