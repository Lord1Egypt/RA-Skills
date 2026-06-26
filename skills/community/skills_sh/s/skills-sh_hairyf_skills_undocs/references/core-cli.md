---
name: undocs-cli
description: Use the undocs CLI to develop and build documentation sites
---

# Undocs CLI

The undocs CLI provides commands to develop and build documentation sites.

## Installation

The CLI is included when you install undocs:

```bash
npm install -D undocs
# or
pnpm add -D undocs
# or
yarn add -D undocs
```

## Commands

### Development Server

Start the development server:

```bash
npx undocs dev [dir]
```

- `dir` (optional): Documentation directory (defaults to current directory)
- Starts a Nuxt dev server on port 4000 (or `PORT` environment variable)
- Supports hot module replacement (HMR) for configuration changes
- Watches for changes in documentation files

### Build

Build static documentation for production:

```bash
npx undocs build [dir]
```

- `dir` (optional): Documentation directory (defaults to current directory)
- Generates a static site in `.output/public/`
- Requires `url` configuration for production builds (for SEO)

## Configuration HMR

The CLI supports hot module replacement for configuration changes:

- Changes to `description`, `shortDescription`, and `landing` trigger fast reload
- Other configuration changes trigger a full Nuxt restart
- Configuration is watched automatically in development mode

## Environment Variables

- `PORT`: Port number for development server (default: 4000)
- `NUXT_DOCS_DEV`: Set to `1` to enable development mode
- `NUXT_PUBLIC_SITE_URL`: Site URL (auto-inferred from deployment platform)

## Key Points

- The CLI automatically sets up Nuxt configuration
- No manual Nuxt config needed - everything is handled by undocs
- Branch detection is automatic (from git or environment variables)
- Site URL is inferred from deployment platform environment variables

<!--
Source references:
- https://github.com/unjs/undocs/tree/main/cli
-->
