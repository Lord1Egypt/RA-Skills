## Description:

Intent-based model router that detects fix, plan, and flow requests and routes them to the configured AI model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wizelements](https://clawhub.ai/user/wizelements)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, OpenClaw users, and teams use this skill to standardize model selection by routing debugging, planning, and general prompts to configured agents or cloud models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be routed automatically to cloud model providers.

Mitigation: Confirm which providers may receive prompts and avoid sending secrets or sensitive customer data unless the selected provider is trusted.

Risk: Setup scripts and shell aliases are referenced but not included in the provided artifact files.

Mitigation: Verify any setup script or shell profile changes from a trusted source before running or sourcing them.

Risk: Broad trigger words may route a prompt to an unintended model.

Mitigation: Review routing behavior for sensitive workflows and use the documented override flags when a specific model is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wizelements/skills/smart-router-ai)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit intent labels, confidence scores, model routing choices, shell aliases, dashboard commands, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: release metadata, skill frontmatter, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
