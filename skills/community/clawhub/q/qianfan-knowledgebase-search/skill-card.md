## Description:

Searches and retrieves information from private Baidu Qianfan knowledge bases using semantic, full-text, hybrid, and reranked search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hannatao](https://clawhub.ai/user/hannatao)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to query private Baidu Qianfan knowledge bases and retrieve structured result chunks, scores, and document metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private search queries and knowledge-base identifiers are sent to Baidu Qianfan.

Mitigation: Use the skill only when Baidu Qianfan is approved for the data being searched, and avoid submitting confidential queries outside approved workflows.

Risk: The script logs the full parsed request body to standard output.

Mitigation: Remove or redact the diagnostic request print before using the skill with sensitive searches.

Risk: The skill requires a Baidu Qianfan API key.

Mitigation: Provide the key through environment management, avoid storing it in prompts or files, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hannatao/skills/qianfan-knowledgebase-search)
- [Baidu Qianfan Knowledgebase Search API endpoint](https://qianfan.baidubce.com/v2/knowledgebases/search)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON search results and status or error text on standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and knowledge-base identifiers; accepts query, top_k, score threshold, recall, rerank, graph, and expansion options.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
