# Research and Tool Playbook

Use this reference to execute current social-arbitrage research honestly and reproducibly. It is tool-agnostic: use the strongest available browser, web, search, finance, filing, transcript, and platform tools. Never pretend an unavailable tool worked.

## 1. Preflight and access ledger

Before a current scan:

1. Record the current date, time, and timezone.
2. Determine the requested scope and U.S.-listing universe.
3. Inventory available research tools and signed-in browser surfaces.
4. Check which social platforms, search tools, news sources, SEC data, issuer pages, and market-data tools are actually accessible.
5. Record material access gaps and their expected effect on coverage or confidence.

Use a ledger:

| Channel | Access | Method | Material limitation |
|---|---|---|---|
| Web search | Available / limited / unavailable | Tool used | Indexing or recency limits |
| TikTok | Available / limited / unavailable | Browser or indexed pages | Comment or login limits |
| Reddit | Available / limited / unavailable | API, browser, or indexed pages | Community or rate limits |
| X | Available / limited / unavailable | API, browser, or indexed pages | Auth or search limits |
| YouTube | Available / limited / unavailable | Metadata, captions, comments | Comment or transcript gaps |
| Instagram | Available / limited / unavailable | Browser or indexed pages | Login and metadata limits |
| Google Trends | API / website / unavailable | Exact surface | Relative scaling or access |
| SEC/issuer | Available / limited / unavailable | EDGAR and IR | Filing or bot limits |
| Market data | Available / limited / unavailable | Exact source | Delays or missing fields |

Never claim to have inspected inaccessible posts, comments, accounts, transaction data, or proprietary datasets.

## 2. Define the scan before searching

### Broad default scan

If the user provides no scope:

- Scan all eight sector lenses from `methodology.md`.
- Search for both positive and negative changes.
- Prefer changes observed within the most recent days or weeks, adjusted for the business mechanism.
- Do not force one idea per sector.
- Stop with no qualifying signals if nothing clears the gates.

### Targeted scan

For a named trend, sector, company, geography, or demographic:

- State the exact research question.
- Build competing hypotheses before searching.
- Include obvious and second-order public-company mappings.
- Test whether the supplied observation is true before accepting the user's framing.

### Reassessment

For an older idea:

- Recover the original claim, baseline, evidence date, catalyst, and falsifier.
- Search for new confirming and disconfirming evidence.
- Recheck exposure, materiality, awareness, and price reaction.
- Upgrade, maintain, downgrade, or reject; do not anchor to the prior tier.

## 3. Discovery queries

Search for changed behavior, not only the topic name.

### Change language

- `suddenly`, `now`, `used to`, `stopped`, `switching`, `can't find`, `sold out`
- `waitlist`, `backorder`, `discount`, `clearance`, `canceling`, `downgrade`
- `everywhere`, `first time`, `new favorite`, `replacement`, `alternative`
- `hiring`, `layoffs`, `capacity`, `lead time`, `shortage`, `surplus`

### Intent language

- `where to buy`, `ordered`, `booked`, `installed`, `renewed`, `returned`
- `worth it`, `cancelled`, `switching from`, `replacing`, `using daily`
- `doctor recommended`, `employer requires`, `school adopted`, `developer migrated`

### Baseline and contradiction language

- prior year, prior launch, seasonal pattern, historical average, peer comparison
- inventory, discounting, returns, complaints, churn, wait times, availability
- management guidance, analyst expectations, estimate revisions, price reaction

Build term families for brands, categories, use cases, symptoms, slang, misspellings, competitors, complements, and substitutes. Document ambiguous terms.

## 4. Channel guidance

### TikTok

Use for emerging language, demonstrations, creator spread, comments, and consumer use.

Inspect:

- Post dates and creator history.
- View and comment velocity rather than lifetime totals alone.
- Purchase-intent and repeated-use language.
- Spread across unrelated creators and cohorts.
- Sponsorship, affiliate links, copied scripts, and synthetic engagement.

Do not infer platform-wide volume from a personalized feed.

### Reddit

Use for niche expertise, troubleshooting, adoption narratives, buyer research, and longitudinal community history.

Inspect:

- Account history and incentives.
- Community norms and selection bias.
- Old versus new thread frequency.
- Whether claims link to primary evidence.
- Brigading, stock-promotion communities, and reposts.

### X

Use for real-time professional discussion, product incidents, policy, weather, supply, and event reaction.

Inspect:

- Original source versus quote/repost cascades.
- Account expertise and conflicts.
- Bot-like repetition.
- Whether finance accounts are reacting to already-public news.

### YouTube

Use for long-form demonstrations, interviews, captions, creator history, and comments.

Inspect:

- Upload date, sponsorship, and disclosure.
- Historical performance of the channel.
- Comment persistence and intent.
- Transcript context rather than isolated clips.

### Instagram

Use for fashion, beauty, travel, food, lifestyle, and creator spread. Apply the same sponsorship and authenticity checks as TikTok. If login blocks direct inspection, disclose the gap.

### Niche forums and communities

