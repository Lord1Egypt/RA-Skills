## Description:

使用 UAPI 的“每日新闻图”单接口 skill，处理 每日新闻图、新闻海报、每日内容 等请求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to identify and call UAPI's GET /daily/news-image endpoint when a user asks for a daily news image, news poster, or daily digest image. It helps confirm that the response is JPEG binary data and that callers should handle timeouts and service errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad phrases such as daily digest may activate the skill and lead the agent to make an external request to UAPI.

Mitigation: Use explicit invocation or narrower triggers when users require strict control over external calls.

Risk: The endpoint returns JPEG binary data and may take several seconds while fetching and rendering current news.

Mitigation: Handle the response as image/jpeg and use a client timeout of at least 10 seconds.

Risk: The external service can return server or upstream errors.

Mitigation: Surface 500 and 502 failures clearly and advise retrying later when the upstream news or rendering service is unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shuakami/skills/uapi-get-daily-news-image)
- [UAPI API Base](https://uapis.cn/api/v1)
- [UAPI](https://uapis.cn)
- [每日新闻图](references/operations/get-daily-news-image.md)
- [快速上手](references/quick-start.md)
- [Daily 分类接口](references/resources/Daily.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint details and optional code or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The endpoint returns image/jpeg binary data rather than JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
