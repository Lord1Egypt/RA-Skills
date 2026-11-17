## Description:

Create, update, hide, show, list, and delete Übersicht desktop widgets on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paranoidearth](https://clawhub.ai/user/paranoidearth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use Widget to create, install, update, hide, show, list, and delete Übersicht desktop widgets. The skill helps agents generate JSX widgets, install built-in templates, and guide host setup for a local macOS widget environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can make persistent host changes, including installing or starting Übersicht and copying the skill into ~/.claude.

Mitigation: Run setup only on a macOS host where those changes are intended, and use the check mode first when diagnosing the environment.

Risk: The widget installer can overwrite files outside the widget folder when given an unsafe custom target name.

Mitigation: Avoid custom target names until path validation is added; prefer built-in template filenames and review the destination before installation.

Risk: Widget management actions can modify or delete files in the Übersicht widgets directory.

Mitigation: Review requested hide, show, delete, and replacement actions before allowing them, and keep backups of important widget files.

Risk: Some templates run local shell commands, query system state, control audio settings, or call an external weather endpoint.

Mitigation: Inspect the selected template before installation and disable templates whose local command, network, or interactive behavior is not acceptable.

## Reference(s):

- [Widget ClawHub release](https://clawhub.ai/paranoidearth/skills/widget)
- [Reusable widget patterns](patterns.md)
- [Homebrew](https://brew.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSX widget code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or copy .jsx widget files and propose macOS setup commands for Übersicht.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
