# Sage Router Terms of Service

**Status: draft for launch review. Not legal advice. Have counsel review before enforcement.**

Last updated: 2026-06-21

These Terms govern your use of Sage Router software, the sagerouter.dev website, the api.sagerouter.dev API, and Sage Cloud hosted services (together, the "Service"), operated by Earl Vanze ("we", "us").

## 1. The Service

Sage Router is local-first AI model routing infrastructure. The open-source core runs on your own machine or server and routes requests across provider accounts, API keys, subscriptions, and local models that you already control. Sage Cloud adds optional hosted convenience: team config sync, provider health monitoring, dashboards, uptime checks, routing policy sync, and an optional reliability/failover layer.

## 2. Bring your own access

You are responsible for obtaining and maintaining all authorized access to third-party model providers. You must comply with each provider's Terms of Service. Sage Router does not resell model access, pool accounts, share subscriptions, or bypass provider terms. You grant Sage Router only the technical permission to route requests to providers you have configured.

## 3. Credentials and custody

By default, provider credentials are stored on your machine or server and are not transmitted to hosted Sage infrastructure. If you explicitly enable optional hosted relay/proxy features, secrets are stored encrypted at rest only as needed for those features. You are responsible for securing your credentials.

## 4. Acceptable use

You agree not to: resell or pool provider access through the Service; bypass provider rate limits, auth, or terms; abuse, overload, or attack the Service; route traffic that is unlawful, infringing, or fraudulent; or reverse-engineer hosted Sage Cloud beyond what open-source licenses permit for the core.

## 5. Plans and billing

Paid plans (lite, pro, max) and usage-based metered billing are billed in advance via Stripe or supported crypto rails. Fees are non-refundable except where required by law. We may change pricing with reasonable notice; existing subscriptions keep their current term terms.

## 6. Uptime and reliability

Sage Cloud hosted convenience features are provided on a commercially-reasonable basis. We do not guarantee uninterrupted availability of third-party providers, which are outside our control. The local-first core continues to function independently of Sage Cloud availability.

## 7. Data

Route-event telemetry you choose to sync to Sage Cloud may include selected model, attempts, elapsed time, auth type, and plan. It does not include provider credentials. See our Privacy Policy.

## 8. Disclaimer

The Service is provided "as is" without warranties. To the maximum extent permitted by law, we are not liable for indirect, incidental, special, consequential, or lost-profit damages, or for amounts exceeding your fees paid in the prior 12 months.

## 9. Termination

You may stop using the Service at any time. We may suspend or terminate access for breach of these Terms. Upon termination, paid terms end per the billing section; your local router remains yours under its open-source license.

## 10. Changes

We may update these Terms with reasonable notice. Continued use after changes constitutes acceptance.

## 11. Contact

Open an issue at https://github.com/earlvanze/sage-router or email the operator via the contact details on sagerouter.dev.
