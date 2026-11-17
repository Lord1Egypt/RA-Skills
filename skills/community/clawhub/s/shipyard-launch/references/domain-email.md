# Own address and real sign-up emails

Why: the free `name.vercel.app` address works, but a real address looks trustworthy, and real sign-up emails let you know a person owns the email they typed. Until then the app is in "starter" mode: anyone can sign up without confirming their email.

## 1. Domain

1. Ask: do they already own a domain? If not, explain: a domain is your own web address, about $10 to $15 a year. Good places: Cloudflare Registrar (at cost) or Porkbun. The student buys it themselves; you never pay or enter card details. Suggest a short name that matches the app; `.com` is safest, other endings are fine.
2. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/launch-domain.mjs" <appDir> <domain>`. It adds the domain and `www.<domain>` to the Vercel project and prints a table of DNS records. DNS records are the lines at the registrar that point the name at your app.
3. Show the table as it is, and tell them where to paste it: registrar dashboard, the domain, DNS (or "DNS records"). Type, name and value go in exactly. If the registrar is Cloudflare, set the proxy to "DNS only" (grey cloud) for the Vercel records.
4. Run `... launch-domain.mjs <appDir> <domain> --check`. It waits up to 10 minutes and shows progress. DNS can take longer; if it times out, say so, tell them to try again in an hour, and run `--check` again then. When it passes, the script updates the app's public address in Vercel, the profile, and the sign-in settings in Supabase. Then redeploy (`deploy.mjs`).
5. **The `www` redirect is a button the student presses.** Vercel serves `www.<domain>` as a second copy of the site until it is told to redirect, and the Vercel command line cannot do that. The script prints the steps (Vercel dashboard, the project, Settings, Domains, Edit next to `www`, Redirect to Another Domain, the main address, 308, Save). `--check` stays failed (exit 1, "still opens as a second copy") until `https://www.<domain>` answers with a redirect, so run it again after.

## 2. Sending domain and Resend

1. Resend is the service that sends your app's emails. Needs `RESEND_API_KEY` in the keys file (setup step, `accounts.md`), made with **Full access** because it creates the domain and a key for the app. That key stays on the student's computer. The script makes a separate sending-only key for this app (it can send from the domain and do nothing else) and gives that one to Supabase and Vercel, so a leak of the app never exposes the Resend account. If missing: `secrets-init.mjs`, they paste it, then `secrets-check.mjs --live`.
2. Use a sending address on a subdomain such as `send.<domain>`. This keeps your main domain's own email safe.
3. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/launch-email.mjs" <appDir> --domain send.<domain>`. It creates the domain in Resend and prints a second DNS table (SPF, DKIM, return path). The student pastes those at the registrar too.
4. Run it again with `--check`. When Resend says verified, the script makes the app's sending-only key, connects Supabase's sign-up emails to Resend and saves the sending settings in Vercel.

## 3. Switch to verified sign-ups

1. Run `launch-email.mjs <appDir> --switch-to-verified`. It turns on Supabase's email confirmation and sets `NEXT_PUBLIC_SIGNUP_MODE=verified` in Vercel. This value is baked in at build time, so redeploy after. If the app has the email list, it also sets a cut-off: people who ticked the box while sign-ups were unconfirmed never proved the address was theirs, so they are left out of newsletters until they tick again in Settings. Tell the student.
2. Supabase's "Confirm signup" email should link to `{{ .SiteURL }}/auth/confirm?token_hash={{ .TokenHash }}&type=email` so the link works on any device. `launch-email.mjs` sets this; check its output says so.
3. Send yourself a test: sign up with a second email address, check the email arrives (also look in spam), click the link, land signed in. Sign-in without confirming should say "email not confirmed" with a resend button.
4. Open `/admin/health`: sign-up mode and Resend domain should be green.

## What changes for users

- New people get a confirmation email and must click it before the first sign-in.
- The email address they type is now proven to be theirs. Google sign-in becomes safe to switch on.
- Password-reset emails reach everyone, not just the owner.
- Emails come from `noreply@send.<domain>`. If they land in spam, tell the student to wait a day, mark one "not spam", and check the SPF/DKIM lines are verified.

## Receiving mail and owner emails

Receiving at `hello@<domain>` (ImprovMX catch-all to Gmail), replying from Gmail, DMARC, Papaki DNS steps, a deliverability test and the "<App> is live" email are in `/shipyard:email` (`email-check.mjs`, `notify.mjs`).

## If something fails

- "Domain not found at registrar": wait, check for typos in the table.
- Vercel says the domain is owned by another account: the student must remove it there first.
- Resend stays "pending": a record is missing or has a stray extra domain on the end (some registrars add it automatically; paste the name without the domain part).
- `launch-domain --check` says DNS is not right but the site opens: some registrars flatten the main address, and Cloudflare's orange cloud shows its own addresses. The script now also accepts a site that answers like Vercel. At Cloudflare, still set the records to "DNS only" (grey cloud); Vercel recommends it.
- The script says it removed an older Resend key: that happens on a new computer or when the sending domain changed (a key only works for the domain it was made for). Run `deploy.mjs` straight away, because the live app's own emails use the old key until it is deployed again.
