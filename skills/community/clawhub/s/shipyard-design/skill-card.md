## Description:

Helps users choose or change an app's visual style, including colours, typography, layout, homepage design, dark mode, and icons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipposk](https://clawhub.ai/user/philipposk)

### License/Terms of Use:

MIT-0

## Use Case:

Beginners and developers use this skill to choose an app's visual direction and apply a complete, readable light and dark design, with matching guidance and icons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill may lead to commits or pull requests without a clear approval checkpoint.

Mitigation: Review the approval steps and get clear approval before any commit or pull request.

Risk: Unpinned package commands may install changing releases.

Mitigation: Inspect package commands and pin the versions to run before installation.

Risk: Security coverage was incomplete: 12 of 13 components were scanned, and one file was only partly inspected.

Mitigation: Review the partly inspected file and complete a full security scan before relying on the result.

## Reference(s):

- [Shipyard design skill](https://clawhub.ai/philipposk/skills/shipyard-design)
- [Design token guidance](artifact/references/tokens.md)
- [Design direction guidance](artifact/references/directions.md)
- [Ready-made looks](artifact/references/presets.md)
- [Visual quality guidance](artifact/references/anti-slop.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Natural-language guidance and app code or configuration changes, including design tokens and a DESIGN.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The chosen workflow and target app determine which files are produced; visual themes are designed as light and dark pairs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
