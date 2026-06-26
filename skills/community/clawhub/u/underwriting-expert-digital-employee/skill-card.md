## Description: <br>
Covers health review, medical assessment, underwriting conclusion interpretation, follow-up, and dual-recording quality checks to help underwriting personnel evaluate health risk more accurately and efficiently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance underwriting staff use this skill to structure health reviews, medical risk assessments, underwriting decision explanations, customer follow-up, and dual-recording quality checks. Outputs are advisory and require qualified human review before operational use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill addresses regulated insurance operations and may handle sensitive customer, health, financial, audio, or identity data. <br>
Mitigation: Use only in explicitly permissioned environments; minimize and mask sensitive data, enforce access controls, and retain encrypted audit logs according to policy. <br>
Risk: The artifact declares no tools, storage, network access, or PII handling while its workflows describe MCP tools, customer contact, OCR/ASR processing, and audit logging. <br>
Mitigation: Treat all tool use and customer contact as disabled unless separately configured, approved, logged, and reviewed by authorized personnel. <br>
Risk: Underwriting conclusions, notices, and quality findings may affect customers if used without expert oversight. <br>
Mitigation: Require qualified human approval before applying outputs to underwriting decisions, customer communications, compliance findings, or follow-up actions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown reports, structured checklists, risk assessments, decision explanations, and customer-facing notice drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory outputs for regulated insurance workflows; human review is required before use with customers or policy decisions.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
