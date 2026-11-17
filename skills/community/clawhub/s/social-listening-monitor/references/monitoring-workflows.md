# Monitoring workflows

Use focused searches. Run each query separately so the reason for a match stays clear.

## Brand name and misspellings

1. Search the exact brand name.
2. Search one common misspelling at a time.
3. Keep posts that clearly refer to the brand.
4. Group useful posts into questions, praise, problems, and purchase intent.
5. Cite the public URL beside every note.

Example query set:

```text
Acme Analytics
Acme Analtyics
"Acme Analytics" pricing
```

Do not treat every match as a real mention. Common words and short brand names create noise.

## Competitor pricing, launch, and problem searches

Use separate searches for separate marketing questions:

```text
CompetitorName pricing
CompetitorName launched
CompetitorName new feature
CompetitorName problem
CompetitorName alternative
switching from CompetitorName
```

For each useful post, record:

- what happened;
- who said it;
- when it was published;
- why it may matter;
- the public source URL.

Describe what the post says. Do not guess sentiment, buying intent, or business impact.

## Weekly cited competitor brief

1. Run the selected competitor searches on LinkedIn, X, and Reddit.
2. Compare returned URLs with the user's external history file or database.
3. Remove URLs already reviewed.
4. Put new posts under `Launches`, `Pricing`, `Problems`, and `Other`.
5. Note source failures and gaps.
6. Prepare this short review format:

```text
# Weekly competitor brief

## What changed
- Finding — source URL

## Questions or complaints to review
- Finding — source URL

## Possible marketing actions
- Action tied to the cited finding

## Search gaps
- Failed source or query
```

Human review is required. The API supplies public search results; OpenClaw or another external
system supplies scheduling, stored history, deduplication, classification, and delivery.
