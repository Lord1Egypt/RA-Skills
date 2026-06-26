---
name: sniplink
description: OpenClaw skill. One-shot URL saver for tools and services discovered on X, GitHub, or anywhere. Drop a link, get it categorized, tagged, and stored — no friction, no multi-step forms. Built for ADHD brains and anyone who keeps losing track of tools they saved across bookmarks, notes, and chats.
---

# SnipLink — The ADHD-Friendly URL Saver

## Who It's For

You found something cool. You want it saved **now** — before you forget, before you lose the tab, before the momentum dies.

SnipLink saves it instantly: title, description, category, tags, social links. Done in seconds. No multi-step forms, no "where should I put this" paralysis.

## Trigger
Use this skill when:
1. User shares a URL and wants it saved — "save this", "remember this", "add to my stash"
2. User shares an X/Twitter link — detect tweet content, extract the real target, and save it
3. User asks "what tools do I have for X" or wants to search their saved links
4. User is brainstorming and needs quick tool suggestions by tag or category

> **Zero friction.** One URL in, clean record out. Confirm once, forget about it.

## Workflow

### 1. Saving a Link (One-Shot)

**Step 1: Detect source type**
- **X/Twitter URL** (`x.com`, `twitter.com`) → go to **X/Twitter Pipeline** (see below)
- **GitHub.com repo URL** → use `gh api` (structured data, no scraping)
- **All other URLs** → use `web_fetch`

**Step 2: Extract info**

For GitHub repos, extract:
- Repo name, description, primary language, star count, license, topics/tags, last updated, owner

For all other pages:
- `web_fetch` → title, meta description, pricing, features
- Skip if behind login, paywall, or CAPTCHA

**Step 3: Auto-categorize**
- **AI/ML** — AI services, LLMs, machine learning
- **Development** — Coding tools, APIs, frameworks, testing
- **Productivity** — Task management, notes, workflow automation
- **Marketing** — SEO, social media, ads, content
- **Design** — Graphics, UI/UX, video, prototyping
- **Finance** — Billing, accounting, payments
- **Communication** — Messaging, email, calls, CRM
- **Data** — Analytics, databases, visualization
- **Other** — Anything else

**Step 4: Auto-generate tags**
- Extract from description, GitHub topics, or page keywords
- Common: free, paid, api, no-code, open-source, mobile, cloud, etc.

**Step 5: Social media lookup**
- `web_search` tool name + "LinkedIn" / "Twitter"
- Store URLs if found

**Step 6: Present for approval (MANDATORY)**
- Show the user a clean summary of what was extracted:
  - Title, description, category, tags, price
  - Source (direct URL / tweet / GitHub)
- Ask: "Save this? (yes / no / edit)"
- If user says no → discard, ask if they want to modify
- If user says edit → let them adjust fields before saving
- If user says yes → save to database
- NEVER save without user seeing the extracted data first

---

### X/Twitter Pipeline

**Trigger:** User shares an `x.com` or `twitter.com` URL and wants it saved.

**Step 1: Extract tweet content (use fxtwitter API first)**
- Primary method: `curl -sL "https://api.fxtwitter.com/{user}/status/{id}"`
  - Returns JSON with `tweet.text`, `tweet.author`, `tweet.media`, `tweet.raw_text.facets` (links inside tweet)
  - Works without browser, no login, no CAPTCHA — fast and reliable
- Extract username and ID from URL patterns: `x.com/{user}/status/{id}` or `twitter.com/{user}/status/{id}` or `x.com/i/status/{id}`
- If fxtwitter fails, fallback to browser: `browser_navigate` to the tweet URL + snapshot
- If both fail, tell the user the tweet is unreachable and ask them to paste the text

**Step 2: Understand tweet context (CRITICAL — no blind clicking)**
- Read the full tweet text carefully
- Determine the tweet's intent:
  - **Sharing a tool/service** → tweet describes or links to something useful
  - **Announcing a launch** → new product, repo, or feature
  - **Thread/review** → opinion about an existing tool
  - **Mentioning a repo by name** → no direct link, but repo name is in the text
  - **Just a meme/comment** → nothing to save, tell the user politely

