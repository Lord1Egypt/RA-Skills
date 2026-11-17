## Description:

Save web articles locally with images by downloading image assets, generating Markdown, and optionally converting the result to PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barryqin9999](https://clawhub.ai/user/barryqin9999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to archive web articles, including WeChat Official Account articles, as local Markdown, image assets, optional HTML/PDF files, and shareable outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact external sites and download untrusted article content or images.

Mitigation: Confirm the source URL before fetching, limit use to trusted sources when possible, and review saved files before opening or sharing them.

Risk: Article text and images, including content from private or authenticated pages, can be persisted locally.

Mitigation: Avoid private or authenticated pages unless persistence is intended, save only to approved workspaces, and delete sensitive outputs after use.

Risk: Generated Markdown or PDF files can be sent to Feishu without tight scope or confirmation.

Mitigation: Require explicit confirmation of the recipient and file path before Feishu delivery.

Risk: The workflow references an external local WeChat helper under ~/.agent-reach.

Mitigation: Review or remove that helper reference before deployment, and only run reviewed local tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barryqin9999/skills/save-article-with-images)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, Python, CSS, and message-command examples; generated article artifacts may include Markdown, downloaded images, HTML, PDF, and metadata JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact external article and image hosts, persist local article artifacts, and send generated files to Feishu when that delivery step is used.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
