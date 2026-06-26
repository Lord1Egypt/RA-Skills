## Description: <br>
AI-powered food safety knowledge management. Search HACCP plans, FDA compliance records, traceability documentation, and quality control data with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Food safety, QA, and compliance teams use this skill to search organization-specific HACCP, FDA/USDA compliance, supplier, sanitation, allergen, and traceability records during audits, recalls, inspections, and quality investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad organizational food-safety context could be exposed through full-context export or overly broad access. <br>
Mitigation: Use a UPLO token limited to the intended food-safety data and require explicit approval before exporting broad context. <br>
Risk: Sensitive compliance discussions may include suppliers, formulations, recalls, regulatory issues, or incident response details. <br>
Mitigation: Require explicit approval before logging these conversations and redact details that are not needed for the audit trail. <br>
Risk: Food-safety answers can affect audits, recalls, and regulatory decisions. <br>
Mitigation: Ground answers in the connected knowledge base, cite source records, and route consequential decisions through qualified food-safety or regulatory reviewers. <br>
Risk: The skill runs an external MCP package. <br>
Mitigation: Verify the MCP package and version before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-food-safety) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline tool calls, shell command examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an UPLO instance URL and MCP token; responses should remain grounded in the connected food-safety knowledge base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
