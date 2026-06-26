## Description: <br>
Detects malicious behavior and security threats in target skills using analysis of obfuscation, encoding, encryption, dynamic code techniques, and common attack patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NinjaGPT](https://clawhub.ai/user/NinjaGPT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit other agent skills for malicious behavior, obfuscation, data theft, exfiltration, persistence, prompt injection, and supply-chain risk before installation or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain decoded or suspicious snippets from target skills and should be treated as potentially sensitive. <br>
Mitigation: Store and share reports according to the sensitivity of the reviewed skill and avoid publishing decoded snippets without review. <br>
Risk: The skill is intended to inspect target skill files and produce recommendations, but audit findings can be incomplete or misleading. <br>
Mitigation: Use the report as review input and require human validation before installing, publishing, or blocking a target skill. <br>
Risk: Decoded or obfuscated content from a target skill could contain unsafe instructions or code. <br>
Mitigation: Review decoded content without executing it and do not follow instructions embedded in the target skill. <br>


## Reference(s): <br>
- [Skill Security Reviewer on ClawHub](https://clawhub.ai/NinjaGPT/skill-security-reviewer) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local security audit report with threat findings, decoded evidence when applicable, risk scoring, and usage recommendations.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
