## XIV. SEO Case Studies

> Based on 6 case study articles (2024-2026)

### 14.1 StickerBaker Review Points

**Website Info**: AI sticker generation website (stickerbaker.com)

**What's Done Well**:
- Homepage core area directly shows tool entry, improving dwell time
- Latest works list on homepage updates frequently, attracting crawlers
- Sticker detail pages can be indexed, capturing long-tail keyword traffic
- Similar stickers module improves keyword density

**Areas for Improvement**:
- Title only uses 12 characters, wasting 60-character limit
- Inconsistent H tag usage (homepage has two H1s)
- Search results page uses client-side rendering (crawlers can't capture dynamic content)
- URLs use pure numeric IDs, easily scraped
- Missing canonical tags
  - Source: "SEO Review Report for AI Sticker Generator StickerBaker"

**Improvement Suggestions**:
- Change URL to `/sticker/29961-fairy-unicorn` format
- Switch search results page to server-side rendering
- Add discovery pages for crawlers to index all stickers
- Add topic pages to aggregate related stickers
  - Source: "SEO Review Report for AI Sticker Generator StickerBaker"

### 14.2 SEO Failure Case Lessons

**Case**: ChatGPT4o.ai wrapper site

**Failure Reasons**:
- After release, homepage accidentally output full Q&A text
- Homepage word count jumped from 400 to 2000-3000
- Core keyword density plummeted
- Google's semantic analysis determined page content was chaotic
- Result: Impressions crashed, rankings dropped, clicks went to zero

**Lessons**:
- Keyword density is important
- Page content should be topic-focused
- Check SEO-related metrics before release
  - Source: "A Real SEO Failure Case"

### 14.3 CNN Election SEO Strategy

**Background**: CNN dominated search rankings during 2024 US election

**Core Strategy**:
1. **Publish new URL daily**: Stay in Google Top Stories
2. **Include dates in URLs**: Signal freshness (e.g., 10-15-24)
3. **Use LiveBlogPosting Schema**: Tell Google content updates in real-time
4. **40-50 content updates daily**: Refresh with timestamps
5. **High-quality relevant images**: Clear candidate headshots improve CTR
6. **Homepage links to important content**: Ensure quick crawling and indexing

**Insights**:
- Even major sites prioritize SEO
- Freshness signals are important for hot topic rankings
  - Source: "How CNN Dominated 2024 US Election-Related Searches"

### 14.4 AISEO Effect Verification

**Case**: An SEO blogger was mistakenly reported by media as a "well-known AI overseas self-media blogger"

**Discovery**:
- Authoritative media information directly affects AI answers
- Perplexity, Gemini, DeepSeek and other connected AIs base answers on search results
- Claude, ChatGPT and other non-connected AIs haven't been "contaminated" yet

**AISEO Strategy Verification**:
- High-authority site information is trusted by AI
- Conclusive, definitive statements are more easily believed by AI
- The more certain the tone, the more AI believes it
  - Source: "Made News Overnight to Test AISEO; Perfect for Testing AISEO Effect"

### 14.5 Pixverse SEO Review

**Website Info**: AI video generation website, 62.36 million annual visits

**Core Problem**: 24.1 million search traffic is almost entirely brand keywords, no SEO done

**Specific Issues**:
1. Main domain redirects to app subdomain
2. Pure client-side rendering (body only has a few lines of code)
3. Multi-language switching via JS, URL unchanged
4. Title only shows brand name, no business keywords
5. Incorrect canonical causing duplicate pages
6. Entire page has no headings

**Improvement Suggestions**:
- Switch to server-side rendering
- Use URL parameters for multi-language (?lang=ko)
- Add "AI Video Generator" to title
- Add introduction div below root div with text and images
- Set correct canonical and hreflang
  - Source: "SEO Review: Pixverse with 62.36 Million Annual Visits"

**Key Insight**:
> When brand is strong enough, you get brand keyword traffic even without SEO
> But this means giving up massive non-brand keyword traffic

### 14.6 Raphael AI Brand Keyword Hijacking Case (Deep Analysis)

**Background**: raphael.app had its brand keywords hijacked by raphaelai.org (impostor)

**Timeline**:
- January 2025: raphael.app launched, 1 million visits next month
- February 2025: Impostor site raphaelai.org launched
- March-June 2025: Impostor took #1 ranking for "raphael ai"
- July-October 2025: Impostor traffic surpassed the original
- October 2025: Turning point, original's DR rose from 47 to 48
- November 2025-January 2026: Original reclaimed brand keyword, monthly visits exceeded 2 million

**Impostor's Tactics**:
1. Exact match domain (raphaelai.org contains "raphael ai")
2. Structured data declaring sitename as "Raphael AI"
3. YouTube influencer marketing causing confusion
4. Fake app download pages to occupy search spots
5. Copied original's homepage copy for descriptions

**How Google Determines Brand Entity Ownership**:
1. **Exact Match Domain (EMD)**: Domain containing brand name
2. **Structured Data Markup**: sitename and organization declarations
3. **Page Context**: Title, H1, body keyword density

**How the Original Recovered**:
- Dofollow backlink from Hong Kong Metropolitan University's .edu domain
- .edu/.gov domains have extremely high trust authority
- DR rising from 47 to 48 triggered Google's "anti-EMD fraud" logic
- Google NavBoost data (real user search experience) proved original was more popular

**Replicable Strategies**:
- Websites must declare sitename structured data
- Seek .edu/.gov high-authority domain backlinks
- Continuously build great products for organic user sharing
- User dwell time is an important experience signal
- Brand building should be transparent, don't fear being associated

**Core Lesson**:
> "Good products spread themselves"
> Backlinks are the ignition point, but product strength is the moat
> Even if endorsement links break, user voting data protects the true king
  - Source: "Deep Dive SEO Data: How Raphael AI Achieved Counter-Growth"

---
