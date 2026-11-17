---
name: new-app
description: Build and publish a new web app, or bring an existing app up to the full Shipyard standard (secrets, data rules, tests, deploy, legal pages, and a proposed look). Use for "new app", "build me an app", "make a website", "publish my app", "upgrade my app", "review my app", "review an existing app", "run Shipyard on this app", or "improve this app". If the folder has no .shipyard-app.json, follow references/upgrade.md. Do not stop.
---

# Shipyard new app

> Part of the Shipyard plugin. This skill runs Shipyard's own scripts and key guard, so it does not work on its own. If it was installed by itself (for example through skills.sh, ClawHub, Hermes, pi or aiden) and Shipyard's `scripts/` folder is not on this computer, stop and install the full plugin first by following https://github.com/philipposk/shipyard/blob/main/INSTALL.md, then start again.

You build a real app from an idea and publish it, then prove it works. The student describes what they want in plain words; you do everything technical.

## First: which app is this?

When the current folder is an app that already exists, run `node "${CLAUDE_PLUGIN_ROOT}/scripts/which-app.mjs" <app folder>` before the steps below.

- The output says `shipyard`: Shipyard made it. If they asked to review it or bring it up to standard, read `references/upgrade.md` and follow it. If they asked for a new app, continue below.
- The output says `general`: this is an existing app Shipyard did not make. Do not stop. Do not say design, ops or launch cannot run and then only change the easy things. Those scripts will refuse; that is expected. Read `references/upgrade.md` and follow it. That path proposes a real look and brings secrets, sign-in, data isolation, costs, tests, deploys, legal pages and the other build rules up to the same standard.
- The output says `damaged`: `.shipyard-app.json` is here but broken. Say so. Do not treat the folder as a general app.
- There is no app folder yet, only an idea: continue below.

## Rules (always)

- You do the work. Run scripts and commands yourself. Never hand the student a command you could run.
- Never ask for keys in the chat and never read `~/.shipyard/secrets.env` or `.env*` files. Scripts handle keys and print only names with a tick or a cross.
- Plain English, short messages, one question at a time with your recommended answer.
- Verify before saying done. Say what was checked and what was not.
- Commits and pushes are the student's call: always ask "OK to save this to GitHub?" first. Never push to a branch that publishes automatically once the app is live; use a branch and a pull request, and merge only when the checks are green.
- Save the student's usage: give helper agents one model cheaper than yours, and only for mechanical work. If you run on Opus, helpers use Sonnet (`model: "sonnet"`) for builds, test runs, searches, doc and copy edits, simple UI fixes. If you run on Sonnet, helpers use Haiku only for lookups (finding files, listing things) and code edits stay on Sonnet. Keep sign-in, data privacy (RLS), keys, payments and the final check on your own model. At most a couple of helpers at a time, and re-check their "done" yourself.
- Progress is saved in the profile (`apps[].step`). If the usage limit hits, "run it again later" is enough.

## 0. Check setup

Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/setup-status.mjs"`. If GitHub, Vercel or Supabase are not done, offer `/shipyard:setup` and stop. Check `node "${CLAUDE_PLUGIN_ROOT}/scripts/profile.mjs" show` for an app already in progress (a `step` that is not empty): offer to continue it.

If the student wants to improve an app they already have, read `references/upgrade.md` and follow it instead of the steps below.

## 1. Interview

Read `references/interview.md`. Ask at most 5 questions, about outcomes not technology (who it is for, the one main thing they do, free or paid or email list, installable on phones, a look they like). Rambling answers are fine. If the app would be better with AI, needs speech-to-text or should be usable by other tools or AI assistants, read `references/ai-and-keys.md` and `references/api-and-mcp.md`. Pick the layout from the profile default or ask: `bottom-nav` for phone-first apps, `sidebar` for tools and dashboards, `top-nav` for site-like apps (links in the top bar, tabs on phones).

## 2. Spec and plan

Read `references/build-rules.md`. Choose a short slug (lowercase letters, numbers, hyphens, starts with a letter). Make a folder for the app, then write `SPEC.md` in it: who it is for, the main action, the list of features (small steps), what data is stored, and the hard rules from build-rules. Add a plan of 5 to 8 steps in plain words. End the plan with the 3 best feature ideas for later (see `references/ai-and-keys.md`). Show it and wait for the student to say "go". Nothing is built before that.

## 3. Scaffold

`node "${CLAUDE_PLUGIN_ROOT}/scripts/scaffold.mjs" <slug> --name "<Name>" --description "<one sentence>" --dir <parent folder> --layout <bottom-nav|sidebar|top-nav>`
Add `--private` if the app is for the student only (hidden from search engines), `--no-pwa` if it should not be installable. Then work inside the new folder and move `SPEC.md` into it. Design: if the profile has a default look (`defaults.design`), apply it silently with `node "${CLAUDE_PLUGIN_ROOT}/scripts/apply-design.mjs" <appDir> --preset <id>` and say which look you used. Otherwise run the design skill and ask its one question ("How do you want to choose the look?"); if the student has no preference, the starter look stays and they can change it any time with `/shipyard:design`. Run this after the scaffold and before building features, so every screen uses the chosen look. A look sets the menu style too, so skip the layout question if a look is chosen.

## 4. Build the features

Follow the app's `AGENTS.md`. Small steps. Every piece of logic gets a test. When a feature needs an AI, speech or other service key, give the app the key with `node "${CLAUDE_PLUGIN_ROOT}/scripts/app-keys.mjs" <appDir> <KEY_NAME>` (never ask for keys in the chat). Every new table follows the database rules (row level security, an entry in `supabase/isolation.json`, a numbered migration file). Run `npm install` first, then `npm run typecheck`, `npm run lint` and `npm test` after each feature.

