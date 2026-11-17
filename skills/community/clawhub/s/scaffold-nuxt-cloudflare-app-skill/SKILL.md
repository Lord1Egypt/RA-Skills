---
name: scaffold-nuxt-cloudflare-app
description: Scaffold a new full-stack app on the latest version of Nuxt, deployable to Cloudflare Workers via Wrangler, with NuxtHub for D1/KV/Blob bindings. UI kit is a choice — Nuxt UI (Tailwind-based, default) or Antdv Next (Ant Design system), each with an official Nuxt module. Nuxt Content and i18n are opt-in only (blog/CMS content, or explicit multi-lingual requirement, respectively) — plus SEO, Drizzle, Vitest, pnpm. Use when creating a brand-new Nuxt app, or when asked to set up a Nuxt-on-Cloudflare project.
references:
  - directory-structure
  - nuxt.config.example
  - wrangler.example
  - package.example
  - content.config.example
  - nuxthub-deployment
---

# Nuxt + Cloudflare App Scaffold

This skill scaffolds an **SEO-optimized app on the latest version of Nuxt, deployed to Cloudflare Workers via Wrangler** — content-driven and/or i18n-ready only when the request actually calls for that (see §1). NuxtHub (`@nuxthub/core`) is part of the stack too, but only as the binding/runtime layer for D1, KV, Blob, etc. and local dev emulation — it is not the deploy mechanism (see §7). This is not a minimal `nuxi init` — it's an opinionated, production-oriented stack. Only include the pieces the new app actually needs (see the decision step below); don't cargo-cult every module into a project that doesn't want them.

