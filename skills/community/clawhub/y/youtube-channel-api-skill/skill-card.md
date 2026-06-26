## Description: <br>
This skill helps agents use BrowserAct's YouTube Channel API template to extract structured YouTube channel search results from keywords and optional upload-date filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to discover YouTube channels, collect creator metadata, compare competitors, and build channel datasets for market research or outreach workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BrowserAct API keys can be exposed if pasted into chat or logs. <br>
Mitigation: Set BROWSERACT_API_KEY as an environment variable and avoid sharing the key in conversation. <br>
Risk: Search terms and workflow inputs are sent to BrowserAct. <br>
Mitigation: Avoid confidential or sensitive search terms unless sharing them with BrowserAct is acceptable. <br>
Risk: Long-running polling can consume quota or appear stuck. <br>
Mitigation: Monitor status logs, retry at most once after failure, and stop the process manually if polling appears stuck. <br>


## Reference(s): <br>
- [BrowserAct Console integrations](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Terminal output containing status logs and structured channel result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY and accepts keywords plus an optional upload-date filter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
