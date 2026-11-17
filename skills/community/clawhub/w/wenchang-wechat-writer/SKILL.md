---
name: wenchang-wechat-writer
description: Draft WeChat-style long-form articles from a confirmed topic, outline, evidence pack, or content_state. Use when the user wants title candidates, hooks, an outline, a complete article body, an ending, structural visual anchors, and follow-up topics before content review and publish packaging. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/wenchang-wechat-writer
---

# Wenchang WeChat Writer

This skill turns a confirmed topic into a WeChat-style long-form draft. It should receive a topic brief, outline, evidence pack, or `content_state`.

## Inputs

- confirmed topic or angle
- target reader
- evidence pack, if facts are important
- preferred length and tone, if provided
- existing `content_state`

If the topic is fact-heavy and has no evidence pack, route to `wenchang-research` before drafting.

## Output

1. 8-12 title candidates
2. 3-5 opening hooks
3. article outline
4. full draft
5. ending and discussion prompt
6. structural visual anchors that may deserve later illustration assessment
7. follow-up topics

## Writing Rules

- Start with a clear problem or judgment.
- Give the reader a concrete gain: judgment, method, case, checklist, or next action.
- Use evidence and examples close to the claims they support.
- Keep headings short and useful.
- Avoid generic AI-news tone, empty trend commentary, and template-heavy phrasing.
- Preserve human judgment; do not make the article sound like a generic summary.

## Output Format

```md
## Draft Brief
- Reader:
- Core angle:
- Evidence status:

## Title Candidates
1. ...

## Opening Hooks
1. ...

## Outline
1. ...

## Draft
<article body>

## Ending
<ending and discussion prompt>

## Structural Visual Anchors
- <section or mechanism that may benefit from a later illustration decision>

## Follow-up Topics
- <topic>

## content_state Update
```yaml
content_state:
  draft:
    status:
    file:
    summary:
  next_step:
    skill: wenchang-review
    reason:
    user_decision_needed:
  handoff:
    from_stage: draft
    to_stage: review
    accepted_inputs: []
    ignored_context: []
    stop_condition:
```
```

## Boundaries

- Do not invent facts to make the draft stronger.
- Do not bury missing evidence.
- Do not produce final summaries, sharing copy, tags, cover copy, or illustration plans; use `wenchang-publish-check` after review and `article-to-illustrations` after preflight.
- Do not use private account identity or private project material unless the user provides it for the current run.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
