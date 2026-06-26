# Facebook API Endpoints

Base path: `/v1/facebook`

## Profile & Pages

### Profile
```
GET /v1/facebook/profile?handle={page_name}
```
Public page data. Pass `get_business_hours=true` to include business hours.

## Content

### Profile Posts
```
GET /v1/facebook/profile/posts?handle={page_name}&cursor={cursor}
```
Posts from a Facebook profile/page.

### Profile Reels
```
GET /v1/facebook/profile/reels?handle={page_name}&cursor={cursor}
```
Reels from a Facebook profile/page.

### Profile Photos
```
GET /v1/facebook/profile/photos?handle={page_name}&cursor={cursor}
```
Photos from a Facebook profile/page.

### Post Details
```
GET /v1/facebook/post?url={post_url}
```
Full details for a specific Facebook post.

### Group Posts
```
GET /v1/facebook/group/posts?group_id={id}&cursor={cursor}
```
Public posts from a Facebook group.

### Transcript
```
GET /v1/facebook/post/transcript?url={post_url}
```
Transcript endpoint for Facebook posts/reels. Pass the post URL.

## Comments

### Post Comments
```
GET /v1/facebook/post/comments?url={post_url}&cursor={cursor}
```
Comments on a Facebook post. Passing `feedback_id` instead of URL is significantly faster because it skips the URL resolution step — use it when you've already fetched the post and have the `feedback_id` from the response.

```
GET /v1/facebook/post/comments?feedback_id={id}&cursor={cursor}
```

## Ad Library

### Ad Details
```
GET /v1/facebook/adLibrary/ad?url={ad_url}
```
Full details for a specific ad. Includes EU transparency data.

### Search Ads
```
GET /v1/facebook/adLibrary/search/ads?query={company_name}&cursor={cursor}
```
Search the Meta Ad Library. Note the camelCase `adLibrary` in the path — this is different from most other endpoints and a common source of 404 errors.

Parameters:
- `sort_by` — sort by `total_impressions` or `relevancy_monthly_grouped`
- `start_date` / `end_date` — filter by date range
- `language` — filter by language

### Company Ads
```
GET /v1/facebook/adLibrary/company/ads?company_id={id}&cursor={cursor}
```
Ads for a specific company in the Meta Ad Library.

### Search Companies
```
GET /v1/facebook/adLibrary/search/companies?query={company_name}&cursor={cursor}
```
Search for companies in the Meta Ad Library.

## Notes

- Profile content is split into separate endpoints: posts, reels, and photos
- For comments, using `feedback_id` is much faster than passing the URL
- Ad library supports sorting by `total_impressions` or `relevancy_monthly_grouped`, plus date and language filters
- AI transcripts limited to videos under 2 minutes
- Use `trim=true` to reduce response size
