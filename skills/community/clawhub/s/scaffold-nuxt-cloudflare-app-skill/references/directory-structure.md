# Reference directory structure

Annotated full tree. Items marked **(optional)** only apply if that concern is in scope for the new app (see SKILL.md §1/§3).

```
.
├── app/                              # Nuxt 4 srcDir — everything client/app-facing
│   ├── app.vue                       # root component (usually just <NuxtLayout><NuxtPage/></NuxtLayout>)
│   ├── app.config.ts                 # runtime app config (theme tokens, ui defaults, etc.)
│   ├── error.vue                     # custom error page
│   ├── assets/
│   │   └── css/main.css              # Tailwind entry + custom CSS
│   ├── components/                   # global auto-imported components
│   │   └── OgImage/*.satori.vue      # (optional) @nuxt/image / nuxt-og-image satori templates
│   ├── composables/                  # auto-imported composables (useX.ts)
│   ├── layouts/
│   │   └── default.vue
│   ├── pages/                        # file-based routing
│   │   └── article/[...slug].vue     # (optional, if @nuxt/content) catch-all content route
│   ├── plugins/                      # client/universal Nuxt plugins (e.g. gtag.consent.ts)
│   └── utils/                        # auto-imported plain utility functions
│
├── server/                           # Nitro server
│   ├── api/                          # file-based API routes; suffix = HTTP method
│   │   ├── geo.get.ts
│   │   └── tools/random-hex.get.ts
│   ├── db/                           # (optional, if DB in scope)
│   │   ├── schema.ts                 # Drizzle schema (sqliteTable definitions)
│   │   └── migrations/sqlite/        # drizzle-kit generated migrations
│   ├── middleware/                   # runs on every request; numeric prefix controls order
│   │   └── 00.markdown-negotiation.ts
│   ├── plugins/                      # Nitro plugins (init hooks, cron, etc.)
│   ├── repositories/                 # (optional, if DB in scope) thin data-access layer
│   │   └── newsletter.ts
│   └── utils/                        # auto-imported server-only utilities
│       └── rateLimit.ts
│
├── shared/                           # Nuxt 4 shared layer — importable from app/ AND server/
│   └── types/
│       └── newsletter.ts
│
├── content/                          # (optional, if @nuxt/content) one dir per locale
│   ├── en/
│   │   ├── article/*.md
│   │   ├── about.yml
│   │   └── privacy.yml
│   └── <other-locales>/...
│
├── i18n/                             # (optional, if @nuxtjs/i18n)
│   └── locales/*.json                # one file per locale code
│
├── tests/
│   ├── app/                          # component/composable tests
│   ├── server/                       # API/repository tests
│   └── setup.ts                      # vitest global setup
│
├── public/                           # static passthrough assets
│   ├── favicon.ico
│   └── .well-known/
│
├── content.config.ts                 # (optional, if @nuxt/content) collection + Zod schemas
├── i18n.config.ts                    # (optional, if @nuxtjs/i18n) runtime i18n config
├── nuxt.config.ts
├── wrangler.jsonc                    # Cloudflare Workers config (D1 bindings, compat flags)
├── eslint.config.mjs                 # wraps generated .nuxt/eslint.config.mjs
├── tsconfig.json                     # references-only, points at .nuxt/tsconfig.*.json
├── vitest.config.ts
├── .nuxtrc                           # pins module-specific setup versions
├── .env.example
├── pnpm-workspace.yaml               # onlyBuiltDependencies / ignoredBuiltDependencies
└── package.json
```

Notes:
- `.nuxt/`, `.output/`, `.data/` are generated/local-state directories — gitignored, never hand-authored.
- `tsconfig.json` deliberately has an empty `files: []` and only `references` — all real compiler options live in the generated per-context tsconfigs under `.nuxt/`, produced by `nuxt prepare`.
- File-based API route suffixes (`.get.ts`, `.post.ts`, etc.) are Nitro convention, not Nuxt-specific — this is how the HTTP method is bound without an explicit router.
