---
name: zm-wechat-draft-publish-verify
description: ZM 公众号草稿发布与核验。用于将已准备好的 Markdown/HTML 公众号稿通过 zm-md2wechat-conversion-tool 推送到公众号草稿箱，并强制执行 draft/get 真实落库与排版核验。
homepage: https://github.com/geekjourneyx/zm-md2wechat-conversion-tool-skill
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":["zm-md2wechat-conversion-tool","python3"],"env":["WECHAT_APPID","WECHAT_SECRET"]}}}
---

# zm-wechat-draft-publish-verify

Use `zm-wechat-draft-publish-verify` when the user wants to:

- push a prepared WeChat article into the Official Account draft box
- turn Markdown into WeChat-compatible HTML and then create a draft
- use a stable publishing wrapper instead of manually chaining `upload_image -> create_draft -> draft/get`
- verify that a draft really exists in the WeChat backend before reporting success
- troubleshoot the current `zm-md2wechat-conversion-tool create_draft` publishing chain

## What This Skill Is For

This skill is the **publishing execution layer** for WeChat Official Account drafts.

It is responsible for:

- config validation
- Markdown → HTML conversion when needed
- cover upload
- `draft.json` generation
- `zm-md2wechat-conversion-tool create_draft`
- WeChat `draft/get` backend verification
- outputting machine-readable verification artifacts

It is **not** responsible for:

- topic selection
- long-form writing
- AI-trace review
- editorial approval
- layout strategy decisions before HTML exists
- archive / final content governance

Those stay in the main production workflow.

## Canonical Publish Path

```text
Prepared article HTML or Markdown
→ zm-md2wechat-conversion-tool config validate
→ inspect / preview / convert (if Markdown)
→ zm-md2wechat-conversion-tool upload_image cover.*
→ generate draft.json
→ zm-md2wechat-conversion-tool create_draft draft.json
→ call WeChat draft/get
→ verify title / author / cover / content / visibility
```

## Hard Rules

1. `zm-md2wechat-conversion-tool create_draft` is the formal draft creation action.
2. `test-draft` is only for chain testing, not formal publishing.
3. `convert --mode ai` returning `CONVERT_AI_REQUEST_READY` does **not** mean a draft was created.
4. AI-mode output must be materialized into real WeChat-compatible HTML before entering this skill.
5. Command success is **not** task success.
6. Final success requires backend verification.
7. Preferred execution path is `scripts/publish.sh`, not an ad-hoc hand-built sequence.
8. Local `preview` and local `convert` artifacts are not WeChat backend proof.
9. If `create_draft` succeeds but `draft/get` fails, the result must be treated as unverified or blocked.
10. `media_id` alone is only a submission receipt, not a success proof.

## Inputs

Preferred prepared package:

```text
wechat_package/
  article.html
  cover.png
  images/
  publish-checklist.md
```

Also supported:

- `article.md` + cover image
- `article.html` + cover image

## Requirements

The following must already be available:

- `zm-md2wechat-conversion-tool`
- `python3`

Config file:

```text
~/.config/zm-md2wechat-conversion-tool/config.yaml
```

Expected WeChat credentials:

```yaml
wechat:
  appid: "公众号 AppID"
  secret: "公众号 AppSecret"
```

The current public IP must also be in the WeChat Official Account IP allowlist.

## Validate Before Publish

```bash
zm-md2wechat-conversion-tool config validate --json
```

## Standard Execution

Primary script:

```bash
skills/zm-wechat-draft-publish-verify/scripts/publish.sh
```

Usage:

```bash
./scripts/publish.sh <article.md|article.html> <cover-image> [title] [author] [digest]
```

Examples:

```bash
./scripts/publish.sh article.html cover.png "现在找工作，最累的不是被拒" "野哥" "找工作最累的不是被拒，而是一直没有回音。"
./scripts/publish.sh article.md cover.png "标题" "野哥" "摘要"
```

## What The Script Does

1. `zm-md2wechat-conversion-tool config validate --json`
2. If input is Markdown:
   - `zm-md2wechat-conversion-tool inspect ... --json`
   - `zm-md2wechat-conversion-tool preview ... --json`
   - `zm-md2wechat-conversion-tool convert ... --output ... --json`
