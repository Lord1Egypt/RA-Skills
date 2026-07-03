---
name: zm-md2wechat-conversion-tool
description: ZM Markdown 转公众号格式工具。用于将 Markdown 转为微信公众号 HTML，检查主题、图片、样式、AI 痕迹处理和草稿创建能力；正式发布需配合 ZM 公众号草稿发布与核验 Skill。
homepage: https://github.com/geekjourneyx/zm-md2wechat-conversion-tool-skill
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["zm-md2wechat-conversion-tool"],"env":["WECHAT_APPID","WECHAT_SECRET"]},"install":[{"id":"brew","kind":"brew","formula":"geekjourneyx/tap/zm-md2wechat-conversion-tool","bins":["zm-md2wechat-conversion-tool"],"label":"Install zm-md2wechat-conversion-tool (brew)"},{"id":"go","kind":"go","module":"github.com/geekjourneyx/zm-md2wechat-conversion-tool-skill/cmd/zm-md2wechat-conversion-tool@latest","bins":["zm-md2wechat-conversion-tool"],"label":"Install zm-md2wechat-conversion-tool (go)"}]}}
---

# zm-md2wechat-conversion-tool

Use `zm-md2wechat-conversion-tool` when the user wants to:

- convert Markdown into WeChat Official Account HTML
- inspect resolved article metadata, readiness, and publish risks before conversion
- generate a local preview artifact or upload drafts
- inspect live capabilities, providers, themes, and prompts
- generate covers, infographics, or other article images
- create image posts
- write in creator styles or remove AI writing traces

## Intent Routing

Choose the command family before doing any publish action:

- Use `convert` / `inspect` / `preview` when the user wants a standard WeChat article draft (`news`), HTML conversion, article metadata, article preview, or a draft that needs `--cover`.
- Use `create_image_post` when the user says `小绿书`, `图文笔记`, `图片消息`, `newspic`, `多图帖子`, or asks to publish an image-first post rather than an article HTML draft.
- Do not route `小绿书` / `图文笔记` requests to `convert --draft` just because the user also has a Markdown article. A Markdown file can still be the image source for `create_image_post -m article.md`.
- Treat `convert --draft` and `create_image_post` as different publish targets, not interchangeable command variants.

## Defaults And Config

- Use this skill only when `zm-md2wechat-conversion-tool` is already available on `PATH`.
- Draft upload and publish-related actions require `WECHAT_APPID` and `WECHAT_SECRET`.
- Image generation may require additional image-service configuration in `~/.config/zm-md2wechat-conversion-tool/config.yaml`.
- `convert` defaults to `api` mode unless the user explicitly asks for `--mode ai`.
- Check configuration in this order:
  1. `~/.config/zm-md2wechat-conversion-tool/config.yaml`
  2. environment variables such as `MD2WECHAT_BASE_URL`
  3. project-local `zm-md2wechat-conversion-tool.yaml`, `zm-md2wechat-conversion-tool.yml`, or `zm-md2wechat-conversion-tool.json`
- If the user asks to switch API domain, update `api.zm-md2wechat-conversion-tool_base_url` or `MD2WECHAT_BASE_URL`.
- Treat live CLI discovery output as the source of truth. Do not guess provider names, theme names, or prompt names from repository files alone.

## Discovery First

Run these before selecting a provider, theme, or prompt:

- `zm-md2wechat-conversion-tool version --json`
- `zm-md2wechat-conversion-tool capabilities --json`
- `zm-md2wechat-conversion-tool providers list --json`
- `zm-md2wechat-conversion-tool themes list --json`
- `zm-md2wechat-conversion-tool prompts list --json`
- `zm-md2wechat-conversion-tool prompts list --kind image --json`
- `zm-md2wechat-conversion-tool prompts list --kind image --archetype cover --json`

Inspect a specific resource before using it:

