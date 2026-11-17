---
name: worklittle-jobs-mcp
description: "Worklittle Jobs MCP — search 4M+ jobs with visa/salary/distance filters, swipe to apply, create resumes & cover letters, and connect your Worklittle account"
version: 1.0.0
author: Worklittle | ClawHub
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, jobs, career, search, apply, resume, cover-letter]
---

# Worklittle Jobs MCP

Connect AI assistants to Worklittle for job search, application, resume, and cover letter generation across 4+ million job listings.

## Source

- GitHub: https://github.com/worklittle/jobs-mcp
- Official Registry: `io.github.worklittle/jobs`
- Remote MCP: https://mcp.worklittle.com/
- Docs: https://docs.worklittle.com/mcp
- Support: support@worklittle.com

## What It Does

- **Search 4M+ jobs** with filters: visa sponsorship, salary, distance, location, company, job type, seniority
- **Swipe & apply** — connect your Worklittle account to save jobs and apply directly
- **Generate documents** — create hiring-manager-ready resumes and cover letters
- **Market insights** — get aggregate job market statistics and trends
- **ATS tools** — manage job listings and candidates (employer-side)

## Installation

### Add MCP Server

In your Hermes Agent config (`config.yaml`), add:

```yaml
mcpServers:
  worklittle:
    url: https://mcp.worklittle.com/
    headers:
      Authorization: "Bearer REDACTED-SECRET"
```

Or run via CLI:

```bash
hermes mcp add worklittle --url https://mcp.worklittle.com/
```

### Get API Key

1. Sign up at https://worklittle.com/business
2. Generate API key at https://worklittle.com/business/api-keys
3. Keys start with `sk-wl-api01-`

## Tools

### Job Search & Application

| Tool | Description |
|------|-------------|
| `search_jobs` | Search jobs by keyword, company, location, visa, salary, distance |
| `get_job_details` | Get full job description, qualifications, company info |
| `get_job_keywords` | Extract distilled skill/tech keywords from a job description |
| `get_market_overview` | Aggregate job market statistics (no params required) |
| `submit_job_application` | Submit application to a Worklittle-hosted job ($0.01/submit) |
| `apply_for_job` | Alternative apply endpoint |

### Document Generation

| Tool | Description |
|------|-------------|
| `create_resume` | One-page resume (HTML, PDF, or DOCX). Uses real facts only. |
| `create_cover_letter` | One-page cover letter tailored to a specific job |

### Account & Profile

| Tool | Description |
|------|-------------|
| `search_jobs` (app mode) | Opens interactive Jobs app with swipe, Maps, Saved, profile |
| `get_company` | Read your Worklittle company identity |
| `set_company` | Update company identity (requires verified work email) |

### ATS (Employer Tools)

| Tool | Description |
|------|-------------|
| `list_posted_jobs` | List your ATS job postings |
| `create_job_listing` | Create a candidate-facing job listing |
| `list_candidates` | List candidates for your organization |
| `bookmark_candidate` | Bookmark a candidate (shared across org) |
| `create_candidate_notes` | Add notes to a candidate profile |
| `update_candidates` | Move candidate through pipeline stages |

## Usage

### Search Jobs

```python
# Example: search remote software engineer jobs with visa sponsorship
search_jobs(
    query="software engineer",
    location="remote",
    visa_sponsored=True,
    min_salary=120000,
    distance_miles=50,
    limit=20
)
```

### Get Job Details

```python
# After searching, get details for a specific role
get_job_details(job_id="abc123")
```

### Generate Keywords for Resume Tailoring

```python
# Extract skills from a job description (better than using full JD text)
keywords = get_job_keywords(job_id="abc123")
# Returns: ["Python", "React", "AWS", "GraphQL", "Kubernetes", ...]
```

### Create Resume

```python
# One-page resume from your context
resume = create_resume(
    format="pdf",  # html, pdf, or docx
    context={"experience": [...], "education": [...]}
)
```

### Apply to a Job

```python
# Submit application (requires jobs:apply scope on API key)
submit_job_application(
    job_id="abc123",
    resume_url="...",
    cover_letter="..."
)
# Cost: $0.01 per successful submission
```

### Market Overview

```python
# Get high-level job market stats
overview = get_market_overview()
# Returns: total_jobs, remote_ratio, top_hiring_companies, salary_ranges...
```

## Prompt Guide

### Job Search Flow

```
1. User: "Find me remote Python jobs with visa sponsorship paying $150k+"
2. Agent: Call search_jobs with filters → present results with salary, visa status, distance
3. User: "Tell me more about X"
4. Agent: Call get_job_details(job_id) → summarize key requirements
5. User: "What skills does this role need?"
6. Agent: Call get_job_keywords(job_id) → show distilled tech stack
7. User: "Apply to this one"
8. Agent: Call submit_job_application or open Jobs app via search_jobs app mode
```

### Resume Building Flow

```
1. User: "Tailor my resume for this job"
2. Agent: Call get_job_keywords(job_id) to get exact skill requirements
3. Agent: Call create_resume with job context → generates targeted resume
4. Agent: Suggest specific improvements based on keyword gap analysis
```

## Protocol

- **Transport**: JSON-RPC 2.0 over HTTP (Streamable HTTP)
- **Auth**: Bearer token (`sk-wl-api01-*`)
- **Base URL**: `https://mcp.worklittle.com/`
- **Dual-era support**: Modern 2026-07-28 Streamable HTTP + legacy initialize protocols

## Pitfalls

- **API key scope matters** — `submit_job_application` requires `jobs:apply` scope
- **External vs Worklittle jobs** — `submit_job_application` only works for employer-posted jobs on Worklittle, not external `apply_url` listings
- **Keyword vs full JD** — use `get_job_keywords` instead of full job description for resume/cover letter generation (better quality)
- **No vector embeddings** — search is substring/FTS based, not semantic
- **Negative terms** — use leading dash to exclude, e.g., `"software engineer -junior"`
- **Price per application** — $0.01 per successful submit; budget accordingly for bulk applications

## Integration with Other Tools

```yaml
# Combined workflow: search → apply → track
# Use with:
# - hermes mcp tools (native)
# - mcporter CLI (ad-hoc)
# - REST API directly (for apps without MCP libraries)
```

## Verification

After installing, test with:

```bash
# Check MCP connection
hermes mcp list

# Test search
hermes mcp call worklittle search_jobs '{"query": "remote python", "limit": 3}'

# Expected: JSON array of job listings with title, company, salary, location
```

## References

- GitHub: https://github.com/worklittle/jobs-mcp
- Documentation: https://docs.worklittle.com/mcp
- Official Registry: `io.github.worklittle/jobs`
- Privacy: https://worklittle.com/privacy
