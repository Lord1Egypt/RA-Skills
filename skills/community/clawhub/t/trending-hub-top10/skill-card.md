## Description:

基于每小时收录的抖音、微博、B站、快手、知乎、头条、百度等7大平台热点数据，聚合全网最热TOP10热点。支持回溯近7天热点。不支持具体热点的查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, content operations teams, brand PR teams, and data analysts use this skill to identify the top cross-platform hot topics, compare discussion patterns, and generate shareable trend reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Redfox API key and contacts Redfox for each query.

Mitigation: Use a scoped key where possible, keep it in environment configuration, avoid logging it, and revoke or rotate it if exposure is suspected.

Risk: Generated HTML reports may contain external topic links and should be reviewed before sharing or opening in sensitive browser contexts.

Mitigation: Review generated reports before distribution and open them in a browser context appropriate for untrusted external links.

Risk: Subscription and keyword-monitoring behavior is described but should be treated as unsupported without a real implementation and clear controls.

Mitigation: Do not rely on subscription or keyword-monitoring flows unless the publisher provides implemented consent, management, and cancellation behavior.

## Reference(s):

- [Instruction List](artifact/references/instruction-list.md)
- [Output Templates](artifact/references/output-templates.md)
- [Prediction Logic](artifact/references/prediction-logic.md)
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox Hot Keyword API](https://redfox.hk/story/api/hotKeyword/list)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls, files]

**Output Format:** [Markdown summaries, structured JSON, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and can query up to 7 days of hourly hotspot data.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
