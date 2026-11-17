## Description:

Image generation and screenshot tool using Rendshot for HTML/CSS rendering, website screenshots, reusable templates, social graphics, Open Graph images, thumbnails, and other programmatic visual content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoohero500](https://clawhub.ai/user/zoohero500)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content teams use this skill to generate images from prompts, templates, or raw HTML/CSS and to capture webpage screenshots through Rendshot tools, API, CLI, or SDKs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive prompts, HTML, screenshots, internal URLs, account pages, secrets, or customer data may be sent to Rendshot or another configured rendering endpoint.

Mitigation: Use the skill only with content intended for that service, avoid submitting secrets or private data, and prefer private or self-hosted deployments for sensitive rendering workloads.

Risk: CLI or SDK installation may pull changing package versions over time.

Mitigation: Pin CLI and SDK package versions when using Rendshot in repeatable or production workflows.

## Reference(s):

- [Rendshot API & CLI Reference](references/api-endpoints.md)
- [Rendshot MCP Tools Reference](references/mcp-tools.md)
- [Rendshot API](https://api.rendshot.com)
- [ClawHub Rendshot Skill Page](https://clawhub.ai/zoohero500/skills/rendshot)

## Skill Output:

**Output Type(s):** [Files, API Calls, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON tool-call examples, bash commands, SDK code snippets, and generated image or screenshot outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG or JPG images, image URLs, rendered HTML, template variables, or saved reusable templates depending on the selected Rendshot workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
