# Speed on a phone (tap feedback and screen switches)

Lighthouse (`verify --only lighthouse`) scores the first load of public pages. It never taps a tab, never signs in, and never sees a slow server round trip between screens. This check covers that gap. Run it in every review and before every launch, on every main screen (each bottom tab or sidebar entry, and the main action screens), signed out and signed in.

## Budgets

| What | Budget | How it is measured |
|---|---|---|
| Tap to visible feedback (tab colour, pressed state, spinner) | under 100 ms | from the tap until the tapped item looks active |
| Tab or screen switch, data already visited | under 300 ms | from the tap until the real content shows (no skeleton) |
| Tab or screen switch, first visit | skeleton under 100 ms, content under 1 s | same, skeleton counted separately |
| Server response for one screen | under 300 ms to the first byte from the student's country | `curl -w "%{time_starttransfer}"` with the `RSC: 1` header |

Measure at 390x844 with touch and 4x CPU slow-down in Playwright: that is roughly a mid-range phone. `tap-timing.mjs` (next to this file) does it: `node tap-timing.mjs <base url> <first path> "Tab A,Tab B,Tab A,Tab C"`. It prints, per tap, the highlight time, the content time, how many requests went out, and what element is really under the tap point (to find covers).

## Rule for reviews

Measure every main screen before and after. Any screen over budget is a finding (strong area), fixed in the same review, with the before and after table in the pull request. A tab that "cannot be tapped" is first checked with the element-under-the-tap column: if the right link is there, it is a missing feedback problem, not a broken button.

## Common causes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Every screen slow, even simple ones; `x-vercel-id` shows `iad1` | Functions run in Washington (Vercel's default) while the database is in Europe; each query crosses the ocean, several times per page | `vercel.json` with `"regions": ["<region next to the database>"]` (Supabase eu-central-1 → `fra1`). The Shipyard template ships `fra1`. |
| The tab colour changes only when the next page arrives | Active state comes from the URL (`usePathname`), which changes after the server answers | Optimistic active state: set it on tap, clear it when the URL changes. Keep `aria-current` for the real page. |
| A tap does nothing for a second, then the page jumps | No `loading.tsx` for that route, or the route shares its boundary with the page it came from (an index page at the same level as its siblings) | A `loading.tsx` with a skeleton per tab; move an index page into a route group (`(overview)/page.tsx` + `loading.tsx`) so it gets its own boundary. |
| Going back to a tab already seen is as slow as the first time | Every page is `force-dynamic` and the browser keeps nothing | `experimental.staleTimes: { dynamic: 30 }` in `next.config.ts`; after a write that changes counts, call `router.refresh()` (for example when leaving a practice screen). |
| Many small sequential waits on the server | `await` chains: viewer, then library, then data, then the shell's own query | `Promise.all` for independent reads; `cache()` per request; start shell queries at the same time as page data. |
| Sticky bars or floating buttons swallow taps | A fixed element over the bottom bar (higher `z-index`, no `pointer-events: none` when hidden) | Check the element under the tap point; hidden floating buttons get `pointer-events: none`. |
| 300 ms delay or a double-tap zoom on taps | Missing `touch-action: manipulation` on tap targets | `touch-manipulation` (Tailwind) on nav links and buttons. |
| Big first load of one screen | A heavy client component (charts, editors, audio) in the main bundle | `next/dynamic` for that component, with a skeleton. |

## Privacy rules that run once per row

A slow screen with fast pages and few requests is often the database's privacy rules (RLS). A policy condition runs once **per row** unless Postgres can run it once per query. `has_access(library_id)` with a lookup inside cost one real app 0.6 to 0.9 s per query on 600 to 900 rows (ChatFix, fixed to 8 to 10 ms).

| Write | Never |
|---|---|
| `user_id = (select auth.uid())` | `user_id = auth.uid()` |
| `(select private.is_admin())` | `is_admin()` |
| `library_id in (select private.allowed_ids())`, where `allowed_ids()` is a `stable security definer` function with `set search_path = ''` that returns the ids the person may see | `has_access(library_id)` or any function given a column |

Index every column a policy compares (`user_id`, `library_id`, `org_id`). The template's `schema-rules` test flags per-row policies in new migrations. For a live project, `node rls-speed.mjs <project-ref>` (next to this file, needs `SUPABASE_ACCESS_TOKEN`) lists per-row policies and the Supabase performance advisor's `auth_rls_initplan` and unindexed foreign key findings, and exits 1 if there are any. To time one, run as a real member inside a rolled-back transaction: `begin; set local role authenticated; select set_config('request.jwt.claims', '{"sub":"<user id>","role":"authenticated"}', true); explain analyze select * from <table>; rollback;`. When rewriting a policy, hash every visible row (`md5(string_agg(t::text, ','))`) for several users and for anon before and after, and ship only when they match.
