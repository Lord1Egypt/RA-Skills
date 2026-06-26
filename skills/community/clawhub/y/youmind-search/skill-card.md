## Description: <br>
Search the public Internet with YouMind Search. Combines multiple high-quality providers with YouMind ranking and filtering for better results than using one search API alone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p697](https://clawhub.ai/user/p697) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to search the public Internet through YouMind Search for fresh information, online research, recent news, source gathering, domain-filtered lookup, and scholar-style queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to YouMind with the user's YouMind API key. <br>
Mitigation: Avoid including secrets, private workspace content, or sensitive personal data in queries unless the user intends to share that information with the configured search endpoint. <br>


## Reference(s): <br>
- [YouMind homepage](https://youmind.com/) <br>
- [ClawHub skill page](https://clawhub.ai/p697/youmind-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YOUMIND_API_KEY. Search requests can use category, freshness, includeDomains, and excludeDomains parameters.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
