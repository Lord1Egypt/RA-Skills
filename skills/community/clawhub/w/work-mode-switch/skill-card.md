## Description:

OpenClaw agent work-mode switching guidance for 12 collaboration modes, including free, chat, planning, research, deep research, writing, coding, translation, execution, review, self-check, and self-learning modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jijinbao-code](https://clawhub.ai/user/jijinbao-code)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to choose an appropriate collaboration mode and set expectations for how an AI assistant should respond to different task types. It is intended to guide behavior through documentation rather than perform actions on its own.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous wording may cause an agent to interpret casual phrases as mode-switching instructions.

Mitigation: Prefer explicit commands such as "switch to review mode" and confirm the intended mode before changing behavior.

Risk: Mode guidance can encourage file creation, cleanup, memory updates, or system-maintenance suggestions in some workflows.

Mitigation: Confirm with the user before allowing file operations, cleanup, memory updates, or system-maintenance actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jijinbao-code/skills/work-mode-switch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text guidance with task-specific outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by selected mode and may include discussion notes, research reports, documents, code, review findings, checklists, or learning plans.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
