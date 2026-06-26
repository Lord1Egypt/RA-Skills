# Recipe: Answer with Sources

## Goal
Answer a user's question with a concise, grounded response that includes inline citations and a sources list, using Tavily Search (and Extract when deeper text is needed).

## When to use
- The user wants a direct answer AND wants to see where it came from.
- Accuracy and traceability matter more than speed.
- Do NOT use for pure URL extraction (`extract-and-summarize.md`) or multi-section reports (`build-research-brief.md`).

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `question` | Yes | The user's question. |
| `TAVILY_API_KEY` | Yes | From environment. Never hardcode. |
| `freshness` | No | If the question is time-sensitive, set `topic:"news"` + `time_range`. |
| `min_sources` | No | Minimum independent sources required before answering (default 2). |

## Steps
1. **Read `TAVILY_API_KEY`** from environment; abort if missing.
2. **Plan the query** (see `prompts/query-planning.md`): extract keywords, decide freshness.
3. **Search** via `POST https://api.tavily.com/search` with `include_answer:true`, `search_depth:"advanced"`, and a small `max_results` (e.g. 5).
4. **Validate status** (`401`/`422`/`429`).
5. **Rank `results` by `score`.** Keep the strongest, independent (different-domain) sources.
6. **Deepen if needed.** If snippets are insufficient for confident claims, `extract` the top 1–3 URLs for full `raw_content`.
7. **Synthesize** the answer strictly from retrieved content (see `prompts/synthesis.md`). Attach an inline `[n]` to each claim.
8. **Run a hallucination check** (`prompts/hallucination-check.md`): every claim must map to a cited source.
9. **Return** the answer with inline `[n]` citations followed by a numbered sources list.

## Output format
```
<Concise answer with inline citations like this [1], and this [2].>

Sources:
[1] Title — https://example.com/a
[2] Title — https://example.com/b
```
If confidence is low, prepend a one-line caveat about source quality.

## Example
Question: "When does the EU AI Act's high-risk provisions take effect?"
1. Search `topic:"news"`, `time_range:"year"`, `include_answer:true`.
2. Keep two reputable, independent results.
3. Answer in 2–3 sentences, each fact carrying `[1]`/`[2]`, then list both sources.

## Edge cases
- **Fewer than `min_sources` good results:** State that the answer could not be confidently sourced; do not pad with weak sources.
- **Conflicting sources:** Present the disagreement and cite both; do not silently pick one.
- **No `answer` field returned:** Synthesize from `results` yourself.
- **429:** Back off/retry; if persistent, return partial findings with a note.

## Production notes
- Always cite; an uncited claim is a defect (see `tests/failure-cases.md`).
- Prefer independent domains for corroboration over multiple pages from one site.
- Keep the answer tight; the value is the grounding, not length.
- > Verification needed: confirm `include_answer` behavior and answer quality settings with https://docs.tavily.com
