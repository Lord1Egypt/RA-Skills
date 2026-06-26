---
name: research-pipeline
description: Automated literature research pipeline for Chopin's academic work. Combines arXiv search, paper summarization, and Obsidian note-taking into a single workflow. Use when Chopin asks to research a topic, find papers, do a literature review, or stay updated on formation control / event-triggered communication / multi-agent systems. Triggered automatically by daily cron for research topic updates.
---

# Research Pipeline

Automated end-to-end research workflow: search → summarize → save to Obsidian.

## Workflow

### Step 1: Search arXiv

Use the `arxiv` skill to search for papers on the target topic.

```
Search arXiv for: <query>
Limit: 5-10 most relevant papers
```

Key research topics for Chopin:
- Multi-vehicle formation control
- Event-triggered communication
- Collision avoidance in multi-agent systems
- Reinforcement learning for formation control
- Learning-based control with event-triggered communication

### Step 2: Summarize Papers

For each promising paper, use `paper-summarize-academic` to get:
- Paper title, authors, date
- Core contribution
- Key methodology
- Relevance to Chopin's research

### Step 3: Save to Obsidian

Use the `obsidian` skill to create literature notes:
- One note per paper in `References/` folder
- Tag with: #paper #formation-control #event-triggered etc.
- Include: title, authors, year, arXiv link, summary, key takeaways

### Step 4: Report to Chopin

Send a brief digest via Feishu with:
- Number of papers found
- Top 3 most relevant papers with 1-line summary each
- Link to full notes in Obsidian

## Research Topics Tracker

Maintain a `research-topics.md` in workspace tracking:
- Active topics of interest
- Last searched date
- Papers found count

See `references/research-topics.md` for Chopin's current research profile.

## Cron Integration

When triggered by daily cron (research update):
1. Check `research-topics.md` for active topics
2. Search arXiv for each topic (new papers since last check)
3. Summarize and save new findings
4. Report only genuinely new/interesting papers (avoid spam)
