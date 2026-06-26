## Description: <br>
Runs a structured, 1,000-iteration deep security audit covering OWASP, authentication, infrastructure, supply chain, compliance, business logic, and final reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorukardahan](https://clawhub.ai/user/dorukardahan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security engineers, and release owners use this skill to perform authorized deep security reviews before major releases, during compliance preparation, or after security incidents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may inspect sensitive project details and produce reports that include vulnerabilities, environment details, or secret locations. <br>
Mitigation: Run it only on systems the user is authorized to audit, set scope before execution, and keep .ralph-report.md private. <br>
Risk: Active probing during a security review can affect target systems if it is run without approval. <br>
Mitigation: Require explicit approval before active probing and keep checks within the agreed audit scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dorukardahan/ralph-ultra) <br>
- [Severity and triage guidance](references/severity-guide.md) <br>
- [Expert persona descriptions](references/personas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with structured per-iteration audit findings and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write .ralph-report.md checkpoints and a final audit report.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
