---
name: WeChat Article Summarize
description: Read one or more WeChat public account article links from mp.weixin.qq.com, extract cleaned full text and optional image links, summarize each article in Chinese with summarize, and generate a structured markdown file saved to a user-chosen directory. Use when the user shares WeChat article URLs and wants single-article notes, multi-article daily reports, article summaries, image extraction, or a structured markdown digest. Before processing, first confirm summarize is configured and working, ask whether to include images, and ask where to save the final file.
---

# WeChat Article Summarize

把一个或多个微信公众号文章链接整理成结构化 markdown，支持单篇整理和多篇日报汇总。

## 功能简介

- 读取一个或多个 `mp.weixin.qq.com` 文章链接
- 抽取文章正文、标题、发布时间，以及可选的图片链接
- 自动修复常见的微信正文乱码问题
- 调用 `summarize` 用中文总结全文内容
- 生成结构化 markdown 文件
  - 单篇文章整理
  - 多篇文章汇总 / 日报
- 支持按日期 + 标题，或日期 + 篇数 + 汇总说明命名
- 支持把文件保存到用户指定目录

## 使用前需要确认

在真正开始抓取文章之前，需要先确认：

1. `summarize` 已经配置好 API key，并且可正常使用
2. 是否需要在最终 markdown 中保留图片链接
3. 最终文件保存到哪个目录

## 适用场景

- 总结单篇微信文章
- 把多篇微信文章汇总成一份日报
- 输出适合继续阅读、归档或二次整理的 markdown 文件

## Workflow

### Step 0: Confirm prerequisites before fetching anything

Do not fetch article content until all three items are clear:

1. **summarize is ready**
   - Ask the user to configure summarize API access first if needed.
   - Verify summarize by running a tiny Chinese test.
   - Proceed only if summarize returns a usable `summary`.

2. **Image preference**
   - Ask whether the final markdown should include image links.
   - Map user intent to `include_images=true|false`.

3. **Output directory**
   - Ask where to save the final markdown file.
   - If the user says “下载文件夹”, use `~/Downloads`.
   - Create the target directory if it does not exist.

If any of the three items is missing, stop and ask before continuing.

### Step 1: Extract each WeChat article

For each `mp.weixin.qq.com` URL, run:

```bash
python3 scripts/read_wechat_article.py '<wechat_url>' --out '<temp_dir>'
```

This produces structured metadata, raw HTML, and a first-pass markdown export.

### Step 2: Clean the body text

Do not trust the first-pass article markdown blindly.

If the body contains mojibake or obvious encoding corruption, repair it from `raw.html` by running:

```bash
python3 scripts/fix_wechat_body.py '<raw.html>' --out '<body-fixed.txt>'
```

Use the cleaned body text as the canonical input for summarization.

### Step 3: Summarize in Chinese

Always summarize the cleaned local text, not the original WeChat URL.

Run:

```bash
python3 scripts/summarize_cn.py '<body-fixed.txt>' --out '<summary.json>' --length short
```

or for a combined report:

```bash
python3 scripts/summarize_cn.py '<combined-input.md>' --out '<summary.json>' --length medium
```

The script enforces Chinese output and fails if the returned summary is not sufficiently Chinese.

### Step 4: Normalize summary text before writing markdown

Never write summarize output directly into the final file.

Normalize paragraph breaks and spacing with:

```bash
python3 scripts/normalize_markdown_text.py '<input.txt>' --out '<normalized.txt>'
```

Use this for:
- each single-article summary
- the combined daily-report overview

This prevents ugly line wrapping and mixed-language formatting artifacts.

### Step 5: Build the final markdown

#### Single article

Run:

```bash
python3 scripts/build_mindmap_markdown.py \
  --result '<result.json>' \
  --body '<body-fixed.txt>' \
  --summary '<summary.json>' \
  --output-dir '<chosen-dir>' \
  --include-images true
```

#### Multiple articles / daily report

Run:

```bash
python3 scripts/build_batch_report.py \
  --inputs '<dir1>' '<dir2>' '<dir3>' \
  --output-dir '<chosen-dir>' \
  --include-images true \
  --report-label '微信文章日报'
```

The batch report must:
1. summarize all articles individually
2. summarize the full set as one combined overview
3. place the combined overview first
4. then append each single article section

## Output rules

### Naming

#### Single article

```text
YYYYMMDD-文章标题.md
```

#### Multiple articles

```text
YYYYMMDD-<总文章数量>篇-<汇总说明>.md
```

### Content rules

#### Single article output should contain
- title
- source URL
- publish time
- summarize-generated Chinese summary
- mindmap-style structure
- optional image section

#### Batch report output should contain
- combined daily overview at the top
- combined mindmap
- per-article title, URL, date, summary, and mindmap
- optional image overview

## Non-negotiable quality gates

Before writing the final markdown:

1. **Summary language check**
   - If the summary is not mainly Chinese, retry or fail.

2. **Paragraph normalization**
   - Collapse unnatural line breaks inside prose.
   - Keep markdown headings and bullet lists intact.

3. **Clean body source**
   - Prefer repaired text from `raw.html` when the extracted body is corrupted.

## Bundled scripts

- `scripts/read_wechat_article.py` — fetch WeChat article metadata, body, raw HTML, and image links
- `scripts/fix_wechat_body.py` — repair mojibake and extract clean text from raw HTML
- `scripts/summarize_cn.py` — run summarize in Chinese and enforce a language check
- `scripts/normalize_markdown_text.py` — normalize prose paragraphs and line breaks
- `scripts/build_mindmap_markdown.py` — generate single-article markdown files
- `scripts/build_batch_report.py` — generate multi-article combined reports
- `scripts/run_wechat_mindmap_workflow.py` — orchestrate the full workflow end to end after the required user confirmations
