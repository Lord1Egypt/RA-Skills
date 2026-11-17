## Description:

Converts a topic or article into a multi-image Xiaohongshu/RedNote knowledge carousel with 3:4 PNG slides for business owners, entrepreneurs, and knowledge creators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horisony](https://clawhub.ai/user/horisony)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to turn source topics or articles into dense, polished RedNote/Xiaohongshu knowledge carousels for professional or entrepreneurial audiences. It plans slide structure, visual style, and image export expectations for 1080x1440 PNG output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner summary says the skill asks for an unexplained LibTV/Liblib API key requirement.

Mitigation: Review the API key requirement before installation, avoid placing real credentials in TOOLS.md, and prefer environment variables or a secret manager when credentials are needed.

Risk: The scanner summary says the skill may add fixed BaoAI branding and engagement prompts without clear user control.

Mitigation: Review generated slides before publication and remove or revise branding and calls to action when they do not match the user's account or consent.

Risk: The scanner guidance flags external Google Fonts usage for confidential content.

Mitigation: Disable external font loading or use local fonts when working with confidential or restricted material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horisony/skills/snapdesign-rednote)
- [Publisher profile](https://clawhub.ai/user/horisony)
- [Liblib API key provider](https://liblib.ai)
- [Google Fonts stylesheet dependency](https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with HTML/CSS/JavaScript and shell or Python command snippets for generating PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected agent output is a set of 3:4 PNG carousel images, typically 1080x1440 pixels, plus any supporting local generation files.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
