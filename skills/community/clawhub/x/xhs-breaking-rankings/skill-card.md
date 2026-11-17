## Description:

小红书低粉爆款笔记挖掘小红书平台上粉丝量低于 5000 且点赞数超过 500 的高互动笔记，并输出榜单与爆款规律分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External Xiaohongshu creators, content operators, MCN agencies, brand teams, and content strategists use this skill to find low-follower high-engagement notes, monitor category trends, discover rising creators, and export shareable reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles RedFox API credentials.

Mitigation: Use a revocable, low-scope REDFOX_API_KEY and prefer setting it directly in the current environment.

Risk: Shell-profile discovery can broaden where credentials are read from.

Mitigation: Avoid relying on shell-profile discovery when possible and review local profile files before use.

Risk: Generated HTML exports may execute browser code from remote or cached fields and CDN scripts.

Mitigation: Open generated HTML only from trusted runs and review exports before sharing or opening them in sensitive browser contexts.

Risk: Server security evidence marks the release as suspicious because credential handling and generated HTML need review before use.

Mitigation: Review and scan the skill before installation or deployment.

## Reference(s):

- [小红书低粉爆款笔记 API 接口规范](artifact/references/api-spec.md)
- [RedFoxHub](https://redfox.hk/)
- [ClawHub skill page](https://clawhub.ai/if530770/skills/xhs-breaking-rankings)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance]

**Output Format:** [Markdown report with ranking tables and analysis, JSON cache files, and optional HTML export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a REDFOX_API_KEY; results depend on RedFoxHub data availability, selected category, and selected date.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
