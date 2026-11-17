# Owner emails: "<App> is live" and other notices

Ported from 6x7-app-factory's `notify-ready.ts` (PR #3), which sends the deploy email in production. Before that fix, every app's email arrived as "CommitR" (the name in the shared sender line), and nothing said why it was sent. Now:

- **Sender name is the app** (`Ballpark <noreply@send.example.com>`): the verified address stays, only the display name changes. Slugs become names (`journal-find` -> "Journal Find").
- **First line says why**: "You're receiving this because you deployed Ballpark to ballpark.example.com." Every automated email should open with one.
- **Plain text and HTML**, one link, no marketing.

## Send one

1. Dry run, always first: `node "${CLAUDE_PLUGIN_ROOT}/scripts/notify.mjs" <app-slug> --url https://<app address> --dry-run`. Show the student the from, to, subject and first line.
2. Real send only after every check passed (`verify.mjs`, `launch-check.mjs`): the same command without `--dry-run`. Never say "live" while only the `*.vercel.app` address works.
3. Other owner emails (a backup finished, a health check failed): `--kind custom --subject "..." --message "..." --reason "You're receiving this because ..."`.

It uses `RESEND_API_KEY` from the keys file (the key stays on this computer), the recipient from `owner.email` in the profile (or `--to`), and sends from `noreply@<the verified Resend domain in the profile>` (or `--from`). Without a verified domain Resend only delivers to the account's own address.

## Emails the app sends to its users

Sign-up and password emails are Supabase's, set up by `/shipyard:launch`. For other app emails (receipts, reminders), copy the same rules into the app's server code: app name as sender, a "why you got this" first line, plain-text version, one clear link, no free-mail Reply-To (use one at the domain or none), and an unsubscribe link for anything that is not strictly transactional (the newsletter module has one). Sending goes through the app's own sending-only Resend key, never the full-access one.
