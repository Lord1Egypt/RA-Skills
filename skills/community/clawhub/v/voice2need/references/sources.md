# Configure sources

This is the configuration reference bundled with the skill. The host assistant writes the JSON for the user's agreed question and scope. Replace example dates, queries, IDs and file paths; never run a template against real sources without the corresponding authorization.

The schemas below match the bundled adapters. Unknown provider options are not a supported extension mechanism. A provider changing its API/schema needs a compatibility check; do not silently change providers or broaden the source list.

## 1. A complete research config

```json
{
  "project": "Podcast revision research",
  "domain": "Independent podcast production",
  "language": "en",
  "window": {
    "start": "2026-08-01T00:00:00Z",
    "end": "2026-09-01T00:00:00Z"
  },
  "retention_days": 30,
  "limits": {"max_requests": 100, "max_units": null},
  "analysis": {"max_packet_records": 80, "max_packet_chars": 24000},
  "questions": {"Q08": "How do podcast editors work around revision mistakes, and what does that cost?"},
  "sources": [
    {
      "id": "reddit-discovery-01",
      "platform": "reddit",
      "mode": "discovery",
      "subreddit": "podcasting",
      "query": "editing workflow",
      "max_posts": 20,
      "max_comments": 1000,
      "max_items": 2000,
      "max_pages": 5,
      "max_charge_usd": 1
    }
  ]
}
```

Save configs and runs outside the installed skill directory. This example is a schema illustration, not a claim that these limits or this community fit every project.

| Root field | Meaning |
| --- | --- |
| `domain` | Required nonempty research field; keep it consistent across runs to be combined |
| `sources` | Required nonempty array of explicit jobs for collection; the built-in demo is a separate offline path |
| `project`, `language` | Report label and host-analysis language; the renderer does not call a translation service |
| `window.start`, `window.end` | UTC timestamps; use an explicit half-open interval `[start,end)`; each job inherits it unless that job explicitly overrides `start`/`end` |
| `retention_days` | Positive integer, default 30; records a retention review date, not automatic deletion |
| `limits.max_requests` | Nonnegative Session HTTP-request cap, default 100; failures also consume attempts |
| `limits.max_units` | Optional nonnegative internal resource-unit cap; `null` leaves it unset; not a dollar cap or a complete provider quota model |
| `analysis` | Packet subject-record/character limits; optional `evidence_ids` selects candidate IDs; context/long records can exceed limits without truncation |
| `questions` | Optional question wording by Q01–Q14, or an array of `{"id":"Q08","question":"..."}`; all fourteen slots remain |

Each job requires a unique `id` of 1–80 letters, digits, `_` or `-`, and `platform` in `reddit`, `youtube`, `x`, `discord`. Specify a mode explicitly. A changed collection scope uses a new config and new run directory; resuming reuses the unchanged config and run directory. Prior source/spend authorization still applies within its stated boundary.

## 2. Accounts and budget boundaries

| Operation | Named environment variable / external tool |
| --- | --- |
| Reddit Actor | `APIFY_API_TOKEN` |
| YouTube discovery, metadata, comments and replies | `YOUTUBE_API_KEY` |
| Explicit YouTube transcript Actor | `APIFY_API_TOKEN`; this separate mode does not itself need a YouTube API key |
| X search and lookup | `X_BEARER_TOKEN`, with access to the selected endpoint |
| Import existing DiscordChatExporter JSON | No account credential needed |
| Live Discord export | An installed DiscordChatExporter command and `DISCORD_TOKEN`; intended account and specific channel access must already be confirmed |

Do not put tokens in the config, commands, findings, chat or public files. The adapter reads only its named environment variable. No browser-cookie extraction, account switching, joining communities or automatic credential setup is part of this skill.

Budget dimensions are separate:

- Session counts HTTP requests and adapter-supplied units; cached responses do not consume a new request.
- Reddit uses one Apify Actor run per job. `max_charge_usd` is a positive cap passed for that Actor run, default 1. Sum caps across approved jobs; it is not a global project cap or a promise of the actual charge.
- YouTube transcript mode starts one Actor per distinct selected video. A job with three videos and `max_charge_usd: 1` allows up to three separately capped runs, not one dollar for the whole job. Use an explicit video list and sum the caps before running.
- YouTube API accounting and X resource billing depend on provider/account rules. Local request/unit counters are operational limits, not a dollar invoice. Check the account's current limits for a live plan instead of inheriting old pricing.
- DiscordChatExporter performs its own requests inside external processes. Those requests are **outside Session's `max_requests`/`max_units` counters**. Bound channels, window, parallelism and process timeout instead; DCE respects its own service rate limits.

An Actor may continue remotely after local polling stops. Saved run IDs/checkpoints prevent automatic duplicate starts. A POST with an unknown outcome requires inspecting the recorded provider state before any new paid start. Do not erase that state to force a retry.

## 3. Reddit: discover, then fetch chosen discussions

Provider: `fatihtahta/reddit-scraper-search-fast` through the bundled Apify adapter. Discovery collects candidate posts, not comments. Inspect candidate URLs and task relevance, then create a separate deep job with only the selected discussion URLs.

