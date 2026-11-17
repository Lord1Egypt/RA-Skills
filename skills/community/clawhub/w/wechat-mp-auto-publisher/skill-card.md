## Description:

自动撰写技术文章并发布到微信公众号，从选题到发布支持全流程自动化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizz0725](https://clawhub.ai/user/lizz0725)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and operators use this skill to create Chinese technical articles, generate supporting image prompts, gather background material, and publish drafts to a WeChat Official Account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled topics, search terms, or filenames may reach shell execution paths.

Mitigation: Review inputs before execution and replace shell-string execSync usage with argument-array process execution before using the skill on untrusted content.

Risk: Documentation and troubleshooting steps may expose WeChat or image-generation secrets if copied into logs or chat.

Mitigation: Use presence-only credential checks, avoid printing .env files or secrets, and keep API keys and WeChat credentials in protected configuration.

Risk: The workflow can publish generated content to a real WeChat account.

Mitigation: Use a test account first and require explicit final confirmation before publishing to a production WeChat Official Account.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/lizz0725/skills/wechat-mp-auto-publisher)
- [Alibaba Cloud Bailian API key setup](https://bailian.console.aliyun.com/?tab=globalset#/efm/api_key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles and prompts with inline shell commands and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local framework, article, and image files before publishing a WeChat draft.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
