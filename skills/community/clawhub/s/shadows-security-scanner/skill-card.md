## Description: <br>
Shadows Security Scanner guides agents through a seven-phase security audit covering reconnaissance, dependency checks, application and API review, hardening, secrets verification, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NakedoShadow](https://clawhub.ai/user/NakedoShadow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security reviewers, and release engineers use this skill to run an evidence-based repository security audit before production deployments, after incidents, or when sensitive code paths change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects repository source files, dependency manifests, and git history, so generated reports may expose sensitive project details or secret-like values. <br>
Mitigation: Run it only on intended repositories in a secure terminal and review reports before sharing them. <br>
Risk: Dependency audit phases may contact external vulnerability databases, and HTTP header checks may make an outbound request when a target URL is provided. <br>
Mitigation: Confirm that network access is acceptable for the environment and only provide target URLs that are in scope for the audit. <br>
Risk: Pattern-based checks can produce false positives or miss vulnerabilities outside the documented signatures. <br>
Mitigation: Treat findings as review inputs and complement them with dedicated SAST, SCA, DAST, and secrets-scanning tools where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NakedoShadow/shadows-security-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/NakedoShadow) <br>
- [ClawHub homepage from skill metadata](https://clawhub.ai/NakedoShadow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security audit report with command output summaries and findings tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only workflow; reports may include file paths, command output, vulnerability identifiers, and secret-like matches from the inspected repository.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
