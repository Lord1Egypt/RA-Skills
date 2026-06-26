## Description: <br>
Rendshot helps agents render HTML/CSS to images, capture URL screenshots, fill templates, and generate visual content programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoohero500](https://clawhub.ai/user/zoohero500) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-producing agents use this skill to create social images, thumbnails, Open Graph images, rendered HTML cards, and website screenshots through Rendshot tools, API, CLI, or SDKs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Render inputs, prompts, template variables, screenshot target URLs, and the Rendshot API key may be sent to Rendshot or a configured endpoint. <br>
Mitigation: Use the skill only with approved endpoints and avoid sending sensitive HTML, secrets, authenticated pages, or regulated data unless authorized controls are in place. <br>
Risk: Screenshot requests can expose internal, localhost, cloud metadata, or authenticated URLs if a user supplies them. <br>
Mitigation: Do not target localhost, internal services, cloud metadata endpoints, or authenticated pages unless explicitly authorized and reviewed. <br>


## Reference(s): <br>
- [Rendshot MCP Tools Reference](references/mcp-tools.md) <br>
- [Rendshot API & CLI Reference](references/api-endpoints.md) <br>
- [Rendshot API](https://api.rendshot.com) <br>
- [ClawHub Rendshot Release Page](https://clawhub.ai/zoohero500/rendshot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, shell, TypeScript, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to call Rendshot MCP tools or use the Rendshot API, CLI, and SDKs; generated images and screenshots are produced by Rendshot or the configured endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
