## Description: <br>
Generates concise company and organization research reports from Qibook enterprise data, selecting templates by entity type and turning multi-dimensional business data into structured Markdown analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinadaas-department](https://clawhub.ai/user/chinadaas-department) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business researchers, analysts, legal professionals, financial users, and enterprise counterparties use this skill to request a company, branch, hospital, school, law firm, government entity, or other organization report from a company name. It is suited for company background research, credit-oriented analysis, business due diligence, and structured enterprise insight reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried organization names are sent to the configured QIBOOK service using the user's API key. <br>
Mitigation: Use only with an approved QIBOOK endpoint, validate or lock down QIBOOK_BASE_URL, and require explicit confirmation before external lookups for ambiguous requests. <br>
Risk: Report templates include instructions that conceal AI authorship. <br>
Mitigation: Remove or revise those instructions before customer-facing, legal, credit, investment, or compliance use. <br>
Risk: Generated reports may be incomplete or misleading if the external data is sparse, stale, or unavailable. <br>
Mitigation: Require human review and source validation before relying on the output for customer-facing, legal, credit, investment, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinadaas-department/qibook-company-wiki-deepresearch) <br>
- [Publisher profile](https://clawhub.ai/user/chinadaas-department) <br>
- [Qibook credential setup](https://skill.qibook.com) <br>
- [Sample company report](examples/sample_company_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with setup guidance and structured error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Selects templates by entity type and applies documented word limits based on input data size.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
