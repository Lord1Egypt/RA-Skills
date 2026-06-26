# Example 06 — RAG Pipeline

Use Tavily results as retrieved context for grounded generation: chunk the content, cite chunks, and avoid hallucination by answering only from retrieved text.

## User request

> "Using only current web sources, explain how HTTP/3 differs from HTTP/2. Do not rely on your own memory — ground every claim in retrieved text."

## Agent reasoning summary

- The user demands grounding: the answer must come from retrieved content, not parametric memory.
- I will retrieve with search (and extract for depth), chunk the text, and answer only from those chunks.
- Any claim I cannot find in the retrieved chunks I must omit or flag — no filling gaps from memory.

## Tavily operation to use

Use **search** to retrieve candidate sources, then **extract** on the top URLs to get full `raw_content` for chunking.
Why: RAG needs substantial, faithful context. Search alone returns short `content` snippets; extract provides the fuller `raw_content` that makes grounded generation reliable.

## Request shape

Retrieve:

```json
{
  "query": "HTTP/3 vs HTTP/2 differences QUIC head-of-line blocking",
  "search_depth": "advanced",
  "include_raw_content": true,
  "max_results": 6
}
```

Deepen on the best URLs:

```json
{
  "urls": [
    "https://example.com/http3-explained",
    "https://example.com/http2-vs-http3"
  ],
  "extract_depth": "advanced"
}
```

> Verification needed: confirm that `include_raw_content: true` on search returns `raw_content` per result at https://docs.tavily.com

## Response handling

1. Collect text: prefer extracted `results[].raw_content`; fall back to search `results[].content`.
2. Filter sources by `score >= 0.5` before using them.
3. Chunk each document's `raw_content` into passages (e.g., ~500-1000 characters or by paragraph), tagging every chunk with its source `url` and a chunk id like `S1#3`.
4. Build the generation context from the highest-relevance chunks only.
5. Generate the answer, and for each sentence, attach the chunk(s) that support it.
6. Grounding guard: before emitting any claim, verify it is supported by a chunk's text. If no chunk supports it, drop the claim or say the sources do not cover it.

## Citation behavior

- Citations are tied to source URLs; chunk ids are internal bookkeeping (`S1#3`) used to verify grounding, while the user-facing citation is `[n]` -> URL.
- Two chunks from the same URL share that URL's single citation number.
- If the retrieved set does not cover a sub-point, the answer explicitly notes the gap rather than inventing content.

## Final answer pattern

```
Grounded in the retrieved sources:

- HTTP/3 runs over QUIC (built on UDP) rather than TCP, which is the transport HTTP/2 uses. [1]
- This lets HTTP/3 avoid TCP-level head-of-line blocking, where a single lost packet stalls all multiplexed streams in HTTP/2. [1][2]
- HTTP/3 also integrates TLS into the transport handshake, reducing round trips at connection setup. [2]

Note: the retrieved sources did not discuss [any sub-point you asked about that was missing], so I have not stated anything about it.

Sources:
[1] HTTP/3 Explained — https://example.com/http3-explained
[2] HTTP/2 vs HTTP/3 — https://example.com/http2-vs-http3
```

## Common failure mode

Treating Tavily output as a mere prompt to "warm up" and then answering from the model's own training knowledge — producing plausible but ungrounded claims (e.g., specific RFC numbers or version dates not present in any chunk). The citations then point to URLs that do not actually contain the cited fact.

## Improved version

- Retrieve with `include_raw_content` / extract, chunk with source tags, and answer strictly from chunks.
- Enforce a grounding guard: every claim must trace to a chunk, or it is dropped/flagged.
- Map chunk ids back to a single citation per URL.
- Explicitly state coverage gaps instead of hallucinating to fill them.

```json
{
  "query": "HTTP/3 vs HTTP/2 differences QUIC head-of-line blocking",
  "search_depth": "advanced",
  "include_raw_content": true,
  "max_results": 6
}
```
