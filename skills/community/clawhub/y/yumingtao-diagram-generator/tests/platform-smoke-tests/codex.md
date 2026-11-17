# Codex Smoke Test

Use the `diagram-generator` skill to create a standalone HTML system map from this brief.

## Requirements

- Use `html-first` mode.
- Write the result to `commerce-system-map.html`.
- Follow `resources/generation-rules.md`, `resources/diagram-ir.md`, and `resources/template.html`.
- Use the atlas-style visual system.
- Do not include visible draw.io controls.
- Do not leave placeholder text.
- After writing the file, check for overlap, clipped labels, marker color mismatch, missing notes rail, and missing export buttons.
- If editing an existing diagram, preserve unrelated content and fix the requested layout defects with local coordinate and path changes.

## Brief

- Web and mobile users enter through CloudFront and an API gateway.
- Authentication is handled by an external OIDC provider.
- Backend services run in Kubernetes.
- Services include user, catalog, order, payment, and notification.
- PostgreSQL stores transactional records.
- Redis caches sessions and hot product data.
- Kafka carries order-created and payment-completed events.
- Object storage stores invoices and exported reports.
- Payment service integrates with a third-party payment processor.
- Observability stack collects logs, metrics, traces, and alerts.

## Self-Check

After generating the diagram, run the output checker against the generated
file and fix anything it reports before delivering it:

```bash
node scripts/check-diagram.mjs <generated-file.html>
```

The run must end with `check-diagram: PASSED` with zero errors.
