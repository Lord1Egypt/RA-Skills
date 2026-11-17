---
name: wechat-to-cards
description: Adapt a reviewed WeChat article or publish package into WeChat-specific inline-card requirements, Moments copy, community share text, or archive assets while reusing the shared long-to-cards and cards-to-images pipeline. Use when the user asks for 公众号贴图, 朋友圈分发文案, 社群转发文案, WeChat card assets, or visual snippets after the long-form body exists. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/wechat-to-cards
---

# WeChat To Cards

## Goal

Add WeChat-specific distribution decisions around the canonical card pipeline.

Preserve the article's main argument, evidence, and reader promise. Produce skimmable card copy and share assets without rewriting the source into a different thesis.

This is an optional WeChat adapter. Use `long-to-cards` as the canonical card-authoring skill and `cards-to-images` as the canonical renderer. Keep Moments and community copy here.

## Inputs

Collect:

- source article, draft, outline, or publish package
- target use: article inline images, Moments, community share, or archive cards
- `delivery_mode`: `publish_ready` for real inline-card images or explicit `copy_only`
- `asset_url_policy`: `local` by default or `public` when a stable URL is required
- desired card count
- target reader
- preferred tone
- claims, examples, or sections to preserve
- claims, examples, or sections to avoid

If the user provides only a topic, route to topic planning or drafting first. This skill works best after there is a source article or clear outline.

When an approved publish package exists, treat its title, summary, cover copy, tags, and CTA as the source of truth. Generate card-specific copy around those decisions and report any proposed change instead of silently replacing approved metadata.

## Process

### 1. Diagnose The Source

Identify:

- article core claim
- reader problem
- strongest proof or example
- section structure
- reusable framework, checklist, or contrast
- publish-sensitive claims that need evidence
- parts unsuitable for cards

Do not pull in internal research notes, diagnosis notes, `content_state`, or private drafting context unless the user explicitly asks for internal planning assets.

### 2. Choose The WeChat Use Case

Pick the package type:

- Article inline cards: support reading, summarize key points, and break dense sections.
- Moments cards: strong hook, one clear takeaway, minimal context.
- Community share cards: explain why this article is worth opening.
- Summary carousel: make the article understandable without opening the full text.
- Archive cards: preserve a reusable method, checklist, or concept.

Use one primary package type per output. If multiple are requested, separate them clearly.

For article inline cards, summary carousels, or archive cards, prepare a `long-to-cards` handoff with `platform_profile=wechat-inline`. Reuse its card sequence, copy, source anchors, alt text, and image order instead of maintaining a separate generic card contract here.

For Moments or community text without cards, generate the requested distribution copy and use `delivery_mode=copy_only`.

### 3. Add WeChat-specific Constraints

- mark each image as a vertical card or horizontal diagram
- identify its article insertion anchor when it will appear inside the long-form body
- preserve approved title, summary, cover copy, and CTA
- keep cards readable outside the article when they may also be shared
- specify one distribution CTA per package

### 4. Continue The Shared Image Pipeline

When `delivery_mode=publish_ready`, use:

```text
wechat-to-cards
  -> long-to-cards (platform_profile=wechat-inline)
  -> cards-to-images
  -> visual QA
  -> human confirmation
```

Do not stop at visual suggestions. Return to this adapter after rendering only when Moments copy, community copy, or WeChat-specific insertion notes still need to be merged.

### 5. Add Distribution Assets

Add:

- Moments copy
- community share copy
- card-specific CTA
- optional provisional cover or summary only when no publish package exists
- source caveats

## Output Format

Use this structure:

```markdown
# WeChat Card Package

## Source Diagnosis
- Core claim:
- Reader problem:
- Strongest reusable material:
- Card package type:
- Claims needing evidence:
- Dropped material:

## Shared Card Handoff
- Long-to-cards input:
- Platform profile: wechat-inline
- Delivery mode:
- Article insertion anchors:
- Vertical-card or horizontal-diagram decisions:
- Canonical card package:

## Distribution Assets
- Delivery mode:
- Shared card package:
- Image manifest:
- Moments copy:
- Community share copy:
- Card-specific CTA:
- Publish-package fields reused:
- Provisional metadata, if no package exists:
- Proposed metadata changes:
- Source caveats:
- Follow-up card ideas:

## Handoff
- Next skill:
- Platform profile: wechat-inline
- Asset URL policy:
- User confirmation needed:
- Stop condition:
```

## Quality Rules

- Keep the article's original thesis intact.
- Require shared cards to remain understandable when separated from the article.
- Prefer concrete claims, contrasts, checklists, and examples over broad slogans.
- Keep cover text specific and inspectable.
- Mark unverified metrics, claims, dates, and examples before publish.
- Preserve source attribution and uncertainty.

## Boundaries

- Do not duplicate generic card-authoring or rendering rules already owned by `long-to-cards` and `cards-to-images`.
- Do not stop at copy when a WeChat inline-card request uses `delivery_mode=publish_ready`.
- Do not publish to WeChat or upload images externally.
- Do not invent cases, metrics, screenshots, quotes, or reader reactions.
- Do not include private article paths, account names, draft archives, or internal content systems.
- Do not convert internal review notes into reader-facing cards.
- Do not claim the assets are publish-ready until source claims and visuals are checked.
- Do not overwrite approved publish-package metadata.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
