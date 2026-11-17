# AgentKey Tool Reference

Use this reference after the skill triggers. AgentKey's catalog can change, so call `describe_tool` before `execute_tool` and follow the returned `execute_as` template.

## Recommended Discovery

Use `list_tools(prefix="social/reddit")` if an endpoint name fails or if the user asks for a Reddit capability not listed here.

Use `find_tools(q="<full user request>")` for mixed requests like "find Reddit tickers and verify stock prices".

## Reddit Endpoints

- `reddit/app_fetch_trending_searches`
  - Purpose: broad Reddit trending search terms.
  - Known cost: 0.2 credits.
  - Params: optional `need_format`.

- `reddit/app_fetch_subreddit_feed`
  - Purpose: low-cost hot/rising/top feed by subreddit.
  - Known cost: 0.2 credits.
  - Required param: `subreddit_name`.
  - Useful params: `sort` (`BEST`, `HOT`, `NEW`, `TOP`, `CONTROVERSIAL`, `RISING`), `after`, `need_format`.

- `reddit/search_v1`
  - Purpose: keyword search across Reddit.
  - Known cost: 4.4 credits.
  - Required param: `keyword`.
  - Use after low-cost feeds when the user names a ticker, theme, or catalyst.

- `reddit/app_fetch_post_details`, `reddit/app_fetch_post_details_batch`, `reddit/app_fetch_post_comments`
  - Purpose: evidence and comment-level verification.
  - Always run `describe_tool` first; costs and params can differ by provider.

## Finance Endpoints

- `yfinance/getQuote`
  - Purpose: realtime quote validation.
  - Known cost: 0.1 credits.
  - Required param: `symbols` as a comma-separated ticker string.

- `Finnhub/companyNews`
  - Purpose: recent company news for catalyst checks.
  - Known cost: 0.1 credits.
  - Required params: `symbol`, `from`, `to` in `YYYY-MM-DD`.

## Cost Plans

Quick scan: one trending call plus one or two subreddit feeds. Good for a rough pulse.

Standard scan: trending, 4-6 subreddit feeds, quote validation for shortlisted tickers, and optional company news. Ask for confirmation before executing.

Deep scan: standard scan plus post details/comments for top tickers. Use only when the user asks for evidence depth or due diligence.
