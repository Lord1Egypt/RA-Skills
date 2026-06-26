## Description: <br>
Search X (Twitter) posts using the xAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search X/Twitter posts, filter results by handles or date ranges, and return cited social-media findings for user queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries, filters, and related prompt text to xAI. <br>
Mitigation: Use it only for queries where third-party sharing with xAI is acceptable, and avoid secrets, regulated data, or proprietary topics. <br>
Risk: The skill requires an xAI API key. <br>
Mitigation: Provide the key through XAI_API_KEY or the agent's configured secret storage, and avoid embedding credentials in prompts, command history, or skill files. <br>


## Reference(s): <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>
- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/x-search-bwm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON response from the helper script, with text results and citation URLs suitable for agent summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY; supports handle filters, excluded handles, date ranges, image understanding, and video understanding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
