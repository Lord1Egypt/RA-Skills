## Description: <br>
Search X (Twitter) posts using the xAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratikbhosale7](https://clawhub.ai/user/pratikbhosale7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search X/Twitter posts through the xAI API, with optional handle filters, date ranges, and image/video understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and filters are sent to xAI under the configured API key. <br>
Mitigation: Avoid confidential search terms and install only when sending those queries to xAI is acceptable. <br>
Risk: The XAI_API_KEY is required for use and could be exposed through local configuration or shell history. <br>
Mitigation: Keep the API key private, prefer environment or configured secret storage, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>
- [ClawHub skill page](https://clawhub.ai/pratikbhosale7/x-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results with text, citations, search count, token usage, and Markdown-ready presentation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY; supports handle include/exclude filters, date range filters, and image/video understanding flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
