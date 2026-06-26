## Description: <br>
Scan any URL, skill, or infrastructure for security vulnerabilities using the ZOO Security Scanner API with x402 payment in USDC and no API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crazycompanyinc](https://clawhub.ai/user/crazycompanyinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to request security scans of URLs, skills, or infrastructure and interpret returned findings, scores, and recommendations. It is intended for authorized scanning workflows that may involve paid third-party API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send scan targets to ZOO Technologies. <br>
Mitigation: Use it only for targets you own or are authorized to test, and avoid submitting sensitive internal targets without approval. <br>
Risk: The skill can trigger USDC payments through x402. <br>
Mitigation: Require explicit human approval before each scan or payment and verify current pricing before use. <br>
Risk: Security scan results may be incomplete or require interpretation. <br>
Mitigation: Review findings before acting on them and use additional validation for high-impact remediation decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/crazycompanyinc/zoo-security-scanner) <br>
- [ZOO Technologies](https://zootechnologies.com) <br>
- [x402 Discovery](https://xgate.run) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown with curl examples and JSON scan responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan results include status, score, findings, and recommendations when returned by the third-party API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
