---
name: wenchang-orchestrator
description: Orchestrate a reusable content workflow from topic or draft through research, review, platform adaptation, adaptive image generation, recoverable external handoff, long-form illustrations, publish-ready card rendering, image URL preparation, release checks, and knowledge asset capture. Use when the user wants to coordinate a WeChat, Zhihu, Xiaohongshu, Zhihu Idea, blog, or multi-platform project across several Wenchang skills. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/wenchang-orchestrator
---

# Wenchang Orchestrator

Turn a content request into a staged workflow. Enter at the stage supported by the user's actual input and keep human judgment at fact, image-plan, external-write, and final-publish gates.

## Core Workflow

```text
source intake
  -> topic and research when needed
  -> evidence
  -> draft
  -> content review
  -> publish preflight
  -> platform branches
  -> local image production, adaptive generation, and QA
  -> image publishing plan when public URLs are needed
  -> publish final check
  -> manual publishing
  -> reusable asset capture
```

Do not force a reviewed draft through topic discovery or drafting again.

| User input | Entry point | Default path |
| --- | --- | --- |
| Broad direction | topic discovery | topic -> research -> evidence -> draft -> review -> preflight |
| Clear topic | research or evidence | research -> evidence -> draft -> review -> preflight |
| Existing draft | content review | review -> evidence or edit -> preflight |
| Reviewed long-form draft | publish preflight | preflight -> illustration branch -> image plan -> final |
| Reviewed card-based source | card adaptation | `long-to-cards` -> `cards-to-images` -> visual QA -> human confirmation -> final |
| Existing publish assets | final check | final -> manual publishing decision -> asset capture |

## Platform Branches

After `wenchang-publish-check` preflight:

- WeChat or Zhihu long-form: route accepted image needs to `article-to-illustrations`, insert reviewed local images, then route illustrated Markdown to `md-img-r2` plan mode when public URLs are required.
- Xiaohongshu, WeChat inline cards, Zhihu Idea, or generic carousel: route source material to `long-to-cards` with `delivery_mode=publish_ready`, then to `cards-to-images`. For generative or mixed work, let `resilient-imagegen` resolve `generation_backend=auto`; use `chatgpt-image-handoff` when Computer Use or manual handoff is selected. Continue until real local images pass per-image visual QA and a `cards-manifest` exists. Stop at human confirmation before platform upload.
- Explicit copy-only request: use `long-to-cards` with `delivery_mode=copy_only` and record that image production was intentionally skipped.
- WeChat Moments, community copy, or WeChat-specific insertion notes: use `wechat-to-cards` as an adapter around the shared card pipeline. Do not require it for ordinary long-form publishing.
- Public archive or URL reuse: route checked local images to `md-img-r2` plan mode only when `asset_url_policy=public`. Direct platform upload can use local image files.

Merge the completed branch artifacts back into `wenchang-publish-check` final mode.

## Automation And Gates

Proceed automatically when the next step is low risk:

- select the entry stage
- produce a research map, evidence pack, outline, or draft when inputs are sufficient
- run content review and publish preflight
- produce illustration decisions, card packages, approved-scope local card images, manifests, and dry-run image plans
- prepare a local ChatGPT Handoff Pack and inspect available generation capabilities
- update compact state and reusable case artifacts

Pause when:

- key claims lack evidence
- review recommends a major rewrite or platform change
- a long-form image plan, sensitive supplied asset, or paid generation needs new user judgment
- a Computer Use prompt submission or reference upload is the next action
- publish-ready card images have passed QA and await human confirmation
- an upload, URL rewrite, account action, or external publication is next
- current platform requirements or hot tags need live verification

Never treat a dry-run plan as an upload or a final package as permission to publish.

## Compact State Contract

Keep full body text, publish copy, plans, and manifests in their own artifacts. Store pointers and statuses in `content_state`.

```yaml
content_state:
  request:
    raw_intent:
    current_stage:
    target_platforms: []
  source:
    body_file:
    fact_status: unknown
    review_status: unknown
  platforms:
    wechat:
      body_file:
      publish_package_file:
      illustration_status: not_assessed
    zhihu:
      body_file:
      publish_package_file:
      illustration_status: not_assessed
    xiaohongshu:
      cards_file:
      caption_status: pending
      tag_freshness: unverified
  cards:
    delivery_mode: publish_ready
    platform_profile:
    package_file:
    images_dir:
    manifest_file:
    generation_backend: auto
    handoff_run_id:
    render_status: not_started
    visual_qa_status: pending
    human_confirmation: pending
    asset_url_policy: local
    r2_state: not_planned
  images:
    plan_file:
    manifest_file:
    generation_runtime_file:
    selected_backend:
    r2_report_file:
    r2_status: not_planned
  publish_gate:
    mode: preflight
    status: blocked
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

Use these R2 states: `not_planned`, `planned`, `confirmed`, `uploaded`, and `verified`.

Use these card states:

- `render_status`: `not_started`, `planned`, `generated`, or `failed`
- `visual_qa_status`: `pending`, `passed`, or `needs_revision`
- `human_confirmation`: `pending`, `approved`, or `rejected`

For `delivery_mode=publish_ready`, a completed `long-to-cards` package with no generated images must route to `cards-to-images`. Never route directly from card copy to the final release decision.

## Output Format

````markdown
## Current Stage
- Entry:
- Active branch:
- Workflow:

## Completed
- ...

## Blockers And Human Decisions
- ...

## Recommendation
- Next skill:
- Reason:

## Artifact Pointers
- Source body:
- Platform bodies:
- Publish package:
- Card package:
- Card images and manifest:
- Illustration plan:
- Image manifest:
- Image-generation handoff:
- R2 report:

## content_state
```yaml
<updated compact content_state>
```
````

## Boundaries

- Do not collapse the workflow into one oversized output or duplicate full bodies inside state.
- Do not treat research possibilities as verified facts or topic tags as verified hot tags.
- Do not let one skill silently overwrite another skill's approved artifact.
- Do not leave a `publish_ready` card branch at copy or prompt output.
- Do not upload, publish, delete, or perform irreversible account actions without explicit user confirmation.
- Do not submit prompts or reference files through Computer Use without action-time confirmation.
- Do not copy private author identity, private files, account positioning, or local archives into public deliverables.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
