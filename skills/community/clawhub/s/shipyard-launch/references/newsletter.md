# Email list (newsletter)

For apps whose owner wants to send updates to people who said yes.

## Needs first

Real sign-up emails working (`domain-email.md`): sending needs the verified Resend domain, `RESEND_API_KEY` and `RESEND_FROM` in Vercel.

## Add it

1. `add-module.mjs <appDir> newsletter --dry-run`, show it, then run it for real. It makes a private signing secret for unsubscribe links and saves it in `.env.local` (never printed).
2. `provision-supabase.mjs <appDir>` (new tables), `npm install`, `provision-vercel.mjs <appDir>` (pushes the new settings, including the secret), then redeploy.
3. Run `legal-generate.mjs <appDir>` again so the privacy page mentions email updates and how to unsubscribe. Regenerate every time you add a module.

## Rules to tell the student

- **Consent.** The tick box at sign-up and in Settings is unticked by default. Only people who ticked it are ever emailed. Never import a list of addresses that did not opt in.
- **Confirmed addresses only.** In the starter sign-up mode anyone can make an account with someone else's email, so a tick there proves nothing. The box is hidden, and the server refuses a yes, until sign-ups need a confirmed email (or the person signed in with Google). Finish `domain-email.md` first. When `launch-email.mjs --switch-to-verified` runs, ticks given before it are ignored until the person ticks again.
- **Unsubscribe.** Every email has an unsubscribe link and the mail-program one-click header. The link opens a page with a button; nothing happens until it is pressed, so mail scanners cannot unsubscribe people by accident.
- **Content.** Real updates about the app. Their postal address and contact email are in the privacy page; many countries want the sender identified in each commercial email, so keep the footer.

## Sending

The owner (admin) opens `/admin/newsletter`: write the message, see the preview, press "Send test to me", read it on a phone, then send. The confirm box shows how many people will get it. A second send of the same subject within 15 minutes, or a changed subscriber count, is blocked on purpose. Sends go out in batches of 100.

## Check

`/admin/health` shows the newsletter check. If it fails: the secret or Resend settings are missing; re-run `provision-vercel.mjs` and redeploy. Account deletion removes the person's subscription.
