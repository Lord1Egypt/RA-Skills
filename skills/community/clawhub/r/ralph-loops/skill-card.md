## Description:

Runs autonomous iterative AI loops for requirements, planning, and building workflows using structured prompts and fresh context per iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qlifebot-coder](https://clawhub.ai/user/qlifebot-coder)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use Ralph Loops to run structured autonomous iteration across requirements interviews, implementation planning, and build tasks while preserving progress in files and loop state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous loop execution can act with broad local authority and permission checks disabled.

Mitigation: Run it only in an isolated VM or container, use a disposable branch, provide task-specific credentials only, and review diffs before any push or tag.

Risk: Dashboard, process, and Git controls are underprotected according to the authoritative security evidence.

Mitigation: Disable the dashboard or restrict it to loopback with authentication, and avoid repositories or workspaces containing sensitive files until those issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qlifebot-coder/skills/ralph-loops)
- [Ralph Loops skill documentation](artifact/SKILL.md)
- [Ralph Loops setup guide](artifact/SETUP.md)
- [Geoffrey Huntley Ralph technique](https://ghuntley.com/ralph/)
- [Clayton Farr Ralph Playbook](https://github.com/ClaytonFarr/ralph-playbook)
- [How to Ralph Wiggum fork](https://github.com/ghuntley/how-to-ralph-wiggum)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prompts, markdown specs and plans, code edits, shell command output, and JSON loop state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write project files, update Git history through configured prompts, and archive loop state under ~/clawd/logs/ralph-archive.]

## Skill Version(s):

1.0.2 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
