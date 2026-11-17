## Description:

This skill helps Chinese social-media creators track topics, customize writing profiles, draft and review posts, and optionally prepare Tencent Docs backups and WeChat draft publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suzanneyp](https://clawhub.ai/user/suzanneyp)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and social-media operators use this skill to plan Chinese-platform posts, learn or apply custom writing profiles, run quality and fact checks, and prepare content for Tencent Docs or WeChat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing or backup workflows can send content to Tencent Docs or WeChat.

Mitigation: Require explicit approval before remote writes, verify the target account, and review the exact article and cover image before publishing or backing up content.

Risk: The skill documents an optional unpinned third-party MCP install.

Mitigation: Review and pin the repository and dependencies before installing that MCP component, or skip the optional reader workflow.

Risk: WeChat AppSecret and MCP tokens are needed for optional publishing integrations.

Mitigation: Store credentials in a secure configuration or secrets manager and avoid hard-coded paths, committed tokens, or relying on claimed existing configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suzanneyp/skills/weixin-content-creator)
- [Publisher profile](https://clawhub.ai/user/suzanneyp)
- [Tencent Docs MCP setup](https://docs.qq.com/desktop/wikispace?tab=1)
- [WeChat access token API](https://api.weixin.qq.com/cgi-bin/token)
- [WeChat material upload API](https://api.weixin.qq.com/cgi-bin/material/add_material)
- [WeChat draft creation API](https://api.weixin.qq.com/cgi-bin/draft/add)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text with optional JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include article drafts, review reports, fact-check summaries, publishing status, cover-image guidance, and optional API or MCP configuration snippets.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
