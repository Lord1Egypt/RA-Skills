# Example Architecture Brief

Create a standalone HTML system map for a commerce platform.

## System

- Web and mobile clients connect through a CDN and API gateway.
- Identity is handled by an external OIDC provider.
- Backend services run in Kubernetes.
- Services include user, catalog, order, payment, and notification.
- PostgreSQL stores transactional records.
- Redis stores sessions and hot catalog data.
- Kafka carries order-created and payment-completed events.
- Object storage stores invoices and exports.
- Observability stack collects metrics, logs, and traces.
- Payment service calls a third-party payment processor.

## Requirements

- Show the public edge, cluster boundary, trust boundary, event flow, and data stores.
- Include protocol labels.
- Include a notes rail.
- Use the atlas-style template and make it readable and exportable.
