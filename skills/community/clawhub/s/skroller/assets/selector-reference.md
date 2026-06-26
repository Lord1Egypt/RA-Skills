# CSS Selector Reference

Quick reference for social media automation selectors. Test before each run—platforms change these frequently.

## ⚠️ Compliance Notice

Before using these selectors:
- Review each platform's Terms of Service
- Respect rate limits and robots.txt
- Use for permitted purposes only (research, personal analysis)
- Do not collect personal data at scale without consent
- Comply with GDPR, CCPA, and applicable privacy laws

---

## Twitter/X

```css
/* Post container */
[data-testid="tweet"]

/* Post text */
[data-testid="tweetText"]

/* Author name */
[data-testid="User-Name"]

/* Timestamp */
time[datetime]

/* Engagement metrics */
[data-testid="like"] span
[data-testid="retweet"] span
[data-testid="reply"] span

/* Post URL */
a[href*="/status/"]

/* Hashtags */
a[href*="/hashtag/"]

/* Media */
[data-testid="tweetPhoto"] img
video[src]
```

**Test:**
```bash
node -e "console.log(document.querySelector('[data-testid=\"tweet\"]'))"
```

---

## Reddit

```css
/* Post container (new design) */
[data-testid="post-container"]

/* Post title */
[data-testid="post-title"]

/* Author */
[data-testid="post-author"]

/* Score/votes */
[data-testid="vote-count"]

/* Subreddit name */
[data-testid="subreddit-name"]

/* Post URL */
a[href*="/comments/"]

/* Thumbnail */
[data-testid="post-thumbnail"]

/* Flair */
[data-testid="post-flair"]
```

**Test:**
```bash
curl "https://www.reddit.com/search.json?q=test" | jq '.data.children[0].data'
```

---

## Instagram

```css
/* Post article */
article

/* Post link */
a[href*="/p/"]

/* Author aria label */
a[aria-label*="profile"]

/* Likes count */
span containing "likes"

/* Caption */
a[aria-label*="Image by"]

/* Comments count */
span containing "comments"

/* Reel indicator */
[data-testid="reel-play-button"]
```

**Note:** Instagram selectors change frequently. Use browser dev tools to inspect.

---

## TikTok

```css
/* Video post */
[data-e2e="search-post"]

/* Description */
[data-e2e="search-post-desc"]

/* Author */
[data-e2e="search-post-author"]

/* Likes */
[data-e2e="search-post-like"]

/* Comments */
[data-e2e="search-post-comment"]

/* Shares */
[data-e2e="search-post-share"]

/* Video thumbnail */
[data-e2e="search-post-img"]
```

**Test:**
```bash
node -e "console.log(document.querySelector('[data-e2e=\"search-post\"]'))"
```

---

## LinkedIn

```css
/* Post container */
div.ember-view[data-id]

/* Post text */
span[dir="ltr"]

/* Author link */
a[href*="/in/"]

/* Author name */
a[href*="/in/"] span

/* Timestamp */
span[aria-label]

/* Likes button */
button[aria-label*="Like"]

/* Comments button */
button[aria-label*="Comment"]

/* Post URL */
a[href*="/posts/"]
```

**Note:** LinkedIn requires login for most content.

---

## YouTube

```css
/* Video renderer */
ytd-video-renderer

/* Video title */
#video-title

/* Channel name */
#channel-name

/* View count */
#metadata-line

/* Thumbnail */
#thumbnail img

/* Video URL */
#video-title href

/* Duration */
#text[aria-label*="seconds"]
```

**API Alternative:**
```javascript
// More reliable
GET https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={API_KEY}
```

---

## Debugging Selectors

### Quick Test in Browser Console
```javascript
// Test if selector matches anything
document.querySelectorAll('SELECTOR').length

// Log first match
console.log(document.querySelector('SELECTOR'))

// Watch for dynamic loading
new MutationObserver(() => {
  console.log('New elements:', document.querySelectorAll('SELECTOR').length);
}).observe(document.body, { childList: true, subtree: true });
```

### Playwright Debug Mode
```bash
PWDEBUG=1 node scripts/skroller.js --platform twitter --query test
```

### Selector Validation Script
```javascript
// Save as test-selectors.js
const platforms = {
  twitter: '[data-testid="tweet"]',
  reddit: '[data-testid="post-container"]',
  // ... add more
};

for (const [platform, selector] of Object.entries(platforms)) {
  const count = document.querySelectorAll(selector).length;
  console.log(`${platform}: ${count} matches`);
}
```

---

## Updating Selectors

When selectors break:

1. Open browser dev tools (F12)
2. Inspect element on a post
3. Copy selector (right-click → Copy → Copy selector)
4. Test in console: `document.querySelectorAll('new-selector').length`
5. Update `scripts/skroller.js` and `references/platform-details.md`
6. Test the skill end-to-end

**Pro tip:** Use multiple fallback selectors:
```javascript
const postSelector = '[data-testid="tweet"]' || '.tweet-container' || '.js-stream-item';
```

---

## Legal & Ethical Use

**Before automating content collection:**
- ✅ Verify your use case complies with platform ToS
- ✅ Check robots.txt for allowed paths
- ✅ Respect rate limits to avoid service disruption
- ✅ Do not collect personal data without consent
- ✅ Use for research, analysis, or permitted purposes only
- ❌ Do not resell or redistribute collected data commercially
- ❌ Do not use for harassment, spam, or manipulation
- ❌ Do not bypass authentication or access controls

**GDPR/CCPA Compliance:**
- Anonymize any personal data collected
- Honor data deletion requests
- Limit retention to necessary periods
- Document lawful basis for processing

---

## Hacker News

```css
/* Post container */
.athing

/* Title link */
.titleline a

/* Author */
.hnuser

/* Score/points */
.score

/* Timestamp */
.age

/* Domain */
.sitebitexpost
```

**Test:**
```bash
curl -s "https://news.ycombinator.com/search?query=test" | grep -o '.athing' | wc -l
```

---

## Product Hunt

```css
/* Search result */
[data-test="search-result"]

/* Headline/title */
[data-test="headline"]

/* User name */
[data-test="user-name"]

/* Vote button */
[data-test="vote-button"]

/* Post link */
a[href*="/posts/"]
```

---

## Medium

```css
/* Article */
article

/* Title */
[data-testid="post-title"]

/* Author name */
[data-testid="post-author-name"]

/* Claps count */
[data-testid="clap-count"]

/* URL */
a[data-testid="post-title"] href

/* Timestamp */
time[datetime]
```

---

## GitHub

```css
/* Issue/PR row */
li.Box-row

/* Title */
a.title

/* Author */
a.author

/* Comments count */
[aria-label*="comment"]

/* URL */
a.title href

/* Timestamp */
relative-time[datetime]
```

**API Alternative:**
```bash
# More reliable
curl "https://api.github.com/search/issues?q=bug+is:open"
```

---

## Pinterest

```css
/* Pin grid item */
[data-grid-item]

/* Pin title */
[data-pin-title]

/* Pin user */
[data-pin-user]

/* Save count */
[data-save-count]

/* Pin URL */
a[href*="/pin/"]
```

**Note:** Pinterest has aggressive bot detection. Use sparingly.