- `zm-md2wechat-conversion-tool providers show openrouter --json`
- `zm-md2wechat-conversion-tool providers show volcengine --json`
- `zm-md2wechat-conversion-tool themes show autumn-warm --json`
- `zm-md2wechat-conversion-tool prompts show cover-default --kind image --json`
- `zm-md2wechat-conversion-tool prompts show cover-hero --kind image --archetype cover --tag hero --json`
- `zm-md2wechat-conversion-tool prompts show infographic-victorian-engraving-banner --kind image --archetype infographic --tag victorian --json`
- `zm-md2wechat-conversion-tool prompts render cover-default --kind image --var article_title='Example' --json`

When choosing image presets, prefer the prompt metadata returned by `prompts show --json`, especially `primary_use_case`, `compatible_use_cases`, `recommended_aspect_ratios`, and `default_aspect_ratio`.
When choosing an image model, prefer `providers show <name> --json` and read `supported_models` before hard-coding `--model`.

## Core Commands

Configuration:

- `zm-md2wechat-conversion-tool config init`
- `zm-md2wechat-conversion-tool config show --format json`
- `zm-md2wechat-conversion-tool config validate`

Conversion:

- `zm-md2wechat-conversion-tool inspect article.md`
- `zm-md2wechat-conversion-tool preview article.md`
- `zm-md2wechat-conversion-tool convert article.md --preview`
- `zm-md2wechat-conversion-tool convert article.md -o output.html`
- `zm-md2wechat-conversion-tool convert article.md --draft --cover cover.jpg`
- `zm-md2wechat-conversion-tool convert article.md --mode ai --theme autumn-warm --preview`
- `zm-md2wechat-conversion-tool convert article.md --title "新标题" --author "作者名" --digest "摘要"`

Image handling:

- `zm-md2wechat-conversion-tool upload_image photo.jpg`
- `zm-md2wechat-conversion-tool download_and_upload https://example.com/image.jpg`
- `zm-md2wechat-conversion-tool generate_image "A cute cat sitting on a windowsill"`
- `zm-md2wechat-conversion-tool generate_image --preset cover-hero --article article.md --size 2560x1440`
- `zm-md2wechat-conversion-tool generate_cover --article article.md`
- `zm-md2wechat-conversion-tool generate_infographic --article article.md --preset infographic-comparison`
- `zm-md2wechat-conversion-tool generate_infographic --article article.md --preset infographic-dark-ticket-cn --aspect 21:9`
- `zm-md2wechat-conversion-tool generate_infographic --article article.md --preset infographic-handdrawn-sketchnote`

Drafts and image posts:

- `zm-md2wechat-conversion-tool create_draft draft.json`
- `zm-md2wechat-conversion-tool test-draft article.html cover.jpg`（only for smoke tests; not the formal publish path）
- `zm-md2wechat-conversion-tool create_image_post --help`
- `zm-md2wechat-conversion-tool create_image_post -t "Weekend Trip" --images photo1.jpg,photo2.jpg`
- `zm-md2wechat-conversion-tool create_image_post -t "Travel Diary" -m article.md`
- `echo "Daily check-in" | zm-md2wechat-conversion-tool create_image_post -t "Daily" --images pic.jpg`
- `zm-md2wechat-conversion-tool create_image_post -t "Test" --images a.jpg,b.jpg --dry-run`

Writing and humanizing:

- `zm-md2wechat-conversion-tool write --list`
- `zm-md2wechat-conversion-tool write --style dan-koe`
- `zm-md2wechat-conversion-tool write --style dan-koe --input-type fragment article.md`
- `zm-md2wechat-conversion-tool write --style dan-koe --cover-only`
- `zm-md2wechat-conversion-tool write --style dan-koe --cover`
- `zm-md2wechat-conversion-tool write --style dan-koe --humanize --humanize-intensity aggressive`
- `zm-md2wechat-conversion-tool humanize article.md`
- `zm-md2wechat-conversion-tool humanize article.md --intensity aggressive`
- `zm-md2wechat-conversion-tool humanize article.md --show-changes`
- `zm-md2wechat-conversion-tool humanize article.md -o output.md`

## Article Metadata Rules

For `convert`, metadata resolution is:

