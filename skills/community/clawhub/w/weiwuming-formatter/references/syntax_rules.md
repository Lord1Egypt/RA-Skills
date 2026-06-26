# WeChat Article Editor Syntax Rules

Use this reference only to map source document structure into the "谓无名" editor syntax. Preserve source wording exactly unless the user asks for rewriting.

## Structure

| Syntax | Use |
|---|---|
| `### 标题 / 作者` | Main title with author when both are explicit in source |
| `## 标题` | Section heading (no `---[dot]` after or before it) |
| `---[dot]` | Visual divider only when explicitly present in the source document |
| `>` | Blockquote/citation |

### Article Structure Order

Every article must follow this order:

1. **编者按** — `>>>` / `<<<`, ~500 chars, after `### 标题 / 作者`
2. **正文** — body text with keyword blocks (books, persons, etc.) inline
3. **目录** (if any) — `---[toc]` ... `---[/toc]`
4. **注释** (if any) — `---[notes]` ... `---[/notes]`
5. **来源说明** — `---[note]` ... `---[/note]` block with push source attribution
6. **作者简介** — `---[bio-title:作者简介]` ... `---[/bio]`
7. **译者简介** (if any) — `---[bio-title:译者简介]` ... `---[/bio]`
8. **延伸阅读** — `---[reading-title:延伸阅读]` ... `---[/reading]`
9. **末尾固定内容** — `[staff:...]` + `---[follow]` ... `---[/follow]` + profile

### ## Heading Rule

- `##` section headings stand on their own. Do **NOT** add `---[dot]` after `##` headings or before them.
- `---[dot]` is only used when the source document explicitly contains a visual divider.

## Editor Notes (编者按)

**Every article must begin with a 编者按** placed after the `### 标题 / 作者` line and before the first `##` section heading.

```markdown
>>>
编者按内容（约500字）：概述文章主要内容，并进行简要评议，点出文章的学术意义或现实关怀，或提出值得进一步思考的问题。语气应与"谓无名"的编辑风格一致——审慎、有见地、保持开放。
<<<
```

Rules:
- The 编者按 must be approximately 500 Chinese characters.
- It must: (1) summarize the main content and key arguments; (2) provide brief editorial commentary.
- The 编者按 is written by the formatter, not copied from the source.

## Notes

```markdown
---[notes]

^[① 注释原文]

---[/notes]
```

Inline note references such as `^①` should be preserved.

## Source Note (来源说明)

Every article must include a `---[note]` block for push source attribution, placed after notes (if any) and before author bio.

```markdown
---[note]

- 本次推送内容为《书名》一书的"章节名"。

- 感谢XXX授权转载。

- 图片源于作者/互联网。

---[/note]
```

Rules:
- The three lines follow this pattern:
  1. 本次推送内容为《书名》一书的"章节名"（或"某某"文章）。— identifies the source work.
  2. 感谢XXX授权转载。— thanks the rights holder (出版社/作者/本人). If the content is original, omit this line.
  3. 图片源于作者/互联网。— credits image source. Use "作者" if images are from the author, "互联网" if from the web.
- Endnote entries within `---[note]` use `- ・ 内容` format.

Use book blocks only when the source already provides a book/info block or the user asks to mark one. Do not search to complete missing fields.

```markdown
[book:封面URL|书名|作者|出版社|年份]
[enbook:封面URL|English Title|Author|Publisher|Year]
[jpbook:封面URL|書名|著者|出版社|年]
```

Rules:
- If cover URL is missing, leave the first field empty: `[book:|书名|作者|出版社|年份]`.
- Do not use placeholder URLs.
- Do not add `[待确认]` or `[信息缺失]` inside the article.
- Keep source-provided metadata as written, even if incomplete; report suspected issues in `校对提醒`.

## Extended Reading

**Every article must include an extended reading section** based on the article's content. Use `douban-mcp` `search-book` as the primary tool to find 2–5 relevant books and add them above the staff entries.

```markdown
---[reading-title:延伸阅读]

[reading-book:书名|作者|译者|封面URL]
[reading-enbook:Title|Author|Publisher|封面URL]
[reading-jpbook:書名|著者|出版社|封面URL]

---[/reading]
```

Rules:
- If `封面URL` is missing, leave it empty. The editor will show a blank book-cover placeholder. Do not invent a URL.
- Book recommendations must be factually accurate and relevant to the article's subject matter.
- Use web search to find correct titles, authors, publishers, and years.
- **Format Rule**: Each field MUST be separated by `|` (pipe character). Do NOT use `、` or other delimiters within fields. Example: `[reading-book:日本现代文学的起源|柄谷行人|赵京华|https://xxx.jpg]`