Use for professional, technical, hobby, medical-provider, industrial, or enthusiast knowledge. Treat small samples and unverifiable identities as limitations. Never expose private personal information.

### Google Trends

Use an authorized API if available; otherwise use the website. The API is limited access and must not be assumed.

Rules:

- Website scores are normalized within each request; they are not absolute search volumes.
- Use a stable anchor term when comparing separate requests when possible.
- Test term versus topic, singular/plural, brand/category, slang, and ambiguous meanings.
- Compare same-season periods and event windows.
- Inspect geography where the business mechanism is regional.
- Treat search as awareness or intent evidence, not confirmed sales.

Official references:

- https://developers.google.com/search/blog/2025/07/trends-api
- https://developers.google.com/search/apis/trends

### Retailers, reviews, pricing, and inventory

Use for availability, assortment, discounting, purchase language, returns, and review velocity.

Check:

- Historical review cadence, not only star rating.
- Seller identity and marketplace versus first-party inventory.
- Geographic or account-specific availability.
- Promotions, bundles, and channel stuffing.
- Whether inventory scarcity reflects demand or supply failure.

### App stores and software communities

Use app rankings, review velocity, release notes, developer forums, package downloads, public repositories, job postings, and integration announcements.

Distinguish:

- Downloads from active use.
- Trials from paid conversion.
- Developer experiments from production workloads.
- Job-posting intent from deployed spend.

### Gaming data

Use Steam or equivalent public activity, reviews, wishlists when available, community behavior, streaming, and publisher disclosure. Distinguish one-time launches from retention and monetization.

### Jobs and labor

Use posting counts, role taxonomy, geography, required skills, seniority, and employer mix. Control for duplicate postings, staffing firms, evergreen requisitions, and seasonal hiring.

### Weather, public agencies, and local reporting

Use official weather, emergency, health, permit, transportation, agriculture, energy, and labor data. Match geography and date to the proposed business effect. Local reporting can expose conditions before national coverage but still needs primary corroboration.

### News and trade publications

Search in diffusion order when practical:

1. Raw behavior and niche communities.
2. Trade and vertical publications.
3. Local and general-interest media.
4. Financial media.
5. Analysts and company disclosure.

Do not confuse this order with source authority. SEC filings are stronger for issuer facts even when they appear later.

### SEC and investor relations

Use primary issuer sources for identity, ownership, segments, geography, customers, suppliers, revenue, margins, inventory, capacity, risk, and management awareness.

Official SEC resources:

- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data

Verify ticker and exchange with another reliable source. SEC mapping alone is not a guarantee.

### Market data

Record as-of values for price, market capitalization, liquidity, recent reaction, valuation when relevant, and upcoming events. Use finance tools for discovery and reliable exchange/issuer sources for confirmation.

## 5. Fallback behavior

When a preferred source is inaccessible:

1. Record it in the access ledger.
2. Decide which gate the gap affects.
3. Use a genuinely independent substitute: indexed public pages, captions, trade reporting, search behavior, retailer data, public datasets, SEC, IR, or market data.
4. Lower confidence or tier if the missing source prevents authentication or corroboration.
5. Return no signal if the remaining evidence cannot clear the gates.

Never:

- Attribute indexed snippets to direct platform inspection.
- Guess unavailable counts or comments.
- Present cached or old data as current.
- Treat one aggregator as multiple sources.

## 6. Baseline selection

For each observation choose at least one primary baseline and, when useful, a control.

| Signal | Useful baseline | Common trap |
|---|---|---|
| Search interest | Same season, prior event, geography, peer term | Relative 0–100 score treated as volume |
| Social posts | Creator/channel normal, prior launch, sustained velocity | Lifetime view count |
| Comments | Historical cadence and intent mix | Repeated or coordinated text |
| Reviews | Review velocity and verified-purchase mix | Static star rating |
| Inventory | Normal stock by region/channel | Supply shortage mistaken for demand |
| Pricing | Historical promotion calendar and peers | Inflation or bundle change |
| App rank | Category, country, prior release | Short paid-acquisition burst |
| Jobs | Duplicate-adjusted historical postings | Evergreen requisitions |
| Weather | Seasonal normal and control region | One local event generalized nationally |

If no defensible baseline exists, call the observation anecdotal and cap it at C.

## 7. Authenticity protocol

For social or review evidence, ask:

1. Is there a disclosed sponsorship, affiliate link, free product, or financial interest?
2. Are wording, timing, visuals, or comments duplicated?
3. Are accounts established and behaviorally plausible?
4. Did one recommendation algorithm create the apparent cluster?
5. Is content recycled, mislabeled, or detached from its date/location?
6. Is a stock promoter involved?
7. Does independent real-world evidence agree?

Affirmative manipulation rejects the signal. Unresolved authenticity caps it at C.

FTC guidance:

- https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- https://www.ftc.gov/news-events/topics/truth-advertising/advertisement-endorsements

## 8. Independence protocol

Create a source-dependency map for A/B candidates:

```text
original observation A ─┬─ repost 1
                        ├─ article copying A
                        └─ aggregator quoting article

independent source B ─── public dataset
independent source C ─── retailer behavior
```

