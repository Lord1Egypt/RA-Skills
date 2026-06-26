# Biweekly SEO Audit Framework

A structured process for auditing SEO performance every two weeks. Designed for SaaS companies running active content programs where catching issues early directly affects pipeline.

## Why Biweekly

- **Monthly is too slow.** A ranking drop on a high-value page can cost 2-4 weeks of traffic before you even notice. By the time you act, you have lost a month of leads.
- **Weekly is too noisy.** Google ranking fluctuations within a 7-day window are normal. Reacting to weekly noise leads to unnecessary rewrites and wasted effort.
- **Biweekly is the sweet spot.** 14 days gives enough data to distinguish real trends from noise, while keeping response time tight enough to prevent compounding losses.

For SaaS companies publishing 4+ articles per month, biweekly audits catch problems before they become expensive.

## Data Sources

Pull data from these sources before each audit. Consistency matters — use the same tools and date ranges every cycle.

### Google Search Console (GSC)

- **Queries:** Top queries by clicks and impressions for the audit period.
- **Pages:** Top pages by clicks, impressions, average position, and CTR.
- **Position changes:** Compare average position for target keywords vs. previous period.
- **Index coverage:** Any new errors, warnings, or excluded pages.
- **Core Web Vitals:** Any pages falling below "Good" thresholds.

**Pull method:** GSC web interface > Performance > set date range to last 14 days. Export as CSV. Compare against previous 14-day export.

### Google Analytics 4 (GA4)

- **Sessions by source/medium:** Organic search sessions vs. previous period.
- **Engagement rate:** Pages with high traffic but low engagement (< 40%) need attention.
- **Bounce rate by page:** Identify content that is ranking but not retaining visitors.
- **Conversion events:** Track signups, demo requests, or trial starts attributed to organic.
- **New vs. returning users:** Shifts in this ratio can signal audience changes.

**Pull method:** GA4 > Reports > Acquisition > Traffic acquisition. Filter to "Organic Search." Set comparison date range.

### Keyword Tracking (SemRush or DataForSEO)

- **Keyword movements:** Any target keyword that moved more than 5 positions (up or down).
- **New ranking keywords:** Keywords your site started ranking for that you were not targeting.
- **Lost keywords:** Keywords where you dropped off page 1 or out of the top 20 entirely.
- **Competitor movements:** Did a direct competitor gain positions on your target keywords?
- **New competitors:** Any new domains appearing in your target SERPs.

**Pull method:** SemRush Position Tracking or DataForSEO SERP API. Export keyword movement report for the 14-day window.

## Audit Template

Use this template for every audit. Store completed audits in a consistent location (e.g., `seo/audits/` directory or a shared doc).

```markdown
## Audit #{N} — {YYYY-MM-DD}
Period: {start date} to {end date}

### Performance vs Previous Period

| Metric                  | This Period | Previous Period | Delta   |
|-------------------------|-------------|-----------------|---------|
| Organic sessions        |             |                 |         |
| Organic clicks (GSC)    |             |                 |         |
| Total impressions (GSC) |             |                 |         |
| Average CTR             |             |                 |         |
| Average position        |             |                 |         |
| Organic signups         |             |                 |         |
| Indexed pages           |             |                 |         |

### Winners (Improving)

Pages or keywords that gained positions, clicks, or impressions.

| Page / Keyword | Metric Improved | Previous | Current | Notes |
|----------------|-----------------|----------|---------|-------|
|                |                 |          |         |       |

What is working? Can this be replicated on other pages?

### Losers (Declining)

Pages or keywords losing positions or traffic. These need immediate investigation.

| Page / Keyword | Metric Declined | Previous | Current | Likely Cause |
|----------------|-----------------|----------|---------|--------------|
|                |                 |          |         |              |

For each loser, determine:
1. Did a competitor publish better content on this topic?
2. Is the content outdated (stats, screenshots, product changes)?
3. Did internal linking change (removed links, changed anchors)?
4. Is there a technical issue (slow load, broken elements, redirect)?

### CTR Check

Any page with >1,000 impressions and <1% CTR has a title/meta description problem. The page is ranking but nobody is clicking.

| Page                | Impressions | CTR   | Current Title | Suggested Fix |
|---------------------|-------------|-------|---------------|---------------|
|                     |             |       |               |               |

Common fixes:
- Add a number or year to the title ("7 Ways to..." or "2026 Guide").
- Include a benefit or outcome in the meta description.
- Add the primary differentiator ("Free," "No Code," "In 5 Minutes").
- Test a question format if the query is a question.

### New Content Performance

How did articles published in the last 30 days perform?

| Article          | Publish Date | Impressions | Clicks | Avg Position | Indexed? |
|------------------|--------------|-------------|--------|--------------|----------|
|                  |              |             |        |              |          |

Expectations:
- New content should be indexed within 3-7 days.
- Initial impressions should appear within 7-14 days.
- If a page has zero impressions after 14 days, check indexing status and submit via GSC.

### Indexing Status

| Issue Type                  | Count | Action Needed |
|-----------------------------|-------|---------------|
| New pages not yet indexed   |       |               |
| Pages with crawl errors     |       |               |
| Pages with redirect issues  |       |               |
| Soft 404s                   |       |               |
| Pages excluded by noindex   |       |               |

If new pages are not indexed:
1. Submit URL via GSC "Request Indexing."
2. Add internal links from high-authority pages.
3. Include the URL in your next sitemap update.
4. Check robots.txt is not blocking the path.

### Action Items

Prioritize by impact. Maximum 5 items per audit — more than that and nothing gets done.

1. [ ] {Highest priority action — usually fixing a declining high-traffic page}
2. [ ] {Second priority — often a CTR optimization}
3. [ ] {Third priority — new content adjustment or indexing fix}
4. [ ] {Fourth priority}
5. [ ] {Fifth priority}

Owner: {who is responsible}
Deadline: {next audit date — all items should be resolved before then}
```

