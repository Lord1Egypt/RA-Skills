# AGENTS.md Smoke Test

Use this smoke test for Cursor, OpenCode, Windsurf, and similar agents that consume `AGENTS.md`.

## Task

Generate a standalone HTML system map from the brief below.

## Requirements

- Read `AGENTS.md`.
- Follow `resources/generation-rules.md`, `resources/diagram-ir.md`, and `resources/template.html`.
- Use `html-first` mode.
- Use atlas-style design.
- Include export controls and notes rail.
- Do not include visible draw.io controls.
- Do not leave placeholder text.
- Return or write one complete HTML file.
- If the prompt includes an existing diagram, inspect it first and preserve unrelated content while fixing the requested defect.

## Brief

- Browser and mobile clients enter through CDN and WAF.
- API gateway routes requests to Kubernetes services.
- OIDC provider handles identity.
- User, catalog, order, payment, and notification services serve the commerce workflow.
- PostgreSQL stores users and orders.
- Redis caches sessions and hot catalog data.
- Kafka transports order and payment events.
- Object storage stores invoices and exports.
- External payment processor handles authorization.
- Observability stack collects logs, metrics, traces, and alerts.

## Self-Check

After generating the diagram, run the output checker against the generated
file and fix anything it reports before delivering it:

```bash
node scripts/check-diagram.mjs <generated-file.html>
```

The run must end with `check-diagram: PASSED` with zero errors.
