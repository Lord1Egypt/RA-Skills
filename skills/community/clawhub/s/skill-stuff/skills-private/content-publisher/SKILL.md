---
name: content-publisher
description: Deploys approved content to Substack, LinkedIn, Twitter, Instagram, and Reddit via headless browser. Use when a user has approved content from thought-leader and wants it posted across platforms without manually logging in to each one.
license: MIT
compatibility: Requires lobstrkit with Exine browser (user Chrome session). LinkedIn/Reddit/Instagram/Twitter posting uses the user's own authenticated Chrome session on their own device.
allowed-tools: browser
metadata:
  openclaw.emoji: "🚀"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "publishing,deployment,substack,linkedin,twitter,instagram,reddit,automation"
  openclaw.triggers: "publish this,post this,deploy content,publish to all platforms,schedule post,go live"
  openclaw.requires: '{"config": ["channels"]}'
  openclaw.homepage: https://clawhub.com/skills/content-publisher


# Content Publisher

Takes approved content from thought-leader and gets it live.
Handles the platform UI so you don't have to.

---

## File structure

```
content-publisher/
  SKILL.md
  config.md          ← platform credentials, settings, auto-post preferences
  log.md             ← deployment log: what was posted, where, when, confirmation
  queue.md           ← approved pieces waiting to deploy
```

---

## How it works

The browser tool navigates each platform's interface exactly as a user would.
No official API required. The headless browser emulates the posting flow.

This means:
- It works even when platforms don't have public APIs (Reddit, Instagram)
- It can handle multi-step posting flows (Substack draft → publish)
- It uploads images exactly as a user would drag and drop
- It gets the same confirmation the user would see

---

## Browser routing — critical

