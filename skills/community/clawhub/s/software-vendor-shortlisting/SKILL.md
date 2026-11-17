---
name: software-vendor-shortlisting
description: Build a requirements-based software shortlist using Crawlora product discovery, public vendor pages, and review samples. Use to compare vendors against must-haves, pricing assumptions, integration needs, and demo questions before a buying decision.
---

# Software vendor shortlisting

Produce a buyer-specific shortlist with evidence and unresolved questions.
A vendor's advertised capability, a reviewer's experience, and a capability
verified in the user's environment are different evidence types.

## Setup and API contract

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Use the bundled `scripts/crawlora.sh`, which sends `x-api-key` to
`https://api.crawlora.net/api/v1`. Read [reference/endpoints.md](reference/endpoints.md)
for selected endpoints and parameters. Check application `code` as well as HTTP
status; successful payloads are inside `data`. Stop on authentication errors,
back off on `429`, and retry a transient upstream failure once. Bound requests
by the user's scope and credit budget. Preserve source URLs, IDs, retrieved pages,
and timestamps with intermediate evidence so an interrupted comparison can resume.

## Establish criteria and discover candidates

1. Start with the business workflow, current tools, team size, budget/currency,
   deployment needs, required integrations, migration constraints, and must-have
   features. Use a supplied vendor list first. Distinguish disqualifying conditions
   from preferences, and confirm weights before presenting a weighted ranking.
2. Discover candidates through Capterra search, Product Hunt product search, or
   Bing. Capterra can return a fallback list for a query with no genuine match:
   validate category/use-case relevance rather than accepting every hit.
   Bing rejects `site:` queries and may mark results `low_confidence`; resolve
   the official domain directly instead of treating a weak hit as confirmation.
3. Fetch Capterra product details using returned numeric `product_id`. Product
   Hunt details accept a slug or ID, but alternatives require a product slug.
   Do not substitute a launch/user ID or guess a slug from a brand name. An
   alternatives list is a discovery lead, not proof that products meet the same
   requirements or have equivalent scope.
4. Resolve each product's official website, owner, edition, and regional offer.
   Read relevant pricing, feature, integration, deployment, and public trust/docs
   pages with `/web/scrape`. Its POST body is the flat options object, for example
   `{"url":"https://vendor.example/pricing","formats":["markdown"]}`; do not
   wrap it in `scrapeOption`. Use URLs actually supplied or discovered, not that
   illustrative domain. Preserve page sections or short excerpts supporting claims.

```sh
scripts/crawlora.sh /capterra/search q="project management"
scripts/crawlora.sh /producthunt/search query="project management" type=product page=1
# Resolve the numeric product ID from search before requesting details/reviews:
# scripts/crawlora.sh /capterra/product product_id="$PRODUCT_ID"
# scripts/crawlora.sh /capterra/product/reviews product_id="$PRODUCT_ID" page=1
```

## Evaluate evidence and tradeoffs

- Build a requirement-by-vendor matrix with supported, unsupported, and unknown
  states, source URL/date, edition, and evidence type. Missing evidence is not
  evidence of absence. A hard requirement with unknown status leaves a vendor
  conditional; marketing silence should not silently disqualify it.
- Capterra's normalized product response provides identity, description, category,
  and aggregate rating; it does not guarantee a feature matrix or current pricing.
  Its review endpoint promises author, headline, and rating. Use full text, review
  dates, company size, and reviewer role only when actually returned; otherwise
  state that the sample cannot support those segment or recency conclusions.
- Aggregate review counts can be nonzero while the returned review page is empty.
  Report that as no review text collected; do not fabricate themes or infer zero
  reviews. Use the other available evidence and flag the missing review sample.
- Sample reviews to find implementation friction and demo questions. Keep source,
  sample count, selection method, and available dates. Do not infer population
  sentiment, suitability for the user's industry, or statistical significance
  from a handful of headlines. Stars and Product Hunt popularity are not fit scores.
- Compare the same pricing basis: edition, seats, active users, usage units,
  billing interval, minimum commitment, currency, and mandatory add-ons. An
  annual-plan monthly equivalent is not a month-to-month offer. Show scenario
  arithmetic and excluded/unknown implementation, migration, support, and tax
  costs. Quote-only pricing remains unknown; never invent a total-cost estimate.
- Verify integration claims at the workflow level: native connector versus API,
  one-way versus two-way sync, supported objects, and plan restrictions. A logo
  does not prove the required data flow works. Public security/compliance claims
  should remain attributed claims with dates/scope, not certifications you have
  independently audited or guarantees of fitness for the user's requirements.
- Rank on the user's criteria. If using weights, expose the rubric and how unknowns
  affect coverage and scores; do not give unknown features zero silently or let
  popular products bypass must-haves. Prefer a conditional shortlist when key
  evidence needs a demo or trial rather than an unjustified universal winner.

## Deliverable

Return the requirements matrix, a justified shortlist, price scenarios, rejected
or conditional candidates with reasons, and a focused demo/trial checklist.
Separate claims, review observations, and your inferences. Include sources and
collection dates, and describe which unresolved answers would change the ranking.
Do not sign up for trials, contact sales, purchase software, or send the user's
internal requirements to vendors unless asked.
