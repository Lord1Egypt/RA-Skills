---
name: wenchang-publish-check
description: Build and verify platform-specific publish packages for reviewed content. Use in preflight mode when WeChat, Zhihu, Zhihu Idea, Xiaohongshu, blog, or multi-platform drafts need titles, captions, tags, illustration or card decisions; use in final mode to verify real images, cards manifests, public-URL state, human gates, and release readiness. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/wenchang-publish-check
---

# Wenchang Publish Check

Own the publishing specification and release gate for reviewed content. Keep the formal platform body in its own file and store titles, summaries, captions, tags, image status, and blockers in a separate publish package.

## Inputs

- reviewed source or platform draft
- target platforms
- fact and review status
- existing platform bodies and card packages
- card images directory and `cards-manifest` when card delivery is `publish_ready`
- illustration plan, long-form image manifest, or R2 report when available
- current platform requirements or user constraints
- existing `content_state`

Route back to `wenchang-review` when the argument or structure is unstable. Route to `wenchang-research` when release-critical claims lack support.

## Choose A Mode

- `preflight`: run after content review and before image production. Generate the publish package, illustration decisions, and production blockers.
- `final`: run after platform bodies, cards, images, and any required public URLs are complete. Verify the package and make the release decision.

When the user does not name a mode, infer it from artifact state. State the selected mode.

## Preflight

### Common Checks

- the source body and fact baseline are identified
- each target platform has one formal body or an explicit pending body
- the reader promise and single CTA remain consistent
- titles and summaries do not overstate the body
- claims needing evidence are blockers, not hidden caveats
- every long-form platform gets an illustration decision
- every card-based platform gets a `delivery_mode`, `platform_profile`, and `asset_url_policy`
- external writes and human decisions are visible

### WeChat Package

Generate:

- 3-5 accurate article titles
- one search title
- one summary
- cover copy
- sharing copy
- core keywords
- illustration decision and slot count

### Zhihu Package

Generate:

- question, judgment, and experience title candidates when supported by the body
- opening lead
- short summary
- topic tags
- illustration decision and slot count
- comment prompt

### Xiaohongshu Package

Generate:

- cover title
- first-line hook
- body caption or post description
- image or card order
- save, comment, or follow CTA
- grouped tags with freshness state

Do not label tags as currently hot unless they were checked against a current source during this run.

### Card-based Platform Package

For Xiaohongshu, WeChat inline cards, Zhihu Idea, and generic carousels, record:

- `delivery_mode`: `publish_ready` by default or explicit `copy_only`
- `platform_profile`
- canonical card package
- required image count, order, ratio, and dimensions
- image output directory and manifest target
- `asset_url_policy`: `local` by default or `public`

When `delivery_mode=publish_ready`, set missing real images or a missing manifest as production blockers and route to `cards-to-images`.

## Tag Freshness Contract

Use four groups:

```yaml
tags:
  core_tags: []
  scene_tags: []
  series_tags: []
  verified_hot_tags:
    status: unverified
    checked_at:
    source:
    values: []
```

Set `verified_hot_tags.status` to `verified` only when `checked_at`, `source`, and current values are present. Use ordinary topic tags when live verification is unavailable.

## Final

Verify:

- the fact and review gates passed
- required platform bodies exist and match the source baseline
- every required publish field is filled
- Xiaohongshu caption, cards, and image order agree
- every `publish_ready` card image exists at the manifest path
- image count and order match the canonical card package
- recorded dimensions and aspect ratios match the platform profile
- every card has `generation_status=generated` and `visual_qa_status=passed`
- exact text, clipping, and page order were checked per image rather than only through a contact sheet
- `human_confirmation` is recorded accurately; pending confirmation keeps the package at `needs_review`
- each accepted illustration exists at its recorded anchor
- image alt text and source notes are present
- local images were either intentionally retained or processed through the reviewed publishing path
- required public URLs are accessible and match the latest replacement report
- no tag is presented as current without freshness evidence
- no private path, credential, internal note, or account detail appears in public artifacts
- every external upload or publishing action still requires the user's decision

Assign one status:

- `ready_to_publish`: all required artifacts are complete, required card images are user-approved, and no blocker remains
- `needs_review`: the package is complete enough for human editorial judgment but still has explicit review items
- `blocked`: a missing fact, body, image, URL, platform asset, or permission prevents publishing

## Output Format

```markdown
# Publish Package

## Decision
- Mode: preflight / final
- Status: ready_to_publish / needs_review / blocked
- Blockers:
- Human decisions:

## Source Baseline
- Formal source:
- Fact status:
- Review status:
- Reader promise:
- CTA:

## WeChat
- Body file:
- Title candidates:
- Search title:
- Summary:
- Cover copy:
- Sharing copy:
- Keywords:
- Illustration decision:

## Zhihu
- Body file:
- Title candidates:
- Opening lead:
- Summary:
- Topic tags:
- Illustration decision:
- Comment prompt:

## Xiaohongshu
- Cards file:
- Cover title:
- First-line hook:
- Body caption:
- Image order:
- CTA:
- Tags and freshness:

## Card Images
- Delivery mode:
- Platform profile:
- Card package:
- Images directory:
- Cards manifest:
- Image order and dimensions:
- Render status:
- Visual QA status:
- Human confirmation:
- Asset URL policy:

## Images
- Illustration plan:
- Image manifest:
- R2 report:
- URL verification:

## Knowledge Asset
- Preserve:
- Asset type:
- Suggested location:
```

Update `content_state` with file pointers, statuses, blockers, and the next handoff. Do not copy full body text into state.

## Boundaries

- Do not rewrite the full article during a publish check.
- Do not invent current platform rules or trending tags.
- Do not make a package look ready when blockers remain.
- Do not generate images, upload files, or publish externally in this skill.
- Do not accept copy, visual prompts, a contact sheet, or planned filenames as proof that card image files exist.
- Do not mark a publish-ready card package ready while visual QA or human confirmation is pending.
- Do not overwrite platform metadata that the user has already approved without reporting the proposed change.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
