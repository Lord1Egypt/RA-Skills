## Description:

Keep the Feishu registry sheet in sync whenever a new local skill, workflow, or template is created or significantly updated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g-hanasq](https://clawhub.ai/user/g-hanasq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep local skills, reusable workflows, and templates represented in a Feishu registry sheet or queued in a local backlog when direct sync is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically write metadata to a named Feishu sheet or local backlog without explicit user confirmation.

Mitigation: Review the target tab, fields, and write destination before use; add a dry-run or confirmation step for environments where unintended registry updates would be harmful.

Risk: The skill references a specific Feishu registry and local OpenClaw workspace paths that may not match the installing user's environment.

Mitigation: Confirm the registry URL and local workspace paths before enabling the skill, or adapt them to the intended workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g-hanasq/skills/registry-sync)
- [Publisher profile](https://clawhub.ai/user/g-hanasq)
- [Feishu registry sheet](https://bytedance.larkoffice.com/sheets/Bf6qsMV9fhqrD6tPE6TcQhF7nEe)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text]

**Output Format:** [Markdown or concise text confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe whether registry changes were written directly or queued.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
