## Description:

Convert manual incident runbooks into automated, executable playbooks. Parse existing runbooks, generate scripts for each step, add health checks, rollback procedures, and notification hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this skill to convert incident runbooks into executable playbooks, audit existing runbooks for automation gaps, dry-run generated playbooks, and create structured runbook templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated playbooks can translate operational documentation into live Bash commands that affect production systems.

Mitigation: Require qualified operator review and explicit approval before execution; default generated scripts to DRY_RUN=true.

Risk: Source runbooks may contain stale, unsafe, or untrusted operational steps.

Mitigation: Treat source runbooks as untrusted input and inspect each generated command, health check, decision point, and rollback step before use.

Risk: Notification hooks can expose incident details or credentials if misconfigured.

Mitigation: Verify webhook destinations before sending incident details and run generated playbooks with least-privileged credentials in a controlled environment.

## Reference(s):

- [Runbook Automator on ClawHub](https://clawhub.ai/charlie-morrison/skills/runbook-automator)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks, audit tables, templates, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated playbooks may include DRY_RUN controls, health checks, rollback steps, and notification hooks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
