## Description: <br>
Triage security and virus scanner findings for skills and automations, separating confirmed risks from false positives and producing prioritized remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okikesolutions](https://clawhub.ai/user/okikesolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to convert scanner findings into a claim map, evidence-backed risk ranking, remediation plan, and re-scan checklist for skill or automation releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Triage output could misclassify scanner findings or encourage unsafe remediation if accepted without review. <br>
Mitigation: Review the generated evidence map, risk ranking, patch plan, and re-scan checklist before applying changes or approving a release. <br>
Risk: Scanner evidence may include sensitive configuration context. <br>
Mitigation: Follow the skill guardrail to avoid leaking secrets from .env files and keep data-routing transparency findings separate from security-impact findings. <br>


## Reference(s): <br>
- [Security Triage Output Template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown structured as scanner claim map, evidence, risk ranking, patch plan, data-routing assessment, and re-scan checklist.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No hidden scripts or persistence; outputs are reviewer-facing triage guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
