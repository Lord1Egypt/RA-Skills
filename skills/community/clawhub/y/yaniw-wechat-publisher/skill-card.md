## Description:

Helps agents manage multiple WeChat Official Accounts, generate account-specific article drafts, create cover images, and publish approved content to WeChat drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgedu-new](https://clawhub.ai/user/zgedu-new)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate one or more WeChat Official Accounts by drafting posts, selecting cover styles, managing account configuration, and publishing approved drafts through the WeChat API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat publishing credentials and the evidence security summary flags a credential-like AppSecret in the documentation.

Mitigation: Review credential handling before installation, replace any credential-like example with unmistakably invalid placeholders, and rotate the value if it was ever real.

Risk: The security guidance flags access-token previews and missing support files for documented environment-variable workflows.

Mitigation: Stop printing access-token previews, add the documented .env.example and .gitignore files when relying on them, and provide credentials only in an isolated environment.

Risk: The skill can upload media and create WeChat drafts for configured accounts.

Mitigation: Provide only credentials for accounts the agent is intended to publish drafts for, and retain the documented user-confirmation steps before publishing.

Risk: The security guidance notes unpinned Python dependencies.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zgedu-new/skills/yaniw-wechat-publisher)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [Workflow guide](references/workflow_guide.md)
- [Article format](references/article_format.md)
- [Cover styles](references/cover_styles.md)
- [Configuration template](references/config.template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown article drafts, HTML and PNG cover assets, JSON configuration and logs, shell commands, and concise status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before content approval, cover selection, and publishing.]

## Skill Version(s):

1.1.0 (source: server release evidence and changelog, released 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
