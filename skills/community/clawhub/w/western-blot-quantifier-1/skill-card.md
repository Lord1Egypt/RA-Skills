## Description:

Automatically identify Western Blot gel bands, perform densitometric analysis, and calculate normalized values relative to loading controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a bounded workflow helper for Western Blot band quantification tasks, including reviewing inputs, assumptions, and limitations before returning results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill materially overstates its Western Blot analysis capability.

Mitigation: Review outputs carefully and do not rely on the skill for scientific quantification until real image loading, input validation, documented normalization, and documented exports are verified.

Risk: The security review identifies broad unpinned dependencies.

Mitigation: Install and run the skill only in an isolated virtual environment or container with audited, pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/western-blot-quantifier-1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, CLI commands, and CSV-style result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to generated quantification results and visualization paths when supported by validated inputs and execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and scripts/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
