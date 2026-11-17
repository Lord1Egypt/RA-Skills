## Description:

A Xiaohongshu writing assistant that analyzes popular posts to generate publish-ready copy and may initiate an Alipay recharge when API credits are insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External Xiaohongshu creators, content operators, and brand teams use this skill to analyze popular posts and produce platform-style titles, post copy, hashtags, and source notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Insufficient API credits can trigger an Alipay recharge workflow and potential charges.

Mitigation: Require separate approval to install payment software and for each recharge; verify the payee and amount before paying.

Risk: Search terms are sent to external services.

Mitigation: Avoid searching with confidential or sensitive topics.

Risk: The security review flags unsafe HTML content and filename handling in generated files.

Mitigation: Prefer a corrected version that uses JSON-only output, confines files to one folder, prevents accidental overwrites, and safely displays external text.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/redfox-data/skills/xhs-copywriter-redfox)
- [小红书热门笔记数据格式说明](references/xhs_hot_article_format.md)
- [支付宝充值接管流程](references/alipay-recharge.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown with recommended titles, post copy, hashtags, and source notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically includes 3–6 title options, a complete post body, 5–10 hashtags, and 2–3 reference posts.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
