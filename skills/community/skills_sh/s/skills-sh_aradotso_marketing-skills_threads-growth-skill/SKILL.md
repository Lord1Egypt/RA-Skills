---
name: threads-growth-skill
description: Systematically improve Threads content using real performance data and algorithm-aware drafting
triggers:
  - set up threads growth tracking
  - draft a threads post
  - analyze my threads performance
  - update my threads patterns
  - check my threads insights
  - score this threads draft
  - optimize my threads content
  - run threads algorithm check
---

# Threads Growth Skill

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Data-driven Threads content optimization that learns from your actual post performance. Uses browser automation to scrape Insights, identifies winning patterns, and drafts algorithm-compliant posts with AI-tone detection.

## What this does

- **Performance tracking**: Scrapes your real Threads Insights (views, likes, replies, shares)
- **Pattern detection**: Identifies what works for YOUR account (not generic advice)
- **Smart drafting**: Creates posts using your patterns + algorithm red-line checks + AI-tone detection
- **Automated updates**: Bi-weekly cron keeps your performance database current
- **Share optimization**: Prioritizes DM forwardability (3-5x weight vs likes per Mosseri 2025)

## Installation

```bash
# Clone into Hermes skills directory
git clone https://github.com/krumjahn/threads-growth-skill ~/.hermes/skills/social-media/threads-growth

# OR create directory structure manually
mkdir -p ~/.hermes/skills/social-media/threads-growth/{references,scripts}
```

## First-time setup

### 1. Export Threads cookies

Required for authentication (cookies last ~60 days):

```bash
# Install Cookie-Editor browser extension
# Navigate to threads.net (logged in)
# Export cookies as JSON
# Save to ~/.hermes/skills/social-media/threads-growth/cookies.json
```

### 2. Run setup script

```bash
cd ~/.hermes/skills/social-media/threads-growth
bash scripts/setup.sh
```

This will:
- Validate cookie format
- Test authentication
- Run first Insights scrape (~5 min)
- Create `references/winning-formats.md`
- Set up bi-weekly cron job

### 3. Configure environment

```bash
# Set your Threads username
export THREADS_USERNAME="your_username"

# Optional: Custom data path
export THREADS_DATA_PATH="$HOME/.hermes/skills/social-media/threads-growth"
```

## Key files

```
threads-growth/
├── SKILL.md                        # This file
├── cookies.json                    # Your session cookies (gitignored)
├── references/
│   └── winning-formats.md          # Performance database (auto-updated)
└── scripts/
    ├── setup.sh                    # One-time setup
    └── scrape_insights.sh          # Insights scraper
```

## Core workflows

### Draft a new post

```bash
# User says: "draft a threads post about [topic]"
# Skill loads winning-formats.md
# Generates draft following your patterns
# Runs algorithm + AI-tone checks
# Returns scored draft
```

**Example pattern matching:**
```markdown
# From winning-formats.md (auto-generated)
Top format: Anti-Demo Hook + Problem/Solution + Proof
Avg engagement: 2,340 views, 186 likes, 23 replies, 12 shares

Structure:
1. Failure state (specific)
2. What you discovered
3. How to implement (3-5 steps)
4. Proof/result (concrete metric)

Best performing: Posts with DM-forwardable utility (how-to, tool lists, templates)
```

### Algorithm red-line check

12 hard suppression rules from Meta's 2025 guidelines:

```bash
# Automatically checked in every draft:
# 1. No external links in first post (only replies OK)
# 2. No bare URLs (use "link in bio" instead)
# 3. No follower begging ("follow me", "help me hit X followers")
# 4. No engagement bait ("comment if you agree", "double tap")
# 5. No fake news/misinformation signals
# 6. No sensationalized language (all caps, excessive punctuation)
# 7. No violent/graphic imagery
# 8. No sexual content
# 9. No hate speech
# 10. No spam patterns (repetitive, copy-paste)
# 11. No impersonation
# 12. No coordinated manipulation
```

### AI-tone detection

Flags and fixes 15 common AI tells before posting:

```bash
# Sentence-level tells:
- "Delve", "utilize", "leverage" → Replace with plain language
- "It's worth noting that" → Cut
- "In today's digital landscape" → Cut or rephrase
- "Game-changer", "unlock" → Use concrete verbs
- Passive voice → Convert to active

# Structure-level tells:
- Lists starting "1. First..." → Vary openings
- Three parallel paragraphs → Break rhythm
- Summary ending "In conclusion..." → Cut
- Overly balanced pros/cons → Take a stance
- Academic hedging ("perhaps", "somewhat") → Be direct
```

### Score a draft

```bash
# Before publishing, get predictive score:
# - DM forwardability (0-10)
# - Repost likelihood (0-10)
# - Algorithm compliance (pass/fail)
# - AI-tone flags (count)
# - Estimated reach multiplier (vs your baseline)
```

## Insights scraper

### Manual run

```bash
cd ~/.hermes/skills/social-media/threads-growth
bash scripts/scrape_insights.sh
```

### What it collects

```bash
# For each post (last 50):
- Post ID
- Publish timestamp
- Text content
- Views (reach)
- Likes
- Replies (total + depth)
- Shares (DM forwards + reposts)
- Save count
```

### Auto-update cron

```bash
# Installed during setup:
# Runs every 2 weeks (Sunday 2 AM)
0 2 * * 0 [ $(($(date +\%s) / 604800 \% 2)) -eq 0 ] && bash ~/.hermes/skills/social-media/threads-growth/scripts/scrape_insights.sh
```

## Hook framework

Built-in post structures ranked by performance:

