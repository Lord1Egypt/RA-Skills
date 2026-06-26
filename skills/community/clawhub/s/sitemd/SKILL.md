---
name: sitemd
description: Build and manage websites from Markdown. Create pages, generate content, configure settings, and deploy — all through MCP tools.
homepage: https://sitemd.cc
metadata:
  openclaw:
    primaryEnv: SITEMD_TOKEN
---

# sitemd

Build websites from Markdown with MCP tools. Works as an OpenClaw skill or plugin — your agent can create, manage, and deploy websites through conversation.

## First Steps

1. **If no binary** (`sitemd/sitemd` does not exist) — run `./sitemd/install` to download it
2. Call `sitemd_status` to understand the project state
3. **If fresh project** — read files in `pages/`, then create pages with `sitemd_pages_create`
4. Call `sitemd_site_context` with a content type to get site identity, conventions, and existing pages
4. Validate with `sitemd_content_validate`
5. Deploy with `sitemd_deploy`

## Authentication

sitemd uses email magic links. When your owner needs to log in:

1. Call `sitemd_auth_login` — returns a browser URL
2. Send the URL to your owner as a message (WhatsApp, Telegram, Discord, etc.)
3. They tap the link and complete login in their browser
4. Call `sitemd_auth_poll` every few seconds until it returns `approved`

For automated deploys, use `sitemd_auth_api_key` to create a long-lived key, then set `SITEMD_TOKEN` in your environment.

## Project Structure

- `sitemd` — Compiled binary (run `./sitemd/sitemd launch`)
- `install` — Bootstrap script (run `./sitemd/install` to download binary)
- `pages/` — Markdown content files with YAML frontmatter
- `settings/` — Site configuration (YAML frontmatter in `.md` files)
- `theme/` — CSS and HTML templates
- `media/` — Images and assets
- `site/` — Built output

## MCP Tools

| Tool | Purpose |
|---|---|
| `sitemd_status` | Project state overview |
| `sitemd_pages_create` | Create new pages (writes file + nav + groups) |
| `sitemd_pages_create_batch` | Create multiple pages in one call |
| `sitemd_pages_delete` | Delete a page (cleans up nav + groups) |
| `sitemd_groups_add_pages` | Add pages to group sidebar |
| `sitemd_site_context` | Site identity, pages, conventions |
| `sitemd_content_validate` | Validate content quality |
| `sitemd_seo_audit` | SEO health check with scored report |
| `sitemd_init` | Initialize project from template |
| `sitemd_build` | Build without deploying |
| `sitemd_deploy` | Build and deploy site |
| `sitemd_activate` | Activate site (permanent) |
| `sitemd_clone` | Clone an existing website |
| `sitemd_config_set` | Set backend config (routes secrets vs non-secrets) |
| `sitemd_auth_login` | Start login flow |
| `sitemd_auth_poll` | Poll for login completion |
| `sitemd_auth_status` | Check auth state and license info |
| `sitemd_auth_api_key` | Create API key for automation |
| `sitemd_auth_setup` | Enable user authentication |
| `sitemd_update_check` | Check for updates |
| `sitemd_update_apply` | Apply updates |

Read pages, settings, and groups files directly — no MCP tool needed for reads.

## Settings Files

All configuration is in `settings/*.md` frontmatter:

| File | Controls |
|---|---|
| meta.md | Site title, brand name, description, URL |
| header.md | Navigation items, brand display, search |
| footer.md | Footer links, copyright, social |
| groups.md | Page groups for sidebars and dropdowns |
| theme.md | Colors, fonts, layout, light/dark/paper modes |
| build.md | Dev server port, output directory |
| deploy.md | Domain, deploy target |
| seo.md | OG images, sitemaps, structured data |

## Content Types

sitemd supports structured content generation. Call `sitemd_site_context` with a type to get conventions and existing pages. The syntax reference is below.

- **page** — General pages. Second person, present tense, lead with reader value.
- **docs** — Documentation. Imperative mood, show what to type, code blocks, tables.
- **blog** — Blog posts. Opinionated, date line, 400-1200 words.
- **changelog** — Release notes. Terse, Added/Changed/Fixed/Removed sections.
- **roadmap** — Product roadmap. Shipped/In Progress/Planned sections.

## Markdown Extensions

Beyond standard markdown, sitemd supports rich components. The syntax reference is below.

- `button: Label: /slug` — styled buttons. Modifiers: `+outline`, `+big`, `+newtab`, `+color:red`
- `card: Title` / `card-text:` / `card-image:` / `card-link:` — responsive card grids
- `embed: URL` — auto-detects YouTube, Vimeo, Spotify, X, CodePen, etc.
- `gallery:` with indented `![alt](url)` — image grid with lightbox
- `image-row:` with indented `![alt](url)` — equal-height image row
- `![alt](url +width:N +circle +bw +expand)` — image modifiers
- `[text]{tooltip content}` — inline tooltips
- `modal: id` with indented content, trigger via `[link](#modal:id)` — modal dialogs
- `{#custom-id}` — inline anchors
- `[text](url+newtab)` — link modifiers
- `form:` with indented YAML — forms
- `gated: type1, type2` ... `/gated` — gated sections
- `data: source` / `data-display: cards|list|table` — dynamic data