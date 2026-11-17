# Social Arbitrage Report Contract

Use this exact section order for broad current reports. For a narrow follow-up, keep every section relevant to the claim and never omit gates, sources, counterarguments, or falsifiers for brevity.

## Formatting rules

- Lead with the result, not the research chronology.
- Use direct dated links near the claims they support.
- Separate facts from inference and data gaps.
- Call direction a `research bias`.
- Do not provide entries, exits, sizing, leverage, options, allocation, or execution instructions.
- Do not force candidates. Use the no-signal variant when needed.
- Prefer a few defensible candidates to a long speculative list.
- A dated report is stale after its as-of window; say so.

## Full report template

```markdown
# U.S. Social Arbitrage Trend Report

**As of:** YYYY-MM-DD HH:MM timezone
**Scope:** Broad U.S. cross-sector scan or exact targeted scope
**Evidence window:** Exact dates examined
**Universe:** NYSE, Nasdaq, and NYSE American common stocks and ADRs; exclusions stated
**Boundary:** Research watchlist with long/short/neutral research bias; not investment advice or execution guidance

## Access and limitations

| Channel | Access | Method used | Material limitation |
|---|---|---|---|
| Web search | Available / limited / unavailable | Tool or surface | Limitation |
| Social platforms | Per-platform status | Tool or surface | Limitation |
| Google Trends | API / website / unavailable | Exact surface | Scaling or delay |
| SEC and issuer sources | Status | EDGAR / IR | Limitation |
| Market data | Status | Source | Timestamp or missing field |

State how access gaps affect coverage or confidence. Never imply access that did not occur.

## Executive summary

- **Observations reviewed:** count or honest qualitative description
- **A — Immediate research:** count
- **B — Active watchlist:** count
- **C — Early signal:** count
- **Rejected:** count
- **Highest-priority conclusion:** one sentence or `No qualifying A/B signals`
- **Largest evidence gap:** one sentence

Summarize at most three conclusions. Do not invent counts when the research surface cannot support them.

## Sector and channel coverage

| Lens | Channels examined | Meaningful change found | Coverage gap |
|---|---|---|---|
| Consumer / retail | ... | ... | ... |
| Technology / AI | ... | ... | ... |
| Media / gaming | ... | ... | ... |
| Healthcare / wellness | ... | ... | ... |
| Travel / housing / finance | ... | ... | ... |
| Industrials / energy | ... | ... | ... |
| Weather / climate / agriculture | ... | ... | ... |
| Labor / policy / culture | ... | ... | ... |

## Ranked research watchlist

| Tier | Ticker / company | Research bias | Detected change | Exposure | Awareness | Evidence confidence | Next discriminating event |
|---|---|---|---|---|---|---|---|
| A/B/C | TICKER — Company | Long / Short / Neutral | One sentence | Direct / contractual / verified second-order / hypothesized | Undiscovered / emerging / partially disseminated / consensus | High / medium / low with reason | Exact event or evidence |

For ADRs, identify the foreign operating company and relevant geography.

## A/B research cards

### TICKER — Company — Tier — Directional research bias

**1. Why it surfaced**
State the original observation and how it was discovered.

**2. Baseline and detected change**
State comparison period, metric or qualitative evidence, acceleration/persistence/breadth, and limitations.

**3. Evidence timeline**

| Date | Evidence | Claim type | Source | What it supports |
|---|---|---|---|---|
| YYYY-MM-DD | Observation | Fact / inference / estimate / data gap | [Direct source](URL) | Exact gate or mechanism |

**4. Authenticity and corroboration**
Disclose sponsorship, bot, duplication, account, recycled-content, selection-bias, and independence checks. Identify at least two independent evidence channels.

**5. Business-impact mechanism**

`observed change → behavior → financial variable → exposed segment → possible result or expectations effect`

Label unsupported arrows.

**6. Issuer exposure and materiality**
Verify legal issuer, ticker, exchange, security type, product/brand/customer/supplier/geography link, segment denominator, market capitalization, liquidity, and as-of dates. Distinguish direct from second-order exposure.

**7. What the market probably knows**
Summarize company disclosure, trade/general/financial coverage, analyst or estimate context when available, and recent price reaction. Classify awareness.

**8. Why now and dissemination path**
State what changed now, likely catalyst, reporting window, and any dominant competing event.

**9. Strongest counterargument**
Present the best evidence-based alternative, not a token disclaimer.

**10. First rejection test**
Name the quickest high-information check that could eliminate the idea.

**11. Falsifiers**

- Observable condition that breaks the trend claim.
- Observable condition that breaks exposure or materiality.
- Observable condition that breaks the information gap or timing.

**12. Data gaps and next actions**

- Missing evidence.
- Exact source or query to revisit.
- Date or threshold for reassessment.

## C-tier early signals

| Observation | Possible ticker | Research bias | Passed gates | Unresolved gates | Next proof needed |
|---|---|---|---|---|---|
| ... | TICKER or `none` | Long / Short / Neutral | ... | ... | ... |

State: `C-tier tickers are mapping hypotheses, not investable candidates.`

## Rejected false positives

| Observation | Tempting mapping | Rejection reason | Evidence that would reopen it |
|---|---|---|---|
| ... | TICKER or theme | Static popularity / manipulation / single source / weak mechanism / no exposure / immaterial / consensus / ineligible | Exact evidence |

## Monitoring plan

| Candidate or observation | What to monitor | Source/query | Confirmation threshold | Rejection threshold | Next review |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | YYYY-MM-DD or event |

## Bottom line

State the highest-priority research work and unresolved risk. Repeat that directional labels are research biases, not recommendations.
```

## No-qualifying-signals variant

Use this when no A/B candidate clears the gates:

```markdown
# U.S. Social Arbitrage Trend Report

**As of:** YYYY-MM-DD HH:MM timezone
**Result:** No qualifying A/B signals

## Why the set is empty

State which gates most often failed and whether access gaps affected the result. Do not apologize for an empty set.

## Coverage

Include the sector/channel table and access ledger.

## C-tier observations

List only reproducible early changes and their unresolved gates. A possible ticker may appear only as a clearly labeled mapping hypothesis.

## Rejected false positives

List the strongest tempting ideas and why they failed.

## Monitoring plan

State what future evidence could create a candidate and when to revisit it.

## Bottom line

No current observation satisfied change, authenticity, corroboration, mechanism, exposure, materiality, information-gap, falsifiability, and U.S.-universe requirements. This is a research result, not a request to lower standards.
```

## Targeted-report adaptation

For one trend or ticker, replace the broad sector table with:

- Claim being tested.
- Competing hypotheses.
- Evidence channels examined.
- Gate-by-gate verdict.
- Issuer mapping comparison.

Keep the research card, rejected alternatives, monitoring plan, access ledger, as-of timestamp, sources, counterargument, and falsifiers.

## Final audit before responding

For every A/B ticker verify:

- [ ] U.S. listing and security type.
- [ ] Current as-of time.
- [ ] Change versus baseline.
- [ ] Timestamped evidence.
- [ ] Authenticity checks.
- [ ] Two independent evidence channels.
- [ ] Causal business mechanism.
- [ ] Direct or verified second-order exposure.
- [ ] Plausible materiality denominator.
- [ ] Awareness and price-reaction analysis.
- [ ] Long, short, or neutral **research bias**.
- [ ] Strongest counterargument.
- [ ] First rejection test.
- [ ] Observable falsifiers.
- [ ] Direct dated source links.
- [ ] Data gaps and next actions.

If any required gate is affirmatively failed, move the idea to Reject. If an important gate is unresolved, lower the tier and label it. Never silently omit the failed field.
