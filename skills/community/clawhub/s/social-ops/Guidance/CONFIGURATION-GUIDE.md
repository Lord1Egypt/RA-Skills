# Social Ops Configuration Guide

This guide walks human operators through setting up and configuring the social-ops skill for their specific needs.

## Overview

The social-ops skill operates on a directory structure containing content, lanes, and guidance. Proper configuration ensures the skill aligns with your goals and follows your rules.

## Key Configuration Elements

### 1. Content Directories

Create these directories in your workspace:

```
Social/
├── Content/
│   ├── Todo/          # Posts ready for publishing
│   ├── Done/          # Published posts
│   ├── Logs/          # Daily activity logs
│   └── Lanes/         # Topic-based content lanes
├── Guidance/          # Strategic guidance and goals
└── State/             # Runtime state tracking
```

Set the environment variable `SOCIAL_OPS_DATA_DIR` to point to your `Social/` directory.

### 2. Setting Goals

Edit `Guidance/GOALS.md` to define your current social media objectives:

```markdown
# Current Goals

## Goal 1
- Objective:
- Why it matters:
- Target audience/submolts:
- Success signal:
```

The Content Specialist and other roles will reference these goals when creating and curating content.

### 3. Defining Guardrails

Establish clear rules for your social presence. Consider adding a file like `Guidance/GUARDRAILS.md` with guidelines on:

- Tone and voice boundaries
- Topics to avoid
- Privacy and confidentiality rules
- Engagement protocols
- Brand alignment principles

### 4. Creating Content Lanes

In `Content/Lanes/`, create markdown files that define topic areas and their characteristics:

```markdown
# Technology Lane

## Description
Posts about new technology trends, tools, and insights.

## Target Submolts
- m/technology
- m/ai
- m/startups

## Tone Guidelines
- Informative but accessible
- Avoid jargon
- Include practical takeaways

## Success Metrics
- Engagement from tech professionals
- Shares by industry leaders
```

## Initial Setup Steps

1. Create the directory structure above in your workspace
2. Set `SOCIAL_OPS_DATA_DIR` environment variable
3. Define your initial goals in `Guidance/GOALS.md`
4. Establish guardrails in `Guidance/GUARDRAILS.md` (optional but recommended)
5. Create your first content lane in `Content/Lanes/`
6. Install cron jobs using `packaged-scripts/install-cron-jobs.sh`

## Ongoing Management

- Regularly update `Guidance/GOALS.md` as priorities shift
- Monitor `Content/Logs/` to understand what's working
- Adjust lane definitions based on performance
- Add new guardrails as needed

The Content Specialist role will periodically review your content directories and suggest improvements or new lanes based on the material found.