```json
{
  "id": "reddit-threads-01",
  "platform": "reddit",
  "mode": "threads",
  "urls": ["https://www.reddit.com/r/podcasting/comments/REPLACE_POST_ID/topic/"],
  "max_posts": 1,
  "max_comments": 5000,
  "max_items": 6000,
  "max_pages": 10,
  "page_size": 1000,
  "max_charge_usd": 1,
  "max_polls": 30,
  "poll_seconds": 2
}
```

Replace the post ID with a real, selected native post ID. `threads.urls` accepts exact Reddit discussion URLs, not arbitrary domains or a subreddit listing. Set `max_posts` to cover the intended number of selected threads; its default is only 1 in threads mode. Windows filter comment dates for threads, while an older root post can remain context.

| Job option | Supported meaning/default |
| --- | --- |
| `mode: discovery` | `subreddit` with optional `query`; default `max_posts: 100`; no comments |
| `allow_broad_search: true` | Explicit cross-subreddit discovery using `query`; omit `subreddit` only when this wider scope is agreed |
| `mode: threads`, `urls` | Fetch selected post bodies/comments; query/subreddit discovery fields are removed for this mode |
| `max_posts` | Positive integer, up to 10,000; discovery default 100, threads default 1 |
| `max_comments` | Per-post Actor cap, default 5,000, maximum 50,000; this is not a completeness guarantee |
| `max_items` | Total dataset-item cap passed to the Actor/helper, default 10,000; posts and comments can both consume it |
| `max_pages`, `page_size` | Apify dataset retrieval bounds, defaults 100 pages and 1,000 items per page; these are not Reddit's native comment-page counts |
| `max_polls`, `poll_seconds` | Remote-run polling bounds, defaults 30 and 2 seconds; the remote run may still be active at the local deadline |
| `max_charge_usd` | Positive per-Actor cap, default 1 |

Advanced `actor_input` accepts only documented keys: `queries`, `subredditName`, `subredditKeywords`, `urls`, `sort`, `subredditSort`, `timeframe`, `subredditTimeframe`, `dateFrom`, `dateTo`, `commentDateFrom`, `commentDateTo`, `forceSortNewForTimeFilteredRuns`, `includeNsfw`, `strictSearch`, `strictTokenFilter`, `maxPosts`, `maxComments`, `scrapeComments`, `maximize_coverage`, `sentiment_analysis`, `content_analysis`.

Query/keyword/URL fields are nonempty string arrays. Sort values: `relevance`, `hot`, `top`, `new`, `comments`. Timeframe values: `all`, `year`, `month`, `week`, `day`, `hour`. Boolean fields require JSON booleans. Top-level job targets, window and limits take precedence where mapped. `scrapeComments` is forced by mode; automatic `maximize_coverage`, `sentiment_analysis` and `content_analysis` are forced off and cannot be enabled. Avoid advanced fields unless the agreed research scope needs them.

Read returned counts and missing-parent gaps. The adapter explicitly leaves whole-comment-population completeness unverified, even if displayed and fetched counts happen to agree.

## 4. YouTube: candidate videos → discussions → optional transcripts

Choose one discovery entry point:

```json
{"id":"yt-search-01","platform":"youtube","mode":"search","query":"podcast revision workflow","order":"relevance","language":"en","region_code":"US","max_pages":3}
```

```json
{"id":"yt-channels-01","platform":"youtube","mode":"channels","channel_ids":["REPLACE_CHANNEL_ID"],"handles":["@REPLACE_HANDLE"],"max_pages":5}
```

In channel mode supply `channel_ids`, `handles`, or both. It reads upload playlists and checks video publication dates. Search/channel jobs identify videos; they do not automatically fetch all comments or transcripts. Review their returned `video_ids` before deep collection.

```json
{"id":"yt-discussions-01","platform":"youtube","mode":"videos","video_ids":["REPLACE_WITH_11_CHAR_VIDEO_ID"],"max_pages":100}
```

`videos` accepts `video_ids`, canonical YouTube `urls`, or both. It obtains metadata and available comment threads, then paginates replies when embedded replies are incomplete. `max_pages` applies to each pagination stream, including reply streams; use the root request cap as an additional total bound. Disabled comments, unavailable videos, page caps and reply-count mismatches remain explicit gaps.

When spoken content is necessary, add an explicitly approved transcript job:

```json
{"id":"yt-transcripts-01","platform":"youtube","mode":"transcript","video_ids":["REPLACE_WITH_11_CHAR_VIDEO_ID"],"language":"en","max_charge_usd":1,"max_polls":30,"poll_seconds":2,"max_pages":10}
```

This invokes `starvibe/youtube-video-transcript`, one Actor per selected video, with provider input `youtube_url` and optional `language`. `max_pages` bounds dataset pagination. An empty transcript or a provider error is not a usable transcript. There is no automatic transcript provider fallback and no implied transcript collection when only comments were requested.

Mode aliases exist for compatibility (`discovery`, `channel`, `uploads`, `deep`, `comments`); prefer the explicit canonical names above. Search's `language` is a relevance preference, not a promise that every returned discussion is in that language.

