## Description: <br>
AI-powered environmental knowledge management. Search impact assessments, compliance monitoring data, sustainability reports, and environmental permits with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, environmental managers, compliance officers, sustainability teams, and legal counsel use this skill to search organizational environmental records, permits, monitoring data, ESG metrics, and impact assessment materials for grounded environmental compliance and sustainability answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an external MCP package to an API key and can access environmental organizational knowledge. <br>
Mitigation: Use a dedicated least-privileged UPLO token, confirm the npm package and UPLO server URL are trusted, and restrict access to the intended environmental pack. <br>
Risk: Broad organizational export and knowledge-base change actions could expose sensitive records or alter organizational knowledge without adequate review. <br>
Mitigation: Require explicit approval before exporting organizational context or writing knowledge-base updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-environmental) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with environmental findings, citations to organizational records when available, inline MCP tool calls, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include permit numbers, regulatory programs, compliance periods, monitoring methods, applicable limits, trends, benchmarks, and responsible knowledge owners when supported by the connected knowledge base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
