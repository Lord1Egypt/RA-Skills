# TwittrAPI read endpoints (most used)

Base URL `https://api.twittrapi.com`, header `X-API-KEY`, add `format=simple`. All `GET` except likers.
Paginated endpoints take `count` (default 20) and `cursor` and return `nextCursor` / `hasNextPage`.
Every endpoint with all parameters and error codes: https://twittrapi.com/openapi.json or
https://twittrapi.com/llms-full.txt. The MCP tool with the same function is in brackets.

## Users

| Path | What | Paginated |
| --- | --- | --- |
| `/user/by/username/{username}` | Profile by handle (no `@`) [`get_user_by_username`] | no |
| `/user/{userId}` | Profile by numeric ID [`get_user_by_id`] | no |
| `/username/to/id/{username}` | Handle to numeric ID [`username_to_id`] | no |
| `/user/users/by/ids?ids=1,2,3` | Up to 500 profiles at once [`users_by_ids`] | no |
| `/user/{userId}/tweets` | A user's tweets [`get_user_tweets`] | yes |
| `/user/{userId}/tweetsAndReplies` | Tweets and replies [`get_user_tweets_and_replies`] | yes |
| `/user/{userId}/media` | Tweets with photos or videos [`get_user_media`] | yes |
| `/user/{userId}/followers` | Followers [`get_followers`] | yes |
| `/user/{userId}/followings` | Accounts the user follows [`get_following`] | yes |
| `/user/{userId}/verifiedFollowers` | Verified followers [`get_verified_followers`] | yes |

The `/user/{userId}/...` timelines also accept `userId` = `-1` plus `?username=<handle>`, which
saves the lookup call when you only have the handle.

## Search

| Path | What |
| --- | --- |
| `/search?searchItem=<query>&category=Latest` | Search like X's search box [`search_tweets`]. `category`: `Top` (default), `Latest`, `People`, `Photos`, `Videos`. Paginated. |

`searchItem` (max 512 characters) supports X operators: `from:user`, `to:user`, `"exact phrase"`,
`lang:en`, `since:2025-01-01`, `until:2025-02-01`, `min_faves:100`, `min_retweets:10`,
`filter:media`, `-filter:replies`, `OR`, `-word`. URL-encode the query.

## Tweets

| Path | What | Paginated |
| --- | --- | --- |
| `/tweet/{tweetId}` | A tweet and its reply thread [`get_tweet`] | yes (replies) |
| `/tweet/{tweetId}/retweets` | Users who retweeted [`get_tweet_retweets`] | yes |
| `/tweet/{tweetId}/favorites` | Users who liked. `POST` with JSON `cookie` (the author's X session) and `proxy`; works only for your own tweets | yes |
| `/tweet/{tweetId}/quotes` | Tweets quoting it [`get_tweet_quotes`] | yes |

The tweet ID is the number at the end of a tweet URL: `https://x.com/<user>/status/<tweetId>`.

## Lists and communities

| Path | What | Paginated |
| --- | --- | --- |
| `/lists/details?listId=<id>` | List name, owner, counts [`get_list_details`] | no |
| `/lists/tweets?listId=<id>` | Tweets from the list's members [`get_list_tweets`] | yes |
| `/lists/members?listId=<id>` | Members [`get_list_members`] | yes |
| `/communities/{communityId}` | Community details [`get_community`] | no |
| `/communities/{communityId}/tweets` | Tweets in a community [`get_community_tweets`] | yes |
| `/communities/search/{searchTerm}` | Find communities [`search_communities`] | yes |

## Trends

| Path | What |
| --- | --- |
| `/trends/{woeid}` | Trending topics: `1` worldwide, `23424977` US, `23424975` UK [`get_trends`] |
| `/misc/locations` | All locations with trends and their WOEIDs [`get_trend_locations`] |

## Account and billing

| Path | What |
| --- | --- |
| `/balance` | Balance and price per call. Free. |
