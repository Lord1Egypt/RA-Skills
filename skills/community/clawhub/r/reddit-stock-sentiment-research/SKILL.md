---
name: reddit-stock-sentiment-research
description: Summarize sampled Reddit discussion about a publicly traded company or ticker and, when useful, compare it with same-window Yahoo Finance price context. Use for requests like “what are Reddit investors saying about NVDA?” or “summarize bullish and bearish Reddit themes”; it is not a trading signal or price forecast.
---

# Reddit stock sentiment research

Build a bounded, auditable brief about Reddit discussion around one publicly traded company or security. Separate what Redditors said from observed price movement, and distinguish the sampled posts from the full investor population.

## Establish the security and scope

- Confirm the ticker, issuer, exchange/market, and requested time window. Resolve ambiguous names or ticker strings with Yahoo Finance search and verify the selected symbol in its quote or company info.
- Agree which communities matter and what question the user wants answered: discussion themes, perceived catalysts/risks, or comparison with a dated price window. If omitted, state a modest sample scope and the default market/time range.
- Ticker text can be an ordinary word or a different company's symbol. Require company, product, market, or subreddit context before counting a result as relevant.

## Collect public discussion

1. Search Reddit with the verified ticker and issuer name as separate query variants. Use a relevant subreddit filter when it improves precision; do not assume a search result page is exhaustive.
2. Review a small first page, record the query/filter/sort/time, and label each candidate relevant, ambiguous, or unrelated. If noise dominates, tighten the query or community instead of paging deeply through false matches.
3. Fetch the original post and comments only for selected relevant threads. Deduplicate by post ID. Keep post count and sampled comment count separate; repeated comments in one thread are not independent investor opinions.
4. Reddit's time filter is supported for top/comments sorts, not as a reliable date filter for new. For new results, inspect source dates locally and retain unknown dates as unknown. The default search feed may leave score and comment-count fields unpopulated; missing engagement is unknown, not zero.
5. Use Reddit's ordinary public feed by default. Engagement metrics require the more expensive metrics mode; request it only when explicitly relevant, and label the resulting counts as approximate because Reddit fuzzes voting data. Comment metric mode can expose only part of a large thread.

## Add price context only when useful

Use Yahoo Finance search to resolve the security, then retrieve a quote or a historical series matching the discussion window. Record symbol, currency, interval, start/end, and whether prices are adjusted. Keep market sessions and post dates aligned; do not treat a current quote as historical context.

If news context helps explain a documented event, use the ticker news surface or a primary filing source and preserve publication dates. Do not repeat an unverified Reddit rumor as a fact or imply that discussion caused a price move.

## Classify and report sampled evidence

Classify selected posts/comments by the view they actually express: positive, negative, mixed, neutral/question, or unclear. Separately tag themes such as product experience, financial performance, valuation, catalyst, risk, or speculation. Quote sparingly and link each example to its post; do not infer the author's portfolio, identity, or trading activity from a comment.

Return a brief with:

- Security identity, market, discussion window, retrieval time, and Reddit queries/communities.
- Relevant, ambiguous, and excluded post counts; thread and comment sample sizes.
- A theme table with stance, evidence count, representative post links, and counterexamples.
- Optional Yahoo Finance price context with currency, interval, exact dates, and adjustment basis.
- Coverage limits and unanswered questions. Do not report an overall sentiment percentage without a clear sampled denominator.

Reddit sentiment is neither a representative poll nor a forecast. Do not recommend buying, selling, holding, or timing a security from this workflow.

## Examples

~~~sh
scripts/crawlora.sh /yahoo-finance/search q="NVIDIA" quotes_count=5
scripts/crawlora.sh /reddit/search q="NVDA" sort=top time=month limit=10
scripts/crawlora.sh /reddit/search q="NVIDIA" subreddit=stocks sort=top time=month limit=10
# After selecting a post and confirming the symbol, substitute their identifiers:
# scripts/crawlora.sh /reddit/comments/<post-id> sort=top limit=25
# scripts/crawlora.sh /yahoo-finance/ticker/<symbol>/history period=1mo interval=1d
~~~

Read reference/endpoints.md for exact route parameters. Use the bundled scripts/crawlora.sh helper, which keeps CRAWLORA_API_KEY in an HTTP header.
