## Description:

Rapproche les opérations bancaires avec les factures et notes de frais classées, signale les paiements réglés, partiels, impayés ou en retard, et produit un suivi mensuel par client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting teams and their agents use this skill to reconcile bank transactions against classified invoices and expense reports, identify missing or duplicate payment evidence, and prepare a concise payment-status report for the accountant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated sidecar, transcription, report, and temporary vision files can contain sensitive financial records.

Mitigation: Install and run the skill only in a controlled accounting workspace, and exclude generated financial artifacts from sync, backups, and source control unless that sharing is intended.

Risk: The vision queue can process files outside the intended client folder when the queue is modifiable by another party.

Mitigation: Review or patch path-containment checks before using resolve_vision.py with queues that anyone else can modify.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trendex/skills/rapprochement-paiements)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON accounting artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-client company.json and rapprochement.json files, consolidated reconciliation summaries, and vision sidecar guidance when documents need review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
