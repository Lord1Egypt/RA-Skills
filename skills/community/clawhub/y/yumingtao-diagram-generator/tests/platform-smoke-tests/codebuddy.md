# CodeBuddy Smoke Test

Use `CODEBUDDY.md` as the workspace rule and create a standalone HTML system map.

## Requirements

- Use `html-first` mode.
- Follow the shared resources under `resources/`.
- Use atlas-style visual design.
- Include SVG, PNG, Copy PNG, and Print controls.
- Include the notes rail.
- Do not expose draw.io controls.
- Do not leave placeholder text.
- If revising an existing diagram, preserve unrelated content and fix only the requested layout defects.

## Brief

- Users enter through web and mobile clients.
- Public traffic passes through CDN, WAF, and API gateway.
- OIDC handles authentication.
- Kubernetes services implement users, catalog, orders, payments, and notifications.
- PostgreSQL stores transactional data.
- Redis stores sessions and hot reads.
- Kafka carries domain events.
- Object storage stores invoices and exports.
- Observability receives logs, metrics, traces, and alerts.

## Self-Check

After generating the diagram, run the output checker against the generated
file and fix anything it reports before delivering it:

```bash
node scripts/check-diagram.mjs <generated-file.html>
```

The run must end with `check-diagram: PASSED` with zero errors.
