---
name: website-manager
description: Create, recreate, redesign, publish, and operate websites managed from Notion, including blogs, CMS-driven sections, widgets, filtering/search interactions, SEO/AEO/GEO improvements, and lightweight deployment workflows. Use when a user wants one skill that can both build and manage a website over time, with OpenClaw-friendly automation but no hard dependency on OpenClaw-specific tooling.
homepage: https://docs.openclaw.ai/tools/skills
metadata:
  {
    "openclaw":
      {
        "skillKey": "website-manager",
        "emoji": "🌐",
        "primaryEnv": "NOTION_ACCESS_TOKEN",
        "notes":
          "Credentials are conditional. Only request Notion or Netlify env vars when the user explicitly wants automated CMS provisioning, sync, or deploys.",
      },
  }
runtime_metadata:
  primary_credentials:
    - NOTION_ACCESS_TOKEN
    - NETLIFY_AUTH_TOKEN
  optional_env_vars:
    - NOTION_ACCESS_TOKEN
    - NOTION_TOKEN
    - NOTION_PARENT_PAGE_ID
    - NETLIFY_AUTH_TOKEN
    - NETLIFY_SITE_ID
    - NETLIFY_ACCOUNT_SLUG
    - NETLIFY_SITE_NAME
  conditional_env_vars:
    planning_only: []
    notion_cms_provisioning:
      - NOTION_ACCESS_TOKEN
      - NOTION_TOKEN
      - NOTION_PARENT_PAGE_ID
    notion_cms_sync:
      - NOTION_ACCESS_TOKEN
      - NOTION_TOKEN
      - NOTION_PARENT_PAGE_ID
    netlify_existing_site_deploy:
      - NETLIFY_AUTH_TOKEN
      - NETLIFY_SITE_ID
    netlify_new_site_deploy:
      - NETLIFY_AUTH_TOKEN
      - NETLIFY_ACCOUNT_SLUG
      - NETLIFY_SITE_NAME
  credential_scope_guidance:
    - Use a Notion internal integration scoped only to the shared parent page used for CMS creation and sync.
    - Use the least-privileged Netlify token that can create deploys for the intended site or account.
    - Do not provide Notion or Netlify credentials for blueprinting, planning, or validation-only runs.
  local_runtime_outputs:
    - .website-manager/notion.json
    - .website-manager/deploy.json
  privileged_operations:
    - outbound_network_requests
    - persistent_file_writes
    - remote_deploys
---

# Website Manager

## Overview

Use this skill when the user wants one workflow that covers both website creation and ongoing website management.

This skill is for:
- rebuilding or redesigning an existing website
- creating a new website starter
- adding or refining pages, widgets, and blog/CMS features
- managing content from Notion
- improving SEO, schema, internal linking, filtering, and discoverability
- setting up lightweight publishing and recurring upkeep

Keep the output portable. The site should not become locked to one host or one agent platform unless the user explicitly asks for that.

## Credentials

Core website planning, content modeling, blueprint generation, and validation do not require secrets.

Automated Notion CMS creation and sync do require:
- `NOTION_ACCESS_TOKEN` or `NOTION_TOKEN`
- `NOTION_PARENT_PAGE_ID` for the shared parent page where the CMS will be created

Automated Netlify deploys do require:
- `NETLIFY_AUTH_TOKEN`
- optional `NETLIFY_SITE_ID` when deploying to an existing site

Credential rule:
- only request these values when the user wants automated CMS creation, CMS sync, or automated deploys
- prefer `NOTION_ACCESS_TOKEN` as the canonical variable name and treat `NOTION_TOKEN` as a compatible fallback
- for Notion, share a single parent page with the integration and create the CMS as child databases/pages beneath it
- prefer the least-privileged Netlify token that can create deploys for the target site
- do not assume these env vars exist just because the skill is installed
- if `NETLIFY_SITE_ID` is missing, the deploy helper may create a new Netlify site automatically and persist the returned non-secret site identifiers
- never store secrets in Notion or repo files; only store non-secret IDs and URLs
- if the user only wants planning, blueprinting, content modeling, or validation, do not request any secrets

## Persisted Files

The helper scripts may write non-secret runtime metadata to local JSON files.

Default locations:
- `.website-manager/notion.json`
- `.website-manager/deploy.json`

Storage rule:
- review these files before committing or syncing them anywhere
- they should contain IDs and URLs, not secrets
- keep them local by default unless you intentionally want them in your project workflow

Read as needed:
- `references/default-stack.md` first for the opinionated baseline this skill should assume
- `references/site-types/*.md` for visual direction and default token choices; use `generic.md` as the fallback when no specialized type clearly fits
- `references/seo-aeo-geo.md` for metadata, schema, FAQ, and local SEO rules
- `references/widgets-and-interactions.md` for widgets, filtering, search, pagination, and collection UX
- `references/notion-cms-model.md` for the Notion database structure
- `references/deployment-shapes.md` for site architecture choices
- `references/hosting-decision.md` when choosing where and how to deploy
- `references/openclaw-automation.md` when recurring upkeep is needed in OpenClaw

Use the helper scripts when useful:
- `scripts/generate_blueprint.py` to generate the default site/CMS/publish blueprint
- `scripts/create_notion_cms.py` to create the default Notion CMS under a shared parent page
- `scripts/netlify_zip_deploy.py` to deploy a finished site to Netlify with the opinionated zip workflow

## When To Use It

