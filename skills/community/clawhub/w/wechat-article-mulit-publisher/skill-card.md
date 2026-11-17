## Description:

Extracts articles from Markdown files or web links and prepares or publishes them to WeChat Official Accounts with multi-account support, standard and viral templates, cover image generation, and draft publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diwuwudi123](https://clawhub.ai/user/diwuwudi123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to convert trusted Markdown files or article URLs into WeChat Official Account previews, drafts, material uploads, or publish submissions across configured accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or delete content in a real WeChat Official Account.

Mitigation: Review commands before execution, run with --dry-run first, and use --publish or --delete-draft only after confirming the target account and media ID.

Risk: Trusted input boundaries matter because Markdown or HTML can reference local image paths or remote URLs that the script may upload or fetch.

Mitigation: Use trusted article inputs in a dedicated, low-privilege working directory and avoid processing untrusted Markdown or HTML.

Risk: Remote and local content upload behavior can expose unintended material to the WeChat account.

Mitigation: Inspect generated preview HTML and resolved image sources before running non-dry-run publish or material upload commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diwuwudi123/skills/wechat-article-mulit-publisher)
- [Publisher profile](https://clawhub.ai/user/diwuwudi123)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON runtime results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write preview HTML files and can create, publish, list, or delete WeChat drafts and upload image materials when the corresponding commands are run.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
