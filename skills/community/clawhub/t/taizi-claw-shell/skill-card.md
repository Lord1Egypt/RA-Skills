## Description:

Runs shell commands inside a dedicated tmux session named 'claw', returning command output and prompting before destructive commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run shell commands in a dedicated tmux session named 'claw' and read back command output while keeping that work separate from other tmux sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides broad shell authority and may expose sensitive files, credentials, or network access if installed in a privileged environment.

Mitigation: Use only in a tightly sandboxed environment with no sensitive files, credentials, or network access.

Risk: User-supplied shell input may execute outside the stated tmux boundary and the current safety controls are weak.

Mitigation: Call tmux with argument arrays instead of shell strings and add real user approval or stricter command policy before trusting the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fresh3/skills/taizi-claw-shell)
- [Publisher profile](https://clawhub.ai/user/fresh3)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [JSON object containing the submitted command and captured terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns captured output from the latest tmux pane contents after command execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
