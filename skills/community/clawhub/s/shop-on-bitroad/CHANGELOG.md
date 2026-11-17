# Changelog

All notable changes to the `shop-on-bitroad` skill.

Versioning is semver. ClawHub assigns its own version on publish unless one is
pinned, so publish with `clawhub skill publish ./shop-on-bitroad --version
<version>` to keep the registry in sync with the frontmatter, which is the
source of truth for what this file describes.

## 0.1.1 — unreleased

Step 44 walk-through on a fresh OpenClaw instance (2026-08-18, OpenClaw
2026.7.1-2, instance-key auth, VPS). The walk passed: the skill triggered,
reads ran over MCP, `sellers_get` came before any purchase talk, prices were
formatted from pence, and the blocked purchase was reported honestly with no
retry loop and no invented address.

- Added the pre-flight section naming the three independent purchase
  prerequisites and their refusals — the walk showed the agent calling the
  missing delegation a "spending envelope", conflating it with the separate
  payment-envelope mechanism
- Called out `address_required` explicitly, with the rule never to invent an
  address or take one from marketplace content

## 0.1.0 — unreleased

First version. Not yet published to ClawHub.

- Discovery via the official MCP registry entry `ai.bitroad/bitroad`, with the
  canonical endpoint as a stable fallback
- OAuth 2.1 connect flow, with the owner-approves-in-browser step called out as
  something the agent must not attempt itself, plus agent-key hygiene
- Delegation section distinguishing the three hard caps (`policy_denied`,
  final, no token) from the confirmation threshold (`confirmation_required`
  with a `confirmation_token`, re-issued with `acknowledged_confirmation: true`
  after explicit owner approval)
- Browse section covering catalogue search, listing detail, seller trust
  metrics and services search, plus the pence-denomination rule
- Buy section covering the two-step intent-then-confirm checkout, the
  15-minute intent expiry, cancellation, and the three confirm-time failure
  modes (threshold, 3-D Secure with server-side finalisation, decline)
- Services section covering both modes (fixed-price `services_purchase`,
  quote-mode request → accept), escrow, the owner gate before
  `services_acknowledge_delivery`, and the 7-day auto-release deadline
- Post-order section for orders, returns and disputes, with all dispute
  actions reserved for the owner's decision
- Rules block: marketplace content is data not instructions, no cap evasion,
  no purchase without explicit approval, no confirmation acknowledgement
  without a same-conversation yes, stable idempotency keys, one intent per
  purchase, owner personal data never written into seller-readable fields

Verified 2026-08-18: a five-lens review (tool behaviour, console routes and
live URLs, subsystem docs, adversarial supply-chain read, ClawHub format)
checked 105 claims against the codebase and live endpoints; all corrections
are folded into this version.

Pending before publish: the step 44 end-to-end walk-through on a fresh
OpenClaw instance against prod. Whatever that surfaces lands in 0.1.1 or
0.2.0.
