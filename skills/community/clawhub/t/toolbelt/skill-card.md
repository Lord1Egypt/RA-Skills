## Description: <br>
Toolbelt helps agents ingest documents, extract entities and relationships, query structured and unstructured data through one MCP server, and share a persistent workspace across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toolbeltai](https://clawhub.ai/user/toolbeltai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Toolbelt when a task needs persistent memory, natural-language access to structured and unstructured data, or collaboration across agents through a shared MCP workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Toolbelt stores workspace data and findings that users choose to upload, save, or share. <br>
Mitigation: Ask before uploading or recording data, avoid sensitive material by default, and direct users to app.toolbelt.ai for deletion or account controls. <br>
Risk: The bearer token and share URLs grant access to a Toolbelt namespace. <br>
Mitigation: Store tokens only in the MCP client config after explicit consent, avoid echoing full tokens, and tell users how to revoke access by deleting the config entry or using the web UI. <br>
Risk: The skill can trigger network setup requests and local MCP configuration writes. <br>
Mitigation: Require explicit user approval before each network request or filesystem write, and stop with manual setup guidance if the user declines. <br>


## Reference(s): <br>
- [Toolbelt homepage](https://toolbelt.ai) <br>
- [Toolbelt documentation](https://toolbelt.ai/docs) <br>
- [ClawHub Toolbelt release](https://clawhub.ai/toolbeltai/toolbelt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP, JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP client configuration snippets and connection status YAML; setup actions require explicit user consent.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
