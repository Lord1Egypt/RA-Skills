## Description: <br>
AI-powered accounting knowledge management. Search bookkeeping records, tax preparation documents, audit support files, and financial statement workpapers with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and accounting teams use this skill to search organizational accounting knowledge, retrieve context for bookkeeping, tax, audit, reconciliation, and financial statement questions, and identify relevant knowledge owners. It is intended to ground responses in UPLO knowledge sources with citations and classification-aware handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad organizational exports can expose sensitive bookkeeping, tax, audit, and financial statement information. <br>
Mitigation: Install only for a trusted UPLO instance with an accounting-scoped, least-privilege token, and require explicit user or admin approval before full organizational exports. <br>
Risk: Conversation logging can retain confidential financial context without clear controls. <br>
Mitigation: Define redaction, retention, access control, deletion, and audit rules before enabling conversation logging. <br>
Risk: Accounting or tax outputs may be mistaken for professional advice. <br>
Mitigation: Surface relevant workpapers and responsible knowledge owners, cite the source account, period, and document, and avoid presenting independent tax advice or accounting opinions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/RooJenkins/uplo-accounting) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>
- [UPLO Finance related skill](https://clawhub.com/skills/uplo-finance) <br>
- [UPLO Knowledge Management related skill](https://clawhub.com/skills/uplo-knowledge-management) <br>
- [UPLO Agriculture related skill](https://clawhub.com/skills/uplo-agriculture) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should cite UPLO sources, respect classification tiers, distinguish estimates from actuals, and avoid fabricating accounting information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
