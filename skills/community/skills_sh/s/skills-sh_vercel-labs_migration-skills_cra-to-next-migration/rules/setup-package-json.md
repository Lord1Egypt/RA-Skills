---
title: Update Dependencies and Scripts
impact: CRITICAL
impactDescription: Required for Next.js to run
tags: setup, dependencies, scripts, package-json
---

## Update Dependencies and Scripts

CRA includes react-scripts which bundles all tooling. Next.js requires explicit dependencies and different scripts.

**CRA package.json (before):**

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.0.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

**Next.js package.json (after):**

> **Important:** Use Next.js 16.x or later. Do NOT use Next.js 14.x or 15.x. Run `npm info next version` to check for the latest version.

```json
{
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "next": "^16.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.0.0"
  },
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

**Key changes:**
- Remove `react-scripts` and `react-router-dom`
- Add `next` as a dependency
- Replace scripts with Next.js equivalents
- `start` becomes `dev` for development
- `start` is now for production server
