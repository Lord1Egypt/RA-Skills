# Prompt: Citation Generation

## Purpose
Convert a set of Tavily results into inline `[n]` citations and a matching numbered sources list, so every factual statement in an answer is traceable to a specific source.

## Reusable prompt template
```
Generate citations for the answer below using only these sources.

Draft answer:
{{draft_answer}}

Sources (from Tavily results):
{{results_json}}   # array of {title, url, content, raw_content}

Tasks:
1. Assign a stable number [1], [2], ... to each source actually used, in order of first appearance.
2. Insert inline [n] markers immediately after each factual claim, pointing to the source(s) that support it.
3. A claim supported by multiple sources may carry multiple markers, e.g. [1][3].
4. Remove from the list any source not cited in the final text.
5. Output the cited answer, then a "Sources:" list as "[n] Title — URL".

Rules:
- Do NOT cite a source that does not actually support the claim.
- Do NOT invent URLs or titles; use only what is in {{results_json}}.
- Every factual sentence must carry at least one citation.
- Keep numbering contiguous (no gaps) after pruning unused sources.
```

## Variables
| Variable | Description |
|----------|-------------|
| `{{draft_answer}}` | The synthesized answer text needing citations. |
| `{{results_json}}` | The Tavily results available as sources. |

## Example use
Provide a two-sentence draft about a product launch date and price, plus three Tavily results. The model attaches `[1]` to the date sentence and `[2]` to the price sentence, drops the unused third source, and renumbers.

## Bad example
```
The product launched in March and costs $999.

Sources:
[1] https://news.example.com
[2] (general knowledge)
[3] Some Blog — https://blog.example.com   <- never cited in text
```
No inline markers, a non-source citation, and an unused dangling source.

## Good example
```
The product launched in March 2026 [1] and is priced at $999 [2].

Sources:
[1] Official Launch Announcement — https://example.com/launch
[2] Product Pricing Page — https://example.com/pricing
```

> Verification needed: if you rely on Tavily's `include_answer` output, confirm whether it returns source attribution at https://docs.tavily.com
