---
name: sharpagent-intelligence-monitor
version: 1.0.0
description: "SharpAgent Intelligence Monitor — Multi-track parallel intelligence aggregation system. Auto-collects from RSS/arXiv/GitHub/36kr, 3D dynamic scoring, five-factor trust verification, structured briefing output. For daily intelligence summaries, tech trend tracking, and competitive monitoring."
metadata:
  openclaw:
    emoji: "📡"
    tags:
      - intelligence
      - monitor
      - daily-briefing
      - frontier
      - sharpagent
      - analysis
---

# SharpAgent Intelligence Monitor v1.0.0

> **Let your agent scan the frontier for you every day.**
> Multi-track parallel collecting → 3D dynamic scoring → Five-factor trust verification → Structured briefing output.
> Based on AI Frontier Monitor architecture + SharpAgent five-factor verification + frontier scouting experience.

## Contract

```yaml
contract:
  name: sharpagent-intelligence-monitor
  version: "1.0.0"
  category: monitor
  trust_level: verified
  reads:
    - InformationSource
    - FiveFactorResult
  writes:
    - InformationSource
    - CrossValidation
  preconditions:
    - "Access to web_search tool"
    - "Access to curl/jq for API fetching"
  postconditions:
    - "Each info item has a score (0-5)"
    - "Output tiered: core/watching/quick-scan"
    - "Cross-track signals extracted"
  calibration:
    default_mode: professional
    modes_supported: [warm, professional, deep]
  compliance:
    jurisdiction: global
    safety_level: standard
  lifecycle:
    status: active
    publish_as: SharpAgent
```

## Architecture: 5-Track Parallel + Five-Factor Verification

```
Sources (5 tracks parallel)
    ↓
3D Automatic Scoring (relevance/quality pre-filter)
    ↓
Dynamic Tiers (core / watching / quick-scan)
    ↓
Cross-Track Signal Detection
    ↓
Five-Factor Trust Verification ← SharpAgent differentiator
    ↓
Structured Briefing Output
    ↓
Archive to Ontology
```

### Track 1: 🏢 Enterprise — 11 RSS Feeds

| Feed | URL | Priority |
|------|-----|----------|
| OpenAI Blog | openai.com/blog | ⭐⭐⭐⭐⭐ |
| Anthropic Blog | anthropic.com/blog | ⭐⭐⭐⭐⭐ |
| AWS ML Blog | aws.amazon.com/blogs/machine-learning | ⭐⭐⭐⭐⭐ |
| Google AI Blog | ai.googleblog.com | ⭐⭐⭐⭐ |
| Meta AI Blog | ai.meta.com/blog | ⭐⭐⭐⭐ |
| Techmeme | techmeme.com/feed | ⭐⭐⭐⭐ |
| The Verge AI | theverge.com/ai-artificial-intelligence | ⭐⭐⭐ |
| Hacker News | news.ycombinator.com | ⭐⭐⭐ |
| Product Hunt | producthunt.com | ⭐⭐ |
| Ars Technica AI | arstechnica.com/ai | ⭐⭐ |
| Wired AI | wired.com/tag/artificial-intelligence | ⭐⭐ |

### Track 2: 🇨🇳 China — 36kr Hotlist

```bash
curl -s "https://openclaw.36krcdn.com/media/hotlist/{date}/24h_hot_list.json"
```

Covering: China tech hotspots, AI dynamics, funding, industry trends

### Track 3: 📚 Papers — arXiv

Fetch latest from:
- cs.AI (Artificial Intelligence)
- cs.LG (Machine Learning)
- cs.CL (Computation and Language)

### Track 4: 🔥 GitHub Trending (AI/ML)

Fetch daily trending repos in:
- AI agents
- LLM tools
- ML frameworks

### Track 5: 🔍 Web Search Supplement

Use `web_search` tool for topics with insufficient coverage.

---

## Scoring: 3-Dimensional Dynamic

Each candidate is scored on 3 dimensions:

| Dimension | Weight | What to Look For |
|-----------|--------|-----------------|
| 🏢 Enterprise Landing | 40% | Real deployment, company name, scale, customer evidence |
| 📊 Data Support | 30% | Quantified results (%, improvements, benchmarks) |
| 💡 Learnability | 30% | Methodology, architecture, lessons learned, patterns |

### Source Bonuses

| Source | Bonus |
|--------|-------|
| OpenAI / Anthropic / AWS official | +1.0 |
| Techmeme / peer-reviewed papers | +0.5 |
| Product Hunt / HN | +0.3 |
| 36kr (China relevance) | +1.0 for Chinese audience |

### Dynamic Tiers (based on actual score distribution)

```
Score Distribution → Dynamic Thresholds
    ↓
🔴 Core: top ~15% or ≥3.5 (max 3)
🟡 Watching: top ~30% or ≥2.5 (max 5)
🟢 Quick Scan: ≥1.0 (max 8)
```

---

## Signal Detection

Extract cross-track signals into 3 categories:

| Signal Type | Keywords | Output |
|-------------|----------|--------|
| 🛠 Tech Trends | new model, architecture, framework, benchmark, SOTA | Tech radar update |
| 🏢 Product Releases | launch, GA, open-source, preview, beta | Release tracker |
| 💰 Funding/M&A | series, raised, acquire, investment, valuation | Money map |

---

