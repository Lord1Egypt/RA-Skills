# Keyword research tools playbook

## Contents
1. Free tools
2. Paid tools
3. Recommended stacks
4. Common issues

---

## 1. Free tools

### Google Search Console (GSC)
- **URL**: https://search.google.com/search-console/
- **Requires**: Google account with verified site ownership
- **Main use**: Queries the site already shows for, CTR, average position
- **Flow**: Performance → Search results → set date range → sort by Query
- **Export**: Download icon (top right) → CSV
- **Limitation**: Only queries where the site already appeared in SERPs; fully uncovered queries do not appear

### Google Keyword Planner (GKP)
- **URL**: https://ads.google.com/home/tools/keyword-planner/
- **Requires**: Google Ads account (free signup; no need to run ads)
- **Main use**: Volume bands, related terms, geo/language data
- **Flow**: Discover new keywords → enter seeds or site URL → pick country/language
- **Limitation**: Volume shown as ranges (e.g. 1K–10K), not exact; “competition” is Ads competition, not SEO difficulty
- **Login**: If not signed into Ads, data is fuzzier—have the user sign into their Google Ads account

### Google Trends
- **URL**: https://trends.google.com/
- **Requires**: None (public)
- **Main use**: Relative interest between terms, seasonality, regional interest
- **How**: Enter terms → pick region and time range → compare up to 5 terms
- **Limitation**: No absolute search volume—relative index only

### Google Autocomplete (Search Suggest)
- **URL**: https://www.google.com/ (use the search box)
- **Requires**: None
- **Main use**: Real user search patterns, long-tail variants
- **Tips**:
  - Add a space after the term to trigger suffix suggestions
  - Prefix with letters: `a [term]`, `b [term]` … `z [term]`
  - Underscore mid-phrase for infix suggestions: `maid _ singapore`
  - Use Incognito to reduce personalization from history

### AnswerThePublic
- **URL**: https://answerthepublic.com
- **Requires**: Free account (3 searches/day)
- **Main use**: Visual maps of question-, preposition-, and comparison-style keywords
- **How**: Enter a core term → language/country → download CSV or screenshot
- **Most useful output**: Questions (Who/What/When/Where/Why/How) → FAQ ideation
- **Over limit**: Wait 24h for reset, or paid plan (~$99/mo)

### AlsoAsked
- **URL**: https://alsoasked.com
- **Requires**: Free tier (3 runs/month—not per day)
- **Main use**: Full tree expansion of Google People Also Ask
- **How**: Enter term → language/country → view PAA tree
- **Why it matters**: These are questions Google treats as follow-ups—good SERP-feature targets
- **Over limit**: Free quota is tight—use on your strongest seed terms first

### Ahrefs free keyword tool
- **URL**: https://ahrefs.com/keyword-generator
- **Requires**: None (public, no signup)
- **Main use**: From a seed, ~100 related terms + KD estimate + monthly volume estimate
- **Limitation**: 100 terms per run, no export, no competitor gap

### Semrush free account
- **URL**: https://www.semrush.com/features/keyword-magic-tool/
- **Requires**: Free registered account
- **Quota**: 10 keyword queries per day
- **Main use**: Volume, KD, SERP features, basic competitor comparison
- **How**: Keyword Magic Tool → enter term → country → filter by difficulty

### Bing Webmaster Tools
- **URL**: https://www.bing.com/webmasters/
- **Requires**: Microsoft account + verified site
- **Main use**: Bing query data + AI Copilot grounding query reports
- **Extra value**: Bing AI Performance shows keywords used when Copilot retrieves your content—a distinct GEO/AEO signal

---

## 2. Paid tools

### Ahrefs
- **Pricing**: Lite $129/mo, Standard $249/mo
- **URL**: https://ahrefs.com
- **Strengths**: Strongest backlink index; large keyword DB; deepest Site Explorer competitor workflows
- **Key features**:
  - Site Explorer: competitor domain → Organic Keywords → full ranking list
  - Content Gap: competitors vs your site → terms they have and you lack
  - Keywords Explorer: multi-angle analysis, SERP history, CTR estimates
  - Rank Tracker: track positions for chosen terms

