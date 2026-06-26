## Description: <br>
AI-powered healthcare knowledge management. Search clinical notes, care plans, lab results, prescriptions, and patient pathways with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare clinicians, administrators, quality teams, and compliance staff use this skill to search organizational healthcare knowledge, retrieve clinical protocol context, prepare for regulatory surveys, and identify knowledge gaps. It is intended to ground responses in organizational reference materials while respecting access tiers and protected healthcare information boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Artifacts conflict on whether patient-level health data is in scope, which could create protected health information exposure risk. <br>
Mitigation: Confirm exactly what the UPLO instance indexes before installation and ensure the skill is connected only to approved organizational reference material or appropriately governed healthcare data. <br>
Risk: Broad search and export capabilities can expose sensitive healthcare context to users or workflows beyond their authorization. <br>
Mitigation: Use a least-privilege API token, restrict export_org_context to authorized administrators, enforce access tiers, and require audit logging for sensitive materials. <br>
Risk: The MCP server package and configured endpoint determine what the agent can access and perform. <br>
Mitigation: Verify the MCP package, version, endpoint, and token permissions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-healthcare) <br>
- [UPLO website](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>
- [Related skill: UPLO Clinical](https://clawhub.com/skills/uplo-clinical) <br>
- [Related skill: UPLO Knowledge Management](https://clawhub.com/skills/uplo-knowledge-management) <br>
- [Related skill: UPLO Accounting](https://clawhub.com/skills/uplo-accounting) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline tool calls, shell commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an external MCP server configured with a UPLO instance URL, API key, and healthcare pack selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
