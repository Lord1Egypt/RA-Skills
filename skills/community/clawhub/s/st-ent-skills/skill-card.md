## Description:

Search 699pic enterprise photo and video assets, check whether assets were already downloaded, inspect download records, and generate download links through the local 699pic OpenAPI integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[st699pic](https://clawhub.ai/user/st699pic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise asset users use this skill to search 699pic photo and video assets, verify enterprise download history, and request download links after confirming the target asset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send an enterprise API key to a configurable service endpoint.

Mitigation: Use only a narrowly scoped SERVICE_API_KEY, keep SERVICE_API_BASE_URL on a trusted HTTPS endpoint, and review the script before execution.

Risk: Broad image or video search requests may route user queries through the enterprise asset service.

Mitigation: Confirm the user's intent before invoking search tools for generic image or video requests.

Risk: A local MCP registration named st-mcp may have environment, command, or permission settings that differ by machine.

Mitigation: Inspect and authorize the local MCP registration before using it, including command, arguments, environment variables, and permissions.

## Reference(s):

- [699pic OpenAPI MCP reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/st699pic/skills/st-ent-skills)
- [ClawHub publisher profile](https://clawhub.ai/user/st699pic)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown image summaries with optional JSON and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results should embed available preview or thumbnail images and include asset identifiers, titles, extensions, and relevant asset flags.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
