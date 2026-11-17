# Sorsa API v3 Reference

- **Base URL:** `https://api.sorsa.io/v3`
- **Auth:** `ApiKey: YOUR_API_KEY` header on every request.
- **Docs:** https://docs.sorsa.io/ (LLM index: https://docs.sorsa.io/llms.txt)
- **OpenAPI:** https://docs.sorsa.io/v3/openapi.json (Swagger: https://api.sorsa.io/v3/swagger.json)

HTTP status codes (all endpoints): `200` OK, `400` bad params, `401` bad/missing key, `403` forbidden, `404` not found, `429` rate limited, `500` server error. Errors return `{"message": "..."}`.

## Contents
1. [Data models](#data-models)
2. [Users](#section-1-users)
3. [Tweets](#section-2-tweets)
4. [Search](#section-3-search)
5. [Verification / checks](#section-4-verification)
6. [Community](#section-5-community)
7. [Lists](#section-6-lists)
8. [Sorsa Info (crypto analytics)](#section-7-sorsa-info)
9. [Technical / converters](#section-8-technical)

---

## Data models

**User** (full profile): `id`, `username`, `display_name`, `description`, `location`, `profile_image_url`, `profile_background_image_url`, `followers_count`, `followings_count`, `tweets_count`, `favourites_count`, `media_count`, `verified` (bool), `protected` (bool), `can_dm` (bool), `possibly_sensitive` (bool), `created_at` (ISO 8601), `bio_urls` (string[]), `pinned_tweet_ids` (string[]).

**CommunityUser** (compact): `id`, `username`, `display_name`, `profile_image_url`, `verified`, `protected`.

**Follower**: all `User` fields except `location`, plus `followerDate` (ISO 8601, when the follow started).

**Tweet**: `id`, `full_text`, `created_at`, `lang`, `conversation_id_str`, `likes_count`, `retweet_count`, `reply_count`, `quote_count`, `view_count`, `bookmark_count`, `is_reply`, `is_quote_status`, `is_replies_limited`, `in_reply_to_tweet_id`, `in_reply_to_username`, `user` (User), `entities` (array of `{type: photo|video|url, link, preview}`), `quoted_status` (Tweet, if quote), `retweeted_status` (Tweet, if retweet).

**Trend**: `name`, `query`, `url`.

**Space** (a.k.a. Place, returned by `/spaces`): `id`, `title`, `state`, `scheduled_start` (int), `created_at` (int), `updated_at` (int), `media_key`, `is_subscribed` (bool), `creator` (User), `participants` (`{ total, admins[], speakers[], listeners[] }` where each participant has `id`, `username`, `name`, `avatar`, `is_verified`, `start`), `settings` (booleans: `is_locked`, `is_muted`, `disallow_join`, `is_space_available_for_replay`, `is_space_available_for_clipping`, and more), `stats` (`{ total_live_listeners, total_participants, total_replay_watched }`).

**Response envelopes:**
- `TweetsResponse`: `{ tweets: Tweet[], next_cursor: string|null }`
- `TweetsBulkResponse`: `{ tweets: Tweet[] }` (no pagination)
- `UsersResponse`: `{ users: User[], next_cursor: string|null }`
- `CommunityUsersResponse`: `{ users: CommunityUser[], next_cursor: string|null }`
- `FollowersResponse`: `{ users: Follower[] }` (Follower includes `followerDate`)
- `TopFollowersResponse`: `{ users: TopFollower[] }` (TopFollower includes a `score`, no `followerDate`)
- `TrendsResponse`: `{ trends: Trend[] }`

**User identifier rule:** where you see "id rule", provide exactly ONE of `user_link`, `username`, or `user_id`.

---

## Section 1: Users

**GET /info** — user profile. Params: id rule. Returns `User`.

**GET /info-batch** — up to 100 profiles. Params: `usernames` (string[]) OR `user_ids` (string[]). Returns `{ users: User[] }`.

**GET /about** — about metadata. Params: id rule. Returns `{ country, username_change_count, last_username_change_at }`.

**GET /followers** — followers, up to 200/page. Params: id rule + `next_cursor` (int). Returns `UsersResponse`.

**GET /follows** — following, up to 200/page. Params: id rule + `next_cursor` (int). Returns `UsersResponse`.

**GET /verified-followers** — verified followers. Params: id rule + `next_cursor` (string). Returns `UsersResponse`.

---

## Section 2: Tweets

**POST /tweet-info** — one tweet's full data. Body: `{ tweet_link }` (URL or ID). Returns `Tweet`. Nested original is included for replies/quotes/retweets.

**POST /tweet-info-bulk** — up to 100 tweets, no pagination. Body: `{ tweet_links: string[] }`. Returns `TweetsBulkResponse`.

**POST /user-tweets** — a user's tweets, up to 20/page. Body: id rule + optional `next_cursor`. Returns `TweetsResponse`.

**POST /comments** — replies under a tweet, up to 20/page. Body: `{ tweet_link, order_by?: "Relevance"|"Recency"|"Likes" (default Relevance), next_cursor? }`. Returns `TweetsResponse`.

**POST /quotes** — quote tweets, up to 20/page. Body: `{ tweet_link, next_cursor? }`. Returns `TweetsResponse`.

**POST /retweeters** — users who retweeted (newest first). Body: `{ tweet_link, next_cursor? }`. Returns `UsersResponse` (note: users, not tweets).

**POST /article** — long-form X Article. Body: `{ tweet_link }`. Returns `{ full_text, preview_text, cover_image_url, published_at, likes_count, retweet_count, reply_count, quote_count, bookmark_count, views_count, author: User }`.

**GET /trends** — trending topics for a location. Param: `woeid` (integer, required; WOEID location identifier). Returns `TrendsResponse` (`{ trends: [{ name, query, url }] }`). This is a GET endpoint despite living under the Tweets group.

---

## Section 3: Search

**POST /search-tweets** — search tweets, up to 20/page. Body: `{ query (required), order?: "popular"|"latest", next_cursor? }`. Supports Twitter advanced-search operators (`from:`, `to:`, `since:`, `until:`, quoted phrases, hashtags). Returns `TweetsResponse`.

**POST /mentions** — tweets mentioning a handle, up to 20/page; richest filters. Body: `{ query, order?, min_likes?, min_replies?, min_retweets?, since_date? (YYYY-MM-DD), until_date? (YYYY-MM-DD), next_cursor? }`. Returns `TweetsResponse`.

**POST /search-users** — search accounts. Body: `{ query (required), next_cursor? }`. Returns `UsersResponse`.

**GET /spaces** — Twitter/X Space details. Params: `id` (Space ID) OR `link` (Space URL). Returns a `Space` object (metadata, `creator`, `participants` broken down into admins/speakers/listeners, `settings`, `stats`). GET endpoint.

---

## Section 4: Verification

**POST /check-follow** — does user_2 follow user_1. Body: one identifier per side (`*_1` and `*_2`). Returns `{ follow: bool, user_protected: bool }`.

**GET /check-comment** — did a user reply under a tweet. Params: `tweet_link` (required) + id rule for the user. Returns `{ commented: bool, tweet: Tweet|null }`.

**POST /check-quoted** — did a user quote or retweet a tweet. Body: `{ tweet_link, id rule }`. Returns `{ status: "quoted"|"retweet"|"not_found", date|null, text|null, user_protected }`.

**POST /check-retweet** — did a user retweet (scans up to 100 retweets/request). Body: `{ tweet_link, id rule, next_cursor? }`. Returns `{ retweet: bool, user_protected, next_cursor|null }`.

**POST /check-community-member** — is a user in a Community. Body: `{ community_id (required), id rule }`. Returns `{ is_member: bool }`.

---

## Section 5: Community

**POST /community-members** — community members, paginated. Body: `{ community_link (ID or URL), next_cursor? }`. Returns `CommunityUsersResponse`.

**POST /community-tweets** — community feed, up to 20/page. Body: `{ community_id (required), order?: "popular"|"latest" (default latest), next_cursor? }`. Returns `TweetsResponse`.

**POST /community-search-tweets** — keyword search inside a community, up to 20/page. Body: `{ community_link (required, ID or URL), query?, order?, next_cursor? }`. Returns `TweetsResponse`.

---

## Section 6: Lists

**GET /list-members** — profiles of accounts in a List. Params: `list_id` (required) + `next_cursor?` (int). Returns `UsersResponse`.

**GET /list-followers** — subscribers of a List. Params: `list_link` (required, URL or ID) + `next_cursor?`. Returns `UsersResponse`.

**GET /list-tweets** — feed from list members, up to 20/page. Params: `list_id` (required) + `next_cursor?`. Returns `TweetsResponse`.

---

## Section 7: Sorsa Info

These endpoints read Sorsa's internal database, which primarily indexes crypto accounts (influencers, projects, VCs). Coverage is partial outside crypto, and a first request for a new or large account may be slow while it indexes. All take the id rule.

**GET /score** — crypto influence score. Returns `{ score: number }`.

**GET /score-changes** — score deltas. Returns `{ week_delta, month_delta }`.

**GET /followers-stats** — follower breakdown. Returns `{ followers_count, influencers_count, projects_count, venture_capitals_count, user_protected }`.

**GET /top-followers** — top 20 followers by Sorsa Score. Returns `TopFollowersResponse` (each item is a profile plus a `score`; note this differs from the `FollowersResponse` shape, no `followerDate`).

**GET /top-following** — top 20 followed accounts by Sorsa Score. Returns `FollowersResponse`.

**GET /new-followers-7d** — new followers in the last 7 days (crypto-indexed only). Returns `FollowersResponse`.

**GET /new-following-7d** — newly followed accounts in the last 7 days (crypto-indexed only). Returns `FollowersResponse`.

---

## Section 8: Technical

**GET /username-to-id/{user_handle}** — handle to numeric ID. Returns `{ id }`.

**GET /id-to-username/{user_id}** — numeric ID to current handle. Returns `{ handle }`.

**GET /link-to-id** — profile URL to numeric ID. Param: `link` (required). Returns `{ id }`.

**GET /key-usage-info** — usage for the current key (read from the `ApiKey` header). Returns `{ key_requests, remaining_requests, total_requests, valid_until }`.