## SharpAgent Integration: Five-Factor Secondary Verification

After the 3D scoring pass, add the SharpAgent five-factor as a secondary trust gate:

```
Article → 3D Score → Five-Factor Verification → Final Tier
```

**Five-factor weights** (in intel context):
- 🔗 Source Anchor: 0.30 — Is the source reliable?
- 🧠 Logic Anchor: 0.20 — Is the analysis self-consistent?
- 🌍 Compliance Anchor: 0.15 — Is it compliant?
- 🏳️ Interest Anchor: 0.15 — Marketing bias?
- 🔄 Cross Anchor: 0.20 — Multiple sources confirm?

**Final Confidence** = `score_3d * 0.6 + five_factor_confidence * 0.4`

**Quality Gates**:
- Five-factor < 5 → Excluded from briefing
- Source Anchor < 3 → Discarded
- Interest = confirmed → Manual review required

---

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 SharpAgent Intelligence Briefing · {Day} {Date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Overview
   Sources: {N} tracks
   Candidates: {total} | High quality: {quality}
   🔗 Trust check: passed {pass}/{total}

🔴 Core Intelligence ({N} items)
### 1. {Title}
🔗 {Link}
💡 Takeaway: {One-line insight}
🔗 Trust score: {score}/10

🟡 Worth Watching ({N} items)
1. **{Title}** 🔗 {Link}

🟢 Quick Scan ({N} items)
• [{Title}]({Link})

📚 arXiv Papers (≤3)
**{Title}** — {Authors}
Abstract: {Abstract[:150]} → {Link}

🔥 GitHub Trending AI (≤3)
**{Repo}** ({Lang}) +{TodayStars}⭐ → {Link}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Today's Signals
🛠 Tech Trends: {signal}
🏢 Product Launches: {signal}
💰 Capital Movements: {signal}

🔍 Five-Factor Trust Analysis
   🔗 Source Anchor: {avg}/10
   🧠 Logic Anchor: {avg}/10
   🌍 Compliance: {pass_rate}%
   🏳️ Interest Conflicts: {conflict_rate}%
   🔄 Cross Anchor: {avg}/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ {HH:MM} | sharpagent-intelligence-monitor v1.0 | SharpAgent
```

## Workflow

### Step 1: Fetch All Tracks

```bash
# Enterprise RSS
python3 scripts/rss-crawler.py

# 36kr
curl -s "https://openclaw.36krcdn.com/media/hotlist/$(date +%Y-%m-%d)/24h_hot_list.json"

# arXiv
bash scripts/arxiv-fetch.sh --category cs.AI --days 7 --max 10

# GitHub Trending
bash scripts/github-trending-fetch.sh --period daily
```

### Step 2: Score Candidates

Run each candidate through the 3D scoring engine. Source bonuses applied per track.

### Step 3: Apply Five-Factor Verification

Each core-tier candidate gets full five-factor review:
1. 🔗 Is the source reliable?
2. 🧠 Is the analysis internally consistent?
3. 🌍 Is it compliant?
4. 🏳️ Any marketing bias?
5. 🔄 Can we verify it independently?

Watch-tier candidates get a lightweight check (source + logic).
Scan-tier candidates skip verification.

### Step 4: Compute Final Confidence

```
final_confidence = score_3d * 0.6 + five_factor_confidence * 0.4
```

### Step 5: Detect Cross-Track Signals

Compare candidates across all 5 tracks. Same topic in multiple tracks = signal, not just a single item. High signal = high priority.

### Step 6: Render & Deliver

Render in calibration-appropriate mode:
- **Warm**: Tier labels + confidence indicators only
- **Professional**: Full briefing with per-item analysis
- **Deep**: Full briefing + five-factor breakdown per core item

### Step 7: Archive

Save to `data/briefings/{YYYY-MM-DD}-briefing.md`

---

## Edge Cases

| Situation | Action |
|-----------|--------|
| RSS empty | Run with remaining tracks, skip RSS section |
| arXiv API timeout | Skip papers, log warning |
| GitHub fetch fails | Skip trending, log warning |
| 36kr 404 (no data) | Skip 36kr items |
| Zero quality items (<2 at ≥2.5) | Return `NO_REPLY` |
| Same company multiple sources | Deduplicate, keep highest score |
| 3 consecutive days <3 core items | Trigger source review |
| Five-factor fails all core items | Return "No reliable intel today" |

## Quality Gates

| Check | What | Fail action |
|-------|------|-------------|
| Max 16 items/day | 3+5+5+3(papers)+3(GitHub) | Trim tiers |
| NO_REPLY when <2 quality | <2 items at score ≥2.5 | Return NO_REPLY |
| Dedup same entity | Cross-source same-company | Keep highest score |
| Five-factor filter | Core items must pass verification | Drop or flag |
| 3-day threshold fail | Trigger review | Review alert |

## Integration Points

### Five-Factor Review Skill
- `sharpagent-five-factor-review` called per core candidate
- Verification results appended to briefing

### Calibration Framework
- Output mode controlled by calibration settings
- Deep mode includes full five-factor breakdown

### Ontology
- Each briefed item archived as InformationSource
- FiveFactorResult attached as validation

## Version History

- **v1.0.0** — Initial release. 5-track intel monitor with five-factor verification.

---

*SharpAgent · MIT-0 · 2026-05-11*
