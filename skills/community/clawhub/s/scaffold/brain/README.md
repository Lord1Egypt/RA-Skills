<!--
brain/ - Extended Knowledge & Projects

WHAT THIS IS: The folder where your agent stores non-memory, non-operational content.
Think of it as your agent's filing cabinet - organized knowledge, project files,
research, and specialized domain content.

HOW TO CUSTOMIZE:
  - Create subdirectories as you start new projects or domains
  - Your agent will create folders here autonomously as needed
  - The structure below is a starting point - adapt it to what you actually do
-->

# brain/ - Structure Guide

The `brain/` directory is where your agent stores extended knowledge, project files, and research. Unlike `memory/` (which is operational logs and curated long-term memory), `brain/` is organized by domain and project.

---

## Default Structure

```
brain/
├── README.md           ← you are here
├── [project-name]/     ← one folder per project or venture
│   ├── README.md       ← what this project is, status, links
│   └── ...             ← project files
├── learning/           ← articles, notes, things your agent is digesting
│   ├── reading-queue.md
│   └── ...
└── [domain]/           ← specialized knowledge domains
    └── ...
```

---

## What Goes Where

| Content Type | Where It Lives |
|---|---|
| Raw session logs | `memory/YYYY-MM-DD.md` |
| Curated long-term memory | `MEMORY.md` |
| Lessons learned | `memory/lessons.md` |
| Active task backlog | `memory/active-tasks.md` |
| **Project files, research, specs** | `brain/[project-name]/` |
| **Learning queue, digested articles** | `brain/learning/` |
| **Domain knowledge** | `brain/[domain]/` |
| Environment-specific tool notes | `TOOLS.md` |

---

## Starting Projects

When starting a new project, have your agent create:
```
brain/[project-name]/
├── README.md     - what it is, current status, key links
└── [relevant files]
```

This keeps project context out of MEMORY.md (which has a hard 80-line limit) while making it easy to load with `read brain/[project-name]/README.md`.

---

## Learning System

The `brain/learning/` folder is for reading queue management. Structure:
```
brain/learning/
├── reading-queue.md    - articles/papers queued to read
├── digests/            - summaries after reading
└── [topic].md          - notes organized by topic
```

Your agent can proactively pull from the reading queue during quiet heartbeat periods.

---

## Tips

- **Keep README.md files in project folders** - they let your agent quickly orient to a project without reading all the files
- **Don't put secrets in brain/** - same rules as everywhere else
- **Link from MEMORY.md to brain/** - "Full details: brain/[project]/README.md" keeps MEMORY.md lean
- **brain/ is git-safe** (assuming you scrub credentials) - commit it for backup and versioning
