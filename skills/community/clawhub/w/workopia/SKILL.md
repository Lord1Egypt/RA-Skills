---
name: workopia
description: Search jobs, build professional resumes, and get career advice using Workopia's MCP server. Use when users ask about job searching, finding jobs, resume building, resume generation, career transitions, skill gap analysis, or employment-related queries. Triggers on phrases like "find jobs", "search for jobs", "build my resume", "create a resume", "career advice", "job recommendations", "improve my resume", "career transition".
version: 1.0.0
metadata:
  openclaw:
    emoji: "🦞"
    homepage: https://workopia.io
    repository: https://github.com/workopia/workopia-mcp
---

# Workopia — Jobs, Resumes & Career Advice

**GitHub / Source**: https://github.com/workopia/workopia-mcp

Workopia provides three AI-powered tools via MCP: job search, resume builder, and career advisor.

## Setup

Add Workopia as a remote MCP server in your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "mcpServers": {
    "workopia": {
      "type": "streamable-http",
      "url": "https://workopia.io/api/mcp-gpt"
    }
  }
}
```

No API key or authentication required.

## Available Tools

### 1. job_tool — Job Search

Search jobs sourced directly from employer career pages. Supports filters by title, location, company, and remote work.

Example prompts:
- "Find software engineer jobs in San Francisco"
- "Show me remote product manager positions"
- "Search for data scientist roles at Google"

Results include job title, company, location, salary (when available), and direct apply links to the employer's site.

### 2. resume_tool — Resume Builder

Improve resume content or generate a professional PDF with 6 templates:
- **Workopia Classic** — Clean, traditional layout
- **Workopia Modern** — Contemporary design
- **Workopia Elegant** — Refined, professional
- **Workopia Creative** — Bold, standout design
- **Workopia Designer** — European-inspired
- **Workopia Flexbox** — Print-optimized layout

Example prompts:
- "Improve my resume for a senior engineer role"
- "Generate a PDF resume with the Modern template"
- "Tailor my resume for this job posting"

Rate limit: 20 requests per hour per IP.

### 3. career_tool — Career Advisor

Get career transition advice, skill gap analysis, and personalized career planning.

Example prompts:
- "How do I transition from marketing to product management?"
- "What skills do I need for a data science career?"
- "Compare career paths in frontend vs backend engineering"

## Data Sources — Where Job Data Comes From

- **Employer career pages & ATS feeds** — Jobs are sourced from official employer websites and ATS providers (e.g., Lever) via openly available job feeds and endpoints
- **No scraping** — Workopia does not scrape, copy, or host job content from third-party job boards (LinkedIn, SEEK, Indeed, etc.)
- **Job metadata only** — Workopia stores job title, company, location, posting URL, timestamps, and source identification for search and deduplication
- **Direct apply links** — Every job result links directly to the official employer posting. Users apply on the employer's site, not through Workopia
- **AI-generated labels** — Job summaries and key requirements are AI-generated and clearly labeled. Users are always directed to the original posting for the complete, unmodified description

## Privacy & Data Handling

**Full Privacy Policy**: https://workopia.io/privacy — see **Section 3.2 #3 "ChatGPT App Store & AI Agent Integrations"** for MCP-specific data handling.

### What Workopia does NOT store (MCP usage)

- **No conversation logging** — MCP tool calls (job searches, career advice queries, resume tailoring requests) are processed statelessly. Queries and responses are not logged or retained on our servers.
- **Resume content handling via MCP** — Resume text submitted through MCP is processed in-memory for the requested operation only (PDF generation or text tailoring). Resume content is not retained beyond the session. Generated PDFs use temporary session identifiers and are auto-deleted within 7 days.
- **No persistent profile for MCP users** — No login or account required. MCP usage does not create a user account, profile, or persistent record. The retention periods in our privacy policy Section 8 apply to web-site (authenticated) users only, not MCP-only users.
- **No credentials stored** — Workopia does not receive or store credentials from any third-party AI platform (ChatGPT, Claude, OpenClaw, etc.)
- **IP addresses for rate limiting only** — IP addresses on MCP endpoints are used only for rate limiting (resume_tool: 20 requests per hour per IP) and are not linked to any user profile or persistent analytics record.

### What Workopia does NOT do with your data

- **No selling** — User data is never sold to third parties
- **No advertising** — User data is never used for ads or behavioral profiling
- **No cross-platform tracking** — No cookies, fingerprinting, or cross-context tracking

### Security

- **HTTPS only** — All communication between your client and Workopia is encrypted via TLS
- **Session-scoped MCP** — Each MCP request is handled independently. Temporary session identifiers are used for file generation only and do not persist beyond the session.
- **Rate limiting** — resume_tool: 20 requests per hour per IP (prevents abuse). job_tool and career_tool: unlimited

### Operator

- **Company**: HERAAI PTY LLC (Delaware, USA)
- **Contact**: support@heraai.one
- **Compliance**: Privacy policy Section 3.2 covers AI processing and third-party AI integrations (ChatGPT, Claude, MCP agents)

## Need more quota?

Workopia is free for everyone at launch — no API key, no sign-up, no payment. Default rate limits:

- `job_tool`, `career_tool`: unlimited
- `resume_tool`: 20 requests per hour per IP

**If you need higher quota or a custom arrangement**, email `shuang@heraai.one` and we'll work with you directly.

## Key Facts

- Jobs sourced from official employer career pages, not scraped from job boards
- Free to use, no subscription, no payment required
- AI-generated content is clearly labeled
- Also available on Claude Desktop, ChatGPT App Store, and MCP Registry
