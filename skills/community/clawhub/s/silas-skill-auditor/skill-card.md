## Description: <br>
A skill-auditing checklist that helps agents review installed or remote skills for code security, permission risks, data leakage, and content compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aohoyo](https://clawhub.ai/user/aohoyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill before or after installing another skill to structure a security review, inspect risky file patterns, score findings, and produce a markdown audit report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release declares wallet and sensitive-credential capabilities even though the security evidence describes this as a checklist with no executable payload. <br>
Mitigation: Do not grant wallet, credential, or broad profile access unless the publisher provides a corrected package that clearly justifies those capabilities. <br>
Risk: Audit reports and scores may be incomplete or misleading if the wrong skill name or temporary path is reviewed. <br>
Mitigation: Confirm the target skill name and temporary path before running review commands, and treat results as a checklist that still requires human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aohoyo/silas-skill-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/aohoyo) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs checklist-style security findings, scores, and recommendations; it does not include an executable payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
