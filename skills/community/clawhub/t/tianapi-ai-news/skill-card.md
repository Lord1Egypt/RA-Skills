## Description:

聚合人工智能、大模型、算法等AI领域前沿新闻资讯，支持关键词检索和分页查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve TianAPI AI news by keyword and page, then present titles, sources, publication times, and links in agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a TianAPI API key, and server security evidence reports inconsistent environment variable names plus less-safe credential examples.

Mitigation: Store the key in a protected environment variable, avoid passing it on the command line, do not commit scripts/.env, and verify whether the runtime expects TIANAPI_AI_NEWS_KEY or TIANAPI_AI_KEY before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-ai-news)
- [TianAPI AI News API](https://www.tianapi.com/apiview/22)
- [TianAPI homepage](https://www.tianapi.com)
- [TianAPI AI API endpoint](https://apis.tianapi.com/ai/index)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON news results with titles, sources, publication times, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TianAPI API key and supports result count, keyword, and page parameters.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
