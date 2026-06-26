## Description: <br>
Call 2000+ tools via curl, zero installation. Supports tool-level semantic search - get full inputSchema in one step and invoke directly. Covers search, dev, docs, finance, maps, travel, AI media, social, productivity, enterprise, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxyd-ai](https://clawhub.ai/user/lxyd-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with MCPMarket, search available remote tools, inspect input schemas, and invoke selected tools through documented curl calls. It also supports browsing categories, checking credits, fetching skills, and submitting ratings after successful use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a broad remote tool gateway that can invoke account-linked services. <br>
Mitigation: Confirm the selected tool, arguments, and intended side effects with the user before posts, purchases, deletions, financial actions, business changes, or other consequential calls. <br>
Risk: The workflow stores a persistent MCPMarket access token in ~/.uno/token. <br>
Mitigation: Use restrictive file permissions, remove ~/.uno/token when finished, and separately revoke any linked downstream service access in MCPMarket or the connected service. <br>
Risk: Some downstream services may require OAuth linking through MCPMarket before use. <br>
Mitigation: Show the user the exact authorization URL from the service response, require explicit approval before linking, and retry the original call only after authorization is complete. <br>
Risk: The skill can fetch untrusted remote skill content and submit ratings that affect ranking. <br>
Mitigation: Review fetched skill content before loading or following it, and ask for confirmation before submitting tool or skill ratings. <br>


## Reference(s): <br>
- [ClawHub listing for uno](https://clawhub.ai/lxyd-ai/uno) <br>
- [MCPMarket homepage](https://mcpmarket.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local bearer token file at ~/.uno/token and returns remote API responses that may contain nested JSON strings.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