| Hook Type | Use Case | Avg. Multiplier |
|-----------|----------|-----------------|
| Anti-Demo | You hit failure → found fix | 1.5x |
| Secret Knowledge | Insider info + steps | 1.4x |
| Truth/Comparison | A vs B, clear winner | 1.2x |
| Builder Journey | Workflow switch + results | 1.1x |
| Link Drop | Just a link | 0.2x (avoid) |

### Anti-Demo example structure

```markdown
I wasted 6 weeks posting at "optimal times"
(my reach actually dropped 40%)

Then I found this:

Threads doesn't care about your timezone.
It cares about YOUR audience's active hours.

How to find them:
1. Export your Insights (this skill does it)
2. Map reply times (not post times)
3. Post 1 hour before peak reply window
4. Track for 2 weeks

My reach jumped 2.3x in 10 days.
Same content. Better timing.
```

## Signal weighting

Based on Mosseri 2025 algorithm updates:

```bash
# DM forwards: 3-5x weight of likes
# Deep replies (3+ back-and-forth): 2x weight of top-level
# Saves: 2x weight of likes
# Reposts: 1.5x weight of likes
# Likes: 1x baseline
# Views: Outcome, not signal
```

**Optimization priority:**
1. DM forwardability (utility, tools, templates)
2. Conversation depth (ask questions, provide incomplete info)
3. Save-worthiness (reference value)
4. Repost-ability (identity signal for sharer)
5. Likability (lowest priority)

## Multi-part Threads

For posts >500 chars:

```bash
# Skill automatically chains parts
# Each part: 450-500 chars (leaves buffer)
# Structure:
# Part 1: Hook + problem
# Part 2-N: Steps/details
# Final part: Proof/CTA

# Algorithm treats as one post if:
# - Published within 60 seconds
# - No external engagement between parts
# - Same thread chain
```

## Configuration options

```bash
# Environment variables (optional)
export THREADS_USERNAME="your_username"          # Required
export THREADS_DATA_PATH="$HOME/.hermes/..."    # Default shown
export THREADS_SCRAPE_LIMIT=50                   # Posts to fetch (default 50)
export THREADS_MIN_PERFORMANCE_SAMPLE=10         # Min posts for pattern detection
export THREADS_COOKIE_WARNING_DAYS=7             # Days before expiry to warn
```

## Troubleshooting

### Cookie expiry

```bash
# Symptoms: Scraper fails with 401/403
# Fix: Re-export cookies from browser
# 1. Login to threads.net
# 2. Export cookies (Cookie-Editor)
# 3. Save to cookies.json
# 4. Run: bash scripts/scrape_insights.sh
```

### Missing Insights data

```bash
# Threads only shows Insights for posts with 100+ views
# For new accounts: Wait until you have 10+ qualifying posts
# Check: references/winning-formats.md for sample size

# If sample size < 10:
# - Patterns unreliable
# - Skill uses general best practices until enough data
```

### Scraper hanging

```bash
# Usually: Slow network or Threads rate limiting
# Fix 1: Kill process, wait 5 min, retry
# Fix 2: Reduce THREADS_SCRAPE_LIMIT to 25

pkill -f scrape_insights
sleep 300
bash scripts/scrape_insights.sh
```

### Pattern detection not working

```bash
# Need minimum viable sample:
# - 10+ posts with Insights
# - At least 5 with 500+ views
# - Published over 2+ weeks

# Check your data:
cat references/winning-formats.md | grep "Sample size"
```

## Algorithm knowledge base

Adapted from [AK-Threads-Booster](https://github.com/akseolabs-seo/AK-Threads-booster):

### Boost signals
- Original thinking (not reposted content)
- Conversation starters (questions, incomplete info)
- DM-forwardable utility
- Identity-signal repostability
- Consistent posting (3-5x/week better than daily)

### Suppression signals
- External links in main post
- Engagement bait
- Follower begging
- Repetitive content
- Low reply rate (<2%)

### Timing myths
- "Post at 9 AM" → Wrong. Post 1hr before YOUR audience's active window
- "Post daily" → Wrong. 3-5x/week with high quality beats daily low quality
- "First hour decides reach" → Partially true. First 3 hours matter most.

## Example: Complete workflow

```bash
# 1. User requests
"Draft a threads post about my new AI coding workflow"

# 2. Skill loads patterns
cat references/winning-formats.md
# Identifies: Anti-Demo hook + 3-step process performs best for you

# 3. Generates draft
I tried using ChatGPT for code review.
It missed 3 critical bugs in production code.

Switched to Claude + this prompt structure:
1. Show the code
2. Ask "what breaks first?"
3. Request refactor with error handling

Caught 12 issues ChatGPT missed.
Same AI. Better questions.

# 4. Runs checks
✓ Algorithm compliance (no red-line violations)
✓ AI-tone scan (0 flags)
✓ DM forwardability: 8/10 (actionable steps)
✓ Estimated reach: 1.4x your baseline

# 5. User approves and posts
```

## Data privacy

- All data stored locally (`~/.hermes/skills/social-media/threads-growth`)
- Cookies never transmitted (used only for Threads authentication)
- Insights data never shared
- No tracking, no analytics

## Performance baseline

Typical results after 6 weeks:
- 1.5-2.5x reach improvement
- 2-3x engagement rate increase
- 40-60% reduction in low-performing posts
- Better pattern recognition every 2-week cycle

## Updates

```bash
# Pull latest version
cd ~/.hermes/skills/social-media/threads-growth
git pull origin main

# Refresh patterns (optional)
bash scripts/scrape_insights.sh
```

---

**Built by [@krumjahn](https://www.threads.com/@krumjahn)** — Running live since April 2026. MIT License.
