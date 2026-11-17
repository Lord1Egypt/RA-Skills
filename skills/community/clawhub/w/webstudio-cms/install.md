# Webstudio Install & Self-Hosting

How to set up and deploy Webstudio. Source: official docs (self-hosting, VPS with
Docker, CLI).

## Two separate things

The **Builder** (the tool you build in) and the **site** (the published project)
are hosted separately. You build in the Builder, then the site is deployed
independently.

- The Builder and generated sites are open-source.
- Self-hosting the **Builder** in production is harder and currently not recommended
  by Webstudio. It IS recommended to self-host the **sites**.
- For our setup we run a self-hosted Builder + self-hosted publisher via Docker
  Compose (see `database.md`). For most people, Webstudio Cloud for the Builder +
  self-host the exported site is the supported path.

## Export a project (before deploying anywhere)

Two ways:

1. **Webstudio CLI** (`npx webstudio`) - supports static AND dynamic (JS app) exports.
   Use this if you self-host the Builder.
2. **Download button in the Builder** - Publish > Export > Build and download
   static site. Static only.

Two export types:

- **JavaScript application** - a dynamic Remix app. Most functionality (CMS, webhook
  forms, image optimization, redirects). Needs app-capable hosting.
- **Static site** - HTML/CSS/JS. More versatile hosting but NO dynamic pages,
  redirects, statuses, client navigation, webhook forms, image optimization,
  robots.txt, or sitemap.xml.

> For human-readable class names in the export, disable Atomic CSS (Project Settings).

## The CLI

Current package is `webstudio`. Run with `npx` (do NOT install globally, do NOT use
the old `@webstudio-is/cli` / `wstd`).

Resolve and review a version first, then pin it for every automated run:

```bash
npm view webstudio version
npx --yes webstudio@<approved-version> --version
npx --yes webstudio@<approved-version> <command>
```

Do not use `@latest` in an unattended admin workflow. Record the approved version with the
deployment. Pin production container images by immutable digest as described in `security.md`.

Needs Node.js 22+. Link a project non-interactively:

```bash
npx webstudio link --link "<share-link-with-build-access>"
```

Treat the share link as a credential. Prefer `init --link ... --json` for automation, check
`permissions --json`, and keep `.webstudio` state out of public repositories and logs.

## Native administration with CLI/MCP

Current Webstudio CLI/MCP is the supported agent path for project inspection and mutation. It can
edit the native visual-builder model, sync/import/export, publish/unpublish, manage domains, inspect
permissions, and run audits. Start with:

```bash
npx --yes webstudio@<approved-version> init --link "<share-link-with-build-access>" --json
npx --yes webstudio@<approved-version> permissions --json
npx --yes webstudio@<approved-version> meta.index
```

Then request only the needed MCP tools. Use `--dry-run` for supported mutations before committing.
For large JSON/JSX inputs, use a mode-0600 input file under the linked project rather than shell
interpolation. See the version-matched official MCP reference before relying on a tool name.

The share link comes from the Builder's Share dialog (needs Build access).

## Deploy a site

### VPS with Docker (self-host the site)

```bash
# 1. build locally in the project
webstudio build --template docker   # produces Dockerfile, package.json, build/

# 2. on the VPS: install docker, upload the build
scp -r ./example-site user@VPS_IP:/home/user/example-site
docker build -t website .

# 3. run it (Node server on :3000)
docker run -d --name webstudio -p 3000:3000 --restart unless-stopped webstudio-site

# 4. reverse-proxy with nginx + Let's Encrypt
#    nginx proxies :80/:443 -> 127.0.0.1:3000; certbot for TLS
```

Docker build needs a minimum of 1 GB RAM and 1 core CPU.

### Other supported platforms

- **Serverless (JS app):** Netlify, Vercel.
- **Servers (Docker):** Flightcontrol, DigitalOcean+Hetzner via Coolify.
- **Static:** Cloudflare Pages, GitHub Pages, Netlify, Vercel.
- **Local static preview:** `npx --yes serve@<approved-version> .` (static files use absolute URLs).

## Self-hosting the Builder (our setup)

Docker Compose stack (services: `app`, `db`, `postgrest`, `minio`, `publisher`,
`migrate`, `db-setup`, `minio-init`). See `database.md` and `api.md` for the full
schema, env config, and the load/commit build pattern. Env vars come from the
deployment's secret/config mechanism. Do not read `.env` automatically or disclose secret values.
See `security.md` and `api.md`.
