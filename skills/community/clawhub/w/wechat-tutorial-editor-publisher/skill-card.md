## Description:

Writes tutorial-style WeChat Official Account articles in Markdown by imitating an author's style and supports publishing them to the WeChat draft box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niko-yang-arch](https://clawhub.ai/user/niko-yang-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and developers use this skill to turn tutorial steps, images, and author profile details into a WeChat-ready Markdown article, then prepare or execute publication through wenyan-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles WeChat publishing credentials and references storing or reading secrets from local files.

Mitigation: Use a proper secret store or short-lived environment injection; do not store WeChat AppSecret in the skill directory or TOOLS.md.

Risk: The helper server accepts personal information and file uploads into writable local directories.

Mitigation: Run the server only on loopback with authentication or a per-session token, and add upload size limits plus file type validation.

Risk: Generated articles can append personal contact details or QR code material.

Mitigation: Require explicit approval for any personal footer, QR code, or contact details before including them in an article.

Risk: The publish script can install a global npm package automatically.

Mitigation: Review the script before execution and prefer a pinned, local dependency installation path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niko-yang-arch/skills/wechat-tutorial-editor-publisher)
- [wenyan-cli GitHub](https://github.com/caol64/wenyan-cli)
- [wenyan website](https://wenyan.yuzhi.tech)
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/offiaccount/)
- [wenyan upload and IP whitelist documentation](https://yuzhi.tech/docs/wenyan/upload)
- [Theme reference](references/themes.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown articles with frontmatter, JSON step data, shell commands, and publishing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local article, image, personal profile, and step-data files before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
