## Description:

小红书每日爆款笔记推荐 helps agents query Xiaohongshu daily breakout notes by keyword or category, analyze title and content patterns, and produce ranked trend reports for content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand operators, MCN teams, and growth analysts use this skill to monitor Xiaohongshu daily breakout notes, identify fast-rising topics, and turn ranking data into reusable content ideas or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent credential handling and shell profile reads can expose or retain the RedFox API key longer than intended.

Mitigation: Use a scoped, revocable RedFox API key through a session-scoped secret mechanism, and avoid writing or echoing the key in shell profiles.

Risk: Daily subscription pushes may create ongoing activity beyond a one-time query.

Mitigation: Enable subscription pushes only after confirming where subscription state is stored and how cancellation works.

Risk: Generated HTML reports and /tmp cache files may contain untrusted or user-influenced data.

Mitigation: Treat generated reports and cache files as untrusted artifacts, especially on shared systems or where other users or processes can modify cache files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/if530770/skills/xhs-daily-breaking)
- [Core workflow](references/core_workflow.md)
- [RedFox API endpoint](https://redfox.hk/story/api/cozeSkill/getXhsCozeSkillDataOne)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [markdown, text, html, shell commands, guidance]

**Output Format:** [Markdown ranking tables and analysis text, with optional standalone HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may read or write local cache/report files during execution.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
