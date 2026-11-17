## Description:

Workflow Chain coordinates multiple PrecisionLedger pipeline scripts into sequential or parallel workflows for QBO-backed, multi-step client work, using pipeline manifests and client SOPs to choose applicable pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance operations agents use this skill to assemble and run multi-pipeline PrecisionLedger workflows for monthly close, analysis packages, year-end tax prep, and reusable client templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run multiple local accounting pipeline scripts and write reports using QBO-backed client data.

Mitigation: Confirm the client slug, reporting period, output directory, and selected scripts before execution.

Risk: Shell command examples use user-supplied values for client slugs, dates, and output paths.

Mitigation: Validate inputs and quote shell variables before running generated commands.

Risk: The workflow may require a QBO reconnect step before accessing client data.

Mitigation: Run re-authentication only for the intended client and account, and verify authorization before continuing.

## Reference(s):

- [Workflow Chain ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/workflow-chain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and workflow summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected pipeline layers, run status, skipped steps, failures, output locations, and elapsed time.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
