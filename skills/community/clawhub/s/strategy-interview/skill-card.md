## Description:

Strategy Interview guides users through a structured conversation to build or think through strategy for a company, product, team, career, or initiative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and strategy practitioners use this skill to develop a grounded strategy through guided discovery, challenge framing, kernel development, and pressure-testing before producing strategy notes or a strategy draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential strategy, personnel, competitive, or career details may be persisted in local working notes or final Markdown files.

Mitigation: For sensitive discussions, use chat-only mode or require confirmation before writing .beagle state, strategy-notes.md, or strategy-draft.md files.

Risk: Premature strategy drafts can present untested assumptions as confident guidance.

Mitigation: Do not produce strategy-draft.md until the strategy kernel has been confirmed, unless the user explicitly requests a provisional draft with unconfirmed elements marked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/strategy-interview)
- [The Kernel of Good Strategy](references/kernel.md)
- [Bad Strategy: Patterns to Catch in Real Time](references/bad-strategy.md)
- [Landscape Mapping: Seeing the Terrain Before Choosing the Route](references/wardley-mapping.md)
- [The Strategic Choice Cascade](references/playing-to-win.md)
- [Value Innovation: When the Real Problem Is the Competitive Arena Itself](references/blue-ocean.md)
- [Output Templates](references/output-template.md)
- [Pressure-test scenarios](references/pressure-tests.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Conversational guidance and Markdown files such as strategy-draft.md, strategy-notes.md, and optional .beagle strategy state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local working notes and final Markdown strategy artifacts when the interview reaches the appropriate phase and the user confirms file output.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
