# Cron: Content Scout

Read {baseDir}/SKILL.md — it contains full content system documentation.
Read the `tg-channel-manager` skill config from openclaw.json.

## Task

Find fresh news and write drafts to content-queue.md.

## Steps

### 1. Search for news

For each query from `config.searchQueries`, run:

```bash
curl '$SEARXNG_URL/search?q=<query (URL-encoded)>&format=json&time_range=day&language=en'
```

### 2. Filtering

- ONLY news from the last 24 hours
- INCLUDE: `config.searchInclude`
- EXCLUDE: `config.searchExclude`

### 3. Decision

- Found fresh interesting news → write a news draft (step 4A)
- Did NOT find news → write an evergreen article draft (step 4B)

### 4A. News Draft

1. Read content-queue.md — do not duplicate topics
2. **MANDATORY** dedup check:
   ```bash
   python3 {baseDir}/scripts/dedup-check.py --base-dir . --topic "topic" --links "url1" "url2"
   ```
   If matches found — DO NOT create a draft, move to the next news item.
3. **MANDATORY** open the source and read its content. Do not write a post from a headline alone!
4. Write a draft following the format from SKILL.md, style per `config.postStyle`
5. Pick a rubric from `config.rubrics` — choose the most fitting one

### 4B. Evergreen Article (if no news found)

1. Read `config.evergreen` — pick a topic
2. Find and read documentation/sources on the topic
3. Write a draft — detailed, in plain language
4. Style per `config.postStyle`, add `articleFooter` if set
5. Pick a rubric from `config.rubrics` — choose the most fitting one

### 5. Write to Queue

Add the draft to content-queue.md with **draft** status (NOT pending!).

## Rules

- Maximum `config.maxDraftsPerRun` drafts per run
- DO NOT PUBLISH anything. Only write drafts to the file
- Do not duplicate existing draft/pending topics
- BEFORE creating — MANDATORY dedup-check.py
- Post language: `config.language`
