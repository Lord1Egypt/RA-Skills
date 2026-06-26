# Example 01 — Basic Search

A simple factual question answered with a single Tavily search and a citation.

## User request

> "What is the capital of Australia?"

## Agent reasoning summary

- This is a single, well-defined factual question — one search is enough.
- I want a fast, low-cost call, so `search_depth: "basic"` and a small `max_results`.
- Tavily's `answer` field often resolves simple facts directly; I will still keep one supporting source to cite.

## Tavily operation to use

Use the **search** endpoint (`POST https://api.tavily.com/search`).
Why: the user asks for a fact that lives on the open web. Search returns a synthesized `answer` plus ranked `results` I can cite. Extract/crawl/map are not appropriate because the user gave no URLs.

## Request shape

HTTP call:

```http
POST https://api.tavily.com/search
Authorization: Bearer <TAVILY_API_KEY>
Content-Type: application/json
```

```json
{
  "query": "capital of Australia",
  "search_depth": "basic",
  "include_answer": true,
  "max_results": 3
}
```

Equivalent tool-call args (if invoking via a Tavily tool rather than raw HTTP):

```json
{
  "query": "capital of Australia",
  "search_depth": "basic",
  "include_answer": true,
  "max_results": 3
}
```

## Response handling

Representative response (truncated):

```json
{
  "answer": "The capital of Australia is Canberra.",
  "results": [
    {
      "title": "Canberra - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Canberra",
      "content": "Canberra is the capital city of Australia...",
      "score": 0.97,
      "raw_content": null
    },
    {
      "title": "Australia's Capital City | australia.gov.au",
      "url": "https://www.australia.gov.au/...",
      "content": "Canberra became the capital in 1913...",
      "score": 0.89,
      "raw_content": null
    }
  ]
}
```

Parsing steps:
1. If `answer` is present and non-empty, use it as the primary statement.
2. Sort `results` by `score` (descending). Keep only results with `score >= 0.5` to drop weak matches.
3. Pick the top 1 result as the citation backing the answer.
4. Deduplicate by normalized URL host+path (not needed here, but always check).

## Citation behavior

- Attach an inline marker `[1]` to the factual claim.
- Map `[1]` to the highest-scoring result's `title` and `url`.
- Do not cite the `answer` field itself — cite a concrete `results[].url`.

## Final answer pattern

```
The capital of Australia is Canberra. [1]

Sources:
[1] Canberra - Wikipedia — https://en.wikipedia.org/wiki/Canberra
```

## Common failure mode

Returning only the `answer` text with no source, or citing the synthesized `answer` as if it were a URL. This leaves the user unable to verify the claim and breaks the citation contract.

Another common mistake: requesting `search_depth: "advanced"` and `max_results: 20` for a one-line fact, wasting latency and credits.

## Improved version

- Keep `search_depth: "basic"` and `max_results: 3` for trivial facts.
- Always pair the `answer` with the single top-scoring `results[].url` as `[1]`.
- If `answer` is empty, fall back to the top result's `content` and cite it.

```json
{
  "query": "capital of Australia",
  "search_depth": "basic",
  "include_answer": true,
  "max_results": 3
}
```

```
The capital of Australia is Canberra. [1]

Sources:
[1] Canberra - Wikipedia — https://en.wikipedia.org/wiki/Canberra
```

> Verification needed: confirm exact default values for `search_depth` and `max_results` with https://docs.tavily.com
