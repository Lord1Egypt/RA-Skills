# WordPress Trade Site Builder

> OpenClaw interactive skill — AI agent guides you through 9 phases to deploy a production-ready WordPress site for international trade businesses.

## Overview

This skill wraps the [wordpress-trade-starter](https://github.com/iPythoning/wordpress-trade-starter) template into an interactive guided workflow. After installation, tell your OpenClaw agent "help me build a trade website" and it will walk you through the entire process:

| Phase | What It Does | Time |
|-------|-------------|------|
| 1. Business Info | Company name, products, target markets, languages, contacts | 2 min |
| 2. Server Setup | SSH connection, firewall, swap, timezone | 5 min |
| 3. Docker Deploy | Clone template, generate .env, launch 3 containers | 3 min |
| 4. SSL Certificate | Let's Encrypt or Cloudflare Origin certificate | 3 min |
| 5. WordPress Init | Setup wizard, wp-config, permalinks | 3 min |
| 6. Theme & Plugins | Astra + 9 recommended plugins batch install | 5 min |
| 7. Multilingual + SEO | Polylang languages, Rank Math SEO, base pages | 5 min |
| 8. Cloudflare + Perf | DNS, SSL/TLS, triple-layer cache, PageSpeed test | 5 min |
| 9. Security + Verify | File permissions, xmlrpc block, backup, monitoring | 5 min |

**~35 minutes total** from zero to a production-ready trade website.

## Architecture

```
                ┌─────────────┐
                │  Cloudflare  │  CDN + WAF + SSL
                └──────┬──────┘
                ┌──────▼──────┐
                │    Nginx     │  Reverse Proxy + Cache + Gzip
                └──────┬──────┘
                ┌──────▼──────┐
                │  WordPress   │  6.7 + Apache + Plugins
                └──────┬──────┘
                ┌──────▼──────┐
                │   MySQL 8    │  Persistent Volume
                └─────────────┘
```

## Install

```bash
clawhub install wordpress-trade-site
```

## Usage

After installation, tell your OpenClaw agent:

- "Help me build a trade website"
- "Deploy a WordPress B2B site"
- "Set up an international trade website"

The agent will automatically start the 9-phase guided deployment.

## Who Is This For

- **Trade companies** — Manufacturers, exporters, and trading companies building B2B websites
- **WordPress beginners** — Want a production-grade starting point
- **Developers** — Rapidly deploy WordPress sites for international clients

## Tech Stack

- Docker Compose (WordPress 6.7 + MySQL 8 + Nginx Alpine)
- Triple-layer cache (WP Super Cache + Nginx Proxy Cache + Cloudflare CDN)
- Auto WebP (Imagify + Nginx/Apache conditional serving)
- SEO-ready (Rank Math + Structured Data + XML Sitemap)
- Multilingual (Polylang — EN/ZH/RU/ES/FR/AR)

## Source

[iPythoning/wordpress-trade-starter](https://github.com/iPythoning/wordpress-trade-starter)

## License

MIT
