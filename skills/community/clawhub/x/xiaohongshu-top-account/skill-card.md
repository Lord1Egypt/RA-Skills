## Description:

小红书账号榜单追踪分析工具，支持查询日榜周榜月榜TOP50排名和热门账号

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

Brand and MCN operators, Xiaohongshu creators, and content researchers use this skill to query daily, weekly, or monthly Xiaohongshu account rankings by category, review top accounts, export HTML reports, and set scheduled ranking updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and sends ranking requests to a third-party service.

Mitigation: Install only if you trust RedFox with the key, configure the key through environment variables, and confirm the key can be reset or revoked.

Risk: Generated HTML reports may run active web content and contact a third-party CDN when opened.

Mitigation: Review generated reports before sharing or opening them in sensitive environments, and avoid using reports built from untrusted JSON or API data.

Risk: Scheduled ranking pushes may create recurring local or platform notifications.

Mitigation: Confirm the requested cadence and category before enabling a subscription, and disable scheduled tasks that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/xiaohongshu-top-account)
- [Xiaohongshu ranking API documentation](references/api_docs.md)
- [Xiaohongshu account scoring rules](references/score_rules.md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, HTML files, configuration, guidance]

**Output Format:** [Markdown ranking tables with optional generated HTML report files and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; generated HTML reports may load third-party web resources when opened.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
