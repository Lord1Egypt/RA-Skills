name: Vietnam Fullstack Jobs
description: Search ITviec, TopDev, ITJobs, and TopCV for the latest full-stack developer job listings using Firecrawl. Finds jobs with React, Next.js, TypeScript, Node.js, NestJS, and related technologies. Requires firecrawl-search skill and FIRECRAWL_API_KEY env var. Trigger for requests like "tìm việc fullstack", "job mới", "fullstack jobs", or "việc làm lập trình viên".
---

Search ITviec.com, TopDev.vn, ITJobs.com.vn, and TopCV.vn for the latest full-stack developer job listings using the firecrawl-search skill. Summarize results in a clear, scannable format.

---

## Procedure

Run all search queries automatically, without asking for confirmation. Deduplicate results across all queries and sources.

**Step 1 — Search ITviec**

```bash
python3 skills/firecrawl-search/scripts/search.py "site:itviec.com fullstack developer React Node NestJS" --limit 10
python3 skills/firecrawl-search/scripts/search.py "site:itviec.com full-stack TypeScript Next.js" --limit 10
```

**Step 2 — Search TopDev**

```bash
python3 skills/firecrawl-search/scripts/search.py "site:topdev.vn fullstack developer React Node NestJS" --limit 10
python3 skills/firecrawl-search/scripts/search.py "site:topdev.vn full-stack TypeScript Next.js" --limit 10
```

**Step 3 — Search ITJobs**

```bash
python3 skills/firecrawl-search/scripts/search.py "site:itjobs.com.vn fullstack developer React TypeScript NodeJS" --limit 10
python3 skills/firecrawl-search/scripts/search.py "site:itjobs.com.vn full-stack Next.js NestJS" --limit 10
```

**Step 4 — Search TopCV**

```bash
python3 skills/firecrawl-search/scripts/search.py "site:topcv.vn fullstack developer React NodeJS TypeScript" --limit 10
python3 skills/firecrawl-search/scripts/search.py "site:topcv.vn lập trình viên fullstack Next.js NestJS" --limit 10
```

**Step 5 — Fallback scrape (if any source returns fewer than 2 unique results)**

```bash
python3 skills/firecrawl-search/scripts/scrape.py "https://itviec.com/it-jobs/full-stack"
python3 skills/firecrawl-search/scripts/scrape.py "https://topdev.vn/jobs?q=fullstack"
python3 skills/firecrawl-search/scripts/scrape.py "https://www.itjobs.com.vn/vi/search?Keyword=fullstack"
python3 skills/firecrawl-search/scripts/scrape.py "https://www.topcv.vn/tim-viec-lam-lap-trinh-vien-fullstack"
```

**Step 6 — Extract & summarize**

For each unique job listing: extract job title, company, tech stack (if visible), source site, and URL. Group by source site. Within each group, sort newest/most relevant first.

---

## Output Format

```
FULLSTACK JOBS VIỆT NAM — [Date]

== ITVIEC ==
[Job Title] — [Company]
Tech: [Stack if available]
Link: [URL]

== TOPDEV ==
[Job Title] — [Company]
Tech: [Stack if available]
Link: [URL]

== ITJOBS ==
[Job Title] — [Company]
Tech: [Stack if available]
Link: [URL]

== TOPCV ==
[Job Title] — [Company]
Tech: [Stack if available]
Link: [URL]

Tổng: [N] vị trí tìm được từ [M] nguồn
```

**Important:**

- No markdown syntax.
- Respond in Vietnamese — but keep job titles and tech names in English.
- Skip duplicates (same job title + company, regardless of source).
- If a source returns no results, note it briefly and move on.
