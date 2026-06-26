## Description: <br>
Provides a unified 同花顺问财 workflow for market data, index data, financial metrics, company information, events, operating data, ratings, reports, announcements, news, A-share screening, and sector screening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhofchina](https://clawhub.ai/user/hhofchina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query 同花顺问财 for Chinese market, company, research, announcement, news, stock-screening, and sector-screening information through a single agent-facing workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and the IWENCAI_API_KEY are sent to the configured 同花顺问财 API endpoint. <br>
Mitigation: Use the default official endpoint unless an alternative is fully trusted, protect the API key, and avoid submitting confidential investment plans, proprietary research, or unrelated secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hhofchina/wen-cai) <br>
- [同花顺问财 API endpoint](https://openapi.iwencai.com) <br>
- [同花顺问财 web query fallback](https://www.iwencai.com/unifiedwap/chat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown tables or lists, optional raw JSON, and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IWENCAI_API_KEY and may use IWENCAI_BASE_URL to select the API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
