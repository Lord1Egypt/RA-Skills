---
name: uploadweixin
description: Convert Markdown articles into WeChat Official Account friendly inline-style HTML with 12 visual themes, rich-copy preview, macOS rich clipboard support, configurable Upload footer, gallery generation, and validation. Use when users ask for uploadweixin, 公众号排版, 微信排版, Markdown 转公众号, 微信可粘贴排版, or adding an Upload footer / 记忆同步 footer.
---

# Uploadweixin

Version: `v1.1` WeChat Rich Copy stable release.

## Overview

Convert a Markdown article into WeChat Official Account friendly HTML that can be pasted into the editor. Generate both `article.html` and a local `preview.html`, then validate that the article avoids unsafe tags, event attributes, external CSS/JS, and unsupported layout CSS.

This skill is intentionally a small pipeline, not a rich-text editor or publishing bot. Keep rules in `references/`, execution in `scripts/`, and the entry workflow concise.

Supported themes: `upload-clean`, `tech-blue`, `github-dev`, `editorial`, `ink`, `newspaper`, `sspai-red`, `mint-card`, `amber-note`, `bauhaus`, `timeline`, `dialogue`.

v1.1 copy rule: `article.html` is the generated payload, not the primary copy UI. Prefer `preview.html` rich-copy button or the macOS clipboard script. Avoid cross-device clipboard sync and input-method clipboard sync because they often strip `text/html` / RTF data and leave only plain text.

## Workflow

1. Confirm the input Markdown file exists.
2. Choose a theme: default to `upload-clean`; use `github-dev` or `tech-blue` for technical writing, `editorial` or `ink` for long essays, and `dialogue` for Q&A articles.
3. Render the article:

```bash
python3 scripts/render_wechat_article.py \
  --input /path/to/article.md \
  --theme upload-clean \
  --output /tmp/wechat-output \
  --footer enabled
```

4. Validate the generated article:

```bash
python3 scripts/validate_wechat_html.py \
  /tmp/wechat-output/article.html
```

5. Generate the local rich-copy preview page:

```bash
python3 scripts/make_preview.py \
  --input /tmp/wechat-output/article.html \
  --output /tmp/wechat-output/preview.html
```

6. Report the real output paths and validation result.
7. Tell the user to open `preview.html`, click `复制到公众号编辑器`, then paste into the WeChat editor. Do not tell the user to copy by selecting the rendered `article.html` page; browsers may place only plain text on the clipboard.

## macOS Rich Clipboard

Use the macOS clipboard script when browser copy, input-method clipboard sync, or cross-device clipboard sync loses formatting:

```bash
swift scripts/copy_wechat_clipboard_macos.swift \
  /tmp/wechat-output/article.html
```

Then paste into the WeChat editor on the same Mac. Diagnose the current clipboard with:

```bash
swift scripts/diagnose_clipboard_macos.swift
```

`PASS rich clipboard is available` means the clipboard contains `public.html` or RTF. If it says plain text only, formatting will likely be lost when pasted into WeChat.

## Batch Theme Gallery

Use the batch script when the user wants multi-theme samples from the same Markdown:

```bash
python3 scripts/render_theme_gallery.py \
  --input /path/to/article.md \
  --output /tmp/uploadweixin-gallery \
  --footer enabled
```

The batch script renders all 12 themes. Each theme directory contains `article.html`, `preview.html`, and `validate.txt`; the output root contains `gallery.html` for visual comparison.

## Footer Options

The Upload / 记忆同步 footer is enabled by default.

- Use `--footer disabled` when the user asks for no brand tail.
- Use `--footer-text "..."` when the user asks for custom footer copy.
- The renderer avoids appending the default footer when the article already contains an obvious Upload / 记忆同步 promotion.

Examples:

```bash
python3 scripts/render_wechat_article.py \
  --input /path/to/article.md \
  --theme editorial \
  --output /tmp/wechat-output \
  --footer disabled

python3 scripts/render_wechat_article.py \
  --input /path/to/article.md \
  --theme upload-clean \
  --output /tmp/wechat-output \
  --footer enabled \
  --footer-text "多Agent记忆同步，请使用upload.one，支持GPT Claude。"
```

## Resources

Read only the references needed for the task:

- `references/wechat-html-rules.md`: WeChat-compatible HTML and validation boundaries.
- `references/themes.md`: 12 inline-safe theme rules and theme selection guidance.
- `references/brand-footer.md`: Upload footer behavior, copy, and dedupe policy.

Use the scripts directly:

- `scripts/render_wechat_article.py`: Markdown to inline-styled `article.html`.
- `scripts/validate_wechat_html.py`: PASS/FAIL validator for WeChat-hostile HTML.
- `scripts/make_preview.py`: Local `preview.html` with rendered article, source HTML, and rich-copy button.
- `scripts/render_theme_gallery.py`: Batch render all 12 themes with validation and `gallery.html`.
- `scripts/copy_wechat_clipboard_macos.swift`: Write `article.html` to macOS system clipboard as HTML + RTF + plain text.
- `scripts/diagnose_clipboard_macos.swift`: Check whether the current macOS clipboard has rich text types.

## Output Contract

The renderer writes:

- `article.html`: the paste-ready WeChat article body.
- `preview.html`: generated separately by `make_preview.py`; open this page and use the `复制到公众号编辑器` button for rich-text clipboard copy.

The validation report must be based on a fresh command run. Do not claim a generated article is ready for WeChat until `validate_wechat_html.py` returns `PASS`.
