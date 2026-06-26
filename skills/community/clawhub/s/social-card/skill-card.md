## Description: <br>
Generate social preview images (OG, Twitter, GitHub) with a fluent builder API. Single dependency - Pillow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content publishers, and automation agents use this skill to generate local Open Graph, Twitter/X, GitHub, square, and custom social preview images from titles, subtitles, tags, themes, and brand colors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and imports the external `social-card` Python package. <br>
Mitigation: Install from a trusted package source, pin the expected version where appropriate, and review the package before using it in sensitive publishing workflows. <br>
Risk: Generated social preview images can misrepresent a project, page, or entity if prompts or source text are wrong. <br>
Mitigation: Review generated cards before publication, especially for branded, legal, financial, or customer-facing content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vveerrgg/social-card) <br>
- [Publisher Profile](https://clawhub.ai/user/vveerrgg) <br>
- [GitHub Repository](https://github.com/HumanjavaEnterprises/huje.socialcard.OC-python.src) <br>
- [PyPI Package](https://pypi.org/project/social-card/) <br>
- [huje.tools](https://huje.tools) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying package renders image files or raw PNG, JPEG, and WEBP bytes locally using Pillow.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
