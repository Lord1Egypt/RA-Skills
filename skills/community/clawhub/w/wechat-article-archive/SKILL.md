---
name: wechat-article-archive
description: Save WeChat Official Account articles from mp.weixin.qq.com links into a user-specified local folder as Markdown plus a local assets/ image folder. Use when the user provides a WeChat public-account article URL and asks to 保存/归档/下载/导出/存到指定目录/生成 md, especially when they want article.md with WeChat images copied under assets/ instead of saving to IMA or another cloud service.
---

# WeChat Article Archive

Archive a WeChat Official Account article to local files:

```text
target-folder/
  Article title.md
  assets/
    image-01-xxxx.jpg
    image-02-xxxx.png
```

## Workflow

1. Confirm the user provided both:
   - a `mp.weixin.qq.com` article URL
   - a destination folder
2. Run the bundled script from this skill directory:

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/wechat-article-archive"
.venv/bin/python scripts/archive_wechat_article.py "<wechat-url>" "<destination-folder>"
```

3. Read the JSON output and report:
   - Markdown file path
   - `assets/` directory path
   - downloaded image count
   - any image download failures

## Script

Use `scripts/archive_wechat_article.py`.

Arguments:

```bash
.venv/bin/python scripts/archive_wechat_article.py "<url>" "<output_dir>" [--filename "custom.md"] [--skip-images] [--image-timeout 10]
```

Behavior:

- Parses the article with the bundled `extract.js`.
- Preserves title, author, account name, publish time, original link, body text, headings, tables, blockquotes, lists, code blocks, and inline image order.
- Downloads body images into `<output_dir>/assets/`.
- Rewrites Markdown image links to relative `assets/...` paths.
- If the body contains no inline images but the article has a cover image, inserts and downloads the cover image.
- Uses a per-image timeout so slow image hosts do not block the whole task indefinitely.
- Prints a JSON result for verification.

## Dependencies

Run once if dependencies are missing:

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/wechat-article-archive"
npm install
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

If `npm install` fails because of a registry mirror, retry with:

```bash
npm install --registry=https://registry.npmjs.org
```

Required commands:

- `python3`
- `node`
- npm dependencies declared in `package.json`

If `node` is not on PATH but available elsewhere, set:

```bash
NODE=/absolute/path/to/node .venv/bin/python scripts/archive_wechat_article.py "<url>" "<output_dir>"
```

## Errors

- `不支持的链接` → URL is not a supported WeChat article link.
- `访问过于频繁` → WeChat blocked the request temporarily; retry later or use another network/session.
- `extractor not found` → skill files are incomplete.
- `Cannot find module ...` → run `npm install` in the skill directory.
- image failures in JSON → Markdown was created, but one or more images could not be downloaded; report the failures and keep the original URLs in Markdown for those images.
- very slow image downloads → rerun with `--image-timeout 5`, or use `--skip-images` if the user only needs Markdown text and original image URLs.

## Notes

- Prefer this skill only for local file archiving. Do not use it for IMA upload, knowledge-base import, or WeChat message sending.
- Do not create nested folders per article unless the user asks. The destination folder itself is the article archive folder.
- Do not overwrite unrelated files manually. The script creates or reuses the destination folder and `assets/`.
