# Sage Router Landing Page Deployment

## Hosting decision

Frontend hosting decision: use Cloudflare Pages for the static marketing site, especially while the free tier is sufficient. Keep backend/control plane decisions separate from the static frontend.


Static frontend for `sagerouter.dev`.

## Local preview

```bash
cd web
npm install
npm run dev
```

Production build:

```bash
cd web
npm run build
npm run preview
```

Build output is written to `web/dist`.

For production, prefer the repo-level deploy helper:

```bash
set -a; source /home/digit/.openclaw/.env; set +a
scripts/deploy_sagerouter_public.sh
```

The helper deploys Cloudflare Pages to production branch `main`. Deploying this
repo's `master` branch with Wrangler creates a preview deployment only, so do
not use `--branch master` for the live `sagerouter.dev` custom domains.
It also compiles `web/functions` into `dist/_worker.js` and `dist/_routes.json`
before upload so `/api/waitlist` is served by the Pages Function instead of the
static app shell.

## Recommended deploy path: Cloudflare Pages

Use Cloudflare Pages for the marketing site and keep the router service separate.

Cloudflare Pages settings:

- Project name: `sage-router-web`
- Production branch: `main`
- Root directory: `web`
- Build command: `npm ci && npm run build`
- Build output directory: `dist`
- Custom domain: `sagerouter.dev`
- Function env vars for waitlist and funnel-event capture: `SAGEROUTER_SUPABASE_URL` and `SAGEROUTER_SUPABASE_SERVICE_ROLE`
- Optional exact-origin overrides for public insert guards: `SAGEROUTER_WAITLIST_ALLOWED_ORIGINS` and `SAGEROUTER_FUNNEL_ALLOWED_ORIGINS`
- Optional Cloudflare Turnstile waitlist guard: set both `SAGEROUTER_TURNSTILE_SECRET_KEY` and `SAGEROUTER_TURNSTILE_SITE_KEY`

Waitlist and funnel-event writes require an explicit trusted `Origin`; `Referer`
is stored only as sanitized attribution metadata and is not accepted as a write
authorization fallback.

Do not deploy the Python router service or any local provider credentials to Pages. This site is static marketing/docs content only.

## DNS

After the Pages project exists, attach:

- `sagerouter.dev`
- optionally `www.sagerouter.dev`

Let Cloudflare manage the required CNAME/flattened records.

## Deployment phases

### Phase 1 — Static site foundation (complete)

- [x] Cloudflare Pages project: `sage-router-web`
- [x] Custom domain: `https://sagerouter.dev`
- [x] Canonical URL set to `https://sagerouter.dev/`
- [x] `robots.txt`, `sitemap.xml`, `llms.txt`, and `llms-full.txt` reachable at site root
- [x] Waitlist form wired to AOps Supabase via Cloudflare Pages Function
- [x] Browser-origin write guard and optional Turnstile abuse guard supported for the public waitlist form

### Phase 2 — Public launch polish (in progress)

- [x] GitHub repo homepage points back to `https://sagerouter.dev/`
- [x] GitHub repo description/topics configured for discovery
- [x] Integration guide pages published for Codex, Claude Code, OpenClaw, Hermes, Pi agents, Cursor, Aider, Continue, OpenHands, Ollama / Ollama Cloud, NVIDIA NIM, OpenAI-compatible clients, Anthropic-compatible clients, and harness fallback
- [x] Public sitemap ping endpoints checked (Google deprecated, Bing returned gone)
- [ ] Submit sitemap in Google Search Console / Bing Webmaster Tools dashboards
- [ ] Confirm indexing in Google Search Console / Bing Webmaster Tools dashboards

### Phase 3 — Hosted reliability layer (future)

- [ ] Architecture review for key custody and customer data boundaries
- [ ] Hosted health/observability control plane design
- [ ] Optional managed router deployment path

## Deployment boundary

The landing page must not include provider API keys, user credentials, systemd environment files, or router runtime config.

Hosted Sage Router infra, if added later, should be a separate service with explicit architecture review for key custody and customer data boundaries.
