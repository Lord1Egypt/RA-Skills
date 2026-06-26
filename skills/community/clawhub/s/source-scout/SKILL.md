---
name: source-scout
license: MIT-0
description: Use this skill for factual knowledge questions, especially random “what/where/who/how/why” questions and scientific/medical/history/current-affairs explanations. It enforces a grounded answer process: search the internet, cite reliable sources, and include a sourced image/photo/figure when useful. Trigger even when the user does not explicitly ask for sources if the answer relies on external knowledge.
---

# Source Scout

Source Scout turns quick factual answers into grounded, source-backed answers. It is designed for the everyday “random knowledge question” where answering from memory is tempting but citations and visuals make the response much more trustworthy.

## Trigger

Use this skill for factual questions such as:

- “where is…?”, “what is…?”, “why…?”, “who is…?”, “how does…?”
- science, medicine, biology, history, geography, or technical explainers
- current facts that may have changed
- any answer where citations or a visual would materially improve trust

Do **not** use for pure opinion, brainstorming, private/local memory lookup, local file/code work, or casual chat.

## Default workflow

1. **Search the web first** with the available web search tool.
   - Prefer authoritative sources: official organizations, government/NIH/NCBI/WHO, papers/reviews, textbooks, reputable institutions.
   - For scientific or medical topics, favor NCBI/PubMed/PMC, review articles, medical institutions, and official health agencies.
2. **Cross-check core claims** across at least two reliable sources when feasible.
3. **Answer concisely** in the user’s language.
4. **Cite sources** with names and URLs. Usually 2–5 sources is enough.
5. **Include a sourced image/photo/figure when useful.**
   - Prefer existing online images from Wikimedia Commons, official institutions, NCBI/PMC figures, or clearly attributed educational pages.
   - Prefer open-license or official educational images. Include attribution/licence when available.
   - If the runtime supports media attachments, download the image locally and attach the local file rather than relying on a raw external image URL.
   - Do not generate a custom image unless no suitable sourced image exists or the user explicitly wants a custom schematic.
6. **Be transparent about uncertainty.** If sources disagree or evidence is limited, say so briefly.

## Recommended output shape

Keep it compact:

- Direct answer first.
- 2–4 explanation bullets if useful.
- Image attachment or image link if useful.
- `Sources:` list with URLs.

## Image handling pattern

When an image is useful:

1. Search for a source page, not only a raw image URL.
2. Inspect the source page enough to identify attribution/licence.
3. Download the image locally if attachments are supported.
4. Verify the file type.
5. Attach the local file, and cite the source page.

Example shell pattern, when appropriate in your environment:

```bash
mkdir -p shared/artifacts
curl -L --fail '<image-url>' -o shared/artifacts/<descriptive-name>.<ext>
file shared/artifacts/<descriptive-name>.<ext>
```

## Quality bar

A good Source Scout answer should make the user feel: “this was quick, but it wasn’t hand-wavy.”

Avoid citation dumping. Prefer a few strong sources and a clear answer.
