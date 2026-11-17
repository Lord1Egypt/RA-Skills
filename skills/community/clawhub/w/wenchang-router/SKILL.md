---
name: wenchang-router
description: Route a content request or content_state to the next Wenchang stage. Use when the user gives a topic, source, draft, reviewed article, illustration plan, card package, card-image manifest, R2 report, publishing task, or asks what should run next for WeChat, Zhihu, Zhihu Idea, Xiaohongshu, blog, or multi-platform delivery. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/wenchang-router
---

# Wenchang Router

Identify the current stage, active platform branch, missing evidence, and next skill. Do not perform the downstream task inside the routing response.

## Stage Routing

| Stage | Signals | Route to |
| --- | --- | --- |
| topic discovery | broad direction, “what should I write” | platform topic skill or topic brief |
| storm research | external trend, product, article, or unsettled angle | `storm-research` |
| evidence | fact-heavy claims, data, sources | `wenchang-research` |
| drafting | confirmed topic, outline, and evidence | `wenchang-wechat-writer` or target-platform writer |
| content review | existing draft, diagnosis, editing | `wenchang-review` |
| publish preflight | reviewed draft needs titles, summaries, captions, tags, images | `wenchang-publish-check` in `preflight` mode |
| long-form illustrations | WeChat or Zhihu draft has an accepted image need | `article-to-illustrations` |
| card adaptation | long source needs Xiaohongshu, WeChat inline, Zhihu Idea, or generic card assets | `long-to-cards` |
| card image production | `publish_ready` card package exists but real images or manifest do not | `cards-to-images` |
| card image revision | images exist but visual QA is pending or failed | `cards-to-images` |
| card human gate | visual QA passed and `human_confirmation=pending` | stop for user confirmation |
| WeChat distribution adapter | Moments, community copy, or WeChat-specific insertion notes requested | `wechat-to-cards` |
| image URL plan | checked local Markdown or card-manifest images exist and `asset_url_policy=public` | `md-img-r2` in plan mode |
| confirmed image apply | reviewed plan plus explicit upload or rewrite confirmation | `md-img-r2` apply path |
| final publish check | bodies, cards, images, and package are assembled | `wenchang-publish-check` in `final` mode |

If the platform is missing, default to a long-form source path and record platform adaptation as pending. Do not invent platform requirements.

## Routing Rules

- Route a changing argument back to review before illustration or publish packaging.
- Route unsupported claims back to research before release work.
- Require one illustration decision per long-form platform; do not reuse one platform's decision silently.
- Route every card-based platform through `long-to-cards` with a platform profile.
- When `delivery_mode=publish_ready`, route completed card copy to `cards-to-images`; allow a copy-stage stop only for explicit `copy_only`.
- Keep the approved card package as the rendering and final-check source of truth.
- Stop for human confirmation after every required card image passes visual QA.
- Route to `md-img-r2` only after local image references exist in reviewed platform Markdown or a checked card manifest.
- Route card images to `md-img-r2` only when `asset_url_policy=public`; direct platform upload may retain local files.
- Stop before external upload, URL rewrite, paid generation, or platform publication unless the user explicitly approved it.

## Output Format

````markdown
## Routing Decision
- Platform branch:
- Current stage:
- Recommended skill and mode:
- Reason:
- Blockers:
- User decision needed:

## Accepted Inputs
- ...

## Ignored Or Stale Context
- ...

## content_state Update
```yaml
content_state:
  request:
    current_stage:
    target_platforms: []
  source:
    body_file:
    fact_status:
    review_status:
  cards:
    delivery_mode:
    platform_profile:
    package_file:
    images_dir:
    manifest_file:
    render_status:
    visual_qa_status:
    human_confirmation:
    asset_url_policy:
    r2_state:
  images:
    plan_file:
    manifest_file:
    r2_status:
  publish_gate:
    mode:
    status:
    blockers: []
  next_step:
    skill:
    reason:
    user_decision_needed:
  handoff:
    from_stage:
    to_stage:
    accepted_inputs: []
    ignored_context: []
    stop_condition:
```
````

## Boundaries

- Do not write the final article, cards, or images in the routing stage.
- Do not skip evidence gathering for release-critical claims.
- Do not treat a recommendation as user confirmation.
- Do not route a `publish_ready` card package directly to final publishing while images or visual QA are missing.
- Do not route around an unresolved human or external-write gate.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
