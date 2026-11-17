## Description:

Converts Markdown articles into WeChat Official Account-compatible inline-styled HTML with theme previews, content-structure enhancements, code highlighting, copy-to-WeChat output, and optional draft publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[love254443233](https://clawhub.ai/user/love254443233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and publishing assistants use this skill to format Markdown drafts for WeChat Official Account publishing, compare theme previews, generate WeChat-compatible HTML, and optionally push finished content to a WeChat draft box.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local file discovery can expose more local files than intended when resolving article images.

Mitigation: Narrow vault_root to a specific attachment folder and use only trusted local articles.

Risk: Auto-opened preview files may display unsanitized local article content in a browser.

Mitigation: Review generated previews before use and consider --no-open when processing unfamiliar content.

Risk: Publishing can fetch arbitrary external image URLs and sends article content, images, and WeChat credential-backed requests to WeChat.

Mitigation: Avoid untrusted external image URLs, keep WeChat credentials in environment-managed secrets, and publish only content approved for WeChat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/love254443233/skills/wechat-typeset-pro)
- [Publisher profile](https://clawhub.ai/user/love254443233)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces formatted article HTML, browser preview or gallery files, optional enhanced Markdown, and optional WeChat draft publishing actions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
