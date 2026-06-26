---
name: wechat-formatter
description: |
  Convert uploaded .doc/.docx files or pasted text into WeChat article markdown using the "谓无名" editor syntax.
  Use when the user uploads Word documents, pastes article text, asks to format for WeChat, add syntax markers,
  排版文章, or convert academic/articles into the custom WeChat editor markdown. The skill preserves source content,
  extracts Word structure, and produces editor-ready markdown without inventing missing information or image URLs.
compatibility:
  - Python 3 standard library for .docx OOXML extraction
  - LibreOffice/soffice for legacy .doc normalization when available
  - Codex file read/write capabilities
---

# WeChat Article Formatter

Convert Word documents and pasted text into markdown for the "谓无名" WeChat article editor.

## Core Rules

- Preserve the uploaded document's content, order, wording, punctuation, names, dates, and citations as faithfully as possible.
- Do not rewrite, polish, summarize, expand, translate, or fact-complete the article unless the user explicitly asks.
- Do not search online to fill missing book/person/publication data — **exception: keyword blocks and extended reading recommendations always require web search** to find accurate person, book, event, and photo information.
- Do not invent placeholders such as `https://placeholder`, `[待确认]`, or `[信息缺失]` in the formatted article.
- If an image has no usable hosted URL, do not output standalone image syntax for it.
- **Keyword block images are uploaded to a public image host and URLs filled into syntax** — after downloading images to a local `images/` folder, each image is automatically uploaded to `https://img.scdn.io/api/v1.php` (public image host). The returned URL is then inserted into the corresponding syntax field. If the upload fails, fall back to an empty image field and report in `校对提醒`.
- For book/reading-book blocks that are already present in the source but lack a cover URL, leave the image field empty (e.g. `[book:|书名|作者|出版社|年份]`); if an image is available and uploaded successfully, the returned URL will be filled in.
- If typos, grammar issues, punctuation issues, or political/compliance risks are found, keep the formatted article faithful to the source and report the issues after the markdown under `校对提醒`.

### 编者按（Editor's Note）

- **Every article must begin with a 编者按** placed after the `### 标题 / 作者` line and before the first `##` section heading.
- **Syntax format**: `>>>` must be on the same line as the content start, and `<<<` must be on a separate line at the end.
  - Correct:
    ```
    >>> 编者按内容...
    <<<
    ```
  - Incorrect:
    ```
    >>>
    编者按内容...
    ```
- The 编者按 should be approximately 500 characters (Chinese) and must:
  1. Summarize the main content and key arguments of the article.
  2. Provide a brief editorial commentary — highlighting significance, raising questions, or connecting to broader context.
- Write the 编者按 in a tone consistent with the "谓无名" editorial style: thoughtful, measured, and intellectually engaging.

### Article Structure Order

Every article must follow this order:

1. **编者按** — `>>>` / `<<<`, ~500 chars, after `### 标题 / 作者`
2. **正文** — body text with keyword blocks (books, persons, etc.) inline
3. **目录** (if any) — `---[toc]` ... `---[/toc]`
4. **注释** (if any) — `---[notes]` ... `---[/notes]`
5. **来源说明** — `---[note]` ... `---[/note]` block with:
   - 本次推送内容为《书名》一书的"章节"。
   - 感谢XXX授权转载。
   - 图片源于作者/互联网。
6. **作者简介** — `---[bio-title:作者简介]` ... `---[/bio]`
7. **译者简介** (if any) — `---[bio-title:译者简介]` ... `---[/bio]`
8. **延伸阅读** — `---[reading-title:延伸阅读]` ... `---[/reading]`
9. **末尾固定内容** — `[staff:...]` + `---[follow]` ... `---[/follow]` + profile

### ## Heading Rule

- `##` section headings must always be followed by `---[dot]`. The `##` and `---[dot]` are bound together as a single unit.
- Every `##` heading line must be immediately followed by a separate `---[dot]` line.
- `###` subheadings do NOT have `---[dot]` after them. Only `##` headings use `---[dot]`.

---

### Keyword Blocks and Extended Reading

- **Search for key information mentioned in the article**: identify important persons, books, events, movies, and TV shows referenced in the text.
- **Use `web-access` skill for all web searches and page fetching.** Search strategy:
  - **Priority: search Douban** for books, movies, and TV shows first
  - For discovering information sources and keyword searches: use **WebSearch** via web-access skill
  - For extracting specific information from known URLs: use **WebFetch** via web-access skill
  - For non-public content or sites requiring login: use **browser CDP** via web-access skill
  - Always prioritize first-hand sources (official websites, original documents) over secondary reporting
