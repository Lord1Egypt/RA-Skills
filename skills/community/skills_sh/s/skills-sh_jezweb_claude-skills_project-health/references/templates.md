# Templates

Templates for CLAUDE.md files, rules topic files, sub-directory context, and .gitignore. Use these when creating new files or restructuring existing ones.

---

## Root CLAUDE.md (Minimal)

For simple projects with a single developer:

```markdown
# [Project Name]

[One-line description]

## Stack

[Tech stack summary]

## Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run deploy` | Deploy to [platform] |

## Gotchas

- [Non-obvious thing 1]
- [Non-obvious thing 2]
```

Target: 30-60 lines.

## Root CLAUDE.md (Comprehensive)

For projects with external integrations, multiple contributors, or complex workflows:

```markdown
# [Project Name]

**Repository**: [URL]
**Owner**: [Name]

[One-line description]

## Stack

[Tech stack with key decisions noted]

## Directory Structure

[Annotated tree of key directories]

## Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run deploy` | Deploy to [platform] |
| `npm test` | Run test suite |

## Key Files

| File | Purpose |
|------|---------|
| `src/index.ts` | Entry point |
| `wrangler.jsonc` | Cloudflare config |

## Critical Rules

- [Never do X because Y]
- [Always do A before B]

## Gotchas

- [Non-obvious thing 1]
- [Non-obvious thing 2]
```

Target: 60-150 lines.

---

## Project-Type Templates

### Cloudflare Worker

```markdown
# [Project Name]

**Repository**: https://github.com/[org]/[repo-name]
**Last Updated**: [date]

## Stack

- Cloudflare Workers + Static Assets
- Vite + React 19 + @cloudflare/vite-plugin
- Tailwind v4 + shadcn/ui (neutral palette)
- D1 (SQLite) + Drizzle ORM
- Hono (API routing)
- pnpm

## Commands

| Command | Purpose |
|---------|---------|
| `pnpm dev` | Local dev server (Vite + Miniflare) |
| `pnpm build` | Production build |
| `pnpm deploy` | Deploy to Cloudflare |
| `pnpm db:migrate:local` | Run D1 migrations locally |
| `pnpm db:migrate:remote` | Run D1 migrations on production |

## Cloudflare

- **Compatibility flags**: `nodejs_compat` (never use `node_compat`)
- Always use Workers + Static Assets (never Cloudflare Pages)

## Critical Rules

- Run migrations on BOTH local AND remote before testing
- Set `account_id` in wrangler.jsonc to avoid interactive prompts
- D1 bulk inserts: batch into chunks of ~10 rows (parameter limit)
- `wrangler secret put` does NOT auto-deploy — run `wrangler deploy` after

## Gotchas

[Add as discovered]
```

### Vercel App

```markdown
# [Project Name]

**Repository**: https://github.com/[org]/[repo-name]
**Last Updated**: [date]

## Stack

- Next.js / Vite + React 19
- Tailwind v4 + shadcn/ui (neutral palette)
- pnpm

## Commands

| Command | Purpose |
|---------|---------|
| `pnpm dev` | Local dev server |
| `pnpm build` | Production build |
| `vercel deploy` | Deploy to Vercel |
| `vercel deploy --prod` | Deploy to production |

## Gotchas

[Add as discovered]
```

### Node Generic

```markdown
# [Project Name]

**Repository**: https://github.com/[org]/[repo-name]
**Last Updated**: [date]

## Stack

- Node.js + TypeScript (ES modules)
- pnpm

## Commands

| Command | Purpose |
|---------|---------|
| `pnpm dev` | Local dev server |
| `pnpm build` | Production build |
| `pnpm test` | Run tests |

## Gotchas

[Add as discovered]
```

### Python

```markdown
# [Project Name]

**Repository**: https://github.com/[org]/[repo-name]
**Last Updated**: [date]

## Stack

- Python 3.12+
- uv (package management)

## Commands

| Command | Purpose |
|---------|---------|
| `uv run python main.py` | Run the application |
| `uv sync` | Install dependencies |
| `uv run pytest` | Run tests |

## Gotchas

[Add as discovered]
```

### Ops / Admin (Claude Code Plugin)

```markdown
# [Project Name]

**Repository**: https://github.com/[org]/[repo-name]
**Last Updated**: [date]

## Purpose

[What this operational project does]

## MCP Servers

| Server | Purpose |
|--------|---------|
| [server] | [what it does] |

## Gotchas

[Add as discovered]
```

---

## Sub-Directory CLAUDE.md

For directories with external integrations, non-obvious config, or common gotchas:

```markdown
# [Component Name]

## Key Integrations

- **[Service]**: [endpoint], [auth method], [secret location]

## Commands

[Directory-specific commands if different from root]

## Gotchas

- [Non-obvious thing specific to this directory]
```

Target: 15-50 lines.

**Don't create when**: parent CLAUDE.md covers it, directory is self-explanatory, content would be under 10 lines.

## Rules Topic File (.claude/rules/*.md)

For correction rules, patterns, and technical facts:

```markdown
# [Topic Name]

## [Pattern/Rule Category]

| If Claude suggests... | Use instead... |
|----------------------|----------------|
| [Wrong pattern] | [Correct pattern] |

[Code example if helpful]

**Last Updated**: [date]
```

Target: 20-80 lines per topic file.

---

## Section Placement Guide

| Content Type | Where It Goes |
|-------------|---------------|
| Project name, owner, purpose | Root CLAUDE.md |
| Tech stack, architecture overview | Root CLAUDE.md |
| Build/deploy/test commands | Root CLAUDE.md |
| Critical "never do X" rules | Root CLAUDE.md |
| Directory structure | Root CLAUDE.md |
| External service integrations | Sub-directory CLAUDE.md |
| Directory-specific gotchas | Sub-directory CLAUDE.md |
| Correction rules (training cutoff) | `.claude/rules/<topic>.md` |
| Session-specific discoveries | Auto-memory (managed by Claude Code) |

## Anti-Patterns

- Verbose explanations of standard tools or frameworks
- Changelogs or version history (use git)
- Content Claude already knows from training
- Duplicating parent CLAUDE.md content in child files
- Generic best practices not specific to the project
- Empty template sections with placeholder text

---

## .gitignore Templates

### Cloudflare Worker / Node

```
node_modules/
.wrangler/
dist/
.dev.vars
*.log
.DS_Store
.env
.env.local
.claude/settings.local.json
.claude/plans/
.jez/screenshots/
.jez/artifacts/
```

### Python

```
__pycache__/
*.pyc
.venv/
dist/
*.egg-info/
.env
.env.local
.DS_Store
.claude/settings.local.json
.claude/plans/
.jez/screenshots/
.jez/artifacts/
```

### Ops / Admin

```
.DS_Store
.env
.env.local
.claude/settings.local.json
.claude/plans/
.jez/screenshots/
.jez/artifacts/
```

### PHP / WordPress

```
vendor/
node_modules/
*.log
.DS_Store
.env
.env.local
.claude/settings.local.json
.claude/plans/
.jez/screenshots/
.jez/artifacts/
```

### Go

```
bin/
*.exe
*.test
*.out
.DS_Store
.env
.claude/settings.local.json
.claude/plans/
.jez/screenshots/
.jez/artifacts/
```

### Rust

```
target/
Cargo.lock
.DS_Store
.env
.claude/settings.local.json
.claude/plans/
.jez/screenshots/
.jez/artifacts/
```
