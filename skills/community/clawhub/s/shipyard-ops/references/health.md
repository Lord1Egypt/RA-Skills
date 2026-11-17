# Scheduled health checks

A small GitHub workflow looks at the live app every 6 hours and opens one issue if something is wrong. When everything is fine again it closes the issue by itself.

## What it checks

- The home page answers.
- `/api/health` answers.
- `/api/ops/summary` (with the app's secret) says the app's own checks pass and shows how many unresolved errors there are.

## Set it up

1. Make sure the errors module is in (`errors.md`). `ops-setup` adds it if not.
2. `node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-setup.mjs" <appDir> --only health`
   It writes `.github/workflows/health.yml`, makes `CRON_SECRET` (a long random password the checker uses), sends it to Vercel and to GitHub secrets without showing it, and saves the app address as the repo variable `SITE_URL`.
3. Branch, pull request, green checks, merge. GitHub runs scheduled workflows only from the main branch.
4. Redeploy (`deploy.mjs <appDir>`) so the app knows `CRON_SECRET`.
5. Start one run now: `gh workflow run health.yml`, then `gh run list --workflow health.yml -L 1`. Expect a green run. Ask the student before starting it.
6. `ops-status.mjs <appDir>` should show the workflow and the last run.

## What the student sees

- A GitHub issue labelled `ops-alert` titled the same every time, with the results of each check. There is only ever one open. GitHub emails repo owners about new issues by default.
- The issue closes itself when the next run is all green.

## Good to know

- Public repos: GitHub pauses scheduled workflows after 60 days without any activity in the repo. `ops-status` shows the last run, so a pause is visible. Any push or manually started run wakes it.
- Runs use GitHub Actions minutes. Public repos are free; private repos have a monthly allowance that a 6-hourly check barely touches.
- The workflow has the smallest permissions it needs (read the code, write issues) and never uses pull request text in a command.
- A failing check is not always a bug in the app: a paused Supabase project (free tier, a week of no use) or an expired key also show up here. Read the issue body first.

## When an issue appears

Follow `self-healing.md`. Do not close the issue by hand; fix the cause and let the next run close it.
