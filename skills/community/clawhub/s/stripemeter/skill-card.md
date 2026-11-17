## Description:

Integrate Stripe usage-based billing with idempotent event ingestion, late-event handling, and pre-invoice reconciliation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geminimir](https://clawhub.ai/user/geminimir)

### License/Terms of Use:


## Use Case:

Developers and billing engineers use Stripemeter to implement usage metering for Stripe-based products, inspect usage drift, replay late events, and validate usage-based pricing before invoices are finalized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick start clones and runs mutable remote code with Docker and pnpm without pinning or verification.

Mitigation: Pin a reviewed commit and inspect Docker Compose files, package scripts, migrations, and dependency lockfiles before running the quick start.

Risk: Stripe usage posting and billing examples can affect real billing data if live credentials are used without controls.

Mitigation: Use test Stripe keys, narrowly scoped credentials, and shadow mode until the integration has been reviewed.

Risk: Local services and monitoring dashboards may expose operational data or default credentials if reachable beyond the developer machine.

Mitigation: Avoid exposing local services, change the Grafana default password, and restrict network access during evaluation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/geminimir/skills/stripemeter)
- [API Documentation](docs/welcome.md)
- [Ingest API](docs/api/ingest.md)
- [Reconciliation Summary API](docs/api/reconciliation-summary.md)
- [Usage History API](docs/api/usage-history.md)
- [Simulator Guide](docs/simulator-getting-started.md)
- [Simulator Scenarios](docs/simulator-scenarios.md)
- [Reconciliation Runbook](RECONCILIATION.md)
- [Alert Configuration](ops/ALERTS.md)
- [Quick Start Referenced Repository](https://github.com/geminimir/stripemeter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, TypeScript, Python, JSON, YAML, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local development commands, API examples, SDK snippets, reconciliation procedures, simulator scenarios, and alerting configuration.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
