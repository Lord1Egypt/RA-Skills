---
name: xiaohongshu-ops
description: End-to-end Xiaohongshu (小红书 / RedNote) operations skill for setting content style, saving an operating profile, generating posts in that house style, choosing or generating suitable images, and publishing through the dedicated independent browser flow. Use when the user says things like “帮我运营小红书”, wants a Xiaohongshu operating style configured, wants ongoing post generation in a fixed house style, or wants to test or run a full Xiaohongshu publishing workflow.
---

# Xiaohongshu Ops

Use this skill as the single entry point for Xiaohongshu operations.

## Workflow

1. Read `data/xiaohongshu/profile.json` when it exists.
2. If profile setup is incomplete, ask concise setup questions and save the result with `scripts/init_profile.js`.
3. Read `data/xiaohongshu/rules.md` for current local operating rules.
4. Generate topic/title/body/page structure in the configured house style.
5. Choose image strategy from `stock`, `cards-lite`, or `mixed`.
6. Build assets and publish through the dedicated independent browser flow when publishing is requested.

## Profile setup

Keep setup questions short. Cover positioning, goals, audience, style, image mode, publish preference, and whether auto learning should be enabled.
Do not ask again for information the user already provided.

## Watermark rule

Do **not** remove watermarks.
Do **not** instruct or script watermark removal.
If an image source has watermarks, reject it and choose a different source.

## Auto learning

Support automatic daily learning in reference mode.
If `autoLearning.enabled` is true in the profile, treat trend/style learning as a daily background reference task.
Write learning outputs into local reference files instead of silently mutating the main profile.

## Publish path

Use the dedicated independent browser profile for real publishing:

- `~/.openclaw/browser/xhs-independent-user-data`

Do not treat the user's normal browser or OpenClaw's shared browser profile as the canonical publish path.

## Offer first-run publish test

After setup, ask the user whether to do a first publish test.

Recommended wording:
- 是否要先自动生成并准备发布一篇测试笔记，顺手验证小红书发布链路是否正常？

## References

Read these only when needed:

- `references/questions.md` — profile intake prompts
- `references/profile-schema.json` — profile fields and expected structure
- `references/workflow.md` — fuller operating workflow
- `references/content-rules.md` — title/body constraints and writing rules
- `references/content-templates.md` — content structure patterns
- `references/content-output-format.md` — expected output shape
- `references/content-ideas.md` — topic/angle inspiration
- `references/image-sources.md` — image sourcing guidance
- `references/stock-providers.md` — stock image source notes
- `references/cards-usage.md` — card-generation guidance
- `references/cards-input-example.json` — card input example
- `references/publish-independent-browser.md` — dedicated browser publish path
- `references/publish-usage.md` — publish flow details
- `references/auto-learning.md` — daily reference-learning behavior
- `references/repo-notes.md` — repository-oriented notes for standalone Git usage

## Scripts

Use these scripts as low-freedom helpers when deterministic execution is better than rewriting logic inline:

- `scripts/init_profile.js`
- `scripts/fetch_stock_images.js`
- `scripts/select_image_mode.js`
- `scripts/build_image_pipeline.js`
- `scripts/run_ops_once.js`
- `scripts/build_xhs_post.js`
- `scripts/generate_xhs_cards.js`
- `scripts/xhs_publish.js`
- `scripts/xhs_independent_browser.js`
- `scripts/xhs_independent_publish.js`

## Safety rule

Default to the profile's publish preference. If the profile says review-before-publish, stop for review. If the profile allows direct publish and the user asks for publishing, use the independent browser path.

## File convention

Persistent config:
- `data/xiaohongshu/profile.json`

Runtime outputs can go under:
- `/tmp/openclaw/uploads/xhs_*`

## Content storage rule

Do not treat generated post content as a long-term local content library.
For each new run, default to regenerating:
- title
- body
- page structure
- images

Use runtime outputs as temporary working files only.
Do not rely on old note content by default unless the user explicitly asks to reuse an older draft.

## Active content constraints

Read `references/content-rules.md` when generating Xiaohongshu copy.
Read `data/xiaohongshu/rules.md` as the local source of truth for current Xiaohongshu operating rules.
Current default rules:
- title must be a natural phrase within 20 characters
- mixed Chinese/English titles should preserve important English terms instead of clipping them mid-word
- body should stay within 2000 characters

## Integration

This skill orchestrates:
- content generation
- image strategy selection
- stock-image planning
- cards-lite fallback when needed
- dedicated-browser publishing

Use the saved profile as the style source of truth.
