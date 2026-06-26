## Description: <br>
Search the web using iFlytek ONE SEARCH API (万搜/聚合搜索). Returns titles, summaries, URLs, and full text from web pages. Good for Chinese-language web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the Chinese web through iFlytek ONE SEARCH and return titles, summaries, URLs, and optionally full page text. It is useful when Chinese-language results or an alternative search provider are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to iFlytek ONE SEARCH. <br>
Mitigation: Avoid confidential, personal, or regulated search terms unless that use is approved for the environment. <br>
Risk: Full-text retrieval may return more page content than needed. <br>
Mitigation: Use --no-fulltext when titles, URLs, and summaries are sufficient. <br>
Risk: The skill requires an iFlytek API password. <br>
Mitigation: Provide XFYUN_API_PASSWORD through the environment and do not hard-code or share the credential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/xfyun-search) <br>
- [iFlytek ONE SEARCH console](https://console.xfyun.cn/services/cbm) <br>
- [iFlytek ONE SEARCH API endpoint](https://search-api-open.cn-huabei-1.xf-yun.com/v2/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-style search result text by default, or raw JSON when --raw is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XFYUN_API_PASSWORD. Supports result limit, rerank control, full-text control, and raw JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
