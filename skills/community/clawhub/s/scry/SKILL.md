---
name: scry
version: "1.0.0"
description: "Research any topic across 26+ sources: Reddit, X, YouTube, GitHub, HN, Bluesky, ArXiv, Dev.to, Polymarket, and more. The most comprehensive research skill available."
argument-hint: 'scry AI agents, scry best Claude Code skills, scry bitcoin ETF --deep'
allowed-tools: Bash, Read, Write, WebSearch
homepage: https://github.com/khalidsh/scry-skill
user-invocable: true
---

# SCRY v1.0 — Research Any Topic Across 26+ Sources

Search Reddit, X, YouTube, GitHub, Hacker News, Bluesky, Dev.to, ArXiv, Polymarket, Stack Overflow, Product Hunt, Mastodon, Wikipedia, GDELT, CoinGecko, SEC EDGAR, TikTok, Instagram, HuggingFace, Substack, and more. Surface what people are discussing, building, citing, betting on, and debating right now.

## CRITICAL: Parse User Intent

Before doing anything, parse the user's input for:

1. **TOPIC**: What they want to learn about
2. **TARGET TOOL** (if specified): Where they'll use the prompts
3. **QUERY TYPE**:
   - **RECOMMENDATIONS** — "best X", "top X" → wants a LIST
   - **NEWS** — "what's happening with X" → wants current events
   - **PROMPTING** — "X prompts" → wants techniques + copy-paste prompts
   - **GENERAL** — anything else → wants broad understanding
4. **DOMAIN**: Auto-detected or user-specified
   - **tech** — programming, AI, software, frameworks
   - **science** — research, papers, experiments
   - **finance** — stocks, earnings, markets
   - **crypto** — blockchain, tokens, DeFi
   - **news** — politics, geopolitics, events
   - **entertainment** — movies, music, gaming, social
   - **general** — everything else

**Store these variables:**
- `TOPIC = [extracted topic]`
- `TARGET_TOOL = [extracted tool, or "unknown"]`
- `QUERY_TYPE = [RECOMMENDATIONS | NEWS | PROMPTING | GENERAL]`
- `DOMAIN = [auto-detected or user-specified]`

**DISPLAY your parsing:**

```
I'll research {TOPIC} across 26+ sources to find what's been discussed in the last 30 days.

Parsed intent:
- TOPIC = {TOPIC}
- DOMAIN = {DOMAIN}
- QUERY_TYPE = {QUERY_TYPE}
- TARGET_TOOL = {TARGET_TOOL or "unknown"}

Research typically takes 1-3 minutes. Starting now.
```

---

## Research Execution

**Step 1: Run the SCRY script (FOREGROUND — do NOT background this)**

**CRITICAL: Run in FOREGROUND with 5-minute timeout. Read the ENTIRE output.**

```bash
for dir in \
  "." \
  "${CLAUDE_PLUGIN_ROOT:-}" \
  "$HOME/.claude/skills/scry" \
  "$HOME/.agents/skills/scry"; do
  [ -n "$dir" ] && [ -f "$dir/scripts/scry.py" ] && SKILL_ROOT="$dir" && break
done

if [ -z "${SKILL_ROOT:-}" ]; then
  echo "ERROR: Could not find scripts/scry.py" >&2
  exit 1
fi

python3 "${SKILL_ROOT}/scripts/scry.py" "$ARGUMENTS" --emit=compact
```

Use a **timeout of 300000** (5 minutes) on the Bash call.

The script will automatically:
- Detect your domain (tech/science/finance/crypto/news/entertainment/general)
- Discover available API keys and binaries
- Search all available sources in parallel
- Score results with domain-aware weights
- Deduplicate and cross-link across sources
- Detect conflicts between sources
- Output a comprehensive research report

**Read the ENTIRE output.** It contains sections for every source that returned results.

**Add `--domain=DOMAIN` if you detected the domain in intent parsing.**
**Add `--deep` if the user asked for comprehensive results.**

---

## Step 2: WebSearch Supplement

After the script finishes, do WebSearch to supplement with blogs, tutorials, and news.

