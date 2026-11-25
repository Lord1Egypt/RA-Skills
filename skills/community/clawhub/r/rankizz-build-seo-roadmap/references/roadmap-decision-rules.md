# Roadmap decision rules

These are planning heuristics, not Google ranking rules.

## Evidence hierarchy

Prefer evidence in this order:

1. first-party Search Console and Analytics outcomes
2. directly observed page and live SERP evidence
3. Rankizz provider estimates and metrics
4. clearly labeled inference

Never replace a missing higher-quality source with an unlabeled estimate.

## Authority

Ahrefs DR is a relative, logarithmic estimate of backlink-profile strength. Google does not use DR as a ranking factor. Use it to choose realistic competitors and expose backlink gaps, not to decide whether a site deserves to rank.

Referring domains matter more than many repeated links from one site. Review relevance, editorial context, dofollow status, source-page quality, spam signals, and whether links point to the pages that need support.

## Traffic and opportunity

Treat a complete 28-day window as the minimum quick baseline and 90 days as the better view for low-volume or seasonal sites. Compare like-for-like periods when seasonality matters.

Search Console average position is an aggregate, not an exact rank. Focus on trends in clicks and impressions plus query/page evidence.

For low-authority sites, volume `>=1000` and KD `0–10` is a useful preferred screen only after business relevance and intent. If no valid candidates meet it, say so and use lower-volume or higher-KD opportunities with better conversion fit rather than fabricating an ideal list.

## Competitor labels

Use the owner's measured DR as a reference:

- **Proof competitor:** equal or lower DR and already visible in the live top 20 for a target query.
- **Peer SEO competitor:** roughly within 10 DR points and competing for the same intents.
- **Stretch competitor:** materially stronger but still useful for a specific page or format comparison.
- **Aspirational competitor:** substantially stronger or broader; learn from patterns but do not use it as the only benchmark.

Business competitors and SEO competitors are not interchangeable. Use SERP overlap and query intent to name SEO competitors.

## Page-type choice

Prefer product-led utility when all are true:

- the query implies a task that an interactive experience can complete
- the business can build and maintain real functionality
- the page has a clear differentiated outcome
- live results support the format or reveal an underserved need

Otherwise choose the page type searchers expect: product, category, comparison, guide, reference, case study, template, or another appropriate format. Avoid thin programmatic pages and fake tools.

## Optimization priority

Prioritize an existing page when it has meaningful impressions, ranks roughly 4–20, converts, or already owns relevant links. Diagnose intent and quality before changing titles or adding text.

Prioritize a new page when no current URL satisfies a distinct intent and creating it will not introduce cannibalization.

## Backlink goal

For DR below 60, keep a parallel authority workstream. Size the target from:

- the relevant referring-domain gap to proof/peer competitors
- the number of linkable assets that can actually ship
- outreach capacity and existing relationships
- page-level authority needs

Report a range and separate controllable activities from acquired-link outcomes.

## Official research basis

Retrieved 2026-08-16:

- Google, helpful and reliable people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google, Search ranking systems and link analysis: https://developers.google.com/search/docs/appearance/ranking-systems-guide
- Google, page experience: https://developers.google.com/search/docs/appearance/page-experience
- Google, crawlable internal links and anchor text: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google, spam policies including scaled content and link abuse: https://developers.google.com/search/docs/essentials/spam-policies
- Google Search Console, performance use cases: https://support.google.com/webmasters/answer/17010961
- Google Search Console, metric aggregation: https://support.google.com/webmasters/answer/17011364
- Ahrefs, Domain Rating definition: https://help.ahrefs.com/en/articles/1409408-what-is-domain-rating-dr
- Ahrefs, DR is not a search-engine ranking factor: https://help.ahrefs.com/en/articles/907673-do-search-engines-use-domain-authority-domain-rating-as-a-ranking-factor
