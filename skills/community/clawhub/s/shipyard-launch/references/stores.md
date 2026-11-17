# Phone and desktop apps

## Start with the installable web app

Every Shipyard app can be added to a phone's home screen (PWA, an installable web app) at no cost. Many apps never need the stores. Ask why they want the store: discoverability, notifications, or "feels real". If it is only the look, stay with the installable web app.

## Before any shell

- The app must be live on a custom or at least stable HTTPS address (`go-live.md` steps 1 to 4). The shell loads that address.
- Account deletion in the app and public privacy and terms pages are required by the stores; the template has them.
- Payments: Apple requires its own in-app purchase for digital subscriptions sold inside an iOS app in most regions. Do not put Stripe buttons for digital goods in the iOS app without checking the rules for the student's region. Android has its own rules too; check Google Play's current payments policy.

## Costs and people

| Store | Cost | Notes |
|---|---|---|
| Apple App Store | $99 a year | Needs a Mac with Xcode |
| Google Play | $25 once | New personal accounts must run a closed test with 12 testers for 14 days first |
| Microsoft Store | free for individuals | Windows apps |
| Mac or Windows download | free | Signing a Mac app (notarization) needs the paid Apple account; unsigned apps show a scary warning |

Prices change; say "at the time of writing" and have them check the store pages.

## Add the shell

- Phone: `node "${CLAUDE_PLUGIN_ROOT}/scripts/add-shell.mjs" <appDir> mobile`. It refuses without a live HTTPS address. It writes a `mobile/` folder with a Capacitor wrapper (a thin app that shows your site), an offline page, icons, the iOS privacy file, `STORE.md` (listing draft) and a `README.md` with the exact next commands. App id comes from `--app-id` or is derived; it must be a reverse domain like `com.example.myapp`. Choose it once: it cannot change after publishing.
- Desktop: `add-shell.mjs <appDir> desktop` writes `desktop/` (Electron) and a GitHub workflow that builds on tags named `desktop-v*`.
- Do not run `npx cap add ios` or `npx cap add android` or open Xcode/Android Studio for them without asking: they need those tools installed. If the student wants to, follow the shell's README with them and say what each command does.

## Check

`node "${CLAUDE_PLUGIN_ROOT}/scripts/store-check.mjs" <appDir>` checks app id, address, icons, privacy file, usage strings, account deletion, store listing fields and the web pages. Fix every cross.

## Apple "4.2" warning

Apple rejects apps that are only a website in a frame. Before submitting: a native tab bar or a native feature in the main flow, a designed offline screen, no external payment links for digital goods, and a demo login for reviewers in the listing notes. Say the review can still reject it; it is not a promise.

## Testers

Tell them early: Google Play needs 12 testers for 14 days, so find friends now. Apple uses TestFlight for testers. Student does the store sign-ups and payments themselves.

## Going all the way to the stores

When the student really wants the App Store and Google Play, work through these in order. They come from shipping a real Next.js, Supabase and Vercel app to both stores.

1. `stores-audit.md`: the readiness audit. Fix every point before building anything.
2. `stores-build.md`: the Capacitor 7 wrapper, Android AAB build and signing on Linux, iOS build on a Mac.
3. `stores-listing.md`: screenshots, the Play feature graphic, listing text, App Privacy and Data safety answers, and which developer account to open.
4. `stores-gotchas.md`: problems that cost hours last time. Read it before starting.
