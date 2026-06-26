# SkillBoss.co Known Working Skills

> Last updated: 2026-04-14 (午后)  
> Total: **39 verified skills**

This is a manually curated list of skills that exist on SkillBoss.co and can be downloaded.

## ✅ Verified Skills (39)

### Batch 1 (Published to TobeyRebecca)
- https://www.skillboss.co/skills/a-stock-trading-assistant
- https://www.skillboss.co/skills/academic-deep-research
- https://www.skillboss.co/skills/academic-writing
- https://www.skillboss.co/skills/adaptive-reasoning
- https://www.skillboss.co/skills/adaptive-suite
- https://www.skillboss.co/skills/anycrawl
- https://www.skillboss.co/skills/apex
- https://www.skillboss.co/skills/api-designer
- https://www.skillboss.co/skills/appdeploy
- https://www.skillboss.co/skills/app-store-changelog
- https://www.skillboss.co/skills/audio-transcribe
- https://www.skillboss.co/skills/backtest-expert
- https://www.skillboss.co/skills/baidu-scholar-search
- https://www.skillboss.co/skills/baidu-web-search
- https://www.skillboss.co/skills/browser-automation

### Batch 2 (Published to ModestyRichards)
- https://www.skillboss.co/skills/ai-daily-briefing
- https://www.skillboss.co/skills/ai-image-generation
- https://www.skillboss.co/skills/ai-meeting-notes
- https://www.skillboss.co/skills/ai-news-collector
- https://www.skillboss.co/skills/ai-news-oracle
- https://www.skillboss.co/skills/architecture-designer
- https://www.skillboss.co/skills/arxiv
- https://www.skillboss.co/skills/arxiv-watcher
- https://www.skillboss.co/skills/asr
- https://www.skillboss.co/skills/audiopod
- https://www.skillboss.co/skills/markdown-converter
- https://www.skillboss.co/skills/news-aggregator
- https://www.skillboss.co/skills/price-tracker
- https://www.skillboss.co/skills/seedance-video

### Batch 3 (Published 2026-04-14 - TobeyRebecca 5个 + ModestyRichards 5个)
- https://www.skillboss.co/skills/audio-transcribe
- https://www.skillboss.co/skills/backtest-expert
- https://www.skillboss.co/skills/baidu-scholar-search
- https://www.skillboss.co/skills/baidu-web-search
- https://www.skillboss.co/skills/browser-automation
- https://www.skillboss.co/skills/markdown-converter (重复)
- https://www.skillboss.co/skills/news-aggregator (重复)
- https://www.skillboss.co/skills/price-tracker (重复)
- https://www.skillboss.co/skills/seedance-video (重复)
- https://www.skillboss.co/skills/adhd-assistant

### Discovered via Playwright (2026-04-14, Not Yet Published)
- https://www.skillboss.co/skills/adhd-daily-planner
- https://www.skillboss.co/skills/admapix
- https://www.skillboss.co/skills/advanced-skill-creator
- https://www.skillboss.co/skills/agent-builder
- https://www.skillboss.co/skills/agent-chronicle
- https://www.skillboss.co/skills/agent-church
- https://www.skillboss.co/skills/agent-council
- https://www.skillboss.co/skills/agent-directory
- https://www.skillboss.co/skills/agent-evaluation
- https://www.skillboss.co/skills/agent-orchestration

## ❌ Tested But Don't Exist

Common names that seem logical but return 404:
- ai-email-assistant
- ai-code-reviewer
- ai-content-generator
- automation-helper
- calendar-assistant
- code-formatter
- data-scraper
- email-automation
- file-organizer
- git-helper
- image-optimizer
- instagram-insights
- linkedin-scraper
- tiktok-trends
- twitter-intel
- youtube-analyzer

## 🔍 How to Find More

### Method 1: Playwright Auto-Discovery (Recommended) ✨

Run the scraper script:
```bash
cd skills/skill-publisher/scripts
python3 scrape-skillboss.py
```

Output: `/tmp/skillboss-all-skills.txt`

**Pros**:
- Automated
- Discovers 20-50+ skills in one run
- Easy to re-run for updates

**Cons**:
- Requires Playwright installation
- May miss skills behind pagination
- Takes ~30 seconds

### Method 2: Manual Browsing

1. **Visit the correct page**:
   - ✅ https://www.skillboss.co/skills (works)
   - ❌ https://www.skillboss.co/browse (404)

2. **Copy skill URLs manually**

### Method 3: Pattern Testing
   ```bash
   # Test if a skill exists
   curl -I "https://www.skillboss.co/api/skills/skill-name/download"
   # HTTP 200 = exists
   # HTTP 404 = doesn't exist
   ```

3. **Check GitHub/ClawHub**:
   - Look at what others have published
   - Skills often reference SkillBoss in their docs

## 📝 Naming Patterns (Observed)

SkillBoss skills seem to follow these patterns:
- Lowercase with hyphens: `browser-automation`
- Domain/product names: `baidu-scholar-search`
- Action + noun: `backtest-expert`, `price-tracker`
- Platform + feature: `arxiv-watcher`

**Not** common:
- CamelCase
- Underscores
- "ai-" prefix (only 5/29 have it)

## 🤝 Contributing

Found a new working skill? Add it here:
1. Verify it downloads: `curl -I "https://www.skillboss.co/api/skills/NAME/download"`
2. Add to the appropriate section above
3. Update the count in the header

---

**Why this list matters**:
SkillBoss.co has no public listing API, so we can't auto-discover skills. This list enables batch operations without manual URL hunting.
