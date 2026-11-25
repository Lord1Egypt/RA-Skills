---
name: review
description: "Review, fix and ship a whole web app with many helper agents: one reviewer per area, a skeptic that tries to disprove every finding, fixes in waves that never touch the same file, a dead-code sweep, a second review of the fixes, a local production check, a live microphone test, and stacked pull requests under the 150-file review limit. Works on apps Shipyard made and on any other app. Use for \"review the whole app\", \"full audit\", \"check everything another agent added\", \"audit, fix and clean\", \"release check\", \"is my app ready to ship\", or \"/shipyard:review\"."
---

# Shipyard review

> Part of the Shipyard plugin. This skill runs Shipyard's own scripts and key guard, so it does not work on its own. If it was installed by itself (for example through skills.sh, ClawHub, Hermes, pi or aiden) and Shipyard's `scripts/` folder is not on this computer, stop and install the full plugin first by following https://github.com/philipposk/shipyard/blob/main/INSTALL.md, then start again.

You check a whole app the way a careful team would before a big release: many reviewers, each on one part of the app, then a skeptic for every problem they report, then fixes, then a fresh review of the fixes, then real checks. The student gets a list of what was wrong in plain words, the fixes as pull requests small enough to review, and a short list of what is left. This is the biggest thing Shipyard does, so it is for an app that already works, before a release or after another agent added a lot of code.

## First: which app is this?

Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/which-app.mjs" <app folder>` on the current folder when that folder is the app.

- The output says `shipyard`: this folder was made by Shipyard. Continue with the steps below. Step 8 also runs Shipyard `verify`.
- The output says `general`: an existing app Shipyard did not make. Do not stop. The review works on any app in git: use the app's own type check, tests and build in place of `verify.mjs` (which needs a Shipyard app). After step 12, offer new-app's `references/upgrade.md` for anything the Shipyard standard still lacks.
- The output says `damaged`: `.shipyard-app.json` is here but broken. Say so. Do not treat the folder as a general app.

## Rules (always)

- You do the work. Run every script yourself. Never hand the student a command you could run.
- Plain English, short messages, one question at a time with your recommended answer. Explain any new word in five words or fewer ("a worktree: a second copy of the code").
- Warn before step 3, and wait for a yes: a full review of a big app runs a hundred or more helper agents and uses a large share of the student's plan. Offer the small version (`references/areas.md`, "Size it") when their plan is small or the app is.
- Review and fix in a fresh worktree made from the latest `origin/main`, never in the student's own folder. Give every helper the worktree's absolute path and tell it never to read another checkout.
- Helper agents: your strongest model for sign-in, data rules, live audio, AI costs and the database, and for the final yes or no; a cheaper one for the other areas and for mechanical work (builds, test runs, searches).
- Never change the deploy build pipeline (build script, deploy workflow, hosting settings) during a review or a cleanup.
- Never open, print or search `~/.shipyard/secrets.env`, `.env.local` or any `.env` file other than `.env.example`.
- Commits, pushes, pull requests and merges: ask first, once per action. Never push to `main`. Merge one pull request at a time, and only after the one before it deployed and passed its smoke test.
- A helper's "fixed" or "passed" is a lead, not proof. Re-check before saying done, and say what was not checked.

## Steps

Read `references/workflows.md` before step 3: it says how to run the helper workflows here and what to pass them.

1. **Scout.** Fetch every branch, make the worktree from `origin/main`, install (`npm ci`), then take a baseline: type check (`npx tsc --noEmit`), every test suite, a full build with placeholder keys. Check that the latest production deploy finished; a failed one can sit there unnoticed.
2. **Whose code.** List commit authors (`git log --format='%ae' | sort | uniq -c`). Another agent often commits under its own email; its recent work gets extra scrutiny. Read the app's open-items or known-issues doc so nothing known is reported again.
3. **Review.** Pick the areas (`references/areas.md`; the example `${CLAUDE_PLUGIN_ROOT}/skills/review/examples/nextjs-supabase-areas.json` has 17 for a Next.js and Supabase app with AI). Run the review workflow. Expect most findings that survive the merge of duplicates to survive the skeptic too.
4. **Content gaps** (at the same time as 3). Compare what shipped with what the home page, help, privacy page, onboarding, `llms.txt`, structured data, manifest and README say, in every language the app has. The privacy page must name every new kind of data captured and every outside AI or email service it goes to.
5. **Decide.** Read the confirmed list. Choose sensible defaults for the decisions it needs and write them down; move big or risky changes to the open-items doc instead of fixing them now. Show the student the list, worst first, one line of user impact each with its `id`, and ask which to fix (recommend: all confirmed, minus the deferred ones).
6. **Fix.** `node "${CLAUDE_PLUGIN_ROOT}/scripts/review/plan-waves.mjs" <review.json> --repo <worktree> --strong <areas> --skip <ids of deferred findings>` splits the fixes into waves that never share a file and leaves out what step 5 deferred; then run the fix workflow. Findings under "unverified" (their skeptic failed) get checked by hand first. If a helper dies halfway, start a new one that first reads that batch's partial diff.
7. **Review the fixes.** Run the diff review with the changed files grouped by area, new untracked files included. Never skip this: fixes bring new bugs. Rerun any area whose reviewer failed.
8. **Check.** Type check, every test suite and a full build must pass. Then the local production check in `references/ship.md`. For a Shipyard app, also run `node "${CLAUDE_PLUGIN_ROOT}/scripts/verify.mjs" <app folder>`. Then measure every main screen on a throttled phone (`references/speed.md`), signed out and signed in; a screen over budget is a finding to fix now, with before and after numbers in the pull request.
9. **Docs.** README against the code, the open-items doc (decisions, leftovers, what shipped), the app's `AGENTS.md` rules, `.env.example` with every variable the code reads.
10. **Ship.** Read `references/ship.md`. With a yes: commit (urgent fixes first), split into stacked pull requests if the change is over 150 files, push and open them. Merge one at a time, with a merge commit, each only with a yes and after the one before deployed and passed its smoke test.
11. **Live test** (apps that record from a microphone). After the live part deploys, run the voice test in `references/ship.md` and check the saved result. Tell the student a test record was created.
12. **Share.** Write what this review taught into the app's `AGENTS.md` and `~/.shipyard/learnings.md`, and tell the student what is left and why.

`references/lessons.md` holds the rules every app should follow after a review like this. Use it in steps 3, 5 and 7.

## Done when

- Every confirmed finding is fixed, deferred with a written reason, or waiting for a decision the student was asked about.
- The fixes were reviewed a second time, and type check, tests and build pass on every pull request.
- The deployed app passed its smoke test after each merge (and the live test, where it applies).
- The student knows what was found, what changed, what is left, and what was not checked.
