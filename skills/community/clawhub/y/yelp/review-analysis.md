# Yelp Review Analysis

Use this file when the user wants to understand review quality, not just scores.

## Core dimensions

Evaluate every business on these dimensions:
- average rating
- review volume
- recency of the visible review sample
- recurring praise themes
- recurring complaint themes
- severity of the newest negative feedback

## Signal weighting

Use this rough weighting:

| Signal | Weight | Why it matters |
|--------|--------|----------------|
| Recurring complaint cluster | High | Repeated pain is usually operational, not random |
| Newest 1-3 star reviews | High | Fresh decline matters more than old praise |
| Review volume | Medium | Stability check for the rating |
| Average rating | Medium | Useful summary, weak on its own |
| Single standout review | Low | Anecdotal unless repeated |

## Pattern labels

Group review findings into reusable buckets:
- service speed
- food or product quality
- cleanliness
- staff attitude
- pricing or value
- wait times
- consistency
- delivery or pickup reliability

Use the same labels across businesses so comparisons stay clean.

## Evidence rule

Separate:
- evidence: what reviews visibly say
- inference: what pattern likely exists
- uncertainty: what you cannot confirm from the visible sample

Do not present inference as fact.

## Low-confidence situations

Treat the analysis as low-confidence when:
- review volume is very low
- visible reviews are old
- the newest reviews are mixed and few
- the business changed category, ownership, or location recently

## Output pattern

Return:
1. summary judgment
2. top praise themes
3. top risk themes
4. whether the latest reviews change the decision

## Common mistakes

- Averaging away fresh complaints behind an old 4.5 rating
- Ignoring sample size and treating five reviews like five hundred
- Mixing Yelp review evidence with another platform without labeling the source
