## Description:

Guides agents in configuring and using Google Stitch's remote MCP API to manage Stitch projects and screens, generate UI screens from prompts, edit screens, and create design variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arielletolome](https://clawhub.ai/user/arielletolome)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design teams use this skill to let an agent configure Google Stitch MCP access, list or create Stitch projects, retrieve screens, and generate, edit, or vary UI screen designs through Stitch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill need a Google Stitch API key and may expose it if prompts, configuration, or logs are handled carelessly.

Mitigation: Keep the API key private, pass it through protected MCP client configuration or environment variables, and rotate or remove it when access is no longer needed.

Risk: Prompts and project data sent through the remote MCP API are processed by Google Stitch and may include sensitive design or business information.

Mitigation: Avoid sending sensitive prompts or project data unless sharing that information with Google Stitch is appropriate for the user's environment.

Risk: Generation and edit calls can create or change remote Stitch project content and may continue after a transient connection failure.

Mitigation: Check screen status with retrieval calls before retrying generation or edit operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arielletolome/skills/stitch)
- [Publisher Profile](https://clawhub.ai/user/arielletolome)
- [Stitch MCP Setup and Authentication](https://stitch.withgoogle.com/docs/mcp/setup/)
- [Stitch MCP Reference](https://stitch.withgoogle.com/docs/mcp/reference/)
- [Stitch MCP Guide](https://stitch.withgoogle.com/docs/mcp/guide/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, Code]

**Output Format:** [Markdown with inline bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides remote MCP endpoint configuration and request examples; generated Stitch screen artifacts are retrieved from Google Stitch download URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
