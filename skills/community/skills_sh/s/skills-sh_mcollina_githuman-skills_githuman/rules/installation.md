# Installation

GitHuman can be run directly with npx or installed globally.

## Quick Start (No Installation)

```bash
npx githuman serve
```

This downloads and runs GitHuman immediately, opening the web interface at http://localhost:3847.

## Global Installation

For frequent use, install globally:

```bash
npm install -g githuman
```

Then run commands directly:

```bash
githuman serve
githuman list
githuman todo list
```

## Requirements

- Node.js 24 or later (uses native SQLite)
- Git repository (GitHuman works within git repos)

## Data Storage

GitHuman stores data in `.githuman/reviews.db` (SQLite database) in your repository root. This file contains:

- All reviews and their status
- Inline comments and suggestions
- Todos and their completion status

**Important**: The `.githuman/` directory is not tracked by git. Back it up if you need to preserve review history.
