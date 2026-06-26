---
name: nodeops-auth
description: Add NodeOps PKCE OAuth authentication to a Next.js app. Trigger when the user wants to set up NodeOps login, integrate NodeOps OAuth, add @nodeops-createos/integration-oauth, or connect a Next.js project to NodeOps identity/SSO. Also trigger on "add NodeOps auth", "setup NodeOps authentication", or "add NodeOps login".
---

# NodeOps Auth Setup

Add NodeOps PKCE OAuth to an existing Next.js (App Router) project.

## Prerequisites

Before starting, verify the project is compatible:

- **App Router required**: Check if `app/` directory exists. If only `pages/` exists, stop and tell the user: "This skill only supports Next.js App Router. Your project uses Pages Router."
- **Next.js required**: Check `package.json` for `next` in dependencies. If missing, stop and tell the user this is a Next.js-only package.

## Idempotency

Before each step, check if the work is already done. Skip steps that are already complete:
- If `@nodeops-createos/integration-oauth` is already in `package.json` dependencies, skip install.
- If `app/api/auth/me/route.ts` and `app/api/auth/token/route.ts` already exist, skip route creation.
- If `AuthProvider` from `@nodeops-createos/integration-oauth` is already imported in the layout, skip wrapping.
- If `app/callback/page.tsx` (or `.jsx`) already exists, skip callback page creation.
- If `.env.example` already exists and contains `NODEOPS_`, skip env file creation.

## Steps

1. **Detect project setup** — read `package.json` and check for lock files:
   - Package manager: if `pnpm-lock.yaml` exists → pnpm, if `yarn.lock` exists → yarn, else → npm
   - TypeScript: if `tsconfig.json` exists use `.ts`/`.tsx` extensions, else `.js`/`.jsx`
   - Confirm `app/` directory exists (App Router). If only `pages/` exists, stop.
   - Confirm `next` is in dependencies. If not, stop.

2. **Install the package** — run the appropriate install command:
   - npm: `npm install @nodeops-createos/integration-oauth`
   - pnpm: `pnpm add @nodeops-createos/integration-oauth`
   - yarn: `yarn add @nodeops-createos/integration-oauth`
   - **If install fails**: check if the user has network access and the registry is reachable. Suggest running the command manually if it keeps failing.

3. **Create the API routes** — create two separate route files, creating directories as needed:

   `app/api/auth/me/route.ts` (or `.js`):
   ```ts
   export { GET } from '@nodeops-createos/integration-oauth/server/me';
   ```

   `app/api/auth/token/route.ts` (or `.js`):
   ```ts
   export { POST } from '@nodeops-createos/integration-oauth/server/token';
   ```