LinkedIn, Reddit, Instagram, and Twitter/X ALWAYS use lobstrkit Exine
(the user's local Chrome session). NEVER route these through parav cloud browser.

Reason: These platforms have aggressive bot detection. parav-stealth running on
a cloud VPS will eventually be detected. Lobstrkit Exine sits on the user's
real Chrome session on their own device — indistinguishable from manual use.

```
Lobstrkit Exine (user Chrome):  LinkedIn, Reddit, Instagram, Twitter/X
Lobstrkit Composio:             Substack (if API available), email newsletters
Parav DAG:                      Never for authenticated social posting
```

The content-publisher skill checks which MCP provider handles each platform
before dispatching. If lobstrkit is not running, social posting is blocked
with an explanation — not silently routed to parav.

---

## Platform publishing flows

### Substack

**Authentication:** Stored session cookie or email/password in config.md (encrypted via OpenClaw secrets).

**Posting flow:**
1. Navigate to Substack dashboard → New Post
2. Set title from approved draft
3. Paste body content (formatted markdown → Substack rich text)
4. Upload OG image (header image)
5. Set subtitle if provided
6. Preview — take screenshot, present to user if not auto-post
7. Publish (or Save as Draft if user prefers to publish manually from Substack)

**Substack-specific:**
- Supports scheduling: "Publish now" or "Schedule for [DATE TIME]"
- Supports "Publish to everyone" vs "Paid subscribers only"
- Captures: post URL, subscriber count at time of publish

**Confirmation logged:**
```
Published: Substack
Title: [title]
URL: [post URL]
Published at: [timestamp]
Subscribers at publish: [N]
```

---

### LinkedIn

**Authentication:** Stored session or OAuth token.

**Posting flow:**
1. Navigate to LinkedIn → Start a post
2. Paste approved content
3. Upload image if provided
4. Check hashtag limit (max 3, skill enforces)
5. Preview
6. Post

**LinkedIn-specific:**
- No scheduling via UI without Premium — if user has Premium, scheduling is supported
- Detects if post is from personal profile or company page (config.md)
- Captures: post URL, initial impression count (checked 1h after posting)

**Confirmation logged:**
```
Published: LinkedIn
URL: [post URL]
Posted at: [timestamp]
Profile: [personal / company page name]
```

---

### Twitter/X

**Authentication:** Stored session or OAuth.

**Single tweet posting flow:**
1. Navigate to Twitter/X → Compose
2. Paste tweet text
3. Upload image if provided
4. Check character count (enforced before this step)
5. Post

**Thread posting flow:**
1. Compose first tweet
2. Click "+" to add next tweet in thread
3. Repeat for each tweet in thread
4. Post all at once

**Twitter-specific:**
- Handles threads up to 25 tweets
- Supports image per tweet (up to 4 images per tweet)
- Detects if posting to personal account or via organisation account
- Captures: tweet URL, initial impression count

**Confirmation logged:**
```
Published: Twitter/X
URL: [tweet URL or thread URL]
Posted at: [timestamp]
Type: [single / thread of N]
```

---

### Instagram

**Authentication:** Stored session.

**Single post flow:**
1. Navigate to Instagram web or use mobile node if available
2. Create new post
3. Upload image (required — Instagram requires an image)
4. Paste caption
5. Add location if relevant (config.md setting)
6. Post

**Carousel flow:**
1. Upload multiple images in sequence
2. Caption applies to the set
3. Post

**Instagram-specific:**
- Web posting is more limited than app — mobile node preferred if available
- Reels require video — this skill handles images only; video content is out of scope for v1
- Story posting: supported for single images
- Hashtags: added at end of caption if user has a hashtag set configured

**Confirmation logged:**
```
Published: Instagram
Type: [single / carousel of N / story]
Posted at: [timestamp]
```

---

### Reddit

**Authentication:** Stored session or username/password (encrypted).

**Reddit posting is the most nuanced.**
Reddit has strong spam detection. The skill takes extra care here.

**Pre-posting check:**
1. Verify the target subreddit is in config.md with confirmed posting permissions
2. Check subreddit rules (web_fetch the rules page)
3. Verify the post type is allowed (link / text / image)
4. Check account karma and age — new accounts can't post everywhere
5. Flag any rule conflicts before attempting to post

**Text post flow:**
1. Navigate to subreddit → Submit
2. Select "Text" post type
3. Set title (critical on Reddit — it's the hook)
4. Paste body content
5. Submit

**Link post flow (for Substack pieces):**
1. Navigate to subreddit → Submit
2. Select "Link" post type
3. Paste Substack URL
4. Set title (different from Substack title — Reddit title is for Reddit)
5. Add first comment with context (optional but effective)
6. Submit

**Reddit-specific caution:**
- Never use the exact same title on Reddit as on other platforms
- Reddit titles should be written for that community, not repurposed from elsewhere
- First comment can add nuance or invite discussion — use it
- Don't post the same content to multiple subreddits simultaneously (karma farming detection)

**Confirmation logged:**
```
Published: Reddit
Subreddit: r/[subreddit]
Type: [text / link]
URL: [post URL]
Posted at: [timestamp]
```

---

## Queue management

Approved pieces from thought-leader go into queue.md.

```md
# Publishing Queue

## [PIECE SLUG] — [PIECE TITLE]
Approved: [timestamp]
Platforms approved: [list]
Auto-post: [yes/no per platform]

### Substack
Status: pending / posted / failed
Target time: [now / scheduled]

### LinkedIn
Status: pending / posted / failed
Target time: [now / scheduled]

### Twitter/X
Status: pending / posted / failed

### Instagram
Status: pending / posted / failed

### Reddit
Subreddit: r/[subreddit]
Status: pending / posted / failed
```

---

## Deployment modes

### Immediate deployment (default)
All approved platforms deployed as soon as approved.
30-minute cancel window always available.

### Scheduled deployment
User can specify a time:
`/publish [piece] at [DATE TIME]`
Skill registers a cron job for the scheduled time.
Cancel any time before deployment: `/publish cancel [piece]`

### Staggered deployment
Some users prefer not to post everything at once.
`/publish [piece] stagger [30min / 1h / 2h]`
Posts each platform with the specified gap between them.

---

## Error handling

If a platform deployment fails:

**Retry automatically:** For transient failures (network, timeout).
**Alert and wait:** For auth failures ("your session expired, please re-authenticate").
**Skip and log:** For platform-specific blocks ("this subreddit requires 30 days account age").

All failures logged to log.md with reason.

User is notified of any failure with:
- What failed
- Why (if determinable)
- What to do

---

## Re-authentication flow

When a session expires:
`/publish auth [platform]`

Skill navigates to the platform login page.
User completes authentication in the browser.
Session stored encrypted via OpenClaw secrets.

---

## Management commands

- `/publish [piece]` — deploy approved piece to all approved platforms
- `/publish [piece] [platform]` — deploy to one platform only
- `/publish [piece] at [time]` — schedule deployment
- `/publish queue` — show current queue
- `/publish log` — show deployment log
- `/publish auth [platform]` — re-authenticate a platform
- `/publish cancel [piece]` — cancel pending deployment
- `/publish status [piece]` — check deployment status

---

## config.md structure

```md
# Content Publisher Config

## Platforms

### Substack
auth: session (stored in OpenClaw secrets)
default: publish immediately
allow_scheduling: true

### LinkedIn
auth: session (stored in OpenClaw secrets)
account_type: personal / company page
company_page: [page name if applicable]
default: publish immediately

### Twitter/X
auth: session (stored in OpenClaw secrets)
account: @[handle]
default: publish immediately

### Instagram
auth: session (stored in OpenClaw secrets)
default_hashtags: [hashtag set — optional]
preferred_input: web / mobile node

### Reddit
auth: session (stored in OpenClaw secrets)
username: u/[username]
default_subreddits:
  [topic]: r/[subreddit]
  [topic]: r/[subreddit]
posting_delay: 60min  (minimum time between Reddit posts — spam prevention)

## Global settings
cancel_window: 30min
stagger_default: none
log_retention: 90 days
```

---

## What makes it good

The platform-specific posting flows handle the quirks each platform has.
LinkedIn's character limits are different from Twitter's. Substack has a draft mode.
Reddit titles need to be different from everywhere else.
These aren't edge cases — they're the actual job.

The Reddit extra caution is real.
Reddit's spam detection is aggressive. A flagged post is worse than no post.
The pre-posting check (rules, karma, account age) prevents most failures before they happen.

The 30-minute cancel window is always there.
Mistakes happen. The window means they're recoverable.

The log is the memory.
What was posted, when, what URL, what the initial stats were.
The content-dashboard reads from this log.
