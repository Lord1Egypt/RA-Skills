## Description:

获取微博热搜榜单并按热度排序，无需 API Key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzihao0731](https://clawhub.ai/user/chenzihao0731)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch current Weibo hot topics for monitoring Chinese social-media trends or integrating trending-topic lists into agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to v2.xxapi.cn when fetching Weibo hot topics.

Mitigation: Install and run it only in environments where this external API call is acceptable.

Risk: The upstream API may be unavailable, slow, or rate limited.

Mitigation: Cache results when polling frequently and handle command failures in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenzihao0731/skills/weibo-hot)
- [API service homepage](https://v2.xxapi.cn)
- [Weibo hot topics API](https://v2.xxapi.cn/api/weibohot)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text lines in hot|title format, with optional Markdown guidance from the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; calls v2.xxapi.cn and may be subject to API availability and rate limits.]

## Skill Version(s):

1.0.0 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
