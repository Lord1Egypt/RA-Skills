## Description:

Wx Huitu helps agents turn WeChat article text or data descriptions into publication-ready PNG chart packages using chart recommendations, generated HTML, and Puppeteer screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, analysts, and developers use this skill to extract chart-worthy data from WeChat article drafts or data descriptions, choose an appropriate C01-C18 chart layout, and produce PNG charts for article embedding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The screenshot workflow launches Chrome or Edge through Puppeteer and disables the browser sandbox while rendering generated HTML.

Mitigation: Review before installing and run chart rendering in a low-privilege or isolated environment when processing untrusted article content.

Risk: Generated chart data can leave the local environment if Feishu cloud sync is enabled.

Mitigation: Keep cloud sync off by default and enable it only after explicit user confirmation for content that is acceptable to upload.

Risk: The workflow writes generated PNG and HTML files to local storage.

Mitigation: Use a known output directory and review generated files before sharing or publishing them.

Risk: The generated HTML loads Google Fonts over the network.

Mitigation: Avoid rendering sensitive or restricted content unless network access is acceptable for the environment.

## Reference(s):

- [Skill Definition](SKILL.md)
- [README](README.md)
- [Workflow Reference](references/workflow.md)
- [Chart System Reference](references/chart-system.md)
- [Design Tokens Reference](references/design-tokens.md)
- [ClawHub Skill Page](https://clawhub.ai/edwardwason/skills/wx-huitu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with generated HTML/CSS/SVG and PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated chart files are saved locally; Feishu upload is optional and requires explicit user confirmation.]

## Skill Version(s):

2.2.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
