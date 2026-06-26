---
name: tooldeck
description: Auto-scrapes URLs to extract tool/service info, auto-categorizes, and saves to a personal database. Use when user explicitly shares a URL to save or asks to remember a service. Always confirm before saving. Never auto-save without user intent.
---

# ToolDeck - Personal Service/Tool Database

## Trigger
Use this skill when:
1. User shares a URL and explicitly asks to save it
2. User asks to "save" or "remember" a service or tool they provided
3. User asks "what tools do I have for X"
4. User explicitly requests tool suggestions for a project

> **Privacy first:** Never scrape, save, or monitor URLs without explicit user request. The skill is entirely passive — it only acts when the user intentionally asks it to.

## What It Does

User provides a URL with intent to save → scrape → extract info → categorize → confirm → save to database

## Workflow

### 1. Saving a Tool (User-Initiated Only)

**Step 1: Confirm intent**
- Only proceed if user explicitly asked to save a URL
- Never auto-save from casual browsing or project context

**Step 2: Scrape the URL**
- Use `web_fetch` to get page info
- Extract: title, description, pricing, features, logo
- **Respect robots.txt** — do not scrape pages that disallow it
- **Skip authenticated/private pages** — do not attempt to scrape pages behind login walls, paywalls, or CAPTCHAs

**Step 3: Auto-categorize**
- Analyze content to detect category:
  - **AI/ML** - AI services, LLMs, machine learning
  - **Development** - Coding tools, APIs, frameworks
  - **Productivity** - Task management, notes, workflow
  - **Marketing** - SEO, social media, ads
  - **Design** - Graphics, UI/UX, video
  - **Finance** - Billing, accounting, payments
  - **Communication** - Messaging, email, calls
  - **Data** - Analytics, databases, visualization
  - **Other** - Anything else

**Step 4: Find social media**
- Search for LinkedIn, Facebook, Instagram, Twitter
- Use `web_search` with tool name + "social media"

**Step 5: Auto-generate tags**
- Extract keywords from description
- Common tags: free, paid, api, no-code, ai, etc.

**Step 6: Confirm and save**
- Present the extracted info to the user
- Only save after user confirms
- Confirm: "Saved: [title] ([category])"

### 2. Retrieving Tools

- By category: "Show me all AI tools"
- By search: "Find something for PDF"
- Full list: "List all my saved tools"

### 3. Tool Suggestions (Opt-In Only)

- Only suggest tools when the user explicitly asks for project help
- Do not proactively monitor or inject suggestions during normal chat

## Content Boundaries

**Never scrape:**
- Pages behind login, paywall, or authentication
- Pages blocked by robots.txt
- Private/intranet URLs
- URLs containing personal data (icloud, google drive shared links, etc.)

**Sanitization:**
- Do not store OAuth tokens, API keys, or session IDs if present in URLs
- Strip tracking parameters (utm_*, fbclid, etc.) from URLs before saving

## Database Location

`/workspace/skills/tooldeck/references/database.json`

## Format

```json
{
  "tools": [
    {
      "url": "https://example.com",
      "title": "Tool Name",
      "description": "What it does",
      "category": "Development",
      "tags": ["python", "api", "free"],
      "use_case": "For building APIs",
      "notes": "Good alternatives to X",
      "saved_date": "2026-04-04",
      "price": "Free / $X/mo",
      "social_media": {
        "linkedin": "...",
        "facebook": "...",
        "instagram": "..."
      },
      "contact": {
        "email": "...",
        "location": "..."
      }
    }
  ]
}
```
