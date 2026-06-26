## Description: <br>
Search X (Twitter) posts using the xAI API. Use when the user wants to find tweets, search X/Twitter, look up what people are saying on X, or find social media posts about a topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[testmsr](https://clawhub.ai/user/testmsr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query X/Twitter posts through the xAI Grok API, optionally filtering by handles, date range, and image or video understanding. It returns summarized search results with citations to original posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to xAI and may spend quota on the configured XAI_API_KEY. <br>
Mitigation: Avoid confidential queries, use a dedicated API key where appropriate, and monitor xAI usage. <br>
Risk: Publisher and bundled metadata are not perfectly aligned. <br>
Mitigation: Verify the publisher profile and release details before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/testmsr/x-skill-a) <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON object printed to stdout, with setup and usage guidance expressed as shell commands and configuration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY. Query options include allowed or excluded handles, date range, and image or video understanding; handle lists are limited to 10 entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
