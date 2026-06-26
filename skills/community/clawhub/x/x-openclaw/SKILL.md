---
name: xclaw
description: Extract posts from X (Twitter) timeline or profile pages with engagement metrics, media URLs, and download local copies. Use when asked to scrape, list, or analyze X posts from home timeline, user profiles, or search results without clicking into individual posts.
---

# XCLAW

Extract posts from X (Twitter) pages with full metadata including text, author, timestamp, engagement metrics, media URLs, and download local copies.

## When to Use

- List recent posts from a user's profile
- Extract posts from home timeline
- Capture post URLs without navigating into individual posts
- Gather engagement metrics (likes, reposts, replies, views)
- Download images and video thumbnails
- Analyze content patterns across multiple posts

---

## File Structure

```
intel/x/
├── {date}-{time}-X.md      # Intel file
└── media/
    └── {YYYYMMDD}-{HHMMSS}/        # Media folder (same timestamp)
        ├── image_{postId}_{index}.jpg
        └── video_{postId}_poster.jpg
```

---

## File Naming

| Item | Format | Example |
|------|--------|---------|
| Intel file | `{date}-{time}-X.md` | `2026-03-16-143052-X.md` |
| Media folder | `{YYYYMMDD}-{HHMMSS}` | `20260316-143052` |
| Image | `image_{postId}_{index}.jpg` | `image_2032741269689213289_0.jpg` |
| Video thumbnail | `video_{postId}_poster.jpg` | `video_2032741269689213289_poster.jpg` |

---

## OUTPUT FORMAT — EXACT FORMAT REQUIRED

WRITE THE INTEL FILE IN THIS EXACT FORMAT. FOLLOW EVERY COMPONENT PRECISELY.

```
# X Intelligence Report

**Scraped:** {date} {time} (Asia/Shanghai)
**Source:** X Home Timeline
**Posts Collected:** {count}

---

## Post {n}: {Topic Title}

**Author:** {Name} (@{handle})
**Posted:** {relative time}
**URL:** {post_url}

**Content:**
{post_text_content}

**Metrics:** ❤️ {likes} 🔁 {reposts} 💬 {replies} 👁 {views}

**Media:**
🖼️ media/{folder}/image_{postId}_{index}.jpg

**Signal:** {🔴 HIGH / 🟡 MEDIUM / 🟡 LOW / ⚪ SKIP} — {Brief signal assessment}

---

## Post {n+1}: ...

(MORE POSTS...)

---

## Summary

**High Signal (Tier 1):**
1. {Topic} — {One-line summary}
2. {Topic} — {One-line summary}

**Medium Signal (Tier 2):**
- {Topic} — {One-line summary}
- {Topic} — {One-line summary}

**Skip:**
- {Topic} — {Reason}
```

### Media in Output Format (Conditional)

IF THE POST HAS MEDIA, INCLUDE THE MEDIA LINE AFTER METRICS:

```
**Media:**
🖼️ media/{folder}/image_{postId}_{index}.jpg
```

OR FOR VIDEO THUMBNAILS:

```
**Media:**
🎬 media/{folder}/video_{postId}_poster.jpg
```

IF THE POST HAS NO MEDIA, OMIT THE MEDIA SECTION ENTIRELY.

---

## WORKFLOW

### Step 1: Create Media Folder FIRST

BEFORE EXTRACTING ANY POSTS, create the media folder:

```bash
# Create folder with current timestamp
# Format: YYYYMMDD-HHMMSS
mkdir -p ../../intel/x/media/{YYYYMMDD}-{HHMMSS}

# Example
mkdir -p ../../intel/x/media/20260316-143052
```

### Step 2: Navigate to Target Page

```javascript
// For home timeline
browser.navigate({ url: "https://x.com/home" })

// For a specific user profile
browser.navigate({ url: "https://x.com/username" })
```

### Step 3: Scroll to Load More Posts

```javascript
browser.act({ 
  fn: "() => { for(let i=0; i<3; i++) { window.scrollBy(0, window.innerHeight); } return 'scrolled'; }",
  kind: "evaluate"
})
```

### Step 4: Extract Posts with Media URLs

