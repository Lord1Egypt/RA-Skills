# Workflows

## Role Split

- `weread-skills`: official API documentation and endpoint semantics. Required dependency, installed from `https://cdn.weread.qq.com/skills/weread-skills.zip`.
- `weread-plus`: orchestration, analysis, exports, recommendations, and privacy-safe presentation.

Do not edit `weread-skills`. If official docs and this skill conflict, trust the official skill for endpoint fields and update this skill later.

## Decision Tree

### User asks for a daily book briefing or "每天读一本书"

If the user provides one book title:

```bash
python3 scripts/weread_daily_read.py --book "书名"
```

If the user provides several book titles and wants one book per day:

```bash
python3 scripts/weread_daily_read.py --book "书名 A" --book "书名 B" --book "书名 C" --date "2026-06-22"
```

If the user keeps a book list file:

```bash
python3 scripts/weread_daily_read.py --books-file books.txt --output daily-read.md
```

Then summarize or refine the returned dossier:

- daily selected book and why it was selected
- data boundary: metadata, table of contents, popular highlights, and public reviews; not a full-text replacement
- theory/framework signals
- core viewpoints
- story, plot, or case-study signals
- main conclusions
- public review consensus and disagreements
- reading questions for the user

Popular-highlight coverage:

- `/book/bestbookmarks` returns the whole-book popular highlight list with text and highlight counts, but the official endpoint is fixed to the service's top set and does not paginate.
- `weread_daily_read.py --highlight-scope auto` fetches whole-book highlights and also chapter-level popular highlights when the chapter count is within `--max-chapters`.
- Use `--highlight-scope chapters --max-chapters N` when the user explicitly asks for broader chapter-level extraction. Explain that this is best-effort coverage, not a guaranteed full corpus of every underline on WeRead.
- Keep quotes compact in ordinary answers. Use the fetched highlights as evidence for analysis instead of dumping very long copyrighted passages.

### User asks "what should I read?"

Run:

```bash
python3 scripts/weread_recommend.py --mode expand --count 8
```

If the user provides a topic or goal:

```bash
python3 scripts/weread_recommend.py --goal "主题或目标" --mode expand --count 8
```

If the user provides a seed book:

```bash
python3 scripts/weread_recommend.py --seed-book "书名" --mode expand
```

Then summarize:

- Top 1 pick
- 3-5 alternatives
- why each fits
- why each may not fit
- next action

Default recommendation output excludes books already marked finished by `/shelf/sync` (`finishReading == 1`) and equivalent editions with the same normalized title and author. Only use `--include-finished` when the user explicitly asks for rereads, edition comparison, or retrospective analysis.

### User asks whether a book is worth reading

Run:

```bash
python3 scripts/weread_reviews.py --book "书名" --type all --count 20 --format json
python3 scripts/weread_reviews.py --book "书名" --popular-thoughts --highlight-count 3 --thought-count 5 --format json
```

Then combine:

- book facts
- public review consensus
- praise and criticism patterns
- high-signal popular highlights
- fit for this user when their profile is available

### User asks for other people's reviews

Run:

```bash
python3 scripts/weread_reviews.py --book "书名" --type recommend --count 10 --format markdown
```

Review types:

- `all`: all public reviews
- `recommend`: positive/recommended reviews
- `bad`: low-rated reviews
- `recent`: latest reviews
- `normal`: neutral/general reviews

### User asks who wrote a thought or review

If the user has a review ID:

```bash
python3 scripts/weread_reviews.py --review-id "reviewId" --format json
```

If the user asks about thoughts below popular highlights:

```bash
python3 scripts/weread_reviews.py --book "书名" --popular-thoughts --highlight-count 3 --thought-count 5 --format markdown
```

Only display author fields returned by the API. Do not infer anything else.

### User asks to export personal notes

Run:

```bash
python3 scripts/weread_notes_export.py --book "书名" --format markdown
```

For files:

```bash
python3 scripts/weread_notes_export.py --book "书名" --format markdown --output /path/to/book-notes.md
```

Exports contain personal highlights and personal thoughts. Bookmarks are counted by the official API but bookmark contents are not exportable through the current endpoint.

### User asks for reading report or bookshelf planning

Run:

```bash
python3 scripts/weread_report.py --mode monthly
python3 scripts/weread_report.py --mode annually
python3 scripts/weread_report.py --shelf
```

For planning, combine report output with recommendations:

```bash
python3 scripts/weread_report.py --mode monthly --shelf --format json
python3 scripts/weread_recommend.py --mode expand --count 8 --format json
```

Planning rule: `readLongest` and `recentBooks` from reading reports show what the user spent time on; they are evidence for taste and current focus, not candidate lists. Before putting any report book into a future plan, cross-check the shelf entry and exclude it when `finishReading == 1` or `relatedFinished == true`.

## Error Handling

- Missing `WEREAD_API_KEY`: ask the user to set it.
- `upgrade_info` in API response: stop, tell the user the official skill needs upgrading, and do not continue the workflow.
- Multiple search matches: show candidates and ask the user to choose unless one exact title match is obvious.
- Empty result: state the endpoint returned no data and suggest a narrower query or another review type.
