# Choosing the review areas

An area is one part of the app that one reviewer reads closely: sign-in, the database rules, the AI calls, uploads. Small areas find more than big ones, because a reviewer that has to read everything skims.

## Start from the example

`${CLAUDE_PLUGIN_ROOT}/skills/review/examples/nextjs-supabase-areas.json` lists 17 areas for a Next.js and Supabase app with AI features, written for the Shipyard template's folders (`src/app`, `src/lib`, `src/proxy.ts`, `supabase/migrations`). Copy it to the scratch folder and edit it for this app:

- Drop areas the app does not have (payments, live audio, more than one language). Leaving them in costs usage and finds nothing.
- Replace folder names with the real files. Look at the tree first (`git ls-files | head -200`, the `src/app/api` folder, the migrations). A scope that names real files gets a much better review.
- Split an area that covers more than about 40 files. Merge two areas that together cover fewer than 10.
- Say what each area should look for, in one or two sentences. The example's scopes show the kind of failures that were real in a big app.

Each area is `{ "key": "short-name", "strong": true or false, "scope": "files and what to check" }`. `strong: true` means your strongest model: use it for sign-in, API routes, the database, sharing, AI and keys, and live or realtime features. Everything else gets a cheaper model.

## Size it

| App | Areas | What it costs |
| --- | --- | --- |
| Small (under about 50 source files) | 4 to 6: sign-in and API routes, database, the main feature, tests and cleanup | a moderate share of a plan; fine on most paid plans |
| Medium | 8 to 12 | a large share of a plan; do it on a day with room |
| Big (hundreds of files, several features) | 15 to 20 | the biggest plans only, or split it over several days (security areas first) |

Other ways to make it cheaper: `maxPerArea: 8` in the review arguments, and a review of only the code another agent added (`focusAuthor`, with areas that cover only those files).

## Known issues are not findings

Pass the app's open-items or known-issues doc as `openItems`. Reviewers skip what is listed there, and skeptics refute it. Without it, the same old problems come back in every review.
