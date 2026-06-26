---
name: vitepress-generator
description: Quickly generate static websites using VitePress. Supports installing dependencies, initializing projects, local preview, building, and deployment.
---

# VitePress Static Website Generator

## Feature Overview

Quickly generate static websites using VitePress. Supports installing dependencies, initializing projects, local preview, building, and deployment.

## Trigger Scenarios

- User mentions "static website", "documentation site", "generate website", "build documentation", "create blog", "VitePress", "vitepress", "vuepress", "documentation site", "technical documentation", "project documentation", "personal blog", etc.

## Quick Start

When users need to create a static website, follow the process below:

### 1. Check Environment

First, confirm that the user has Node.js installed:

```bash
node -v
npm -v
```

If not installed, prompt the user to install Node.js first (v18+ recommended).

### 2. Create Project Directory

```bash
mkdir <project-name>
cd <project-name>
npm init -y
```

### 3. Install VitePress

```bash
npm add -D vitepress
```

### 4. Initialize Project Structure

Create the basic directory structure:

```
<project-name>/
├── docs/
│   ├── .vitepress/
│   │   └── config.mts
│   ├── index.md
│   └── guide/
│       └── getting-started.md
├── package.json
└── README.md
```

### 5. Configure Scripts

Add the following to `package.json`:

```json
{
  "scripts": {
    "docs:dev": "vitepress dev docs",
    "docs:build": "vitepress build docs",
    "docs:preview": "vitepress preview docs"
  }
}
```

### 6. Local Preview

```bash
npm run docs:dev
```

Default access: http://localhost:5173

### 7. Build

```bash
npm run docs:build
```

Output directory: `docs/.vitepress/dist/`

## Complete Configuration Reference

For detailed configuration options, see [references/config-guide.md](references/config-guide.md)

## Theme Customization

For custom themes and styles, see [references/theme-customization.md](references/theme-customization.md)

## Deployment Guide

For deployment to different platforms, see [references/deployment.md](references/deployment.md)

## Quick Command Reference

| Command | Description |
|------|------|
| `npm run docs:dev` | Start local development server |
| `npm run docs:build` | Build production version |
| `npm run docs:preview` | Preview build results |

## Important Notes

1. **Node.js Version**: Requires v18 or higher
2. **Port Usage**: Development server uses port 5173 by default
3. **Build Output**: Build artifacts are located in `docs/.vitepress/dist/` directory
4. **Config Files**: Supports `.mts`, `.ts`, `.mjs`, `.js` formats