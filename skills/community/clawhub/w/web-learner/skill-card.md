## Description:

自主上网学习技能 - 让 AI 能够主动搜索、浏览和从互联网获取知识。当用户要求了解最新信息、学习新知识、查询新闻、获取某个主题的详细信息，或需要从网络上获取数据时触发此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackeven02](https://clawhub.ai/user/jackeven02)

### License/Terms of Use:


## Use Case:

External users and agents use this skill as a Chinese-first web research helper for current information, news, weather, market data, URLs, documentation, and unfamiliar topics. It guides the agent to search, fetch, browse when needed, synthesize results, and cite sources in concise Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web research can send search terms, URLs, and task context to external sites or search providers.

Mitigation: Avoid submitting sensitive information in prompts or URLs, and review source selection before sharing results.

Risk: Broad trigger guidance may lead the agent to browse the web when a local answer would be sufficient.

Mitigation: Confirm that current or external information is needed before invoking web search, fetch, or browser tools.

Risk: Fetched web content may be incomplete, outdated, or misleading.

Mitigation: Compare important claims across sources and cite the sources used in the final answer.

## Reference(s):

- [Web Learner reference resources](artifact/references/resources.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured Chinese prose with source references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links, summarized findings, and fallback guidance when web access fails.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