Choose queries based on QUERY_TYPE:
- **RECOMMENDATIONS**: `best {TOPIC} recommendations`, `{TOPIC} list examples`
- **NEWS**: `{TOPIC} news 2026`, `{TOPIC} announcement update`
- **PROMPTING**: `{TOPIC} prompts examples 2026`, `{TOPIC} techniques tips`
- **GENERAL**: `{TOPIC} 2026`, `{TOPIC} discussion`

Exclude reddit.com, x.com, twitter.com (covered by script).

---

## Judge Agent: Synthesize All Sources

**Ground your synthesis in the ACTUAL research content, not pre-existing knowledge.**

1. Weight sources by domain relevance (tech: GitHub/HN/SO highest; science: ArXiv/S2 highest; etc.)
2. Cross-platform signals are strongest — items with `[also on: ...]` tags are most important
3. Note conflicts between sources (flagged in the output)
4. Extract top 3-5 actionable insights

### CITATION RULES
- Cite sparingly: 1-2 per topic, 1 per pattern
- Priority: @handles > r/subreddits > YouTube channels > GitHub repos > HN > ArXiv > web
- Never paste raw URLs — use source names
- **BAD:** "per https://arxiv.org/abs/..." → **GOOD:** "per ArXiv"
- **BAD:** "per @x, @y, @z" → **GOOD:** "per @x" (pick strongest)

### If QUERY_TYPE = RECOMMENDATIONS
Extract SPECIFIC NAMES — products, tools, repos, people. Count mentions. List by popularity.

---

## Display Format

**FIRST — What I learned:**

```
What I learned:

**{Topic 1}** — [1-2 sentences, per @handle or r/sub]

**{Topic 2}** — [1-2 sentences, per @handle or r/sub]

KEY PATTERNS from the research:
1. [Pattern] — per @handle
2. [Pattern] — per r/sub
3. [Pattern] — per GitHub repo
```

**THEN — Stats (copy EXACTLY, replacing placeholders):**

The script outputs a stats block — display it as-is. If it doesn't appear, build one:

```
---
✅ All agents reported back!
├─ 🟡 HN: {N} stories │ {N} points │ {N} comments
├─ 🦞 Lobsters: {N} items │ {N} points
├─ 📝 Dev.to: {N} articles │ {N} reactions
├─ 🐙 GitHub: {N} repos │ {N}★
├─ 🦋 Bluesky: {N} posts │ {N} likes
├─ 🟠 Reddit: {N} threads │ {N} upvotes
├─ 🔵 X: {N} posts │ {N} likes
├─ 🔴 YouTube: {N} videos │ {N} views
├─ 📄 ArXiv: {N} papers │ {N} citations
├─ 📊 Polymarket: {N} markets │ {odds summary}
├─ 🌐 Web: {N} pages — Source, Source, Source
└─ 🗣️ Top voices: @handle1, @handle2 │ r/sub1, r/sub2
---
```

**Omit any source line that returned 0 results.**

**LAST — Invitation (adapt to QUERY_TYPE):**

Include 2-3 SPECIFIC suggestions based on research findings.

---

## WAIT FOR USER'S RESPONSE

After showing results, STOP and wait.

## WHEN USER RESPONDS

- **Question** → Answer from research (no new searches)
- **Go deeper** → Elaborate using findings
- **Create something** → Write a tailored prompt
- **Different topic** → Run new research

---

## Agent Mode (--agent flag)

If `--agent` in ARGUMENTS:
1. Skip intro display
2. Skip AskUserQuestion calls
3. Run research + output report
4. Stop (no follow-up invitation)

---

## Security & Permissions

**What this skill does:**
- Searches 26+ public APIs and RSS feeds for research data
- Runs `gh` CLI for GitHub search (uses your existing auth)
- Runs `yt-dlp` for YouTube search (public data)
- Optionally uses ScrapeCreators API for TikTok/Instagram
- Stores cached results in ~/.cache/scry/ (24h TTL)

**What this skill does NOT do:**
- Does not post, like, or modify content on any platform
- Does not access private accounts or data
- Does not share API keys between providers
- Does not write to any external service

**Bundled scripts:** `scripts/scry.py` (orchestrator), `scripts/lib/` (shared utilities + source modules)
