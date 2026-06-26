## Description: <br>
SEO DataForSEO helps agents run DataForSEO keyword research, SERP analysis, competitor analysis, YouTube SEO research, and trend tracking with local JSON and Markdown summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamkristopher](https://clawhub.ai/user/adamkristopher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
SEO practitioners, marketers, and developers use this skill to gather keyword metrics, SERP data, competitor intelligence, and trend signals through DataForSEO for content and landing-page planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DataForSEO API requests can consume account quota or incur charges. <br>
Mitigation: Confirm the DataForSEO account and request scope before running research, and monitor usage for large batches. <br>
Risk: The .env file and local results/ files may contain API credentials, client topics, competitor domains, or strategy-sensitive research. <br>
Mitigation: Keep credentials out of source control and delete or protect saved results before sharing the workspace. <br>
Risk: SEO queries and target domains are sent to DataForSEO. <br>
Mitigation: Avoid submitting confidential client data unless the user is authorized to send it to DataForSEO. <br>


## Reference(s): <br>
- [DataForSEO API reference](references/api-reference.md) <br>
- [DataForSEO API access](https://app.dataforseo.com/api-access) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, JSON result files, and Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DataForSEO credentials; API responses are saved under results/ by category.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