- **Image download, upload, and URL insertion**: All images are downloaded locally first, then uploaded to the public image host `https://img.scdn.io/api/v1.php`. The returned URL is inserted into the corresponding syntax field.
  - After obtaining Douban item_id, construct the source URL as:
    - Books: `https://dou.img.lithub.cc/book/<id>.jpg`
    - Movies: `https://dou.img.lithub.cc/movie/<id>.jpg`
    - TV shows: `https://dou.img.lithub.cc/tv/<id>.jpg`
    - Music: `https://dou.img.lithub.cc/music/<id>.jpg`
  - **Download** each image to the `images/` directory under the same project folder using Bash (`curl -L -o` or PowerShell `Invoke-WebRequest`).
  - **Naming convention** (use Chinese name, remove punctuation `《》·：` etc., keep alphanumeric and CJK):
    - Book covers: `book_<书名>.jpg` — e.g. `book_浮世通鉴日本大众文化史.jpg`
    - Person photos: `person_<姓名>.jpg` — e.g. `person_鲁迅.jpg`
    - Movie/TV posters: `movie_<片名>.jpg` — e.g. `movie_千与千寻.jpg`
    - Extended reading covers: `reading_<书名>.jpg` — e.g. `reading_菊与刀.jpg`
    - If filename conflicts occur, append `_2`, `_3` etc.
  - **Upload to image host**: after downloading each image, immediately upload it via curl:
    ```
    curl -s -X POST -F "image=@images/<filename>.jpg" -F "outputFormat=webp" -F "cdn_domain=edgeoneimg.cdn.sn" https://img.scdn.io/api/v1.php
    ```
    - Parse the JSON response; on success (`"success": true`), extract the `url` field (e.g. `https://img.scdn.io/i/xxx.webp`).
    - Use `outputFormat=webp` for static images (recommended for better compression).
    - If the upload fails (rate limit 429, server error 500, etc.), fall back to an empty image field and report in `校对提醒`.
    - If multiple images need uploading, add a brief pause (1 second) between uploads to avoid hitting the rate limit (5 requests / 5 seconds).
  - **Insert returned URL into syntax**: fill the image/cover field with the uploaded URL:
    - `[book:https://img.scdn.io/i/xxx.webp|书名|作者|出版社|年份]` (URL filled)
    - `[universal:https://img.scdn.io/i/xxx.webp|姓名|身份/简介]` (URL filled)
    - `[reading-book:书名|作者|译者|https://img.scdn.io/i/xxx.webp]` (cover URL filled)
    - If upload failed: `[book:|书名|作者|出版社|年份]` (empty, fallback)
  - Example: after searching Douban for book ID 35769236, download as `book_浮世通鉴日本大众文化史.jpg`, upload to image host, get URL `https://img.scdn.io/i/abc123.webp`, output as `[book:https://img.scdn.io/i/abc123.webp|浮世通鉴：日本大众文化史|日文研项目组 编著，党蓓蓓 译|北京大学出版社|2025]`
- **Search timeout handling**: if a search takes too long, times out, or returns no results after reasonable attempts, leave the image URL field empty (no download or upload needed):
  - `[universal:|姓名|身份/简介]` (no image URL)
  - `[book:|书名|作者|出版社|年份]` (no image URL)
  - Report missing search results in `校对提醒`.
- **Upload failure handling**: if the image host upload fails (rate limit, server error, timeout), fall back to an empty image field and report in `校对提醒`:
  - `[book:|书名|作者|出版社|年份]` (upload failed, empty image field)
  - The local file in `images/` is still available for manual upload if needed.
- Insert the appropriate syntax block **immediately after the paragraph where the keyword is first mentioned**:
  - Persons → `[universal:<uploaded_url>|姓名|身份/简介]` (download photo to `images/person_<姓名>.jpg`, upload, fill URL; or empty if upload failed)
  - Books → `[book:<uploaded_url>|书名|作者|出版社|年份]` / `[enbook:<uploaded_url>|Title|Author|Publisher|Year]` / `[jpbook:<uploaded_url>|書名|著者|出版社|年]` (download cover to `images/book_<书名>.jpg`, upload, fill URL; or empty if upload failed)
    - **Field separator rule**: each field MUST be separated by `|`, do NOT use `、` or other delimiters within fields.
    - **Book name**: do NOT add 《》 or similar punctuation around the book name.
    - Example: `[book:https://img.scdn.io/i/abc123.webp|浮世通鉴：日本大众文化史|日文研项目组 编著，党蓓蓓 译|北京大学出版社|2025]` (cover downloaded and uploaded)
    - Incorrect: `[book:xxx.jpg|《书名》|作者，出版社，年份]` (missing separators and extra punctuation)
  - Movies/TV → `[universal:<uploaded_url>|片名|导演/主演/年份/简介]` (download poster to `images/movie_<片名>.jpg`, upload, fill URL; or empty if upload failed)
  - Events → `[universal:图片URL|事件名称|简要说明]`
  - Photos → `[universal:图片URL|图说第一行|图说第二行]`