## 5. X: search/lookup plus bounded reference context

```json
{"id":"x-search-01","platform":"x","mode":"search_recent","query":"\"podcast editing\" -is:retweet","page_size":100,"max_pages":5,"sort_order":"recency","hydrate_context":true,"context_depth":1,"max_context_requests":10,"max_context_ids":1000}
```

```json
{"id":"x-lookup-01","platform":"x","mode":"lookup","tweet_ids":["REPLACE_NUMERIC_POST_ID"],"max_pages":5,"hydrate_context":true,"context_depth":2,"max_context_requests":5,"max_context_ids":300}
```

Replace lookup IDs with selected numeric native post IDs, stored as strings. `search_recent` must fit the provider/account's searchable time range. Use `search_all` only with the necessary account access and approved historical scope; the adapter never silently substitutes it.

| Option | Behavior/default |
| --- | --- |
| `query` | Required nonempty string for `search_recent`/`search_all`; search operators remain explicit in the saved query |
| `page_size` | Search minimum 10; maximum 100 for recent, 500 for all; default 100 |
| `max_pages` | Maximum search pages or 100-ID lookup batches, default 100 |
| `tweet_ids` | Nonempty numeric-ID array for lookup; deduplicated and batched by 100 |
| `hydrate_context` | Default true; looks up explicit replied-to, quoted and retweeted IDs |
| `context_depth` | Positive integer 1–10, default 1; set `hydrate_context: false` to disable, not depth zero |
| `max_context_requests` | Positive lookup-request cap, default 10, maximum 1,000 |
| `max_context_ids` | Positive context-ID cap, default 1,000, maximum 100,000 |

This is not a crawler for every reply to a post. Search/lookup results and their bounded references retain separate authors, types and long text. Missing/deleted/inaccessible references remain gaps. A retweet is an occurrence, not a new independent adoption story. Requested-resource units are a conservative local counter, not an invoice.

## 6. Discord: existing exports or an explicitly scoped live export

Offline import is the simplest path:

```json
{"id":"discord-import-01","platform":"discord","mode":"import","input":["/replace/with/absolute/export.json"],"skip_channel_names":["welcome","rules","rank"]}
```

`input` accepts one path or an array. Use absolute paths so the host working directory cannot change which file is read. Optional `channel_ids` filters the supplied export channels; accessible thread exports under those parent channels are retained. `skip_channel_names` is an exact lowercase-name list; replace it or use `[]` when those names are relevant to the question.

The importer copies the original bytes. Truncated JSON recovers only complete messages into a separate derived raw envelope; it neither modifies the original nor claims the missing tail was read. Supplied exports cover their recorded channels, not the entire server.

Live export example, deliberately unconfirmed until actual account/access facts are established:

```json
{
  "id": "discord-export-01",
  "platform": "discord",
  "mode": "export",
  "dce_command": ["/replace/with/DiscordChatExporter.Cli"],
  "channel_ids": ["REPLACE_NUMERIC_TEXT_OR_FORUM_CHANNEL_ID"],
  "start": "2026-08-01T00:00:00Z",
  "end": "2026-09-01T00:00:00Z",
  "account_confirmed": false,
  "access_confirmed": false,
  "parallel": 2,
  "timeout_seconds": 3600
}
```

Only set `account_confirmed` and `access_confirmed` to true after the intended `DISCORD_TOKEN` account and access to those specific channels have actually been confirmed. Reuse an existing valid confirmation; do not infer it from a token merely being present. Never expose the token while checking the boundary.

`channel_ids` must be individual visible text/forum channel IDs, **not category IDs or a guild/server ID**. The adapter checks numeric shape, not the semantic channel type; the host must verify the channel selection. A category cannot be passed as shorthand for every child channel.

`dce_command` accepts either one installed executable or `["dotnet", "/path/DiscordChatExporter.Cli.dll"]`; no extra flags. The adapter supplies its own bounded flags: JSON/text output, chosen window, all accessible threads, no media, rate-limit respect, and one DCE worker per process. `parallel` is 1 or 2; `timeout_seconds` is an integer from 1 to 86,400. Both confirmation flags and `--live` are required.

If one export fails, new channels stop starting and existing partial files/logs are retained. Some inaccessible threads may be omitted during DCE discovery, so population completeness remains unverified. DCE's internal HTTP requests are outside Session request/unit accounting; a root `max_requests: 0` does not disable a separately authorized live DCE process.

## 7. From collection to analysis

After discovery, inspect the selected URLs/IDs and save the deep jobs in a new config/run. Stay within the already confirmed research/source/budget boundary; ask only when the deeper work would materially expand it. Keep per-run raw pointers intact. Never concatenate normalized records from different raw roots without a provenance-preserving merge.

Run `status` and `verify`, then follow [operations](operations.md) to prepare packets and write findings. Investigate source failures, missing context and empty content as named gaps. A small useful pilot should lead to the agreed collection, not endless restarts of the same pilot; an empty or failed source is not proof that the need is absent.
