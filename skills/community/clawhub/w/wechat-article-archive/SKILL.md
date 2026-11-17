---
name: wechat-article-archive
description: Save WeChat Official Account articles and image-note / 小绿书 pages from mp.weixin.qq.com into a user-specified local folder as Markdown plus local assets. Use when the user asks to 保存/归档/下载/导出公众号文章、提取多张图片、从浏览器保存的最终 HTML 恢复文章，or generate Markdown with WeChat images copied locally instead of uploading to IMA or another cloud service.
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
.venv/bin/python scripts/archive_wechat_article.py "<url>" "<output_dir>" [--filename "custom.md"] [--skip-images] [--html-file "page.html"] [--image-timeout 30]
```

Behavior:

- Parses the article with the bundled `extract.js`.
- Preserves title, author, account name, publish time, original link, body text, headings, tables, blockquotes, lists, code blocks, and inline image order.
- Downloads body images into `<output_dir>/assets/`.
- Rewrites Markdown image links to relative `assets/...` paths.
- Supports WeChat image-note / 小绿书 pages by extracting every top-level image from `picture_page_info_list` in display order.
- Preserves image-note / 小绿书 body text from the page description, decodes escaped line breaks, and writes the text before the ordered images.
- When `picture_page_info_list` also appears on a normal long article, prefers the substantive structured HTML body instead of replacing it with the short page description and image list.
- Accepts a browser-saved final page source through `--html-file` when direct URL fetching is blocked or returns a different page. Keep the original WeChat URL as the first argument so metadata retains the source link.
- If the body contains no inline images but the article has a cover image, inserts and downloads the cover image.
- Prints a JSON result for verification. Check `body_text_length`, `body_img_count`, `downloaded_image_count`, and `image_failures`; do not treat `ok: true` alone as proof that the article is complete.

## Dependencies

Run once if dependencies are missing:

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/wechat-article-archive"
npm install
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
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
- Image-note / 小绿书 pages use a different WeChat page structure from normal articles. Do not treat an empty `#js_content` as an image-less article when `picture_page_info_list` is present.

## Notes

- Prefer this skill only for local file archiving. Do not use it for IMA upload, knowledge-base import, or WeChat message sending.
- Do not create nested folders per article unless the user asks. The destination folder itself is the article archive folder.
- Do not overwrite unrelated files manually. The script creates or reuses the destination folder and `assets/`.
