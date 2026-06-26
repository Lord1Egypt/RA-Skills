## Description: <br>
Scans BNB Chain and EVM contracts, transactions, deployers, URLs, campaigns, and wallet approvals using ShieldBot's public security API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ridwannurudeen](https://clawhub.ai/user/Ridwannurudeen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and external users use this skill to inspect blockchain contracts, pending transactions, deployer histories, phishing URLs, scam campaigns, and wallet approvals before interacting with BNB Chain or supported EVM networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends wallet addresses, transaction details, URLs, and free-text security questions to ShieldBot's public API. <br>
Mitigation: Use only data you are comfortable sharing with ShieldBot, and do not submit seed phrases, private keys, passwords, internal-only links, or unreleased transaction plans. <br>
Risk: Automated blockchain scans and approval recommendations can be incomplete or misleading. <br>
Mitigation: Review the returned analysis independently and inspect any unsigned revoke or transaction request before signing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ridwannurudeen/shieldbot-security) <br>
- [ShieldBot Website](https://shieldbotsecurity.online) <br>
- [ShieldBot API Reference](artifact/references/api-reference.md) <br>
- [Supported Chains](artifact/references/chains.json) <br>
- [Risk Flags](artifact/references/risk-flags.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-formatted security summaries and shell commands, with optional raw JSON from the ShieldBot API client.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided blockchain addresses, transaction details, URLs, and questions; no API key is required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
