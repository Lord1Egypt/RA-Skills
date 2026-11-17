## Description:

通过浏览器操作网页版微博，用户登录后 Agent 撰写内容并自动发布。无需 API，需 Browser Relay 挂上微博标签页。Keywords: 微博, 发微博, 自动发布, Weibo, ZeeLin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft and publish posts through an already logged-in Weibo web session. It is intended for workflows where the user wants browser-based Weibo posting without using a Weibo API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish through the user's logged-in Weibo account.

Mitigation: Use it only when the user explicitly intends to publish, and require final user confirmation before running the posting command.

Risk: Unsafe command handling could allow untrusted post text to affect command invocation.

Mitigation: Do not pass untrusted text as the post body until safe argument passing is implemented.

Risk: Browser snapshots may be written to a predictable temporary file.

Mitigation: Use private temporary files for snapshots and remove them after troubleshooting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/zeelin-weibo-autopost)
- [Publisher profile](https://clawhub.ai/user/kelcey2023)
- [Weibo](https://weibo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local browser automation against a logged-in Weibo tab and report whether submission was attempted.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