- **Movie/TV detection**: if a `[universal:...]` block contains a title that is a movie or TV show (e.g., a well-known film title, drama series name), search **Douban** first to get its item_id, download the poster to `images/movie_<片名>.jpg`, upload to image host, and fill the URL in the syntax.
- If a search cannot find a real hosted image URL, leave the URL field empty (e.g., `[book:|书名|作者|出版社|年份]`). Do not invent URLs. No file is downloaded or uploaded in this case.
- **Extended reading recommendations**: based on the article's subject matter, use web-search to find 2–5 relevant books on **Douban** and add them in a `---[reading-title:延伸阅读]` / `---[/reading]` block **above the staff entries**. Format: `[reading-book:书名|作者|译者|<uploaded_url>]` — fields MUST be separated by `|`, cover URL filled from image host upload (download cover to `images/reading_<书名>.jpg`, upload, fill URL; or empty if upload failed).
- All searched data must be factual. If uncertain, report in `校对提醒`.

### Staff and Fixed Footer

- The last section of every article must contain **two `[staff:...]` entries**:
  1. `[staff:作者姓名|编辑]` — filled with the actual author name(s) from the source.
  2. `[staff:春生、|审校]` — the 审校 (reviewer) always defaults to **春生、**.
- After the staff entries, **every article must include the fixed follow section**:
  ```
  ---[follow]

  东亚视角 全球视野

  寻找东亚论述的"虫洞"与"黑洞"

  点击下图关注"谓无名"

  ---[/follow]
  ```
- This footer block is mandatory for all articles, regardless of whether the source contains it.

## Workflow

1. Detect input type.
   - For `.docx`, run `python scripts/extract_docx.py <file.docx>`.
   - For legacy `.doc`, use the same script. It detects the OLE container and tries LibreOffice conversion to `.docx` before extraction.
   - For pasted text, analyze the text directly.

2. Analyze structure.
   - Preserve paragraph order from the extraction JSON `content` array.
   - Use style hints, heading levels, alignment, bold runs, tables, footnotes, endnotes, and image relationships only as formatting clues.
   - Treat tables as source content. Convert simple tables to readable text blocks; if a table is structurally important, preserve rows in markdown table form.

3. Apply editor syntax. Read `references/syntax_rules.md` when exact syntax is needed.
   - Main article title or chapter heading: `### 标题 / 作者` when the source clearly contains both.
   - **编者按**: write ~500-char editorial summary/commentary with `>>>` on the same line as content start, placed after `### 标题 / 作者` and before the first `##` heading.
   - Section heading: `## 标题` followed by `---[dot]` (always bound together).
   - Major visual divider from source: do NOT use `---[dot]` for this (already included after `##`).
   - Blockquote: `> 原文`.
   - Notes: `---[notes]` ... `---[/notes]`; note entries use `^[① 内容]`.
   - Source note: `---[note]` ... `---[/note]` for push source attribution (本次推送内容为..., 感谢...授权转载, 图片源于...).
   - Bio: `---[bio-title:作者简介]`, `[bio:原文]`, `---[/bio]`.
   - **Keyword blocks**: after identifying key persons/books/events/photos in the article, use `web-access` skill for all searches (WebSearch for keyword searches, WebFetch for URL-based extraction, CDP for complex sites); download images to `images/` directory, upload to image host, then insert `[book:<url>|...]`, `[universal:<url>|...]`, etc. blocks (with uploaded URL) right after the paragraph where each keyword first appears. If upload failed, use empty image field as fallback.
   - **Extended reading**: use `web-access` skill web-search to find related books and add `---[reading-title:延伸阅读]` ... `---[/reading]` block above staff. Format: `[reading-book:书名|作者|译者|<url>]` — fields MUST be separated by `|`, cover URL filled from image host upload (download cover to `images/reading_<书名>.jpg`, upload, fill URL; or empty if upload failed).
   - Staff credit: `[staff:作者姓名|编辑]` + `[staff:春生、|审校]` (reviewer always defaults to 春生、).
   - Follow section: the fixed `---[follow]` ... `---[/follow]` footer is mandatory for every article.

