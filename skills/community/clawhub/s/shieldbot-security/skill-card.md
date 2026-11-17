## Description:

BNB Chain security scanner that scans contracts, simulates transactions, detects phishing, investigates deployers, tracks scam campaigns, and audits wallet approvals via ShieldBot's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ridwannurudeen](https://clawhub.ai/user/ridwannurudeen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and external users use this skill to check BNB Chain and supported EVM contracts, transactions, phishing URLs, deployers, scam campaigns, and wallet approvals before interacting with assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, URLs, transaction fields, and free-text questions are sent to ShieldBot or the configured API endpoint.

Mitigation: Do not submit private keys, seed phrases, confidential trading plans, unreleased transaction calldata, or sensitive personal details.

Risk: The skill depends on a Python package install and calls an external API.

Mitigation: Install it in an isolated environment, prefer pinned dependency versions, and review the configured API base URL before use.

Risk: Automated blockchain risk checks can be incomplete or misread as financial advice.

Mitigation: Review the returned risk verdicts, warnings, and raw details before acting, and treat scan output as security guidance rather than financial advice.

Risk: Public API calls are rate-limited.

Mitigation: Handle 429 responses and avoid high-volume automation that exceeds the documented 30 requests per minute limit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ridwannurudeen/skills/shieldbot-security)
- [ShieldBot Website](https://shieldbotsecurity.online)
- [ShieldBot API Reference](references/api-reference.md)
- [Supported Chains](references/chains.json)
- [Risk Flags](references/risk-flags.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and formatted plain-text security findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can output raw JSON when invoked with --raw; formatted responses lead with risk verdicts and classifications.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
