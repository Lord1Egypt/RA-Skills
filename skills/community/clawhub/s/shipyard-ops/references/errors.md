# Error alerts and the logs page

When something breaks for a visitor, the app writes it down and emails the owner. The student does not need to hear about it from a user first.

## What it does (tell the student)

- **Crashes on a page** show a friendly screen with "Try again", and a short note is sent to the app.
- **Failures in the app's own server code** are logged too, when the code uses the helper `serverError(area, err, what)`. The visitor sees "Couldn't do X. Please try again." and the real cause goes in the log.
- **The logs page** is `/admin/logs`, for admins only (everyone else sees "not found"). It groups repeats of the same problem, shows how often and when, filters by area, and has a "Mark resolved" button.
- **Email alerts** go to the admin addresses, at most once per problem every 6 hours (`ERROR_ALERT_HOURS` changes it), and at most 10 emails an hour overall. They need Resend. Without it, problems are only logged.
- **Crashes reported by visitors' browsers** (anyone on the internet can send those) always produce the same short email, "A page crashed for a visitor", with no page name and none of the visitor's words, and all of them together send at most one email per alert window. The details are in the logs page, which only admins can open.
- **Nothing sensitive is stored.** Keys, tokens, passwords, cookies, request bodies, email addresses and phone numbers are stripped before anything is saved or emailed. The log does keep the signed-in user's id; it is cleared if that account is deleted.
- **Old rows are deleted after 90 days.** Supabase's scheduled-job feature (pg_cron) does it when it is switched on in the project (Dashboard, Integrations, Cron). If not, the daily health check cleans up instead.
- The Health page gets a check, "errors in 24 hours": a warning for any open problem, a failure above 50 different ones.

## Add it

1. `node "${CLAUDE_PLUGIN_ROOT}/scripts/add-module.mjs" <appDir> errors --dry-run`, show the list, then run it for real. (`ops-setup.mjs` does this for you if the module is missing.)
2. `provision-supabase.mjs <appDir>` applies the new table. Then `npm install`, a branch, pull request, green checks, merge, redeploy.
3. Run `legal-generate.mjs <appDir>` again: the privacy page should mention the error log (it keeps a user id for 90 days).
4. Test it: open `/admin/logs` as the owner. It should load and say there are no problems.

## Using it in new code

In API routes, catch errors and `return serverError('billing', err, 'start the checkout')`. Pick a short area name (billing, auth, upload). Never put secrets or whole request bodies in the message.

## When an alert arrives

Open `/admin/logs`, find the problem, read the message and the area. Then follow `self-healing.md`. Mark it resolved only after the fix is live; if it comes back, it reopens as a new row.

## Details students may ask about

- Table `error_log`, no direct access for visitors or signed-in users (only the server's secret key).
- Client reports go to `POST /api/errors`: same address only, 4 KB limit, 5 reports a minute per visitor.
- `GET /api/ops/summary` is for the health workflow. It needs the secret `CRON_SECRET` and returns only check names, pass or fail, and two counts. No messages, no personal data.
