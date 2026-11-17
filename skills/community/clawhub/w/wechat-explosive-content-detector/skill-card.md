## Description:

Provides WeChat Official Account content creators with trend data on high-performing articles using low-follower/high-read, top-read, growth, and originality signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, editors, and MCN operators use this skill to query recent WeChat Official Account articles, compare trending examples, and choose more specific content lanes for follow-up research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The data-fetching script disables TLS certificate and hostname verification when calling the external trend API, which can allow network attackers to alter API responses or inject misleading links into generated reports.

Mitigation: Use only in network environments where that risk is acceptable, review generated links before sharing or acting on them, and restore normal TLS verification before broad deployment.

Risk: The skill sends search keywords and dates to an external trend API.

Mitigation: Avoid submitting confidential campaign plans, private client names, or other sensitive terms as query keywords.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/wechat-explosive-content-detector)
- [WeChat explosive content workflow](artifact/references/gzh_explosive_content_workflow.md)
- [WeChat trend data format](artifact/references/gzh_trend_data_format.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown summaries with generated HTML or JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries use a keyword and optional date window, then return up to 10 selected article recommendations plus follow-up lane suggestions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
