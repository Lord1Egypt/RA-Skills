## Description:

Governed Veeam Backup & Replication operations for health checks, diagnostics, backup jobs, restores, repositories, and session tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

External Veeam administrators and developers use this skill to inspect backup health, diagnose failed jobs and low-capacity repositories, manage backup jobs, and track restore progress through CLI or MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks this skill suspicious because connected-model guidance reportedly permits destructive backup actions without action-specific approval; scan coverage was partial.

Mitigation: Use read-only or restricted Veeam credentials where possible. Before enabling writes, verify the approval behavior and review dry-run previews for destructive actions; check audit health.

## Reference(s):

- [Project homepage (Clawdis metadata)](https://github.com/AIops-tools/Veeam-AIops)
- [Capabilities](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Setup guide](references/setup-guide.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Structured JSON results and concise text reports, with CLI commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some reads may be paginated or explicitly marked as truncated.]

## Skill Version(s):

0.20.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
