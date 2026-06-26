# Project Types

Detect project type from file presence to determine which documentation files are expected. Only suggest docs that match — no enterprise bloat.

## Detection Heuristics

Check indicators in priority order (first match wins for primary type, but types can stack):

| Indicator Files | Project Type | Permission Preset |
|----------------|-------------|-------------------|
| `wrangler.jsonc` or `wrangler.toml` | cloudflare-worker | JS/TS + Cloudflare Worker |
| `vite.config.*` + `src/` with `.tsx` files | vite-react | JS/TS |
| `vite.config.*` without React | vite-app | JS/TS |
| `next.config.*` | nextjs | JS/TS + Vercel |
| `astro.config.*` | astro | JS/TS + Static Site Generators |
| `src/index.ts` + `FastMCP` or `McpAgent` imports | mcp-server | JS/TS |
| `skills/` dir + SKILL.md files within | skills-repo | — |
| `src/routes/` or `src/api/` or `app/api/` | api-project | (from parent type) |
| `drizzle.config.*` or `prisma/schema.prisma` or D1 bindings in wrangler | database-project | Database |
| `.claude/agents/` + operational scripts | claude-ops | — |
| `package.json` only (generic Node) | node-project | JS/TS |
| `pyproject.toml` or `setup.py` or `requirements.txt` | python-project | Python |
| `Cargo.toml` | rust-project | Rust |
| `go.mod` | go-project | Go |
| `Gemfile` or `Rakefile` | ruby-project | Ruby |
| `composer.json` or `wp-config.php` | php-project | PHP |
| `pom.xml` or `build.gradle` or `build.gradle.kts` | java-project | Java/JVM |
| `*.sln` or `*.csproj` or `global.json` | dotnet-project | .NET |
| `mix.exs` | elixir-project | Elixir |
| `Package.swift` | swift-project | Swift + macOS |
| `Dockerfile` or `docker-compose.yml` | docker | Docker |
| `fly.toml` | fly-deployment | Hosting Platforms |
| `railway.json` or `railway.toml` | railway-deployment | Hosting Platforms |
| `netlify.toml` | netlify-deployment | Hosting Platforms |
| `vercel.json` | vercel-deployment | Vercel |
| `supabase/config.toml` | supabase-project | Hosting Platforms + Database |
| `hugo.toml` or `hugo.yaml` | hugo | Static Site Generators |
| `pubspec.yaml` | flutter-project | Mobile Development |

**Stacking**: A Cloudflare Worker with D1 bindings is both `cloudflare-worker` and `database-project`. Union the expected docs.

## Expected Documentation Per Type

### All projects

| Doc | Purpose |
|-----|---------|
| `CLAUDE.md` (root) | Project identity, stack, commands, critical rules |

### cloudflare-worker

| Doc | Purpose |
|-----|---------|
| `ARCHITECTURE.md` | Worker entry point, bindings, routes, middleware |

### vite-react / nextjs

| Doc | Purpose |
|-----|---------|
| `ARCHITECTURE.md` | Component tree, routing, state management, build pipeline |

### mcp-server

| Doc | Purpose |
|-----|---------|
| `ARCHITECTURE.md` | Server structure, tool registration, auth flow |
| `API_ENDPOINTS.md` | Tool catalogue with parameters and return types |

### api-project

| Doc | Purpose |
|-----|---------|
| `API_ENDPOINTS.md` | Routes, methods, request/response schemas, auth requirements |
| `DATABASE_SCHEMA.md` | Tables, relationships, indexes, migration workflow |

### database-project

| Doc | Purpose |
|-----|---------|
| `DATABASE_SCHEMA.md` | Tables, relationships, indexes, migration commands |

### skills-repo

| Doc | Purpose |
|-----|---------|
| Per-skill `SKILL.md` | Each skill directory needs its own SKILL.md |

### claude-ops

No additional docs beyond CLAUDE.md — operational repos are typically self-documenting through their agents and scripts.

## Doc Templates

### ARCHITECTURE.md outline

```markdown
# Architecture

## Overview
[One paragraph: what this project does and how it's structured]

## Stack
[Tech stack with versions]

## Directory Structure
[Tree with purpose annotations]

## Key Flows
[1-3 main data/request flows through the system]

## Deployment
[How to deploy, what happens on deploy]
```

### DATABASE_SCHEMA.md outline

```markdown
# Database Schema

## Tables
[Table per section: name, columns, types, constraints]

## Relationships
[Foreign keys, join patterns]

## Migrations
[How to create/run migrations, local vs remote]

## Indexes
[Non-obvious indexes and why they exist]
```

### API_ENDPOINTS.md outline

```markdown
# API Endpoints

## Authentication
[Auth method, where tokens come from]

## Endpoints
[Per endpoint: method, path, params, response shape, auth required]

## Error Handling
[Standard error format, common error codes]
```

## docs/ Directory

Projects with a `docs/` folder get its contents scanned for staleness and overlap with CLAUDE.md. Common patterns:

| Pattern | Example |
|---------|---------|
| Component docs | `docs/RICH_CONTENT_COMPONENTS.md` |
| API guides | `docs/api-guide.md` |
| Planning briefs | `docs/briefs/feature-x.md` |

The audit doesn't manage docs/ content — it flags staleness (broken file references) and overlap (sections duplicated with CLAUDE.md).

## Rules

- Only suggest docs that match detected project type
- Simple projects (node-project, python-project) just need CLAUDE.md
- Don't create empty template docs — only suggest when there's content to fill
- Prefer one well-maintained doc over three sparse ones
- If CLAUDE.md duplicates ARCHITECTURE.md or docs/, move the content to docs/ and keep CLAUDE.md concise
