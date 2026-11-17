## Description:

Zhipu Search helps agents query Zhipu AI web search with selectable engines, result counts, recency and domain filters, and content detail controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyhit2005](https://clawhub.ai/user/whyhit2005)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent run web searches through Zhipu/BigModel when it needs current information, a supported search engine, time or domain filtering, or controlled result detail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Zhipu/BigModel and may expose sensitive input.

Mitigation: Do not include secrets, private internal text, or personal data in search queries.

Risk: The optional user_id parameter can identify an end user.

Mitigation: Omit user_id or use a pseudonymous value unless a specific workflow requires it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/whyhit2005/skills/whyhit2005-zhipu-search)
- [Zhipu/BigModel API base URL](https://open.bigmodel.cn/api/paas/v4)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text search summaries or JSON search result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; optional parameters control engine, intent recognition, result count, domain filter, recency filter, content size, request ID, and user ID.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
