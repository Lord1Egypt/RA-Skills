---
name: Vue.js / Nuxt.js
detect:
  files: ["nuxt.config.js", "nuxt.config.ts", "vue.config.js"]
  dependencies: ["vue", "nuxt", "@nuxt/kit", "vuex", "pinia"]
  keywords: ["Vue", "Nuxt", "Vue.js", "Nuxt.js"]
---

## attack-surface-frontend

**Vue.js XSS Vectors:**
1. **`v-html` Directive:**
   - Grep for `v-html` in all `.vue` files — this renders raw HTML without escaping
   - For each occurrence: is the bound value user-controlled or derived from user input?
   - Can an attacker inject `<script>`, `<img onerror=...>`, or event handlers via `v-html`?
2. **Dynamic Component Rendering:**
   - Grep for `:is` or `v-bind:is` on `<component>` — can an attacker control which component renders?
   - Are there `render()` functions or JSX that interpolate user content?
3. **Template Compilation at Runtime:**
   - Is `Vue.compile()` or `app.config.compilerOptions` used with user-controlled templates?
   - Is the full Vue build (with template compiler) shipped to production? (enables runtime template injection)
4. **URL Injection:**
   - Grep for `:href`, `:src`, `:action` bindings with user-controlled values
   - Can an attacker inject `javascript:` protocol URLs?
   - Are `router.push()` / `router.replace()` calls using unsanitized user input? (open redirect)
5. **Vue Devtools in Production:**
   - Is `Vue.config.devtools` or `app.config.performance` enabled in production? (exposes component state)
   - Is `__VUE_DEVTOOLS_GLOBAL_HOOK__` accessible?

**Nuxt.js-Specific:**
6. **Server Routes (Nuxt 3):**
   - Glob for `server/api/**/*.ts`, `server/routes/**/*.ts`, `server/middleware/**/*.ts`
   - Do server API routes validate auth? (Nuxt server routes have no built-in auth middleware)
   - Is `readBody()`, `getQuery()`, `getRouterParams()` input validated before use?
7. **SSR Data Leaking:**
   - Are server-side `useAsyncData()` or `useFetch()` calls returning sensitive data that gets serialized to `__NUXT_DATA__`?
   - Check the HTML source for `<script>window.__NUXT__=` — does it contain data not intended for the client?
8. **Nuxt Plugins:**
   - Do Nuxt plugins (`plugins/` directory) run on both server and client? Is server-only data leaking through shared plugin state?

## attack-surface-http

**Nuxt Server Endpoints:**
1. Glob for `server/api/**` and `server/routes/**` — these are Nuxt's server-side HTTP handlers
   - Are all endpoints using `defineEventHandler` with proper input validation?
   - Is `readBody` used without schema validation?
   - Can query parameters from `getQuery()` inject unexpected types?
2. **Middleware:**
   - Read `server/middleware/` files — do they enforce auth on all protected routes?
   - Is there a gap between Nuxt route middleware (client-side) and server middleware (actual protection)?

## config-infrastructure

**Nuxt Configuration Security:**
1. Read `nuxt.config.ts`/`nuxt.config.js`:
   - Is `ssr: false` set? (SPA mode loses server-side security boundaries)
   - Check `runtimeConfig` vs `runtimeConfig.public` — are secrets in the public config?
   - Is `devtools` enabled in production?
2. **Environment Variables:**
   - Nuxt exposes `NUXT_PUBLIC_*` variables to the client — are there secrets with this prefix?
   - Is `runtimeConfig` used instead of hardcoded values for API keys?
3. **Nitro Configuration:**
   - Check `nitro.routeRules` for security headers and caching rules
   - Are there route rules that disable CORS or security headers for specific paths?

## dependency-audit

**Vue/Nuxt Dependency Concerns:**
1. Check Vue version for known XSS bypasses in template compiler
2. If using `vue-sanitize` or `dompurify` for HTML sanitization: is it configured correctly?
3. Are Nuxt modules from `nuxt.config` from trusted sources? (community modules may have vulnerabilities)
4. Is `@nuxt/content` used? Check for Markdown injection if content is user-contributed