## Keyword Blocks

**Identify key persons, books, events, and photos mentioned in the article.** Search the web for accurate details and insert the appropriate syntax block **immediately after the paragraph where the keyword is first mentioned**.

### Persons

```markdown
[universal:图片URL|姓名|身份/简介]
```

### Books

```markdown
[book:封面URL|书名|作者|出版社|年份]
[enbook:封面URL|English Title|Author|Publisher|Year]
[jpbook:封面URL|書名|著者|出版社|年]
```

**Important Format Rule**: Each field MUST be separated by `|` (pipe character). Do NOT use `、` or any other delimiter to combine author, publisher, and year into a single field.

- ❌ Wrong: `[jpbook:https://xxx.jpg|书名|作者、出版社、年份]`
- ✅ Correct: `[jpbook:https://xxx.jpg|竹内好全集|竹内好|岩波書店|2005]`

### Events

```markdown
[universal:图片URL|事件名称|简要说明]
```

### Photos

```markdown
[universal:图片URL|图说第一行|图说第二行]
```

### Movies / TV Shows

**If a `[universal:...]` block contains a title that is a movie or TV show, use `douban-mcp` `search-movie` to look up its details and fill in the fields.**

```markdown
[universal:封面URL|片名|导演/主演/年份/简介]
```

Rules:
- Use `douban-mcp` `search-movie` with the title as keyword (`q`).
- Fill in: cover image URL, title, director/cast, year, and a one-line synopsis.
- If the search result is a TV series rather than a movie, still use `search-movie` (it covers both); optionally also call `list-tv-reviews` for additional context.
- If no cover URL is found, leave it empty.

Rules:
- Use `douban-mcp` `search-book` as the primary tool for book lookups; use `douban-mcp` `search-movie` for movie/TV lookups; use web search for persons, events, and other non-book/non-movie keywords.
- If a hosted image URL cannot be found, leave the URL field empty. Do not invent URLs.
- Insert the keyword block right after the paragraph where the keyword first appears, not at the end of the article.
- If uncertain about factual accuracy, report in `校对提醒` rather than writing potentially incorrect data.

## Images

| Syntax | Use |
|---|---|
| `![alt](url)` | Source contains a real hosted image URL |
| `[bio-img:url]` | Bio photo with real hosted URL |
| `[universal:url|第一行|第二行|...]` | Generic image block with real hosted URL |

Rules:
- Word embedded image targets such as `word/media/image1.png` are not hosted URLs.
- If no hosted URL exists, omit the image syntax entirely.
- Report omitted images after the formatted markdown.

## Bio

```markdown
---[bio-title:作者简介]

[bio:简介原文]

---[/bio]
```

Only include `[bio-img:url]` if a hosted URL is provided or present in source.

## Staff and Follow

**Every article must end with two staff entries and the fixed follow section.**

```markdown
[staff:作者姓名|编辑]

[staff:春生、|审校]

---[follow]

东亚视角 全球视野

寻找东亚论述的"虫洞"与"黑洞"

点击下图关注"谓无名"

---[/follow]
```

Rules:
- `[staff:作者姓名|编辑]` — fill with the actual author name(s) from the source document.
- `[staff:春生、|审校]` — the 审校 (reviewer) **always** defaults to `春生、`.
- The fixed follow section is **mandatory for every article**, regardless of whether the source contains it.
- Do not modify the follow section text — it is a fixed footer.

## Validation

Before delivery, check:
- Paired syntax markers are closed.
- No placeholder URL appears.
- No local image path appears as an article image URL.
- Original wording is preserved.
- **编者按** is present (~500 chars) after `### 标题 / 作者` and before the first `##` heading.
- **No `---[dot]`** is placed after or before `##` headings (unless source explicitly has a divider).
- **Article structure order** is correct: 编者按 → 正文 → 目录(如有) → 注释(如有) → 来源说明(`---[note]`) → 作者简介 → 译者简介(如有) → 延伸阅读 → 末尾固定内容.
- **`---[note]` source attribution** is present with push source info.
- **Two staff entries** are present: author as 编辑, `春生、` as 审校.
- **Fixed follow section** is present at the end of the article.
- **Extended reading section** is present above staff entries with relevant book recommendations.
- **Keyword blocks** are inserted after relevant paragraphs for key persons, books, events, and photos.
- Typos, grammar, punctuation, and political/compliance issues are reported separately under `校对提醒`.
