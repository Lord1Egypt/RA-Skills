## Description:

Generates complete D&D 5e adventure modules across one-shot, short, medium, long, and sandbox structures using a library of narrative paradigms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dajiaohuang](https://clawhub.ai/user/dajiaohuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and tabletop RPG creators use this skill to generate structured D&D 5e adventure modules, write them to Markdown files, and prepare them for campaign import and scene indexing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated module import, re-import, indexing, deletion, or scene export actions can affect an existing campaign database.

Mitigation: Review the generated module file first and require explicit user confirmation before running those actions against an existing campaign.

Risk: Installing from a mutable source can make later installs resolve to different skill content.

Mitigation: Prefer a pinned ClawHub or package version, or an immutable source reference, before installation.

## Reference(s):

- [SagaSmith Module Generator on ClawHub](https://clawhub.ai/dajiaohuang/skills/sagasmith-modulegen)
- [SagaSmith-agent runtime](https://github.com/dajiaohuang/SagaSmith-agent)
- [SagaSmith skills package](https://github.com/dajiaohuang/SagaSmith-skills)
- [D&D DM skill reference](https://github.com/ackiles/dnd-dm-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown adventure modules with optional JSON scene indexes and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes module files under modules/ and asks for review before multi-step generation or existing campaign import actions.]

## Skill Version(s):

1.1.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
