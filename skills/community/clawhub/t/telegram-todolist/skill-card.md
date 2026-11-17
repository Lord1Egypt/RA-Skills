## Description:

Telegram Todo List helps an agent manage a workspace TODO.md file through Telegram-style commands for querying, organizing, and completing tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hengbo12345](https://clawhub.ai/user/hengbo12345)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent read, summarize, add, edit, delete, move, and complete tasks in a Markdown todo list from Telegram commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or delete tasks in /root/.openclaw/workspace/TODO.md when given organize or execute commands.

Mitigation: Review intended task changes before running destructive organize or execute actions, and keep a backup of important TODO.md content.

Risk: The artifact uses Chinese default text and response strings.

Mitigation: Adjust the template and output strings or request localization support before using it in an environment that requires another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hengbo12345/skills/telegram-todolist)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, create, update, or delete tasks in /root/.openclaw/workspace/TODO.md when asked to organize or execute todo commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
