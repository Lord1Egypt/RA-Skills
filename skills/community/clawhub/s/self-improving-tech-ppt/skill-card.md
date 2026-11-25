## Description:

A model-agnostic workflow and Python toolkit for creating and iterating high-density technical architecture and planning slides in editable PowerPoint, with programmatic style checks and visual review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theosunny](https://clawhub.ai/user/theosunny)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical planners use this skill to create or refine executive technical architecture and planning presentations, including single-page schematics. It guides structured content, editable PowerPoint generation, consistency checks, and visual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External document sharing may expose presentation content to unintended recipients.

Mitigation: Review the destination, access controls, and presentation contents before sharing documents.

Risk: The browser renderer runs Chrome with its sandbox disabled.

Mitigation: Render in an isolated environment and avoid processing untrusted content in that browser.

Risk: The documented install command does not pin a release version.

Mitigation: Review the package and choose a specific trusted version before installing.

## Reference(s):

- [Server-resolved source repository](https://github.com/theosunny/self-improving-tech-ppt)
- [ClawHub skill release](https://clawhub.ai/theosunny/skills/self-improving-tech-ppt)
- [Design and anti-AI rules](references/design-and-anti-ai-rules.md)
- [PowerPoint engine](scripts/ppt_engine.py)

## Skill Output:

**Output Type(s):** [PowerPoint presentations, SVG previews, PNG images, Guidance]

**Output Format:** [Editable .pptx files with optional SVG and PNG previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for 16:9 technical architecture and planning slides; visual QA crops may also be produced.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
