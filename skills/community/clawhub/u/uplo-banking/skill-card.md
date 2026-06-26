## Description: <br>
AI-powered banking knowledge management. Search KYC records, regulatory reports, risk assessments, and loan processing documentation with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Banking employees, compliance teams, risk managers, and developers use this skill to query institution-specific KYC/AML records, regulatory reports, risk assessments, loan documentation, directives, and subject matter experts through UPLO-backed MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access highly sensitive banking, KYC, AML, regulatory, customer, and examination materials. <br>
Mitigation: Deploy only in a controlled banking environment with verified role-based access and least-privilege UPLO MCP tokens. <br>
Risk: Full organizational context export can expose broad internal knowledge and sensitive records. <br>
Mitigation: Restrict or disable full context export unless an administrator explicitly requires it and access controls are reviewed. <br>
Risk: Conversation logging can retain sensitive customer, compliance, or regulatory information. <br>
Mitigation: Require opt-in logging with redaction, access controls, and retention limits before using real customer or compliance data. <br>
Risk: Banking compliance outputs may be misused if unsupported by source material or if restricted information such as SAR existence is disclosed. <br>
Mitigation: Require cited UPLO sources, respect classification tiers, avoid guessing when information is unavailable, and never confirm or deny the existence of a SAR. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RooJenkins/uplo-banking) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO Schemas](https://uplo.ai/schemas) <br>
- [UPLO Knowledge Management](https://clawhub.com/skills/uplo-knowledge-management) <br>
- [UPLO Risk Management](https://clawhub.com/skills/uplo-risk-management) <br>
- [UPLO Accounting](https://clawhub.com/skills/uplo-accounting) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should cite UPLO sources, respect classification tiers, mask sensitive customer identifiers where appropriate, and state when the knowledge base lacks an answer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
