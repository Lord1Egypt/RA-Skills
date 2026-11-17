## Description:

Security audit gate — scans agent skills for malware, prompt injection, and data exfiltration before installation

This skill is ready for commercial/non-commercial use.

## Publisher:

[alikayhan](https://clawhub.ai/user/alikayhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Safuclaw before installing third-party skills to audit skill contents and bundled files for malware, prompt injection, data exfiltration, and related supply-chain risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Safuclaw uploads full skill contents and bundled files to an external paid audit service.

Mitigation: Review the file manifest before auditing and exclude directories that may contain secrets, private keys, .env files, proprietary code, or unrelated personal data.

Risk: The remote audit result can strongly influence or block skill installation decisions.

Mitigation: Use Safuclaw as one security signal and require explicit user confirmation before proceeding when verification is unavailable or the result is not acceptable.

Risk: Audits require a 0.99 USDC x402 payment on Base.

Mitigation: Confirm the user is comfortable with the payment requirement and wallet funding flow before attempting an audit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alikayhan/skills/safuclaw)
- [Publisher profile](https://clawhub.ai/user/alikayhan)
- [Safuclaw homepage](https://safuclaw.com)
- [Safuclaw API endpoint](https://api.safuclaw.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with HTTP examples, JSON request and response shapes, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable Safuclaw API and x402 payment flow for paid audits.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
