# Lane B: web research (WebSearch + WebFetch)

Use this lane for what the YouTube API cannot give: demand signals, other platforms, news context, and what people say about a topic. It supports the YouTube data; it does not replace it.

## What to look for

- **Demand signals:** questions people keep asking (Reddit, Quora, forums), complaints, "I wish someone would explain ...".
- **Cross-platform confirmation:** is the same angle also winning on X, Reddit, TikTok, newsletters? Confirmation across platforms strengthens a pattern.
- **Timing context:** news, launches, seasons or events that explain a spike and tell you whether it will repeat.
- **Competitor view:** a creator's own "most popular" lists, interviews, and recaps of what worked for them.

## Query patterns

Start short (2 to 5 words) and vary the angle. Use the real current year from the conversation, not a remembered one.

- `<niche> viral <year>`, `<niche> trending now`
- `<niche> content ideas reddit`, `<niche> "blew up" views`
- `<niche> most asked questions`, `<niche> beginner mistakes`
- `<creator or brand> most popular videos`
- `<niche> trends report <year>` for industry write-ups

Search each distinct angle separately rather than one long combined query. When a result looks useful, fetch the page with WebFetch instead of relying on the snippet.

## Confidence labels

Attach one to every figure or claim from this lane.

| Label | Meaning |
|---|---|
| High | YouTube API numbers pulled by the script (Lane A) |
| Medium | A fetched public page that shows the figure and a date |
| Low | Search snippet, secondhand claim, or number without a date |

Do not put Low-confidence figures in ranking tables. Mention them in prose, marked as unverified.

## Platform limits (set expectations honestly)

- **YouTube pages** fetched as text rarely give reliable stats; use the API for numbers.
- **TikTok and Instagram:** public view counts are usually not retrievable through search or fetch, and the shell cannot scrape them. Use them only for qualitative signals (what angles recur, what creators discuss) and say that the numbers are unavailable.
- **X:** results are patchy; treat as qualitative.
- **Reddit:** search and thread pages are often readable and are valuable for audience language.
- If a site refuses a fetch, say so and move to another source. Do not try to work around the block.

## Using what you find

Paraphrase, do not copy. Quote at most a few words from any single source, and only when the exact wording matters. Credit each source with a link in the report's source list so the user can verify it.
