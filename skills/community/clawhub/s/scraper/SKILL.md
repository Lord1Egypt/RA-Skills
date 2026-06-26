---
name: scraper
description: Structured extraction and cleanup for public, user-authorized web pages. Use when the user wants to collect, clean, summarize, or transform content from accessible pages into reusable text or data. Do not use to bypass logins, paywalls, captchas, robots restrictions, or access controls. Local-only output.
---

# Scraper

Turn messy public pages into clean, reusable data.

## Core Purpose
Scraper is a safe extraction skill for public, user-authorized pages.
It helps the agent:
- fetch page content from a URL
- extract readable text
- strip boilerplate where possible
- save clean output locally
- prepare content for later summarization or analysis

## Safety Boundaries
- Only use on public or user-authorized pages
- Do not bypass logins, paywalls, captchas, robots restrictions, or rate limits
- Do not request or store credentials
- Do not perform stealth scraping, account creation, or identity evasion
- Save outputs locally only

## Runtime Requirements
- Python 3 must be available as `python3`
- No external packages required

## Local Storage
All outputs are stored locally under:
- `~/.openclaw/workspace/memory/scraper/jobs.json`
- `~/.openclaw/workspace/memory/scraper/output/`

## Key Workflows
- **Capture a page**: `fetch_page.py --url "https://example.com"`
- **Extract readable text**: `extract_text.py --url "https://example.com"`
- **Save cleaned content**: `save_output.py --url "https://example.com" --title "Example"`
- **List prior jobs**: `list_jobs.py`

## Scripts
| Script | Purpose |
|---|---|
| `init_storage.py` | Initialize scraper storage |
| `fetch_page.py` | Download a page with standard headers |
| `extract_text.py` | Convert HTML into cleaned plain text |
| `save_output.py` | Save extracted output and register a job |
| `list_jobs.py` | Show past scraping jobs |
