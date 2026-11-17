## Description:

Automatically collects AI news, formats it into WeChat public-account HTML, and creates scheduled WeChat draft posts with deduplication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[403914291](https://clawhub.ai/user/403914291)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and WeChat public-account maintainers use this skill to prepare recurring AI-news posts, generate fixed-layout HTML content, and create WeChat draft articles for review or scheduled publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires WeChat public-account AppID/AppSecret credentials and caches access tokens or status files locally.

Mitigation: Use secure secret storage or environment variables, protect config and memory files with owner-only permissions, and rotate credentials if examples or local files are exposed.

Risk: The skill can create WeChat drafts automatically, including through scheduled operation.

Mitigation: Test with a non-production account first, keep automation disabled until configured, and review generated drafts before publication.

Risk: Some documentation paths recommend privileged installation commands or curl-based setup steps.

Mitigation: Avoid sudo or curl-to-shell style installation unless the source is independently trusted and verified; prefer least-privilege package installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/403914291/skills/wechat-publisher-easy)
- [Skill overview](artifact/skill.md)
- [Install guide](artifact/docs/install-guide.md)
- [User guide](artifact/docs/user_guide.md)
- [Publishing rules](artifact/docs/publish-rules.md)
- [Template guide](artifact/docs/templates.md)
- [Troubleshooting guide](artifact/docs/troubleshooting.md)
- [WeChat public platform](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, HTML article content, and runtime draft/status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates WeChat draft IDs and local status or result files when the publishing script runs.]

## Skill Version(s):

2.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
