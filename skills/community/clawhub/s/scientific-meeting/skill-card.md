## Description:

Helps teams plan, run, review, and follow up on meetings using a scientific meeting framework, Tencent Meeting CLI workflows, and a Feishu Bitable task board.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1027399464-tech](https://clawhub.ai/user/1027399464-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, team leads, and meeting facilitators use this skill to prepare structured agendas, guide live meeting behavior, generate concise meeting reviews, calculate meeting ROI, and convert decisions into tracked tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose or execute meeting and task-board write actions through Tencent Meeting and Feishu workflows.

Mitigation: Require explicit user confirmation after showing the action details before creating, updating, canceling, inviting, removing, calling, kicking, batch-writing, or updating records.

Risk: Tencent Meeting and Feishu credentials are needed for the integrated workflows.

Mitigation: Store credentials only in the documented ~/.config files with mode 600, avoid printing tokens or secrets, and limit the Feishu app to the intended Bitable permissions and workspace.

Risk: Installing the Tencent Meeting CLI with an unpinned global npm command may introduce supply-chain or version drift risk.

Mitigation: Review or pin the tmeet package version before global installation in managed or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1027399464-tech/skills/scientific-meeting)
- [Publisher profile](https://clawhub.ai/user/1027399464-tech)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, code]

**Output Format:** [Markdown guidance with inline shell commands and JSON task data examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Tencent Meeting CLI and a Feishu Bitable helper script when the required user credentials and confirmations are present.]

## Skill Version(s):

3.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
