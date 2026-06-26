# Platform Selectors Reference

Per-platform extraction hints for `scrape-creator-profile`. Use these to
target the right elements after fetching a page.

---

## YouTube

| Field | Selector / Path |
|-------|----------------|
| Display name | `<meta name="title">` or `yt-formatted-string#text.ytd-channel-name` |
| Subscriber count | `#subscriber-count` · `yt-formatted-string.ytd-subscribe-button-renderer` · `meta[itemprop="interactionCount"]` |
| Bio / About | `#description-inner` on the About tab · `<meta name="description">` |
| Verified badge | `#channel-header .badge-style-type-verified` |
| Avatar | `#avatar img` |
| Total views | `yt-formatted-string.ytd-channel-about-metadata-renderer` (look for "views" label) |
| Recent videos | `ytd-rich-item-renderer` → title in `#video-title`, views in `#metadata-line` |
| JSON-LD | `<script type="application/ld+json">` — `@type: "ProfilePage"` |

**Notes**: YouTube usually renders with web_fetch. The About tab is a separate
URL: `https://www.youtube.com/@{handle}/about` — fetch this for bio and view
count data.

---

## Instagram

| Field | Selector / Path |
|-------|----------------|
| All profile data | `window._sharedData.entry_data.ProfilePage[0].graphql.user` (older) |
| New API response | `<script type="application/json" data-sjs>` — look for `"profile_pic_url"` key |
| Follower count | `edge_followed_by.count` in JSON blob |
| Following count | `edge_follow.count` in JSON blob |
| Post count | `edge_owner_to_timeline_media.count` |
| Bio | `biography` field |
| Verified | `is_verified` boolean |
| External URL | `external_url` field |

**Notes**: Instagram almost always requires browser mode. Extract JSON from
page source before JS execution when possible — look for the `<script>` tag
containing `"biography"`.

---

## TikTok

| Field | Selector / Path |
|-------|----------------|
| All profile data | `<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">` |
| Within JSON | `__DEFAULT_SCOPE__["webapp.user-detail"].userInfo.user` |
| Follower count | `userInfo.stats.followerCount` |
| Following count | `userInfo.stats.followingCount` |
| Heart/like count | `userInfo.stats.heartCount` |
| Video count | `userInfo.stats.videoCount` |
| Bio | `userInfo.user.signature` |
| Verified | `userInfo.user.verified` |
| Avatar | `userInfo.user.avatarLarger` |

**Notes**: Requires browser mode. Parse the JSON blob — do not rely on CSS
selectors as TikTok's class names are obfuscated and change frequently.

---

## Twitter / X

| Field | Selector / Path |
|-------|----------------|
| Display name | `[data-testid="UserName"] span:first-child` |
| Handle | `[data-testid="UserName"] span:nth-child(2)` |
| Bio | `[data-testid="UserDescription"]` |
| Follower count | `a[href$="/followers"] span` |
| Following count | `a[href$="/following"] span` |
| Verified | `[data-testid="icon-verified"]` or `[aria-label="Verified account"]` |
| Location | `[data-testid="UserProfileHeader_Items"] [data-testid="UserLocation"]` |
| Website | `[data-testid="UserProfileHeader_Items"] a[href]` |
| Join date | `[data-testid="UserProfileHeader_Items"] [data-testid="UserJoinDate"]` |
| Avatar | `[data-testid="UserAvatar"] img` |

**Notes**: web_fetch may work for public profiles. Browser mode is more
reliable. Logged-in session improves data access.

---

## LinkedIn

| Field | Selector / Path |
|-------|----------------|
| Display name | `<meta property="og:title">` (format: "Name - Title \| LinkedIn") |
| Headline | `<meta property="og:description">` (first sentence) |
| Avatar | `<meta property="og:image">` |
| All profile data | `<script type="application/ld+json">` — `@type: "Person"` |
| Company | `schema:worksFor` in JSON-LD |
| Location | `schema:address` or Open Graph description |

**Notes**: LinkedIn aggressively blocks unauthenticated scrapers. Without a
logged-in browser session, you'll usually only get Open Graph meta tags. If
the user needs richer data, suggest they log in via browser-attach mode.

---

## Twitch

| Field | Selector / Path |
|-------|----------------|
| Display name | `<meta property="og:title">` |
| Bio | `<meta property="og:description">` |
| Avatar | `<meta property="og:image">` |
| Follower count | Requires Twitch API (see Apify actor or manual API call) |
| Viewer count (live) | `<meta name="description">` may include "watching" count |

**Notes**: Public profile pages expose limited data via meta tags. For
follower counts, use the Twitch Helix API (requires client_id) or the Apify
actor in `references/apify-actors.md`.

---

## Substack

| Field | Selector / Path |
|-------|----------------|
| Display name | `<meta property="og:title">` |
| Bio | `<meta name="description">` |
| Avatar | `<meta property="og:image">` |
| Subscriber count | Not publicly exposed |
| Recent posts | `<article>` elements on homepage — title in `h2`, date in `time` |

**Notes**: web_fetch works well for Substack. Subscriber counts are not
publicly visible; omit that field.

---

## GitHub

| Field | Selector / Path |
|-------|----------------|
| Display name | `[itemprop="name"]` |
| Bio | `[data-bio-text]` or `[itemprop="description"]` |
| Location | `[itemprop="homeLocation"]` |
| Company | `[itemprop="worksFor"]` |
| Website | `[itemprop="url"]` |
| Followers | `a[href$="?tab=followers"] span.text-bold` |
| Following | `a[href$="?tab=following"] span.text-bold` |
| Public repos | `[itemprop="owns"] .Counter` or `a[href$="tab=repositories"] span` |
| Avatar | `[itemprop="image"]` |

**Notes**: web_fetch works well for GitHub profiles.

---

## Patreon

| Field | Selector / Path |
|-------|----------------|
| Display name | `<meta property="og:title">` |
| Bio | `<meta property="og:description">` |
| Avatar | `<meta property="og:image">` |
| Patron count | Text matching "X patrons" on page |
| Monthly income | Not always public; check "per month" text |

**Notes**: web_fetch usually works. Some creators hide patron/income counts.
