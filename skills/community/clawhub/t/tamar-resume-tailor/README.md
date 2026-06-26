# Tamar Resume Tailor — ClawHub Skill

Tailor your resume for any job in seconds using AI. Upload your resume, provide a job description or URL, and Tamar will reframe your real experience to match the role — honestly, no exaggerations.

## What This Skill Does

- Parses your resume (PDF, DOCX, TXT)
- Checks for an existing experience profile (enriched Q&A data = higher quality)
- Analyzes a job description (URL or text)
- Rewrites your resume to highlight the most relevant experience
- Accepts natural-language feedback to refine the result
- Downloads a polished PDF

## Requirements

- Node.js 18+
- A free Tamar account at [ask-tamar.com](https://ask-tamar.com)
- An API key (Profile → API Keys)

## Installation

Install the CLI and configure your API key **before** enabling this skill. The skill will not attempt to install packages on your behalf.

```bash
npm install -g tamar-cli
tamar auth --key tmr_your_key_here
```

The API key is stored locally in `~/.tamarrc`. This file is only accessed by the `tamar` CLI binary — the skill instructs the agent to use CLI commands (`tamar status`, `tamar profile`, etc.) rather than reading config files directly.

## Quick Start

```bash
# Upload your resume
tamar upload resume.pdf

# Check your experience profile
tamar profile

# Tailor it for a job (URL or pasted text in a temp file)
tamar tailor --job 'https://linkedin.com/jobs/12345'

# Refine with feedback
tamar feedback 'Make the summary shorter and highlight Python more'

# Download the PDF
tamar download
```

## Commands

| Command | Description |
|---------|-------------|
| `tamar auth --key <key>` | Configure API key |
| `tamar upload <file>` | Upload and parse a resume |
| `tamar profile` | View your experience profile(s) |
| `tamar tailor --job <url\|text>` | Generate a tailored resume |
| `tamar feedback "<text>"` | Apply feedback and create a new version |
| `tamar download` | Download the latest resume as PDF or JSON |
| `tamar status` | Check plan, usage, and subscription status |

## API Documentation

Full API reference: [ask-tamar.com/developers](https://ask-tamar.com/developers)

## Pricing

Free tier includes 1 tailored resume. Paid plans at [ask-tamar.com](https://ask-tamar.com).
