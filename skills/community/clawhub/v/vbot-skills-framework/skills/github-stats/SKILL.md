---
name: github-stats
description: Use when user wants to check GitHub repo stats, stars, forks, or activity.
triggers: ["github", "stars", "⭐", "repo", "仓库"]
version: 1.0.0
---

# 📊 GitHub Stats Skill

> Quick GitHub repository statistics

## Usage

```bash
gh api repos/{owner}/{repo} -q '.stargazers_count,forks_count,description'
```

## Example Triggers

- "这个仓库有多少 stars"
- "check github stats for..."
- "X 仓库怎么样"

## Response Format

```
⭐ {stars} | 🍴 {forks}
{description}

{other stats}
```

## Common Metrics

| Metric | Command |
|--------|---------|
| Stars | `gh api ... -q '.stargazers_count'` |
| Forks | `gh api ... -q '.forks_count'` |
| Description | `gh api ... -q '.description'` |
| Language | `gh api ... -q '.language'` |
| Created | `gh api ... -q '.created_at'` |
