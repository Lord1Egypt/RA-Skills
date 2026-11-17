## Description:

Learns a persistent local portrait of the user, including language, expertise, knowledge gaps, and communication preferences, so agent replies can be phrased in language the user understands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbc0315](https://clawhub.ai/user/zbc0315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain a local, editable user portrait that helps the agent adjust language, vocabulary level, and response style across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains a cross-session local profile that can influence future replies across projects.

Mitigation: Review ~/.claude/user-portrait/profile.md periodically and use the pause or reset controls when ongoing personalization is not wanted.

Risk: The portrait may contain inferred language, expertise, knowledge gaps, or communication preferences that should not carry over on shared machines or sensitive contexts.

Mitigation: Avoid installing it on shared machines, and use show, correct, pause, resume, reset, or manual edits to keep the local profile under user control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zbc0315/skills/user-portrait)
- [Related user-portrait Claude Code plugin](https://github.com/zbc0315/user-portrait)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with local file paths and shell commands when managing the portrait]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local portrait file and pause marker under ~/.claude/user-portrait/.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