Before the first deploy, always write `src/lib/home-content.ts` for this app: the headline, the subline, the three points, and the `preview` rows (3 to 5 sample rows of the app's real main feature, for example a note and its day). The template's stand-in words must never reach a live homepage.

## 5. Database

`node "${CLAUDE_PLUGIN_ROOT}/scripts/provision-supabase.mjs" <appDir>`
It creates the Supabase project, applies the migrations and writes `.env.local`. If it says two projects are already active (free limit), explain the two choices in plain words: pause a project the student does not use (dashboard link in the message), or put this app in an existing project with `--shared <project id>`. Shared is safe for the other apps: the app gets its own space (a separate schema) and nothing of theirs is touched. Before any shared run, read `references/shared-project.md` and do the dry run first. If the apps sit on subdomains of one domain and should share one sign-in, also read `references/shared-sign-in.md`. The template's `vercel.json` runs the server next to a database in eu-central-1 (`fra1`); if the database is elsewhere, set `regions` to the Vercel region nearest it (for example us-east-1 → `iad1`). Then run `npm run build` to check the app builds.

## 6. Save to GitHub

Ask: "OK to save this first version to GitHub?" If yes: `git add -A`, check nothing secret is staged (`node scripts/secret-scan.mjs --staged` inside the app), `git commit`, then `gh repo create <slug> --private --source . --push`. The branch must be called `main`. `package-lock.json` must be included.

## 7. Publish

1. `node "${CLAUDE_PLUGIN_ROOT}/scripts/provision-vercel.mjs" <appDir>` (links Vercel, sets the environment values, turns off the login wall that would block visitors). It also connects GitHub. If it says it could not, fix that now (`vercel git connect --yes` in the app folder) and check the Vercel project's Git settings show the repo with production branch `main`. Otherwise later merges never go live.
2. `node "${CLAUDE_PLUGIN_ROOT}/scripts/deploy.mjs" <appDir>`. It refuses if there are unsaved changes; save and push first. It prints the address and adds it to the sign-in settings.

## 8. Verify

`node "${CLAUDE_PLUGIN_ROOT}/scripts/verify.mjs" <appDir>`
Read `references/verify.md` for what each check means and how to fix a failure. Fix, save, redeploy and re-run until all checks are green, or explain plainly what is left and why. Then run `SUPABASE_ACCESS_TOKEN=... node "${CLAUDE_PLUGIN_ROOT}/skills/review/references/rls-speed.mjs" <project-ref>` and fix every per-row policy it lists (see `skills/review/references/speed.md`). Look at the two phone screenshots it saves (light and dark) and say if anything looks wrong. Do not say the app is live until the checks pass on the real address. After any fix, run verify again and read the fixes once more before launch: a clean run from before the fix proves nothing about the fix.

## 9. Owner account

`node "${CLAUDE_PLUGIN_ROOT}/scripts/make-owner.mjs" <appDir> --url <address>`
It makes the student's own account (their email from the profile) with the app's secret key, switches on the admin flag and opens a one-time sign-in window in their browser. The app refuses sign-ups with that email on purpose: starter-mode sign-up does not check that the person owns the email, so a stranger could otherwise take the owner's address first. Admin is the `is_admin` flag only, never an email. Never print or paste the link. If the account already existed and the student did not make it, run it again with `--reset-password` (not allowed in a shared project: the account is shared with the other apps there).

## 10. Hand off

- Write `HANDOFF.md` in the app: what is where, how to run the checks (the exact verify command), how to make changes (branch, pull request, green checks, merge), and the known limits. Always include: "Starter mode: anyone can sign up without email confirmation, and the email they type is not checked. Never trust an email address as proof of who someone is. The owner account was made by Shipyard (`make-owner.mjs`) and admin comes only from the `is_admin` flag. Google sign-in stays off, and email sign-up is switched off if you turn it on, until real email confirmation works. `/shipyard:launch` sets that up."
- Update the profile (`status: live`, last step) via the scripts; do not edit profile.json by hand.
- Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/build-story.mjs" <appDir>`: it writes `BUILD-STORY.md` (the cleaned prompts, how many, tokens, estimated cost per model, time per step). Show the totals in one line. Steps marked (fix) are corrections: for each one Shipyard should have known, add a learning (next point). Never publish the story without the student reading it first.
- If you learned something that would help future apps (a mistake and its fix), append one line to `~/.shipyard/learnings.md`. Read `references/lessons.md` only when you need to check a past lesson.
- Final message: the address, what was verified, what was not, and what the student does next ("to change anything, tell me what you want"). Keep it short. End with what is next: "When you want your own web address, real sign-up emails, privacy and terms pages, payments, an email list, or phone and desktop apps, run `/shipyard:launch`. `/shipyard:ops` sets up error alerts, scheduled health checks, code review on pull requests, safe auto-merge and backups." Then offer the video in one line, and start it only on a yes: "Want a short product video of your app with an AI voice (`/shipyard:video`)? It takes 2 to 4 hours of back-and-forth and a lot of Claude usage, the voice costs a few cents per minute, and it is best done after launch."

## After go-live: the CI gate

The app has a test gate that GitHub runs on every pull request (types, style, tests, full build, leaked-key scan). From now on: new branch, small change, pull request, wait for the green tick (`gh pr checks --watch`), then merge. GitHub cannot block a merge on a free private repository, so you keep this rule yourself: never merge while red.