- Title: `--title` -> `frontmatter.title` -> first Markdown heading -> `未命名文章`
- Author: `--author` -> `frontmatter.author`
- Digest: `--digest` -> `frontmatter.digest` -> `frontmatter.summary` -> `frontmatter.description`

Limits enforced by the CLI:

- `--title`: max 32 characters
- `--author`: max 16 characters
- `--digest`: max 128 characters

Draft behavior:

- Formal article drafts should use the Agent-orchestrated `upload_image -> draft.json -> create_draft -> draft/get verification` chain.
- `test-draft` is for smoke tests only because it uses test metadata defaults unless wrapped externally.
- `convert --draft` remains a compatible shortcut, but do not treat it as the primary formal workflow when exact title/author/digest/content control is required.
- If digest is still empty when creating a draft, the draft layer generates one from article HTML content with a 120-character fallback.
- Creating a draft through `convert --draft` requires either `--cover` or `--cover-media-id`.
- `create_draft` requires a JSON file with `articles[].title` and `articles[].content`; for formal WeChat drafts also provide `author`, `digest`, `thumb_media_id`, and `show_cover_pic`.
- `--cover` is a local image path contract for article drafts. `--cover-media-id` / `thumb_media_id` is for an existing WeChat permanent cover asset. Do not assume a WeChat URL or `mmbiz.qpic.cn` URL can be reused as `thumb_media_id`.
- `inspect` is the source-of-truth command for resolved metadata, readiness, and checks.
- `preview` v1 writes a standalone local HTML preview file. It does not start a workbench, write back to Markdown, upload images, or create drafts.
- `convert --preview` is still the convert-path preview flag; it is not the same thing as the standalone `preview` command.
- `preview --mode ai` is degraded confirmation only; it must not be treated as final AI-generated layout.
- `--title` / `--author` / `--digest` affect draft metadata, not necessarily visible body HTML.
- Markdown images are only uploaded/replaced during `--upload` or `--draft`, not during plain `convert --preview`.

## Agent Rules

- Start with discovery commands before committing to a provider, theme, or prompt.
- Route by publish target first: article draft => `convert`; image post / 小绿书 / newspic => `create_image_post`.
- Prefer the confirm-first flow for article work: `inspect` -> `preview` -> generate/confirm HTML -> `upload_image` -> `create_draft` -> `draft/get` verification.
- If the user says `小绿书`, `图文笔记`, `图片消息`, `newspic`, or asks for a multi-image post, prefer `create_image_post` even when the source content lives in Markdown.
- Prefer `generate_cover` or `generate_infographic` over a raw `generate_image "prompt"` call when a bundled preset fits the task.
- Validate config before any draft, publish, or image-post action.
- If draft creation returns `45004`, check digest/summary/description before assuming the body content is too long.
- If the user asks for AI conversion or style writing, be explicit that the CLI may return an AI request/prompt rather than final HTML or prose unless the workflow completes the external model step.
- Do not perform draft creation, publishing, or remote image generation unless the user asked for it.

## Safety And Transparency

- Reads local Markdown files and local images.
- May download remote images when asked.
- May call external image-generation services when configured.
- May upload HTML, images, drafts, and image posts to WeChat when the user explicitly requests those actions.

## 标准状态机

所有执行结果必须使用以下三种结论之一：

- `PASS`：必要输入齐全，流程执行完成，审核项通过，可以进入下一阶段或交付。
- `NEEDS_REVISION`：可以继续推进，但存在必须返工项；必须列出返工范围、owner、复审标准。
- `BLOCKED`：缺关键素材、缺权限、缺确认、工具不可用或存在伪造风险；不得继续假装完成，必须说明阻塞原因和下一步。

## 执行步骤

1. 确认输入文件存在。
2. 检查最小必填字段。
3. 执行转换或生成。
4. 检查输出文件存在且可打开。
5. 清理操作备注、路径说明、脏文本。
6. 检查图片、样式、链接和格式。
7. 输出审核结论：`PASS` / `NEEDS_REVISION` / `BLOCKED`。
8. 如需正式发布，交给对应发布/核验 Skill 继续执行。

