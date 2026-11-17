## Description:

Manage Tencent Cloud CVM instances with the TCCLI command-line tool. Covers instance creation, querying, deletion, launch template management, price inquiry, and related resource cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agilebuilder](https://clawhub.ai/user/agilebuilder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Tencent Cloud CVM instances through TCCLI, including creation, inspection, lifecycle operations, price checks, launch templates, and cleanup of related resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to manage billable Tencent Cloud CVM resources, including instance creation and cleanup.

Mitigation: Require user confirmation for cost-incurring and destructive operations, show price checks before creation, and verify resource release after cleanup.

Risk: Workspace-local defaults may store instance login passwords in plaintext.

Mitigation: Prefer SSH keys, environment variables, runtime entry, or a secrets manager; do not commit the defaults file.

Risk: TAT guidance can enable broad remote shell command execution on cloud instances.

Mitigation: Use narrowly scoped Tencent Cloud permissions, confirm commands before execution, and prefer direct SSH for simple single-machine maintenance.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/agilebuilder/dev-skills/tree/master/skills/tccli-cvm)
- [ClawHub skill page](https://clawhub.ai/agilebuilder/skills/tccli-cvm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, JSON snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that create, modify, delete, or inspect Tencent Cloud resources.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
