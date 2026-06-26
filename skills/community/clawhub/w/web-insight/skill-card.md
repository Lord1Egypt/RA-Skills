## Description: <br>
Web Insight helps agents run filtered public web and social-media monitoring searches, parse time and area filters, and return concise summaries with structured JSON exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longgggggg](https://clawhub.ai/user/longgggggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and analysts use this skill to monitor public online content for brand management, market analysis, competitor tracking, and risk awareness. It supports keyword, sentiment, time, platform, geography, domain, and engagement filters for public-content investigation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured search endpoint sends API keys and search terms over plain HTTP. <br>
Mitigation: Use the skill only with non-sensitive searches until the endpoint is changed to HTTPS or routed through an approved secure service. <br>
Risk: Full search results are saved locally by default. <br>
Mitigation: Set an explicit output directory, review local retention needs, and remove saved result files that contain sensitive investigation context. <br>
Risk: API-key checks can expose the configured key when users inspect the .env file directly. <br>
Mitigation: Avoid displaying or sharing .env contents; validate the presence of FEEDAX_SEARCH_API_KEY without printing the secret value. <br>


## Reference(s): <br>
- [Feedax API key and service](https://www.feedax.cn) <br>
- [Domain taxonomy](references/domains.json) <br>
- [Scene taxonomy](references/scenes.json) <br>
- [Media platform list](references/media_names.json) <br>
- [Area code data](assets/area_codes.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [Markdown or plain-text search summaries plus saved JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full normalized search results are saved to a configurable output directory; the default is ~/Desktop/舆情搜索结果/.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
