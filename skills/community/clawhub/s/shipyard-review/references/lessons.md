# Lessons from a full review

From one full review of a big Next.js, Supabase and AI app (October 2026): 148 raw findings, 117 confirmed and fixed, then 14 regressions found in those fixes by the second review, shipped as 5 stacked pull requests, each deployed and smoke-tested. One line each. new-app's `references/build-rules.md` and `references/lessons.md` carry the ones every new app must follow; a star means Shipyard `verify` checks it.

## Build and CI
- ★ `next build` type-checks every `.ts` file, tests included, but `node --test` only strips the types. A typo in a test passes CI and breaks the production build. CI runs `tsc --noEmit` (`npm run typecheck`) before the tests.
- ★ Next 16 removed `next lint`. Run ESLint directly (`eslint .`).
- Never change the deploy build script or the deploy workflow in a cleanup pass, however much simpler it looks. Hosting settings may depend on it, and a mistake there only shows in production.
- Preview deploys may lack the database settings. Check with a local production build (`next build`, then `next start`) and placeholder keys.

## Security and correctness
- ★ A signed-out call to `/api/*` answers 401 with JSON, never a redirect to sign-in. The browser follows the redirect, gets a 200 page, and the app thinks the call worked.
- A delete or write with the server key that is driven by a value the user can change (a storage path, a file name) checks it first: the right prefix, the right owner. Tables like that are written only from the server.
- Never let the browser pick the AI model on the app's key. Allowlist model ids, rate-limit every AI, speech-to-text and text-to-speech proxy, cap request body sizes, and clean ids before putting them in a provider's URL.
- MCP servers cap the number of calls in one batch and charge the rate limit for each tool call, not each HTTP request.
- Lookups with a key the user typed use `Object.hasOwn` (`?error=__proto__` otherwise finds a built-in).
- Deleting data never resets monthly usage or quota counters. Otherwise "delete and re-upload" is unlimited use.
- Debounced saves flush on `pagehide` and `visibilitychange` with `keepalive`, or the last edit is lost when the tab closes.
- After renewing a signed media URL, restore the playback position once `loadedmetadata` fires; setting it earlier is ignored.
- Chunked uploads cap the size of each part, and the page does not let the person leave while parts failed.
- Theme CSS like `:root:is(...) button:not([class])` outranks a component's own rules. Exclude containers such as menus and toggles from it.
- Keep a deprecated way of signing in (`?token=`) working with a log line, instead of breaking clients that already use it.
- When a feature ships, update the home page, help, privacy page, `llms.txt`, structured data and manifest, in every language the app has.

## Speed
- Vercel runs functions in Washington (`iad1`) unless `vercel.json` sets `regions`. With the database in Europe every page makes several ocean crossings: put functions next to the database (`fra1` for eu-central-1).
- A bottom tab lights up on tap (optimistic state), every tab has its own `loading.tsx`, and visited tabs stay cached (`staleTimes`). Measure taps with `references/speed.md`; a tab that "cannot be tapped" was usually a tap with no feedback for over a second.

## Process
- Reviewers per area, the strongest model for security, live audio, AI and the database. Merge duplicates, then one skeptic per finding that tries to disprove it. About 85% of merged findings survived.
- Fix in waves whose batches share no file. Then a knip sweep for dead code, then a second, fresh review of the whole fix diff. Then type check, tests, build, a local production check and a real live session.
- Give every helper the absolute path of the worktree. Some drift into the main checkout otherwise.
- Another agent's commits may carry a different author email. List authors before choosing what gets extra scrutiny.

## Pull requests
- CodeRabbit's free plan skips pull requests over 150 files. Keep each one at 150 or fewer; ship a bigger release as a stack, merge each with a merge commit (a squash makes the next one show the earlier files again), change the next one's target to `main` after each merge, and smoke-test the live app between merges.
