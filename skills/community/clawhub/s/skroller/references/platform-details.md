# Platform Details

Platform-specific selectors, quirks, and implementation notes for skroller.

## ⚖️ Compliance Notice

**Before collecting data from any platform:**
- Review the platform's Terms of Service regarding automated access
- Check robots.txt for disallowed paths
- Respect rate limits to avoid service disruption
- Do not collect personal data without proper legal basis
- Use only for permitted purposes (research, analysis, where allowed)
- Comply with GDPR, CCPA, and applicable privacy regulations

---

## Twitter/X

**URL Patterns:**
- Profile: `https://twitter.com/<username>`
- Search: `https://twitter.com/search?q=<query>&f=live`
- Hashtag: `https://twitter.com/search?q=%23<hashtag>`

**Key Selectors:**
```css
Post container: [data-testid="tweet"]
Text: [data-testid="tweetText"]
Author: [data-testid="User-Name"]
Timestamp: time[datetime]
Likes: [data-testid="like"] span
Retweets: [data-testid="retweet"] span
URL: a[href*="/status/"]
```

**Quirks:**
- Infinite scroll via `scroll` event
- May require login for full results
- Rate limits: ~100 requests/hour unauthenticated
- Use `f=live` for chronological vs `f=top` for algorithmic

**Anti-bot:**
- Add random delays (1-3s)
- Rotate user agents
- Consider residential proxies for high volume

---

## Reddit

**URL Patterns:**
- Search: `https://www.reddit.com/search/?q=<query>`
- Subreddit: `https://www.reddit.com/r/<subreddit>/`
- User: `https://www.reddit.com/user/<username>/`

**Key Selectors:**
```css
Post: [data-testid="post-container"]
Title: [data-testid="post-title"]
Author: [data-testid="post-author"]
Score: [data-testid="vote-count"]
URL: a[href*="/comments/"]
```

**Quirks:**
- Prefer API (`https://oauth.reddit.com`) when possible
- JSON endpoint: `https://www.reddit.com/<path>/.json`
- Rate limits: 60 requests/minute with OAuth
- No login required for most public content

**API Alternative:**
```javascript
// Use Reddit API for more reliable scraping
const response = await fetch(`https://oauth.reddit.com/search.json?q=${query}`, {
  headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();
```

---

## Instagram

**URL Patterns:**
- Profile: `https://www.instagram.com/<username>/`
- Hashtag: `https://www.instagram.com/explore/tags/<hashtag>/`
- Reels: `https://www.instagram.com/reels/`

**Key Selectors:**
```css
Post: article
Text: a[aria-label*="Image by"]
Author: a[aria-label]
Likes: span containing "likes"
URL: a[href*="/p/"]
```

**Quirks:**
- Heavy JavaScript rendering
- Login required for most content
- Rate limits: ~50 requests/hour
- Frequent selector changes
- Consider using unofficial API wrappers

**Anti-bot:**
- Very aggressive bot detection
- Use real browser fingerprints
- Limit to <100 scrolls/session
- Consider 3rd party services (scraptik, etc.)

---

## TikTok

**URL Patterns:**
- Search: `https://www.tiktok.com/search?q=<query>`
- Profile: `https://www.tiktok.com/@<username>`
- Hashtag: `https://www.tiktok.com/tag/<hashtag>`

**Key Selectors:**
```css
Post: [data-e2e="search-post"]
Desc: [data-e2e="search-post-desc"]
Author: [data-e2e="search-post-author"]
Likes: [data-e2e="search-post-like"]
URL: a[href*="/video/"]
```

**Quirks:**
- Very heavy JavaScript
- Long scroll delays needed (2-3s)
- Login recommended for full results
- Rate limits: ~30 requests/hour
- Video content requires additional handling

**Anti-bot:**
- Aggressive detection
- Use headful browser for reliability
- Add mouse movement simulation
- Consider TikTok official API for business use

---

## LinkedIn

**URL Patterns:**
- Search: `https://www.linkedin.com/search/results/content/?keywords=<query>`
- Profile: `https://www.linkedin.com/in/<username>/`
- Company: `https://www.linkedin.com/company/<company>/`

**Key Selectors:**
```css
Post: div.ember-view[data-id]
Text: span[dir="ltr"]
Author: a[href*="/in/"]
Timestamp: span[aria-label]
Likes: button[aria-label*="Like"]
URL: a[href*="/posts/"]
```

