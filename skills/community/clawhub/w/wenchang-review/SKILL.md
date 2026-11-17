---
name: wenchang-review
description: Diagnose or edit an existing content draft. Use when the user has a draft and wants to know whether it is publishable, needs light edits, needs a full chapter edit, should be rewritten, should switch platforms, or should be dropped. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/wenchang-review
---

# Wenchang Review

Wenchang Review evaluates whether a draft deserves more work and what the smallest useful next action is.

## Modes

Default to diagnosis mode. Use full-edit mode only when the user explicitly asks to edit, rewrite, cut, polish, or produce a publishable version.

### Diagnosis Mode

Return issues and minimum fixes. Do not rewrite the full article.

### Full-Edit Mode

Return an edited draft after diagnosing. Prioritize:

1. argument strength
2. evidence near claims
3. reader value
4. readable structure
5. clean prose

## Diagnosis Dimensions

- core problem clarity
- structure and flow
- reader gain
- evidence and examples
- human judgment and specificity
- platform fit
- long-term asset value
- risks: empty trend talk, tool manual tone, overpromised title, unsupported claims

## Diagnosis Output

```md
## Review Decision
- Recommended action: publish / light edit / full edit / rewrite / switch platform / stop investing
- Main reason:

## Key Issues
1. ...

## Minimum Fixes
1. ...

## Platform Fit
- WeChat:
- Zhihu:
- Xiaohongshu:

## Knowledge Asset Value
- Preserve:
- Could become:

## content_state Update
```yaml
content_state:
  diagnosis:
    recommendation:
    key_issues: []
    minimum_fixes: []
  knowledge_asset:
    should_preserve:
    asset_type:
    suggested_bucket:
  next_step:
    skill:
    reason:
    user_decision_needed:
  handoff:
    from_stage: review
    to_stage:
    accepted_inputs: []
    ignored_context: []
    stop_condition:
```
```

## Full-Edit Output

```md
## Edit Decision
- Main original problem:
- What changed:
- Still needs user confirmation:

## Edited Draft
<edited article>

## Change Log
1. ...

## Strongest Line
<one sentence worth keeping>
```

## Boundaries

- Do not default to full rewrite.
- Do not preserve unsupported claims for smoother prose.
- Do not change the author's core position silently.
- If the core position fails, return a diagnosis instead of hiding the failure with editing.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
