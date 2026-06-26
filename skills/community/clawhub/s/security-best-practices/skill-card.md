## Description: <br>
Review code with secure-by-default standards, prioritize exploitable risks, and deliver minimal-diff fixes with evidence and regression checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to request evidence-backed security reviews, hardening guidance, prioritized findings, and minimal-risk remediation plans for codebases and workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project-specific security findings, preferences, and accepted-risk notes may be stored locally if memory is enabled. <br>
Mitigation: Ask for consent before creating ~/security-best-practices/, decide what may be stored there, and avoid storing secrets. <br>
Risk: Security guidance can be misleading if findings are speculative or lack repository evidence. <br>
Mitigation: Require concrete scope, file and line evidence, severity rationale, and verification checks before presenting findings as actionable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/security-best-practices) <br>
- [Skill Homepage](https://clawic.com/skills/security-best-practices) <br>
- [Setup](artifact/setup.md) <br>
- [Review Playbook](artifact/review-playbook.md) <br>
- [Severity Model](artifact/severity-model.md) <br>
- [Remediation Patterns](artifact/remediation-patterns.md) <br>
- [Memory Template](artifact/memory-template.md) <br>
- [Risk Exceptions](artifact/exceptions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown security reports, prioritized findings, remediation plans, optional code changes, shell commands, and local memory templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local notes under ~/security-best-practices/ only after user consent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
