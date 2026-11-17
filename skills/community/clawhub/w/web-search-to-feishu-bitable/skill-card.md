## Description:

Automatically searches web keywords, extracts page information, and saves standardized results into a Feishu Bitable personal knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mildnes](https://clawhub.ai/user/mildnes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and knowledge workers use this skill to collect web search results for keyword lists, summarize the retrieved pages, and organize them into a Feishu Bitable knowledge base with consistent fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create Feishu Bitable apps or tables and batch-add records using the user's authorized Feishu account.

Mitigation: Confirm the destination Bitable, table, and fields before running it, especially when updating an existing knowledge base.

Risk: Fetched web content can be unavailable, duplicated, stale, or misleading after summarization.

Mitigation: Review imported records before relying on them for decisions or sharing the knowledge base.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mildnes/skills/web-search-to-feishu-bitable)
- [Publisher profile](https://clawhub.ai/user/mildnes)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration]

**Output Format:** [Structured Feishu Bitable records plus a Feishu link returned as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends records with title, URL, summary, tags, and category fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
