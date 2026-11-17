## Description:

Build cinematic websites with templates, animated previews, complete build prompts, and editable UI and 3D components from VividSites. Requires a connected VividSites MCP server and a paid library account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krumjahn](https://clawhub.ai/user/krumjahn)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and designers use this skill to find and compare cinematic website designs, retrieve implementation prompts and editable components, and apply them to a requested site using their host's development tools. It requires VividSites MCP access and a paid library account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catalog access requires a connected MCP server, a personal API key, and paid library entitlement; missing access can prevent results.

Mitigation: Confirm connector setup and account entitlement before relying on catalog results, and report authentication or access errors accurately.

Risk: Retrieving premium prompts may use the account's existing daily allowance.

Mitigation: Consider quota use before requesting premium prompts and retrieve only the prompt needed for the selected design.

Risk: Retrieved prompts and component code may contain instructions, dependencies, or implementation details that need review before use.

Mitigation: Treat retrieved material as source material, review and adapt it to the requested work, and check dependencies before installation.

## Reference(s):

- [VividSites connector setup](https://github.com/krumjahn/vividsites-connectors)
- [VividSites MCP access](https://www.vividsites.app/mcp)
- [VividSites support](https://www.vividsites.app/support)
- [ClawHub skill release](https://clawhub.ai/krumjahn/skills/vividsites-library)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with code snippets and retrieved asset or prompt details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieved prompts retain their implementation instructions and supplied asset URLs; output depends on the requested design or component.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
