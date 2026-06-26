## Description: <br>
AI-powered insurance knowledge management. Search policy documents, claims records, underwriting guidelines, and actuarial data with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance employees use this skill to search organization-specific policy forms, claims records, underwriting guidelines, actuarial data, reinsurance terms, and regulatory filing materials. It supports grounded retrieval, contextual GraphRAG queries, directive review, owner lookup, and outdated-knowledge flagging for underwriting, claims, compliance, actuarial, and producer workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects through an external MCP server with access to sensitive insurance context and export-style tools. <br>
Mitigation: Review the UPLO tenant and token scope, use a dedicated least-privilege token, restrict accessible packs and classification tiers, and require human approval before full organization exports. <br>
Risk: The MCP server package is installed through an unpinned npx command. <br>
Mitigation: Pin or verify the MCP server package provenance before installation. <br>
Risk: Actions that change shared knowledge-base state can affect downstream insurance guidance. <br>
Mitigation: Require review before using update, proposal, stale-entry, or knowledge-gap workflows that modify or influence shared knowledge-base content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-insurance) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline tool calls, shell commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured UPLO MCP access and should respect classification tiers for sensitive insurance data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
