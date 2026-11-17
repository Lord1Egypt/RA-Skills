## Description:

水务设备知识库 AI 助手，提供设备查询、选型建议、参数对比等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhulihuaaaaa](https://clawhub.ai/user/zhulihuaaaaa)

### License/Terms of Use:

MIT-0

## Use Case:

水务设备销售、运维和工程人员 use this skill to answer knowledge-base questions, compare liquid-level meters, water gauges, flow meters, and water-quality sensors, draft purchasing inquiries, and retrieve related documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive interaction details, prompts, quote information, tool data, and retrieval snippets may be written to local audit logs.

Mitigation: Restrict log directory access to trusted users, review retention settings before deployment, and avoid entering confidential purchasing or contact details unless the log handling policy is approved.

Risk: The skill uses third-party credential and query flows for embeddings and Tavily updates.

Mitigation: Use provider-specific credentials, verify the embedding endpoint configuration before using a real OpenAI key, and review outbound query content before enabling live updates.

Risk: Recurring knowledge-base updates can run in the background and write new retrieved content into the local knowledge base.

Mitigation: Enable cron only when recurring updates are intended, constrain configured source and destination paths, and review generated Markdown updates before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhulihuaaaaa/skills/water-knowledge-assistant)
- [Application cases](artifact/references/application-cases.md)
- [Parameter glossary](artifact/references/parameter-glossary.md)
- [Selection guide](artifact/references/selection-guide.md)
- [DashScope OpenAI-compatible endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional shell commands and generated inquiry drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved snippets, comparison tables, document paths, and generated Markdown knowledge-base updates.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
