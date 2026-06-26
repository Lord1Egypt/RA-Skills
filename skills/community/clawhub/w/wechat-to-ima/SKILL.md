---
name: wechat-to-ima
description: Save WeChat Official Account articles into IMA notes or into a named IMA knowledge base with preserved article structure. Use when the user sends an mp.weixin.qq.com link and wants to save, archive, import, collect, or store the article in IMA/笔记/知识库. Handles parsing article metadata, preserving inline body images in order, falling back to the cover image when the body has no images, then either saving to IMA notes or resolving a target knowledge base and adding the article there. When the user asks for a 知识库, route only to that knowledge base and do not create an extra user-visible IMA note.
---

# WeChat to IMA

Save a WeChat article into IMA with two user-facing flows:

1. **解析公众号文章 → 存到 IMA 笔记**
2. **解析公众号文章 → 查知识库 → 加入该知识库**

不要把内部实现细节当成用户流程来描述。

## Workflow

1. Parse the WeChat article.
2. Keep inline body images in original order.
3. If the body contains no inline images, insert the cover image near the top.
4. If the user wants **笔记**: save into IMA notes and read back once to verify the note is not empty.
5. If the user wants **知识库**: resolve the target knowledge base by name or ID, then add the parsed article there as a Markdown knowledge item.

### Flow mapping

- `scripts/save_wechat_to_ima.py <url>` → **解析公众号文章 → 存到 IMA 笔记**
- `scripts/save_wechat_to_ima.py <url> <knowledge_base_name_or_id>` → **解析公众号文章 → 查知识库 → 加入该知识库**

## Requirements

- IMA credentials are required. Configure either:
  - environment variables: `IMA_OPENAPI_CLIENTID` and `IMA_OPENAPI_APIKEY`
  - or local files: `~/.config/ima/client_id` and `~/.config/ima/api_key`
- Python 3 and Node.js must be available.
- Run `npm install` once inside this skill directory so the bundled extractor dependencies are available.
- `skills/ima-skill/ima_api.cjs` is used when present, so this skill stays aligned with the latest IMA OpenAPI wrapper and error handling.

## Setup

### Option A: environment variables

```bash
export IMA_OPENAPI_CLIENTID="<your_client_id>"
export IMA_OPENAPI_APIKEY="<your_api_key>"
```

### Option B: local credential files

```bash
mkdir -p ~/.config/ima
printf '%s' '<your_client_id>' > ~/.config/ima/client_id
printf '%s' '<your_api_key>' > ~/.config/ima/api_key
```

### Install dependencies

```bash
cd skills/wechat-to-ima
npm install
```

## Quick start

### Save to IMA notes

```bash
python3 scripts/save_wechat_to_ima.py "https://mp.weixin.qq.com/s/xxxxx"
```

### Save to a named IMA knowledge base

```bash
python3 scripts/save_wechat_to_ima.py "https://mp.weixin.qq.com/s/xxxxx" "知识库名称"
```

Behavior:

- without a knowledge-base argument → save to **IMA notes**
- with a knowledge-base name or ID → save to **that knowledge base only**, without creating an extra user-visible note

## Common errors

- `missing env: ...` → IMA credentials are not configured yet
- `knowledge base not found: ...` → the specified knowledge base name/ID cannot be resolved
- `knowledge base ambiguous: ...` → multiple knowledge bases matched; use the exact name or ID
- extractor/dependency errors → run `npm install` in this skill directory first

## Output

The script prints JSON with:

- `title`
- `account`
- `author`
- `publish_time`
- `body_img_count`
- `cover_used`
- `markdown_path`
- `note_id`
- `readback_ok`
- `knowledge_base_name` (when requested)
- `knowledge_base_id` (when requested)
- `knowledge_media_id` (when requested)
- `knowledge_file_name` (when requested)

## Notes

- Prefer this skill over ad-hoc manual parsing when the user wants the article stored in IMA.
- This skill is self-contained for article parsing and does not depend on a separate `wechat-article-extractor` installation.
- The IMA readback check uses plain text, so it confirms content landed successfully but does not visually render images in the terminal output.
- When the user names a target knowledge base, this skill resolves the knowledge base by name and routes the article into that knowledge base only.
- Knowledge-base mode should not create an extra user-visible IMA note. Instead, upload the rebuilt Markdown into the target knowledge base as the final artifact.
- Strict target rule: if the user specified a knowledge-base name, do **not** silently substitute another addable knowledge base. If exact resolution fails, stop and report that the requested target is not found/accessible, then use a logged-in IMA desktop/web session or ask for the exact knowledge-base ID.
- If parsing succeeds but the article body has no inline images, that is expected for some articles; use the cover-image fallback instead of treating it as a failure.
- If the original article contains code or code-block-style content, preserve it as fenced Markdown code blocks when importing into IMA; do not flatten code into ordinary prose.
