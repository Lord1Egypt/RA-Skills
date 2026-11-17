## Description:

Monitors server CPU, RAM, Docker containers, and configured websites, with status reporting and restart-oriented recovery actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnsmh](https://clawhub.ai/user/mrnsmh)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check server resource health, Docker container state, and named web service availability. It supports operational status review and restart-oriented recovery for monitored services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic recovery and service restart behavior could disrupt production workloads if monitored targets, restart scope, and approval boundaries are unclear.

Mitigation: Require explicit configuration for monitored resources, use approval or report-only mode before production restarts, log actions, and provide a way to disable recurring self-healing.

Risk: Operational status output may expose service names, URLs, container state, or infrastructure details.

Mitigation: Restrict use and report sharing to authorized operators, and redact sensitive infrastructure details before external distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrnsmh/skills/supervisorclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text operational status summaries, with JSON status output from the bundled monitor script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports resource percentages, HTTP health, and Docker container status for configured targets.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
