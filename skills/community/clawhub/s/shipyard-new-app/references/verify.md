# Verify

Run: `node "${CLAUDE_PLUGIN_ROOT}/scripts/verify.mjs" <appDir>` (add `--url <address>` if the address is not saved yet, `--only routes,auth` to re-run some checks). It prints a tick or cross per check, plus what it could not check and why. It saves `<appDir>/.shipyard/verify.json` and writes the result to the profile. Exit 0 = every check that ran passed; exit 1 = a check failed, or nothing could be verified (no check ran, or a check you picked with `--only` was skipped). A line that says NOT VERIFIED or NOT FULLY VERIFIED is not a pass: do not tell the student the app works. An app that shares its Supabase project with other apps (`--shared`) skips the `auth` and `isolation` checks unless you add `--allow-test-users`: a test user runs the other apps' sign-up triggers, so it only happens when the owner agrees. Say so; do not call those checks passed.

Re-run after every fix. "Vercel says ready" is not proof; only the real address passing is.

| Check | What it proves | If it fails |
|---|---|---|
| hygiene | Every link and button has a readable name (logo text hidden on phones counts as none); no tablist/menu roles without their items; warns on non-composited animations and a missing script-src CSP; CI can pass (local actions exist, lock file matches package.json, workspace packages built before tests); sign-in API routes do not crash without env vars; zoom is not locked; there is a meta description; an SPA catch-all rewrite has a real public/robots.txt; accent-coloured text is readable in dark mode. Warns when the app is marked private (noindex), when robots, sitemap or metadataBase/canonical are missing, when the root layout or home page hard-codes noindex outside the private switch, when a shared-project app's auth cookie has no domain, and when public/ has images but no IMAGE-SOURCES.md licence log | Add `aria-label`; run `npm install` and commit the lock file; add the build step; guard the env vars. Private warning: ask the owner, delete the marker to go public |
| lighthouse (only with `--only lighthouse`) | Lighthouse on `/`, `/about`, `/sign-in`, phone and desktop: performance 90, accessibility 95, best practices 95, SEO 90 (SEO skipped for private apps) | Fix the audits it names (see `launch/references/seo-performance.md`), redeploy, re-run |
| routes | Home, about, help, privacy, terms, sign-in, manifest, icons, robots, sitemap and llms.txt answer 200; a made-up page gives a styled 404 with the app name; sign-up is not blocked | A route 404 or 500: look at the page file. Sign-up 405: the route is not public in `src/proxy.ts` |
| protection | Visitors are not stopped by a Vercel login wall | Run `provision-vercel.mjs` again, or turn off Deployment Protection in the Vercel project settings (the script prints the click path) |
| auth | A throwaway user can be created, sign in, load their profile and sign out | Cookie name in `proxy.ts` must match `src/lib/supabase/cookies.ts`; check Supabase redirect URLs include the app address (`deploy.mjs` adds it) |
| isolation | User B cannot see, change or delete user A's rows when asking the database directly; signed-out visitors see nothing. It does not call the app's own API routes, which is why `secrets` also bans the server key outside a few files | A table lacks row level security or has a too wide rule. Add a migration; never loosen the test |
| browser | At phone size, light and dark: no console errors, no failed requests, no sideways scrolling; two screenshots saved | Fix the error shown. If skipped, run `npm install` in the app (Playwright) and `npx playwright install chromium` |
| proxy | `src/proxy.ts` exists, exports `proxy`, covers every `/api/auth/*` route, cookie name matches | Add the missing prefix to `PUBLIC_PREFIXES` |
| secrets | No key-shaped text in tracked files; `.env` and `.env.local` are not tracked; the secret server key (`@/lib/admin`, `createSupabaseAdmin`, `SUPABASE_SERVICE_ROLE_KEY`) is used only in `lib/admin.ts`, `lib/auth/*` and the sign-up and forgot-password routes | For the server key: use the signed-in person's own client (`createSupabaseServer`) in routes and server actions, so the database privacy rules apply. For keys: remove the key from the file, rotate it at the provider (a leaked key counts as stolen), and if it was committed ask before rewriting history |

## Reporting

- CI counts only if it ran: for each workflow, `gh run list --workflow <file> --limit 1` must show a completed run whose steps executed. A job that was skipped, never triggered, or failed at setup (wrong path, missing action) is NOT VERIFIED.

- After you fix anything verify or a review found, re-run the review on the fixed code (verify again, then read the diff of the fixes) before launch. Fixes bring new bugs, and a clean run from before the fix proves nothing about the fix.

- Say which checks passed and which were skipped, with the reason.
- Show the screenshot paths and say what you see. If you did not look, say so.
- Things verify does not cover: forgot-password email (needs a verified domain), Google sign-in, payments, real devices, accessibility. Say "not verified" for what applies.
