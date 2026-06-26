## Description: <br>
Searches the web using the iFlytek ONE SEARCH API and returns titles, summaries, URLs, and full page text, with emphasis on Chinese-language web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokkmiao](https://clawhub.ai/user/kokkmiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Chinese-language web searches through iFlytek ONE SEARCH, including queries that need result titles, summaries, URLs, and optional full text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published artifact references scripts/search.py, but that helper script is not included. <br>
Mitigation: Confirm the intended search script is supplied by the publisher or another trusted source before installing or running the skill. <br>
Risk: Search queries and the iFlytek API password are sent to the iFlytek search service. <br>
Mitigation: Use only an API password intended for this service and avoid confidential queries unless that data sharing is acceptable. <br>


## Reference(s): <br>
- [iFlytek Console](https://console.xfyun.cn/services/cbm) <br>
- [iFlytek ONE SEARCH API Endpoint](https://search-api-open.cn-huabei-1.xf-yun.com/v2/search) <br>
- [ClawHub Skill Page](https://clawhub.ai/kokkmiao/test-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown search results by default, or raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result count is configurable from 1 to 20; full text and reranking can be disabled.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
