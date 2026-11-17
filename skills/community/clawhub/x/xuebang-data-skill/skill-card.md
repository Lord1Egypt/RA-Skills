## Description:

登录学邦后台并读取首页今日经营数据与待办数据，整理为简洁汇总。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuansir123](https://clawhub.ai/user/chuansir123)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized Xuebang or EDU.BOSS users use this skill to sign in with their own credentials and retrieve same-day business metrics and pending-task counts from the dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to saving EDU.BOSS credentials in a local workspace note file.

Mitigation: Revise the skill to keep credentials session-only by default, or use a dedicated secret store with explicit opt-in consent, deletion guidance, and clear protection details.

Risk: Broad triggers could invoke the skill for requests that are not clearly Xuebang or EDU.BOSS related.

Mitigation: Narrow activation triggers to Xuebang and EDU.BOSS-specific requests before installation.

Risk: Declared tool permissions may not fully align with file access implied by credential storage.

Mitigation: Align declared permissions with any required file access, or remove local credential-file storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chuansir123/skills/xuebang-data-skill)
- [Xuebang EDU.BOSS login page](https://boss.xuebangsoft.net/eduboss/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses "未读取到" for missing fields and avoids reproducing full passwords.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
