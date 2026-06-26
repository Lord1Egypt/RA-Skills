# Setup - REST API

Read this when `~/rest-api/memory.md` does not exist or is empty.

Start by identifying the API outcome first: what clients need, which domain is in scope, and what reliability target is required.

## Integration First

Early in the conversation, confirm activation behavior:

- Should this support activate whenever the user asks to design or implement REST endpoints?
- Should it proactively enforce contract-first and security checks when API work appears risky?
- Should architecture decisions and release checklists be logged by default for future sessions?

If the user declines setup details, continue immediately and set integration to `declined`.

## Capture the Minimum Useful Baseline

Collect only information required to start useful API work:

- Product domain and API consumers (web app, mobile app, partners, internal systems).
- Primary resources, high-priority endpoints, and required operations.
- Non-functional constraints: latency, availability, throughput, and compliance.
- Authentication model and authorization boundaries.
- Deployment target and release timeline.

Ask one focused question at a time and produce concrete artifacts quickly.

## First-Session Output

Before ending setup, deliver at least one actionable artifact:

- Initial OpenAPI contract draft for core resources.
- Endpoint and error model matrix.
- Security control checklist.
- MVP test and observability plan.

## Persistence Rules

When memory is enabled:

- Create `~/rest-api/memory.md` from `memory-template.md`.
- Update `last` after meaningful progress.
- Store decisions, constraints, and pending risks in concise form.
- Never store raw secrets, tokens, or unrelated personal data.
