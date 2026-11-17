## Description:

Helps agents use the rem CLI to manage macOS Reminders, including reminder and list CRUD, search, natural-language due dates, import/export, and script-friendly output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bro3886](https://clawhub.ai/user/bro3886)

### License/Terms of Use:


## Use Case:

Developers and automation users use this skill to manage Apple Reminders from agent workflows and terminal scripts on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended installation paths can execute mutable remote code or install the latest unpinned source.

Mitigation: Use a pinned, signed, or checksum-verified release before installing.

Risk: `rem skills install` can write into AI-agent skill directories and affect later agent sessions.

Mitigation: Review generated skill files and install only into trusted agent environments.

Risk: Reminder and list deletion commands can remove local Reminders data.

Mitigation: Review targets before destructive commands and avoid `--force` unless the target is confirmed.

## Reference(s):

- [Complete Command Reference](references/commands.md)
- [Natural Language Date Reference](references/dates.md)
- [rem install script](https://rem.sidv.dev/install)
- [go-eventkit docs](https://github.com/BRO3886/go-eventkit)
- [ClawHub skill page](https://clawhub.ai/bro3886/skills/rem-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON, CSV, table, or plain-text CLI output examples when describing rem workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
