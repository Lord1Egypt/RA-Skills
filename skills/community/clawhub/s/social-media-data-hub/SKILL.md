---
name: social-media-data-hub
description: Unified Apify-based retrieval for TikTok, Instagram, X/Twitter, and YouTube profile, post, and comment data with cross-platform normalization for analysis workflows.
metadata: {"openclaw":{"emoji":"📊","requires":{"env":["APIFY_TOKEN"],"bins":["python3"]}}}
---

# Social Media Data Hub

Use Apify to collect social media data from TikTok, Instagram, X/Twitter, and YouTube through one consistent workflow.

## Core Capabilities

1. **Profile lookup** - Retrieve profile metadata such as follower count, content volume, and bio.
2. **Bulk post retrieval** - Pull recent or popular posts for an account together with engagement metrics.
3. **Single-post lookup** - Input a post URL and return a normalized record with key metrics.
4. **Comment retrieval** - Fetch comment threads for a supported post URL.
5. **Cross-platform normalization** - Map all supported platforms into one shared schema for analysis.

## Actor Mapping

| Platform | Actor ID | Purpose |
|------|----------|------|
| TikTok | `clockworks/tiktok-scraper` | Profiles, posts, comments |
| Instagram | `apify/instagram-scraper` | Profiles, posts, comments |
| X/Twitter (bulk) | `apidojo/tweet-scraper` | Bulk tweet retrieval (50+ items) |
| X/Twitter (precise) | `apidojo/twitter-scraper-lite` | Single tweet, conversation, or small batches |
| YouTube | `streamers/youtube-scraper` | Channels and videos |

## Usage

All scripts live under `{baseDir}/scripts/`, are executed with `python3`, and return JSON.

### Profile Lookup

```bash
python3 {baseDir}/scripts/fetch_profile.py --platform tiktok --username "khaby.lame"
python3 {baseDir}/scripts/fetch_profile.py --platform instagram --username "natgeo"
python3 {baseDir}/scripts/fetch_profile.py --platform twitter --username "elonmusk"
python3 {baseDir}/scripts/fetch_profile.py --platform youtube --channel-url "https://www.youtube.com/@MrBeast"
```

### Bulk Post Retrieval

```bash
python3 {baseDir}/scripts/fetch_posts.py --platform tiktok --username "khaby.lame" --count 20
python3 {baseDir}/scripts/fetch_posts.py --platform instagram --username "natgeo" --count 30
python3 {baseDir}/scripts/fetch_posts.py --platform twitter --username "elonmusk" --count 100
python3 {baseDir}/scripts/fetch_posts.py --platform youtube --channel-url "https://www.youtube.com/@MrBeast" --count 50
```

### Single-Post Lookup

```bash
python3 {baseDir}/scripts/fetch_single_post.py --url "https://www.tiktok.com/@user/video/123456"
python3 {baseDir}/scripts/fetch_single_post.py --url "https://www.instagram.com/p/ABC123/"
python3 {baseDir}/scripts/fetch_single_post.py --url "https://x.com/user/status/123456"
python3 {baseDir}/scripts/fetch_single_post.py --url "https://www.youtube.com/watch?v=ABC123"
```

### Comment Retrieval

```bash
python3 {baseDir}/scripts/fetch_comments.py --url "https://www.tiktok.com/@user/video/123456" --count 50
python3 {baseDir}/scripts/fetch_comments.py --url "https://www.instagram.com/p/ABC123/" --count 30
python3 {baseDir}/scripts/fetch_comments.py --url "https://x.com/user/status/123456" --count 100
```

### Cross-Platform Normalization

`normalize.py` is used internally by the fetch scripts and can also be run directly:

```bash
echo '<raw_json>' | python3 {baseDir}/scripts/normalize.py --platform tiktok --type post
```

## Unified Data Model

### Normalized Post (`NormalizedPost`)

| Field | Type | Description |
|------|------|------|
| `platform` | string | `tiktok` / `instagram` / `twitter` / `youtube` |
| `post_id` | string | Platform-native post ID |
| `post_url` | string | Post URL |
| `text` | string | Caption, text body, or title |
| `created_at` | string | ISO 8601 timestamp |
| `author_name` | string | Author username |
| `author_display_name` | string | Display name |
| `likes` | int | Like count |
| `comments` | int | Comment count |
| `shares` | int | Share or repost count, or `null` |
| `views` | int | View count, play count, or `null` |
| `saves` | int | Save or bookmark count, or `null` |
| `hashtags` | list | Hashtag list |
| `media_type` | string | `video` / `image` / `text` / `carousel` |

### Normalized Profile (`NormalizedProfile`)

| Field | Type | Description |
|------|------|------|
| `platform` | string | Platform identifier |
| `username` | string | Username or handle |
| `display_name` | string | Display name |
| `bio` | string | Biography or profile summary |
| `followers` | int | Follower count |
| `following` | int | Following count, or `null` |
| `posts_count` | int | Total content count, or `null` |
| `profile_url` | string | Profile URL |
| `verified` | bool | Verification status |

## Cost Reference (BRONZE Tier)

| Operation | TikTok | Instagram | X/Twitter | YouTube |
|------|--------|-----------|---------|---------|
| Per post | $0.003 | $0.0023 | $0.0004 | $0.003 |
| Bulk 1K items | $3.00 | $2.30 | $0.40 | $3.00 |
| Single-item lookup | ~$0.50 (minimum charge) | $0.0023 | $0.05 | $0.003 |

See `{baseDir}/references/apify_actors_reference.md` for actor inputs, selection guidance, and pricing details.

## Notes

- TikTok has a $0.50 minimum per run, so bulk retrieval is usually more cost-effective than single-item lookups.
- For X/Twitter, use `tweet-scraper` when you need 50 or more items and `twitter-scraper-lite` for smaller batches or single tweets.
- Instagram comments are limited to 50 comments per post.
- YouTube comments are not handled by these scripts; use a dedicated YouTube Comments Scraper actor instead.
- All scripts call the Apify REST API directly and do not rely on the `apify-client` SDK.
