## Description: <br>
Security Defense Line 安全防线 helps agents provide digital-asset security guidance across smart contract review, wallet checks, transaction risk review, phishing detection, multisig planning, and incident response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and digital-asset operators use this skill to request structured guidance for contract auditing, wallet hygiene, transaction review, phishing checks, multisig operations, and incident response. It should be treated as an assistant for security review workflows rather than a source of final asset-safety decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because the skill presents mock or random digital-asset safety checks as usable protection. <br>
Mitigation: Do not rely on its risk scores, audit reports, transaction simulations, or multisig state changes for real asset decisions; require independent review and trusted security tooling before acting. <br>
Risk: The skill includes a paid billing flow that sends a user identifier to skillpay.me. <br>
Mitigation: Use the billing flow only when users understand the payment requirement and are comfortable sharing the required user identifier with the billing provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-defense-line) <br>
- [Publisher profile](https://clawhub.ai/user/shenmeng) <br>
- [Contract auditing reference](artifact/references/contract-auditing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, command examples, configuration snippets, and structured review notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include security checklists, risk summaries, audit-style findings, remediation suggestions, and incident-response steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
