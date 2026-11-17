## Description:

Generate a SuperCoolPeep avatar from supercoolpeeps.com using a 68-digit seed and optional trait type such as ape, skeleton, or zombie.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbdbking](https://clawhub.ai/user/dbdbking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to generate SuperCoolPeep avatar images from random or supplied 68-digit seeds, including optional ape, skeleton, and zombie trait selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Chromium browser with sandbox protections disabled while loading a remote website.

Mitigation: Run it only in a disposable or tightly sandboxed environment and consider removing the no-sandbox Chromium flags before use.

Risk: Generated output depends on remote content from supercoolpeeps.com.

Mitigation: Review the generated image and rerun in a controlled network environment when reproducibility or content assurance matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dbdbking/skills/supercoolpeep-generator)
- [Publisher profile](https://clawhub.ai/user/dbdbking)
- [SuperCoolPeeps website](https://supercoolpeeps.com)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated PNG file when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a 68-digit seed and optional ape, zombie, or skeleton trait argument.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
