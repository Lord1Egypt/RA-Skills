## Description: <br>
Search X (Twitter) posts using the xAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinbrother](https://clawhub.ai/user/kevinbrother) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search X/Twitter posts through the xAI API, with optional handle filters, date ranges, and image or video understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an xAI API key and sends X/Twitter search terms to xAI. <br>
Mitigation: Install only when this data sharing is acceptable, keep the API key in the documented environment/configuration mechanism, and avoid secrets, private business details, or sensitive personal information in queries. <br>


## Reference(s): <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>
- [ClawHub skill page](https://clawhub.ai/kevinbrother/slugname2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [JSON response containing search status, query text, citations, search count, and token usage; skill guidance is Markdown with shell examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY; can filter included or excluded handles, date range, and image or video understanding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