```javascript
browser.act({
  fn: "() => {
    const articles = document.querySelectorAll('article[data-testid=\"tweet\"]');
    const posts = [];
    articles.forEach(article => {
      const url = article.querySelector('a[href*=\"/status/\"]')?.href;
      if (!url || url.includes('/analytics') || url.includes('/photo')) return;
      
      const text = article.querySelector('[data-testid=\"tweetText\"]')?.innerText || '';
      const timeEl = article.querySelector('time');
      const timestamp = timeEl?.innerText || '';
      const datetime = timeEl?.dateTime || '';
      
      // Get author info
      const nameEl = article.querySelector('[data-testid=\"User-Name\"]');
      const name = nameEl?.querySelector('span')?.innerText || '';
      const handle = nameEl?.querySelector('a[href*=\"/\"]')?.innerText || '';
      
      // Get engagement metrics
      const metricButtons = article.querySelectorAll('button[role=\"button\"]');
      let replies = '0', reposts = '0', likes = '0', views = '0';
      
      metricButtons.forEach(btn => {
        const txt = btn.innerText || '';
        const label = btn.getAttribute('aria-label') || '';
        if (label && label.includes('Reply')) {
          const match = txt.match(/(\d+)/);
          if (match) replies = match[1];
        }
        if (label && label.includes('Repost')) {
          const match = txt.match(/(\d+)/);
          if (match) reposts = match[1];
        }
        if (label && label.includes('Like')) {
          const match = txt.match(/(\d+)/);
          if (match) likes = match[1];
        }
      });
      
      // Views are in an <a> link (not button), e.g. <a href="/.../analytics">71K</a>
      const viewLink = article.querySelector('a[href*=\"/analytics\"]');
      if (viewLink) {
        const v = viewLink.innerText.trim();
        views = v.replace(/[^0-9KMB.]/g, '') || '0';
      }
      
      // Get media URLs - images and video thumbnails
      const mediaUrls = [];
      
      // Image posts: pbs.twimg.com/media/
      const images = article.querySelectorAll('img[src*=\"pbs.twimg.com/media/\"]');
      images.forEach(img => {
        if (img.src && !mediaUrls.includes(img.src)) {
          mediaUrls.push(img.src);
        }
      });
      
      // Also check for image links in <a> tags
      const imageLinks = article.querySelectorAll('a[href*=\"pbs.twimg.com/media/\"]');
      imageLinks.forEach(link => {
        if (link.href && !mediaUrls.includes(link.href)) {
          mediaUrls.push(link.href);
        }
      });
      
      // Video thumbnails: pbs.twimg.com/amplify_video_thumb/
      const videoThumbs = article.querySelectorAll('img[src*=\"pbs.twimg.com/amplify_video_thumb/\"]');
      videoThumbs.forEach(img => {
        if (img.src && !mediaUrls.includes(img.src)) {
          mediaUrls.push(img.src);
        }
      });
      
      const postId = url.match(/\/status\/(\d+)/)?.[1] || '';
      
      posts.push({ 
        name,
        handle,
        text: text.substring(0, 500),
        timestamp, 
        datetime,
        url,
        postId,
        mediaUrls,
        metrics: { replies, reposts, likes, views }
      });
    });
    return posts.slice(0, 10);
  }",
  kind: "evaluate"
})
```

### Step 5: Download Media Files

FOR EACH POST WITH MEDIA, DOWNLOAD THE FILES:

```bash
# Download image - replace URL with actual media URL from extraction
curl -L -o "../../intel/x/media/{folder}/image_{postId}_{index}.jpg" "https://pbs.twimg.com/media/xxx?format=jpg&name=large"

# Download video thumbnail
curl -L -o "../../intel/x/media/{folder}/video_{postId}_poster.jpg" "https://pbs.twimg.com/amplify_video_thumb/xxx"
```

IMPORTANT: 
- USE `-L` FLAG TO FOLLOW REDIRECTS
- ADD `&name=large` FOR FULL-RESOLUTION IMAGES
- USE THE ACTUAL URLS EXTRACTED FROM STEP 4

### Step 6: Write Intel File

WRITE THE MARKDOWN FILE TO `../../intel/x/{date}-{time}-X.md`

FOLLOW THE EXACT OUTPUT FORMAT SHOWN ABOVE. INCLUDE:
- Header with Scraped, Source, Posts Collected
- Each post with Author, Posted, URL, Content, Signal
- Media references if present
- Summary section at the end

### Step 7: Close Chrome Tab

```javascript
browser.close()
```

---

## Key Selectors

| Element | Selector |
|---------|----------|
| Article container | `article[data-testid="tweet"]` |
| Post text | `[data-testid=\"tweetText\"]` |
| Timestamp | `time` |
| User name | `[data-testid=\"User-Name\"]` |
| Post URL | `a[href*=\"/status/\"]` |
| Analytics link (views) | `a[href*=\"/analytics\"]` |
| Metric buttons | `button[role=\"button\"]` |
| Images | `img[src*=\"pbs.twimg.com/media/\"]` |
| Video thumbnails | `img[src*=\"pbs.twimg.com/amplify_video_thumb/\"]` |

---

## Tips

1. **Don't click into posts** - Extract URLs directly from the timeline
2. **Filter URLs** - Exclude `/analytics` and `/photo` URLs
3. **Scroll before extracting** - X loads posts dynamically
4. **Create folder FIRST** - Media folder must exist before downloads
5. **Use -L flag** - curl must follow redirects for pbs.twimg.com URLs
6. **Add &name=large** - Get full-resolution images, not thumbnails
7. **Always close the tab** - Task ends when tab closes
