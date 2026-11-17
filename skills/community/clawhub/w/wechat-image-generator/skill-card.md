## Description:

Generate beautiful images for WeChat articles, including cover images, comparison graphics, and charts, using local Python scripts and HTML templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingyu525](https://clawhub.ai/user/jingyu525)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to generate WeChat article cover images, side-by-side comparison graphics, and simple data visualizations for social media or technical articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Python scripts and browser automation may execute commands on the user's machine.

Mitigation: Review the package before installation and run it only in a trusted local workspace.

Risk: The screenshot helper accepts file paths and should not be used with arbitrary filenames.

Mitigation: Use it only on trusted generated HTML files and expected output paths.

Risk: The local server helper can expose generated files if run on an untrusted network.

Mitigation: Run the server only on trusted networks or change it to bind to 127.0.0.1 and serve only the intended output directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jingyu525/skills/wechat-image-generator)
- [Project Homepage](https://github.com/jingyu525/wechat-image-generator)
- [Issue Tracker](https://github.com/jingyu525/wechat-image-generator/issues)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML or PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates fixed-size 1200x675 HTML templates and provides browser screenshot commands for PNG capture.]

## Skill Version(s):

1.0.2 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
