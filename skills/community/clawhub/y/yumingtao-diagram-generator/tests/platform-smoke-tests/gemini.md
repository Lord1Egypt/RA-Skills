# Gemini Smoke Test

Create a standalone HTML system map using the local Diagram Generator instruction pack.

Attach or paste these files if Gemini cannot read local files:

- `GEMINI.md`
- `resources/generation-rules.md`
- `resources/diagram-ir.md`
- `resources/template.html`

## Requirements

- Use `html-first` mode.
- Use the atlas-style visual system.
- Return one complete HTML document.
- Keep visible text in English.
- Include export controls and the notes rail.
- Do not include draw.io controls unless explicitly requested.
- Do not leave placeholder text.

## Brief

- Browser and mobile clients use CDN and WAF.
- API gateway routes requests into Kubernetes services.
- OIDC provider issues and validates tokens.
- Services include user, order, payment, catalog, and notification.
- PostgreSQL, Redis, Kafka, and object storage provide durable and cached state.
- Payment processor is an external dependency.
- Monitoring stack receives metrics, logs, traces, and alerts.

## Self-Check

After generating the diagram, run the output checker against the generated
file and fix anything it reports before delivering it:

```bash
node scripts/check-diagram.mjs <generated-file.html>
```

The run must end with `check-diagram: PASSED` with zero errors.
