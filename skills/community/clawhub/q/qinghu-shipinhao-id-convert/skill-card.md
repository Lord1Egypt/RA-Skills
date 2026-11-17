## Description:

Converts a WeChat Channels ID beginning with sph into the finder username required by downstream Qinghu tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users of Qinghu data tools use this skill to resolve a WeChat Channels short ID to a finder username for subsequent API queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance can install or upgrade a global npm package, add a Node runtime, and change PATH.

Mitigation: Require explicit approval before installation, upgrades, or PATH changes; prefer a preinstalled, pinned qhkit in a contained environment.

Risk: Configuration steps can overwrite local qhkit token or site settings.

Mitigation: Confirm before changing credentials or site settings, and keep API tokens private.

Risk: The lookup is paid and can consume Qinghu credits.

Mitigation: Check the estimate and obtain user authorization before paid calls; report actual credits used.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-id-convert)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with a finder username and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A paid lookup may consume Qinghu credits; requires qhkit and a Qinghu API token.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
