# Claude Desktop Smoke Test

Use the `diagram-generator` skill to create a standalone HTML system map.

## Requirements

- Use `html-first` mode.
- Follow `resources/generation-rules.md`, `resources/diagram-ir.md`, and `resources/template.html`.
- Use the atlas-style visual system.
- Write one standalone `.html` file.
- Include SVG, PNG, Copy PNG, and Print controls.
- Include the notes rail with System Shape, Critical Flows, and Operational Notes.
- Do not include visible draw.io controls.
- Do not leave placeholder text.

## Brief

- Browser and mobile clients enter through a CDN and WAF.
- Requests are routed to an API gateway.
- OIDC provider handles login and token validation.
- User, catalog, order, payment, and notification services run in Kubernetes.
- PostgreSQL stores users and orders.
- Redis stores sessions and hot catalog reads.
- Kafka transports order-created and payment-completed events.
- Object storage stores invoice PDFs and nightly exports.
- Payment service calls an external payment processor.
- Observability collects logs, metrics, traces, and alerts.

## Self-Check

After generating the diagram, run the output checker against the generated
file and fix anything it reports before delivering it:

```bash
node scripts/check-diagram.mjs <generated-file.html>
```

The run must end with `check-diagram: PASSED` with zero errors.
