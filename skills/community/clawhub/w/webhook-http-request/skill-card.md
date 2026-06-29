## Description: <br>
Webhook Http Request helps agents make HTTP and HTTPS requests with standard methods, optional authentication, custom payloads, and structured response handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill when an agent needs to call REST APIs, send webhooks, submit JSON or form data, fetch web resources, or poll external services through AgentPMT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables outbound HTTP requests that may send sensitive URLs, headers, request bodies, bearer tokens, API keys, or passwords. <br>
Mitigation: Use the skill only for trusted HTTPS services, keep inputs scoped to the task, and avoid placing secrets in prompts or logs. <br>
Risk: Private or loopback network access can increase exposure if enabled unnecessarily. <br>
Mitigation: Keep allow_private disabled unless a specific trusted integration requires it. <br>
Risk: A prompt that merely mentions a URL or request could trigger broader HTTP activity than intended. <br>
Mitigation: Confirm the intended endpoint, method, authentication mode, and payload before making consequential requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/webhook-http-request) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/webhook-http-request) <br>
- [Action Schema](schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, JSON, text] <br>
**Output Format:** [Markdown instructions with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines one request action with HTTP methods, authentication options, body formats, response modes, timeouts, and response size limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
