# GitHub Copilot Smoke Test

Use `COPILOT-INSTRUCTIONS.md` as the custom instruction source and generate a standalone HTML system map.

## Requirements

- Follow `diagram-generator/resources/generation-rules.md`.
- Use `diagram-generator/resources/diagram-ir.md` as the planning model.
- Use `diagram-generator/resources/template.html` as the base structure.
- Produce `docs/commerce-system-map.html` unless another path is requested.
- Use `html-first` mode.
- Include export controls and notes rail.
- Do not include draw.io controls.
- Do not leave placeholder text.

## Brief

- Customers use web and mobile clients.
- CDN and WAF protect the public edge.
- API gateway routes into backend services.
- Identity is delegated to OIDC.
- Kubernetes hosts user, catalog, order, payment, and notification services.
- PostgreSQL, Redis, Kafka, and object storage back the runtime.
- Payment processor and observability stack are external or supporting dependencies.

## Self-Check

After generating the diagram, run the output checker against the generated
file and fix anything it reports before delivering it:

```bash
node scripts/check-diagram.mjs <generated-file.html>
```

The run must end with `check-diagram: PASSED` with zero errors.
