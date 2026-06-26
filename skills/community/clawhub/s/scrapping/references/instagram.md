# Instagram API Endpoints

Base path: `/v1/instagram` (some endpoints have v2 versions)

## Profile & User Data

### Get Profile
```
GET /v1/instagram/profile?handle={username}
```
Returns public profile data, recent posts, and related accounts. This is the most efficient first call — it bundles profile stats with recent content, saving you from making separate requests.

### Basic Profile
```
GET /v1/instagram/basic-profile?userId={user_id}
```
Lightweight profile lookup by numeric user ID. Use this when you already have a `userId` from a previous response and need quick profile data without the overhead of the full profile endpoint. Note the parameter is `userId` (camelCase).

## Content

### User Posts (v2)
```
GET /v2/instagram/user/posts?handle={username}&cursor={cursor}
```
Paginated list of a user's public posts. Use this to get all post types (photos, carousels, reels) in chronological order.
Note: v1 version is being deprecated — use v2.

### Post/Reel Info
```
GET /v1/instagram/post?url={post_url}
```
Full details for a single post or reel: likes, comments, caption, media URLs.

### Reels
```
GET /v1/instagram/user/reels?handle={username}&cursor={cursor}
```
All public reels from a profile. Use this instead of user/posts when you specifically need video content only — it filters out photos and carousels.

### Transcript (v2)
```
GET /v2/instagram/media/transcript?url={post_url}
```
Transcript of an Instagram video post or reel. Note: this is a v2 endpoint.

### Embed HTML
```
GET /v1/instagram/user/embed?handle={username}
```
HTML embed code for a user's profile. Returns raw HTML that can be embedded in a webpage.

## Story Highlights

### Story Highlights
```
GET /v1/instagram/user/highlights?handle={username}
```
List of story highlight collections from a user. Useful for seeing how a creator organizes their evergreen content — highlights are often used for FAQs, testimonials, and product showcases.

### Highlight Details
```
GET /v1/instagram/user/highlight/detail?id={highlight_id}
```
Contents of a specific story highlight. Pass the highlight ID from the highlights list endpoint.

## Search

### Search Reels (v2)
```
GET /v2/instagram/reels/search?query={keyword}&cursor={cursor}
```
Search reels by keyword. Costs 1 credit per 10 reels, max 60 reels. Requires manual pagination.
Note: v1 version is being deprecated — use v2.

## Comments

### Post Comments (v2)
```
GET /v2/instagram/post/comments?url={post_url}&cursor={cursor}
```
Comments on a post or reel. Requires manual pagination.
Note: v1 version is being deprecated — use v2.

## Deprecated

- **Reels using Song** (`GET /v1/instagram/song/reels`) — deprecated endpoint, no longer available.

## Notes

- v2 endpoints require manual pagination (pass cursor yourself) — this gives you more control over how many results to fetch, which is important since each page costs credits
- v1 convenience endpoints that auto-paginate are being phased out (deprecated as of Feb 2026) — always prefer v2 for posts, search, and comments
- Use `trim=true` to reduce response size — especially useful for posts/reels where the full response includes large media URL arrays you may not need
