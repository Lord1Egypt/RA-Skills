## Description:

Create, summarize, or verify local human-readable receipts for AI agent work using the @builtbyecho/trustlog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, inspect, summarize, verify, and optionally preserve local receipts for AI agent work, especially after tests, builds, handoffs, or risky commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned third-party npm CLI in the target project.

Mitigation: Use a pinned or lockfile-managed CLI version, run with minimal environment secrets, and install only after reviewing the package source and release.

Risk: The Vaultline workflow can upload local receipt contents to an external service.

Mitigation: Treat upload as an explicit publication step, inspect receipts before sharing, and provide only the required Vaultline API key for that command.

Risk: Receipts may still contain sensitive project or workflow information after automated redaction.

Mitigation: Inspect generated Markdown and JSON receipts before posting them publicly or handing them to another system.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, JSON]

**Output Format:** [Markdown guidance with inline shell and JavaScript code blocks; referenced receipt artifacts are Markdown and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Receipts are local-first by default; Vaultline upload is an explicit external publication step.]

## Skill Version(s):

0.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
