# Yelp Search Playbook

Use this file when the user wants discovery, comparison, or shortlisting.

## Step 1: Define the decision

Classify the task before searching:
- discover new options in one area
- compare named businesses head to head
- verify one business before a visit, call, or order

The decision type determines how much breadth vs depth is needed.

## Step 2: Bound the market

Always anchor search with one of these:
- city or neighborhood
- full address or coordinates
- phone number
- known business alias

If the user says "near me" but no location is available, ask one location question before searching.

## Step 3: Filter in layers

Recommended filter order:
1. location and business type
2. price or service constraints
3. quality floor
4. operational flags such as open now, delivery, or takeout

Avoid over-filtering the first call. Broad first, then narrow.

## Step 4: Build the comparison table

For each surviving candidate, capture:
- name and alias
- area or neighborhood
- rating and review count
- price level
- review recency signal
- strongest positive theme
- strongest risk theme

## Step 5: Return a decision-ready shortlist

Preferred output structure:

| Business | Why it fits | Main risk | Next check |
|----------|-------------|-----------|------------|
| A | Best overall fit | Can be crowded | verify current wait or hours |
| B | Better value | Fewer reviews | inspect newest reviews |
| C | Strong niche match | farther away | confirm distance or route |

## Ranking priorities

- For exploration: category fit and neighborhood relevance first
- For fast decisions: open status, transaction type, and review recency matter more
- For premium choices: rating stability and complaint severity matter more than review count alone

## Do not do this

- Do not mix businesses from different cities in the same shortlist without saying so.
- Do not use Yelp stars as the only ranking criterion.
- Do not imply a business is "best" when the evidence is thin or stale.
