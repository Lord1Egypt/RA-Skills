# Capability Catalog

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Do not edit endpoint definitions manually.

| Endpoint | Purpose | Required input | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`amazon/best-sellers`](https://docs.socq.ai/api-manual/amazon/best-sellers) | Collect public Amazon best sellers. | urls | `product@1.0` | 0.15 credits/result |
| [`amazon/product-detail`](https://docs.socq.ai/api-manual/amazon/product-detail) | Collect public Amazon product details. | urls | `product@1.0` | 0.15 credits/result |
| [`amazon/product-search`](https://docs.socq.ai/api-manual/amazon/product-search) | Search public Amazon products. | domain, query | `product@1.0` | 0.15 credits/result |
| [`amazon/reviews`](https://docs.socq.ai/api-manual/amazon/reviews) | Collect public Amazon reviews. | urls | `review@1.0` | 0.15 credits/result |
| [`amazon/seller-info`](https://docs.socq.ai/api-manual/amazon/seller-info) | Collect public Amazon seller information. | urls | `seller@1.0` | 0.15 credits/result |
| [`apple-app-store/app-detail`](https://docs.socq.ai/api-manual/apple-app-store/app-detail) | Collect public Apple App Store app details. | urls | `app@1.0` | 0.15 credits/result |
| [`apple-app-store/app-reviews`](https://docs.socq.ai/api-manual/apple-app-store/app-reviews) | Collect public Apple App Store reviews. | urls | `review@1.0` | 0.15 credits/result |
| [`apple-app-store/rankings`](https://docs.socq.ai/api-manual/apple-app-store/rankings) | Collect public Apple App Store category rankings. | urls | `app@1.0` | 0.15 credits/result |
| [`bluesky/post`](https://docs.socq.ai/api-manual/bluesky/post) | Collect a public Bluesky post. | url | `post@1.0` | 0.19 credits/request |
| [`bluesky/profile`](https://docs.socq.ai/api-manual/bluesky/profile) | Collect a public Bluesky profile. | username | `account@1.0` | 0.19 credits/request |
| [`bluesky/user-posts`](https://docs.socq.ai/api-manual/bluesky/user-posts) | Collect one page of public Bluesky user posts. | one of: user_id; username | `post@1.0` | 0.19 credits/request |
| [`douyin/live-room-detail`](https://docs.socq.ai/api-manual/douyin/live-room-detail) | Collect public Douyin live room details. | room_id | `live-room@1.0` | 0.1 credits/request |
| [`douyin/product-data`](https://docs.socq.ai/api-manual/douyin/product-data) | Collect one page of public Douyin live room products. | author_id, room_id | `product@1.0` | 0.1 credits/request |
| [`douyin/user-profile`](https://docs.socq.ai/api-manual/douyin/user-profile) | Collect a public Douyin profile. | one of: url; user_id | `account@1.0` | 0.1 credits/request |
| [`douyin/user-videos`](https://docs.socq.ai/api-manual/douyin/user-videos) | Collect one page of public Douyin user videos. | one of: url; user_id | `reel-video@1.0` | 0.1 credits/request |
| [`douyin/video-comments`](https://docs.socq.ai/api-manual/douyin/video-comments) | Collect one page of public Douyin video comments. | url | `comment@1.0` | 0.1 credits/request |
| [`douyin/video-detail`](https://docs.socq.ai/api-manual/douyin/video-detail) | Collect public Douyin video details. | url | `reel-video@1.0` | 0.1 credits/request |
| [`douyin/video-search`](https://docs.socq.ai/api-manual/douyin/video-search) | Search public Douyin videos. | query | `reel-video@1.0` | 0.1 credits/request |
| [`facebook-ad-library/ad`](https://docs.socq.ai/api-manual/facebook-ad-library/ad) | Facebook Ad Library Ad API | url | `ad@1.0` | 0.6 credits/result |
| [`facebook-ad-library/company-ads`](https://docs.socq.ai/api-manual/facebook-ad-library/company-ads) | Facebook Ad Library Company Ads API | page_id | `ad@1.0` | 0.5 credits/result |
| [`facebook-ad-library/company-search`](https://docs.socq.ai/api-manual/facebook-ad-library/company-search) | Facebook Ad Library Company Search API | query | `advertiser@1.0` | 0.5 credits/result |
| [`facebook-ad-library/search`](https://docs.socq.ai/api-manual/facebook-ad-library/search) | Facebook Ad Library Search API | query | `ad@1.0` | 0.5 credits/result |
| [`facebook-marketplace/item`](https://docs.socq.ai/api-manual/facebook-marketplace/item) | Facebook Marketplace Item API | urls | `listing@1.0` | 0.6 credits/result |
| [`facebook-marketplace/location-search`](https://docs.socq.ai/api-manual/facebook-marketplace/location-search) | Facebook Marketplace Location Search API | query | `marketplace-location@1.0` | 0.3 credits/result |
| [`facebook-marketplace/search`](https://docs.socq.ai/api-manual/facebook-marketplace/search) | Facebook Marketplace Search API | latitude, longitude, query | `listing@1.0` | 0.7 credits/result |
| [`facebook/ad-transcript`](https://docs.socq.ai/api-manual/facebook/ad-transcript) | Extract transcripts from public Facebook ads. | urls | `transcript@1.0` | 0.5 credits/result |
| [`facebook/comment-replies`](https://docs.socq.ai/api-manual/facebook/comment-replies) | Collect public Facebook comment replies. | one of: comment_id + url; expansion_token + feedback_id | `comment@1.0` | 0.3 credits/result |
| [`facebook/comments`](https://docs.socq.ai/api-manual/facebook/comments) | Facebook Comments API | urls | `comment@1.0` | 0.3 credits/result |
| [`facebook/company-reviews`](https://docs.socq.ai/api-manual/facebook/company-reviews) | Collect public Facebook company reviews. | urls | `review@1.0` | 0.5 credits/result |
| [`facebook/event-details`](https://docs.socq.ai/api-manual/facebook/event-details) | Collect public Facebook event details. | urls | `event@1.0` | 0.5 credits/result |
| [`facebook/events-search`](https://docs.socq.ai/api-manual/facebook/events-search) | Search public Facebook events by keyword. | query | `event@1.0` | 0.6 credits/result |
| [`facebook/group-posts`](https://docs.socq.ai/api-manual/facebook/group-posts) | Collect posts from public Facebook groups. | urls | `post@1.0` | 1.2 credits/result |
| [`facebook/pages`](https://docs.socq.ai/api-manual/facebook/pages) | Facebook Page API | urls | `account@1.0` | 2.4 credits/result |
| [`facebook/posts`](https://docs.socq.ai/api-manual/facebook/posts) | Facebook Posts API | urls | `post@1.0` | 1 credits/result |
| [`facebook/profile-events`](https://docs.socq.ai/api-manual/facebook/profile-events) | Collect public Facebook profile events. | urls | `event@1.0` | 0.6 credits/result |
| [`facebook/profile-photos`](https://docs.socq.ai/api-manual/facebook/profile-photos) | Collect public Facebook profile photos. | urls | `reel-video@1.0` | 0.5 credits/result |
| [`facebook/profiles`](https://docs.socq.ai/api-manual/facebook/profiles) | Collect public Facebook profile details. | urls | `account@1.0` | 1.2 credits/result |
| [`facebook/reels`](https://docs.socq.ai/api-manual/facebook/reels) | Collect public Facebook profile reels. | urls | `reel-video@1.0` | 0.7 credits/result |
| [`facebook/video-transcript`](https://docs.socq.ai/api-manual/facebook/video-transcript) | Extract transcripts from public Facebook videos and reels. | urls | `transcript@1.0` | 0.7 credits/result |
| [`google-ad-library/ad`](https://docs.socq.ai/api-manual/google-ad-library/ad) | Collect public Google ad details. | url | `ad@1.0` | 0.5 credits/result |
| [`google-ad-library/advertiser-search`](https://docs.socq.ai/api-manual/google-ad-library/advertiser-search) | Search public Google advertisers. | query | `advertiser@1.0` | 0.5 credits/result |
| [`google-ad-library/company-ads`](https://docs.socq.ai/api-manual/google-ad-library/company-ads) | Collect public Google company ads. | one of: advertiser_id; domain | `ad@1.0` | 0.5 credits/result |
| [`google-maps/place-details`](https://docs.socq.ai/api-manual/google-maps/place-details) | Collect public Google Maps place details. | urls | `place@1.0` | 0.15 credits/result |
| [`google-maps/reviews`](https://docs.socq.ai/api-manual/google-maps/reviews) | Collect public Google Maps reviews. | urls | `review@1.0` | 0.15 credits/result |
| [`google-maps/search`](https://docs.socq.ai/api-manual/google-maps/search) | Search public Google Maps places. | location, query | `place@1.0` | 0.15 credits/result |
| [`google-play/app-detail`](https://docs.socq.ai/api-manual/google-play/app-detail) | Collect public Google Play app details. | urls | `app@1.0` | 0.15 credits/result |
| [`google-play/app-rankings`](https://docs.socq.ai/api-manual/google-play/app-rankings) | Collect public Google Play category rankings. | urls | `app@1.0` | 0.15 credits/result |
| [`google-play/app-reviews`](https://docs.socq.ai/api-manual/google-play/app-reviews) | Collect public Google Play app reviews. | urls | `review@1.0` | 0.15 credits/result |
| [`instagram/audio-reels`](https://docs.socq.ai/api-manual/instagram/audio-reels) | Collect public Instagram reels by audio identifier. | audio_ids | `reel-video@1.0` | 0.5 credits/result |
| [`instagram/comments`](https://docs.socq.ai/api-manual/instagram/comments) | Instagram Comments API | urls | `comment@1.0` | 0.3 credits/result |
| [`instagram/followers-count`](https://docs.socq.ai/api-manual/instagram/followers-count) | Instagram Followers Count API | one of: urls; usernames | `account@1.0` | 0.52 credits/result |
| [`instagram/followers-list`](https://docs.socq.ai/api-manual/instagram/followers-list) | Collect public profiles from an Instagram account follower list. | usernames | `relationship@1.0` | 0.3 credits/result |
| [`instagram/following-list`](https://docs.socq.ai/api-manual/instagram/following-list) | Collect public profiles followed by an Instagram account. | usernames | `relationship@1.0` | 0.3 credits/result |
| [`instagram/hashtag-posts`](https://docs.socq.ai/api-manual/instagram/hashtag-posts) | Collect public Instagram posts matching a hashtag. | hashtags | `post@1.0` | 0.5 credits/result |
| [`instagram/highlight-items`](https://docs.socq.ai/api-manual/instagram/highlight-items) | Collect public Instagram highlight items. | highlight_ids | `highlight@1.0` | 0.5 credits/result |
| [`instagram/post-info`](https://docs.socq.ai/api-manual/instagram/post-info) | Collect public Instagram post details. | urls | `post@1.0` | 0.5 credits/result |
| [`instagram/posts`](https://docs.socq.ai/api-manual/instagram/posts) | Instagram Post API | one of: urls; usernames | `post@1.0` | 0.34 credits/result |
| [`instagram/profiles`](https://docs.socq.ai/api-manual/instagram/profiles) | Collect public Instagram profile metadata and statistics. | usernames | `account@1.0` | 0.6 credits/result |
| [`instagram/reels`](https://docs.socq.ai/api-manual/instagram/reels) | Instagram Reel API | one of: urls; usernames | `reel-video@1.0` | 0.52 credits/result |
| [`instagram/reels-search`](https://docs.socq.ai/api-manual/instagram/reels-search) | Search public Instagram reels. | query | `reel-video@1.0` | 0.5 credits/result |
| [`instagram/search`](https://docs.socq.ai/api-manual/instagram/search) | Instagram Search API | query | `account@1.0` | 0.54 credits/result |
| [`instagram/story-highlights`](https://docs.socq.ai/api-manual/instagram/story-highlights) | Collect public Instagram story highlights. | usernames | `highlight@1.0` | 0.5 credits/result |
| [`instagram/tagged-posts`](https://docs.socq.ai/api-manual/instagram/tagged-posts) | Collect public posts that tag an Instagram profile. | usernames | `post@1.0` | 0.5 credits/result |
| [`instagram/transcript`](https://docs.socq.ai/api-manual/instagram/transcript) | Extract transcripts from public Instagram posts and reels. | urls | `transcript@1.0` | 0.7 credits/result |
| [`instagram/trending-reels`](https://docs.socq.ai/api-manual/instagram/trending-reels) | Collect public trending Instagram reels. | none | `reel-video@1.0` | 0.5 credits/result |
| [`kwai/post`](https://docs.socq.ai/api-manual/kwai/post) | Collect a public Kwai post. | url | `post@1.0` | 0.19 credits/request |
| [`kwai/profile`](https://docs.socq.ai/api-manual/kwai/profile) | Collect a public Kwai profile. | one of: url; username | `account@1.0` | 0.19 credits/request |
| [`kwai/user-posts`](https://docs.socq.ai/api-manual/kwai/user-posts) | Collect one page of public Kwai user posts. | one of: url; username | `post@1.0` | 0.19 credits/request |
| [`linkedin-ad-library/ad`](https://docs.socq.ai/api-manual/linkedin-ad-library/ad) | Collect public LinkedIn ad details. | url | `ad@1.0` | 0.5 credits/result |
| [`linkedin-ad-library/search`](https://docs.socq.ai/api-manual/linkedin-ad-library/search) | Search public LinkedIn ads. | one of: company; company_id; keyword | `ad@1.0` | 0.5 credits/result |
| [`linkedin/companies`](https://docs.socq.ai/api-manual/linkedin/companies) | LinkedIn Companies API | urls | `company@1.0` | 2 credits/result |
| [`linkedin/company-jobs`](https://docs.socq.ai/api-manual/linkedin/company-jobs) | Collect public LinkedIn company jobs. | urls | `job@1.0` | 0.5 credits/result |
| [`linkedin/company-posts`](https://docs.socq.ai/api-manual/linkedin/company-posts) | Collect public LinkedIn company posts. | urls | `post@1.0` | 1 credits/result |
| [`linkedin/jobs`](https://docs.socq.ai/api-manual/linkedin/jobs) | LinkedIn Jobs API | urls | `job@1.0` | 0.8 credits/result |
| [`linkedin/post-comments`](https://docs.socq.ai/api-manual/linkedin/post-comments) | Collect public LinkedIn post comments. | url | `comment@1.0` | 0.5 credits/result |
| [`linkedin/posts`](https://docs.socq.ai/api-manual/linkedin/posts) | LinkedIn Posts API | urls | `post@1.0` | 1 credits/result |
| [`linkedin/profile-posts`](https://docs.socq.ai/api-manual/linkedin/profile-posts) | Collect public LinkedIn profile posts. | urls | `post@1.0` | 1 credits/result |
| [`linkedin/profiles`](https://docs.socq.ai/api-manual/linkedin/profiles) | LinkedIn Profiles API | urls | `account@1.0` | 2.5 credits/result |
| [`linkedin/search-jobs`](https://docs.socq.ai/api-manual/linkedin/search-jobs) | Search public LinkedIn jobs. | location | `job@1.0` | 0.5 credits/result |
| [`linkedin/search-people`](https://docs.socq.ai/api-manual/linkedin/search-people) | Search public LinkedIn people. | urls | `account@1.0` | 1 credits/result |
| [`linkedin/search-posts`](https://docs.socq.ai/api-manual/linkedin/search-posts) | Search public LinkedIn posts. | query | `post@1.0` | 0.5 credits/result |
| [`pinterest/pins`](https://docs.socq.ai/api-manual/pinterest/pins) | Pinterest Pins API | urls | `post@1.0` | 0.5 credits/result |
| [`pinterest/profiles`](https://docs.socq.ai/api-manual/pinterest/profiles) | Pinterest Profiles API | urls | `account@1.0` | 0.6 credits/result |
| [`pinterest/search`](https://docs.socq.ai/api-manual/pinterest/search) | Pinterest Search API | query | `post@1.0` | 0.6 credits/result |
| [`pinterest/user-pins`](https://docs.socq.ai/api-manual/pinterest/user-pins) | Pinterest User Pins API | urls | `post@1.0` | 0.5 credits/result |
| [`reddit/comments`](https://docs.socq.ai/api-manual/reddit/comments) | Reddit Comments API | urls | `comment@1.0` | 0.3 credits/result |
| [`reddit/posts`](https://docs.socq.ai/api-manual/reddit/posts) | Reddit Posts API | urls | `post@1.0` | 0.5 credits/result |
| [`reddit/search`](https://docs.socq.ai/api-manual/reddit/search) | Reddit Search API | query | `post@1.0` | 0.6 credits/result |
| [`reddit/subreddit-details`](https://docs.socq.ai/api-manual/reddit/subreddit-details) | Collect public Reddit community metadata. | urls | `account@1.0` | 0.5 credits/result |
| [`reddit/subreddit-posts`](https://docs.socq.ai/api-manual/reddit/subreddit-posts) | Reddit Subreddit Posts API | urls | `post@1.0` | 0.5 credits/result |
| [`reddit/subreddit-search`](https://docs.socq.ai/api-manual/reddit/subreddit-search) | Search public posts inside one Reddit community. | query, urls | `post@1.0` | 0.6 credits/result |
| [`rednote/comment-replies`](https://docs.socq.ai/api-manual/rednote/comment-replies) | Collect one page of public Rednote comment replies. | comment_id, url | `comment@1.0` | 1 credits/request |
| [`rednote/home-recommendations`](https://docs.socq.ai/api-manual/rednote/home-recommendations) | Collect public Rednote home recommendations. | none | `post@1.0` | 1 credits/request |
| [`rednote/note-comments`](https://docs.socq.ai/api-manual/rednote/note-comments) | Collect one page of public Rednote note comments. | url | `comment@1.0` | 1 credits/request |
| [`rednote/note-detail`](https://docs.socq.ai/api-manual/rednote/note-detail) | Collect public Rednote note details. | url | `post@1.0` | 1 credits/request |
| [`rednote/search-notes`](https://docs.socq.ai/api-manual/rednote/search-notes) | Search public Rednote notes. | query | `post@1.0` | 1 credits/request |
| [`rednote/search-users`](https://docs.socq.ai/api-manual/rednote/search-users) | Search public Rednote users. | query | `account@1.0` | 1 credits/request |
| [`rednote/user-notes`](https://docs.socq.ai/api-manual/rednote/user-notes) | Collect one page of public Rednote user notes. | one of: url; user_id | `post@1.0` | 1 credits/request |
| [`rednote/user-profile`](https://docs.socq.ai/api-manual/rednote/user-profile) | Collect a public Rednote profile. | one of: url; user_id | `account@1.0` | 1 credits/request |
| [`seo/google-organic-serp`](https://docs.socq.ai/api-manual/seo/google-organic-serp) | Retrieve live organic search results. | query | `serp-result@1.0` | 0.1 credits/result |
| [`seo/keyword-difficulty`](https://docs.socq.ai/api-manual/seo/keyword-difficulty) | Calculate ranking difficulty for each input keyword. | keywords | `seo-keyword@1.0` | 0.1 credits/input |
| [`seo/keyword-overview`](https://docs.socq.ai/api-manual/seo/keyword-overview) | Return combined metrics for each input keyword. | keywords | `seo-keyword@1.0` | 0.15 credits/input |
| [`seo/keyword-search-volume`](https://docs.socq.ai/api-manual/seo/keyword-search-volume) | Batch search volume, CPC, competition, and monthly trends. | keywords | `seo-keyword@1.0` | 24 credits/request |
| [`seo/keyword-suggestions`](https://docs.socq.ai/api-manual/seo/keyword-suggestions) | Find long-tail terms containing a seed keyword. | query | `seo-keyword@1.0` | 0.1 credits/result |
| [`seo/keywords-for-site`](https://docs.socq.ai/api-manual/seo/keywords-for-site) | Generate keywords relevant to a website. | target | `seo-keyword@1.0` | 0.1 credits/result |
| [`seo/ranked-keywords`](https://docs.socq.ai/api-manual/seo/ranked-keywords) | Find keywords already ranked by a domain or page. | target | `seo-keyword@1.0` | 0.1 credits/result |
| [`seo/related-keywords`](https://docs.socq.ai/api-manual/seo/related-keywords) | Find semantically and lexically related keywords. | query | `seo-keyword@1.0` | 0.1 credits/result |
| [`seo/relevant-pages`](https://docs.socq.ai/api-manual/seo/relevant-pages) | Find pages with measurable SEO value. | target | `serp-result@1.0` | 0.15 credits/result |
| [`seo/search-intent`](https://docs.socq.ai/api-manual/seo/search-intent) | Classify the intent of each input keyword. | keywords | `seo-keyword@1.0` | 0.1 credits/input |
| [`snapchat/profile`](https://docs.socq.ai/api-manual/snapchat/profile) | Collect a public Snapchat profile. | username | `account@1.0` | 0.19 credits/request |
| [`snapchat/spotlight`](https://docs.socq.ai/api-manual/snapchat/spotlight) | Collect a public Snapchat Spotlight item. | url | `reel-video@1.0` | 0.19 credits/request |
| [`snapchat/spotlight-comments`](https://docs.socq.ai/api-manual/snapchat/spotlight-comments) | Collect one page of public Snapchat Spotlight comments. | url | `comment@1.0` | 0.19 credits/request |
| [`threads/posts`](https://docs.socq.ai/api-manual/threads/posts) | Threads Posts API | urls | `post@1.0` | 0.5 credits/result |
| [`threads/profiles`](https://docs.socq.ai/api-manual/threads/profiles) | Threads Profiles API | urls | `account@1.0` | 0.6 credits/result |
| [`threads/user-posts`](https://docs.socq.ai/api-manual/threads/user-posts) | Threads User Posts API | urls | `post@1.0` | 0.5 credits/result |
| [`tiktok-ad-library/ad`](https://docs.socq.ai/api-manual/tiktok-ad-library/ad) | Collect public TikTok ad details. | url | `ad@1.0` | 0.5 credits/result |
| [`tiktok-ad-library/search`](https://docs.socq.ai/api-manual/tiktok-ad-library/search) | Search public TikTok ads. | query | `ad@1.0` | 0.5 credits/result |
| [`tiktok-shop/product`](https://docs.socq.ai/api-manual/tiktok-shop/product) | TikTok Shop Product API | url | `product@1.0` | 0.7 credits/result |
| [`tiktok-shop/product-reviews`](https://docs.socq.ai/api-manual/tiktok-shop/product-reviews) | TikTok Shop Product Reviews API | url | `review@1.0` | 0.3 credits/result |
| [`tiktok-shop/products`](https://docs.socq.ai/api-manual/tiktok-shop/products) | TikTok Shop Products API | url | `product@1.0` | 0.7 credits/result |
| [`tiktok-shop/search`](https://docs.socq.ai/api-manual/tiktok-shop/search) | TikTok Shop Search API | query | `product@1.0` | 0.7 credits/result |
| [`tiktok-shop/user-showcase`](https://docs.socq.ai/api-manual/tiktok-shop/user-showcase) | TikTok Shop User Showcase API | username | `product@1.0` | 0.7 credits/result |
| [`tiktok/comment-replies`](https://docs.socq.ai/api-manual/tiktok/comment-replies) | Collect public TikTok comment replies. | comment_id, url | `comment@1.0` | 0.5 credits/result |
| [`tiktok/comments`](https://docs.socq.ai/api-manual/tiktok/comments) | TikTok Comments API | urls | `comment@1.0` | 0.25 credits/result |
| [`tiktok/followers-list`](https://docs.socq.ai/api-manual/tiktok/followers-list) | Collect public TikTok follower profiles. | usernames | `relationship@1.0` | 0.5 credits/result |
| [`tiktok/following-list`](https://docs.socq.ai/api-manual/tiktok/following-list) | Collect public TikTok followed profiles. | usernames | `relationship@1.0` | 0.5 credits/result |
| [`tiktok/hashtags`](https://docs.socq.ai/api-manual/tiktok/hashtags) | TikTok Hashtags API | hashtags | `hashtag-trend@1.0` | 0.7 credits/result |
| [`tiktok/live-room-info`](https://docs.socq.ai/api-manual/tiktok/live-room-info) | Collect public TikTok live room metadata and audience metrics. | room_id, user_id | `live-room@1.0` | 0.5 credits/result |
| [`tiktok/popular-songs`](https://docs.socq.ai/api-manual/tiktok/popular-songs) | Get the TikTok App Top 50 or Viral 50 music chart. Choose chart_type top or viral. results_limit defaults to 20, maximum 50. | none | `music@1.0` | 0.5 credits/result |
| [`tiktok/profiles`](https://docs.socq.ai/api-manual/tiktok/profiles) | TikTok Profiles API | usernames | `account@1.0` | 0.6 credits/result |
| [`tiktok/search`](https://docs.socq.ai/api-manual/tiktok/search) | TikTok Search API | query | `reel-video@1.0` | 0.7 credits/result |
| [`tiktok/search-users`](https://docs.socq.ai/api-manual/tiktok/search-users) | Search public TikTok accounts by keyword. | query | `account@1.0` | 0.6 credits/result |
| [`tiktok/song`](https://docs.socq.ai/api-manual/tiktok/song) | Collect public TikTok sound or song details. | one of: music_id; url | `music@1.0` | 0.5 credits/result |
| [`tiktok/song-videos`](https://docs.socq.ai/api-manual/tiktok/song-videos) | Collect public TikTok videos that use a sound. | music_ids | `reel-video@1.0` | 0.5 credits/result |
| [`tiktok/top-search`](https://docs.socq.ai/api-manual/tiktok/top-search) | Search public TikTok videos and photo carousels. | query | `reel-video@1.0` | 0.7 credits/result |
| [`tiktok/trending-feed`](https://docs.socq.ai/api-manual/tiktok/trending-feed) | Collect trending TikTok videos for a region. | region | `reel-video@1.0` | 0.7 credits/result |
| [`tiktok/user-live`](https://docs.socq.ai/api-manual/tiktok/user-live) | Check public TikTok accounts for live streaming status, including offline results. | usernames | `live-status@1.0` | 0.5 credits/result |
| [`tiktok/user-videos`](https://docs.socq.ai/api-manual/tiktok/user-videos) | Collect public videos from TikTok profiles. | usernames | `reel-video@1.0` | 0.5 credits/result |
| [`tiktok/video-transcript`](https://docs.socq.ai/api-manual/tiktok/video-transcript) | Extract transcripts from public TikTok videos. | urls | `transcript@1.0` | 0.5 credits/result |
| [`tiktok/videos`](https://docs.socq.ai/api-manual/tiktok/videos) | TikTok Videos API | urls | `reel-video@1.0` | 0.7 credits/result |
| [`truth-social/post`](https://docs.socq.ai/api-manual/truth-social/post) | Collect a public Truth Social post. | url | `post@1.0` | 0.19 credits/request |
| [`truth-social/profile`](https://docs.socq.ai/api-manual/truth-social/profile) | Collect a public Truth Social profile. | username | `account@1.0` | 0.19 credits/request |
| [`truth-social/user-posts`](https://docs.socq.ai/api-manual/truth-social/user-posts) | Collect one page of public Truth Social user posts. | one of: user_id; username | `post@1.0` | 0.19 credits/request |
| [`twitch/profile`](https://docs.socq.ai/api-manual/twitch/profile) | Collect a public Twitch profile. | username | `account@1.0` | 0.19 credits/request |
| [`twitch/user-videos`](https://docs.socq.ai/api-manual/twitch/user-videos) | Collect one page of public Twitch user videos. | username | `reel-video@1.0` | 0.19 credits/request |
| [`x/community`](https://docs.socq.ai/api-manual/x/community) | Get public X community metadata, member counts, rules and membership policies. | urls | `community@1.0` | 0.5 credits/result |
| [`x/community-posts`](https://docs.socq.ai/api-manual/x/community-posts) | Collect public posts from X communities in creation-time order. | urls | `post@1.0` | 0.7 credits/result |
| [`x/followers-list`](https://docs.socq.ai/api-manual/x/followers-list) | Collect public X follower profiles. | usernames | `relationship@1.0` | 0.5 credits/result |
| [`x/following-list`](https://docs.socq.ai/api-manual/x/following-list) | Collect public X followed profiles. | usernames | `relationship@1.0` | 0.5 credits/result |
| [`x/mentions`](https://docs.socq.ai/api-manual/x/mentions) | Collect public posts that mention an X account. | usernames | `post@1.0` | 0.7 credits/result |
| [`x/post-quotes`](https://docs.socq.ai/api-manual/x/post-quotes) | Collect public quotes of X posts. | urls | `post@1.0` | 0.5 credits/result |
| [`x/post-replies`](https://docs.socq.ai/api-manual/x/post-replies) | Collect public replies to X posts. | urls | `comment@1.0` | 0.5 credits/result |
| [`x/post-retweeters`](https://docs.socq.ai/api-manual/x/post-retweeters) | Collect public profiles that reposted X posts. | urls | `relationship@1.0` | 0.5 credits/result |
| [`x/posts`](https://docs.socq.ai/api-manual/x/posts) | X Posts API | urls | `post@1.0` | 0.5 credits/result |
| [`x/profiles`](https://docs.socq.ai/api-manual/x/profiles) | X Profiles API | usernames | `account@1.0` | 0.6 credits/result |
| [`x/search`](https://docs.socq.ai/api-manual/x/search) | X Search API | query | `post@1.0` | 0.7 credits/result |
| [`x/search-users`](https://docs.socq.ai/api-manual/x/search-users) | Search public X accounts by keyword. | query | `account@1.0` | 0.6 credits/result |
| [`x/thread-context`](https://docs.socq.ai/api-manual/x/thread-context) | Collect the target X post, its ancestors and replies while preserving thread relationships. | urls | `thread-post@1.0` | 0.5 credits/result |
| [`x/trends`](https://docs.socq.ai/api-manual/x/trends) | Collect public X trends by location identifier. | woeids | `hashtag-trend@1.0` | 0.5 credits/result |
| [`x/user-posts`](https://docs.socq.ai/api-manual/x/user-posts) | X User Posts API | usernames | `post@1.0` | 0.5 credits/result |
| [`youtube/channel-live-videos`](https://docs.socq.ai/api-manual/youtube/channel-live-videos) | Collect public YouTube channel live videos. | urls | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/channel-videos`](https://docs.socq.ai/api-manual/youtube/channel-videos) | YouTube Channel Videos API | urls | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/channels`](https://docs.socq.ai/api-manual/youtube/channels) | YouTube Channels API | urls | `account@1.0` | 0.26 credits/result |
| [`youtube/comment-replies`](https://docs.socq.ai/api-manual/youtube/comment-replies) | Collect public YouTube comment replies. | one of: comment_id + url; continuation_token | `comment@1.0` | 0.5 credits/result |
| [`youtube/comments`](https://docs.socq.ai/api-manual/youtube/comments) | YouTube Comments API | urls | `comment@1.0` | 0.3 credits/result |
| [`youtube/community-posts`](https://docs.socq.ai/api-manual/youtube/community-posts) | Collect public YouTube community posts. | urls | `post@1.0` | 0.5 credits/result |
| [`youtube/hashtag-search`](https://docs.socq.ai/api-manual/youtube/hashtag-search) | Search public YouTube videos by hashtag. | hashtags | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/playlist-videos`](https://docs.socq.ai/api-manual/youtube/playlist-videos) | Collect videos from a public YouTube playlist. | urls | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/search`](https://docs.socq.ai/api-manual/youtube/search) | YouTube Search API | query | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/shorts`](https://docs.socq.ai/api-manual/youtube/shorts) | YouTube Shorts API | urls | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/transcripts`](https://docs.socq.ai/api-manual/youtube/transcripts) | YouTube Transcripts API | urls | `transcript@1.0` | 0.5 credits/result |
| [`youtube/videos`](https://docs.socq.ai/api-manual/youtube/videos) | YouTube Videos API | urls | `reel-video@1.0` | 0.5 credits/result |
