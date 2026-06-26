## Description: <br>
AI-powered logistics knowledge management for searching shipment records, warehouse procedures, fleet data, and customs documentation with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Logistics, warehouse, trade compliance, and carrier operations teams use this skill to query organization-specific shipment records, procedures, contracts, fleet data, and customs documentation. It helps agents retrieve grounded operational context, prepare carrier reviews, support customs audits, and flag stale logistics knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exports may include sensitive customer, shipment, pricing, customs, credential, or confidential business data. <br>
Mitigation: Send exports only to authorized recipients and confirm classification and access controls before sharing. <br>
Risk: Conversation logging can preserve sensitive operational or trade compliance details. <br>
Mitigation: Use logging only when approved, make it optional where possible, and exclude sensitive or confidential data from logged conversations. <br>
Risk: Logistics records, rate sheets, carrier contracts, or warehouse procedures can become stale. <br>
Mitigation: Flag outdated entries and verify conflicting operational guidance against the current authoritative source before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-logistics) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline tool calls, shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured UPLO MCP access and should only surface information available in the connected knowledge base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
