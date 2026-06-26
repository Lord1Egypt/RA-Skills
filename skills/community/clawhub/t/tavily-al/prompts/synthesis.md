# Prompt: Synthesis

## Purpose
Write a grounded, cited answer that uses ONLY the retrieved Tavily content. The model must synthesize across sources without adding outside facts, and must surface uncertainty and disagreement instead of smoothing them over.

## Reusable prompt template
```
Write an answer to the question using ONLY the provided sources.

Question:
{{question}}

Sources (from Tavily results/extract):
{{sources_json}}   # array of {title, url, content, raw_content}

Requirements:
- Use only facts found in the sources. If the sources do not answer the question, say so.
- Attach an inline [n] citation to every factual claim.
- If sources disagree, present both positions with their citations.
- Keep it concise and directly responsive; no filler.
- Output: the cited answer, then a "Sources:" list as "[n] Title — URL".
- If confidence is low or coverage is thin, add a one-line caveat at the top.

Forbidden:
- Do NOT add facts, numbers, dates, or names not present in the sources.
- Do NOT cite a source that does not support the claim.
- Do NOT speculate or fill gaps with prior knowledge.
```

## Variables
| Variable | Description |
|----------|-------------|
| `{{question}}` | The user's question to answer. |
| `{{sources_json}}` | Retrieved content (search results and/or extracted text). |

## Example use
Give the model a question about a regulation's effective date plus two extracted sources. It should answer in 1–2 sentences, cite each fact, and if one source is ambiguous, state the uncertainty rather than guessing.

## Bad example
```
The regulation takes effect in 2026 and most experts agree it will be delayed.
```
"Most experts agree" appears nowhere in the sources (fabricated), and there are no citations.

## Good example
```
The high-risk provisions take effect on 2 August 2026 [1]. One source notes implementation guidance is still pending, so timing details may change [2].

Sources:
[1] Official Regulation Text — https://example.eu/regulation
[2] Industry Analysis — https://example.com/analysis
```

> Verification needed: confirm whether Tavily's synthesized `answer` is grounded enough to use verbatim, or should be re-synthesized from `results`, at https://docs.tavily.com
