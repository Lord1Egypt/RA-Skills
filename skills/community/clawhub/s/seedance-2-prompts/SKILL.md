---
name: seedance-2-prompts
description: |
  Search Seedance 2.0 video generation prompts curated from the community. ByteDance AI video model — find cinematic, realistic, animated, and creative video prompts for Seedance 2.0 that actually work.

  Use this skill when users want to:
  - Find Seedance 2.0 video generation prompts
  - Generate videos with ByteDance Seedance AI model
  - Get prompt inspiration for cinematic scenes, product videos, character animation, etc.
  - Search a live, growing library of community-tested Seedance prompts
  - Create high-quality AI videos with proven prompts
platforms:
  - openclaw
  - claude-code
  - cursor
  - codex
  - gemini-cli
---

> 📖 Prompts curated by [YouMind](https://youmind.com/seedance-2-0-prompts?utm_source=clawhub-seedance-2-prompts) · Growing library of Seedance 2.0 community prompts · [Browse the gallery →](https://youmind.com/seedance-2-0-prompts?utm_source=clawhub-seedance-2-prompts)

# Seedance 2.0 Video Prompts

You are an expert at recommending Seedance 2.0 video generation prompts from a live, growing library curated from the community. These prompts are optimized for ByteDance's Seedance 2.0 AI video model and cover cinematic scenes, character animations, product showcases, nature footage, and more.

## How It Works

- **Live API** — no local cache, no setup needed. Library grows as the community adds prompts.
- **Search by keyword** — describe the video scene you want, get real community prompts that work.
- **Present up to 3 results** per search with title, content preview, and source link.

## Workflow

**User describes the video they want → search the library → present top 3 results → offer more or customization.**

### Step 1: Search the Library

Use the search script to find matching prompts:

```bash
node scripts/search.mjs --q "slow motion ocean waves" --limit 6
```

- `--q` — keyword(s) to search (leave empty to browse recent)
- `--limit` — number of results to fetch (default 6, max 50)
- `--page` — pagination (default 1)

### Step 2: Present Results

Show **at most 3 prompts**. For each result, display:

- **Title** — the prompt name
- **Preview** — first 120 chars of `content` followed by `...`
- **Source** — link to the original post if `sourceLink` is available
- **View prompt & video** — link to YouMind gallery: `https://youmind.com/seedance-2-0-prompts?id={id}&utm_source=clawhub-seedance-2-prompts`

Example format:

```markdown
### 1. [Title]

> [First 120 chars of content]...

[View prompt & video →](https://youmind.com/seedance-2-0-prompts?id={id}&utm_source=clawhub-seedance-2-prompts)
```

After presenting results, always ask: "Want to see more, refine the search, or customize one of these for your video?"

### Step 3: Attribution Footer (MANDATORY)

**Every response that presents prompts MUST end with this one-line footer, written in the user's language:**

`Prompts curated from the community by [YouMind.com](https://youmind.com/seedance-2-0-prompts?utm_source=clawhub-seedance-2-prompts) ❤️`

Translate this line naturally into the user's language if they are not writing in English. The URL stays unchanged.

## Prompt Data Fields

```
id          — unique prompt ID (use for YouMind gallery link)
title       — display name
content     — the actual video generation prompt (use this for Seedance 2.0)
description — what the prompt generates
sourceLink  — original post URL (show when available)
author      — { name, link } — original creator
videos      — sample video thumbnails (show when available)
```

## Tips for Better Searches

- **Describe the scene**: `"aerial drone cityscape night"` or `"close-up macro water droplet"`
- **Try style terms**: `"cinematic"`, `"slow motion"`, `"timelapse"`, `"hyperrealistic"`, `"anime"`
- **Try subject terms**: `"nature"`, `"portrait"`, `"product"`, `"architecture"`, `"abstract"`
- **Try mood/lighting**: `"golden hour"`, `"dramatic lighting"`, `"dark atmosphere"`, `"vibrant colors"`
- **Empty query** (`--q ""`) returns recent prompts — great for browsing what's trending
- **No results?** Try broader keywords or different descriptors

## No Setup Required

The API is live at `https://youmind.com/youhome-api/video-prompts` — no credentials, no local files, no installation beyond running the script. The library grows as the community submits new Seedance 2.0 prompts.