Count the A cluster as one source. Prefer evidence with different collection mechanisms and incentives.

## 9. Business-mechanism protocol

Write separate claims for:

1. The real-world change.
2. The customer/supplier/regulator behavior.
3. The financial variable affected.
4. The issuer segment exposed.
5. The reporting or perception window.

For each arrow assign:

- **Fact:** Directly observed or stated by a primary source.
- **Inference:** Reasoned conclusion from facts.
- **Assumption:** Necessary but unverified condition.
- **Estimate:** Quantified approximation with method.
- **Data gap:** Evidence unavailable or unresolved.
- **Research judgment:** Ranking or interpretation.

Do not hide an assumption inside a factual sentence.

## 10. Issuer and U.S.-listing verification

Before printing an A/B ticker:

- Confirm legal issuer name.
- Confirm ticker and NYSE, Nasdaq, or NYSE American listing.
- Confirm security type is common stock or ADR.
- Exclude OTC, funds, shells, pre-merger SPACs, illiquid microcaps, and default-excluded binary biotech.
- Confirm brand/product/customer/supplier/geography link.
- Confirm segment scale and plausible economics.
- Record market capitalization and liquidity as of the report date.

For ADRs, disclose the foreign operator and relevant geography/currency.

## 11. Exposure attribution

Classify:

- **Direct:** The issuer owns the product, service, or economically exposed operation.
- **Contractual:** A customer, supplier, licensing, distribution, or partnership relationship is verified.
- **Second-order verified:** The trend affects a verified supplier, complement, substitute, channel, or cost bearer.
- **Hypothesized:** Capability or thematic fit exists, but economic exposure is unproven.

Only the first three can reach A/B. Hypothesized mappings are C at most.

## 12. Materiality protocol

Use the best available denominator:

- Segment revenue.
- Units or customers.
- Geographic share.
- Gross or operating margin.
- Capacity and utilization.
- Inventory and working capital.
- Customer or supplier concentration.
- Market capitalization and expectations.

If exact impact cannot be quantified, provide a bounded plausibility argument and name what data would resolve it. Do not write “could be huge” without a denominator.

## 13. Information-gap protocol

Search for the same mechanism in:

- Filings and earnings calls.
- Company presentations and guidance.
- Trade publications.
- General and financial media.
- Analyst notes or estimate revisions when accessible.
- Recent price/volume reaction.

Ask:

- Is the trend known but magnitude misestimated?
- Is the mechanism known but timing misread?
- Is one geography or segment ignored?
- Did price react before the supporting evidence strengthened?
- Is the candidate simply consensus momentum?

If management, analysts, estimates, media, and price substantially recognize the thesis, reject the original wedge unless new incremental evidence changes expectations.

## 14. Catalyst and dominant-event protocol

Potential dissemination events:

- Earnings or guidance.
- Product launch or retailer rollout.
- Monthly/quarterly public data.
- App, traffic, booking, or activity update.
- Regulatory decision.
- Industry conference or investor day.
- Weather progression or repair cycle.
- Price, inventory, or capacity change.

Also identify events that could dominate:

- Macro shock.
- Litigation or regulation.
- Acquisition or divestiture.
- Financing or dilution.
- Large unrelated segment change.
- Product cycle or commodity move.

Do not claim a clean catalyst window when a larger event controls the outcome.

## 15. Source quality and citation

Hierarchy for factual claims:

1. Direct observation, official dataset, SEC filing, issuer material.
2. Reputable trade publication or established data provider.
3. General and financial media.
4. Social post, aggregator, or snippet used as a lead.

Rules:

- Link the underlying page, not a search-results page.
- Include publication/event date and access/as-of date for time-sensitive facts.
- Distinguish publication date from the date an event occurred.
- Do not quote more than needed; paraphrase accurately.
- Preserve source disagreements.
- Do not cite inaccessible content as if inspected.
- Use snippets only to locate the underlying source.

## 16. Currentness and stale-data control

Every report states:

- Current as-of timestamp and timezone.
- Evidence collection window.
- Market-data timestamp.
- Known delays, such as Google Trends or filing updates.
- Which facts could have changed since collection.

Historical examples inform method only. Never use a dated example report as current evidence.

## 17. Stopping conditions

Stop and reject or return no signal when:

- The observation lacks a baseline.
- Authenticity is affirmatively compromised.
- No independent corroboration exists.
- The causal chain cannot be defended.
- No eligible issuer has verified exposure.
- The effect is immaterial.
- The thesis is already consensus without an incremental wedge.
- Listing or identity cannot be verified.
- Possible MNPI contaminates the request.
- The user demands a fixed candidate count that evidence cannot support.

Stop researching when additional sources repeat the same evidence and the next unresolved gate requires unavailable primary data. Name the data gap instead of browsing indefinitely.

## 18. Safety references

- Investor.gov, social-media stock scams: https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/social-media-stock-scams
- Investor.gov, internet and social-media fraud: https://www.investor.gov/protect-your-investments/fraud/types-fraud/internet-and-social-media-fraud