4. **Wrap layout with AuthProvider** — read the root layout file. It could be `app/layout.tsx`, `app/layout.jsx`, `app/layout.js`, or `app/layout.ts`. Find whichever exists.
   - Add the import at the top of the file:
     ```tsx
     import { AuthProvider } from '@nodeops-createos/integration-oauth';
     ```
   - Find `{children}` inside the `<body>` tag. Wrap it with `<AuthProvider>`:
     ```tsx
     <AuthProvider>{children}</AuthProvider>
     ```
   - **Do NOT add "use client" to the layout.** `AuthProvider` is already marked `"use client"` internally — it works fine when imported from a Server Component layout.
   - **If the layout already has other providers** (e.g., ThemeProvider, QueryClientProvider), nest `<AuthProvider>` alongside them. Do NOT remove or replace existing providers.
   - **If `{children}` is not directly inside `<body>`** (e.g., it's inside a wrapper div or fragment), wrap wherever `{children}` appears.
   - **If no layout file exists**, stop and tell the user to create a root layout first.

5. **Create the callback page** — ask the user: "Where should users be redirected after login? (default: /dashboard)". Use their answer as the `redirectTo` value. Then create `app/callback/page.tsx` (or `.jsx`):
   ```tsx
   "use client";
   import { useCallbackHandler } from "@nodeops-createos/integration-oauth";

   export default function Callback() {
     const { loading, error } = useCallbackHandler({ redirectTo: "/dashboard" });

     if (loading) return (
       <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
         <p>Signing in...</p>
       </div>
     );
     if (error) return <p>Login failed: {error}</p>;
     return null;
   }
   ```

6. **Create `.env.example`** — create this file at the project root:
   ```
   # ── Client-side (exposed to browser via NEXT_PUBLIC_ prefix) ──────────────────
   NEXT_PUBLIC_NODEOPS_AUTH_URL=https://id.nodeops.network/oauth2/auth
   NEXT_PUBLIC_NODEOPS_CLIENT_ID=your_client_id_here
   NEXT_PUBLIC_NODEOPS_REDIRECT_URI=http://localhost:3000/callback
   NEXT_PUBLIC_NODEOPS_SCOPES=offline_access offline openid

   # ── Server-side only (never sent to browser) ──────────────────────────────────
   NODEOPS_CLIENT_SECRET=your_client_secret_here
   NODEOPS_TOKEN_URL=https://id.nodeops.network/oauth2/token
   NODEOPS_USERINFO_URL=https://autogen-v2-api.nodeops.network/v1/users/me
   ```

7. **Create `.env.local`** — if `.env.local` does not already exist, copy `.env.example` to `.env.local` and remind the user to fill in `NEXT_PUBLIC_NODEOPS_CLIENT_ID` and `NODEOPS_CLIENT_SECRET` with their credentials from the NodeOps developer portal. If `.env.local` already exists, append the missing `NODEOPS_` vars only — do NOT overwrite existing values.

8. **Check `.gitignore`** — read `.gitignore` (if it exists). If `.env.local` is NOT listed, add it to prevent leaking secrets. Also ensure `.env` is listed. If no `.gitignore` exists, create one with at least:
   ```
   .env
   .env.local
   ```

9. **Docker/container deployment** — check if a `Dockerfile` exists in the project root. If it does, verify it handles NodeOps env vars correctly and warn the user if not. If the user asks about Docker or deployment, create or update the Dockerfile.

   **Critical**: `NEXT_PUBLIC_*` vars are baked into the JS bundle at **build time** by Next.js. They must be set as `ENV` or `ARG` in the Dockerfile **before** `RUN npm run build`. Setting them only at runtime does nothing — the bundle will contain `undefined`.

   The two categories of vars:

   | Variable | When needed | Why |
   |---|---|---|
   | `NEXT_PUBLIC_NODEOPS_AUTH_URL` | Build time | Inlined into client JS bundle |
   | `NEXT_PUBLIC_NODEOPS_CLIENT_ID` | Build time | Inlined into client JS bundle |
   | `NEXT_PUBLIC_NODEOPS_REDIRECT_URI` | Build time | Inlined into client JS bundle |
   | `NEXT_PUBLIC_NODEOPS_SCOPES` | Build time | Inlined into client JS bundle |
   | `NODEOPS_CLIENT_SECRET` | Runtime only | Read by API route on each request |
   | `NODEOPS_TOKEN_URL` | Runtime only | Read by API route on each request |
   | `NODEOPS_USERINFO_URL` | Runtime only | Read by API route on each request |

   > **CreateOS note:** CreateOS uses the Dockerfile when one is present. Use a **single-stage** Dockerfile only — multi-stage builds with `COPY --from=builder` fail on this platform. Remove the Dockerfile entirely to fall back to CreateOS's default install/run commands. See the CreateOS section (step 10) for the runtime config workaround for `NEXT_PUBLIC_*` vars.

   Example Dockerfile (single-stage, compatible with CreateOS):
   ```dockerfile
   FROM node:20-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci

   COPY . .

   # NEXT_PUBLIC_* must be present at build time — they get baked into the JS bundle
   ARG NEXT_PUBLIC_NODEOPS_AUTH_URL=https://id.nodeops.network/oauth2/auth
   ARG NEXT_PUBLIC_NODEOPS_CLIENT_ID
   ARG NEXT_PUBLIC_NODEOPS_REDIRECT_URI
   ARG NEXT_PUBLIC_NODEOPS_SCOPES=offline_access offline openid

   ENV NEXT_PUBLIC_NODEOPS_AUTH_URL=$NEXT_PUBLIC_NODEOPS_AUTH_URL
   ENV NEXT_PUBLIC_NODEOPS_CLIENT_ID=$NEXT_PUBLIC_NODEOPS_CLIENT_ID
   ENV NEXT_PUBLIC_NODEOPS_REDIRECT_URI=$NEXT_PUBLIC_NODEOPS_REDIRECT_URI
   ENV NEXT_PUBLIC_NODEOPS_SCOPES=$NEXT_PUBLIC_NODEOPS_SCOPES

   # Server-side vars — only needed at runtime, read per-request by API routes
   ENV NODEOPS_CLIENT_SECRET=""
   ENV NODEOPS_TOKEN_URL=https://id.nodeops.network/oauth2/token
   ENV NODEOPS_USERINFO_URL=https://autogen-v2-api.nodeops.network/v1/users/me

   RUN npm run build

   EXPOSE 3000
   CMD ["npm", "start"]
   ```

   Also ensure `.dockerignore` excludes `.env.local`:
   ```
   .env
   .env.local
   node_modules
   .next
   ```

   **If the project deploys to Vercel or similar**: no Dockerfile is needed — those platforms inject env vars before building automatically. Just remind the user to add the vars in their platform's dashboard.

10. **CreateOS / build-then-inject platforms** — CreateOS uses the Dockerfile when one is present, but injects env vars **after** the build step. This means `NEXT_PUBLIC_*` vars are `undefined` at build time even with ARG/ENV in the Dockerfile. Use the runtime config workaround below, or remove the Dockerfile entirely to fall back to CreateOS's default install/run commands.

    ### What the package handles automatically (v1.x+)

    `AuthProvider` from `@nodeops-createos/integration-oauth` v1.x+ auto-fetches `/api/config` at runtime if `NEXT_PUBLIC_*` vars are missing from the bundle. No extra setup is needed — just make sure the API route exists (step 10a below).

    ### If using an older package version, add manually:

    **10a.** Create `app/api/config/route.ts` (or `.js`):
    ```ts
    import { NextResponse } from 'next/server';

    export const dynamic = 'force-dynamic';

    export async function GET() {
      return NextResponse.json({
        NEXT_PUBLIC_NODEOPS_AUTH_URL:     process.env.NEXT_PUBLIC_NODEOPS_AUTH_URL     || 'https://id.nodeops.network/oauth2/auth',
        NEXT_PUBLIC_NODEOPS_CLIENT_ID:    process.env.NEXT_PUBLIC_NODEOPS_CLIENT_ID    || '',
        NEXT_PUBLIC_NODEOPS_REDIRECT_URI: process.env.NEXT_PUBLIC_NODEOPS_REDIRECT_URI || '',
        NEXT_PUBLIC_NODEOPS_SCOPES:       process.env.NEXT_PUBLIC_NODEOPS_SCOPES       || 'offline_access offline openid',
      });
    }
    ```

    This route reads `NEXT_PUBLIC_*` vars from the server environment at runtime (where they ARE available) and exposes them to the client via a JSON endpoint.

    **10b.** Create `components/EnvBootstrap.tsx` (or `.jsx`):
    ```tsx
    "use client";
    import { useEffect, useState } from "react";

    export default function EnvBootstrap({ children }: { children: React.ReactNode }) {
      const [ready, setReady] = useState(
        // If vars are already baked in (e.g. local dev), skip the fetch
        typeof window !== "undefined" && !!process.env.NEXT_PUBLIC_NODEOPS_CLIENT_ID
      );

      useEffect(() => {
        if (ready) return;
        fetch("/api/config")
          .then((r) => r.json())
          .then((env) => {
            // Patch process.env so AuthProvider picks them up
            Object.assign(process.env, env);
            setReady(true);
          })
          .catch((err) => {
            console.error("Failed to load runtime config:", err);
            setReady(true); // render anyway so error states show
          });
      }, [ready]);

      if (!ready) return null;
      return <>{children}</>;
    }
    ```

    **10c.** Update the root layout to wrap `AuthProvider` with `EnvBootstrap`:
    ```tsx
    import { AuthProvider } from '@nodeops-createos/integration-oauth';
    import EnvBootstrap from '@/components/EnvBootstrap';

    // inside <body>:
    <EnvBootstrap>
      <AuthProvider>{children}</AuthProvider>
    </EnvBootstrap>
    ```

    This ensures env vars are fetched from the server and patched into `process.env` before `AuthProvider` initializes on the client.

11. **Show a summary** — print a clear summary:
    - Files created/modified (list each one)
    - Files skipped (if any were already present)
    - Remind user to fill in the 2 required env vars: `NEXT_PUBLIC_NODEOPS_CLIENT_ID` and `NODEOPS_CLIENT_SECRET`
    - If a Dockerfile exists, remind that `NEXT_PUBLIC_*` vars must be set before `npm run build` in the Dockerfile
    - Show how to use the hooks in any page:
      ```tsx
      import { useAuth, useUser } from '@nodeops-createos/integration-oauth';

      const { isAuthenticated, login, logout, loading, authError } = useAuth();
      const { user } = useUser();
      ```
