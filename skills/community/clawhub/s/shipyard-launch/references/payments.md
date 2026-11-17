# Payments in test mode

Test mode moves no real money. Everything is built and checked there first.

## 1. Pre-checks

- A Stripe account in Test mode, with `STRIPE_SECRET_KEY` (starts `sk_test_`) and `STRIPE_PUBLISHABLE_KEY` in the keys file (setup step, `accounts.md`). Check with `secrets-check.mjs --live`.
- Privacy and terms pages made (`legal.md`), after the billing module is added: they must mention Stripe, subscriptions and the 14-day right to withdraw. Payments also need a phone number for customers (`company.phone`; the answer "none" is allowed).
- Merchant of record option: explain once, then ask. With Stripe, the student is the seller: they handle VAT, invoices and refunds themselves. A merchant of record (Paddle, Lemon Squeezy, Polar, or Stripe's managed payments) is the seller and handles VAT and invoices for about 3.5% to 5% plus fees. Choose one if they sell worldwide to consumers and do not want the tax work. This skill's billing module uses plain Stripe; if they choose a merchant of record, say that part is not built yet and stop at the pricing decision.
- iOS caveat: Apple requires its own in-app purchase for digital subscriptions inside an iOS app in most regions. Selling through the website and phone browser is fine; selling inside the store app is not. See `stores.md`.

## 2. Add the module

1. `node "${CLAUDE_PLUGIN_ROOT}/scripts/add-module.mjs" <appDir> billing --dry-run`, show what changes, then without `--dry-run`. If it stops on a changed file, list the files and ask; `--force-file <path>` replaces one on purpose.
2. Run `provision-supabase.mjs <appDir>` (new tables), `npm install` in the app, and `provision-vercel.mjs <appDir>` (new settings).
3. Plans: ask what they sell. Prices live only in `src/lib/billing/plans.ts`, in the block between `// shipyard:plans:start` and `// shipyard:plans:end`. There is one free plan and one paid plan, in euro. Edit the block (name, price in cents, interval month or year, features, free limits). A changed price makes a new Stripe price; old subscribers keep the old one.
4. Run `npm run typecheck`, `npm run lint`, `npm test`.

## 3. Set up Stripe objects

`node "${CLAUDE_PLUGIN_ROOT}/scripts/stripe-setup.mjs" <appDir>` (test mode). It creates products, prices, the customer portal (cancel, update card, invoices) and the webhook, and puts the webhook secret straight into Vercel. It never prints keys. Safe to run again after editing plans. Then redeploy.

One step is the student's, in the Stripe dashboard: Settings, Business, Public details, add the Terms link (`<site address>/terms`). Checkout shows an "I agree to the Terms and ask for the service to start now" box, which is what lets the terms keep the days already used if someone withdraws; Stripe refuses to show it until that link is saved, and the app then tells the buyer the owner has to finish setting up.

## 4. Try it with a real test purchase

Branch, commit with OK, pull request, green checks, merge, `deploy.mjs`. Then, together:
1. Sign in on the live address, open `/pricing`, press Upgrade.
2. On Stripe's page use card `4242 4242 4242 4242`, any future date, any 3 digits, any name and postcode.
3. Back in the app, Settings should show the paid plan. This proves the webhook works.
4. Press "Manage billing", cancel, and check it shows "ends on <date>". Then buy again and try "Withdraw from contract" in Settings, Billing: the plan ends at once and an email confirms it. The owner refunds what was paid minus the days used in the Stripe dashboard (the owner gets an email saying how much).
5. Try the decline card `4000 0000 0000 0002` and the card needing a code `4000 0025 0000 3155`.

## 5. Check

Open `/admin/health`: Stripe key mode (test), prices, webhook and portal should be green. Run `launch-check.mjs <appDir>`. Gate paid features on the server with `requirePaid()`, never only in the page. Update `HANDOFF.md` with the plan file location.

Going live is a separate step: `go-live.md`.
