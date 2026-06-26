## Description: <br>
Search X (Twitter) posts using the xAI API for tweets, social media posts, and public conversation around a topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taotao666720](https://clawhub.ai/user/taotao666720) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run focused X/Twitter searches through xAI, including keyword searches, handle filters, date ranges, and optional image or video understanding. It is useful when a user asks what people are saying on X or needs cited links to relevant posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, filters, and related request metadata are sent to xAI using the user's API key. <br>
Mitigation: Avoid submitting secrets, sensitive personal data, or regulated information in queries or filters. <br>
Risk: The skill depends on XAI_API_KEY for authenticated API access. <br>
Mitigation: Store the API key securely, scope access according to local policy, and avoid exposing it in prompts, logs, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub listing for X Search (Local)](https://clawhub.ai/taotao666720/x-search-local) <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON printed to stdout, with status, query, text, citations, search count, and token usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and XAI_API_KEY; supports handle filters, exclusions, date ranges, and image/video understanding flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
