## Description:

Manage V2RayN on macOS to list nodes, test proxy connections, check current node status, view logs, and support auto-failover via scripted health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiangwang375-wq](https://clawhub.ai/user/qiangwang375-wq)

### License/Terms of Use:


## Use Case:

Developers and users managing V2RayN on macOS use this skill to check proxy status, inspect configured nodes and logs, test connectivity, and set up cautious health-check automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring health checks can run unattended from an unsafe or mutable script path.

Mitigation: Add the cron job only when the script is stored in a fixed user-owned path with restrictive permissions, and keep removal steps documented.

Risk: A broad restart command can stop unintended processes or disrupt a running proxy session.

Mitigation: Do not run the restart command with sudo; prefer a V2RayN-specific quit and reopen method instead of pkill -f.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes macOS-oriented commands for status checks, log inspection, connectivity testing, and optional recurring health checks.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