## Updating SEO Files Based on Audit Results

After each audit, update the relevant project files to keep your SEO strategy current.

### Keyword Tracking Files

- **Add new ranking keywords** that appeared organically — these are opportunities to create dedicated content.
- **Flag lost keywords** for recovery. Note the date lost and the likely cause.
- **Update priority scores** based on actual performance vs. projected performance.

### Content Calendar

- **Promote recovery actions** — if a key page is declining, its refresh should jump to the top of the calendar.
- **Add new content ideas** based on keywords where you are ranking 8-15 (striking distance).
- **Remove or deprioritize topics** where audit data shows low potential.

### Technical SEO Backlog

- **Log any new technical issues** found during the audit (crawl errors, Core Web Vitals problems, redirect chains).
- **Track resolution status** of previously logged issues.

### Competitor Files

- **Update competitor notes** if a competitor gained ground on key terms.
- **Note new competitors** appearing in your SERPs for the first time.

## When to Escalate

Not every issue is a routine fix. Escalate immediately (do not wait for the next audit) when:

### Significant Traffic Drop

- Organic sessions drop more than 25% week-over-week without a known cause (holiday, seasonality).
- A page that drives signups or demos loses more than 50% of its traffic.
- Multiple high-value pages decline simultaneously — this signals an algorithmic or technical issue, not a content problem.

**Immediate actions:**
1. Check GSC for manual actions or security issues.
2. Check if a site update (deploy, migration, redesign) coincided with the drop.
3. Check Google's search status dashboard for confirmed algorithm updates.
4. Audit robots.txt and sitemap for accidental changes.

### Deindexing

- Pages that were indexed are no longer in Google's index.
- GSC shows a spike in "Excluded" or "Error" pages.

**Immediate actions:**
1. Check for accidental noindex tags, robots.txt blocks, or canonical tag errors.
2. Check if a recent deploy changed meta tags or page templates.
3. Submit affected URLs for re-indexing via GSC.

### Algorithm Update

- Google confirms a core algorithm update (check Search Central blog and SearchEngineLand).
- Industry-wide ranking volatility is high (check SemRush Sensor or Mozcast).

**Immediate actions:**
1. Do not make panic changes. Algorithm updates take 2-4 weeks to fully roll out.
2. Document which pages were affected and how.
3. Compare affected pages against Google's quality guidelines.
4. Plan content improvements based on the update's focus area (usually content quality, E-E-A-T, or spam).

## Calendar Integration

Audits only work if they actually happen. Build them into your operating rhythm.

- **Schedule audits on the same day every two weeks** (e.g., every other Monday morning).
- **Block 60-90 minutes** for the audit itself. Data pull takes 15-20 minutes. Analysis and action items take 40-60 minutes.
- **Add to the content calendar** as a recurring event. Audit dates should be visible alongside publish dates.
- **Pair audits with content planning** — the audit's findings should directly inform what gets written, refreshed, or deprioritized in the next two-week cycle.
- **Share audit summaries with stakeholders** — a 3-line summary (traffic up/down, top win, top risk) keeps leadership informed without requiring them to read the full audit.

**Suggested cadence:**

```
Week 1, Monday:  SEO Audit + action item assignment
Week 1-2:        Execute action items, publish new content
Week 3, Monday:  SEO Audit + action item assignment
Week 3-4:        Execute action items, publish new content
```

Each audit closes the loop on the previous cycle's action items and opens the next cycle.
