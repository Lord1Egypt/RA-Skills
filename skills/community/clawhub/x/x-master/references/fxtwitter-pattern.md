# The fxtwitter Pattern — Fetching X/Twitter Content Safely

**Why this pattern exists | How to use it | Error handling | Examples**

---

## Problem: Why Direct x.com Fetch Fails

### The Technical Issues

1. **JavaScript Rendering:** Twitter/X renders content dynamically via JavaScript. Raw HTTP GET returns an empty HTML shell with no content.
   ```html
   <!-- What you get from direct x.com fetch -->
   <html><body><!-- JS app loads here --></body></html>
   ```

2. **Rate Limiting:** Direct requests to x.com trigger aggressive rate limits (429 Too Many Requests) after a few attempts.

3. **Authentication:** Full content (metrics, replies, sensitive tweets) requires authentication. Direct fetches often hit paywalls or auth walls.

4. **Bot Detection:** X actively blocks requests that look like bots. User-Agent headers, cookie handling, etc. are quickly exhausted.

### Why x.com Blocks You

From X's perspective:
- Uncontrolled scraping damages engagement metrics
- Bots farm data for training
- Ad impressions are lost
- Legal liability (terms of service violations)

X wants developers to use the official API (paid) or accept that casual fetching won't work.

---

## Solution: fxtwitter API Proxy

