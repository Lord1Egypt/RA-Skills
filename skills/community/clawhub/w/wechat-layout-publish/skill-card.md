## Description:

Turns article content into WeChat Official Accounts compatible Markdown and themed HTML, presents built-in Welight theme choices, and can publish drafts or formal posts when WeChat prerequisites are configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[08820048](https://clawhub.ai/user/08820048)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, editors, and publishing teams use this skill to normalize article sources into Markdown, choose a built-in WeChat layout theme, generate WeChat-compatible HTML, and publish through configured WeChat Official Accounts credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing can upload local files or remote article images to WeChat.

Mitigation: Use dry-run first and inspect every cover path, content image source, and generated payload before real publishing.

Risk: WeChat credentials and article content may be routed through a configured proxy.

Mitigation: Use only an administratively controlled HTTPS proxy, and keep WECHAT_APP_SECRET out of shared files.

Risk: Untrusted HTML or article URLs can introduce unwanted content into the generated WeChat output.

Mitigation: Normalize content to Markdown, review the canonical Markdown, and avoid publishing untrusted HTML without manual inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/08820048/skills/wechat-layout-publish)
- [Publish Spec](artifact/references/publish-spec.md)
- [Runtime Config](artifact/references/runtime-config.md)
- [Theme Catalog](artifact/references/theme-catalog.md)
- [Execution Spec](artifact/references/repo-map.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, WeChat-compatible HTML, JSON metadata, and command-oriented publishing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local article, metadata, rendered HTML, dry-run payload, or publish-result files depending on the selected workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
