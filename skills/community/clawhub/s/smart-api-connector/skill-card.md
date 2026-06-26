## Description: <br>
Connects agents to REST APIs with web_fetch, authentication headers, JSON payload handling, error parsing, and retry guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API users use this skill to query REST endpoints, test API health, send authenticated requests, parse responses, and troubleshoot common HTTP errors from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to make external API requests with user-provided parameters. <br>
Mitigation: Review the URL, HTTP method, request body, and redacted headers before execution, especially for write operations. <br>
Risk: API credentials may be exposed if handled carelessly during request setup. <br>
Mitigation: Use scoped test keys when possible, keep keys session-only, prefer environment variables, and avoid persisting credentials to files. <br>
Risk: The curl fallback can execute network commands outside the built-in web_fetch path. <br>
Mitigation: Allow curl only when the exact command is visible, expected, and necessary for the user's request. <br>


## Reference(s): <br>
- [Smart API Connector on ClawHub](https://clawhub.ai/tommot2/smart-api-connector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with parsed API response summaries and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted request summaries, parsed JSON fields, HTTP status explanations, and retry guidance.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and skill heading) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
