## Description:

Automates daily WeChat Official Account article creation by finding hot topics, drafting SEO-oriented HTML, preparing images, and creating a WeChat draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimo970](https://clawhub.ai/user/jimo970)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and account operators use this skill to generate Chinese travel and food articles, prepare supporting imagery, and save drafts for a named WeChat Official Account. It is intended for users who control the target WeChat and Feishu credentials and can review generated content before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires WeChat and Feishu API credentials and can create drafts or send notifications on connected accounts.

Mitigation: Use credentials only for accounts you control, scope access where possible, and review generated drafts before any publication or notification workflow runs.

Risk: The artifact includes fixed account promotion and QR instructions that may not match the installing user's account.

Mitigation: Review or remove the promotional footer, QR reference, and account-specific copy before using the skill.

Risk: The scripts download and upload images and process HTML, local file paths, and remote URLs.

Mitigation: Use trusted image sources and HTML inputs, validate local paths, and harden the upload and download helpers before handling untrusted content.

Risk: The artifact includes a recurring scheduled task example for automated daily execution.

Mitigation: Enable scheduling only when recurring automated runs are intended and monitored.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jimo970/skills/wechat-daily-article)
- [Content Type Templates](references/content-types.md)
- [Image Prompt Guidelines](references/image-prompts.md)
- [WeChat SEO Guidelines](references/seo-guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese prose, HTML article drafts, Markdown guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated articles may include local or remote image references that the bundled scripts upload to WeChat; Feishu notification output is optional.]

## Skill Version(s):

1.8.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
