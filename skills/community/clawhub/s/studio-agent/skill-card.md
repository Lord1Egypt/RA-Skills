## Description:

Use this for ClickZetta Studio requests such as querying tasks, listing workspaces, checking projects, and creating or running ClickZetta jobs from a single JDBC secret configured in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luketalent](https://clawhub.ai/user/luketalent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with ClickZetta Studio from OpenClaw, including task, job, project, workspace, and SQL workflows through a configured JDBC secret.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on live ClickZetta workspaces using a stored JDBC credential.

Mitigation: Install only in trusted ClickZetta environments and use a least-privileged ClickZetta account for the JDBC secret.

Risk: Auto-approval or always-allow behavior can permit remote actions without case-by-case review.

Mitigation: Avoid enabling always-allow or auto-approve modes unless the workspace and requested operations are already trusted.

Risk: Discovery caches can contain sensitive session or workspace material locally.

Mitigation: Inspect local cache and configuration permissions and clear cached state when access should be revoked.

Risk: SQL, job, and task requests can consume compute or change data.

Mitigation: Review user requests before execution and constrain the configured account to the intended projects and workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luketalent/skills/studio-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/luketalent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON runner results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run a Node.js one-shot runner that returns a single JSON object with success content or structured error details.]

## Skill Version(s):

0.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
