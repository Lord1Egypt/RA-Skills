## Description:

Coordinates a child wake-up routine through the installed xiaodu-control-official skill, preferring existing XiaoDu IoT scenes and falling back to conservative smart-screen and supported device actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dueros-mcp](https://clawhub.ai/user/dueros-mcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a configured XiaoDu control skill use this skill to coordinate a wake-up routine for a child, preferring existing scenes and falling back to safe, sequential smart-screen and IoT actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store household wake-up preferences in shared memory and later reuse them when controlling smart-home devices.

Mitigation: Use skill-scoped preference storage with explicit consent, clear deletion controls, and confirmation before reusing older preferences for device control.

Risk: Default wake-up behavior may be unclear about which actions happen automatically versus only after a user asks.

Mitigation: Document default actions separately from requested optional actions, and confirm before controlling ambiguous rooms or devices.

Risk: Household device inventory in documentation can expose sensitive home-context details.

Mitigation: Remove real household inventory from public documentation or replace it with sanitized examples.

## Reference(s):

- [Usage notes](references/usage-notes.md)
- [Test cases](references/test-cases.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with sequential shell command examples and natural-language status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions are planned as a single sequential routine, with unsupported or unconfirmed devices skipped rather than assumed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
