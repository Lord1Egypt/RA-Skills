## Description:

Connect to REST APIs with the agent's built-in web_fetch, including authentication headers, JSON payloads, error parsing, retries, and response summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query, test, and automate REST API calls from an agent while receiving parsed responses and error guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound API calls to user-provided hosts and may send user-provided credentials to those endpoints.

Mitigation: Verify the exact hostname before authenticated requests, use scoped or test credentials, and avoid production secrets.

Risk: The skill includes an exec/curl fallback that can run shell commands when web_fetch is insufficient.

Mitigation: Use web_fetch first and allow the exec/curl fallback only when explicitly needed and after reviewing the command.

Risk: Credential handling depends on session-only use and user discipline.

Mitigation: Keep API keys out of files, prefer environment variables when shell fallback is required, and avoid exposing key values when showing requests.

## Reference(s):

- [Smart API Connector on ClawHub](https://clawhub.ai/tommot2/skills/smart-api-connector)
- [tommot2 Publisher Profile](https://clawhub.ai/user/tommot2)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with API request examples, shell command fallbacks, and parsed response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include web_fetch requests, curl fallback commands, retry guidance, and parsed API response excerpts.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
