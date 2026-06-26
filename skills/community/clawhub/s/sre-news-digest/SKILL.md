---
name: sre-news-digest
description: Generate a categorized and rated news digest from sre.news. Use for creating SRE/DevOps/Solution Architect daily or periodic news summaries with expert scoring, article categorization, and markdown output.
---

# SRE News Digest

Generate a professionally curated, categorized, and rated news digest from [sre.news](https://sre.news) with a senior SRE/DevOps/Solution Architect perspective.

## Workflow

1. **Scrape** — Fetch recent news from sre.news
2. **Read** — Open and read each article to understand its content
3. **Rate** — Score each article (1-5 ⭐) using the scoring rubric
4. **Categorize** — Assign categories from the taxonomy
5. **Format** — Generate the final markdown digest grouped by category

## Step 1: Scrape sre.news

Run the helper script (path relative to this skill's directory):

```bash
python scripts/scrape_sre_news.py [days]
```

The script outputs a JSON array. Each item contains `title`, `url`, `source`, and optionally `date`. The `days` argument filters articles to the requested time range (default: 1 day). If date metadata is unavailable on the page, all articles are returned.

If the script output is incomplete or titles are missing, use the browser to visit `https://sre.news` directly and collect articles manually. When browsing, capture the original article title, URL, and source/publication name for each item.

## Step 2: Read Each Article

Open each article URL and read the content to understand key points, technical depth, and relevance to SRE/DevOps practice. Focus on the article body; avoid following tracker links, ad networks, or unrelated external resources embedded in the page. This step is critical for accurate rating and summarization.

## Step 3: Rate Articles

Rate each article from 1 to 5 stars from a senior SRE/DevOps/Solution Architect perspective. Consult the scoring rubric for detailed criteria:

```
references/scoring-rubric.md
```

## Step 4: Categorize Articles

Assign one or two categories to each article. The scoring rubric file also contains the category taxonomy. Create new categories if existing ones do not fit.

Group articles by their primary category in the final output.

## Step 5: Format Output

Generate the digest in English as a Markdown file. Follow the template structure in:

```
templates/digest_template.md
```

Key formatting rules:

- Title includes the date of the digest
- Articles grouped by category (use `##` for category headers)
- Each article includes: title with link, source, star rating, and a 2-3 sentence expert summary
- Preserve original article titles and URLs exactly as found
- Write summaries from an SRE/DevOps/Solution Architect perspective, highlighting operational impact and practical relevance
- End with a footer crediting sre.news as the source

Save the output to `sre_news_digest.md` in the current working directory, or a user-specified path.
