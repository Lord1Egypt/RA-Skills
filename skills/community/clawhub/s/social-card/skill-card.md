## Description:

Generate social preview images (OG, Twitter, GitHub) with a fluent builder API. Single dependency - Pillow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to generate branded social preview images for websites, repositories, profiles, and automated publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill requires trusting the current social-card package from PyPI.

Mitigation: Install in a virtual environment and pin the package version before use.

Risk: Rendering writes image files to local paths, which can overwrite existing files if a target path is reused.

Mitigation: Render to a controlled output directory and avoid paths where replacing an existing image would matter.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vveerrgg/skills/social-card)
- [GitHub Repository](https://github.com/HumanjavaEnterprises/huje.socialcard.OC-python.src)
- [PyPI Package](https://pypi.org/project/social-card/)
- [huje.tools](https://huje.tools)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with Python and bash code blocks, plus generated image files or image bytes when used by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local social preview images in PNG, JPEG, or WEBP formats through the social-card Python package.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
