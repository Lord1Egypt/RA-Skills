## Description: <br>
Web search via Yep Search API. Own index, fast results with domain filtering and date ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elrandar](https://clawhub.ai/user/elrandar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run web searches through the Yep Search API with options for domain filters, date ranges, safe search, language selection, and optional content highlights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Yep and may include sensitive information if entered directly. <br>
Mitigation: Avoid putting private secrets or sensitive personal data into search queries. <br>
Risk: API calls may spend Yep account credit. <br>
Mitigation: Use a dedicated, revocable Yep API key where possible and monitor account usage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/elrandar/yep-search) <br>
- [Yep platform](https://platform.yep.com) <br>
- [Yep API key setup](https://platform.yep.com/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown-formatted search result list with titles, URLs, descriptions, and optional API cost and balance details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YEP_API_KEY; search queries are sent to Yep and API calls may consume Yep account credit.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