Use this skill when the user asks to:
- recreate, clone, redesign, or migrate a website
- create or improve a blog or CMS-driven site
- manage website content in Notion
- add widgets, filters, searchable listings, or other light interactivity
- publish changes or set up a low-friction hosting flow
- run recurring SEO or content-maintenance tasks

## Workflow

### Default assumptions

Unless the user explicitly says otherwise, assume this stack:
- plain HTML/CSS/JS or a very light static templating setup
- Notion as the CMS
- one shared page shell and one shared token system
- Netlify as the default host
- GitHub optional, not required
- one blog or collection listing pattern with category chips, search, featured items, and pagination

If the user is vague, do not ask them to choose among many architectures. Start from the default stack and only deviate when the site clearly needs it.

### 1) Understand the site and operating model

Start by identifying:
- whether the site is new or based on an existing live site
- the key page types
- the conversion paths
- what should be static versus CMS-driven
- whether the user is solo/non-technical or working with developers

If rebuilding an existing site:
- extract the route map from `sitemap.xml` first
- if no sitemap exists, crawl homepage links up to two levels deep
- classify URLs as `core`, `blog`, `collection`, `embed`, `utility`, `external`, or `skip`

### 2) Choose the implementation shape

Default implementation:
- plain HTML/CSS/JS for small to medium brochure and editorial sites

Use a lightweight static generator or templating layer when there are:
- repeated page layouts
- CMS-backed collections
- listing pages with tags, categories, or filters
- shared article or service templates

Avoid unnecessary framework weight when the user mainly needs:
- easy editing
- low-friction deployment
- simple maintenance

If there is no strong reason to do otherwise, keep:
- one listing template for posts or collection items
- one detail template for posts or collection items
- one site settings source from Notion
- one deployment target

### 3) Lock the shared system once

Define one shared system before generating pages:
- design tokens
- typography
- nav/footer
- responsive grid rules
- card/listing system
- interaction patterns for filters, search, and widgets

Do not redesign each page from scratch.

### 4) Build the core site

Generate in this order:
1. shared shell and tokens
2. homepage
3. service/category hub pages
4. individual detail pages
5. about/contact/trust pages
6. blog or collection listing pages
7. article/detail templates
8. booking/form wrapper pages
9. utility pages such as `404`

### 5) Add widgets and interaction deliberately

Use widgets only when they help the user complete a real task.

Examples:
- booking CTA bars
- opening hours widgets
- maps
- testimonial rails
- newsletter signup blocks
- blog/category filters
- searchable content lists
- pagination or load-more patterns

When building listings, always account for:
- filtering
- empty states
- no-results states
- mobile behavior
- deep-linking or URL-based filter state when useful

Default listing behavior:
- featured section first when featured items exist
- category chips directly under the listing intro
- search input matching title, excerpt, category, and tags
- pagination at 9 items per page by default
- URL query params for search and category when the site has more than a trivial number of posts/items
- reset control whenever filters are active

### 6) Model content in Notion

Use Notion as the editorial source of truth when the user wants a CMS without a custom admin panel.

Typical Notion databases:
- Pages
- Services or Collections
- Blog Posts
- Site Settings

Default database names:
- `Pages`
- `Collections`
- `Blog Posts`
- `Site Settings`

Keep code responsible for layout and rendering.
Keep Notion responsible for content and configuration.

### 7) Choose live versus rebuild behavior

Use rebuild mode for:
- homepage sections
- footer details
- navigation
- site settings
- service pages baked into templates

Use live CMS-backed mode for:
- blog/article listings
- article detail pages
- lightweight collections where server-side fetches are worthwhile

### 8) Bake in SEO / AEO / GEO

Every page should have:
- unique title
- unique meta description
- canonical URL
- valid schema
- clear answer-first content
- internal-link support to nearby pages and related content

Service and editorial pages should include:
- FAQ or answer blocks where appropriate
- local signals when the business is location-aware
- related-content links to improve crawl paths and usability

### 9) Validate before handoff or deploy

Run:

```bash
python3 scripts/validate_links.py ./site-output original-domain.com
python3 scripts/validate_links.py ./site-output original-domain.com --fix
```

The site is not complete until it passes with zero errors.

### 10) Deploy with the lightest workable path

Default hosting recommendation:
- Netlify for non-technical operators and sites that may later need serverless helpers

Optional:
- GitHub when the user wants previews, reviews, or collaboration
- another host when the user already has a strong platform preference

Default deploy workflow:
1. build or prepare the site locally
2. validate links and metadata
3. zip deploy to Netlify
4. only add GitHub later if collaboration demands it

### 11) Automate recurring upkeep

Good recurring jobs:
- broken-link scans
- metadata checks
- sitemap refreshes
- weekly publish queues
- monthly content health reviews
- recurring SEO and internal-link audits

If OpenClaw is available, prefer native cron jobs.
If not, use another scheduler without changing the content workflow.

## Hard Rules

- Never leave recreated internal pages pointing back to the original domain.
- Never hardcode secrets into HTML, scripts, or Notion content.
- Never recreate payment, auth, checkout, or regulated intake flows unless explicitly asked.
- Never force GitHub on a non-technical solo operator.
- Never treat hosting as the CMS.
- Always design listing pages with filtering, empty states, and mobile behavior in mind.
- Keep the site portable first, then adapt it for the chosen host.
- Default to the opinionated stack unless the user gives a concrete reason to diverge.

## Output Contract

Return:
1. the site map or content model
2. what is static versus CMS-driven
3. the implementation shape and hosting recommendation
4. the rebuilt or updated pages/components
5. the widget and interaction behavior
6. the validation result
7. any follow-up publish or automation steps
