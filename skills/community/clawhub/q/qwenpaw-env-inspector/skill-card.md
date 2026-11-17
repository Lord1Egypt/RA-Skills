## Description:

Checks a local QwenPaw environment and recommends repairs for installation, dependency, configuration, permission, connectivity, and plugin issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

QwenPaw users and developers use this skill to diagnose startup failures, installation problems, and skill or plugin loading issues and receive suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The environment-variable check can print full credential values.

Mitigation: Replace the raw check with a presence-only check before running it, and keep diagnostic output private.

Risk: Directory listings and generated reports may expose sensitive local paths or host metadata.

Mitigation: Review and redact reports before sharing them, and run diagnostics only where their output can be kept private.

## Reference(s):

- [QwenPaw Environment Inspector on ClawHub](https://clawhub.ai/trend0522/skills/qwenpaw-env-inspector)
- [QwenPaw website](https://qwenpaw.agentscope.io)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown diagnostic report with issues and suggested repair steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local checks; does not automatically change settings or install packages.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
