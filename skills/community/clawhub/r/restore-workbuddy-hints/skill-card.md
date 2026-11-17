## Description:

Restores WorkBuddy UI hints and tips that were dismissed with the "Do not show again" button.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users and support agents use this skill to inspect dismissed hint entries, restore a specific hidden hint, or restore all hidden WorkBuddy prompt bars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits WorkBuddy's local user-state.json and can change which UI hints reappear.

Mitigation: Use list mode first, close WorkBuddy before changing state, and restore a specific hint with --key when broad restoration is not intended.

Risk: Manual fallback edits to user-state.json could affect unrelated settings if the file is changed incorrectly.

Mitigation: Limit manual recovery to setting tipShowHistory to an empty object and avoid modifying other fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuwenqi123123/skills/restore-workbuddy-hints)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run a local Python helper that lists or clears WorkBuddy tipShowHistory entries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
