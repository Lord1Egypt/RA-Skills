# Vietnam Fullstack Jobs

> Search ITviec, TopDev, ITJobs, and TopCV for the latest full-stack developer job listings using Firecrawl. Finds jobs with React, Next.js, TypeScript, Node.js, NestJS, and related technologies. Requires firecrawl-search skill and FIRECRAWL_API_KEY env var. Trigger for requests like "tìm việc fullstack", "job mới", "fullstack jobs", or "việc làm lập trình viên".

---

## English

### Why

This skill exists to make fullstack jobs requests repeatable instead of ad-hoc. It gives the agent a clear workflow, expected output shape, and domain boundaries so the result is more consistent and easier to reuse.

### What

This repository contains an OpenClaw skill for this domain.

Core scope: Search ITviec, TopDev, ITJobs, and TopCV for the latest full-stack developer job listings using Firecrawl. Finds jobs with React, Next.js, TypeScript, Node.js, NestJS, and related technologies. Requires firecrawl-search skill and FIRECRAWL_API_KEY env var. Trigger for requests like "tìm việc fullstack", "job mới", "fullstack jobs", or "việc làm lập trình viên".

It can help with:

- Turning rough requests into a structured response flow
- Keeping outputs consistent across repeated runs
- Reusing companion knowledge files when the skill folder includes them
- Making the skill easier to publish, review, and install on ClawHub

### How

Use this skill with any AI tool that supports custom instructions or project knowledge. The core entry point is `SKILL.md`, and companion folders can be attached when they exist.

### Getting Started

1. Open your AI tool or agent workspace.
2. Point the agent to `SKILL.md` in this folder.
3. No extra support folders are required beyond `SKILL.md`.
4. Start with a prompt like one of these:

```text
tìm việc fullstack
job mới
fullstack jobs
việc làm lập trình viên
```

### Repository Structure

```text
.
├── README.md
├── SKILL.md
```

### Main File

- `SKILL.md`

---
