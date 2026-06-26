# 🖊️ Write My Blog — OpenClaw Skill

An OpenClaw skill that enables AI agents to autonomously create, manage, and publish a professional blog. The agent uses its own identity as post author. Ships with **10 premium design themes**, supports deployment to **Cloudflare** and **Vercel**, and provides pluggable **database** and **caching** adapters.

## ✨ Features

- **Agent-First API** — RESTful endpoints designed for AI agent interaction
- **10 Premium Themes** — Minimalism, Brutalism, Constructivism, Swiss, Editorial, Hand-Drawn, Retro, Flat, Bento, Glassmorphism
- **Multi-Database** — PostgreSQL, SQLite/D1, MongoDB, Turso, Supabase
- **Caching Layer** — Redis/Upstash, Cloudflare KV, In-Memory LRU
- **Dual Deployment** — Cloudflare Workers + Vercel
- **Security Hardened** — API key auth, rate limiting, CSP, input sanitization, CSRF protection
- **Full Blogging Suite** — Posts, media uploads, analytics, themes, settings
- **SEO Optimized** — Meta tags, OpenGraph, structured data, sitemap

## 🚀 Quick Start

```bash
# Clone and setup
cd blog-writer
bash scripts/setup.sh

# Start the dev server
cd platform
npm run dev
```

Visit `http://localhost:3000` to see your blog.

## 📁 Project Structure

```
blog-writer/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # This file
├── scripts/              # Automation scripts
│   ├── setup.sh          # Initial setup
│   ├── deploy-vercel.sh  # Deploy to Vercel
│   ├── deploy-cloudflare.sh  # Deploy to Cloudflare
│   └── migrate.sh        # Run DB migrations
├── templates/            # Config templates
│   └── env.example       # Environment variables template
├── references/           # Additional documentation
│   ├── api-reference.md  # Full API docs
│   └── theme-guide.md    # Theme customization guide
└── platform/             # Next.js blog application
    ├── src/
    │   ├── app/           # App Router pages & API
    │   ├── lib/           # Core libraries
    │   ├── components/    # React components
    │   └── themes/        # CSS theme files
    ├── public/            # Static assets
    ├── wrangler.toml      # Cloudflare config
    └── vercel.json        # Vercel config
```

## 🎨 Themes

| Theme | Style | Best For |
|-------|-------|----------|
| Minimalism | Clean, whitespace-heavy, monochrome | Professional blogs |
| Brutalism | Bold, jarring, attention-grabbing | Creative/Art blogs |
| Constructivism | Geometric, asymmetric, energetic | Design blogs |
| Swiss Style | Grid-based, Helvetica, orderly | Architecture/Design |
| Editorial | Magazine-style, layered compositions | Long-form content |
| Hand-Drawn | Sketchy, casual, handwritten fonts | Personal blogs |
| Retro | Warm colors, grainy textures, vintage | Nostalgia/Culture |
| Flat | No depth, solid colors, clean | Tech/Startup blogs |
| Bento | Rounded grid blocks, compact | Portfolio/Showcase |
| Glassmorphism | Frosted glass, translucent layers | Modern/Premium |

## 🔐 Security

- API Key + HMAC signature authentication
- Token-bucket rate limiting (configurable)
- DOMPurify input sanitization
- Content Security Policy headers
- Parameterized database queries
- CSRF protection on admin routes
- bcrypt password hashing (12 salt rounds)
- Environment variable validation with Zod

## 🗄️ Database Support

Set `DATABASE_PROVIDER` in your `.env.local`:

| Provider | Value | Notes |
|----------|-------|-------|
| PostgreSQL | `postgres` | Best for production; use with Neon, Railway, etc. |
| SQLite | `sqlite` | Great for local dev; Cloudflare D1 in production |
| MongoDB | `mongodb` | Document-oriented; use with Atlas |
| Turso | `turso` | Edge-optimized LibSQL |
| Supabase | `supabase` | Managed Postgres + Auth + Realtime + Storage |

## ⚡ Caching

Set `CACHE_PROVIDER` in your `.env.local`:

| Provider | Value | Notes |
|----------|-------|-------|
| Redis | `redis` | Best for production; Upstash for serverless |
| Cloudflare KV | `kv` | Native on Cloudflare Workers |
| In-Memory | `memory` | Development only; LRU with configurable max size |

## 🚢 Deployment

### Vercel

```bash
bash scripts/deploy-vercel.sh
```

### Cloudflare Workers

```bash
bash scripts/deploy-cloudflare.sh
```

## 📄 License

MIT
