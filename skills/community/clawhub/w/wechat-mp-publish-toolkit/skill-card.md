## Description:

WeChat Official Account draft push and auto-publish toolkit for creating article drafts, publishing drafts, configuring credentials and IP allowlisting, and setting up daily publishing automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyi162751-collab](https://clawhub.ai/user/yyi162751-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to prepare WeChat Official Account article drafts, upload cover media, publish selected drafts, and configure scheduled publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish scheduled WeChat articles to all subscribers using account credentials.

Mitigation: Use it for draft creation by default and require an explicit approval step before any freepublish/submit action.

Risk: The agent must access a WeChat Official Account AppID and AppSecret.

Mitigation: Store the environment file with tight permissions, avoid shared hosts, and rotate credentials if logs or command history may have exposed them.

Risk: Publishing is irreversible once a draft is submitted.

Mitigation: Verify the draft media ID, title, summary, and cover in the WeChat editor before scheduled or manual publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yyi162751-collab/skills/wechat-mp-publish-toolkit)
- [Publisher Profile](https://clawhub.ai/user/yyi162751-collab)
- [WeChat MP API Guide](references/api-guide.md)
- [Daily Auto-Publish Automation Template](references/automation-template.md)
- [WeChat Official Account Platform](https://mp.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown guidance with inline shell commands, Python and Bash script usage, JSON examples, and automation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft media IDs, publish IDs, API error guidance, and setup instructions; publishing actions require WeChat credentials and account permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
