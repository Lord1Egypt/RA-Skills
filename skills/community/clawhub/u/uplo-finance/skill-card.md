## Description: <br>
AI-powered financial knowledge management. Search financial statements, audit findings, tax documents, and treasury records with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance employees use this skill to search organization-specific financial statements, audit materials, tax records, treasury policies, budgets, forecasts, and variance analyses through UPLO. It supports period-sensitive lookup, contextual finance search, directive retrieval, organizational context export, and finance documentation gap reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected MCP service can expose sensitive finance, audit, treasury, strategic, and organizational context. <br>
Mitigation: Install only for users authorized to view the connected records, use a least-privilege UPLO MCP token, and confirm classification-tier enforcement on the UPLO server. <br>
Risk: Financial records can be period-sensitive, privileged, draft, or subject to disclosure restrictions. <br>
Mitigation: Require outputs to cite the reporting period, document type, and preparation date, and avoid summarizing restricted projections, M&A data, executive compensation, or privileged materials unless access is explicitly permitted. <br>
Risk: Finance search results could be mistaken for financial advice. <br>
Mitigation: Use the skill to surface relevant documents and responsible finance owners rather than making financial recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-finance) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP-backed search guidance, finance document citations, responsible-owner lookup, and knowledge-gap reporting prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
