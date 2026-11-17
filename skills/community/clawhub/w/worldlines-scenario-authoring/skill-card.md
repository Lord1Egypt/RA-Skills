## Description:

WorldLines scenario creation and revision with clear multi-agent dialogue, validation, and real-model playtesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and narrative designers use this skill to create or revise WorldLines worlds, scene flows, Soul dialogue, player-facing presentation, and validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may read local WorldLines project context and player/profile files while validating scenarios.

Mitigation: Read only the local context needed for scenario validation and keep work scoped to the owned world root.

Risk: Scenario edits or test runs could affect engine code, credentials, installed packages, or existing saves if scope is not controlled.

Mitigation: Keep engine code, credentials, installed packages, and existing saves unchanged unless separately authorized; use disposable test roots for playtesting.

Risk: Adapted or embedded source material can create provenance or rights confusion.

Mitigation: Document the title, author, edition or URL, provenance, and permitted-use basis for each embedded source before copying text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/worldlines-scenario-authoring)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with proposed file edits, validation steps, test commands, and scenario text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are scoped to WorldLines scenario authoring and validation tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
