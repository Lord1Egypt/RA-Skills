## Description: <br>
REST API Tester helps developers test REST APIs with configurable headers, authentication, request bodies, response validation, webhook checks, and simple performance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeonardoDpanda](https://clawhub.ai/user/LeonardoDpanda) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to debug API endpoints, test authentication flows, validate webhook payloads, check response times, automate health checks, and test third-party integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API testing examples may send credentials, tokens, or sensitive payloads to an unintended endpoint. <br>
Mitigation: Use only authorized APIs, prefer test environments and least-privilege temporary tokens, sanitize payloads, and verify target URLs before sending requests. <br>
Risk: Webhook testing with a public tunnel can expose local services or received data while the tunnel is running. <br>
Mitigation: Treat ngrok or similar tunnels as public, use them only for limited testing windows, and avoid sending production secrets through exposed listeners. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LeonardoDpanda/rest-api-tester) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples for GET, POST, authentication, webhook listening, performance testing, and response validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
