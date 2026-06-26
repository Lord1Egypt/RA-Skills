## Description: <br>
Trend Scope generates public-opinion trend reports from Feedax data, including sentiment, geography, keyword, media, and time-series analyses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longgggggg](https://clawhub.ai/user/longgggggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to turn Chinese public-opinion search requirements into Feedax report queries, summaries, and saved reports for brand monitoring, market analysis, competitor tracking, incident analysis, and trend review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Report queries, filters, aggregation parameters, and an API key are sent to the Feedax report service, and the security summary flags use of an unencrypted raw-IP service endpoint. <br>
Mitigation: Install only if the Feedax service is trusted, use a dedicated low-privilege API key, and avoid personal, confidential, or sensitive search terms. <br>
Risk: Generated reports can include article-level details and saved files that may expose sensitive search context if shared broadly. <br>
Mitigation: Review saved reports before sharing and use JSON-only output or disable hot articles when article-level details are not needed. <br>


## Reference(s): <br>
- [Trend Scope on ClawHub](https://clawhub.ai/longgggggg/trend-scope) <br>
- [Publisher profile](https://clawhub.ai/user/longgggggg) <br>
- [Feedax](https://www.feedax.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance] <br>
**Output Format:** [Conversation summary plus saved JSON, Markdown, and HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and FEEDAX_REPORT_API_KEY; reports default to the user's Desktop public-opinion report directory unless another output directory is supplied.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
