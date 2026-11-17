## Description:

Search the web using iFlytek ONE SEARCH API (万搜/聚合搜索). Returns titles, summaries, URLs, and full text from web pages. Good for Chinese-language web search.22222

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokkmiao](https://clawhub.ai/user/kokkmiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need Chinese-language web search results through iFlytek ONE SEARCH, including titles, summaries, URLs, and optional full page text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may contain secrets, private personal data, or confidential business material.

Mitigation: Use only intended non-sensitive search terms and avoid sending secrets or confidential material to the search provider.

Risk: The skill requires an XFYUN_API_PASSWORD for the external iFlytek ONE SEARCH service.

Mitigation: Provide the API password through the documented environment variable and avoid hard-coding credentials in skill files or prompts.

Risk: The packaged artifact references scripts/search.py, but that implementation is not included.

Mitigation: Verify or add the missing scripts/search.py implementation before expecting the skill to run.

## Reference(s):

- [test-search on ClawHub](https://clawhub.ai/kokkmiao/skills/test-search)
- [iFlytek Console](https://console.xfyun.cn/services/cbm)
- [iFlytek ONE SEARCH API endpoint](https://search-api-open.cn-huabei-1.xf-yun.com/v2/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output lists search result titles, URLs, and summaries; raw mode returns the full API JSON response including retrieved document content.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
