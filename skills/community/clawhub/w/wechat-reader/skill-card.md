## Description:

Read WeChat public account articles from mp.weixin.qq.com links by using browser automation to extract full article text when requested by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to read, summarize, translate, or present content from user-provided WeChat public account articles that require browser rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation opens user-provided WeChat article links and may encounter login walls, removed content, or access restrictions.

Mitigation: Use the skill only for user-requested article links, report blocked or removed content to the user, and review login walls manually without signing in or bypassing access controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imwyvern/skills/wechat-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or text summary with extracted article content and status notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image alt text, captions, or access-status messages when article content is removed or login-gated.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
