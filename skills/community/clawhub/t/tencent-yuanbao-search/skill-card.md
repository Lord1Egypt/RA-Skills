## Description:

Search the web using Tencent Yuanbao Search (WSA). Prioritize using it when you need to retrieve network information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI agents use this skill to search for current web information, news, and vertical-domain results, then read the returned page titles, summaries, dates, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Tencent and may consume service quota.

Mitigation: Keep queries free of secrets and unnecessary personal information, confirm before sensitive searches, and protect the API key stored locally.

## Reference(s):

- [Tencent Yuanbao Search product page](https://cloud.tencent.com/product/wsa)
- [Tencent Yuanbao Search product documentation](https://cloud.tencent.com/document/product/1806/121794)
- [API key setup guide](references/setup.md)
- [ClawHub release page](https://clawhub.ai/tencent-adm/skills/tencent-yuanbao-search)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown search results with linked titles, summaries, publication dates, source sites, relevance scores, and optional image links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result content and count vary with the query and selected search filters.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
