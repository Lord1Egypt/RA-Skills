## Description:

WorkflowHub helps Codex, OpenClaw, or similar agents remember repeated multi-step work as reusable local workflows, ask before reusing a matching SOP, and offer to save or update workflows after a task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyuqi98](https://clawhub.ai/user/zhangyuqi98)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use this skill to turn recurring agent tasks into local JSON workflows that can be matched, confirmed, compiled into execution briefs, and saved or updated after use. It is intended for repeated multi-step work where explicit confirmation is needed before reusing an existing SOP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web editor can save or delete persistent workflow instructions without authentication or origin checks.

Mitigation: Keep the UI bound to 127.0.0.1, close it when not actively editing workflows, and add authentication or origin checks before using it for sensitive workflows.

Risk: Saved workflows can influence future agent behavior if a user approves reuse.

Mitigation: Inspect workflow JSON before approving reuse, require explicit confirmation before applying a matched SOP, and keep recoverable backups of important workflow files.

## Reference(s):

- [WorkflowHub ClawHub skill page](https://clawhub.ai/zhangyuqi98/skills/workflow-memory-skills)
- [runtime-behavior.md](references/runtime-behavior.md)
- [workflow-schema.md](references/workflow-schema.md)
- [local-ui-spec.md](references/local-ui-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON workflow files, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, render, match, or delete local workflow JSON files when the user confirms the action.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
