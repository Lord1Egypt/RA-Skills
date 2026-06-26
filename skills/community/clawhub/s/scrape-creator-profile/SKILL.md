---
name: scrape-creator-profile
version: 1.0.0
description: >
  Scrape and extract structured data from creator profiles across platforms
  such as YouTube, Instagram, TikTok, Twitter/X, LinkedIn, Twitch, and
  personal websites. Use this skill whenever the user asks to look up, fetch,
  analyze, or collect data about a content creator, influencer, or public
  profile — even if they don't say "scrape". Triggers: "get info on this
  creator", "pull their profile", "what's their follower count", "scrape
  this creator page", "summarize this influencer", "fetch creator stats",
  "analyze this YouTube channel", "get TikTok profile data".
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - python3
      env: []
    envVars:
      - name: APIFY_API_TOKEN
        required: false
        description: >
          Optional Apify API token for enhanced scraping via Apify Actors.
          Without this, the skill falls back to web_fetch + browser mode.
      - name: CREATOR_SCRAPE_DELAY_MS
        required: false
        description: >
          Milliseconds to wait between requests (default: 1500). Increase if
          hitting rate limits.
    allowed-tools:
      - web_fetch
      - browser
      - bash
      - read
      - write
---

# Scrape Creator Profile

Extract structured profile data from a content creator's public page.
Returns a normalized JSON object regardless of platform.

---

## When to Use This Skill

Use this skill for any request that involves:
- Looking up a creator, influencer, streamer, or public figure's profile
- Fetching follower counts, bio, links, recent content, or engagement stats
- Comparing multiple creators
- Building lead lists or research reports about creators
- Monitoring a creator's stats over time

If the user provides a URL, jump straight to **Step 2**. If they only give a
name or handle, start at **Step 1**.

---

## Step 1 — Resolve the Profile URL

If the user gave a username/handle without a URL:

1. Construct the likely URL using the platform mapping below.
2. If the platform is ambiguous, try the most likely one first (see detection
   hints), then ask the user to confirm.

### Platform URL Patterns

| Platform     | URL Pattern                              | Example                                    |
|--------------|------------------------------------------|--------------------------------------------|
| YouTube      | `https://www.youtube.com/@{handle}`      | `https://www.youtube.com/@mkbhd`           |
| Instagram    | `https://www.instagram.com/{handle}/`    | `https://www.instagram.com/natgeo/`        |
| TikTok       | `https://www.tiktok.com/@{handle}`       | `https://www.tiktok.com/@charlidamelio`    |
| Twitter / X  | `https://x.com/{handle}`                 | `https://x.com/sama`                       |
| LinkedIn     | `https://www.linkedin.com/in/{handle}/`  | `https://www.linkedin.com/in/satyanadella/`|
| Twitch       | `https://www.twitch.tv/{handle}`         | `https://www.twitch.tv/shroud`             |
| Substack     | `https://{handle}.substack.com`          | `https://astralcodexten.substack.com`      |
| GitHub       | `https://github.com/{handle}`            | `https://github.com/torvalds`              |
| Patreon      | `https://www.patreon.com/{handle}`       | `https://www.patreon.com/kurzgesagt`       |

### Detection Hints

- `@` prefix with short handle → likely Twitter/X or Instagram
- "yt:" or "youtube" keyword → YouTube
- "channel", "subscribe", "views" → YouTube
- "stream", "live" → Twitch
- "reel", "story", "ig:" → Instagram
- "tiktok", "tt:" or handle with numbers → TikTok
- Professional title + name → LinkedIn

---

## Step 2 — Fetch the Profile Page

### 2a. Try plain web_fetch first

```
web_fetch(url)
```

Check if the response contains useful profile data (bio, follower count, etc.).
If the content is mostly JS placeholders, empty `<div>`s, or a login wall,
move to **2b**.

### 2b. Use browser (managed mode) for JS-heavy sites

Platforms that almost always require browser mode:
- **Instagram** — always requires browser
- **TikTok** — always requires browser
- **LinkedIn** — login wall without session; use browser if session cookies available
- **YouTube** — web_fetch usually works; use browser if blocked

Browser steps:
1. Open the profile URL in managed browser mode.
2. Wait for the main content container to render (look for follower/subscriber
   counts, bio text).
3. Take a DOM snapshot.
4. Extract data from the snapshot using the field map in Step 3.

### 2c. Apify fallback (if APIFY_API_TOKEN is set)

For persistent blocks, use the Apify actor for that platform. See
`references/apify-actors.md` for actor IDs and call patterns.

---

## Step 3 — Extract Structured Fields

Parse the fetched content and populate the following fields. Mark any missing
field as `null` — do not guess.

