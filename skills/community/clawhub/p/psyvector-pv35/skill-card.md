## Description:

Provides emergency-brake and risk-blocking behavior for an agent, with persistent local memory routines described in the artifact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkzfhq](https://clawhub.ai/user/jkzfhq)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users can install this skill to steer an agent toward emergency stops and risk reminders in crisis or high-velocity decision contexts. The artifact also describes automatic local memory storage and recall across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to automatically persist and reload personal or operational memories across sessions.

Mitigation: Review before installing, install only when persistent memory is desired, and manage the local memory file deliberately.

Risk: Stored memories may contain user preferences, decisions, or other sensitive operational information.

Mitigation: Limit what is stored and inspect or delete the local memory file when the retained context is no longer appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkzfhq/skills/psyvector-pv35)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local memory operations under ~/.openclaw/pv_palace/.]

## Skill Version(s):

3.0.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
