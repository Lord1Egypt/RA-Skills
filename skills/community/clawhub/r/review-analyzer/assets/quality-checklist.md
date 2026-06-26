# Review Analysis — Quality Checklist

Run before publishing any Review Analysis report. Every box must be checkable with evidence, not vibes.

## Data Quality
- [ ] All available reviews pulled (not just 5-star or 1-star)
- [ ] Each review has: star, date, variant/SKU, verified-purchase flag, review ID
- [ ] Encoding normalized; emojis and non-ASCII preserved, not mojibaked
- [ ] Exact duplicates and templated spam removed and counted
- [ ] N pulled vs N analyzed both recorded
- [ ] Date range stated (first and last review date)

## Sampling
- [ ] Sample meets size bar (all reviews, or >=150/variant; >=80 minimum)
- [ ] Coverage checked per variant — no variant silently under-sampled
- [ ] Recent reviews weighted or a clear time pivot chosen
- [ ] Any coverage gaps (thin periods/variants) noted in caveats

## Sentiment Coding
- [ ] Sentiment coded from text, not stars
- [ ] 4-label rubric applied (positive/neutral/negative/mixed)
- [ ] Aspects tagged per review; multi-aspect reviews split
- [ ] Negation, sarcasm, and comparatives handled per the guide
- [ ] Star-vs-text mismatches recoded and the mismatch rate logged
- [ ] Codebook anchors written before coding began
- [ ] 10-15% of automated coding hand-verified; disagreement <=10%

## Pain-Point Clustering
- [ ] Mentions mapped to the fixed taxonomy categories
- [ ] Synonyms merged before counting
- [ ] Theme threshold enforced (>=3 mentions or >=2% of reviews)
- [ ] Anecdotes not promoted to "trends"
- [ ] Feature requests clustered separately from complaints

## Quantification
- [ ] Each theme has a raw count AND a % with stated denominator
- [ ] Severity = frequency x impact (return/refund/safety/rating) scored 1-5
- [ ] Trend computed per aspect across time windows
- [ ] Worsening aspects checked against known product/supplier changes
- [ ] Fake/incentivized rate quantified and excluded from sentiment math

## Routing
- [ ] Every pain point tagged PRODUCT / COPY / BOTH
- [ ] Routing rationale written ("would copy have fixed it?")
- [ ] Out-of-scope issues (courier speed, user error) tagged, not counted as defects
- [ ] Quick-win copy edits separated from longer product fixes

## Reporting
- [ ] Overview complete: product, N, date range, avg rating, distribution
- [ ] Aspect sentiment table filled with %s and mention counts
- [ ] Top pain points ranked by severity, each with a verbatim quote + ID
- [ ] Quotes de-identified and traceable to a review ID
- [ ] Action list split into product fixes and copy edits, with owners/ETAs
- [ ] Expected impact stated per action

## Validation
- [ ] Numbers re-checked: percentages sum sensibly, counts reconcile to N
- [ ] A second reader can trace any claim back to source reviews
- [ ] Baseline recorded and a re-run date set (60-90 days)
- [ ] Confidence level (high/med/low) stated with reasoning
