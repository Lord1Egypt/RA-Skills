## Description:

微博热搜榜单查询工具。调用 Redfox 接口获取微博当前热搜榜单，按排名展示热搜标题及跳转链接，并对热搜内容进行创作灵感分析总结。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, creators, and PR teams use this skill to fetch current Weibo hot-search rankings, open related Weibo search links, and receive concise topic analysis for content planning and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Redfox API key and outbound requests to redfox.hk for Weibo trend data.

Mitigation: Confirm the key source, scope, expiration, and revocation path before installation, and avoid exposing the key in prompts, logs, or generated files.

Risk: The skill prompts users toward a recurring daily subscription without clear cancellation or lifecycle controls in the artifact.

Mitigation: Confirm the exact run time and the cancellation or modification process before enabling scheduled pushes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/weibo-hot-search-redfox)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [README.en.md](artifact/README.en.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown trend table with concise prose analysis; the helper script returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and network access to redfox.hk; may create a daily scheduled push after user confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
