## Description:

Operate terminal user interface programs through the tui-agent CLI tool by starting sessions, capturing screens, sending input, and stopping sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbflcy](https://clawhub.ai/user/zbflcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to control terminal-based programs such as editors, system monitors, file managers, database clients, and ncurses applications through repeatable capture-and-input workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to operate local terminal programs through a daemon-backed tui-agent workflow, including editors and shells.

Mitigation: Use it only with explicit user direction for the target program and file paths, review changes before saving files, prefer scoped tools for simple shell commands, and stop tui-agent sessions when finished.

Risk: The security summary classifies the release as suspicious because the automation scope is broad.

Mitigation: Review the skill's scope before installation and apply the evidence guidance for supervised, task-specific use.

## Reference(s):

- [tui-agent source directory](https://github.com/zbflcy/tui-use/tree/main/tui-agent)
- [ClawHub skill page](https://clawhub.ai/zbflcy/skills/tui-use)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes session lifecycle guidance, screen capture and wait patterns, keyboard and mouse commands, platform notes, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
