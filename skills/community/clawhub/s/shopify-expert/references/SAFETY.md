# Safety

## Data and compliance

- Customer and order data are sensitive. Follow Shopify’s **privacy / GDPR / redaction** requirements and app **mandatory webhooks** where applicable — see bundled **`DOC_WEBHOOKS.md`** and live compliance docs on **shopify.dev**.

## Destructive operations

- Mutations (orders, inventory, products, app installs) can affect **production** revenue. Prefer **dev stores** and explicit human approval for bulk changes.

## Rate limits

- Admin API requests are **rate limited**. Implement backoff and avoid tight loops from agents.

## Third-party apps

- Only use tokens and APIs for **apps you control** or that the merchant explicitly authorized.
