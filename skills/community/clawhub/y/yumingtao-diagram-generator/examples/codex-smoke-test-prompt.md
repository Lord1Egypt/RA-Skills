# Codex Smoke Test Prompt

Use the `diagram-generator` skill to create a standalone HTML system map.

## Requirements

- Output a single self-contained `.html` file
- Use inline SVG and embedded CSS
- Include export controls for SVG, PNG, Copy PNG, and Print/PDF
- Keep all visible labels in English
- Use the atlas-style template from `resources/template.html`
- Plan with `resources/diagram-ir.md`
- Include a notes rail with System Shape, Critical Flows, and Operational Notes
- Do not use placeholder labels

## System Brief

- Users access a web frontend and a mobile app.
- Traffic goes through CloudFront and an API gateway.
- Login is handled by an external OIDC identity provider.
- Backend runs in Kubernetes.
- Services include user, catalog, order, payment, and notification.
- PostgreSQL stores transactional records.
- Redis caches sessions and hot product data.
- Kafka carries order-created and payment-completed events.
- Object storage stores invoices and exported reports.
- Observability stack collects logs, metrics, traces, and alerts.
- Payment service integrates with a third-party payment processor.

## Final Instruction

Write the result as a production-ready HTML document in html-first mode, not markdown.
