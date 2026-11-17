## Description:

Convert a local Markdown article into clean WeChat Official Account HTML, with an optional explicitly confirmed draft upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operators use this skill to convert reviewed Markdown articles into WeChat-compatible HTML and, when explicitly confirmed, upload a draft to a configured WeChat Official Account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown can carry unwanted or misleading content into the generated preview HTML because the preview is not sanitized.

Mitigation: Only convert trusted Markdown and review the generated local HTML before sharing or uploading it.

Risk: A confirmed upload sends reviewed article content and optional cover images to a configured WeChat Official Account.

Mitigation: Keep WeChat credentials in environment variables or a secret store, confirm the destination account, and require both --upload and --confirm-upload before uploading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangchao228/skills/wx-md-article)
- [Project homepage](https://github.com/yangchao228/wx-md-article)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated HTML output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default operation generates a local HTML file; upload requires both --upload and --confirm-upload with WeChat credentials supplied outside the skill.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
