---
name: web-to-md
description: "Extracts readable markdown from user-provided URLs via a deterministic fallback chain (markdown.new → r.jina.ai). Use when the user supplies specific URLs and wants reliable extraction, summarization, or analysis."
version: 1.0.0
author: chdlc
license: MIT-0
metadata:
  openclaw:
    requires:
      bins: ["curl"]
  hermes:
    tags: [web, extraction, markdown, url, content]
    related_skills: [use-tinyfish, browser-automation]
    category: utility
---

# Web to Markdown

Deterministic, console-first extraction workflow for user-provided URLs. Enforces a fixed fallback chain to maximize content quality without open-ended browsing.

## When to Use

- The user provides one or more **specific URLs**.
- The task requires reading, extracting, summarizing, or analyzing those URLs.
- A deterministic fallback order is preferred over open-ended browsing.

**Do not use** for open-ended web discovery unless the user explicitly asks for discovery first.

## Fallback Chain

For each URL, attempt in order. Stop at the first sufficient result.

### 1. markdown.new (AI mode)

```bash
curl -s "https://markdown.new/{URL}?method=ai"
```

### 2. markdown.new (Auto mode)

Only if step 1 is insufficient or timed out:

```bash
curl -s "https://markdown.new/{URL}?method=auto"
```

### 3. r.jina.ai (Browser engine)

Only if steps 1–2 are insufficient or timed out:

```bash
curl -s "https://r.jina.ai/{URL}" -H "X-Engine: browser"
```

### 4. Agent tools (last resort)

If all three prefixes fail, report the failure and fall back to the agent's own extraction tools. This is outside the skill's chain — acknowledge it as a fallback.

## Quality Gate

After each step, content is **insufficient** when any condition is true:

- Main article or body text is missing
- Content is clearly truncated
- Output is mostly navigation, boilerplate, placeholders, or login walls
- Useful text is too short for the task
- Important sections requested by the user are absent

**Rule of thumb:** Under ~1,200 useful characters for an article page is almost certainly truncated. Naturally short pages (announcements, status updates) may be legitimately brief — use judgment.

## URL Handling

- Preserve the protocol when present.
- Ensure the URL is shell-safe and **quoted** in all curl commands.
- Process each URL independently when multiple are provided.

## Provenance Reporting

Report exactly one final source label per extracted URL in your response:

| Label | When |
|---|---|
| `markdown.new:ai` | method=ai was sufficient |
| `markdown.new:auto` | method=auto was sufficient (ai failed) |
| `r.jina.ai` | r.jina.ai was sufficient (both markdown.new failed) |
| `agent-tools` | All three prefixes failed; agent used own tools |

## Workflow

1. **Scope gate** — Only process URLs explicitly provided by the user. If discovery is needed, use web search first and confirm candidate URLs before extraction.
2. **Normalize** — Quote URLs, preserve protocol.
3. **Extract** — Run the fallback chain per URL.
4. **Quality gate** — Check each result against the insufficiency conditions.
5. **Continue** — Use the richest sufficient source for the task.
6. **Report** — Include provenance labels in the final response.

## Best Practices

- Keep extraction deterministic — explicit fallback transitions, state why each happened.
- Prefer reproducible commands with quoted URLs.
- Conservative timeout handling: continue immediately to the next fallback when blocked.
- Preserve source traceability via provenance labels.
- Avoid tool-specific assumptions beyond curl and standard HTTP endpoints.

## Edge Cases

- **Page blocks automated access:** Skip to next fallback immediately.
- **Multiple URLs:** Apply the same sequence to each independently.
- **Naturally short pages:** Accept shorter content when it satisfies the request.
- **All prefixes fail:** Report failure clearly, then use agent tools as last resort.

## Common Pitfalls

1. **Output format must be markdown.** If any level returns raw HTML or another format, it breaks the contract. Test each level independently.
2. **Don't skip testing lower fallback levels** just because the top level works. A chain is only as reliable as its weakest link.
3. **Quality is subjective** — the 1,200-char heuristic is a guideline, not a hard rule. Apply judgment for short-form content.

## Verification Checklist

- [ ] curl is installed (`which curl`)
- [ ] Extraction starts with `markdown.new?method=ai`
- [ ] `method=auto` is tried only after ai fails
- [ ] `r.jina.ai` is tried only after both markdown.new attempts fail
- [ ] All three prefixes failing → report + fall back to agent tools
- [ ] Quality checks include: missing body, truncation, boilerplate, too-short content
- [ ] Final response includes provenance label per URL
