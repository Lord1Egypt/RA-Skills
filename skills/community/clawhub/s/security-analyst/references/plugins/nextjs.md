---
name: Next.js
detect:
  files: ["next.config.js", "next.config.mjs", "next.config.ts"]
  dependencies: ["next"]
  keywords: ["Next.js", "NextJS"]
---

## attack-surface-http

**API Routes and Route Handlers:**
1. Next.js API routes (`pages/api/` or `app/*/route.ts`) have NO built-in auth middleware — auth must be explicitly checked in every handler
   - Grep for all `export async function GET/POST/PUT/DELETE/PATCH` in `app/**/route.ts` and `export default function handler` in `pages/api/`
   - For EACH route handler: is auth verified before processing? (no global middleware like Express)
   - Are there API routes that accidentally became public because auth was forgotten?

2. **Server Actions Input Validation:**
   - Grep for `"use server"` directive in files and functions
   - Server Actions receive form data directly — is every input validated and typed?
   - Can a client call a server action with unexpected parameters? (server actions are accessible as POST endpoints)
   - Is the `action` attribute on forms pointing to the correct server action? Can it be manipulated?

3. **Route Handler Parameter Injection:**
   - Do route handlers read `params` from dynamic segments (`[id]`, `[...slug]`)?
   - Are dynamic params validated? (e.g., `params.id` used directly in a database query)
   - Can path traversal via `[...slug]` segments reach unintended resources?

4. **Middleware Bypass:**
   - Read `middleware.ts`/`middleware.js` if it exists
   - Does middleware protect all routes that need it? Check the `matcher` config
   - Can requests to `/_next/` paths bypass middleware? (Next.js internal paths are often excluded)
   - Can requests with unusual headers or methods bypass middleware matching?
   - Are there routes that should be protected but aren't matched by the middleware pattern?

## attack-surface-frontend

**Server Component vs Client Component Data Leaking:**
1. Server Components can access server-side data (databases, secrets, env vars) that should never reach the client
   - Are there Server Components that pass sensitive data as props to Client Components? (this serializes the data to the client bundle)
   - Grep for `"use client"` — components below this boundary receive serialized props
   - Are database query results or internal API responses being passed from Server to Client components without filtering sensitive fields?

2. **`use server` Directive Misuse:**
   - Are there functions marked `"use server"` that expose internal data in their return values?
   - Can a client call a server action and receive data they shouldn't see?
   - Are server action error messages revealing internal details?

3. **Hydration Mismatch Data Exposure:**
   - If server-rendered HTML contains different data than the client hydration, can this expose data?
   - Are there conditional rendering patterns (`typeof window !== 'undefined'`) that show different content on server vs client?
   - Could a mismatch cause server-only data to be included in the initial HTML but not intended for client display?

4. **Client-Side Router Security:**
   - Can the client-side router be manipulated to access routes that should be server-protected?
   - Are there `router.push()` calls with user-controlled destinations? (open redirect)
   - Is `useSearchParams()` used with unsanitized values in rendering? (reflected XSS)

## config-infrastructure

**`next.config.js` Security:**
1. Read `next.config.js`/`next.config.mjs`/`next.config.ts` and check:
   - **Security headers**: Are `Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security` configured in `headers()`?
   - **`poweredBy`**: Is `x-powered-by` disabled? (`poweredBy: false` in config)
   - **`reactStrictMode`**: Is strict mode enabled? (helps catch unsafe lifecycle patterns)

2. **Image Optimization SSRF:**
   - Check `images.remotePatterns` or `images.domains` in config
   - Are remote patterns overly broad? (e.g., `{ protocol: 'https', hostname: '**' }` allows SSRF via `/_next/image?url=`)
   - Can an attacker use the image optimization endpoint to probe internal services?

3. **Rewrites and Redirects:**
   - Check `rewrites()` and `redirects()` in config
   - Can rewrite destinations be influenced by user input? (SSRF via rewrite proxy)
   - Are there open redirects in the `redirects()` configuration? (wildcard path parameters forwarded to destination)
   - Do `beforeFiles` rewrites bypass API route auth?

4. **Server Actions Configuration:**
   - Is `serverActions.bodySizeLimit` configured? (default is 1MB — can an attacker send huge payloads?)
   - Are `serverActions.allowedOrigins` restricted? (prevents CSRF on server actions)

5. **Environment Variable Exposure:**
   - Variables prefixed with `NEXT_PUBLIC_` are exposed to the client bundle
   - Are there `NEXT_PUBLIC_` variables that contain sensitive data? (API keys, secrets)
   - Could renaming a variable to add `NEXT_PUBLIC_` accidentally expose it?