**fxtwitter** (https://github.com/FixTweet/FxTwitter) is a free, open-source API wrapper that:

- ✅ Renders pages server-side (handles JavaScript)
- ✅ Returns clean JSON with full content
- ✅ No authentication required
- ✅ Optimized for bots/agents (low latency)
- ✅ Respects X's rate limits globally
- ✅ Apache 2.0 licensed, community-maintained

**Public instance:** https://api.fxtwitter.com

---

## The Pattern: How to Use It

### Step 1: Extract Username and Tweet ID from x.com URL

Given an x.com or twitter.com URL:
```
https://x.com/example/status/1234567890
https://twitter.com/example/status/1234567890
```

Extract two parts:
- **username:** `example` (the part after /)
- **tweet_id:** `1234567890` (the part after /status/)

### Step 2: Construct fxtwitter URL

```
https://api.fxtwitter.com/{username}/status/{tweet_id}
```

Example:
```
https://api.fxtwitter.com/example/status/1234567890
```

### Step 3: Fetch and Parse JSON

Use your agent's HTTP client to fetch. Most agents have `web_fetch` or similar:

```javascript
// Pseudo-code
const response = await web_fetch("https://api.fxtwitter.com/example/status/1234567890");
const data = JSON.parse(response);
```

### Step 4: Extract Fields of Interest

fxtwitter returns a JSON object with these top-level fields:

```json
{
  "code": 200,
  "message": "OK",
  "tweet": {
    "url": "https://x.com/...",
    "id": "1234567890",
    "text": "Tweet content here",
    "author": {
      "id": "...",
      "name": "Example Name",
      "screen_name": "example",
      "avatar": "https://..."
    },
    "metrics": {
      "likes": 123,
      "retweets": 45,
      "replies": 12,
      "bookmarks": 8
    },
    "created_at": "2026-03-13T10:30:00Z",
    "media": [
      { "type": "photo", "url": "https://..." },
      { "type": "video", "url": "https://..." }
    ],
    "quoted": null,
    "reply_to": {
      "id": "...",
      "text": "Parent tweet..."
    }
  }
}
```

**Key fields:**
- `tweet.text` — Full tweet content
- `tweet.author` — Author name, handle, avatar
- `tweet.metrics` — Likes, retweets, replies, bookmarks
- `tweet.media` — Images, videos, GIFs
- `tweet.reply_to` — If this is a reply, the parent tweet
- `tweet.quoted` — If this is a quote tweet, the quoted tweet

---

## Example: Reading a Tweet

### Input
```
User: Read this tweet for me
https://x.com/example/status/1234567890
```

### Process
1. Extract: `username=example`, `tweet_id=1234567890`
2. Construct: `https://api.fxtwitter.com/example/status/1234567890`
3. Fetch and parse JSON
4. Extract fields

### Output
```
Tweet by @example:
"This is the tweet content. With multiple sentences. And maybe a link."

Metrics: 123 likes, 45 retweets, 12 replies

Posted: March 13, 2026 at 10:30 AM

Media: [1 photo attached]
```

---

## Error Handling

### 404: Tweet Not Found

**Status:** `"code": 404`  
**Reasons:**
- Tweet was deleted
- Tweet ID is wrong
- Tweet is from a protected account
- URL is malformed

**How to handle:**
```javascript
if (data.code === 404) {
  console.log("Tweet not found or deleted. URL might be wrong.");
}
```

### 429: Rate Limit Hit

**Status:** `"code": 429`  
**Reason:** fxtwitter's global rate limit is exhausted

**How to handle:**
```javascript
if (data.code === 429) {
  console.log("Rate limited. Wait 15–30 seconds and retry.");
  // Implement exponential backoff
}
```

### 500: Service Unavailable

**Status:** `"code": 500`  
**Reason:** fxtwitter server is down

**How to handle:**
```javascript
if (data.code === 500) {
  console.log("fxtwitter is down. Check https://status.fxtwitter.com");
  // Retry in 1–5 minutes
}
```

### 403: Protected/Private Account

**Status:** `"code": 403`  
**Reason:** Tweet is from a protected account you don't follow

**How to handle:**
```javascript
if (data.code === 403) {
  console.log("This account is private. You may not have access.");
}
```

### Malformed URL or Missing Fields

**Status:** HTTP 400 or missing `tweet` field  
**Reason:** URL is malformed or doesn't contain a valid x.com path

**How to handle:**
- Validate the x.com URL before constructing fxtwitter URL
- Check that URL contains `/status/` and a numeric ID
- Extract and validate the tweet ID (must be 10–20 digits)

---

## Best Practices

### 1. Always Validate Input URL

```javascript
const urlRegex = /x\.com|twitter\.com/;
if (!urlRegex.test(inputUrl)) {
  console.log("Not an x.com or twitter.com URL");
  return;
}
```

### 2. Extract Carefully

Use regex to extract username and ID:

```javascript
const match = /(?:x\.com|twitter\.com)\/(\w+)\/status\/(\d+)/.exec(url);
if (!match) {
  console.log("Could not extract username/ID");
  return;
}
const [, username, tweetId] = match;
```

### 3. Cache Results

fxtwitter's API is free. Be respectful — don't refetch the same tweet repeatedly.

```javascript
const cache = {};
if (cache[tweetId]) {
  return cache[tweetId]; // Return cached
}
const data = await web_fetch(`https://api.fxtwitter.com/${username}/status/${tweetId}`);
cache[tweetId] = data;
return data;
```

### 4. Handle Network Errors

```javascript
try {
  const response = await web_fetch(fxtwitterUrl);
  // Parse and return
} catch (error) {
  console.log("Network error fetching from fxtwitter:", error.message);
  // Retry or fail gracefully
}
```

### 5. Respect Rate Limits

If you get a 429, backoff exponentially. Don't spam retries.

```javascript
let retries = 0;
while (retries < 3) {
  const response = await web_fetch(fxtwitterUrl);
  if (response.code === 429) {
    const wait = Math.pow(2, retries) * 1000; // Exponential backoff
    await sleep(wait);
    retries++;
  } else {
    return response;
  }
}
```

---

## When NOT to Use fxtwitter

- **DMs:** fxtwitter doesn't fetch DM content
- **User data:** For user lists, followers, etc., use the official X API or x-research-skill
- **Real-time feeds:** For live feed operations, use xurl or official API
- **Private tweets:** Protected accounts' tweets are not accessible

For these, use `x-research-skill` or the official X API v2.

---

## Alternatives

If fxtwitter is down, these alternatives work temporarily:

| Tool | Pros | Cons |
|------|------|------|
| **nitter.net** | Another open-source proxy | May be rate-limited; different API format |
| **Official X API v2** | Official; rate limits are generous | Requires OAuth; paid for high volume |
| **x-research-skill** | Built for agents; full context | Slower; uses token budget |

---

## fxtwitter Links

- **GitHub:** https://github.com/FixTweet/FxTwitter
- **Public API:** https://api.fxtwitter.com
- **Status Page:** https://status.fxtwitter.com
- **Issues/Updates:** https://github.com/FixTweet/FxTwitter/issues

---

## Summary

**The rule:** Never fetch x.com directly. Always use:
```
https://api.fxtwitter.com/{username}/status/{tweet_id}
```

**Extract from:** `https://x.com/{username}/status/{tweet_id}`

**No auth needed.** Returns clean JSON. Optimized for bots.

**Errors are normal.** Handle 404 (deleted), 429 (rate limit), 500 (server down) gracefully.

---

*This pattern is maintained as part of the x-master skill. Update this file if fxtwitter's API changes.*
