## Description:

Smart Search MCP is a technical search toolkit that helps agents generate and use searches across general web, GitHub, Stack Overflow, package, API, cloud, and Chinese developer documentation platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical agents use this skill to route search requests to specialized XiaoBenYang MCP tools and summarize returned search data or URLs for documentation, API reference, open-source project, and technical-community lookup tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key and can store it in a plaintext working-directory .env file.

Mitigation: Use a low-privilege, revocable key; avoid shared or source-controlled working directories; remove or rotate the key if it may have been exposed.

Risk: Search terms and prompts may be sent to the XiaoBenYang service.

Mitigation: Avoid proprietary, confidential, or secret search terms unless the service is approved for that data.

Risk: Server security evidence marked the release as suspicious due to plaintext credential storage and documentation inconsistencies.

Mitigation: Review the skill before installation and confirm credential-handling expectations with the publisher.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-smart-search)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API results, configuration guidance]

**Output Format:** [Markdown summaries of JSON API responses and generated search URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key before use.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