3. `zm-md2wechat-conversion-tool upload_image cover.png --json`
4. Generate `*.zm-md2wechat-conversion-tool-create-draft.json`
5. `zm-md2wechat-conversion-tool create_draft *.json --json`
6. Call official WeChat `draft/get`
7. Save verification output

## Output Artifacts

The script writes artifacts next to the article:

```text
*.zm-md2wechat-conversion-tool-inspect.json
*.zm-md2wechat-conversion-tool-preview.json
*.zm-md2wechat-conversion-tool-convert.json
*.zm-md2wechat-conversion-tool-cover-upload.json
*.zm-md2wechat-conversion-tool-create-draft.json
*.zm-md2wechat-conversion-tool-create-draft-result.json
*.zm-md2wechat-conversion-tool-create-draft-verify.json
```

The final source of truth is:

```text
*.zm-md2wechat-conversion-tool-create-draft-verify.json
```

## Success Criteria

Only report **draft push success** when both are true:

1. `zm-md2wechat-conversion-tool create_draft` returned success
2. `draft/get` verification passed and the backend draft is really present

Otherwise classify as one of:

- submitted but unverified
- verification failed
- blocked by config / credential / IP / content issue

## Draft JSON Shape

```json
{
  "articles": [
    {
      "title": "标题",
      "author": "野哥",
      "digest": "摘要",
      "content": "<section style=\"...\">正文 HTML</section>",
      "thumb_media_id": "封面素材 media_id",
      "show_cover_pic": 0
    }
  ]
}
```

Constraints:

- `articles` must not be empty
- `title` required, recommended ≤ 32 chars
- `author` recommended ≤ 16 chars
- `digest` recommended ≤ 120–128 chars
- `content` required and must be WeChat-compatible HTML
- `thumb_media_id` must come from `zm-md2wechat-conversion-tool upload_image` or equivalent WeChat material upload

## Verification Checklist

At minimum verify:

- draft really exists
- `title` matches expected value
- `author` matches expected value
- `thumb_media_id` exists
- content exists
- no leaked local paths such as `<local-home>/` or `content-factory/`
- content has inline styles or otherwise clearly matches publish-ready WeChat HTML
- article images are actually present when the article uses body images
- for Markdown input, the process did not stop at local preview/convert only
- for AI mode upstream flows, the published content is real generated HTML, not the request-ready payload

## Common Failure Modes

### Invalid IP

```text
errcode=40164 invalid ip ... not in whitelist
```

Action: add the current public IP to the WeChat Official Account backend allowlist.

### Invalid AppSecret

```text
errcode=40125 invalid appsecret
```

Action: fix `~/.config/zm-md2wechat-conversion-tool/config.yaml`.

### AI mode only returned a request

```json
{
  "code": "CONVERT_AI_REQUEST_READY",
  "status": "action_required"
}
```

This is not success. It only means the AI conversion request is ready. Continue by producing HTML, then run the draft chain.

## Operational Guidance For Agents

- Use this skill only when draft creation is actually requested.
- Prefer this skill over improvising raw shell steps.
- Never claim success from `media_id`, `preview`, or `convert` alone.
- Treat verification as mandatory, not optional polish.
- If verification fails, report the exact blocker instead of vague success language.

## Related Files

- `README.md` — quick operator-facing usage
- `references/troubleshooting.md` — failure handling
- `references/themes.md` — related publishing notes
- `scripts/publish.sh` — canonical execution wrapper
- `scripts/setup.sh` — environment setup helper

## Experience Captured

### 2026-05-14

Verified working path using an older article:

```text
AI-ready HTML
→ zm-md2wechat-conversion-tool upload_image
→ draft.json
→ zm-md2wechat-conversion-tool create_draft
→ WeChat draft/get verification passed
```

Verified fields included title, author, digest, cover, content, inline styles, and no local path leakage.

### 2026-05-15

Key lessons added to the standard skill:

- formal publishing should default to `scripts/publish.sh`
- `media_id` is only a receipt
- `CONVERT_AI_REQUEST_READY` is an action-required state, not a success state
- `preview` / `convert` / `test-draft` can mislead people into thinking the draft is already in the backend
- if backend draft verification fails, treat the run as unverified or blocked instead of assuming eventual consistency
