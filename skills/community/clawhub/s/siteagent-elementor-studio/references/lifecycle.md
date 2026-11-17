# Studio lifecycle — where the Elementor build fits

The Elementor build is one stage of the studio toolbox. Hand off cleanly to the neighbours.

| Stage | Tool | Use it for |
|---|---|---|
| **Audit** (pre-sale / onboarding) | `wordpress-api-pro` → `site_audit.py` | No-auth Tier-1 scan of a prospect/client site (CMS, SEO, headers, SSL, PageSpeed) before proposing a build. |
| **Content / commerce** | `wordpress-api-pro` (WP REST) | Seed posts/pages/CPTs, media, WooCommerce products, SEO meta, ACF/JetEngine fields — before or alongside the Elementor build. |
| **Build** (this skill) | the fork `elementor-mcp` | Design + build pages/templates in Elementor. |
| **Host** | `cloudways-mcp` / `hostinger-mcp` | Provision/monitor/maintain the server the site runs on; SSL/cache/backups (Cloudways UI/API for SSL — not an MCP tool). |
| **Ads** | `meta-ads-mcp` | Launch/manage the campaign that drives traffic to the built site. |

## Handoffs

- **Audit → Build:** run `site_audit.py` first; its findings (CMS, theme, current builder, SEO gaps) scope the build brief and tell you whether Elementor/Pro is even present.
- **Build → Content:** use `wordpress-api-pro` to populate real content into the structures you built (drafts-first, dry-run for bulk).
- **Build → Host:** confirm the target server in `cloudways-mcp`/`hostinger-mcp`; clear cache after a deploy; never leave the MCP build plugins active on production.

## "Where am I?" router

- Prospect, no site access yet → **Audit** (`site_audit.py`).
- Site access, needs pages → **Build** (here).
- Pages built, needs real content/products → **Content** (`wordpress-api-pro`).
- Site done, needs server ops/SSL/cache → **Host** (`cloudways-mcp`/`hostinger-mcp`).
- Site live, needs traffic → **Ads** (`meta-ads-mcp`).
