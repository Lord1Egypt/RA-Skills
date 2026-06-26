# Clawhub Release Prep

This file contains a ready-to-use release package for publishing `sticker-manager` to Clawhub.

## Recommended Version

- `v0.2.2`

Reason:
- adds a generic animation-preservation rule for collected remote media
- fixes animated sources (for example GIPHY pages) so they resolve to real GIF assets instead of static previews
- rejects static fallback downloads when the source looked animated

## Listing Metadata

### Name

- `sticker-manager`

### Short Description

- `Manage a local sticker library: save, search, tag, import, and recommend reaction images.`

### Short Description (zh-CN)

- `管理本地表情包库：支持保存、检索、打标签、批量导入和上下文推荐。`

### Long Description

`sticker-manager` is an OpenClaw skill for managing a local sticker and reaction-image library across JPG, JPEG, PNG, WEBP, and GIF formats.

It supports:
- saving the latest inbound image or a specific recent image from chat history
- keyword-based lookup
- rename / delete / cleanup operations
- semantic tagging with emotions, scenes, keywords, and descriptions
- model-oriented recommendation payloads
- context-aware recommendation from chat history
- batch collection and batch import
- lightweight source discovery from directories, URLs, and static pages

The skill is designed so the local inventory workflow remains fast and deterministic, while vision-heavy semantic analysis can be delegated to an outer model layer when needed.

### Long Description (zh-CN)

`sticker-manager` 是一个用于 OpenClaw 的本地表情包管理技能，支持 JPG、JPEG、PNG、WEBP、GIF 等格式。

能力包括：
- 保存最新收到的图片，或从最近聊天历史中指定保存图片
- 按关键词检索表情包
- 重命名、删除、清理低质量文件
- 为表情包添加情绪、场景、关键词和描述
- 输出适合模型决策的语义匹配负载
- 基于聊天历史做上下文感知推荐
- 批量收集与批量导入
- 从目录、URL、静态网页做轻量图源发现

这个 skill 的设计重点是让本地库存管理流程稳定、可预期，而需要视觉理解的部分则通过外层模型链补齐。

## Suggested Tags

- `stickers`
- `media`
- `images`
- `library-management`
- `search`
- `recommendation`
- `productivity`
- `openclaw`

## Key Capabilities

- Save stickers from inbound media or recent history
- Search and manage a local sticker library
- Add semantic metadata for better matching
- Generate model-ready recommendation payloads
- Batch import with deduplication
- Discover candidate sticker sources
- Recommend stickers from chat context

## Behavior Notes For Reviewers

- Default sticker library path: `~/.openclaw/workspace/stickers/library/`
- Default inbound media path: `~/.openclaw/media/inbound/`
- Remote URL discovery is lightweight by default:
  - URL items are recorded as `pending`
  - `--fetch-urls` is required for active remote verification
- Vision-related commands output plans and markers for an outer agent/model layer to execute

## Environment Variables

- `STICKER_MANAGER_DIR`
- `STICKER_MANAGER_INBOUND_DIR`
- `STICKER_MANAGER_LANG`
- `STICKER_MANAGER_VISION_MODELS`

## Publish Checklist

- Confirm `SKILL.md` is the uploaded skill definition
- Confirm `README.md` and `README.zh-CN.md` match the current behavior
- Use version `v0.2.2`
- Include the MIT license from `LICENSE`
- Mention that full vision execution depends on the outer model/tool layer
- Do not claim remote URL verification is automatic unless `--fetch-urls` is exposed in the product UI
- Mention that animated sources are preserved as animated assets when validation confirms animation

## Pre-Publish Verification

Run:

```bash
python3 scripts/check_sensitive.py
python3 -m pytest -q
```

Expected:
- sensitive check passes
- all tests pass

Current verified result:
- `74 passed`

## Release Notes Draft

### v0.2.2

Changed:
- collection now uses a generic animation-preservation rule: suffix → Content-Type → downloaded file validation
- documented animation-preservation behavior in `README.md` and `SKILL.md`

Fixed:
- animated GIPHY page sources now resolve to real GIF assets instead of static preview files
- static fallback downloads are rejected when the original source looked animated

