## Description: <br>
AI-powered hospitality knowledge management. Search guest service standards, property procedures, F&B operations, and event planning documentation with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hospitality operators, property teams, and managers use this skill to search property-specific service standards, operating procedures, food and beverage documentation, event planning materials, and escalation guidance through an UPLO-backed knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad organizational exports can expose internal hospitality procedures, revenue strategy, vendor pricing, or other sensitive operational data. <br>
Mitigation: Use a least-privilege UPLO token scoped to the intended hospitality pack, property, and role, and require explicit approval before full organizational exports. <br>
Risk: Guest service recovery workflows may include guest identifiers, compensation details, or other sensitive incident information. <br>
Mitigation: Redact guest identifiers, compensation details, revenue strategy, and vendor or pricing information before logging or sharing results. <br>
Risk: The skill depends on an external MCP package and UPLO instance for knowledge access. <br>
Mitigation: Install only when the publisher, UPLO instance, MCP package, and configured API token are trusted for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-hospitality) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>
- [README](artifact/README.md) <br>
- [Identity patch](artifact/identity-patch.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include hospitality procedure summaries, contextual search guidance, MCP tool calls, and operational decision logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