This skill owns the *scaffolding* decisions (which modules, how they're wired into `nuxt.config.ts`/directory structure/deployment) — enough on its own to produce a working app end to end. It doesn't cover deep per-module usage (which Nuxt UI/Antdv Next component to reach for, advanced `content.config.ts`/query patterns, theming, forms) — that's what the separate `nuxt-ui`, `antdv-next`, and `nuxt-content` skills are for, **if they happen to be installed in this environment**. They are not bundled with this skill and most environments running this skill won't have them — check your actual available-skills listing before ever telling a user "load skill X"; never assume one of these three exists. When one isn't present, don't stall or guess — this skill's own inline guidance (§4, §8) plus each project's official docs ([ui.nuxt.com](https://ui.nuxt.com), [antdv-next.com](https://www.antdv-next.com), [content.nuxt.com](https://content.nuxt.com)) are sufficient to complete the scaffold and get a working starting point.

Always scaffold with the latest Nuxt release (`nuxi init` pulls it automatically) — don't assume the major version is still 4. Check `npm view nuxt version` or the scaffolded `package.json` if you need to confirm which major landed, since structural conventions (like the `app/` srcDir default introduced in Nuxt 4) can change between majors.

## 1. Clarify scope before scaffolding

Don't ask the user about things you can infer from their request. Only ask (via AskUserQuestion, once, batched) what genuinely isn't decidable from context:

- **App name + domain** — needed for `site.name`/`site.url` in nuxt.config and the `wrangler.jsonc` project name.
- **Which UI kit?** → **Nuxt UI** (Tailwind-based, official `@nuxt/ui` module, this skill's default) or **Antdv Next** (Ant Design's Vue 3 component system, official `@antdv-next/nuxt` module). See §4 for scaffold-time wiring. Default to Nuxt UI unless the user names Ant Design/Antdv or an existing design system that maps to it. The two are mutually exclusive — never install both.
- **Does it need a database?** → Drizzle + D1, accessed at runtime via NuxtHub's `hub:db` binding (see §9), or skip `server/db/` entirely for a static/content-only app.
- **Nuxt Content is opt-in, not default.** Only include `@nuxt/content` + `content.config.ts` + `content/` dir if the user's request mentions a blog, a CMS, or markdown/text content authoring. Absent that, skip it — most apps (tools, dashboards, internal apps) have no need for a file-based content layer.
- **i18n is opt-in, not default.** Only include `@nuxtjs/i18n` + `i18n/locales/*.json` if the user explicitly says the app needs to be multi-lingual/multi-language/localized. Absent that, build single-locale and skip i18n entirely — don't add it speculatively "in case" translation comes up later.
- **Monetization/analytics** (AdSense, GA, cookie consent) — only wire these up if the user mentions ads/analytics; don't add tracking to an app that doesn't want it.

Skip modules that don't apply rather than stubbing them out disabled — an app without a DB should have no `server/db/` folder, no `wrangler.jsonc` `d1_databases` block, no `drizzle-kit`/`better-sqlite3`/`@libsql/client` deps.

## 2. Scaffold the base project

```bash
pnpm dlx nuxi@latest init <app-name>
cd <app-name>
```

`nuxi@latest` always pulls the current latest Nuxt release — don't pin an older major. As of Nuxt 4, the default `srcDir` is `app/`; confirm `app/app.vue` exists after scaffolding. If a newer major changed this default, or the scaffold produced a flatter layout (top-level `pages/`, `components/`), move everything app-facing under `app/` to match this skill's layout (see `directory-structure` reference) unless the new Nuxt version's own convention has moved on.

Set the package manager explicitly and pin native-build allowlists (Cloudflare's build environment needs this to build `better-sqlite3`/`sharp` from source rather than silently skipping the postinstall):

```jsonc
// pnpm-workspace.yaml
onlyBuiltDependencies:
  - better-sqlite3   // only if using a local sqlite DB for dev
  - sharp            // only if using @nuxt/image
ignoredBuiltDependencies:
  - '@parcel/watcher'
  - '@tailwindcss/oxide'
  - esbuild
  - unrs-resolver
  - vue-demi
```

Add `"packageManager": "pnpm@<version>"` to `package.json` (match whatever pnpm version is installed locally — check with `pnpm -v`).

## 3. Install modules — pick from this table, don't install blindly

| Concern | Module(s) | Include when |
|---|---|---|
| UI kit (pick exactly one) | `@nuxt/ui` **or** `@antdv-next/nuxt` (+ `antdv-next`, `@antdv-next/icons`) | always — see §4 for setup |
| Images | `@nuxt/image` | any app with user-facing images; needs `sharp` |
| Markdown content | `@nuxt/content` (v3) | **opt-in** — only if the user mentions a blog, a CMS, or text-content authoring |
| i18n | `@nuxtjs/i18n` | **opt-in** — only if the user explicitly says multi-lingual/multi-language/localization |
| SEO bundle | `@nuxtjs/seo` | almost always — pulls in sitemap, robots, OG image, schema.org as one meta-module |
| Cloudflare bindings (D1/KV/Blob) + local dev emulation | `@nuxthub/core` | **always**, for any app targeting Cloudflare — provides `hub:db`/`hub:kv`/`hub:blob` imports and Miniflare-backed local dev; deployment itself is Wrangler, not this module — see §7 |
| Reactive utils | `@vueuse/nuxt` | almost always |
| Motion/animation | `motion-v/nuxt` | if the UI needs transitions/animation primitives |
| Analytics | `nuxt-gtag`, `@nuxt/scripts` | only if the user wants GA/AdSense |
| Cookie consent | `nuxt-simple-cookie-consent` | only if analytics/ads are present and consent is needed |
| AI-agent discoverability | `nuxt-llms`, `nuxt-ai-ready` | only if the app should expose `/llms.txt` and be crawlable by AI agents |
| Social share buttons | `@stefanobartoletti/nuxt-social-share` | only for content/blog sites |
| Linting | `@nuxt/eslint` | always |
| DB layer | `drizzle-orm`, `drizzle-kit`, `better-sqlite3` (dev), `@libsql/client` | only if the app has a DB |
| Testing | `@nuxt/test-utils`, `vitest`, `@vue/test-utils`, `@vitejs/plugin-vue`, `happy-dom` | always |

```bash
# swap @nuxt/ui for @antdv-next/nuxt antdv-next @antdv-next/icons if that's the chosen UI kit
pnpm add @nuxt/ui @nuxt/image @nuxtjs/seo @nuxthub/core @vueuse/nuxt
pnpm add -D @nuxt/eslint @nuxt/test-utils @vitejs/plugin-vue @vue/test-utils vitest happy-dom
# then add only the optional modules selected in step 1
```

## 4. Wire up the UI kit

Both options are official Nuxt modules with auto-registered components — the wiring is more similar than different. This section covers the scaffold-time wiring only; if a `nuxt-ui` or `antdv-next` skill happens to be installed (check the available-skills listing — don't assume), it's the better source for anything component-level afterward: which component fits a given UI need, theming/design-system work, forms, layouts. If not installed, the official docs linked in each option below cover the same ground.

### Option A: Nuxt UI (default)

1. Add `'@nuxt/ui'` to `modules` in `nuxt.config.ts` (see `nuxt.config.example.ts`).
2. Import its CSS in `app/assets/css/main.css`:
   ```css
   @import "tailwindcss";
   @import "@nuxt/ui";
   ```
3. Wrap the root component in `UApp` — required for toasts, tooltips, and programmatic overlays to work at all, easy to forget since nothing errors loudly if it's missing:
   ```vue
   <!-- app/app.vue -->
   <template>
     <UApp>
       <NuxtLayout><NuxtPage /></NuxtLayout>
     </UApp>
   </template>
   ```

Components auto-import with a `U` prefix (`UButton`, `UCard`, ...); theming goes through `app/app.config.ts`. For anything beyond this — component selection, design-system/forms/layout/recipe guidance — use the `nuxt-ui` skill if it's installed; otherwise [ui.nuxt.com](https://ui.nuxt.com) covers the same ground, and Nuxt UI also ships an [MCP server](https://ui.nuxt.com/docs/getting-started/ai/mcp) worth setting up for live component API lookup regardless of which skill situation applies.

### Option B: Antdv Next

[antdv-next](https://github.com/antdv-next/antdv-next) is Ant Design's Vue 3 component library, with an **official Nuxt module**, `@antdv-next/nuxt` (requires Nuxt ≥ 4.0.0, Vue ≥ 3.5.0):

1. Install: `npx nuxi module add @antdv-next/nuxt` (or manually: `pnpm add -D @antdv-next/nuxt antdv-next @antdv-next/icons` — the upstream docs list all three as devDependencies even though components render at runtime; Nuxt modules commonly work this way). Drop `@nuxt/ui` and its Tailwind CSS import instead — don't run both design systems at once.
2. Configure via the `antd` key (not `hub`, not `ui`):
   ```ts
   // nuxt.config.ts
   export default defineNuxtConfig({
     modules: ['@antdv-next/nuxt'],
     antd: { icon: true } // enables auto-registration of @antdv-next/icons
   })
   ```
3. Add reset styles (and the zero-runtime theme CSS, recommended over runtime CSS-in-JS for SSR):
   ```ts
   export default defineNuxtConfig({
     css: ['antdv-next/dist/reset.css', 'antdv-next/dist/antd.css']
   })
   ```

Components auto-register with an `A` prefix (`AButton`, `ATable`, ...) — same auto-import ergonomics as Nuxt UI's `U` prefix, just a different design system. `antd.prefix`/`antd.include`/`antd.exclude` (and the icon equivalents) narrow what gets registered if bundle size matters. For component API/props/slots/demos/theme-token lookups, use the `antdv-next` skill if it's installed; otherwise [www.antdv-next.com](https://www.antdv-next.com) has the same per-component docs.

## 5. Lay out the directory structure

Use this exact layout — see the `directory-structure` reference for the annotated full tree. Summary:

- `app/` — `app.vue`, `app.config.ts`, `error.vue`, `assets/css/main.css`, `components/`, `composables/`, `layouts/`, `pages/`, `plugins/`, `utils/`
- `server/` — `api/` (file-based, `*.get.ts`/`*.post.ts` suffix = HTTP method), `db/schema.ts` + `db/migrations/sqlite/` (Drizzle, only if DB is in scope), `middleware/`, `plugins/`, `repositories/`, `utils/`
- `shared/types/` — types used by both `app/` and `server/` (Nuxt's `shared/` auto-import layer, introduced in Nuxt 4)
- `content/<locale>/...` + `content.config.ts` — only if `@nuxt/content` is in scope; one subdirectory per locale if i18n is also in scope
- `i18n/locales/*.json` — only if `@nuxtjs/i18n` is in scope
- `tests/app/`, `tests/server/`, `tests/setup.ts` + `vitest.config.ts`
- `public/` — static assets, `favicon.ico`, `.well-known/`
- Root config: `nuxt.config.ts`, `wrangler.jsonc`, `eslint.config.mjs`, `tsconfig.json` (references-only, pointing at `.nuxt/tsconfig.*.json`), `.nuxtrc`, `.env.example`

## 6. Wire up `nuxt.config.ts`

Use `nuxt.config.example.ts` as the template — copy it, then strip out any module blocks for things not selected in step 1. Key points that are easy to miss:

- `modules` order doesn't matter functionally but keep it grouped (UI/content → i18n → SEO/analytics → hub) for readability.
- `site.url` / `site.name` (from `@nuxtjs/seo`) must be set to the real domain — sitemap, OG image, and schema.org all derive from this.
- `hub: { db: { dialect: 'sqlite', applyMigrationsDuringBuild: false } }` — only when a DB is in scope. This is NuxtHub's binding config (it's what makes the `hub:db` import resolve to the right D1 instance locally vs. in production) — it has nothing to do with how the app gets deployed. `applyMigrationsDuringBuild: false` is deliberate: migrations run as an explicit step (`npx nuxt db migrate`, §9), not silently during every build. This minimal shape assumes bindings come from a hand-maintained `wrangler.jsonc` (§7); NuxtHub also accepts a fuller `db: { dialect, driver: 'd1', connection: { databaseId } }` shape that lets it auto-generate `wrangler.json` instead — see `nuxthub-deployment.md`.
- `compatibilityDate` — set to the current date at scaffold time; Nitro/Cloudflare use this to pin runtime behavior.
- `routeRules` for any public API surface that needs CORS opened up (see the commented `/api/tools/**` example in `nuxt.config.example.ts`) — CORS is closed by default, open it explicitly per-route, not globally.
- `nitro.prerender.routes` + `crawlLinks: true` if the site should be statically prerendered where possible.
- If i18n is in scope, use the pattern in `nuxt.config.example.ts`: a `LOCALES` const at the top of the file, `prefix_except_default` strategy, and `detectBrowserLanguage` with `redirectOn: 'root'`.

## 7. Wire up Cloudflare bindings (NuxtHub) and deployment (Wrangler)

These are two separate concerns — don't conflate them:

- **NuxtHub (`@nuxthub/core`)** gives the app its Cloudflare bindings and local dev emulation: D1/KV/R2, accessed via the `hub:db`/`hub:kv`/`hub:blob` virtual-module imports (or the equivalent `@nuxthub/db` package import — see §9), plus Miniflare-backed local dev. This is a runtime/dev-experience layer, configured via the `hub` block in `nuxt.config.ts` (§6).
- **Wrangler** is what actually builds and deploys the app to Cloudflare Workers, configured via `wrangler.jsonc`. **`npx nuxthub deploy` and NuxtHub Admin are deprecated as of NuxtHub v0.10** (Admin sunsets 2025-12-31) — `wrangler deploy` is the only supported deploy path now, not a preference of this skill's.

NuxtHub can actually auto-generate `wrangler.json` from the `hub` block at build time, so a manual `wrangler.jsonc` isn't strictly required for a minimal single-environment app — see `nuxthub-deployment.md` for that shape. This skill still defaults to a hand-maintained `wrangler.jsonc` because observability config and the multi-environment/preview setup below aren't covered by auto-generation.

Copy `wrangler.example.jsonc`, then:

1. Set `name` to the Cloudflare Workers project name (must be globally unique on the account).
2. Set `compatibility_date` to today; keep `compatibility_flags: ["nodejs_compat", "nodejs_als"]` — both are required by NuxtHub's runtime bindings.
3. If a DB is in scope, keep the `d1_databases` block but leave `database_id` blank/placeholder until the DB is actually provisioned (`wrangler d1 create <name>` will produce the real ID — never fabricate one). Same pattern for `kv_namespaces`/`r2_buckets` if KV/Blob are in scope — see `nuxthub-deployment.md` for the required binding names (`DB`, `KV`, `CACHE`, `BLOB`).
4. `migrations_dir: "server/db/migrations/sqlite"` must match wherever migrations are emitted (see §9 — via `npx nuxt db generate`, not raw `drizzle-kit`).

Set `nitro.preset: 'cloudflare_module'` in `nuxt.config.ts` so `nuxt build` emits Nitro's Cloudflare Workers output shape. Deploy with Wrangler directly:

```bash
pnpm build
npx wrangler deploy
```

Alternatively, connect the repo to Cloudflare Workers Builds (git-integrated CI/CD, configured in the Cloudflare dashboard rather than the codebase) so pushes to the deploy branch build and deploy automatically — check the target Cloudflare account/dashboard for whether this is already set up before assuming a manual `wrangler deploy` workflow is needed. For anything beyond this basic flow (Pages instead of Workers, secrets, custom domains, etc.), use a `cloudflare`/`wrangler` skill if one is installed in this environment; otherwise [developers.cloudflare.com/workers](https://developers.cloudflare.com/workers/) is the authoritative source — don't assume such a skill exists.

### Preview environment

Set this up alongside production rather than bolting it on later — there are two independent pieces:

**1. A named Wrangler environment, isolated from production data.** Add an `env.preview` block to `wrangler.jsonc` (see `wrangler.example.jsonc`) with its own Worker name and, if a DB is in scope, its own D1 binding pointing at a separate database. Bindings are **not inherited** between environments — this cuts both ways: skipping it doesn't mean preview falls back to the production database, it means the `DB` binding is simply undefined in that environment and `hub:db` calls fail. Give preview its own database rather than leaving the binding out.

```jsonc
{
  "name": "<app-name>",
  // ...production-level config...
  "env": {
    "preview": {
      "name": "<app-name>-preview",
      "vars": { "NUXT_PUBLIC_SITE_URL": "https://<app-name>-preview.<subdomain>.workers.dev" },
      "d1_databases": [
        {
          "binding": "DB",
          "database_name": "<app-name>-preview",
          "database_id": "<separate-preview-d1-database-id>",
          "migrations_dir": "server/db/migrations/sqlite"
        }
      ]
    }
  }
}
```

Build and deploy against it using **both** the `CLOUDFLARE_ENV` build-time variable and Wrangler's `--env` deploy-time flag (NuxtHub's Cloudflare integration reads the former at build time; Wrangler reads the latter at deploy time — pass both rather than relying on just one):

```bash
CLOUDFLARE_ENV=preview npx nuxi build
npx wrangler deploy --env preview     # or: wrangler dev --env preview, for local preview-env testing
```

NuxtHub's `hub:db`/`hub:kv`/`hub:blob` need no separate config for this — they just resolve to whatever binding is active for the environment that was built/deployed against.

**2. Cloudflare Workers Builds' native per-branch/PR preview URLs.** Since this is git-integrated CI/CD configured in the Cloudflare dashboard (not the codebase), it's something to point out to the user rather than something this skill can wire up directly — but the shape to set up is two build triggers:

- **Production trigger**: branch = the production branch (e.g. `main`), deploy command `npx wrangler deploy`.
- **Preview trigger**: all other branches (`branch_includes: ["*"]`, `branch_excludes: ["main"]`), with `CLOUDFLARE_ENV=preview` set as a build environment variable and deploy command `npx wrangler versions upload --env preview` — `versions upload` (not `deploy`) uploads a version and gets a preview URL without promoting it to the live/production deployment.

Each PR then gets its own stable branch-based preview URL (`<branch-name>-<worker-name>.<subdomain>.workers.dev`) posted as a PR comment, plus a per-commit versioned preview URL — both automatic once the triggers exist, no extra per-PR config. **Preview URLs are opt-in** (a security default changed in Sept 2025): the Worker needs its `workers.dev` subdomain and Preview URLs toggle enabled in **Settings → Domains & Routes**, or the URLs simply won't appear even though builds succeed.

Note this is distinct from `preview_database_id` on a `d1_databases` binding — that field only affects local `wrangler dev --remote`, not git-triggered preview deployments; the `env.preview` block above is what actually isolates preview deployments.

For anything else — Vercel/Netlify/Deno providers, D1-over-HTTP for non-Cloudflare hosts, KV/Blob provider tables — see `nuxthub-deployment.md` and its upstream source.

## 8. Content + i18n (if in scope)

- `content.config.ts`: one `defineCollection` per content type (e.g. `article`, `about`), `type: 'page'`, `source` as an array of `{ include: '<locale>/<pattern>' }` per locale, and a Zod `schema` that always includes the `@nuxtjs/seo` content schemas (`defineRobotsSchema`, `defineSitemapSchema`, `defineOgImageSchema`, `defineSchemaOrgSchema`) alongside the collection's own fields. See `content.config.example.ts`. This SEO-schema layering is scaffold-specific (this skill's own pattern) — for everything else about collections, `queryCollection`, Markdown/MDC rendering, or content databases, use the `nuxt-content` skill if it's installed, otherwise [content.nuxt.com](https://content.nuxt.com) covers the same ground.
- Locale files live in `i18n/locales/<code>.json`; content lives in `content/<code>/...` mirroring the same locale codes.
- Don't scaffold a long list of locales speculatively — start with what the user actually needs (often just `en`) and note that more can be added later by extending the `LOCALES` array + adding a locale dir.

## 9. Database (if in scope)

- `server/db/schema.ts` — Drizzle schema using `sqliteTable` (D1 is SQLite-compatible).
- `server/repositories/` — one file per aggregate/entity, wrapping raw Drizzle queries, e.g. `import { db, schema } from '@nuxthub/db'`, so `server/api/*` handlers stay thin.
- Access the DB via the `hub:db` virtual-module import — `import { db, schema } from 'hub:db'` — or the equivalent `@nuxthub/db` package import; both resolve to the same D1 binding wiring for local dev (via Miniflare) and production. `db`/`schema` are also auto-imported server-side, so an explicit import often isn't even needed. Don't reach for the older `hubDatabase()` composable in new code — it predates the current virtual-module API.
- Generate/apply migrations with the `nuxt db` CLI (from `@nuxthub/db`, wraps Drizzle Kit), not raw `drizzle-kit` commands: `npx nuxt db generate`, `npx nuxt db migrate`, `npx nuxt db sql "<query>"`. Output lands in the same `server/db/migrations/sqlite/` + `meta/_journal.json` shape either way — see `nuxthub-deployment.md`.
- Local dev DB state lives under `.data/` (gitignored) — don't commit it.

## 10. Testing + linting

- `vitest.config.ts`: `environment: 'node'`, `setupFiles: ['./tests/setup.ts']`, `@vitejs/plugin-vue` plugin — even for a Nuxt app, most unit tests run fine under plain Vitest; reach for `@nuxt/test-utils`'s `setup()` only for tests that need the full Nuxt runtime context.
- `eslint.config.mjs` — thin wrapper around the generated `.nuxt/eslint.config.mjs` (`@nuxt/eslint` module generates this at `nuxt prepare`/`dev` time). Add project-specific rule overrides here, don't hand-roll a flat config from scratch.
- `package.json` scripts: `dev`, `build`, `preview`, `postinstall: nuxt prepare`, `lint`, `lint:fix`, `typecheck: nuxt typecheck`, `test: vitest run`.

## 11. Final checklist before handing back to the user

- [ ] `.env.example` documents every required runtime env var (at minimum `NUXT_PUBLIC_SITE_URL` if OG image generation needs it at build time).
- [ ] `site.url` in `nuxt.config.ts` and `name` in `wrangler.jsonc` reflect the real app, not the scaffold's placeholder values.
- [ ] No leftover placeholder/example IDs (AdSense client ID, GA measurement ID, D1 database UUID, domain) — these must come from the new project's own accounts.
- [ ] Every module added in step 3 is actually used — no dead config blocks for skipped features.
- [ ] Only one UI kit is installed (`@nuxt/ui` or `@antdv-next/nuxt`, never both), and its integration matches §4 (module + Tailwind CSS import + `UApp` wrapper for Nuxt UI; module + `antd` config key + reset/theme CSS for Antdv Next).
- [ ] `wrangler.jsonc` has an `env.preview` block with its own Worker name (and its own D1/KV bindings if a DB is in scope) — not just a bare production config (§7 "Preview environment").
- [ ] `pnpm install && pnpm dev` runs clean before considering the scaffold done.
