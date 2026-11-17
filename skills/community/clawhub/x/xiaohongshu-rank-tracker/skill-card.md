## Description:

小红书账号榜单追踪分析工具，支持查询日榜周榜月榜TOP50排名和热门账号

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Brand and MCN operators, Xiaohongshu creators, and content researchers use this skill to query daily, weekly, or monthly Xiaohongshu TOP 50 account rankings by category, generate shareable HTML reports, and optionally set recurring ranking updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and calls an external ranking API.

Mitigation: Verify the API key source, scope, validity period, and revocation path, and keep the key out of prompts, logs, code, and generated outputs.

Risk: Generated HTML reports are active web pages and may contain external account links.

Mitigation: Open only reports generated from trusted data and review profile links before following or sharing them.

Risk: Optional subscriptions can create recurring ranking pushes.

Mitigation: Confirm the requested schedule and cancellation path before enabling a recurring subscription.

Risk: The release security verdict is suspicious because report generation and subscription behavior require review.

Mitigation: Review the skill before installing or enabling automation, following the release security guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/xiaohongshu-rank-tracker)
- [Xiaohongshu Ranking API Documentation](references/api_docs.md)
- [Xiaohongshu Account Scoring Rules](references/score_rules.md)
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown ranking tables with optional downloadable HTML report files and JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; HTML reports may include Xiaohongshu profile links and client-side export controls.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
