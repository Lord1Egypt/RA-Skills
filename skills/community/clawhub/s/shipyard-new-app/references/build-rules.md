# Build rules

Copy these into `SPEC.md` under "Hard rules" and follow them for every feature. The app's `AGENTS.md` repeats them for the coding agent.

## Data and keys
- Every table has row level security (RLS) switched on: the database itself only lets a person see and change their own rows. Add the table to `supabase/isolation.json`; the app's tests and the verify script fail without it. Policies use `(select auth.uid())` and `col in (select private.allowed_ids())`, never a function given a column, so they run once per query, not once per row; index the columns they compare.
- Database changes are new numbered files in `supabase/migrations/`. They can be run twice safely. Never edit one that already ran.
- If people may edit their own row but not every column (like an admin flag), limit the columns with grants. A row rule alone cannot do that.
- The server key lives only in server files. Never put a secret in a name starting with `NEXT_PUBLIC_`: that publishes it to every visitor.
- Never set or change a password from an email address alone. Passwords change only through the person's own session.
- Keys live in `.env.local` (never committed) and in Vercel settings. A leaked-key scan runs before every push and on every pull request.
- Every route under `/api/auth/` must be public in `src/proxy.ts`; other API routes need a signed-in person who finished setup (the proxy answers 403 `onboarding_required` otherwise; list setup-page APIs in `ONBOARDING_ALLOWED`).
- A cookie that skips a check (finished setup, age check) is signed with a server secret and bound to the user id. Never trust a plain value.
- A flag the client may set only under a rule (finished setup needs a name) is checked on the server and can never be set back; billing and counter columns are written only with the server key.
- Nothing changes on a GET (sign-out, delete, join, confirm are POST buttons). A one-time sign-in token is never used by opening a link: the link opens a page, and a button confirms. Mail scanners and crafted links fire GETs.
- Any link sent by email is built from the site address setting, never from the request's Host header. Check every `next` or redirect value points to the same site.
- Lists, totals and leaderboards read every row (the database returns at most 1000 per request) in a fixed order. Never trust one query for "all".
- Limits go on what strangers can trigger (sign-up, emails sent), never on the sign-in of someone who already has an account.
- If the app keeps score (points, streaks, correct answers), the server works it out and stores it. Answers and solutions never reach the browser before the person has played.

## Behaviour (pages)
- Each page sets its own canonical address (never one in the layout). A page that can say "not found" has no `loading.tsx`, so it answers 404 and not 200.
- The page never scrolls sideways, and the sticky header must stay stuck (`overflow-x: clip`, not `hidden`). The service worker caches built files and icons only.

## Costs
- Any AI feature has a spend limit at the provider, a per-app key, a daily cap inside the app, and a per-person limit.
- Do not build a feature that can run up a bill on anyone's key without a cap.

## Behaviour
- Brand name only from `BRAND` in `src/lib/constants.ts`.
- A designed empty state, loading skeleton and error message for every screen that loads data.
- Test with a real second account, not only simulated sessions. Do things in an unusual order too (play first then join a group, catch up on an old day) and check what each account sees of the other.
- Share and copy buttons always show a result: the share sheet on phones; on computers the button itself changes to "Copied!". If the browser blocks copying, show the text in a box to copy by hand. Never let a tap do nothing.
- One rule for what counts in stats, used on every screen (personal stats, group tables, leaderboards) and written in the help text. Things done late (an old day from the archive, offline, catch-up) still show up, marked as late; only streaks can be "on the day only".
- Apps built around content (a daily question, prompts, a quiz) launch with a full back catalogue and months of future content, and every fact has a source someone checked.
- Webhooks (later): check the signature, store event ids only after the change is saved, ignore out-of-order events, answer 500 on a database error so the sender retries.
- Webhooks out to an address the person typed: refuse private and local addresses after resolving the name, pin the checked IP, no redirects, timeout and size cap (see `api-and-mcp.md`).
- Analytics only after consent; paid plans show "Coming soon" until payments work.
- Work on a branch and open a pull request once the app is live; merge only on green checks.

## Copy and look (what visitors read)
- No fake numbers, fake reviews or invented testimonials. No "Made with AI" badges. No lorem ipsum.
- No purple gradients, no gradient card backgrounds. One accent colour.
- No em dashes in text people read. Use commas or full stops.
- No explanatory sentences in menus, no subtitle that repeats the title, no "Tip:" boxes, no developer words (API, token, schema, RLS) where visitors can see them. If something needs explaining, one plain line, or a small "?" that opens a popover on tap (never hover only: phones cannot hover).
- Legal links live in the account menu, not in a crowded footer.
- Touch targets at least 48px. Inputs at least 16px so iPhones do not zoom. Light mode by default with dark mode available, no flash on load.
- Do not hardcode copy that is really data. Do not show debug or backend wording to visitors.
- Phone-first does not mean phone-only. On a computer (1024px and wider) the app uses the screen: the tab bar becomes a left rail and pages use the content width. Do not wrap pages in a narrow `max-w-md mx-auto` column; lay lists out as a wider table or a grid of cards on big screens. Look at a 1440px wide screenshot too, and compare with how big comparable apps look on a desktop.
- Switching tabs must feel instant: every signed-in page folder has a `loading.tsx` that returns `<PageLoading />`, and data loads in the page, not in shared layouts.
- Before saying ready, look at the home page on a phone width and check it against this list.

