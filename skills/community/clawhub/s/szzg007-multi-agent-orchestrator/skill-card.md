## Description:

Orchestrates multi-agent workflows for MOSSRIVER operations by decomposing tasks, assigning agents, monitoring execution, and summarizing results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szzg007](https://clawhub.ai/user/szzg007)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams and agent developers use this skill to coordinate product-line workflows across multiple agents, including task decomposition, priority handling, progress reporting, and result aggregation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate workflows that process customer or lead data and send outbound emails.

Mitigation: Require explicit human confirmation before customer-data processing, lead handling, or outbound email actions are executed.

Risk: Task reassignment, retries, monitoring alerts, and auto-optimization can affect live operational workflows.

Mitigation: Review and approve reassignment, retry, alerting, and auto-optimization settings before enabling the skill in production.

Risk: Misconfigured queues, webhooks, audit logs, or retention settings could route work or data incorrectly.

Mitigation: Verify task queue paths, webhook destinations, audit logging, and retention settings before activation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szzg007/skills/szzg007-multi-agent-orchestrator)
- [Publisher profile](https://clawhub.ai/user/szzg007)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline examples, configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task decomposition reports, execution progress reports, result summaries, priority definitions, and agent coordination guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
