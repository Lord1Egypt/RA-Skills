# Taking real payments

Only start when the student says "I want real payments". Go in this order and do not skip one. If a step is not done, say which and go back.

1. **Own domain** (`domain-email.md`). Live Stripe wants a real website address, and the live check refuses `vercel.app`.
2. **Real sign-up emails** (`domain-email.md`): signup mode `verified`, Resend domain verified.
3. **Legal pages** (`legal.md`) made and read through, with the "have it checked" reminder said once more.
4. **Country checklist** (`country.md`): `LAUNCH-CHECKLIST.md` exists and the student has confirmed business registration and tax steps for their country, or knowingly postponed with an accountant.
5. **Payments work in test mode** (`payments.md`), including a test purchase and cancel.
6. **Vercel Pro.** Free (Hobby) hosting is for non-commercial use only, so taking money needs Pro, $20 a month. The student upgrades in the Vercel dashboard themselves. Ask: "Did you upgrade to Pro?" If yes: `node "${CLAUDE_PLUGIN_ROOT}/scripts/profile.mjs" set accounts.vercel.plan pro`.
7. **Stripe live account.** The student, in the Stripe dashboard only: finish the business details, verify identity, add the bank account for payouts. This can take days. You never enter these for them. When Stripe shows Live mode available, they create a restricted or secret live key (Developers, API keys). They paste it into the keys file as `STRIPE_LIVE_SECRET_KEY` (and the publishable key as `STRIPE_LIVE_PUBLISHABLE_KEY`) after `secrets-init.mjs`. Never in chat.
8. **Dry run of the gate:** `launch-check.mjs <appDir>` (test mode) must have no crosses.
9. **Live set up:** `node "${CLAUDE_PLUGIN_ROOT}/scripts/stripe-setup.mjs" <appDir> --live`. It refuses with a plain list if anything above is missing. It creates live products, prices, portal and webhook, and pushes the live keys to Vercel production only (never to development) without printing them. Add the Terms link in the Stripe dashboard (Settings, Business, Public details) while Test mode is off too. Redeploy. Do not re-run `provision-vercel.mjs` to change payment settings later: it leaves the live values in production alone, but `stripe-setup.mjs --live` is the one that owns them.
10. **One real purchase.** The student buys the cheapest plan with their own card, checks the paid state in the app, then refunds themselves in the Stripe dashboard (Payments, the payment, Refund). Remind them the card fee is not always returned. Never use their card yourself.
11. **Final gate:** `launch-check.mjs <appDir> --live`. Fix every cross. Open `/admin/health` on the live site.
12. **Announce.** Update `HANDOFF.md` and `LAUNCH-CHECKLIST.md`. Tell them what to watch: failed payments in the Stripe dashboard, refunds, support emails to their contact address.

Rules: never switch live keys on while checks are red; never put a live key anywhere but the keys file; if anything charges the wrong amount, tell the student to pause the product in the Stripe dashboard first, then fix.
