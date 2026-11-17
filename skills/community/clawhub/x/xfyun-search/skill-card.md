## Description:

Search the web using iFlytek ONE SEARCH API (万搜/聚合搜索) to return titles, summaries, URLs, and full text from web pages, especially for Chinese-language web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run iFlytek ONE SEARCH queries, especially for Chinese-language web search, and receive result titles, summaries, URLs, and optional full page text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the XFYUN_API_PASSWORD credential are sent to iFlytek's search API.

Mitigation: Use the skill only when iFlytek search is intended, and prefer a dedicated API key with limited quota.

Risk: Full-text retrieval may return more page content than a short search summary.

Mitigation: Disable full-text retrieval with the documented option when only titles, URLs, and summaries are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/xfyun-search)
- [iFlytek ONE SEARCH service console](https://console.xfyun.cn/services/cbm)
- [iFlytek ONE SEARCH API endpoint](https://search-api-open.cn-huabei-1.xf-yun.com/v2/search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown-formatted search results by default, or raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search limit defaults to 10 results and can be set from 1 to 20; reranking and full-text retrieval can be disabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