**Step 3: Extract the target URL**
- If the tweet contains a link → analyze what it links to:
  - GitHub URL → use `gh api` for structured data
  - Website URL → scrape with `web_fetch`
  - Another tweet/thread → follow if relevant, otherwise skip
- If NO link but the tweet mentions a tool/repo name:
  - Search GitHub: `gh search repos <name> --limit 5`
  - Or search the web if it's not a repo
- If multiple links → use the tweet context to determine which one is the main target

**Step 4: Extract info from the target**
- Follow the standard extraction (Steps 2-4 from the main workflow)
- Combine tweet context with page data for richer description

**Step 5: Present for approval (MANDATORY)**
- Show the user:
  - **Tweet summary:** what the tweet said
  - **Extracted target:** URL that was found/followed
  - **Tool info:** title, description, category, tags, price
- Ask: "Save this to SnipLink? (yes / no / edit)"
- NEVER auto-save from tweets — the user must always confirm

**Step 6: Save or discard**
- On approval → save to database with tweet URL as a `source` field in notes
- On rejection → discard cleanly

### 2. Retrieving Saved Links

- By category: "Show me all AI tools"
- By search: "Find something for PDF editing"
- By tag: "Show me everything tagged free"
- Full list: "List all my saved tools"

### 3. Tool Suggestions (Opt-In)

When user asks for project help, search by relevant tags/categories and suggest.

## GitHub Integration

GitHub URLs get treated specially via `gh api`:

```bash
# Repo metadata example
gh api repos/{owner}/{repo}
```

Extracted fields: name, description, language, stargazers_count, topics, license, updated_at, homepage, html_url

No web scraping needed for GitHub — clean, fast, accurate.

## Content Boundaries

**Never scrape:**
- Pages behind login, paywall, or CAPTCHA
- Pages blocked by robots.txt
- URLs containing personal data (iCloud, Google Drive shared links, etc.)

**Sanitization:**
- Strip tracking params from URLs before saving (utm_*, fbclid, etc.)
- Never store OAuth tokens, API keys, or session IDs

## Pitfall: Unreachable Sites

When curl and browser both fail to reach a site (timeouts, connection refused), **stop retrying** after 2 attempts. The issue is connectivity, not permissions.

1. Tell the user clearly: "The site is unreachable from this environment — not a permission issue."
2. Offer alternatives: user describes it manually, save with minimal info and update later, or try from a different network.
3. Do NOT keep retrying the same failing approach — it frustrates the user and wastes turns.
4. Before scraping, briefly state what you're about to do: "Let me scrape the site for details before saving."

## Storage: Obsidian (Single Source of Truth)

SnipLink stores all saved tools as Obsidian notes in the user's vault. This centralizes all knowledge in one place and enables graph connections between tools, projects, and concepts.

### Vault Location
`~/Library/CloudStorage/GoogleDrive-abdulrahmanjahfali@gmail.com/My Drive/My Mind/SnipLink/`

### Structure
- One markdown note per saved tool: `SnipLink/{Tool Name}.md`
- Master index: `SnipLink/SnipLink Index.md`

### Record Format (Obsidian Note)

```markdown
---
title: Tool Name
url: https://example.com
category: Development
tags: [python, api, free]
price: "Free / $X/mo"
saved: 2026-04-04
---

# Tool Name

Description of what it does.

## Details
- **Use case:** What it's used for
- **Notes:** Extra info, source, stats

## Contact
- **Email:** ...
- **Website:** ...

## Social
- [LinkedIn](...)
- [Twitter](...)
```

### Index Format (SnipLink Index.md)
Update the index file when saving a new entry. Use Obsidian wiki-links `[[Tool Name]]` for graph connections. Include Dataview queries for dynamic listing.

## Retrieving Links from Obsidian

When user asks to search saved tools:
1. Use `obsidian` skill to search/read notes in the `SnipLink/` folder
2. Search by tags, category, title, or content
3. Present results as a summary
