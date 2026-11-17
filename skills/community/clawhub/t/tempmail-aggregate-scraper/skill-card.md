## Description:

临时邮箱服务助手。支持生成临时邮箱、获取邮件列表和邮件详情。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and test teams use this skill to create disposable email addresses and retrieve mailbox messages for privacy-preserving registration flows or email-verification testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve mailbox contents, which may expose verification codes or other email data to the agent and MaxHub service.

Mitigation: Use the skill only with disposable mailboxes created for the current task, and fetch message contents only when disclosure is intended.

Risk: The security evidence flags unrelated Douyin/Xiaohongshu routing and inaccurate read-only claims in the artifact instructions.

Mitigation: Review, remove, or explain the unrelated routing before installation, and verify temp-mail API paths against the bundled references before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/new-ironman/skills/tempmail-aggregate-scraper)
- [MaxHub API Website](https://www.aconfig.cn)
- [Email Operations API](artifact/references/api-email.md)
- [Parameter Mapping Reference](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize API response data; API key values should not be revealed.]

## Skill Version(s):

3.6.1 (source: server evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
