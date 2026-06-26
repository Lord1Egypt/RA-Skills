## Description: <br>
Search X (Twitter) posts using the xAI API when a user wants to find tweets, look up what people are saying on X, or find social media posts about a topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[github2cao](https://clawhub.ai/user/github2cao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search X/Twitter through xAI, optionally filtering by handles, exclusions, date ranges, and media-understanding flags. It returns summarized X search results with citations to original posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search text, handle filters, date filters, and media-analysis options are sent to xAI under the user's XAI_API_KEY. <br>
Mitigation: Do not use the skill for secrets, confidential project names, sensitive personal data, or searches that should not be processed by a third-party API provider. <br>
Risk: The skill depends on a user-provided XAI_API_KEY and network access to xAI services. <br>
Mitigation: Configure the API key only in the intended environment and review generated search output and citations before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/github2cao/ssdfsdfsdfsaaaaaaa) <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI console](https://console.x.ai) <br>
- [xAI Responses API endpoint](https://api.x.ai/v1/responses) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search output and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY; supports handle filters, excluded handles, date ranges, and image or video understanding flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
