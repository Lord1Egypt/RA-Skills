# Recipe: Extract and Summarize

## Goal
Given one or more known URLs, pull the full page text with the Tavily Extract API and produce a faithful, grounded summary of each page strictly from the extracted content.

## When to use
- You already have specific URLs (from a prior search or supplied by the user) and need their full text, not just snippets.
- You need to summarize, quote, or cite the actual body of a page.
- Do NOT use this to discover URLs — run `search-the-web.md` first. Do NOT use it to walk a whole site — use `crawl`/`map`.

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `urls` | Yes | A single URL or a list of URLs to extract. |
| `TAVILY_API_KEY` | Yes | Read from environment. Never hardcode. |
| `extract_depth` | No | `"basic"` or `"advanced"` (more thorough extraction of complex pages). Default `"basic"`. |

## Steps
1. **Read `TAVILY_API_KEY`** from the environment. Abort with a clear message if missing.
2. **Validate URLs.** Ensure each is a well-formed absolute `http(s)` URL. Deduplicate the list.
3. **Build the request** to `POST https://api.tavily.com/extract` with header `Authorization: Bearer <TAVILY_API_KEY>` and a JSON body `{ "urls": [...], "extract_depth": "basic" }`.
4. **Send the request** and capture the response.
5. **Check status** (`401`/`422`/`429`) before reading the body.
6. **Split results.** Read `results` (successful extractions) and `failed_results` (URLs that could not be fetched). Report failures explicitly.
7. **Summarize each successful page** using ONLY its `raw_content`. Do not add facts that are not in the text. Keep titles and source URLs attached to each summary.
8. **Retry failures once** at `extract_depth:"advanced"` if the page likely has heavy/dynamic content; if it still fails, report it as unavailable.
9. **Return** the per-URL summaries plus a list of any URLs that failed.

## Output format
The Extract API returns:
```json
{
  "results": [
    { "url": "https://example.com/a", "title": "Title A", "raw_content": "Full extracted text..." }
  ],
  "failed_results": [
    { "url": "https://example.com/b", "error": "reason" }
  ]
}
```
Your deliverable per URL: a short heading (`title` — `url`), a 3–6 sentence summary grounded in `raw_content`, and a note for any failed URL.

## Example
Request body:
```json
{
  "urls": [
    "https://example.com/quarterly-report",
    "https://example.com/press-release"
  ],
  "extract_depth": "advanced"
}
```
Expected handling: summarize each entry in `results` from its `raw_content`; if `press-release` lands in `failed_results`, state that it could not be extracted and continue with the rest.

## Edge cases
- **Some URLs in `failed_results`:** Common for paywalled, login-gated, or JS-heavy pages. Report them; never invent their contents.
- **Empty `raw_content`:** Treat as a failed extraction even if the URL is in `results`; do not summarize from nothing.
- **422:** Malformed `urls` (relative path, typo). Fix and resend; do not retry the identical bad body.
- **429:** Back off and retry a few times; batch fewer URLs per call if it persists.
- **Very long `raw_content`:** Chunk before summarizing to stay within model context; summarize chunks then merge.

## Production notes
- Batch multiple URLs in a single Extract call when possible to reduce overhead.
- Default to `extract_depth:"basic"`; escalate to `"advanced"` only for pages that fail or look incomplete (it costs more).
- Keep `raw_content` server-side/transient; do not echo entire pages back to the user — summarize.
- Always preserve the source URL with each summary so citation steps can reference it.
- > Verification needed: confirm the maximum number of URLs per Extract request with https://docs.tavily.com