```json
{
  "platform": "string",          // youtube | instagram | tiktok | twitter | linkedin | twitch | substack | github | patreon | other
  "handle": "string",            // @-prefixed username
  "display_name": "string",      // Full display name
  "verified": true | false,
  "bio": "string",               // Profile description / about text
  "profile_url": "string",       // Canonical URL used to scrape
  "avatar_url": "string | null",
  "external_links": ["string"],  // Any links in bio or link-in-bio
  "stats": {
    "followers": "number | null",
    "following": "number | null",
    "subscribers": "number | null",
    "total_views": "number | null",
    "total_posts": "number | null",
    "monthly_listeners": "number | null",  // Spotify-style, if applicable
    "engagement_rate": "number | null"     // Percentage, if computable
  },
  "recent_content": [
    {
      "title": "string | null",
      "url": "string",
      "published_at": "ISO 8601 string | null",
      "views": "number | null",
      "likes": "number | null",
      "comments": "number | null"
    }
    // Up to 5 most recent items
  ],
  "contact_info": {
    "email": "string | null",    // Only if publicly listed in bio/links
    "website": "string | null"
  },
  "scraped_at": "ISO 8601 UTC timestamp"
}
```

> **Privacy rule**: Only capture fields that are explicitly public on the
> profile page. Do not infer, deduce, or cross-reference private information.
> Do not store or relay phone numbers even if visible.

### Platform-specific extraction hints

See `references/platform-selectors.md` for CSS selectors and JSON-LD paths
per platform. Quick reference:

- **YouTube**: subscriber count in `#subscriber-count` or meta `itemprop=interactionCount`; description in `#description-inner`
- **Twitter/X**: follower count in `[data-testid="UserProfileHeader_Items"]`; bio in `[data-testid="UserDescription"]`
- **Instagram**: JSON blob in `window._sharedData` or `<script type="application/ld+json">`
- **TikTok**: JSON blob in `<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__">`
- **GitHub**: `itemprop` attributes: `name`, `description`, `follows`, `worksFor`
- **LinkedIn**: Open Graph tags for name, title, headline

---

## Step 4 — Normalize Numbers

Convert abbreviated counts to integers before storing:
- `"12.3K"` → `12300`
- `"4.5M"` → `4500000`
- `"1B"` → `1000000000`
- `"1,234"` → `1234`

Use the helper script:

```bash
python3 ~/.openclaw/workspace/skills/scrape-creator-profile/scripts/normalize_count.py "12.3K"
```

---

## Step 5 — Output

### Default output (conversational)

Present a clean summary in chat:

```
**[Display Name]** (@handle) · Platform
✅ Verified  |  👥 X followers  |  📝 Y posts

Bio: "..."

Top links: url1, url2

Recent content:
  1. "Video Title" — X views (date)
  2. ...

[Full JSON available on request]
```

### Structured output (when user asks for JSON, export, or data)

Return or save the full normalized JSON object from Step 3.

To save to disk:
```bash
python3 ~/.openclaw/workspace/skills/scrape-creator-profile/scripts/save_profile.py \
  --data '<json>' \
  --output ~/creator-profiles/{handle}_{platform}.json
```

---

## Step 6 — Multi-Profile Mode

If the user supplies multiple handles or URLs (comma-separated, line-separated,
or a list):

1. Process each profile sequentially (respect `CREATOR_SCRAPE_DELAY_MS` between
   requests, default 1500 ms).
2. Collect results into an array.
3. Output a comparison table if ≤ 5 profiles; offer to save CSV if > 5.

```bash
python3 ~/.openclaw/workspace/skills/scrape-creator-profile/scripts/compare_profiles.py \
  --profiles '<json array>' \
  --format table   # or csv
```

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Login wall / auth required | Report which fields were blocked; return partial data |
| Rate limited (429) | Wait `CREATOR_SCRAPE_DELAY_MS × 3`, retry once, then report |
| Profile not found (404) | Inform the user; suggest alternate handle spellings |
| JavaScript-only page, no browser | Suggest enabling browser mode in OpenClaw settings |
| Ambiguous handle across platforms | Ask user to confirm platform before scraping |

---

## Legal & Ethical Guardrails

- Only scrape **public** profiles. Do not scrape private accounts even if
  technically accessible.
- Do not extract, store, or relay private contact information (DMs, non-public
  email, phone numbers).
- Respect `robots.txt` disallow rules unless the user explicitly overrides and
  accepts responsibility.
- Do not use this skill to build surveillance systems, stalking tools, or
  targeted harassment infrastructure.
- If the user's intent appears to be harassment or doxxing, refuse and explain why.

---

## Reference Files

- `references/platform-selectors.md` — CSS selectors and JSON-LD paths per platform
- `references/apify-actors.md` — Apify actor IDs and call patterns for fallback scraping
- `scripts/normalize_count.py` — Converts "12.3K" → 12300
- `scripts/save_profile.py` — Saves profile JSON to disk
- `scripts/compare_profiles.py` — Builds comparison table or CSV from multiple profiles
