# General app: the full Shipyard standard

Use this when `which-app.mjs` prints `general`. The app already exists and Shipyard did not make it. There is no `.shipyard-app.json`. That is normal.

This is a different procedure from design, ops, launch and video. Those scripts will refuse the folder. The refusal is expected. It is not a reason to stop, and it is not a reason to only change the easy things.

The result is the same standard as an app Shipyard made, fitted to this stack. Do the whole list. A colour tweak, a font swap, or a dark-mode line on its own is not finished work.

## What stays theirs

Their stack, their pages, their brand. Do not paste the Shipyard template over the app. Do not run `apply-design.mjs`, `ops-setup.mjs`, `ops-status.mjs`, `launch-check.mjs`, `verify.mjs`, or the provision scripts. Those need a Shipyard app. The video scripts are the one exception, and only after this whole guide is done (section 6).

## What they still get

All of it:

- Secrets stay out of git and out of the browser.
- Sign-in cannot be taken over from an email address alone.
- Each person only sees their own data (row level security, or the same rule in this stack).
- Paid calls have a cap.
- Tests exist, and a check runs on every pull request, including a leaked-key scan.
- The publishing branch is not where day-to-day work lands.
- Privacy, terms, a 404 page, a favicon, robots and a sitemap.
- Empty states, error states, system light and dark, no fake numbers, no em dashes in text people read. The behaviour rules in `build-rules.md`.
- A real look, proposed properly (three directions, light and dark), then built into their existing styles. Not a one-colour edit.

If they asked to review and improve the app, or to make it better, that is a yes to this whole list. Ask only before a step that spends money, takes a real payment, or deletes data.

## 1. Audit (read only)

Read the code. Answer with file names. Do not edit yet.

- **Secrets**: keys in tracked files, `NEXT_PUBLIC_` or similar prefixes on secrets, `.env` files in git, a `.gitignore` that covers them.
- **Sign-in**: passwords set from an email alone, redirect values not checked, login cookie handling, public versus protected routes.
- **Data isolation**: does each person only see their own data? Row level security on every table? Admin flags editable by users? Server key used in browser code?
- **Costs**: AI or paid API calls without caps, keys shared between apps.
- **Tests and checks**: tests exist and run? A test gate on pull requests? A leaked-key scan? Does CI run the type check (`tsc --noEmit`) before the tests? Is `next lint` still in `package.json` on Next 16 (it no longer exists)?
- **API routes and AI**: a signed-out call to an API route answers 401 JSON, not a redirect to sign-in. Server-key deletes or writes steered by a path the person can change check the prefix and owner. The browser cannot choose the AI model on the app's key; AI, speech and MCP routes have per-person rate limits and body size caps (MCP: a batch cap, a charge per tool call). Lookups with typed keys use `Object.hasOwn`. Deleting data does not reset usage counters. Debounced saves flush on `pagehide`.
- **Deploy**: pushing straight to the publishing branch, deployment protection, environment values.
- **Phone and behaviour**: phone layout, system light and dark, empty and error states, fake numbers or reviews, em dashes, the copy rules in `build-rules.md`.
- **Legal and basics**: privacy and terms pages, 404 page, favicon, robots, sitemap.
- **Look**: what is hard-coded, what is one accent with no dark pair, what a visitor cannot read. This feeds the proposal. It is not the whole job.
- **Lessons**: go through `lessons.md` and mark which apply.

For a big app (hundreds of files, several features) or after another agent added a lot of code, offer the review skill (`/shipyard:review`): it runs this audit with one helper per area and a skeptic for every finding, then fixes in waves and reviews the fixes again. It uses a large share of the student's plan, so say that first.

## 2. Report

A short list sorted by risk: **Fix now** (secrets, data leaks, account takeover), **Should fix**, **Nice to have**. For each: one plain sentence about what could go wrong for their users, then the file. End with what you could not check. Include the look and the non-visual gaps in the same list. Do not hide the hard ones.

## 3. Propose the look

Read the design skill's `references/propose.md` and `references/directions.md`. Draft three directions that are really different, each a light and dark pair. Use the app's real words.

`node "${CLAUDE_PLUGIN_ROOT}/scripts/theme-packs.mjs" mock <appDir>/.shipyard/design/directions.json --out <appDir>/.shipyard/design/directions.html`

That script does not need a Shipyard app. Show the page. When they pick one (or they already said to improve the look), write that pair into the app's own styles: colours, type, spacing, corners, buttons, empty states, light and dark. Do not run `apply-design.mjs`. If they only wanted the audit, stop after the report.

## 4. Do the rest

After the report, do every **Fix now** item, then **Should fix**, unless they named a smaller list. One area at a time. Smallest change that meets the rule. Add a test where there is logic. A look-only pass is not this step.

## 5. Stack differences

- **Next.js with Supabase**: use the template's pieces as the model (proxy, cookies, migrations with row level security, `secret-scan.mjs`, `.github/workflows/test.yml`, `AGENTS.md`). Copy the idea, adapt names.
- **Other stacks** (Flutter, plain HTML, other servers): no template. Turn each rule into a check that fits their stack, and say clearly what could not be automated. For mobile apps, a web version can be built later with `/shipyard:new-app` and share the same Supabase project.

## 6. Finish

Run the app's own tests. Summarise what now matches the standard and what is left, with the reason. Offer to record any new lesson in `~/.shipyard/learnings.md`.

When no **Fix now** item is left and the app is live, offer the video in one line, and start it only on a yes: "Want a short product video of your app with an AI voice (`/shipyard:video`)? It takes 2 to 4 hours of back-and-forth and a big share of your plan's usage, and the voice costs a few cents per minute." The video skill then runs its scripts with `--general` (see its "First: which app is this?"). Not before: a video brings visitors, so the app must be safe for them first.