**Quirks:**
- Login required for almost all content
- Heavy Ember.js framework
- Rate limits: ~50 requests/hour
- Professional content, lower volume

**Anti-bot:**
- Login required makes scraping TOS-sensitive
- Use only for competitive research
- Consider LinkedIn API for official access
- Respect robots.txt

---

## YouTube

**URL Patterns:**
- Search: `https://www.youtube.com/results?search_query=<query>`
- Channel: `https://www.youtube.com/@<channel>`
- Video: `https://www.youtube.com/watch?v=<id>`

**Key Selectors:**
```css
Video: ytd-video-renderer
Title: #video-title
Channel: #channel-name
Views: #metadata-line
URL: #video-title href
```

**Quirks:**
- Comments require separate scraping
- Use Data API for video metadata
- Search results are algorithmic
- Rate limits: 1000 units/day (API quota)

**API Alternative:**
```javascript
// YouTube Data API for reliable metadata
const response = await fetch(
  `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${query}&key=${apiKey}`
);
```

---

## General Tips

### Selector Maintenance
- Social platforms change selectors frequently
- Test selectors before each run
- Keep selector cheatsheet updated
- Consider using text-based matching as fallback

### Performance
- Batch requests where possible
- Use API endpoints when available
- Cache results to avoid re-scraping
- Parallelize across platforms carefully

### Legal/ToS
- Review each platform's ToS
- Don't scrape personal data at scale
- Use for research, not commercial redistribution
- Consider official APIs for production use

---

## Hacker News

**URL Patterns:**
- Search: `https://news.ycombinator.com/search?query=<query>`
- Front page: `https://news.ycombinator.com/`
- New: `https://news.ycombinator.com/newest`

**Key Selectors:**
```css
Post: .athing
Title: .titleline a
Author: .hnuser
Score: .score
URL: .titleline a href
Timestamp: .age
```

**Quirks:**
- Lightweight HTML, fast scraping
- No login required
- Pagination via `?p=2` parameter
- Rate limits: Minimal, but be respectful

---

## Product Hunt

**URL Patterns:**
- Search: `https://www.producthunt.com/search?q=<query>`
- Topic: `https://www.producthunt.com/topics/<topic>`
- Leaderboard: `https://www.producthunt.com/leaderboard`

**Key Selectors:**
```css
Post: [data-test="search-result"]
Title: [data-test="headline"]
Author: [data-test="user-name"]
Votes: [data-test="vote-button"]
URL: a[href*="/posts/"]
```

**Quirks:**
- Heavy JavaScript rendering
- Login recommended for full features
- Daily leaderboard resets at midnight PST

---

## Medium

**URL Patterns:**
- Search: `https://medium.com/search?q=<query>`
- Publication: `https://medium.com/<publication>`
- Author: `https://medium.com/@<username>`

**Key Selectors:**
```css
Post: article
Title: [data-testid="post-title"]
Author: [data-testid="post-author-name"]
Claps: [data-testid="clap-count"]
URL: a[data-testid="post-title"] href
Timestamp: time[datetime]
```

**Quirks:**
- Paywall limits content access
- Member-only stories require subscription
- Infinite scroll with lazy loading

---

## GitHub

**URL Patterns:**
- Issues search: `https://github.com/search?q=<query>&type=issues`
- Repos search: `https://github.com/search?q=<query>&type=repositories`
- Discussions: `https://github.com/search?q=<query>&type=discussions`

**Key Selectors:**
```css
Issue/PR: li.Box-row
Title: a.title
Author: a.author
Comments: [aria-label*="comment"]
URL: a.title href
Timestamp: relative-time[datetime]
```

**Quirks:**
- Prefer REST API for production use
- Rate limits: 5000 req/hour authenticated
- Search syntax: `is:issue is:open`

**API Alternative:**
```javascript
// GitHub REST API
GET https://api.github.com/search/issues?q=<query>
```

---

## Pinterest

**URL Patterns:**
- Search: `https://www.pinterest.com/search/pins/?q=<query>`
- Profile: `https://www.pinterest.com/<username>/`
- Board: `https://www.pinterest.com/<username>/<board>/`

**Key Selectors:**
```css
Pin: [data-grid-item]
Title: [data-pin-title]
Author: [data-pin-user]
Saves: [data-save-count]
URL: a[href*="/pin/"]
```

**Quirks:**
- Heavy image content
- Masonry layout complicates scrolling
- Login required for most features
- Rate limits: Aggressive bot detection
