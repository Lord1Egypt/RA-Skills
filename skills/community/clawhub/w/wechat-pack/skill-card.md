## Description:

Converts local .docx, Markdown, or HTML files into WeChat-ready HTML and a publish folder containing source files, local assets, optional cover images, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockbotclub](https://clawhub.ai/user/rockbotclub)

### License/Terms of Use:


## Use Case:

Developers and content publishers use this skill to package local articles for WeChat public account publishing with local asset copies and copy-paste HTML output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe asset handling could copy unintended local files or fetch unsafe remote URLs when processing untrusted documents.

Mitigation: Use only trusted local inputs, avoid documents with remote image URLs or unusual local image paths, and inspect generated assets before sharing or publishing.

Risk: Generated HTML from untrusted source documents may carry unsafe or unexpected content.

Mitigation: Do not open generated HTML from untrusted inputs in a sensitive browser context; review the output before pasting it into WeChat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rockbotclub/skills/wechat-pack)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Publish folder containing source files, local assets, optional cover variants, WeChat-ready HTML, and meta.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pandoc for .docx conversion; Pillow enables optional cover image variants.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
