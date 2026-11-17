## Description:

Guides agents in using the npx corp CLI to manage corporate entities, governance, cap tables, finance, agents, and compliance for TheCorporation platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansonkd](https://clawhub.ai/user/hansonkd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to form and operate business entities through TheCorporation's CLI, including governance workflows, equity issuance, finance tasks, document signing, tax filings, and agent work-item loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party CLI for legal, financial, identity, signing, tax, payment, payroll, equity, and agent workflows.

Mitigation: Install only after reviewing and trusting the CLI package, and prefer a pinned, reviewed version.

Risk: CLI actions can materially affect company formation, governance, equity records, payments, filings, and signed documents.

Mitigation: Require human review before signing documents, issuing equity, filing taxes, sending payments, changing API URLs, or activating agents.

Risk: The CLI can run in local, cloud, or self-hosted modes with different data and network exposure.

Mitigation: Verify the active hosting mode and workspace context before use, and run in a least-privileged or isolated environment.

Risk: Command argument details such as cents-based monetary values, active entity context, and shell interpolation can cause incorrect operations.

Mitigation: Use dry-run or JSON verification where available, confirm active entity context, validate monetary units, and escape shell-sensitive characters before executing write operations.

## Reference(s):

- [TheCorporation.ai repository](https://github.com/thecorporationai/thecorporation-mono)
- [ClawHub skill page](https://clawhub.ai/hansonkd/skills/thecorporation-form-and-operate)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and CLI workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup instructions, command sequences, and operational cautions; many CLI examples request JSON output with --json.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
