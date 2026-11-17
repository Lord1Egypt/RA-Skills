---
name: startup-launch-research
description: Screens startup launches, public traction signals, verified revenue profiles, and crowdfunding campaigns using Product Hunt, TrustMRR, and Kickstarter through the Crawlora API. Use for launch research and acquisition screening, not investment guarantees or private diligence.
---

# Startup launch research

Build a dated startup or product launch brief from public launch pages,
revenue-verified profiles, and crowdfunding updates. Keep each source's scope
and evidence type explicit.

## When to use this skill

- Find products launched in a category and compare their positioning.
- Inspect makers, alternatives, launch history, customers, and public reviews.
- Screen public TrustMRR revenue signals or acquisition listings.
- Track Kickstarter funding, updates, comments, and campaign status.

## Research workflow

1. Search Product Hunt or Kickstarter first and retain the returned product,
   project, creator, and slug identifiers. IDs are source-specific.
2. Separate launch engagement, current product details, verified revenue fields,
   campaign funding, and review/comment samples. They measure different things.
3. For TrustMRR, report that revenue is payment-provider-verified as represented
   by the source, with its date and coverage limits. Do not extrapolate MRR to
   valuation, profitability, or future growth.
4. For Kickstarter, preserve goal, pledged amount, backers, status, updates,
   and comments as a point-in-time campaign snapshot. A funded campaign is not
   proof of delivery or product quality.

## Examples

```sh
scripts/crawlora.sh /producthunt/search query="AI note taking" | jq '.'
scripts/crawlora.sh /producthunt/product/<id> | jq '.'
scripts/crawlora.sh /trustmrr/leaderboard | jq '.'
scripts/crawlora.sh /kickstarter/discover term="robotics" | jq '.'
scripts/crawlora.sh /kickstarter/project creator=<creator> slug=<project> | jq '.'
```

## Notes and limits

- Public launch, campaign, and profile data only; no pledges, purchases,
  account access, or outreach occur.
- Preserve collection timestamps and source URLs. Public metrics can be
  incomplete, self-reported, or revised.
- Treat alternatives, reviews, comments, and launch rankings as evidence for
  hypotheses, not a complete market or customer survey.

See [`reference/endpoints.md`](reference/endpoints.md) for the complete generated endpoint list.
