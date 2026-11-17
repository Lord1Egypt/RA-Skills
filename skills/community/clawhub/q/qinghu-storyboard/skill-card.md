## Description:

Creates video storyboard scripts, camera movement suggestions, and storyboard images from product details and optional images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketers use this skill to plan product videos with shot-by-shot scripts, camera directions, and storyboard images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install or update external Node and qhkit tooling in the user's environment.

Mitigation: Review the package source and version, pin qhkit where possible, and approve installations and any PATH or shell startup changes manually.

Risk: Generating images requires configuring a Qinghu API token.

Mitigation: Configure the token through the documented qhkit configuration or environment variable without sharing it in chat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-storyboard)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images]

**Output Format:** [A shot-by-shot Markdown storyboard script with generated storyboard images when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation requires a Qinghu API token; script-only output is available without images.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
