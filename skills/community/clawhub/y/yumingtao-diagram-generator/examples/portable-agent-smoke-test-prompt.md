# Portable Agent Smoke Test Prompt

Use the local `diagram-generator` instruction pack and generate a standalone HTML technical system map.

Follow these files if you can access them:

- `SKILL.md`
- `AGENTS.md`
- `resources/generation-rules.md`
- `resources/diagram-ir.md`
- `resources/template.html`

## Deliverable

Generate one complete `.html` file with:

- inline SVG
- embedded CSS
- the atlas-style visual system from `resources/template.html`
- export buttons for SVG, PNG, Copy PNG, and Print/PDF
- a notes rail for system shape, critical flows, and operational notes

## System Brief

- Browser and mobile clients enter via CDN and WAF.
- Requests are routed to an ingress controller and API gateway.
- OIDC provider issues tokens for user login.
- User, order, payment, and notification services run in Kubernetes.
- PostgreSQL stores orders and users.
- Redis handles cache and sessions.
- Kafka transports domain events.
- Object storage stores invoice PDFs and nightly exports.
- Monitoring stack provides metrics, logs, traces, and alerting.
- Payment processor is an external dependency.

## Quality Bar

- Make the primary request path obvious.
- Show trust boundaries and runtime boundaries.
- Label key protocols and async flows.
- Avoid overlap and empty decorative elements.
- Return HTML only.
