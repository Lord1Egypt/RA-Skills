## Description:

Helps agents fetch real-time hot searches and trending topics from Weibo, Zhihu, Baidu, Douyin, Toutiao, and Bilibili.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lk360287680-byte](https://clawhub.ai/user/lk360287680-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve and summarize current trending topics from major Chinese social media and content platforms. It supports platform-specific lookups, cross-platform comparisons, keyword alerts, and content recommendation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous requests such as "what is trending" may cause an agent to prefer Chinese social-media and content-platform results.

Mitigation: Ask the user to specify the region or source when the request is ambiguous, and label returned results by platform.

Risk: Public trend API responses can be unavailable, cached, stale, or missing expected fields.

Mitigation: Handle request failures and invalid responses, use short-lived caching, and surface update timestamps when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lk360287680-byte/skills/web-hot)
- [Publisher profile](https://clawhub.ai/user/lk360287680-byte)
- [60s API base endpoint](https://60s.viki.moe/v2)
- [60s API documentation](https://docs.60s-api.viki.moe)
- [60s API GitHub repository](https://github.com/vikiboss/60s)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and Bash examples, plus JSON API response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public GET endpoints; no credentials, bundled code, persistence, or local data access are required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
