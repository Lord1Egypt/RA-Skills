---
name: wenchang-research
description: Evidence gathering for content creation. Use when a topic, outline, draft, or content_state needs sources, key facts, contrarian evidence, quote candidates, contradictions, and confidence before writing or publishing. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/wenchang-research
---

# Wenchang Research

Wenchang Research moves a topic from "sounds plausible" to "has evidence." It does not write the article.

## Inputs

- topic, angle, outline, or draft excerpt
- existing `content_state`, if available
- target platform, if known
- user-provided sources, notes, links, or examples

## Evidence Rules

1. Prefer primary sources: official docs, papers, original reports, announcements, datasets, interviews, and direct case material.
2. Avoid SEO summaries and unsupported social reposts for key claims.
3. Pair important claims with a fact, date, data point, source, or concrete case.
4. Always look for contrarian evidence, limits, or uncertainty.
5. If evidence is missing, say so and lower confidence.

## Output Format

```md
## Evidence Decision
- Support level: enough / weak / insufficient
- Main reason:

## Sources
1. <source>: <link or provided material>. <value for the article>

## Key Facts
- <fact> (source: <source>)

## Contrarian Evidence / Limits
- <limit or counterpoint>

## Quote Candidates
> <short quote or paraphrasable claim>

## Contradictions
- <source conflict or uncertainty; write "none found" if applicable>

## content_state Update
```yaml
content_state:
  research:
    sources: []
    key_facts: []
    contrarian_points: []
    usable_quotes: []
    contradictions: []
    confidence:
  next_step:
    skill:
    reason:
    user_decision_needed:
  handoff:
    from_stage: evidence
    to_stage:
    accepted_inputs: []
    ignored_context: []
    stop_condition:
```
```

## Boundaries

- Do not write the article.
- Do not change the topic unless evidence cannot support it.
- Do not skip contrarian points.
- Do not claim live facts are current without checking sources.
- If network access is unavailable, list what must be checked and set confidence to low.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
