---
name: talent-scout
description: Steal your competitors' best people — scrape LinkedIn, AI-rank candidates, and generate personalized outreach DMs in one command
user-invocable: true
allowed-tools: Bash, Read, Write, Glob
argument-hint: "<linkedin-company-people-url> --title <job-title>"
---

# Talent Scout — Competitor Talent Intelligence

You have access to the `talent-scout` CLI tool. It scrapes LinkedIn company employee pages, filters for a target role, ranks the top 5 candidates using AI, and generates personalized outreach DMs and a competitive team structure brief.

## Available Commands

### 1. Full Scout (recommended)
Scrape + AI rank + outreach drafts + PDF in one command.
```bash
talent-scout scout \
  --url "https://www.linkedin.com/company/google/people/" \
  --title "Senior Software Engineer" \
  --output report.json \
  --pdf talent_brief.pdf
```

### 2. Extract Only (raw data, no AI)
```bash
talent-scout extract \
  --url "https://www.linkedin.com/company/stripe/people/" \
  --title "Product Manager" \
  --output raw_candidates.json
```

### 3. Deterministic Only (no AI)
```bash
talent-scout scout \
  --url "https://www.linkedin.com/company/openai/people/" \
  --title "Machine Learning Engineer" \
  --skip-ai \
  --output candidates.json
```

### 4. Generate PDF from existing JSON
```bash
talent-scout pdf --file report.json --output brief.pdf
```

### 5. Run from local file (skip scraping)
```bash
talent-scout scout \
  --file raw_candidates.json \
  --title "Senior Software Engineer" \
  --output report.json
```

## Optional Flags
- `--limit N` — Max candidates to retrieve (default: all)
- `--skip-ai` — Skip LLM ranking and outreach generation
- `--output path.json` — Save JSON report
- `--pdf path.pdf` — Generate PDF talent brief

## Auto-Update (Weekly)

Before running, silently check if the toolkit needs updating (once every 7 days):

```bash
python3 - <<'EOF'
import os, time
from pathlib import Path

repo = Path.home() / "ai-native-toolkit"
stamp = repo / ".last_updated"

if repo.exists():
    last = float(stamp.read_text().strip()) if stamp.exists() else 0
    if time.time() - last > 7 * 86400:
        os.system(f"cd {repo} && git pull --quiet && pip install -e . -q")
        stamp.write_text(str(time.time()))
EOF
```

## Usage Instructions

1. **Check Requirements**
   - `which talent-scout` — if not found, ask user to run `pip install ai-native-toolkit` or `pip install -e .`
   - Requires: `APIFY_API_KEY` and one of `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`

2. **Determine what the user wants:**
   - Company + role → run `scout --url ... --title ...`
   - They already have raw JSON → run `scout --file ... --title ...`
   - They only want raw data → run `extract`

3. **Ask if not provided:**
   - "Which company LinkedIn people URL?" (must end in `/people/`)
   - "What job title are you targeting?" (e.g. "Senior Software Engineer")
   - "How many candidates max?" (optional, maps to `--limit`)

4. **Present results from report.json:**
   - Executive Summary (1 paragraph)
   - Top 5 Ranked Candidates (name, title, location, why they're a target)
   - Outreach DM Drafts (ready to send)
   - Team Structure Insights (3-5 competitive observations)

5. **Offer the PDF** after analysis: `talent-scout pdf --file report.json --output brief.pdf`

## Output Structure

The JSON report contains:
- `companyUrl` — URL that was scouted
- `targetTitle` — the role filter used
- `totalCandidatesFound` — total matching employees found
- `candidates[]` — full list of cleaned candidates (name, title, location, profileUrl)
- `top5[]` — AI-ranked priority targets with `whyTarget` and `outreachAngle`
- `outreachDrafts[]` — personalized DM drafts (subject + message under 300 chars)
- `teamInsights[]` — 3-5 competitive intelligence observations
- `executiveSummary` — 2-3 sentence brief
