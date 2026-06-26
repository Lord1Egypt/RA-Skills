## Description: <br>
AI-powered legal knowledge management. Search contracts, compliance requirements, legal cases, and policy documents with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal, compliance, and operations teams use this skill to search organizational contracts, compliance documents, cases, policies, and legal memoranda, then surface cited internal knowledge and responsible knowledge owners. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents broad access to sensitive legal context. <br>
Mitigation: Use a least-privilege legal-only token, restrict access to the approved UPLO host, and preserve classification boundaries for confidential or restricted records. <br>
Risk: The skill can export full organizational context or log conversation summaries. <br>
Mitigation: Require explicit approval before context export or conversation logging, especially for privileged, regulated, investigation-related, or confidential legal work. <br>
Risk: The MCP server package and UPLO instance become trusted execution and data-access dependencies. <br>
Mitigation: Install only from a trusted UPLO instance, prefer a pinned MCP server version, and review package updates before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RooJenkins/uplo-legal) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO Schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cited legal knowledge, GraphRAG context, organizational context exports, directives, knowledge-owner lookups, and conversation summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