4. Handle images.
   - Extracted Word image relationships are local package targets, not hosted URLs.
   - Do not emit `![alt](...)`, `[bio-img:...]`, or `[universal:...]` for local package targets unless the user provides a real hosted URL.
   - If the source text already contains a hosted image URL, download it to `images/` and then upload to the image host.
   - **Image upload workflow**: for each downloaded image in `images/`:
     1. Create the `images/` directory in the project folder if it does not exist.
     2. Download each image using Bash (`curl -L -o images/<filename>.jpg`) or PowerShell (`Invoke-WebRequest -Uri <url> -OutFile images/<filename>.jpg`).
     3. Upload the local file to the image host:
        ```bash
        curl -s -X POST -F "image=@images/<filename>.jpg" -F "outputFormat=webp" -F "cdn_domain=edgeoneimg.cdn.sn" https://img.scdn.io/api/v1.php
        ```
     4. Parse the JSON response:
        - On success (`"success": true`): extract the `url` field and insert it into the corresponding syntax block (e.g. `[book:https://img.scdn.io/i/xxx.webp|书名|作者|出版社|年份]`).
        - On failure: leave the image field empty (e.g. `[book:|书名|作者|出版社|年份]`) and report in `校对提醒`.
     5. If uploading multiple images, add a 1-second pause between uploads to stay within rate limits (5 requests / 5 seconds).
   - At the end, report all uploaded images with their URLs and corresponding keywords, plus any local-only fallback images.

5. Validate before delivery.
   - No placeholder URLs or invented missing-data markers are present.
   - All image URLs in syntax blocks are valid `https://img.scdn.io/i/...` links from successful uploads, or empty fields for failed uploads/search misses.
   - No unsupported local image paths are emitted as article image URLs.
   - All downloaded images exist in `images/` directory with correct naming (local backup).
   - Syntax markers are paired: `>>>`/`<<<`, `---[notes]`/`---[/notes]`, `---[note]`/`---[/note]`, `---[reading-title:]`/`---[/reading]`, `---[bio-title:]`/`---[/bio]`.
   - The article follows the correct structure order: 编者按 → 正文 → 目录(如有) → 注释(如有) → 来源说明(`---[note]`) → 作者简介 → 译者简介(如有) → 延伸阅读 → 末尾固定内容.
   - Every `##` heading is followed by `---[dot]`.
   - Suspected typos, grammar, punctuation, and political/compliance issues are listed separately, not silently corrected.

## Reporting Format

Return:

```markdown
排版结果：

<editor-ready markdown>

图片处理结果：
- ✅ `images/book_书名.jpg` → 已上传 → https://img.scdn.io/i/xxx.webp → [book:https://img.scdn.io/i/xxx.webp|书名|...]
- ✅ `images/person_姓名.jpg` → 已上传 → https://img.scdn.io/i/yyy.webp → [universal:https://img.scdn.io/i/yyy.webp|姓名|...]
- ❌ `images/movie_片名.jpg` → 上传失败 → [universal:|片名|...]（本地文件已保留，可手动上传）

校对提醒：
- 未发现明显问题。
```

If issues exist, list them with source snippets and a concise reason:

```markdown
校对提醒：
- 可能错别字："..."，建议核对是否应为 "..."。
- 标点疑点："..."，中英文标点混用，建议人工确认。
- 政治/合规风险："..."，建议人工复核表述是否符合发布要求。
- 图片处理：第 N 处图片上传失败，已留空图片字段；本地文件 `images/<filename>.jpg` 已保留，可手动上传至图床后填入。
- 图片下载失败：<关键词>，未找到可用图片源。
- 图片上传失败：<关键词>，图床返回错误 <error_message>，已留空图片字段。
```

## Word Extraction Notes

The bundled extractor adopts the `minimax-docx` approach:

- Detects file signature instead of trusting extensions.
- Treats `.docx` as an OOXML ZIP package.
- Converts `.doc` to `.docx` through LibreOffice when available.
- Uses Python standard-library XML parsing instead of `python-docx`.
- Extracts paragraphs, style names, alignment, run bold/italic/size hints, tables, footnotes/endnotes, and image relationships.

If `.doc` conversion fails or LibreOffice is unavailable, ask the user for a clean `.docx` export.