## Lessons from the Oct 2026 audit of the 6x7 apps (each one is also caught by `verify --only hygiene`)
- Every link and button has a name a screen reader can read. An icon-only control, or a logo link whose text is hidden at phone size (`max-[430px]:hidden`), gets `aria-label` (logo: `` aria-label={`${BRAND.name} home`} ``). Lighthouse calls this "link-name" / "button-name".
- Private (noindex) is a choice the owner makes, not a default. Scaffold with `--private` only when they say the app is private; otherwise public pages (home, about, help, pricing, legal, sign-in) are indexable and in the sitemap, and signed-in routes are disallowed in robots.txt.
- CI must be able to pass on main: commit `package-lock.json` and re-run `npm install` after any dependency change (`npm ci` fails on drift); no `uses: ./local-action` that is not in the repo; in a workspace repo, build the workspace packages before the tests (`npm run build --workspaces --if-present`). No deploy workflow when Vercel deploys from GitHub; a build check is enough.
- API routes, sign-in ones above all, never read env vars with `!`. When Supabase is not configured (preview, CI), answer cleanly: "no user" or a 503 with a message, never a crash.
- Themes: one look = a light and dark pair (a pack). Extra looks only on request, always as packs in Settings > Appearance; never a theme that locks the mode (see the design skill).
- Optional extras (blur, glow, grain, sound) default off.
- Lighthouse budgets on public pages: performance 90 (phone), accessibility 95, best practices 95, SEO 90. See `launch/references/seo-performance.md`.

### From the Praiser fix (Oct 2026)
- No fake ARIA roles: `role="tablist"` only with real `role="tab"` children, `aria-selected` and arrow-key handling; otherwise plain buttons with `aria-pressed`. Same for `menu`/`menuitem`. (hygiene fails on it.)
- Faint grey text must still reach 4.5:1 contrast against its background, in light and dark. Muted text is where every theme fails first. (Lighthouse color-contrast.)
- A Content-Security-Policy with `script-src` (nonce from `src/proxy.ts`), not only `frame-ancestors`. (hygiene warns; Lighthouse csp-xss.)
- Animate only `transform` and `opacity`. A highlight that animates `border`, `width`, `box-shadow` or colours runs on the main thread; use a scaled pseudo-element. (hygiene warns; Lighthouse non-composited-animations.)
- Touch targets at least 48x48px with 8px apart.
- A floating input or bar fixed to the bottom on phones reserves its height (`padding-bottom` on the page, plus `env(safe-area-inset-bottom)`) so it never covers the last content or the on-screen keyboard's field.
- Every CI job you add must actually run: after the first push, `gh run list --workflow <file> --branch main` shows a run that executed its steps (not skipped, not failing at setup). A Lighthouse job that starts the app from a wrong path or URL never scores anything and hides problems for months.

### From the Lighthouse sweep of all apps (Oct 2026)
- Never lock zoom: no `maximumScale: 1`, `userScalable: false` or `user-scalable=no`. (hygiene fails on it; Lighthouse meta-viewport.)
- Every app has a meta description (Next `metadata.description`, or `<meta name="description">` in a Vite `index.html`). (hygiene fails without it.)
- A single-page app whose `vercel.json` rewrites every path to `index.html` ships a real `public/robots.txt`; otherwise `/robots.txt` returns the app page. (hygiene fails on it.)
- The accent colour is rarely readable as small text on the dark background. Use a separate `--accent-text` (in dark, mixed toward the text colour) for accent-coloured words and links. (hygiene fails when `color: var(--accent)` is under 4.5:1 in dark.)
- Small controls (checkboxes, calendar/habit cells) still get a 24px hit area: draw the small visual with a pseudo-element.

### From a full review of a big app (Oct 2026; the review skill's `references/lessons.md` has the rest)
- CI runs `npm run typecheck` before the tests. `next build` type-checks every `.ts` file, tests included, but `node --test` only strips the types, so a typo in a test passes the tests and breaks the production build. Next 16 has no `next lint`: run ESLint directly. (hygiene fails on both.)
- A signed-out call to `/api/*` gets 401 JSON, never a redirect to sign-in: fetch follows the redirect, gets the sign-in page with status 200, and the app thinks it worked. (verify's routes check calls the live app.)
- A delete or write with the server key that a person-controlled value steers (a storage path, a file name) checks the value first: the expected prefix and the owner. Tables like that are written only from the server.
- The browser never picks the AI model on the app's key: allowlist model ids on the server. Every AI, speech-to-text and text-to-speech route has a per-person rate limit and a body size cap, and ids that go into a provider's URL are checked first.
- An MCP endpoint caps how many calls one batch may hold and charges the rate limit for each tool call, not for each HTTP request.
- Lookups with a key the person typed use `Object.hasOwn` (`?error=__proto__` otherwise finds a built-in).
- Deleting data never resets usage or quota counters.
- Debounced saves flush on `pagehide` and `visibilitychange` with `keepalive`. After a signed media URL is renewed, the playback position is restored once `loadedmetadata` fires. Chunked uploads cap the size of each part, and the page warns before leaving while parts failed.
- Theme CSS like `:root:is(...) button:not([class])` outranks a component's own rules: exclude menus, toggles and other containers from it.
- A sign-in method being retired (`?token=` links) keeps working with a log line until clients move, instead of breaking them.
- When a feature ships, the home page, help, privacy page, `llms.txt`, structured data and manifest change with it, in every language the app has.
- Keep each pull request at 150 changed files or fewer (CodeRabbit's free plan skips bigger ones); ship a bigger release as a stack and smoke-test the live app between merges. Never change the build script or deploy workflow in a cleanup.
