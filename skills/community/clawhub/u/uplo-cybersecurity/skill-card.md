## Description: <br>
AI-powered cybersecurity knowledge management. Search threat intelligence, vulnerability assessments, incident response plans, and compliance documentation with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams use this skill to search and synthesize threat intelligence, vulnerability assessments, incident response plans, security policies, and compliance evidence from an organization's UPLO knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and export sensitive organizational security information. <br>
Mitigation: Install only against a trusted UPLO instance, use a least-privilege UPLO token, confirm classification and clearance rules, and review organizational-context exports before sharing them. <br>
Risk: Incident, vulnerability, and compliance details may be sensitive when logged or surfaced to users. <br>
Mitigation: Be deliberate about logging sensitive security details and verify user clearance before disclosing restricted cybersecurity information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-cybersecurity) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query and export sensitive cybersecurity knowledge according to the connected UPLO instance, token permissions, and classification rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
