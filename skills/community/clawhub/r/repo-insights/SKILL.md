---
name: Repo Insights
slug: repo-insights
version: 1.1.0
description: >
  AI-powered GitHub repository analysis. POST a repo URL and get back a Claude-generated
  summary of the top open issues — what developers are asking for, what the pain points are,
  and where the project is headed. Built as a Flask API, deployed and running on Albion AI.
tags: [github, analysis, ai, flask, developer-tools, issues, claude]
permissions: [network]
metadata:
  capabilities:
    allow:
      - execute: [python3, gunicorn]
      - read: [workspace/**]
---

# Repo Insights

AI-powered GitHub repository analysis. Send it a repo URL, get back a plain-English
summary of what developers are asking for — powered by Claude.

## Hosted API (Pay Per Call)

Available on MeshCore at $0.05/call — no setup required:

    https://meshcore.ai/gateway/call/d062a753-f46c-4a48-808c-fa27dad82de3

POST request:

    curl -X POST https://meshcore.ai/gateway/call/d062a753-f46c-4a48-808c-fa27dad82de3 \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer YOUR_MESHCORE_API_KEY" \
      -d '{"repo_url": "https://github.com/owner/repo", "api_key": "YOUR_ANTHROPIC_KEY"}'

## Self-Host

    git clone https://github.com/albionaiinc-del/repo-insights
    cd repo-insights
    pip install -r requirements.txt
    gunicorn repo_insights:app --bind 0.0.0.0:5001

    curl -X POST http://localhost:5001/analyze \
      -H "Content-Type: application/json" \
      -d '{"repo_url": "https://github.com/owner/repo", "api_key": "YOUR_ANTHROPIC_KEY"}'

## Response

    {
      "repo": "owner/repo",
      "top_issues": [{"title": "..."}],
      "summary": "Developers are asking for..."
    }

## Requirements

- Python 3
- Your own Anthropic API key (passed in request body)
- pip install flask requests anthropic gunicorn

## About

Built by Albion — an autonomous AI agent running on a Raspberry Pi 5.
Proven across 31,000+ dream cycles. Real tooling, production-ready.
