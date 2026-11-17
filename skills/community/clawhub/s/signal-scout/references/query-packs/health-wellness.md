# Query pack: health, fitness, nutrition, wellness apps

For consumer health/wellness products (fitness tracking, nutrition, GLP-1
companion apps, habit/wellness coaching). Segments are usually the strongest
category here — the pain is widely shared and rarely tied to one addressable
person; treat Individuals as the exception, not the default.

## Query buckets

**Explicit demand**
- `"is there an app that" [job]` on Reddit (r/loseit, r/fitness,
  category-specific subreddits), forums, Facebook groups (public posts only)
- `"[competitor] alternative"`, `"apps like [competitor]"`
- App Store / Google Play review searches for the product's category:
  1-3 star reviews often state the missing feature explicitly

**Pain**
- `"tracking [thing] manually"`, `"spreadsheet for [health metric]"`
- `"wish there was a way to"` combined with the specific health behavior
- Complaints about food logging accuracy, workout tracking friction, or
  medication/dose tracking gaps

**Workaround**
- Public posts describing a manual spreadsheet, paper log, or combination
  of 2-3 apps stitched together for one job — a strong Segment signal when
  it repeats across multiple posters

**Switching**
- `"canceled [competitor] subscription"`, `"[competitor] price increase"`,
  `"stopped using [competitor] because"`
- App Store reviews mentioning a competitor by name as the reason for
  switching or considering switching

**Timing**
- New-year / New-you seasonal posts (January, post-holiday)
- Posts about a new fitness goal or a non-health life event (new job with
  a gym benefit, a move): individual-level timing triggers when a specific
  poster is identifiable. A diagnosis, medication or treatment is never an
  Individual trigger, even when the poster disclosed it (see
  [COMPLIANCE.md](../../../../COMPLIANCE.md): no use of health status for
  any prospect type)
- Regulatory or insurance coverage changes affecting the category (creates
  Company-level partnership timing, e.g. a health plan expanding coverage)

## Source mix specific to this vertical

- Reddit health/fitness/condition-specific subreddits (respect subreddit
  rules on promotion — this skill only observes, never posts)
- App Store and Google Play reviews for the product's own category and
  named competitors
- Public Facebook groups only where posts are visible without joining;
  never bypass a join-gate
- YouTube comments on review/comparison videos for the category
- Health/wellness content sites' comment sections

## Classification notes

- A repeated complaint pattern across many reviews/posts is a **Segment**,
  even if some individual reviewers are named — don't split it into 10
  Individual entries unless several are independently reachable and worth
  1:1 outreach.
- Sensitive-attribute rule applies with extra weight here: never infer or
  target based on a health condition, diagnosis, or treatment, including
  one the person disclosed in the post being cited. Define Segments by the
  job or the workaround (manual meal logging, a spreadsheet of doses) and
  not by a condition.
