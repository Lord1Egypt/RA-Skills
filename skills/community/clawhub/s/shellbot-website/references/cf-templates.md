# Cloudflare Workers Templates

All templates are used via:
```bash
npm create cloudflare@latest -- <project-name> --template=cloudflare/templates/<template-name>
```

Or with the `create-project.sh` script using short names.

## Fullstack

| Short Name | Template | Description |
|------------|----------|-------------|
| `react-hono` | `react-router-hono-fullstack-template` | React Router 7 + Hono API server. **Default template.** |
| `next` | `next-starter-template` | Next.js on CF Workers via OpenNext |
| `remix` | `remix-starter-template` | Remix fullstack on Workers |
| `react-router` | `react-router-starter-template` | React Router 7 standalone |
| `react-postgres` | `react-postgres-fullstack-template` | React + PostgreSQL book library app |
| `saas-admin` | `saas-admin-template` | Admin dashboard with shadcn/ui components |

## Frontend / Static

| Short Name | Template | Description |
|------------|----------|-------------|
| `astro-blog` | `astro-blog-starter-template` | Astro blog/personal site |
| `vite-react` | `vite-react-template` | React SPA with Vite + Hono backend |
| `angular` | `angular-starter-template` | Angular on Workers |
| `nuxt` | `nuxt-starter-template` | Nuxt.js on Workers |
| `svelte` | `svelte-starter-template` | SvelteKit on Workers |
| `solid` | `solid-starter-template` | SolidStart on Workers |
| `qwik` | `qwik-starter-template` | Qwik City on Workers |

## API / Backend

| Short Name | Template | Description |
|------------|----------|-------------|
| `openauth` | `openauth-template` | OpenAuth server for authentication |
| `x402-proxy` | `x402-proxy-template` | Payment-gated transparent proxy with JWT |
| `platforms` | `workers-for-platforms-template` | Multi-tenant website hosting platform |
| `cron` | `cron-trigger-template` | Scheduled worker with cron triggers |

## Database / Storage

| Short Name | Template | Description |
|------------|----------|-------------|
| `d1` | `d1-template` | D1 SQL database starter |
| `r2-explorer` | `r2-explorer-template` | Google Drive-like interface for R2 buckets |
| `postgres` | `postgres-hyperdrive-template` | PostgreSQL via Hyperdrive |
| `mysql` | `mysql-hyperdrive-template` | MySQL via Hyperdrive |

## AI / ML

| Short Name | Template | Description |
|------------|----------|-------------|
| `llm-chat` | `llm-chat-app-template` | Chat app powered by Workers AI |
| `text-to-image` | `text-to-image-template` | Image generation from text prompts |
| `ai-rag` | `ai-rag-template` | RAG pipeline with Workers AI + Vectorize |

## Real-Time / Communication

| Short Name | Template | Description |
|------------|----------|-------------|
| `durable-chat` | `durable-chat-template` | Real-time chat with Durable Objects |
| `websocket` | `websocket-template` | WebSocket server on Workers |

## Containers / Advanced

| Short Name | Template | Description |
|------------|----------|-------------|
| `containers` | `containers-template` | Container-enabled Workers |

## Choosing a Template

**Building a fullstack web app?** → `react-hono` (default) or `next`
**Building a landing page or blog?** → `astro-blog`
**Building a SaaS dashboard?** → `saas-admin`
**Building an API?** → Start with a basic worker or `openauth` for auth
**Need a database?** → `d1` for SQLite, `postgres` for PostgreSQL
**Need object storage?** → `r2-explorer` for a UI, or add R2 binding to any template
**Building with AI?** → `llm-chat` or `text-to-image`
**Real-time features?** → `durable-chat` for Durable Objects + WebSockets

## Browse All Templates

Full list with live demos: https://developers.cloudflare.com/workers/get-started/quickstarts/
