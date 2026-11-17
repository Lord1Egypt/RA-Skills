## Description:

This skill helps WorkBuddy users generate, format, schedule, and submit WeChat Official Account articles from trending topics or custom Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyy1976](https://clawhub.ai/user/andyy1976)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to prepare WeChat Official Account posts by collecting hot topics, generating article drafts, applying WeChat-ready formatting, and sending approved content to the WeChat draft workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat AppSecret and publishing credentials can be exposed if they are stored in a shared or synced plugin directory.

Mitigation: Store credentials outside shared locations when possible, restrict local file permissions, or use a secret manager or environment variable.

Risk: Automated draft submission or scheduled publishing can publish unsuitable content if enabled without review.

Mitigation: Require manual preview and confirmation before publishing drafts or enabling a daily schedule.

Risk: Hot-topic article generation can produce inaccurate, incomplete, or off-brand claims.

Mitigation: Review generated articles and verify important facts before submitting content to WeChat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyy1976/skills/wechat-publisher-3)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Configuration, Guidance]

**Output Format:** [Markdown, WeChat-ready HTML, configuration JSON guidance, and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can prepare draft content for WeChat publishing and support scheduled posting when configured.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
