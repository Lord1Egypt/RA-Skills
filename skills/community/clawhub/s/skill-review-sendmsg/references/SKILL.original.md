---
name: py-review-skill
description: Automated code review with local lint checks, hard-rule blocking, and LLM batch review for changed .php/.js/.ts/.sql/.sh files. Use when testing or running cron-based repository review workflows.
---

# py-review-skill

## Scripts

- `scripts/review.py` : single repo review (`repo_path from_commit to_commit`)
- `scripts/review_runner.py` : multi-project runner with state tracking and Telegram notifications

## Quick test

1. Prepare env (example):

```bash
export LLM_API_KEY="your_key"
export LLM_API_URL="https://api.deepseek.com/v1/chat/completions"
export LLM_MODEL="deepseek-chat"
```

2. Single repo test:

```bash
python3 scripts/review.py <repo_path> <from_commit> <to_commit>
```

3. Multi-project test:

```bash
export PROJECTS_DATA=$'Demo|ssh://git@example.com/org/repo.git|review|-1001234567890'
python3 scripts/review_runner.py
```
