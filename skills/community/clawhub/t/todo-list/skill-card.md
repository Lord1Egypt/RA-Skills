## Description:

Manages todo items with add, list, completion, deletion, due reminders, tags, projects, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yushenliu06](https://clawhub.ai/user/yushenliu06)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage personal or workspace todo lists from an agent, including task reminders, tags, project tracking, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder cleanup has a confirmed command-injection flaw.

Mitigation: Remove all shell=True reminder deletion calls, validate cron job IDs, and review the skill before installation.

Risk: The skill stores chat routing data and can send todo status or lists to a configured chat target.

Mitigation: Require clear confirmation before external sends and verify channel and target settings before enabling reminders or status delivery.

Risk: The skill copies user-selected attachments and stores todo data locally.

Mitigation: Attach only intended files, avoid sensitive attachments, and harden attachment path handling before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yushenliu06/skills/todo-list)
- [Artifact README](artifact/README.md)
- [Todo reference](artifact/TODO-REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the skill may create local JSON data, attachment copies, session routing configuration, and OpenClaw cron reminders under ~/.openclaw/workspace/memory/.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
