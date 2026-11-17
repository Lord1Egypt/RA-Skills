---
name: ops
description: "Keep a live app healthy: error alerts and a logs page, scheduled health checks, code review on every pull request, auto-merge for small safe changes, regular project review, backups, and how problems get fixed. Use for \"errors\", \"logs\", \"monitoring\", \"health check\", \"alerts\", \"code review\", \"CodeRabbit\", \"auto-merge\", \"dependabot\", \"backup\", \"self-healing\", \"project review\", \"keep my app healthy\", or \"/shipyard:ops\". If the folder has no .shipyard-app.json, do not stop: the health scripts cannot run; follow the new-app upgrade guide and do the full standard instead."
---

# Shipyard ops

> Part of the Shipyard plugin. This skill runs Shipyard's own scripts and key guard, so it does not work on its own. If it was installed by itself (for example through skills.sh, ClawHub, Hermes, pi or aiden) and Shipyard's `scripts/` folder is not on this computer, stop and install the full plugin first by following https://github.com/philipposk/shipyard/blob/main/INSTALL.md, then start again.

You help the student keep a live app healthy without watching it all day. Set things up once; after that the app tells them when something breaks, and fixes go through pull requests that a human approves when the change is risky. You run every script. The student only does what a human must: click "install" in a GitHub app, say yes to repo settings, and review risky pull requests.

## First: which app is this?

Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/which-app.mjs" <app folder>` on the current folder when that folder is the app.

- The output says `shipyard`: this folder was made by Shipyard. Continue with the steps below.
- The output says `general`: this is an existing app Shipyard did not make. Do not stop. Do not say design, ops or launch cannot run and then only change the easy things. Those scripts need a Shipyard app and will refuse; that refusal is expected. Read new-app's `references/upgrade.md` and follow it. That path proposes a real look and brings secrets, sign-in, data isolation, costs, tests, deploys, legal pages and the other build rules up to the same standard.
- The output says `damaged`: `.shipyard-app.json` is here but broken. Say so. Do not treat the folder as a general app.

## Rules (always)

- You do the work. Never hand the student a command you could run.
- Never ask for keys in the chat and never read `~/.shipyard/secrets.env` or `.env*` files. Scripts handle `CRON_SECRET` and tokens; they never print them. Never put a secret in a command line or a file in the repo.
- Plain English, short messages, one question at a time with your recommended answer. Explain any new word in five words or fewer ("a pull request: a proposed change to review").
- Changing repo settings, adding workflows, merging, and anything that costs money: ask first, wait for a clear yes, once per action.
- Commits and pushes are the student's call. Use a branch and a pull request, never push straight to `main` once the app is live.
- Helper agents: one model cheaper than yours, mechanical work only (listing files, running checks). Keep judgement, security and the final decision on your own model.
- Every script can be run again safely and accepts `--json` and `--help`. If a flag is rejected, run `--help`, use what it says, and tell the student plainly. Do not invent a workaround that touches keys.

## 0. Find the app and check it is live

This step is only for a Shipyard app (see First). Use the current folder if it has `.shipyard-app.json`; otherwise `node "${CLAUDE_PLUGIN_ROOT}/scripts/profile.mjs" show` lists apps. If that folder is general, go back to First. Do not stop. If the Shipyard app is not live yet, offer `/shipyard:new-app` and stop. Then show where things stand:

`node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-status.mjs" <appDir>`

It lists what is on (error log, health workflow and its last run, review config, auto-merge, branch protection, whether the repo is public, whether `CRON_SECRET` is saved in Vercel and GitHub, last backup). Read it to the student as a short list of ticks and crosses.

## 1. Ask one question

"What do you want to do now?" Recommend the first one that is not done. Read the matching reference, then follow it:

1. **Error alerts and a logs page** -> `references/errors.md`
2. **Scheduled health checks** -> `references/health.md`
3. **Code review on every pull request** -> `references/review.md`
4. **Auto-merge small, safe changes** -> `references/automerge.md`
5. **A regular project review** -> `references/project-review.md`
6. **Backups of my users' data** -> `references/backups.md`
7. **How self-healing works here** -> `references/self-healing.md`

Good order for most people: 1, 2, 3, then 4. Option 1 is the base: the others read from it.

## What each script does

All are in `${CLAUDE_PLUGIN_ROOT}/scripts/`, run with `node`:

- `ops-setup.mjs <appDir> [--only health,review,automerge,deps] [--json]` adds the errors module if missing, then writes the workflow and config files into the app, and makes `CRON_SECRET` (sent to Vercel and GitHub, never shown). Files the student edited are not overwritten; `--force-file <path>` replaces one on purpose.
- `ops-status.mjs <appDir> [--json]` shows what is set up and what the last health run said.
- `backup-export.mjs <appDir> [--json]` saves every table to a private folder on the student's computer.
- `add-module.mjs <appDir> errors` adds only the error log (use `--dry-run` first if unsure).

## After any change to the app

New workflow files and the error module are code changes: branch, small commit with the student's OK, pull request, green checks, merge, redeploy with `deploy.mjs`. `CRON_SECRET` only takes effect after a redeploy. Update the profile through the scripts, not by hand.

## Honest limits (say them when relevant)

- Alerts only reach the owner's email if Resend is set up (`/shipyard:launch`, real emails). Without it, errors are still logged on `/admin/logs`.
- GitHub cannot force the test check on a free private repo. Auto-merge then does not work, and the student keeps the rule themselves: never merge while red.
- Scheduled workflows on public repos pause after 60 days with no activity on the repo. The status script shows the last run, so a silent pause shows up.
- Reviews, fixes and project reviews use the student's Claude Pro allowance. Warn before long jobs.

## Hand off

- Add an "Ops" section to the app's `HANDOFF.md`: what is on, where the logs page is, who gets alert emails, what the `ops-alert` issue means, what auto-merge will and will not touch, where backups live and that they hold personal data.
- Final message: what is now watching the app, what was checked, what was not, and the one next step. Short.
