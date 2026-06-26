## Description: <br>
Integrate Stripe usage-based billing with idempotent event ingestion, late-event handling, and pre-invoice reconciliation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geminimir](https://clawhub.ai/user/geminimir) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and billing engineers use this skill to design Stripe usage metering, ingest customer usage events, reconcile local totals against Stripe, and prepare pre-invoice corrections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stripe credentials or live billing writes can affect customer invoices if used without safeguards. <br>
Mitigation: Use test or shadow mode first, keep Stripe keys in a secrets manager, avoid committing real keys, and require human approval before live Stripe writes. <br>
Risk: Replay or reconciliation apply actions can change usage counters and billing parity when scoped incorrectly. <br>
Mitigation: Run dry-run replay first, narrow actions by tenant, metric, customer, and period, then verify reconciliation drift before closing the action. <br>
Risk: Docker and package-manager setup commands pull and run external project code. <br>
Mitigation: Review or pin the external repository and dependencies before running Docker, pnpm, migration, or development commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/geminimir/stripemeter) <br>
- [StripeMeter API Documentation](docs/welcome.md) <br>
- [Ingest API](docs/api/ingest.md) <br>
- [Reconciliation Runbook](RECONCILIATION.md) <br>
- [Pricing Simulator Guide](docs/simulator-getting-started.md) <br>
- [Alert Configuration](ops/ALERTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with code blocks, API examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run and live billing command examples that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
