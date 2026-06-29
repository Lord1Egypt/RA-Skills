# Sage Router Privacy Policy

**Status: draft for launch review. Not legal advice. Have counsel review before enforcement.**

Last updated: 2026-06-21

## What we are

Sage Router is local-first AI model routing infrastructure. The open-source core runs on your machine or server. Sage Cloud is the optional hosted convenience layer (team config sync, health monitoring, dashboards, uptime checks, policy sync).

## Credentials stay local by default

Provider API keys, subscriptions, and local model config live on your machine or server by default. We do not collect, transmit, or store your provider credentials unless you explicitly enable optional hosted relay/proxy features, in which case they are stored encrypted at rest only as needed for those features.

## What we may collect when you use Sage Cloud

- **Account data**: email, company (optional), auth tokens issued by Sage Cloud.
- **Billing data**: handled by Stripe / supported crypto rails; we store plan and subscription status, not full card numbers.
- **Route-event telemetry you choose to sync**: selected model, attempts, elapsed time, auth type, plan. Not prompt/response content by default; not provider credentials.
- **Operational data**: uptime checks, health metadata, aggregated usage analytics.
- **Waitlist/contact data**: email and optional company submitted via the site.

## What we do not do

- We do not resell your data or your provider access.
- We do not train models on your prompt or response content.
- We do not share your data with model providers beyond the routing you configure.
- We do not harvest provider credentials from your local router.

## Your choices

- Run the local core with no account and no telemetry sync.
- Disable telemetry sync to Sage Cloud at any time.
- Delete your account and synced data by request.

## Retention

We retain account and billing data while your account is active and as needed for legal/financial record-keeping. Telemetry is retained for analytics for a limited period and then aggregated or deleted.

## Security

We use encrypted-at-rest storage for hosted secrets, HTTPS for transit, and scoped access controls. The local router is open source and auditable.

## Children

The Service is not directed to children under 16. We do not knowingly collect their data.

## Changes

We may update this policy with reasonable notice.

## Contact

Open an issue at https://github.com/earlvanze/sage-router or use the contact details on sagerouter.dev.