### Semrush
- **Pricing**: Pro $139.95/mo, Guru $249.95/mo
- **URL**: https://www.semrush.com
- **Strengths**: Broadest toolkit (40+ tools); strong local SEO; unique paid-search keyword data
- **Key features**:
  - Keyword Magic Tool: strongest expansion workflow
  - Keyword Gap: competitor gap analysis
  - Position Tracking: rank monitoring
  - Local SEO: good for local services

### Moz Pro
- **Pricing**: Starter $49/mo, Standard $99/mo
- **URL**: https://moz.com/pro
- **Strengths**: Domain Authority (DA) is an industry reference; friendly UI; good for beginners
- **Key features**: Keyword Explorer, Rank Tracker, On-Page Grader

### KWFinder (Mangools)
- **Pricing**: Basic $29/mo (annual), Premium $44/mo
- **URL**: https://kwfinder.com
- **Strengths**: Good value; focused on keyword research; simple UI; small teams
- **Key features**: Clear KD scores, SERP analysis, autocomplete mining

### Ubersuggest (Neil Patel)
- **Pricing**: Individual $29/mo, Business $49/mo
- **URL**: https://neilpatel.com/ubersuggest/
- **Strengths**: Low price; basics covered; actively updated
- **Limitation**: Weaker accuracy vs Ahrefs/Semrush; shallow competitor analysis

### Surfer SEO
- **Pricing**: Essential $99/mo, Scale $219/mo
- **URL**: https://surferseo.com
- **Strengths**: Clustering (Keyword Surfer), content scores, Topic Map for architecture
- **Best for**: Systematic cluster planning; more content optimization than raw discovery

### LowFruits
- **Pricing**: $29.90/mo (pay-as-you-go also available)
- **URL**: https://lowfruits.io
- **Strengths**: Low-competition terms with real volume; good for new sites finding wedge keywords
- **Best for**: Tight budget, new sites that need rankable terms quickly

---

## 3. Recommended stacks

### Zero-budget stack
```
GSC (existing queries) + GKP (volume sanity) + Google Autocomplete (long-tail)
+ AnswerThePublic (FAQ angles) + Ahrefs free tool (competitor preview)
```
Coverage: broad, but limited depth on competitor analysis.

### Small budget ($30–50/mo)
```
GSC + KWFinder ($29/mo) or Ubersuggest ($29/mo)
```
Adds clearer KD and basic competitor keyword views.

### Standard ($100–130/mo)
```
GSC + Ahrefs Lite ($129/mo)
```
Full competitor workflows, Content Gap, backlink context.

### Full-feature ($140+/mo)
```
GSC + Semrush Pro ($139.95/mo)
```
Widest coverage: local SEO, Ads keyword data, full competitor suite.

---

## 4. Common issues

### GSC login wall
- User must be signed into Google in Chrome with an account that has verified ownership in GSC.
- Verification methods: HTML file upload, DNS TXT, Google Analytics linking (common).
- Suggested script: “Open https://search.google.com/search-console in Chrome, confirm you see your property’s data, then tell me when you’re ready.”

### Google Ads account for GKP
- GKP needs a Google Ads account; running ads is not required.
- Signup may ask for billing details—user can complete setup without launching campaigns.
- Fallback: Ahrefs free keyword tool or Semrush free tier.

### Quota exhausted (AnswerThePublic / AlsoAsked)
- AnswerThePublic free: 3/day—resume tomorrow or mine manually with Autocomplete.
- AlsoAsked: 3/month—reserve for core seeds; for others, inspect PAA manually in Google.

### No paid-tool account
1. Finish baseline analysis with free tools.
2. List “what a paid tool would confirm next” for the user.
3. Point to trials (Ahrefs ~7 days, Semrush ~7 days).

### Numbers disagree across tools
- Normal—different data sources and models.
- Rule of thumb: treat GKP as a Google-native volume reference; use Ahrefs/Semrush for KD and competitor lists.
- Prioritize relative ranking (which terms look stronger) over chasing exact counts.

### Personalized SERP noise
- Use Incognito for Google SERP checks to reduce history/login skew.
- For a specific region, use URL params like `&gl=sg&hl=en` or a VPN.
