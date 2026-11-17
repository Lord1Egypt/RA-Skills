# Acceptance

## Before deploy

- The website exists on Cargo Hosting, `site.json` is `ready`, and `canonicalUrl` is its HTTPS
  origin.
- `infra/visitor-identification/models/companies.ts` `url` is that origin.
- The workspace's default Snitcher connection is on Cargo's credits
  (`cargo-ai connection connector list`).
- The live price per identified company was read from `cargo-ai connection integration get
  snitcher`, quoted with the credit balance, and the operator agreed that spend grows with traffic.
- `site/` is copied into the app, the layout renders `VisitorConsent` when `visitorTracking()`
  returns settings, and the app's `defineApp` env has
  `NEXT_PUBLIC_SNITCHER_SNIPPET: visitingCompanies.config._trackingScript`.
- `visitors.json` `privacyPolicyUrl` points at a disclosure the operator reviewed.
- `node --import tsx evals/contract.mjs` passes from this skill's folder.
- `npm run check && cargo-ai project plan` pass, and the plan shows the two models and the app update.

## After deploy

In a private window on the canonical origin, network panel filtered to `snitcher`:

- No request on load, after "Reject tracking", or after a reload with the choice denied.
- "Accept tracking" requests `cdn.snitcher.com/releases/latest/radar.min.js` and sends to
  `radar.snitcher.com`.
- Withdrawing from "Privacy choices" reloads the page with no request after it.
- With Global Privacy Control on, the banner says tracking is off and "Accept" is disabled.
- The Cargo URL (`*.app.getcargo.run`) shows no banner and makes no request.
- After the sync interval, `website_visiting_companies` holds rows, or a zero is reported as a
  zero. No row is inserted by hand.
