# twitterapi.io docs

Core official docs used for this CLI:

- Introduction: https://docs.twitterapi.io/introduction
- Documentation index: https://docs.twitterapi.io/llms.txt
- Authentication: https://docs.twitterapi.io/authentication
- Get Tweets by IDs: https://docs.twitterapi.io/api-reference/endpoint/get_tweet_by_ids
- Get User Info: https://docs.twitterapi.io/api-reference/endpoint/get_user_by_username
- Get User Last Tweets: https://docs.twitterapi.io/api-reference/endpoint/get_user_last_tweets
- Get Tweet Replies: https://docs.twitterapi.io/api-reference/endpoint/get_tweet_replies
- Get Tweet Quotations: https://docs.twitterapi.io/api-reference/endpoint/get_tweet_quotations
- Get Tweet Thread Context: https://docs.twitterapi.io/api-reference/endpoint/get_tweet_thread_context
- Get User Mentions: https://docs.twitterapi.io/api-reference/endpoint/get_user_mentions
- Advanced Search: https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search

Important notes from docs:
- API auth uses the `x-api-key` header.
- `GET /twitter/tweets` uses `tweet_ids`.
- `GET /twitter/user/info` uses `userName`.
- `GET /twitter/user/last_tweets` accepts `userName` or `userId`, plus `includeReplies` and `cursor`.
- `GET /twitter/tweet/replies` accepts `tweetId`, optional `sinceTime`, `untilTime`, and `cursor`.
- `GET /twitter/tweet/quotes` accepts `tweetId` and `cursor`.
- `GET /twitter/tweet/thread_context` accepts `tweetId` and `cursor`.
- `GET /twitter/user/mentions` appears to require `userName` on the live endpoint; use username input here and verify against official docs if behavior changes.
- `GET /twitter/tweet/advanced_search` accepts `query`, `queryType`, and `cursor`.
- Advanced search and timeline-style endpoints paginate with `has_next_page` + `next_cursor`.
- For search date filters, prefer `since_time:`, `until_time:`, and `within_time:` operators.
