# Apify Actors — Fallback Scraping Reference

Use these when `web_fetch` + browser mode are both blocked. Requires
`APIFY_API_TOKEN` to be set.

---

## Base API call pattern

```bash
curl -s -X POST \
  "https://api.apify.com/v2/acts/{ACTOR_ID}/run-sync-get-dataset-items?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{INPUT_JSON}'
```

Response: JSON array of result objects.

---

## Actor Registry

### YouTube Channel Scraper
- **Actor ID**: `streamers/youtube-channel-scraper`
- **Input**:
```json
{
  "startUrls": [{"url": "https://www.youtube.com/@{handle}"}],
  "maxResults": 1
}
```
- **Key output fields**: `channelName`, `subscriberCount`, `videoCount`, `totalViewCount`, `description`, `channelUrl`

---

### Instagram Profile Scraper
- **Actor ID**: `apify/instagram-profile-scraper`
- **Input**:
```json
{
  "usernames": ["{handle}"],
  "resultsLimit": 1
}
```
- **Key output fields**: `username`, `fullName`, `biography`, `followersCount`, `followingCount`, `postsCount`, `verified`, `externalUrl`

---

### TikTok Profile Scraper
- **Actor ID**: `clockworks/tiktok-profile-scraper`
- **Input**:
```json
{
  "profiles": ["https://www.tiktok.com/@{handle}"],
  "resultsPerPage": 1
}
```
- **Key output fields**: `userInfo.user`, `userInfo.stats`

---

### Twitter / X Profile Scraper
- **Actor ID**: `apidojo/tweet-scraper`
- **Input**:
```json
{
  "startUrls": [{"url": "https://x.com/{handle}"}],
  "maxItems": 1,
  "mode": "profile"
}
```
- **Key output fields**: `author.name`, `author.followers`, `author.verified`, `author.description`

---

### LinkedIn Profile Scraper
- **Actor ID**: `dev_fusion/linkedin-profile-scraper`
- **Input**:
```json
{
  "profileUrls": ["https://www.linkedin.com/in/{handle}/"]
}
```
- **Key output fields**: `fullName`, `headline`, `summary`, `company`, `location`

---

### Twitch Channel Scraper
- **Actor ID**: `epctex/twitch-scraper`
- **Input**:
```json
{
  "startUrls": [{"url": "https://www.twitch.tv/{handle}"}],
  "maxItems": 1
}
```
- **Key output fields**: `displayName`, `description`, `followers`, `isLive`, `viewerCount`

---

## Cost note

Each Apify actor run costs Apify compute units. Typical profile scrapes use
0.01–0.1 CU each. The free tier includes ~5 CU/month. See
https://apify.com/pricing for current rates.
