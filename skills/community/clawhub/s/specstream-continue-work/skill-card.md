## Description:

Read the finished rows with the page behind each fact, send them where the person works, and start new work only on purpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[specstream](https://clawhub.ai/user/specstream)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and agents use this skill to inspect complete SpecStream finding results, review each decision's evidence and read time, and then export or share selected rows or start cost-bounded monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected results could be shared to an unintended destination.

Mitigation: Confirm the selected results and destination before sharing; Outlook output is a draft and is not sent.

Risk: Finding, adding, or rechecking data and recurring monitors can incur costs or continue to run.

Mitigation: Review prices and monitor limits before starting work; define scope, cadence, and validity, then pause or revoke monitors when no longer needed.

Risk: The remote service's permissions, data handling, and enforcement were not verified.

Mitigation: Use a SpecStream connection you trust.

## Reference(s):

- [ClawHub release](https://clawhub.ai/specstream/skills/specstream-continue-work)
- [SpecStream MCP server](https://api.specstream.ai/mcp)

## Skill Output:

**Output Type(s):** [Analysis, Files, Guidance]

**Output Format:** [Finding summaries and structured result exports (CSV, Excel, JSON, or HTML)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves observed values, sources, and read times; follows result pagination and reports decision details.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
