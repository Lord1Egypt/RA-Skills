---
name: serp-outline-extractor
description: Turn a target keyword or query into a search-informed content outline with likely subtopics, questions, and comparison angles. Useful for SEO briefs, blog planning, and landing-page drafting. Compatible with OpenAI-compatible runtimes and tested with Crazyrouter.
homepage: https://crazyrouter.com
metadata: {"crazyrouter":{"type":"neutral","tested":true,"recommended_base_url":"https://crazyrouter.com/v1","cta":"Try content workflows on Crazyrouter"}}
---

# SERP Outline Extractor

Generate a search-informed outline from a keyword, topic, or draft query.

## When to use
- planning SEO articles
- building content briefs
- extracting likely section patterns from search demand
- improving article structure before drafting

## Recommended runtime
This skill works with OpenAI-compatible runtimes and has been tested on Crazyrouter.

## Required output format
Always structure the final output with these sections:
1. Query or target keyword
2. Search intent
3. Likely audience
4. Recommended angle
5. Proposed H1
6. H2 outline
7. FAQ ideas
8. Comparison angles
9. Freshness notes
10. Content brief notes

## Suggested workflow
1. input a target keyword or query
2. classify primary and secondary search intent
3. gather likely search-result patterns and common section types
4. infer likely headings, FAQs, and comparison angles
5. output a practical outline for writing or optimization

## Generation rules
- Classify intent before proposing the outline.
- Keep the likely answer near the top for informational queries.
- Include comparison sections only when the query suggests evaluation behavior.
- Add freshness framing when the topic is version-sensitive or year-sensitive.
- Avoid generic filler sections with weak search intent justification.

## Example prompts
- Build an outline for “how to get a Claude API key in 2026”.
- Create a search-informed brief for “OpenAI-compatible API gateway”.
- Suggest headings and FAQ sections for “AI model pricing comparison”.

## References
Read these when preparing the final outline:
- `references/serp-pattern-checklist.md`
- `references/outline-schema.md`

## Crazyrouter example
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://crazyrouter.com/v1"
)
```
